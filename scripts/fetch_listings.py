#!/usr/bin/env python3
import json, re, urllib.request, datetime, os

SOURCES = [
    {"name":"PVRPV Real Estate","url":"https://pvrpv.com/realestate/"},
    {"name":"Kim Kieler Sold Listings","url":"https://kimkieler.net/homepage/sold-listings/"},
    {"name":"Mexico Life Realty Blog","url":"https://mexicolife.com/blog/"},
    {"name":"Point2 Puerto Vallarta","url":"https://www.point2homes.com/MX/Real-Estate-Listings/Jalisco/Puerto-Vallarta.html"},
]


def get(u):
    req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=20) as r:
        return r.read().decode('utf-8','ignore')

def infer_type(text):
    t=text.lower()
    if re.search(r'land|lote|lot',t): return 'Land'
    if re.search(r'house|casa|villa',t): return 'House'
    if re.search(r'apartment',t): return 'Apartment'
    return 'Condo'

def build_records():
    rows=[]
    for s in SOURCES:
        try:
            html=get(s['url'])
        except Exception:
            continue
        for m in re.finditer(r'href=["\'](https?://[^"\']+)["\'][^>]*>([^<]{12,130})<',html,re.I):
            url,title=m.group(1),re.sub(r'\s+',' ',m.group(2)).strip()
            if 'vallarta' not in (title + html[:12000]).lower():
                continue
            rows.append({
                "propertyType": infer_type(title),
                "location": "Puerto Vallarta, Jalisco, Mexico",
                "neighborhood": "",
                "salePriceUsd": None,
                "saleDate": "",
                "overview": title,
                "sourceName": s['name'],
                "sourceUrl": url,
                "dataLabel": "Reported Sold / Recently Listed"
            })
            if len(rows) >= 40:
                return rows
    return rows

listings = build_records()
if not listings and os.path.exists('data/latest.json'):
    with open('data/latest.json') as f:
        current = json.load(f)
    listings = current.get('listings', [])

payload = {
    "lastUpdated": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace('+00:00','Z'),
    "listings": listings
}
with open('data/latest.json','w') as f:
    json.dump(payload,f,indent=2)
print(f"Wrote {len(listings)} listings")
