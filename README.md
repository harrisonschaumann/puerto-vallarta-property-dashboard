# Paua Property Group | Puerto Vallarta Real Estate Intelligence Dashboard

This project is now a **self-updating intelligence dashboard** (GitHub Pages compatible) for Puerto Vallarta properties.

## What is automated

- **Daily data collection every morning** using `scripts/fetch_listings.py` (via scheduled GitHub Action).
- **Change tracking** between runs:
  - New listings
  - Changed listings
  - Removed listings
- **Historical snapshots** saved to `data/history.json` for trend tracking.
- **Fresh latest payload** written to `data/latest.json` for the website.
- **AI-style market summary** generated from newest records and change counts.

## Data sources used

Current automated public-source crawl list in `scripts/fetch_listings.py`:

- PVRPV Real Estate
- Kim Kieler Sold Listings
- Mexico Life Realty Blog
- Point2 Puerto Vallarta

> Note: open/public sold data may be incomplete. Confidence labels are attached per listing.

## Confidence labels shown on dashboard

- **Confirmed Sold**: deed/verified closing source (reserved for verified feeds)
- **Reported Sold**: broker/site/public report indicates sold status
- **Recently Listed**: appears as active/new listing signal
- **Unknown**: insufficient status clarity

## Dashboard features added

- Last updated timestamp section
- “New since yesterday” section
- New/changed/removed summary
- AI-style market summary block
- Auto refresh in browser every 10 minutes
- Professional Paua Property Group visual styling

## Local usage

```bash
python scripts/fetch_listings.py
```

Then open `dashboard.html`.

## GitHub Pages compatibility

No server is required. The site reads `./data/latest.json` directly and stays fully static-host friendly.

## Suggested GitHub Action schedule

Run `scripts/fetch_listings.py` at **14:00 UTC daily** (morning in North America), then commit updated `data/latest.json` and `data/history.json`.
