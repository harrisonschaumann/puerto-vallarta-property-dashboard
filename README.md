# Puerto Vallarta Real Estate Market Tracker

This repository publishes a static Puerto Vallarta market dashboard to GitHub Pages, including listing activity, status movement, and neighborhood analytics.

## What the tracker includes

- Property types: apartments, condos, houses, and land.
- Statuses: new, sold, pending, price reductions, and back-on-market.
- Per-property fields:
  - property type
  - address/location
  - neighborhood
  - listing price
  - sold price (if available)
  - date added
  - status
  - overview/description
  - source
- Highlights:
  - New today
  - New this week
  - Price drops
  - Recently sold
- Historical run snapshots in `data/history.json` so changes can be tracked over time.
- Analytics in `data/latest.json`:
  - number of new listings today
  - average prices
  - trend points from recent runs
  - neighborhood activity summary

## Data source limitations (important)

This project uses **public web signals** and does **not** directly integrate with protected MLS databases or government deed registries.

Because of that:

- “All newly listed properties” means all records discoverable from configured public pages, not guaranteed complete market coverage.
- Sold and pending states may be delayed, inferred, broker-reported, or missing on some sources.
- Final sold prices may be unavailable or differ from later official records.
- Source sites can change markup or block scraping, which may reduce coverage temporarily.
- Geographic/address normalization and neighborhood naming can vary by source.

Always treat this dashboard as a market intelligence layer, not a legal record of ownership transfer.

## Local run

```bash
python scripts/fetch_listings.py
```

## Deployment and refresh

- GitHub Pages deployment remains static-site compatible (`dashboard.html` + `data/*.json`).
- Browser auto-refresh is set to 10 minutes by meta refresh and JavaScript interval.
