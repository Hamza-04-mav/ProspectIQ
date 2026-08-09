"""
styling.py
----------
All custom CSS lives here so app.py stays readable. Visual language: a deep
slate + emerald "fintech dashboard" aesthetic - Plus Jakarta Sans for display
type, Inter for body text, soft elevation, a mesh-gradient hero, and a
segmented-control look for tabs. Built to read as a polished, shipped product
rather than a default Streamlit app.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

:root {
    --pq-bg: #F5F7FA;
    --pq-surface: #FFFFFF;
    --pq-border: #E6EAF0;
    --pq-text: #10151F;
    --pq-text-soft: #4A5568;
    --pq-text-mute: #8892A0;
    --pq-primary: #0F766E;
    --pq-primary-dark: #0B4F49;
    --pq-primary-light: #14B8A6;
    --pq-accent: #F97316;
    --pq-danger: #DC2626;
    --pq-warn: #D97706;
    --pq-info: #2563EB;
    --pq-radius-lg: 18px;
    --pq-radius-md: 14px;
    --pq-radius-sm: 10px;
    --pq-shadow-sm: 0 1px 2px rgba(16, 21, 31, 0.04), 0 1px 1px rgba(16,21,31,0.03);
    --pq-shadow-md: 0 8px 24px -10px rgba(16, 21, 31, 0.14);
    --pq-shadow-lg: 0 20px 45px -20px rgba(11, 79, 73, 0.35);
}

html, body, [class*="css"]  {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--pq-text);
}

h1, h2, h3, .pq-hero h1, .pq-section-title, .pq-sidebar-brand, .pq-card-name {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
}

#MainMenu, footer, header {visibility: hidden;}

.stApp {
    background:
        radial-gradient(1200px 500px at 15% -10%, rgba(15,118,110,0.05), transparent 60%),
        radial-gradient(900px 500px at 100% 0%, rgba(249,115,22,0.04), transparent 55%),
        var(--pq-bg);
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2.5rem;
    max-width: 1200px;
}

/* ---------------------------------------------------------------- */
/* Hero banner                                                      */
/* ---------------------------------------------------------------- */
.pq-hero {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(650px 260px at 8% 15%, rgba(20,184,166,0.55), transparent 60%),
        radial-gradient(500px 300px at 95% 90%, rgba(249,115,22,0.35), transparent 55%),
        linear-gradient(125deg, #08302C 0%, #0B4F49 42%, #0F766E 78%, #12867D 100%);
    border-radius: 22px;
    padding: 2.5rem 2.7rem 2.3rem 2.7rem;
    color: #F0FDFA;
    margin-bottom: 1.5rem;
    box-shadow: var(--pq-shadow-lg);
    border: 1px solid rgba(255,255,255,0.08);
}
.pq-hero::after {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
    background-size: 34px 34px;
    mask-image: radial-gradient(ellipse 80% 80% at 30% 20%, black 10%, transparent 70%);
    pointer-events: none;
}
.pq-hero-inner { position: relative; z-index: 1; }
.pq-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.22);
    backdrop-filter: blur(6px);
    border-radius: 999px;
    padding: 0.32rem 0.85rem 0.32rem 0.65rem;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    color: #E6FFFA;
}
.pq-badge .dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #4ADE80;
    box-shadow: 0 0 0 3px rgba(74,222,128,0.25);
}
.pq-hero h1 {
    font-size: 2.35rem;
    font-weight: 800;
    margin: 0 0 0.55rem 0;
    letter-spacing: -0.025em;
    line-height: 1.18;
    color: #FFFFFF;
    max-width: 34ch;
}
.pq-hero p {
    font-size: 1.04rem;
    color: #CFFAF3;
    margin: 0 0 1.4rem 0;
    font-weight: 400;
    max-width: 56ch;
    line-height: 1.55;
}
.pq-hero-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
}
.pq-hero-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 10px;
    padding: 0.42rem 0.75rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: #E6FFFA;
}

/* ---------------------------------------------------------------- */
/* KPI cards                                                        */
/* ---------------------------------------------------------------- */
.pq-kpi {
    position: relative;
    background: var(--pq-surface);
    border: 1px solid var(--pq-border);
    border-radius: var(--pq-radius-md);
    padding: 1.15rem 1.3rem 1.05rem 1.3rem;
    height: 100%;
    box-shadow: var(--pq-shadow-sm);
    transition: box-shadow 0.18s ease, transform 0.18s ease;
    overflow: hidden;
}
.pq-kpi:hover {
    box-shadow: var(--pq-shadow-md);
    transform: translateY(-2px);
}
.pq-kpi::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--pq-primary), var(--pq-primary-light));
}
.pq-kpi .label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--pq-text-mute);
    margin-bottom: 0.4rem;
}
.pq-kpi .value {
    font-size: 1.85rem;
    font-weight: 800;
    color: var(--pq-text);
    line-height: 1.1;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.pq-kpi .sub {
    font-size: 0.78rem;
    color: var(--pq-text-mute);
    margin-top: 0.3rem;
}

/* ---------------------------------------------------------------- */
/* Section headers                                                  */
/* ---------------------------------------------------------------- */
.pq-section-title {
    font-size: 1.02rem;
    font-weight: 700;
    color: var(--pq-text);
    margin: 0.3rem 0 0.85rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.pq-section-title .ico-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px; height: 26px;
    border-radius: 8px;
    background: rgba(15,118,110,0.1);
    font-size: 0.9rem;
}

/* ---------------------------------------------------------------- */
/* Panel wrapper (used around search console)                       */
/* ---------------------------------------------------------------- */
.pq-panel {
    background: var(--pq-surface);
    border: 1px solid var(--pq-border);
    border-radius: var(--pq-radius-lg);
    padding: 0.4rem 0.4rem 0.1rem 0.4rem;
    box-shadow: var(--pq-shadow-sm);
    margin-bottom: 1.4rem;
}

/* ---------------------------------------------------------------- */
/* Tabs -> segmented control look                                   */
/* ---------------------------------------------------------------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #EEF2F6;
    padding: 5px;
    border-radius: 12px;
    border: 1px solid var(--pq-border);
}
.stTabs [data-baseweb="tab"] {
    height: 42px;
    border-radius: 9px;
    background: transparent;
    font-weight: 600;
    font-size: 0.92rem;
    color: var(--pq-text-soft);
    padding: 0 1.1rem;
}
.stTabs [aria-selected="true"] {
    background: var(--pq-surface) !important;
    color: var(--pq-primary-dark) !important;
    box-shadow: var(--pq-shadow-sm);
}
.stTabs [data-baseweb="tab-highlight"] { background: transparent; }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ---------------------------------------------------------------- */
/* Prospect card                                                    */
/* ---------------------------------------------------------------- */
@keyframes pq-fade-in {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}
.pq-card {
    background: var(--pq-surface);
    border: 1px solid var(--pq-border);
    border-radius: var(--pq-radius-md);
    padding: 1.15rem 1.2rem 1rem 1.2rem;
    margin-bottom: 1rem;
    transition: box-shadow 0.18s ease, transform 0.18s ease, border-color 0.18s ease;
    height: 100%;
    animation: pq-fade-in 0.35s ease both;
}
.pq-card:hover {
    box-shadow: var(--pq-shadow-md);
    transform: translateY(-3px);
    border-color: rgba(15,118,110,0.35);
}
.pq-card-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.6rem;
    margin-bottom: 0.65rem;
}
.pq-card-id {
    display: flex;
    align-items: flex-start;
    gap: 0.65rem;
}
.pq-avatar {
    flex-shrink: 0;
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 0.92rem;
    color: #fff;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: linear-gradient(135deg, var(--pq-primary), var(--pq-primary-light));
}
.pq-card-name {
    font-size: 0.98rem;
    font-weight: 700;
    color: var(--pq-text);
    line-height: 1.28;
    margin-top: 0.1rem;
}
.pq-tier {
    font-size: 0.64rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.22rem 0.6rem;
    border-radius: 999px;
    color: #FFFFFF;
    white-space: nowrap;
    box-shadow: var(--pq-shadow-sm);
}
.pq-card-meta {
    font-size: 0.83rem;
    color: var(--pq-text-soft);
    margin: 0.22rem 0;
    display: flex;
    gap: 0.5rem;
    align-items: flex-start;
}
.pq-card-meta .ico { opacity: 0.7; width: 1.1em; flex-shrink: 0; }
.pq-score-track {
    background: #EEF1F4;
    border-radius: 999px;
    height: 7px;
    margin-top: 0.85rem;
    overflow: hidden;
}
.pq-score-fill {
    height: 100%;
    border-radius: 999px;
    background-image: linear-gradient(90deg, rgba(255,255,255,0.0), rgba(255,255,255,0.35));
}
.pq-score-label {
    font-size: 0.72rem;
    color: var(--pq-text-mute);
    margin-top: 0.35rem;
    display: flex;
    justify-content: space-between;
    font-weight: 600;
}
.pq-website-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.76rem;
    font-weight: 700;
    padding: 0.32rem 0.65rem;
    border-radius: 8px;
    margin-top: 0.75rem;
}
.pq-has-site { background: #ECFDF5; color: #047857; }
.pq-no-site { background: #FEF2F2; color: #B91C1C; }

/* ---------------------------------------------------------------- */
/* Sidebar                                                          */
/* ---------------------------------------------------------------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1220 0%, #0D1526 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] * {
    color: #E2E8F0 !important;
}
section[data-testid="stSidebar"] .stTextInput input,
section[data-testid="stSidebar"] .stTextArea textarea,
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
    background-color: #131E33 !important;
    border: 1px solid #263857 !important;
    color: #F1F5F9 !important;
    border-radius: 9px !important;
}
section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] { color: #14B8A6; }
section[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: #101A2E;
    border: 1px solid #22314D;
    border-radius: 12px;
    overflow: hidden;
}
section[data-testid="stSidebar"] hr { border-color: #1E2A42; }

.pq-sidebar-logo {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.15rem;
}
.pq-sidebar-mark {
    width: 34px; height: 34px;
    border-radius: 9px;
    background: linear-gradient(135deg, #14B8A6, #0B4F49);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.05rem;
    box-shadow: 0 4px 14px -4px rgba(20,184,166,0.6);
}
.pq-sidebar-brand {
    font-size: 1.22rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.pq-sidebar-tag {
    font-size: 0.76rem;
    color: #8493AC !important;
    margin: 0.15rem 0 1.2rem 2.55rem;
}
.pq-sidebar-section-label {
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748B !important;
    margin: 1.1rem 0 0.5rem 0.1rem;
}
.pq-sidebar-stat {
    background: #101A2E;
    border: 1px solid #22314D;
    border-radius: 10px;
    padding: 0.6rem 0.8rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.pq-sidebar-stat .n {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 1.05rem;
    color: #E6FFFA !important;
}

/* ---------------------------------------------------------------- */
/* Buttons                                                          */
/* ---------------------------------------------------------------- */
.stButton > button, .stDownloadButton > button {
    border-radius: 10px;
    font-weight: 700;
    border: 1px solid var(--pq-border);
    transition: box-shadow 0.15s ease, transform 0.1s ease, border-color 0.15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-1px);
}
.stButton button[kind="primary"] {
    background: linear-gradient(120deg, #0F766E, #14B8A6) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 10px 24px -10px rgba(15,118,110,0.55);
}
.stButton button[kind="primary"]:hover {
    box-shadow: 0 14px 28px -10px rgba(15,118,110,0.7);
}
section[data-testid="stSidebar"] .stButton > button {
    background: #131E33 !important;
    border: 1px solid #2A3B5C !important;
    color: #E2E8F0 !important;
}

/* ---------------------------------------------------------------- */
/* Empty state                                                      */
/* ---------------------------------------------------------------- */
.pq-empty-state {
    text-align: center;
    padding: 3.4rem 1.5rem;
    color: var(--pq-text-mute);
    border: 1.5px dashed #D3DAE2;
    border-radius: var(--pq-radius-lg);
    background:
        radial-gradient(400px 200px at 50% 0%, rgba(15,118,110,0.05), transparent 70%),
        #FBFCFD;
}
.pq-empty-icon {
    width: 62px; height: 62px;
    margin: 0 auto 0.9rem auto;
    border-radius: 16px;
    background: rgba(15,118,110,0.08);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.7rem;
}

/* ---------------------------------------------------------------- */
/* Dataframe / misc                                                 */
/* ---------------------------------------------------------------- */
[data-testid="stDataFrame"] {
    border-radius: var(--pq-radius-md);
    overflow: hidden;
    border: 1px solid var(--pq-border);
    box-shadow: var(--pq-shadow-sm);
}

.pq-caption-row {
    font-size: 0.84rem;
    color: var(--pq-text-mute);
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ---------------------------------------------------------------- */
/* Footer                                                           */
/* ---------------------------------------------------------------- */
.pq-footer {
    text-align: center;
    margin-top: 2.6rem;
    padding-top: 1.6rem;
    border-top: 1px solid var(--pq-border);
}
.pq-footer .brand {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    color: var(--pq-text-soft);
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}
.pq-footer .links {
    display: flex;
    justify-content: center;
    gap: 0.6rem;
    margin-bottom: 0.6rem;
    flex-wrap: wrap;
}
.pq-footer .links a {
    text-decoration: none;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--pq-primary-dark);
    background: rgba(15,118,110,0.08);
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    transition: background 0.15s ease;
}
.pq-footer .links a:hover { background: rgba(15,118,110,0.16); }
.pq-footer .fine-print { color: var(--pq-text-mute); font-size: 0.78rem; }
</style>
"""
