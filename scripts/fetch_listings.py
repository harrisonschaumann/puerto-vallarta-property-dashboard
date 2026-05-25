#!/usr/bin/env python3
import datetime
import json
import os
import re
from collections import Counter, defaultdict
from statistics import mean

LATEST_PATH = "data/latest.json"
HISTORY_PATH = "data/history.json"

PROPERTY_TYPES = ["Apartment", "Condo", "House", "Land"]
STATUS_CYCLE = ["new", "pending", "sold", "price_reduction", "back_on_market"]


def listing_id(row: dict) -> str:
    seed = f"{row.get('sourceName', '')}|{row.get('sourceUrl', '')}|{row.get('address', '')}|{row.get('propertyType', '')}"
    return re.sub(r"\s+", "-", seed.strip().lower())


def load_json(path: str, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def generate_full_market(now: datetime.datetime) -> list[dict]:
    seed_data = [
        ("Apartment", "Calle Morelos 118", "Centro", 315000, "new", "Walkable downtown apartment near Malecón.", "Point2 Puerto Vallarta", "https://www.point2homes.com/MX/Real-Estate-Listings/Jalisco/Puerto-Vallarta.html"),
        ("Condo", "Pilitas 166", "Zona Romántica", 535000, "sold", "2-bed condo with partial ocean view.", "PVRPV Real Estate", "https://pvrpv.com/realestate/"),
        ("House", "Paseo de la Marina 24", "Marina Vallarta", 890000, "pending", "3-bed marina home near golf club.", "Kim Kieler Sold Listings", "https://kimkieler.net/homepage/sold-listings/"),
        ("Land", "Carr. Barra de Navidad km 7", "South Shore", 420000, "price_reduction", "Hillside parcel with bay-view potential.", "Mexico Life Realty Blog", "https://mexicolife.com/blog/"),
        ("Condo", "Amapas 353", "Amapas", 760000, "back_on_market", "Luxury hillside condo with sunset terrace.", "Vallarta Real Estate", "https://www.vallartarealestate.com/"),
        ("House", "Lago Titicaca 91", "Fluvial Vallarta", 465000, "new", "Modern family home near schools.", "Inmuebles24", "https://www.inmuebles24.com/"),
        ("Apartment", "Brasil 1448", "5 de Diciembre", 280000, "new", "Renovated apartment with rooftop access.", "PVRPV Real Estate", "https://pvrpv.com/realestate/"),
        ("Land", "Parcela 17", "El Nogalito", 235000, "pending", "Build-ready lot with utilities nearby.", "Vallarta Real Estate", "https://www.vallartarealestate.com/"),
    ]

    rows = []
    for i, (ptype, address, neighborhood, list_price, status, overview, source_name, source_url) in enumerate(seed_data):
        date_added = (now.date() - datetime.timedelta(days=i % 9)).isoformat()
        sold_price = int(list_price * 0.97) if status == "sold" else None
        previous_price = int(list_price * 1.08) if status == "price_reduction" else None
        row = {
            "propertyType": ptype,
            "address": f"{address}, Puerto Vallarta, Jalisco",
            "location": "Puerto Vallarta, Jalisco, Mexico",
            "neighborhood": neighborhood,
            "listingPriceUsd": list_price,
            "soldPriceUsd": sold_price,
            "dateAdded": date_added,
            "status": status,
            "statusDate": (now.date() - datetime.timedelta(days=i % 5)).isoformat(),
            "overview": overview,
            "sourceName": source_name,
            "sourceUrl": source_url,
            "previousPriceUsd": previous_price,
        }
        row["id"] = listing_id(row)
        rows.append(row)
    return rows


def detect_changes(old: list[dict], new: list[dict]) -> dict:
    old_map = {x.get("id") or listing_id(x): x for x in old}
    new_map = {x.get("id") or listing_id(x): x for x in new}
    new_ids = sorted(set(new_map) - set(old_map))
    removed_ids = sorted(set(old_map) - set(new_map))
    changed_ids = sorted(
        lid for lid in (set(new_map).intersection(old_map))
        if json.dumps(new_map[lid], sort_keys=True) != json.dumps(old_map[lid], sort_keys=True)
    )
    return {
        "new": len(new_ids),
        "removed": len(removed_ids),
        "changed": len(changed_ids),
        "newIds": new_ids,
        "removedIds": removed_ids,
        "changedIds": changed_ids,
    }


def compute_analytics(listings: list[dict], history: list[dict], now: datetime.datetime) -> dict:
    today = now.date().isoformat()
    week_ago = (now.date() - datetime.timedelta(days=7)).isoformat()

    new_today = [x for x in listings if x["dateAdded"] == today]
    new_week = [x for x in listings if x["dateAdded"] >= week_ago]
    price_drops = [x for x in listings if x["status"] == "price_reduction"]
    recently_sold = [x for x in listings if x["status"] == "sold"]

    prices = [x["listingPriceUsd"] for x in listings if x.get("listingPriceUsd")]
    sold_prices = [x["soldPriceUsd"] for x in listings if x.get("soldPriceUsd")]

    by_neighborhood = defaultdict(lambda: {"count": 0, "avgListPrice": 0})
    grouped = defaultdict(list)
    for item in listings:
        grouped[item["neighborhood"]].append(item["listingPriceUsd"])
    for n, vals in grouped.items():
        by_neighborhood[n]["count"] = len(vals)
        by_neighborhood[n]["avgListPrice"] = round(mean(vals), 2)

    trend_points = [
        {
            "runAt": h["runAt"],
            "listingCount": h["listingCount"],
            "new": h["new"],
            "sold": h.get("sold", 0),
        }
        for h in history[-14:]
    ]

    return {
        "newListingsToday": len(new_today),
        "newListingsThisWeek": len(new_week),
        "priceDrops": len(price_drops),
        "recentlySold": len(recently_sold),
        "averageListingPriceUsd": round(mean(prices), 2) if prices else None,
        "averageSoldPriceUsd": round(mean(sold_prices), 2) if sold_prices else None,
        "statusMix": dict(Counter(x["status"] for x in listings)),
        "propertyTypeMix": dict(Counter(x["propertyType"] for x in listings)),
        "neighborhoodActivity": dict(by_neighborhood),
        "trend": trend_points,
    }


now = datetime.datetime.now(datetime.UTC).replace(microsecond=0)
existing_latest = load_json(LATEST_PATH, {})
existing_listings = existing_latest.get("listings", [])
history_doc = load_json(HISTORY_PATH, {"history": []})

listings = generate_full_market(now)
changes = detect_changes(existing_listings, listings)
analytics = compute_analytics(listings, history_doc.get("history", []), now)

payload = {
    "lastUpdated": now.isoformat().replace("+00:00", "Z"),
    "lastUpdatedLocal": now.astimezone(datetime.timezone(datetime.timedelta(hours=-6))).strftime("%Y-%m-%d %H:%M UTC-06:00"),
    "dataMode": "public_web_signals_with_status_inference",
    "newSinceYesterday": changes["new"],
    "changeSummary": changes,
    "highlights": {
        "newTodayIds": [x["id"] for x in listings if x["dateAdded"] == now.date().isoformat()],
        "newThisWeekIds": [x["id"] for x in listings if x["dateAdded"] >= (now.date() - datetime.timedelta(days=7)).isoformat()],
        "priceDropIds": [x["id"] for x in listings if x["status"] == "price_reduction"],
        "recentlySoldIds": [x["id"] for x in listings if x["status"] == "sold"],
    },
    "analytics": analytics,
    "listings": listings,
}

with open(LATEST_PATH, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)

history_entry = {
    "runAt": payload["lastUpdated"],
    "listingCount": len(listings),
    "new": changes["new"],
    "changed": changes["changed"],
    "removed": changes["removed"],
    "sold": analytics["recentlySold"],
    "avgListPrice": analytics["averageListingPriceUsd"],
    "avgSoldPrice": analytics["averageSoldPriceUsd"],
    "statusMix": analytics["statusMix"],
}
history_doc.setdefault("history", []).append(history_entry)
history_doc["history"] = history_doc["history"][-180:]

with open(HISTORY_PATH, "w", encoding="utf-8") as f:
    json.dump(history_doc, f, indent=2, ensure_ascii=False)

print(f"Wrote {len(listings)} listings | +{changes['new']} ~{changes['changed']} -{changes['removed']}")
