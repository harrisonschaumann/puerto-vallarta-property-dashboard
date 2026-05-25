# Puerto Vallarta Property Dashboard

A beginner-friendly, static dashboard for Puerto Vallarta property activity, designed to run on **GitHub Pages** and refresh data daily with **GitHub Actions**.

## What this project includes
- A mobile-friendly dashboard (`dashboard.html`) with filters for property type, neighborhood, and price.
- A daily data refresh script (`scripts/fetch_listings.py`).
- GitHub Actions workflows for daily data refresh and GitHub Pages deployment.
- Fallback sample Puerto Vallarta data when live sold-property details are not reliably available.

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

## Enable GitHub Pages (exact beginner clicks)

1. In GitHub, open your repository page.
2. Click the **Settings** tab (top navigation in your repo).
3. In the left sidebar, click **Pages**.
4. In **Build and deployment**, open the **Source** dropdown.
5. Select **GitHub Actions**.
6. Wait a few seconds for GitHub to save this automatically.

---

## First-time deploy: where to click

1. Click the **Actions** tab in your repository.
2. In the left workflow list, click **Deploy Dashboard to GitHub Pages**.
3. Click **Run workflow** (right side).
4. In the branch dropdown, leave **main** selected.
5. Click the green **Run workflow** button.
6. Wait for the run to finish (green check mark).

---

## View your live dashboard URL

After the deploy workflow succeeds:

1. Go back to **Settings → Pages**.
2. Under **GitHub Pages**, click the URL GitHub shows.

Your URL will be:

`https://<your-username>.github.io/puerto-vallarta-property-dashboard/`

This works because the deploy workflow publishes `dashboard.html` as `index.html` (homepage file) for GitHub Pages.

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
- Entries are clearly labeled as **Reported Sold / Recently Listed** when sold values are not fully public.
- The scraper uses public pages as signals, not guaranteed deed-level confirmations.
- If live scraping returns nothing, the project keeps the dashboard usable with sample Puerto Vallarta records.
