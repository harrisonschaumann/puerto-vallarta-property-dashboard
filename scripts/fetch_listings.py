#!/usr/bin/env python3
import datetime
import json
import os
import re
import urllib.request

SOURCES = [
    {"name": "PVRPV Real Estate", "url": "https://pvrpv.com/realestate/"},
    {"name": "Kim Kieler Sold Listings", "url": "https://kimkieler.net/homepage/sold-listings/"},
    {"name": "Mexico Life Realty Blog", "url": "https://mexicolife.com/blog/"},
    {"name": "Point2 Puerto Vallarta", "url": "https://www.point2homes.com/MX/Real-Estate-Listings/Jalisco/Puerto-Vallarta.html"},
]


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
            "dataLabel": "Reported Sold / Recently Listed",
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
            "dataLabel": "Reported Sold / Recently Listed",
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

            rows.append(
                {
                    "propertyType": infer_type(title),
                    "location": "Puerto Vallarta, Jalisco, Mexico",
                    "neighborhood": "",
                    "salePriceUsd": None,
                    "saleDate": "",
                    "overview": title,
                    "sourceName": source["name"],
                    "sourceUrl": url,
                    "dataLabel": "Reported Sold / Recently Listed",
                }
            )
            if len(rows) >= 40:
                return rows

    return rows


listings = build_records()
if not listings and os.path.exists("data/latest.json"):
    with open("data/latest.json", encoding="utf-8") as f:
        current = json.load(f)
    listings = current.get("listings", [])

if not listings:
    listings = sample_listings()

payload = {
    "lastUpdated": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "dataMode": "sample",
    "listings": listings,
}

with open("data/latest.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)

print(f"Wrote {len(listings)} listings")
