# Puerto Vallarta Property Dashboard

A beginner-friendly, static dashboard for Puerto Vallarta property activity, designed to run on **GitHub Pages** and refresh data daily with **GitHub Actions**.

## Live dashboard

**GitHub Pages URL:** `https://<your-username>.github.io/puerto-vallarta-property-dashboard/`

> If your dashboard is already deployed, replace `<your-username>` with your GitHub username and keep this exact path.

## What this project includes
- A mobile-friendly dashboard (`dashboard.html`) with filters for property type, neighborhood, and price.
- A daily data refresh script (`scripts/fetch_listings.py`).
- GitHub Actions workflows for daily data refresh and GitHub Pages deployment.
- Fallback sample Puerto Vallarta data when live sold-property details are not reliably available.

---

## Data transparency: live vs sample

This dashboard currently defaults to **sample/indicative market data** with public listing signals. It does **not** claim verified deed-level sold transaction history unless `dataMode` is set to `live_verified` in `data/latest.json`.

How this appears in the UI:
- A status badge at the top of the dashboard.
- A `Data Mode` value in the meta line (`sample`, `hybrid`, or `live_verified`).

---

## Quick start (10–15 minutes)

### 1) Fork or clone this repository
```bash
git clone https://github.com/<your-username>/puerto-vallarta-property-dashboard.git
cd puerto-vallarta-property-dashboard
```

### 2) Preview locally
Open `dashboard.html` in your browser.

If you want to refresh data first:
```bash
python scripts/fetch_listings.py
```
Then refresh the browser tab.

### 3) Push to your GitHub repository
```bash
git add .
git commit -m "Initial dashboard setup"
git push origin main
```

---

## Next steps: connect a real data source

To move from sample data to a production-grade feed:

1. **Choose a source of truth**
   - MLS partner export, brokerage back-office CSV/API, or a commercial property-data API.
2. **Normalize fields in `scripts/fetch_listings.py`**
   - Map upstream fields into the existing schema (`propertyType`, `location`, `neighborhood`, `salePriceUsd`, `saleDate`, `overview`, `sourceName`, `sourceUrl`, `dataLabel`).
3. **Set a reliability policy**
   - Tag records as `Verified Sold`, `Reported Sold / Recently Listed`, or `Sample Market Listing` based on confidence.
4. **Set `dataMode` in `data/latest.json`**
   - Use `live_verified` only when sale date + closed price are verifiable.
5. **Automate validation in CI**
   - Add schema checks and fail the workflow if required fields are missing.
6. **Add provenance fields (recommended)**
   - Add `sourceCapturedAt`, `sourceRecordId`, and `verificationMethod` for auditability.

---

## Enable GitHub Pages (exact beginner clicks)

1. In GitHub, open your repository page.
2. Click the **Settings** tab (top navigation in your repo).
3. In the left sidebar, click **Pages**.
4. In **Build and deployment**, open the **Source** dropdown.
5. Select **GitHub Actions**.
6. Wait a few seconds for GitHub to save this automatically.

---

## Automatic daily refresh

The daily workflow file is:

`.github/workflows/daily-data-refresh.yml`

What it does each day:
1. Runs `python scripts/fetch_listings.py`
2. Commits changes to `data/latest.json` only if the data changed
3. Pushes to `main`
4. The push triggers the deploy workflow, which republishes the site

To run daily refresh manually:
1. Open **Actions**.
2. Click **Daily Data Refresh**.
3. Click **Run workflow**.

---

## Workflow files
- `.github/workflows/deploy-pages.yml` → builds and deploys `dashboard.html` to GitHub Pages as homepage (`index.html`).
- `.github/workflows/daily-data-refresh.yml` → refreshes listing data on a daily schedule.

---

## Data limitations (important)

Sold-property transparency in Puerto Vallarta is limited for public web scraping.

### Why this happens
- There is no single open, official, stable public API with complete sold transaction records.
- Broker and portal pages often show listing prices, not guaranteed final closing prices.
- Some pages provide partial sold context without exact sale date/amount.

### How this dashboard handles that
- Entries are clearly labeled by confidence level.
- The scraper uses public pages as signals, not guaranteed deed-level confirmations.
- If live scraping returns nothing, the project keeps the dashboard usable with curated sample Puerto Vallarta records.
