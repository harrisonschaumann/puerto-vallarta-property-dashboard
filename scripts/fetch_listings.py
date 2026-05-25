#!/usr/bin/env python3
import datetime
import json
import os
import re
import urllib.request
from collections import Counter
from statistics import median

SOURCES = [
    {"name": "PVRPV Real Estate", "url": "https://pvrpv.com/realestate/"},
    {"name": "Kim Kieler Sold Listings", "url": "https://kimkieler.net/homepage/sold-listings/"},
    {"name": "Mexico Life Realty Blog", "url": "https://mexicolife.com/blog/"},
    {"name": "Point2 Puerto Vallarta", "url": "https://www.point2homes.com/MX/Real-Estate-Listings/Jalisco/Puerto-Vallarta.html"},
]

LATEST_PATH = "data/latest.json"
HISTORY_PATH = "data/history.json"


def get(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", "ignore")


def infer_type(text: str) -> str:
    lowered = text.lower()
    if re.search(r"land|lote|lot", lowered):
        return "Land"
    if re.search(r"house|casa|villa", lowered):
        return "House"
    if re.search(r"apartment", lowered):
        return "Apartment"
    return "Condo"


def confidence_label(overview: str, source_name: str) -> str:
    content = f"{overview} {source_name}".lower()
    if "sold" in content:
        return "Reported Sold"
    if "listing" in content or "for sale" in content:
        return "Recently Listed"
    return "Unknown"


def listing_id(row: dict) -> str:
    seed = f"{row.get('sourceName', '')}|{row.get('sourceUrl', '')}|{row.get('overview', '')[:120]}"
    return re.sub(r"\s+", "-", seed.strip().lower())


def sample_listings() -> list[dict]:
    return [
        {
            "propertyType": "Condo",
            "location": "Zona Romántica, Puerto Vallarta, Jalisco",
            "neighborhood": "Zona Romántica",
            "salePriceUsd": 495000,
            "saleDate": "",
            "overview": "Sample record used when live sold-property fields are not consistently public.",
            "sourceName": "Sample Dataset",
            "sourceUrl": "https://github.com/",
            "confidence": "Unknown",
        },
        {
            "propertyType": "House",
            "location": "Marina Vallarta, Puerto Vallarta, Jalisco",
            "neighborhood": "Marina Vallarta",
            "salePriceUsd": 820000,
            "saleDate": "",
            "overview": "Sample house entry representing broker-reported market activity.",
            "sourceName": "Sample Dataset",
            "sourceUrl": "https://github.com/",
            "confidence": "Unknown",
        },
    ]


def build_records() -> list[dict]:
    rows = []
    for source in SOURCES:
        try:
            html = get(source["url"])
        except Exception:
            continue

        for match in re.finditer(r"href=[\"\'](https?://[^\"\']+)[\"\'][^>]*>([^<]{12,130})<", html, re.I):
            url = match.group(1)
            title = re.sub(r"\s+", " ", match.group(2)).strip()
            if "vallarta" not in (title + html[:12000]).lower():
                continue

            row = {
                "propertyType": infer_type(title),
                "location": "Puerto Vallarta, Jalisco, Mexico",
                "neighborhood": "",
                "salePriceUsd": None,
                "saleDate": "",
                "overview": title,
                "sourceName": source["name"],
                "sourceUrl": url,
                "confidence": confidence_label(title, source["name"]),
            }
            row["id"] = listing_id(row)
            rows.append(row)
            if len(rows) >= 60:
                return rows

    return rows


def summarize(listings: list[dict], changes: dict) -> str:
    if not listings:
        return "No listing data is currently available."
    prices = [r["salePriceUsd"] for r in listings if isinstance(r.get("salePriceUsd"), (int, float))]
    med = int(median(prices)) if prices else None
    type_mix = Counter(r.get("propertyType", "Unknown") for r in listings)
    common = ", ".join([f"{k} ({v})" for k, v in type_mix.most_common(3)])
    med_text = f"Median visible price is about ${med:,.0f}." if med else "Public price coverage is limited."
    return (
        f"Market pulse: {changes['new']} new, {changes['changed']} changed, and {changes['removed']} removed listings since yesterday. "
        f"Inventory sample size is {len(listings)}. {med_text} Most common property types: {common}."
    )


def load_json(path: str, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def detect_changes(old: list[dict], new: list[dict]) -> dict:
    old_map = {x.get("id") or listing_id(x): x for x in old}
    new_map = {x.get("id") or listing_id(x): x for x in new}
    new_ids = set(new_map) - set(old_map)
    removed_ids = set(old_map) - set(new_map)
    changed = []
    for lid in set(new_map).intersection(old_map):
        if json.dumps(new_map[lid], sort_keys=True) != json.dumps(old_map[lid], sort_keys=True):
            changed.append(lid)
    return {
        "new": len(new_ids),
        "removed": len(removed_ids),
        "changed": len(changed),
        "newIds": sorted(new_ids),
        "removedIds": sorted(removed_ids),
        "changedIds": sorted(changed),
    }


now = datetime.datetime.now(datetime.UTC).replace(microsecond=0)
existing_latest = load_json(LATEST_PATH, {})
existing_listings = existing_latest.get("listings", [])

listings = build_records()
if not listings:
    listings = existing_listings or sample_listings()

for row in listings:
    row.setdefault("id", listing_id(row))
    row.setdefault("confidence", "Unknown")

changes = detect_changes(existing_listings, listings)
market_summary = summarize(listings, changes)

payload = {
    "lastUpdated": now.isoformat().replace("+00:00", "Z"),
    "lastUpdatedLocal": now.astimezone(datetime.timezone(datetime.timedelta(hours=-6))).strftime("%Y-%m-%d %H:%M UTC-06:00"),
    "dataMode": "reported_public_sources",
    "newSinceYesterday": changes["new"],
    "changeSummary": changes,
    "marketSummary": market_summary,
    "listings": listings,
}

with open(LATEST_PATH, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)

history = load_json(HISTORY_PATH, {"history": []})
history.setdefault("history", []).append(
    {
        "runAt": payload["lastUpdated"],
        "listingCount": len(listings),
        "new": changes["new"],
        "changed": changes["changed"],
        "removed": changes["removed"],
        "marketSummary": market_summary,
        "listings": listings,
    }
)
history["history"] = history["history"][-90:]
with open(HISTORY_PATH, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

print(f"Wrote {len(listings)} listings | +{changes['new']} ~{changes['changed']} -{changes['removed']}")
