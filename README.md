# Paua Property Group | Puerto Vallarta Real Estate Intelligence Dashboard

This project is a **self-updating static dashboard** that publishes Puerto Vallarta listing intelligence to GitHub Pages.

## What is automated

- Daily data collection via `scripts/fetch_listings.py` (GitHub Actions schedule).
- Change tracking between runs:
  - New listings
  - Changed listings
  - Removed listings
- Historical snapshots in `data/history.json`.
- Current payload for the site in `data/latest.json`.
- Auto-generated market summary from current listings and detected changes.

## Data sources used

Current crawl list in `scripts/fetch_listings.py`:

- PVRPV Real Estate
- Kim Kieler Sold Listings
- Mexico Life Realty Blog
- Point2 Puerto Vallarta

> Note: public sold-property fields can be incomplete.

## Dashboard behavior

- Timestamped “last updated” section
- “New since yesterday” summary
- New / changed / removed counters
- Market summary paragraph
- Browser auto-refresh every 10 minutes

---

## Beginner maintenance guide (step-by-step)

Use this exact sequence when maintaining the project.

### 1) One-time repository setup

1. In GitHub, open **Settings → Pages**.
2. Under **Build and deployment**, set:
   - **Source** = GitHub Actions
3. Commit and push to `main` when asked.

### 2) Verify scheduled refresh is enabled

1. Open **Actions → Daily Data Refresh**.
2. Confirm workflow file is `.github/workflows/daily-data-refresh.yml`.
3. Confirm schedule is `0 14 * * *` (14:00 UTC daily).
4. Confirm your repo has Actions enabled (not paused/disabled).

### 3) Verify GitHub Pages deployment pipeline

1. Open **Actions → Deploy Dashboard to GitHub Pages**.
2. Confirm it runs on:
   - Pushes to `main` affecting `dashboard.html`, `data/latest.json`, or the deploy workflow file.
   - Manual `workflow_dispatch` runs.
3. Open the latest run and make sure all jobs are green.

### 4) Confirm the live dashboard URL

1. Open **Settings → Pages**.
2. Copy the **live URL** shown there.
3. Open the URL in browser.
4. Confirm:
   - The page loads.
   - Table rows appear.
   - “Last Updated” has a timestamp.

### 5) Confirm auto-refresh in browser

The dashboard refreshes in two ways:

- `<meta http-equiv="refresh" content="600">`
- JavaScript: `setInterval(() => window.location.reload(), 600000)`

Both mean refresh every 10 minutes.

### 6) Confirm new/changed listing detection

The script compares previous vs current listing IDs and content. To test locally:

```bash
python scripts/fetch_listings.py
```

Then open `data/latest.json` and check:

- `changeSummary.new`
- `changeSummary.changed`
- `changeSummary.removed`
- `newSinceYesterday`

### 7) If anything breaks

- Run the script locally:
  ```bash
  python scripts/fetch_listings.py
  ```
- Validate JSON files:
  ```bash
  python -m json.tool data/latest.json
  python -m json.tool data/history.json
  ```
- Commit and push fixes to `main`.
- Re-run workflows manually from the **Actions** tab if needed.

---

## Local usage

```bash
python scripts/fetch_listings.py
```

Then open `dashboard.html` directly, or serve folder locally.

## GitHub Actions in this repo

- `.github/workflows/daily-data-refresh.yml`
  - Runs daily fetch
  - Commits both `data/latest.json` and `data/history.json` when changed
- `.github/workflows/deploy-pages.yml`
  - Builds static `site/`
  - Publishes via GitHub Pages

## Notes

- This is a static site (no backend server needed).
- Data freshness depends on source site availability during scheduled runs.
