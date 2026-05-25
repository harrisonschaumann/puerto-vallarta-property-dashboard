# Puerto Vallarta Property Dashboard

A beginner-friendly, static dashboard for Puerto Vallarta property activity, designed to run on **GitHub Pages** and refresh data daily with **GitHub Actions**.

## What this project includes
- A mobile-friendly dashboard (`dashboard.html`) with filters for property type, neighborhood, and price.
- A daily data refresh script (`scripts/fetch_listings.py`).
- Automatic deploy to GitHub Pages from a GitHub Actions workflow.
- Fallback sample Puerto Vallarta data when live sold-property details are not reliably available.

---

## Quick start (10–15 minutes)

### 1) Fork or clone this repository
```bash
git clone https://github.com/<your-username>/puerto-vallarta-property-dashboard.git
cd puerto-vallarta-property-dashboard
```

### 2) Preview locally
Just open `dashboard.html` in your browser.

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

## Enable GitHub Pages (public URL)

1. In GitHub, open your repository.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, choose **Source: GitHub Actions**.
4. Save.

After the workflow runs, your site is published at:

`https://<your-username>.github.io/puerto-vallarta-property-dashboard/`

> Tip: The workflow copies `dashboard.html` to `index.html` during deployment so Pages serves it automatically.

---

## Automatic daily refresh + deployment

The workflow file is:

`.github/workflows/daily-data-refresh.yml`

What it does every day:
1. Runs `python scripts/fetch_listings.py`
2. Commits changes to `data/latest.json` if data changed
3. Builds a static site folder (`site/`)
4. Deploys to GitHub Pages

You can also run it manually:
1. Open the **Actions** tab in GitHub.
2. Select **Daily Data Refresh and Deploy**.
3. Click **Run workflow**.

---

## Data limitations (important)

Sold-property transparency in Puerto Vallarta is limited for public web scraping.

### Why this happens
- There is no single open, official, stable public API with complete sold transaction records.
- Broker and portal pages often show listing prices, not guaranteed final closing prices.
- Some pages provide partial sold context without exact sale date/amount.

### How this dashboard handles that
- Entries are clearly labeled as **Reported Sold / Recently Listed** when sold values are not fully public.
- The scraper uses public pages as signals, not guaranteed deed-level confirmations.
- If live scraping returns nothing, the project keeps the dashboard usable with sample Puerto Vallarta records.

---

## File guide
- `dashboard.html` → user interface and filters.
- `data/latest.json` → dataset used by the dashboard.
- `scripts/fetch_listings.py` → daily refresh script.
- `.github/workflows/daily-data-refresh.yml` → automation for refresh + deploy.

