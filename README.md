# Paua Property Group | Puerto Vallarta Real Estate Dashboard

Professional static real estate dashboard for **Paua Property Group**, hosted on **GitHub Pages** with daily data refresh and automated daily email notifications.

## Live website

**GitHub Pages URL:** `https://<your-github-username>.github.io/puerto-vallarta-property-dashboard/`

> After deployment, replace `<your-github-username>` with your actual GitHub username.

---

## What this project now includes

- Professional homepage layout in `dashboard.html`:
  - Sticky header
  - Hero section
  - Property dashboard metrics
  - Filters
  - Listing table
  - Footer
- Mobile-friendly responsive styling.
- Daily data refresh via GitHub Actions every morning.
- Daily email notification that sends the dashboard link to `pauapropertygroup@gmail.com` every morning.
- Clear sample/reported-data labeling if live sold-property data is unavailable.

---

## Data quality and labeling

Sold-property transparency in Puerto Vallarta is limited on open/public sources.

Because of this, the dashboard intentionally supports `dataMode: "sample"` and displays labeled records such as:
- `Reported Sold / Recently Listed`
- `Sample Market Listing`

Only set `dataMode` to `live_verified` if you have verifiable sold-price and sold-date records from a trusted source.

---

## GitHub Pages deployment

This repository uses `.github/workflows/deploy-pages.yml` to deploy:
- `dashboard.html` as `index.html`
- `data/latest.json` as site data

### Enable Pages
1. Go to your repo on GitHub.
2. Open **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.

---

## Daily automation schedules (morning)

### 1) Daily data refresh
Workflow: `.github/workflows/daily-data-refresh.yml`
- Runs at `0 14 * * *` (14:00 UTC daily).
- Refreshes `data/latest.json`.
- Commits and pushes only when changed.

### 2) Daily email notification
Workflow: `.github/workflows/daily-email-notification.yml`
- Runs at `5 14 * * *` (14:05 UTC daily).
- Sends the dashboard link to `pauapropertygroup@gmail.com`.

> 14:00 UTC is morning in North American time zones.

---

## Required GitHub Actions secrets (exact names)

Set these at: **Repository Settings → Secrets and variables → Actions → New repository secret**

1. `SMTP_SERVER`
   - Example for Gmail: `smtp.gmail.com`
2. `SMTP_PORT`
   - Example for Gmail TLS: `465`
3. `SMTP_USERNAME`
   - The SMTP login (for Gmail, typically your Gmail address)
4. `SMTP_PASSWORD`
   - SMTP password (for Gmail, use an **App Password**, not your normal account password)
5. `EMAIL_FROM`
   - The sender address shown in emails (must match/align with SMTP account policy)
6. `DASHBOARD_URL`
   - Your live GitHub Pages URL, e.g. `https://yourusername.github.io/puerto-vallarta-property-dashboard/`

⚠️ Never hardcode credentials in source files.

---

## Local run

```bash
python scripts/fetch_listings.py
```

Then open `dashboard.html` locally.

---

## Notes for production data upgrades

If/when you add a true sold-data feed:
1. Update `scripts/fetch_listings.py` mapping logic.
2. Keep confidence labels in each record.
3. Set `dataMode` to `live_verified` only for verified deed-level/closed records.
