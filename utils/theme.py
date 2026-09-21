"""BloodLife — shared branding, CSS injection, and UI helper utilities."""

import streamlit as st

# ── Colour palette ──────────────────────────────────────────────────────────
NAVY       = "#0B1F33"
BLUE       = "#1769AA"
BLOOD_RED  = "#C62828"
EMERG_RED  = "#B71C1C"
WHITE      = "#FFFFFF"
BG         = "#F5F8FC"
GREEN      = "#2E7D32"
AMBER      = "#F9A825"
GREY       = "#607D8B"
LIGHT_BLUE = "#E8F2FA"

AVAILABILITY_COLOURS = {
    "Available Now":          ("#2E7D32", "🟢"),
    "Available Today":        ("#F9A825", "🟡"),
    "Available Later":        ("#1769AA", "🔵"),
    "Unavailable":            ("#607D8B", "⚪"),
    "Temporarily Unavailable":("#C62828", "🔴"),
}

BLOOD_GROUPS = ["O+", "O−", "A+", "A−", "B+", "B−", "AB+", "AB−"]

COMPONENTS = [
    "Whole Blood",
    "Packed Red Blood Cells (RBC)",
    "Platelets",
    "Fresh Frozen Plasma (FFP)",
    "Cryoprecipitate",
]

URGENCY_LEVELS = ["Critical", "Urgent", "Routine"]


def inject_global_css():
    st.markdown(
        """
<style>
/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: -apple-system, "Segoe UI", system-ui, sans-serif;
}
[data-testid="stAppViewContainer"] > .main {background:#F5F8FC;}
[data-testid="stSidebar"] {background:#0B1F33 !important;}
[data-testid="stSidebar"] * {color:#E8F2FA !important;}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label {color:#E8F2FA !important;}
[data-testid="stSidebar"] hr {border-color:#1769AA44;}
[data-testid="stSidebar"] a {color:#90CAF9 !important;}

/* ── Cards ── */
.bl-card {
    background:#FFFFFF;
    border-radius:12px;
    padding:20px 24px;
    box-shadow:0 1px 6px rgba(11,31,51,.08);
    margin-bottom:16px;
}
.bl-card-dark {
    background:#0B1F33;
    border-radius:12px;
    padding:20px 24px;
    box-shadow:0 2px 10px rgba(0,0,0,.25);
    margin-bottom:16px;
    color:#E8F2FA;
}

/* ── Stat tiles ── */
.bl-stat {
    background:#FFFFFF;
    border-radius:10px;
    padding:18px 20px;
    box-shadow:0 1px 4px rgba(11,31,51,.07);
    text-align:center;
}
.bl-stat .num {font-size:2.2rem;font-weight:700;line-height:1.1;}
.bl-stat .lbl {font-size:.82rem;color:#607D8B;margin-top:4px;text-transform:uppercase;letter-spacing:.06em;}

/* ── Badges ── */
.badge {
    display:inline-block;
    padding:3px 10px;
    border-radius:20px;
    font-size:.75rem;
    font-weight:600;
    letter-spacing:.04em;
}
.badge-green  {background:#E8F5E9;color:#2E7D32;}
.badge-blue   {background:#E3F2FD;color:#1769AA;}
.badge-amber  {background:#FFF8E1;color:#F57F17;}
.badge-red    {background:#FFEBEE;color:#C62828;}
.badge-grey   {background:#ECEFF1;color:#455A64;}
.badge-navy   {background:#E8F2FA;color:#0B1F33;}

/* ── Header banner ── */
.bl-header {
    background:#0B1F33;
    border-radius:12px;
    padding:28px 32px;
    margin-bottom:24px;
    color:#FFFFFF;
}
.bl-header h1 {color:#FFFFFF;font-size:1.9rem;margin:0 0 4px 0;}
.bl-header p  {color:#90CAF9;margin:0;font-size:1rem;}

/* ── Section headings ── */
.section-heading {
    font-size:1.1rem;
    font-weight:700;
    color:#0B1F33;
    border-left:4px solid #1769AA;
    padding-left:10px;
    margin:20px 0 12px 0;
}

/* ── Emergency stripe ── */
.emergency-stripe {
    background:#B71C1C;
    color:#FFFFFF;
    border-radius:8px;
    padding:10px 18px;
    font-weight:600;
    font-size:.9rem;
    margin-bottom:12px;
    display:flex;
    align-items:center;
    gap:10px;
}

/* ── Demo banner ── */
.demo-banner {
    background:#FFF8E1;
    border:1px solid #F9A825;
    border-radius:8px;
    padding:8px 16px;
    font-size:.8rem;
    color:#7B5E00;
    margin-bottom:16px;
}

/* ── Timeline ── */
.tl-step {display:flex;align-items:flex-start;gap:14px;margin-bottom:10px;}
.tl-dot  {width:14px;height:14px;border-radius:50%;margin-top:4px;flex-shrink:0;}
.tl-line {width:2px;height:24px;margin-left:6px;background:#E0E7EF;}

/* ── Inventory cell colours ── */
.inv-ok       {color:#2E7D32;font-weight:600;}
.inv-low      {color:#F9A825;font-weight:600;}
.inv-critical {color:#C62828;font-weight:600;}

/* ── Primary button override ── */
.stButton > button {
    border-radius:8px;
    font-weight:600;
    transition:opacity .15s;
}
.stButton > button:hover {opacity:.88;}

/* ── Input fields ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    border-radius:8px !important;
}
</style>
""",
        unsafe_allow_html=True,
    )


def demo_banner():
    st.markdown(
        '<div class="demo-banner">⚠️  <strong>Demo Environment</strong> — All data shown is simulated for demonstration purposes only.</div>',
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = "", icon: str = "🩸"):
    st.markdown(
        f"""
<div class="bl-header">
  <h1>{icon} {title}</h1>
  {"<p>" + subtitle + "</p>" if subtitle else ""}
</div>""",
        unsafe_allow_html=True,
    )


def stat_tile(num: str, label: str, colour: str = BLUE):
    return f"""
<div class="bl-stat">
  <div class="num" style="color:{colour};">{num}</div>
  <div class="lbl">{label}</div>
</div>"""


def badge(text: str, kind: str = "blue") -> str:
    return f'<span class="badge badge-{kind}">{text}</span>'


def section_heading(text: str):
    st.markdown(f'<div class="section-heading">{text}</div>', unsafe_allow_html=True)


def card_open(dark: bool = False):
    cls = "bl-card-dark" if dark else "bl-card"
    st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)


def card_close():
    st.markdown("</div>", unsafe_allow_html=True)
