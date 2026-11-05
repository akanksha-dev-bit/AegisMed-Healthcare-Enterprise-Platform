"""
Global Design System Theme Tokens for Rumah Sakit Anaverse & AegisMed Platform.
Shared across Landing Page, Dashboard, and Inner Pages.
"""

# Color Palette
PRIMARY = "#1E2FE0"        # Royal blue (buttons, links, accents)
PRIMARY_DARK = "#0F1B8C"   # Hover, footer, dark sections
PRIMARY_LIGHT = "#E8EDFF"  # Icon circles, badges, soft backgrounds
NAVY = "#0B1340"           # Headings, dark CTA banner
TEXT = "#1F2937"           # Dark charcoal for primary body text
TEXT_MUTED = "#6B7280"     # Neutral gray for muted text & metadata
BG = "#F5F8FF"             # Page background (very light blue-white)
CARD = "#FFFFFF"           # Clean white card surfaces
STAR = "#F5B301"           # Rating stars & highlights
SUCCESS = "#16A34A"        # Success green
BORDER = "rgba(30, 47, 224, 0.10)"

THEME_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

  :root {
    --primary:        #1E2FE0;
    --primary-dark:   #0F1B8C;
    --primary-light:  #E8EDFF;
    --navy:           #0B1340;
    --text:           #1F2937;
    --text-muted:     #6B7280;
    --bg:             #F5F8FF;
    --card:           #FFFFFF;
    --star:           #F5B301;
    --success:        #16A34A;
    --border:         rgba(30, 47, 224, 0.10);
    --border-hover:   rgba(30, 47, 224, 0.28);
    --shadow-sm:      0 4px 14px rgba(30, 47, 224, 0.05);
    --shadow-md:      0 10px 40px rgba(30, 47, 224, 0.08);
    --shadow-lg:      0 20px 50px rgba(11, 19, 64, 0.12);
    --shadow-glow:    0 0 24px rgba(30, 47, 224, 0.22);
    --radius-btn:     12px;
    --radius-card:    22px;
    --radius-pill:    999px;
  }

  /* ── Reset & Typography ── */
  html, body, [class*="st-"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--text);
  }

  /* ── Background with soft gradient blobs & faint medical cross watermark ── */
  .stApp {
    background-color: var(--bg) !important;
    background-image:
      radial-gradient(circle at 10% 12%, rgba(30, 47, 224, 0.04) 0%, transparent 45%),
      radial-gradient(circle at 90% 25%, rgba(15, 27, 140, 0.04) 0%, transparent 40%),
      radial-gradient(circle at 50% 80%, rgba(30, 47, 224, 0.03) 0%, transparent 50%),
      radial-gradient(circle at 85% 85%, rgba(11, 19, 64, 0.03) 0%, transparent 45%);
    background-attachment: fixed;
  }

  /* Watermark Cross Pattern */
  .stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image: radial-gradient(circle, rgba(30,47,224,0.06) 1.5px, transparent 1.5px);
    background-size: 48px 48px;
    opacity: 0.65;
    pointer-events: none;
    z-index: 0;
  }

  /* ── Hide Streamlit Elements ── */
  [data-testid="stSidebar"] { display: none !important; }
  section[data-testid="stSidebar"] { display: none !important; }
  [data-testid="collapsedControl"] { display: none !important; }
  #MainMenu, header, footer { visibility: hidden; }

  .block-container {
    padding-top: 1rem !important;
    padding-bottom: 5.5rem !important;
    max-width: 1360px !important;
    position: relative;
    z-index: 1;
  }

  /* ── Global Top Navbar ── */
  .rs-navbar {
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 0.85rem 1.6rem;
    margin-bottom: 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: var(--shadow-md);
    position: sticky;
    top: 0.8rem;
    z-index: 999;
    transition: all 0.3s ease;
  }
  .rs-navbar-brand {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    text-decoration: none;
  }
  .rs-logo-box {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 14px rgba(30, 47, 224, 0.3);
    color: white;
    font-size: 1.4rem;
    font-weight: 800;
  }
  .rs-brand-text {
    display: flex;
    flex-direction: column;
  }
  .rs-brand-name {
    font-size: 1.12rem;
    font-weight: 800;
    color: var(--navy);
    letter-spacing: -0.02em;
    line-height: 1.15;
  }
  .rs-brand-sub {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--primary);
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  /* ── Pill Badges ── */
  .rs-pill-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.45rem 1.1rem;
    border-radius: var(--radius-pill);
    background: var(--primary-light);
    color: var(--primary);
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    margin-bottom: 1rem;
    border: 1px solid rgba(30, 47, 224, 0.12);
  }

  /* ── Cards & Surfaces ── */
  .rs-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 1.6rem;
    box-shadow: var(--shadow-md);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    position: relative;
    overflow: hidden;
  }
  .rs-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 45px rgba(30, 47, 224, 0.12);
    border-color: var(--border-hover);
  }

  /* Floating Glass Card (white 80% + blur 12px) */
  .rs-glass-card {
    background: rgba(255, 255, 255, 0.84);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.9);
    border-radius: var(--radius-card);
    box-shadow: var(--shadow-lg);
  }

  /* ── Dashboard Metric Cards ── */
  .rs-metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 1.35rem 1.5rem;
    box-shadow: var(--shadow-sm);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    height: 100%;
  }
  .rs-metric-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
    border-color: var(--primary-light);
  }
  .rs-metric-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: var(--primary-light);
    color: var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
    margin-bottom: 0.85rem;
  }
  .rs-metric-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .rs-metric-value {
    font-size: 2.1rem;
    font-weight: 800;
    color: var(--navy);
    line-height: 1.15;
    margin: 0.25rem 0;
  }
  .rs-metric-sub {
    font-size: 0.8rem;
    color: var(--text-muted);
  }

  /* ── Section Header Banner ── */
  .rs-page-banner {
    background: linear-gradient(135deg, var(--navy) 0%, #152570 50%, var(--primary) 100%);
    border-radius: var(--radius-card);
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.6rem;
    color: white;
    box-shadow: 0 16px 40px rgba(11, 19, 64, 0.22);
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    overflow: hidden;
  }
  .rs-page-banner::after {
    content: "+";
    position: absolute;
    right: 2rem;
    top: -1.5rem;
    font-size: 12rem;
    font-weight: 900;
    color: rgba(255, 255, 255, 0.05);
    pointer-events: none;
    line-height: 1;
  }
  .rs-page-banner h1 {
    font-size: 1.85rem;
    font-weight: 800;
    color: white !important;
    margin: 0 0 0.35rem 0;
  }
  .rs-page-banner p {
    color: rgba(255, 255, 255, 0.82) !important;
    font-size: 0.95rem;
    margin: 0;
  }

  /* ── Segmented Control & Navigation Styling ── */
  div[data-testid="stSegmentedControl"] {
    background: white !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-pill) !important;
    padding: 0.35rem !important;
    box-shadow: var(--shadow-sm) !important;
  }
  div[data-testid="stSegmentedControl"] button {
    border-radius: var(--radius-pill) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: var(--text-muted) !important;
    border: none !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.2s ease !important;
  }
  div[data-testid="stSegmentedControl"] button[data-state="on"],
  div[data-testid="stSegmentedControl"] button[aria-selected="true"] {
    background: var(--primary) !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(30, 47, 224, 0.35) !important;
  }

  /* ── Tabs Styling ── */
  .stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: var(--radius-pill);
    padding: 0.35rem;
    gap: 0.35rem;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-pill);
    padding: 0.55rem 1.35rem;
    color: var(--text-muted) !important;
    font-weight: 600;
    font-size: 0.9rem;
    border: none !important;
  }
  .stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(30, 47, 224, 0.32);
  }
  .stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.25rem !important;
  }

  /* ── Inputs & Selects ── */
  .stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: white !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius-btn) !important;
    padding: 0.65rem 1rem !important;
    font-size: 0.92rem !important;
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.03) !important;
  }
  .stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(30, 47, 224, 0.15) !important;
  }

  /* ── Buttons ── */
  .stButton > button {
    background: var(--primary) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-btn) !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    padding: 0.6rem 1.6rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 16px rgba(30, 47, 224, 0.28) !important;
  }
  .stButton > button:hover {
    background: var(--primary-dark) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(30, 47, 224, 0.35) !important;
  }

  /* ── Chat Messages ── */
  .rs-chat-user {
    background: linear-gradient(135deg, var(--primary) 0%, #3B4DFF 100%);
    color: white;
    padding: 0.9rem 1.3rem;
    border-radius: 20px 20px 4px 20px;
    margin: 0.5rem 0 0.5rem 25%;
    font-size: 0.93rem;
    box-shadow: 0 4px 14px rgba(30, 47, 224, 0.22);
  }
  .rs-chat-bot {
    background: white;
    color: var(--text);
    border: 1px solid var(--border);
    padding: 0.9rem 1.3rem;
    border-radius: 20px 20px 20px 4px;
    margin: 0.5rem 25% 0.5rem 0;
    font-size: 0.93rem;
    line-height: 1.6;
    box-shadow: var(--shadow-sm);
  }

  /* ── Key-Value Extraction Rows ── */
  .rs-ext-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(30, 47, 224, 0.07);
    font-size: 0.9rem;
  }
  .rs-ext-row .key {
    color: var(--text-muted);
    font-weight: 500;
  }
  .rs-ext-row .val {
    color: var(--navy);
    font-weight: 700;
    text-align: right;
  }

  /* ── Citations & Policy ── */
  .rs-citation-box {
    background: white;
    border-left: 4px solid var(--primary);
    border-radius: 0 14px 14px 0;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.85rem;
    box-shadow: var(--shadow-sm);
    border-top: 1px solid var(--border);
    border-right: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
  }

  /* ── Sticky Real-time Footer ── */
  .rs-sticky-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 9999;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-top: 1px solid var(--border);
    padding: 0.65rem 2.2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.82rem;
    color: var(--text-muted);
    box-shadow: 0 -4px 20px rgba(11, 19, 64, 0.06);
  }
  .rs-footer-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.25rem 0.75rem;
    border-radius: var(--radius-pill);
    background: var(--bg);
    border: 1px solid var(--border);
    font-size: 0.76rem;
    font-weight: 600;
  }
  .rs-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }
  .rs-dot-online  { background: var(--success); box-shadow: 0 0 6px var(--success); }
  .rs-dot-offline { background: #EF4444; box-shadow: 0 0 6px #EF4444; }

  /* ── Animations ── */
  @keyframes floatSlow {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-10px) rotate(2deg); }
  }
  .animate-float {
    animation: floatSlow 5s ease-in-out infinite;
  }
  .animate-float-delayed {
    animation: floatSlow 6s ease-in-out 1.5s infinite;
  }
</style>
"""

