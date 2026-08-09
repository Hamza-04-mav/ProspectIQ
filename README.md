# 🧭 ProspectIQ

**ProspectIQ** is a Streamlit console for B2B prospecting: describe the kind of
business you're targeting in plain English (or fill in a manual form), and it
returns a scored, filterable, exportable list of local-business leads —
flagging which ones don't have a website yet, so agencies and freelancers can
prioritize outreach.

Built as a from-scratch Streamlit reimagining of a Next.js lead-gen tool,
with a different architecture, a custom scoring engine, and its own visual
identity (deep slate + emerald theme, card & table dual views, KPI strip,
donut chart).

![ProspectIQ](docs/screenshot-placeholder.png)

---

## ✨ Features

- **Smart Brief Search** — type a natural-language request like *"boutique
  gyms in Austin that don't have a website yet"* and ProspectIQ extracts the
  category, location, and intent automatically.
  - Works with **zero API keys** via a built-in rule-based parser.
  - Optionally upgrade to **Groq** (fast, free-tier Llama models) for richer
    natural-language understanding.
- **Manual Search** — plain category + location fields for precise control.
- **Prospect Scoring** — every lead gets a transparent 0–100 "prospect score"
  and a Hot / Warm / Cool tier based on website status, rating, review
  volume, and contact completeness.
- **Demo Mode** — generates realistic mock leads instantly so the app is
  fully explorable with no setup — ideal for a live portfolio deployment.
- **Live Data Mode** — plug in a [Serper.dev](https://serper.dev) API key to
  pull real Google Maps business listings.
- **Dashboard KPIs & Chart** — total prospects, missing-website %, average
  rating, hot-lead count, and a website-coverage donut chart.
- **Dual result views** — sortable table view and a visual card grid.
- **Exports** — one-click CSV, Excel, and optional push to a Google Sheet via
  a service-account credential entered at runtime (never stored on disk).

---

## 🧱 Tech Stack

- **UI**: Streamlit, custom CSS
- **Data**: pandas, openpyxl
- **Charts**: Plotly
- **Search**: Serper.dev (Google Maps API) with a mock-data fallback
- **AI parsing**: Groq (OpenAI-compatible endpoint) with a dependency-free
  heuristic fallback used automatically when no key is set
- **Export**: gspread + google-auth (optional)

---

## 🚀 Getting Started

### 0. Add your portfolio credit (optional but recommended)

Near the top of `app.py`, fill in:

```python
DEVELOPER_NAME = "Your Name"
GITHUB_URL = "https://github.com/yourhandle"
LINKEDIN_URL = "https://linkedin.com/in/yourhandle"
PORTFOLIO_URL = "https://yourportfolio.com"
```

These render as pill links in the footer of the deployed app. Leave any of
them blank and that link simply won't appear.

### 1. Clone and install

```bash
git clone <your-repo-url>
cd ProspectIQ
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. (Optional) Add your API keys

The app runs with **zero configuration** in Demo mode. To enable live data
and AI parsing for anyone who visits your deployment — without ever exposing
your keys to them — you have three options, in priority order:

**Option A — hardcode directly in `app.py` (simplest for a personal portfolio deploy):**

Open `app.py` and fill in the `DEPLOYMENT CONFIG` block near the top:

```python
HARDCODED_SERPER_API_KEY = "your-serper-key"
HARDCODED_GROQ_API_KEY = "your-groq-key"
HARDCODED_GROQ_MODEL = "llama-3.3-70b-versatile"
```

These values are used **server-side only** — they're never written into a
visible input field, so a visitor inspecting the page or its network traffic
cannot recover them. This is the easiest option, but keep the repo private if
you go this route, since anyone with repo access can read the keys.

**Option B — Streamlit secrets (recommended if the repo is public):**

```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:

```toml
SERPER_API_KEY = "your-serper-key"
GROQ_API_KEY = "your-groq-key"
GROQ_MODEL = "llama-3.3-70b-versatile"
```

This file is already excluded via `.gitignore`, so it never gets pushed to
GitHub. Leave the `HARDCODED_*` variables in `app.py` blank and this is
picked up automatically instead.

**Option C — environment variables:** same variable names as above, set via
your shell or hosting platform's environment settings.

Get free keys here:
- Serper.dev (Google Maps data): https://serper.dev
- Groq (free-tier Llama models for brief parsing): https://console.groq.com/keys

### 3. Run it

```bash
streamlit run app.py
```

Open the URL it prints — usually **http://localhost:8501**. If a key was
configured through any of the options above, Demo mode automatically
switches off and the sidebar shows a green "Live search enabled" status —
without ever displaying the key itself. Visitors don't need any key of
their own; they can optionally paste their own key into the sidebar to
override yours if they want to use their own quota.

If no key is configured anywhere, Demo mode stays on and the app works
instantly with realistic mock data — no setup required at all.

---

## ☁️ Deploying (Streamlit Community Cloud)

1. Push this folder to a GitHub repo. If you used **Option A** (hardcoded
   keys), make the repo **private**. If you used **Option B** (secrets.toml),
   the repo can be public — the secrets file is already git-ignored.
2. Go to https://share.streamlit.io → **New app** → pick your repo/branch and
   set the main file to `app.py`.
3. If using Option B, open **Advanced settings → Secrets** and paste the
   contents of `.streamlit/secrets.toml.example` filled in with your real
   keys.
4. Deploy. The public URL is what you link from your portfolio — visitors get
   a fully working live app with no keys of their own and no visibility into
   yours.

---

## 📂 Project Structure

```
ProspectIQ/
├── app.py                    # Streamlit UI & orchestration
├── modules/
│   ├── query_parser.py       # Free-text brief → structured search params
│   ├── lead_search.py        # Serper.dev live search + demo generator
│   ├── scoring.py            # Prospect scoring & tiering
│   ├── sheets_export.py      # Optional Google Sheets export
│   └── styling.py            # Custom CSS theme
├── .streamlit/config.toml    # Theme configuration
├── requirements.txt
└── .env.example
```

---

## 🗺️ Roadmap Ideas

- Persist search history / saved lists across sessions with a lightweight DB
- CRM export (HubSpot / Pipedrive) alongside Google Sheets
- Bulk brief upload (CSV of categories × locations)
- Email/SMS outreach templates generated per lead

---

## 📄 License

MIT — free to use, modify, and showcase in your own portfolio.
