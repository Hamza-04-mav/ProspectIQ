"""
ProspectIQ - AI-assisted lead prospecting console
===================================================
Streamlit front end for turning a plain-English brief into a scored,
exportable list of local-business prospects.

Run locally:
    streamlit run app.py
"""

import os
from datetime import datetime
from io import BytesIO

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from modules.query_parser import parse_brief
from modules.lead_search import search_live, LeadSearchError
from modules.scoring import enrich_with_scores, tier_color
from modules.sheets_export import push_to_google_sheet, SheetsExportError
from modules.styling import CUSTOM_CSS

# ============================================================================
# 🔑 DEPLOYMENT CONFIG
# ----------------------------------------------------------------------------
# Paste your keys directly below if you want them baked into this deployment.
# They are used SERVER-SIDE ONLY - never rendered into a visible input field,
# so site visitors cannot read them from the browser (view-source / dev tools
# won't reveal them). Visitors just get a working live app with no setup.
#
# Leave any value as "" to fall back to Streamlit secrets (.streamlit/secrets.toml
# or the Secrets panel on Streamlit Community Cloud), then to environment
# variables, and finally to Demo mode if nothing is configured at all.
# ============================================================================
HARDCODED_SERPER_API_KEY = ""
HARDCODED_GROQ_API_KEY = ""
HARDCODED_GROQ_MODEL = "llama-3.3-70b-versatile"
HARDCODED_GOOGLE_SHEET_ID = ""
HARDCODED_GOOGLE_SERVICE_ACCOUNT_JSON = ""
# ----------------------------------------------------------------------------
# 👤 Portfolio credit (shown in the footer) - edit these with your own info.
# ----------------------------------------------------------------------------
DEVELOPER_NAME = "Hamza Safdar"
GITHUB_URL = "https://github.com/Hamza-04-mav"      # e.g. "https://github.com/yourhandle"
LINKEDIN_URL = "https://www.linkedin.com/in/hamzasafdar04"    # e.g. "https://linkedin.com/in/yourhandle"
PORTFOLIO_URL = ""   # e.g. "https://yourportfolio.com"

def get_secret(name: str, hardcoded: str = "", default: str = "") -> str:
    """Resolves a config value with precedence: hardcoded > st.secrets > env var."""
    if hardcoded:
        return hardcoded
    try:
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return os.environ.get(name, default)


SERPER_KEY = get_secret("SERPER_API_KEY", HARDCODED_SERPER_API_KEY)
GROQ_KEY = get_secret("GROQ_API_KEY", HARDCODED_GROQ_API_KEY)
GROQ_MODEL = get_secret("GROQ_MODEL", HARDCODED_GROQ_MODEL, "llama-3.3-70b-versatile")
SHEET_ID = get_secret("GOOGLE_SHEET_ID", HARDCODED_GOOGLE_SHEET_ID)
SERVICE_ACCOUNT_JSON = get_secret(
    "GOOGLE_SERVICE_ACCOUNT_JSON", HARDCODED_GOOGLE_SERVICE_ACCOUNT_JSON
)

HAS_LIVE_SEARCH = bool(SERPER_KEY)
HAS_AI_PARSING = bool(GROQ_KEY)
HAS_SHEETS_EXPORT = bool(SHEET_ID and SERVICE_ACCOUNT_JSON)

st.set_page_config(
    page_title="ProspectIQ",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
if "leads" not in st.session_state:
    st.session_state.leads = []
if "meta" not in st.session_state:
    st.session_state.meta = None
if "search_count" not in st.session_state:
    st.session_state.search_count = 0
if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------------------------------------------------------
# Sidebar - configuration
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="pq-sidebar-logo">
            <div class="pq-sidebar-mark">🧭</div>
            <div class="pq-sidebar-brand">ProspectIQ</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="pq-sidebar-tag">AI-assisted local business prospecting</div>',
        unsafe_allow_html=True,
    )

    with st.expander("🔑 Search & AI status", expanded=not HAS_LIVE_SEARCH):
        if HAS_LIVE_SEARCH:
            st.success("✅ Live business search is enabled.")
        else:
            st.error(
                "⚠️ No Serper.dev API key configured - live search will fail "
                "until one is set (see README / Streamlit Secrets)."
            )

        if HAS_AI_PARSING:
            st.success("✅ AI-powered brief parsing is enabled (Groq).")
        else:
            st.info("Using the built-in rule-based brief parser.")

        st.caption(
            "Keys are configured server-side by the app owner and are never "
            "exposed to visitors. Optionally use your own key below instead."
        )
        serper_override = st.text_input(
            "Your own Serper.dev key (optional)", type="password", value="",
            placeholder="Leave blank to use the app's default",
        )
        groq_override = st.text_input(
            "Your own Groq key (optional)", type="password", value="",
            placeholder="Leave blank to use the app's default",
        )

    effective_serper_key = serper_override or SERPER_KEY
    effective_groq_key = groq_override or GROQ_KEY

    with st.expander("📤 Google Sheets export (optional)"):
        if HAS_SHEETS_EXPORT:
            st.success("✅ A default export sheet is configured.")
        sheet_id_override = st.text_input("Push to your own Spreadsheet ID", value="")
        sa_json_override = st.text_area(
            "Your own service account JSON", value="", height=90,
            placeholder="Leave blank to use the app's default (if configured)",
        )
        st.caption("Paste your service-account credentials JSON. Nothing is saved to disk.")

    effective_sheet_id = sheet_id_override or SHEET_ID
    effective_sa_json = sa_json_override or SERVICE_ACCOUNT_JSON

    st.divider()
    st.markdown('<div class="pq-sidebar-section-label">Result filters</div>', unsafe_allow_html=True)
    min_rating = st.slider("Minimum rating", 0.0, 5.0, 0.0, 0.1)
    website_filter = st.selectbox(
        "Website status", ["All prospects", "Missing a website only", "Has a website only"]
    )
    result_limit = st.slider("Max results", 5, 40, 15)

    st.divider()
    st.markdown(
        f"""<div class="pq-sidebar-stat">
            <span style="font-size:0.78rem;color:#8493AC !important;">Session searches</span>
            <span class="n">{st.session_state.search_count}</span>
        </div>""",
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------------
# Hero header
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="pq-hero">
        <div class="pq-hero-inner">
            <span class="pq-badge"><span class="dot"></span>Lead Intelligence</span>
            <h1>Find and score your next 20 prospects in seconds.</h1>
            <p>Describe who you're looking for in plain English. ProspectIQ pulls local
            business listings, flags who's missing a website, and ranks every lead by
            outreach potential.</p>
            <div class="pq-hero-stats">
                <span class="pq-hero-chip">⚡ Results in seconds</span>
                <span class="pq-hero-chip">🧠 AI-parsed briefs</span>
                <span class="pq-hero-chip">📊 Explainable scoring</span>
                <span class="pq-hero-chip">🔒 No visitor keys required</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Search console
# --------------------------------------------------------------------------
tab_smart, tab_manual = st.tabs(["✨ Smart brief", "🎯 Manual search"])

brief_text, manual_category, manual_location, manual_intent_missing = "", "", "", False
run_search = False
search_source = "smart"

with tab_smart:
    brief_text = st.text_area(
        "Describe your ideal prospect",
        placeholder='e.g. "Boutique gyms in Austin, Texas that don\'t have a website yet"',
        height=90,
    )
    run_smart = st.button("🔍 Run smart search", use_container_width=True, type="primary")

with tab_manual:
    c1, c2 = st.columns(2)
    with c1:
        manual_category = st.text_input("Business category", placeholder="e.g. dental clinics")
    with c2:
        manual_location = st.text_input("Location", placeholder="e.g. Karachi, Pakistan")
    manual_intent_missing = st.checkbox("Only show businesses missing a website")
    run_manual = st.button("🔍 Run manual search", use_container_width=True)

if run_smart and brief_text.strip():
    run_search, search_source = True, "smart"
elif run_manual and manual_category and manual_location:
    run_search, search_source = True, "manual"

# --------------------------------------------------------------------------
# Execute search
# --------------------------------------------------------------------------
if run_search:
    with st.spinner("Scanning listings and scoring prospects..."):
        try:
            if search_source == "smart":
                brief = parse_brief(
                    brief_text,
                    ai_api_key=effective_groq_key,
                    ai_model=GROQ_MODEL,
                )
                category, location = brief.category, brief.location
                target_missing = brief.target_missing_site
                parsed_by = brief.parsed_by
            else:
                category, location = manual_category, manual_location
                target_missing = manual_intent_missing
                parsed_by = "manual"

            if not category:
                st.error("I couldn't identify a business category - try rephrasing your brief.")
                st.stop()

            if not effective_serper_key:
                raise LeadSearchError(
                    "No Serper.dev API key configured. Add SERPER_API_KEY in "
                    "Streamlit Secrets (or paste your own key in the sidebar) "
                    "to run live searches."
                )
            raw_leads = search_live(category, location, effective_serper_key)

            pre_filter_count = len(raw_leads)

            if target_missing:
                raw_leads = [l for l in raw_leads if not l["has_website"]]

            scored_leads = enrich_with_scores(raw_leads, target_missing)[:result_limit]

            st.session_state.leads = scored_leads
            st.session_state.meta = {
                "category": category,
                "location": location or "Unspecified",
                "target_missing": target_missing,
                "parsed_by": parsed_by,
                "timestamp": datetime.now().strftime("%b %d, %I:%M %p"),
            }
            st.session_state.search_count += 1
            st.session_state.history.insert(0, f"{category} · {location or 'Unspecified'}")
            st.session_state.history = st.session_state.history[:6]

            if not scored_leads:
                if pre_filter_count == 0:
                    st.warning(
                        f"Live search found no businesses matching “{category}” in "
                        f"“{location or 'that area'}”. Try a broader category or a "
                        f"larger nearby city."
                    )
                else:
                    st.warning(
                        f"Found {pre_filter_count} matching businesses, but all of them "
                        f"already have a website - none matched the \"missing a website\" "
                        f"filter. Try unchecking that filter or a different category."
                    )

        except LeadSearchError as exc:
            st.error(f"Search failed: {exc}")
        except Exception as exc:  # noqa: BLE001
            st.error(f"Unexpected error: {exc}")

# --------------------------------------------------------------------------
# Results
# --------------------------------------------------------------------------
leads = st.session_state.leads
meta = st.session_state.meta

if not leads:
    st.markdown(
        """
        <div class="pq-empty-state">
            <div class="pq-empty-icon">📭</div>
            <div style="font-weight:800;color:#1F2937;font-size:1.05rem;font-family:'Plus Jakarta Sans',sans-serif;">No prospects yet</div>
            <div style="font-size:0.88rem;margin-top:0.3rem;">
                Run a smart or manual search above to populate your pipeline.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    filtered = [
        l for l in leads
        if (l.get("rating") or 0) >= min_rating
        and (
            website_filter == "All prospects"
            or (website_filter == "Missing a website only" and not l["has_website"])
            or (website_filter == "Has a website only" and l["has_website"])
        )
    ]

    total = len(filtered)
    missing_site = sum(1 for l in filtered if not l["has_website"])
    avg_rating = (
        sum(l["rating"] for l in filtered if isinstance(l.get("rating"), (int, float))) / total
        if total else 0
    )
    hot_count = sum(1 for l in filtered if l["tier"] == "Hot")

    if meta:
        st.markdown(
            f"""<div class="pq-caption-row">🔎 Query parsed via <b>{meta['parsed_by']}</b> · 
            “{meta['category']}” in “{meta['location']}” · {meta['timestamp']}</div>""",
            unsafe_allow_html=True,
        )

    k1, k2, k3, k4 = st.columns(4)
    kpi_data = [
        (k1, "Prospects found", str(total), "matching current filters"),
        (k2, "Missing a website", str(missing_site), f"{(missing_site/total*100 if total else 0):.0f}% of results"),
        (k3, "Avg. rating", f"{avg_rating:.1f} ★", "across visible prospects"),
        (k4, "Hot leads", str(hot_count), "score 75+"),
    ]
    for col, label, value, sub in kpi_data:
        with col:
            st.markdown(
                f"""<div class="pq-kpi"><div class="label">{label}</div>
                <div class="value">{value}</div><div class="sub">{sub}</div></div>""",
                unsafe_allow_html=True,
            )

    st.write("")
    chart_col, action_col = st.columns([1.3, 1])

    with chart_col:
        st.markdown(
            '<div class="pq-section-title"><span class="ico-badge">📊</span>Website coverage</div>',
            unsafe_allow_html=True,
        )
        has_site_ct = total - missing_site
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Has website", "Missing website"],
                    values=[has_site_ct, missing_site],
                    hole=0.62,
                    marker=dict(colors=["#0F766E", "#F97316"]),
                    textinfo="percent",
                    sort=False,
                )
            ]
        )
        fig.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=230,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with action_col:
        st.markdown(
            '<div class="pq-section-title"><span class="ico-badge">📁</span>Export pipeline</div>',
            unsafe_allow_html=True,
        )
        export_df = pd.DataFrame(filtered)[
            ["name", "address", "phone", "rating", "reviews", "website", "prospect_score", "tier"]
        ].rename(columns={
            "name": "Name", "address": "Address", "phone": "Phone", "rating": "Rating",
            "reviews": "Reviews", "website": "Website", "prospect_score": "Score", "tier": "Tier",
        })

        st.download_button(
            "⬇ Download CSV",
            export_df.to_csv(index=False).encode("utf-8"),
            file_name="prospectiq_leads.csv",
            mime="text/csv",
            use_container_width=True,
        )

        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            export_df.to_excel(writer, index=False, sheet_name="Prospects")
        st.download_button(
            "⬇ Download Excel",
            excel_buffer.getvalue(),
            file_name="prospectiq_leads.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

        if st.button("📤 Push to Google Sheets", use_container_width=True):
            if not effective_sheet_id or not effective_sa_json:
                st.warning("Add a Spreadsheet ID and service account JSON in the sidebar first.")
            else:
                try:
                    with st.spinner("Writing to Google Sheets..."):
                        n = push_to_google_sheet(filtered, effective_sheet_id, effective_sa_json)
                    st.success(f"Pushed {n} prospects to Google Sheets.")
                except SheetsExportError as exc:
                    st.error(str(exc))

    st.write("")
    view_table, view_cards = st.tabs(["📋 Table view", "🗂️ Card view"])

    with view_table:
        st.dataframe(
            export_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Website": st.column_config.LinkColumn("Website"),
                "Score": st.column_config.ProgressColumn(
                    "Score", min_value=0, max_value=100, format="%d"
                ),
            },
        )

    with view_cards:
        cols = st.columns(3)
        for i, lead in enumerate(filtered):
            color = tier_color(lead["tier"])
            initials = "".join(w[0] for w in lead["name"].split()[:2]).upper() or "•"
            website_html = (
                f'<div class="pq-website-pill pq-has-site">🌐 Has website</div>'
                if lead["has_website"]
                else '<div class="pq-website-pill pq-no-site">🚫 No website found</div>'
            )
            rating_txt = f"{lead['rating']}★" if lead.get("rating") else "No rating"
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div class="pq-card">
                        <div class="pq-card-top">
                            <div class="pq-card-id">
                                <div class="pq-avatar">{initials}</div>
                                <div class="pq-card-name">{lead['name']}</div>
                            </div>
                            <div class="pq-tier" style="background:{color}">{lead['tier']}</div>
                        </div>
                        <div class="pq-card-meta"><span class="ico">📍</span>{lead['address']}</div>
                        <div class="pq-card-meta"><span class="ico">📞</span>{lead['phone']}</div>
                        <div class="pq-card-meta"><span class="ico">⭐</span>{rating_txt} · {lead.get('reviews', 0)} reviews</div>
                        {website_html}
                        <div class="pq-score-track">
                            <div class="pq-score-fill" style="width:{lead['prospect_score']}%;background:{color}"></div>
                        </div>
                        <div class="pq-score-label"><span>Prospect score</span><span>{lead['prospect_score']}/100</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

_footer_links = []
if GITHUB_URL:
    _footer_links.append(f'<a href="{GITHUB_URL}" target="_blank">GitHub</a>')
if LINKEDIN_URL:
    _footer_links.append(f'<a href="{LINKEDIN_URL}" target="_blank">LinkedIn</a>')
if PORTFOLIO_URL:
    _footer_links.append(f'<a href="{PORTFOLIO_URL}" target="_blank">Portfolio</a>')
_footer_links_html = "".join(_footer_links)

st.markdown(
    f"""
    <div class="pq-footer">
        <div class="brand">🧭 ProspectIQ</div>
        <div class="links">{_footer_links_html}</div>
        <div class="fine-print">Built by {DEVELOPER_NAME} · Streamlit, Groq &amp; Serper · {datetime.now().year}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
