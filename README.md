# Puerto Vallarta Property Dashboard

A lightweight web dashboard for recently sold (or reported sold / recently listed) real estate in Puerto Vallarta.

## What this project does
- Displays apartments, condos, houses, and land.
- Shows property type, location, price, date, overview, and source URL.
- Includes filters by type, neighborhood, and price range.
- Includes a scheduled daily refresh workflow.

## Data-source research summary
Public, authoritative sold-price registries for Puerto Vallarta are limited and often not open via a stable API. The most accessible practical sources are:

1. **Broker sold-listing pages** (e.g., PVRPV, Kim Kieler)
   - Pros: directly marketed Puerto Vallarta inventory, often includes sold context.
   - Cons: may omit closing date/price or require manual interpretation.
2. **Regional market reports/blog posts** (e.g., Mexico Life)
   - Pros: can include sold/property commentary and neighborhood context.
   - Cons: not a formal government transaction registry.
3. **Large listing portals as fallback** (e.g., Point2)
   - Pros: consistent listing structure and easy public access.
   - Cons: typically listing prices rather than confirmed final sold prices.

Because complete public sold records are not reliably accessible, this dashboard clearly labels rows as **"Reported Sold / Recently Listed"** when a confirmed sold price/date is unavailable.

## Run locally
Open `dashboard.html` in a browser.

## Daily refresh
GitHub Actions runs `.github/workflows/daily-data-refresh.yml` once per day and attempts to refresh `data/latest.json` using `scripts/fetch_listings.py`.
