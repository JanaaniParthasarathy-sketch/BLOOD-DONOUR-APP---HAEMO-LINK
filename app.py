"""
BloodLife — Intelligent Blood-Life Coordination & Prediction Platform
Landing Page / Role Selector
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from utils.theme import inject_global_css, demo_banner, NAVY, BLUE, BLOOD_RED, GREEN, AMBER, GREY, LIGHT_BLUE

st.set_page_config(
    page_title="BloodLife — Intelligent Blood Coordination Platform",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

# ── Session defaults ──────────────────────────────────────────────────────────
if "role" not in st.session_state:
    st.session_state.role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = "Guest"

# ── Sidebar — role switcher ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="text-align:center;padding:16px 0 8px 0;">
  <span style="font-size:2rem;">🩸</span>
  <div style="font-size:1.3rem;font-weight:800;color:#FFFFFF;letter-spacing:.02em;">BloodLife</div>
  <div style="font-size:.72rem;color:#90CAF9;margin-top:2px;">Intelligent Blood Coordination</div>
</div>
<hr/>
""", unsafe_allow_html=True)

    st.markdown('<div style="font-size:.78rem;color:#90CAF9;margin-bottom:6px;text-transform:uppercase;letter-spacing:.06em;">Select Your Role</div>', unsafe_allow_html=True)

    role_options = ["🏠 Home", "👤 Donor", "🧑‍🦽 Patient / Requester",
                    "🏥 Hospital", "🩸 Blood Bank", "🛡️ Administrator"]
    selected_nav = st.radio("Navigation", role_options, label_visibility="collapsed")

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:.75rem;color:#90CAF9;">BloodLife v1.0 · Demo Mode</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.72rem;color:#607D8B;margin-top:4px;">"Connecting Every Drop to the Right Need."</div>', unsafe_allow_html=True)


# ── Page routing ──────────────────────────────────────────────────────────────
role_map = {
    "👤 Donor":              "pages/1_Donor.py",
    "🧑‍🦽 Patient / Requester":"pages/2_Patient.py",
    "🏥 Hospital":           "pages/3_Hospital.py",
    "🩸 Blood Bank":         "pages/4_BloodBank.py",
    "🛡️ Administrator":      "pages/5_Admin.py",
}

if selected_nav != "🏠 Home":
    # We show the dashboard inline using st.switch_page equivalent approach via session state
    # Since this is a single-file multi-page app structure, we'll use page switching
    page_file = role_map.get(selected_nav)
    if page_file:
        st.switch_page(page_file)

# ── Landing Hero ──────────────────────────────────────────────────────────────
demo_banner()

st.markdown(f"""
<div style="background:{NAVY};border-radius:16px;padding:52px 48px 44px 48px;margin-bottom:32px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:-40px;right:-40px;width:260px;height:260px;
       background:rgba(23,105,170,.15);border-radius:50%;"></div>
  <div style="position:absolute;bottom:-60px;right:80px;width:180px;height:180px;
       background:rgba(198,40,40,.10);border-radius:50%;"></div>
  <div style="position:relative;z-index:1;">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
      <span style="font-size:2.8rem;">🩸</span>
      <div style="font-size:3rem;font-weight:900;color:#FFFFFF;letter-spacing:-.01em;">BloodLife</div>
    </div>
    <div style="font-size:1.25rem;color:#90CAF9;font-weight:500;margin-bottom:20px;">
      "Connecting Every Drop to the Right Need."
    </div>
    <p style="color:#B0C4DE;font-size:1rem;max-width:680px;line-height:1.7;margin-bottom:28px;">
      An intelligent healthcare coordination platform connecting donors, hospitals, blood banks
      and communities through real-time matching, predictive analytics and emergency coordination.
      <br/><br/>
      <em style="color:#90CAF9;font-size:.9rem;">Powered by the BloodLife Intelligent Coordination Engine</em>
    </p>
    <div style="display:flex;gap:14px;flex-wrap:wrap;">
      <div style="background:{BLOOD_RED};color:#FFF;padding:12px 28px;border-radius:8px;font-weight:700;font-size:1rem;cursor:pointer;">
        🚨 Request Blood
      </div>
      <div style="background:{BLUE};color:#FFF;padding:12px 28px;border-radius:8px;font-weight:700;font-size:1rem;cursor:pointer;">
        🩸 Become a Donor
      </div>
      <div style="background:rgba(255,255,255,.12);color:#E8F2FA;padding:12px 28px;border-radius:8px;font-weight:600;font-size:1rem;cursor:pointer;border:1px solid rgba(255,255,255,.2);">
        🏥 Hospital / Blood Bank Login
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Platform Statistics ───────────────────────────────────────────────────────
st.markdown('<div style="font-size:1.05rem;font-weight:700;color:#607D8B;text-align:center;margin-bottom:16px;letter-spacing:.08em;text-transform:uppercase;">Platform at a Glance · Sample Data</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
tiles = [
    (c1, "8,742", "Active Donors", BLUE),
    (c2, "284",   "Verified Blood Banks", GREEN),
    (c3, "1,136", "Partner Hospitals", NAVY),
    (c4, "52,480","Requests Fulfilled", BLOOD_RED),
]
for col, num, lbl, clr in tiles:
    with col:
        st.markdown(f"""
<div class="bl-stat" style="border-top:3px solid {clr};">
  <div class="num" style="color:{clr};">{num}</div>
  <div class="lbl">{lbl}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# ── Coordination Engine Diagram ───────────────────────────────────────────────
st.markdown(f"""
<div class="bl-card" style="text-align:center;padding:32px 24px;">
  <div style="font-size:1.1rem;font-weight:700;color:{NAVY};margin-bottom:20px;">
    🧠 BloodLife Intelligent Coordination Engine
  </div>
  <div style="display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:0;font-size:.9rem;">
    <div style="background:{LIGHT_BLUE};border:2px solid {BLUE};border-radius:10px;padding:14px 20px;font-weight:600;color:{NAVY};">
      👤 Donor<br/><span style="font-size:.75rem;color:{GREY};">Availability · History</span>
    </div>
    <div style="color:{BLUE};font-size:1.4rem;padding:0 8px;">→</div>
    <div style="background:{NAVY};border-radius:12px;padding:18px 24px;font-weight:700;color:#FFFFFF;font-size:1rem;border:2px solid {BLUE};">
      🩸 BloodLife<br/><span style="font-size:.75rem;color:#90CAF9;">Intelligence Engine</span>
    </div>
    <div style="color:{BLUE};font-size:1.4rem;padding:0 8px;">→</div>
    <div style="background:{LIGHT_BLUE};border:2px solid {BLUE};border-radius:10px;padding:14px 20px;font-weight:600;color:{NAVY};">
      🏥 Hospital<br/><span style="font-size:.75rem;color:{GREY};">Requests · Urgency</span>
    </div>
  </div>
  <div style="display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:0;font-size:.9rem;margin-top:12px;">
    <div style="background:{LIGHT_BLUE};border:2px solid {BLUE};border-radius:10px;padding:14px 20px;font-weight:600;color:{NAVY};">
      🩸 Blood Bank<br/><span style="font-size:.75rem;color:{GREY};">Inventory · Expiry</span>
    </div>
    <div style="color:{BLUE};font-size:1.4rem;padding:0 8px;">→</div>
    <div style="background:{LIGHT_BLUE};border:2px solid {BLOOD_RED};border-radius:10px;padding:14px 20px;font-weight:600;color:{NAVY};">
      🧑‍🦽 Patient<br/><span style="font-size:.75rem;color:{GREY};">Requests · Tracking</span>
    </div>
    <div style="color:{BLUE};font-size:1.4rem;padding:0 8px;">→</div>
    <div style="background:{LIGHT_BLUE};border:2px solid {BLOOD_RED};border-radius:10px;padding:14px 20px;font-weight:600;color:{NAVY};">
      ✅ Fulfilment<br/><span style="font-size:.75rem;color:{GREY};">Coordination · Safety</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Role Cards ────────────────────────────────────────────────────────────────
st.markdown("<br/>", unsafe_allow_html=True)
st.markdown(f'<div style="font-size:1.15rem;font-weight:700;color:{NAVY};margin-bottom:16px;border-left:4px solid {BLOOD_RED};padding-left:12px;">Choose Your Role</div>', unsafe_allow_html=True)

roles = [
    ("👤", "Donor", "My BloodLife", "Register · Donate · Track your impact · Respond to requests", BLUE, "👤 Donor"),
    ("🧑‍🦽", "Patient / Requester", "Find Blood", "Create request · Track status · Receive updates", BLOOD_RED, "🧑‍🦽 Patient / Requester"),
    ("🏥", "Hospital", "Command Centre", "Manage emergencies · Monitor inventory · Coordinate donors", NAVY, "🏥 Hospital"),
    ("🩸", "Blood Bank", "Operations Centre", "Inventory · Donors · Expiry risk · Demand forecast", "#6A1B9A", "🩸 Blood Bank"),
    ("🛡️", "Administrator", "Network Control", "Platform analytics · Verification · Audit logs · System health", "#2E7D32", "🛡️ Administrator"),
]

col_list = st.columns(5)
for col, (icon, role, subtitle, desc, clr, nav_key) in zip(col_list, roles):
    with col:
        st.markdown(f"""
<div class="bl-card" style="border-top:3px solid {clr};text-align:center;min-height:200px;">
  <div style="font-size:2rem;">{icon}</div>
  <div style="font-weight:700;color:{NAVY};font-size:.95rem;margin-top:8px;">{role}</div>
  <div style="font-size:.78rem;color:{clr};font-weight:600;margin:4px 0 8px 0;">{subtitle}</div>
  <div style="font-size:.78rem;color:{GREY};line-height:1.5;">{desc}</div>
</div>
""", unsafe_allow_html=True)
        if st.button(f"Enter →", key=f"role_btn_{role}", use_container_width=True):
            st.switch_page(role_map.get(f"{'👤' if 'Donor' in nav_key else nav_key.split()[0]} {nav_key.split()[-1] if len(nav_key.split()) > 1 else ''}", f"pages/1_Donor.py"))

# ── AI Feature Highlights ─────────────────────────────────────────────────────
st.markdown("<br/>", unsafe_allow_html=True)
st.markdown(f'<div style="font-size:1.15rem;font-weight:700;color:{NAVY};margin-bottom:16px;border-left:4px solid {BLUE};padding-left:12px;">🧠 Intelligence Capabilities</div>', unsafe_allow_html=True)

feats = [
    ("🎯", "Dynamic Donor Matching", "Multi-factor suitability scoring across blood compatibility, availability, distance, history, and urgency."),
    ("📈", "Blood Demand Forecasting", "Predicts future blood-group and component demand from historical patterns and seasonal trends."),
    ("⚠️", "Expiry Risk Engine", "Monitors blood components approaching expiry for authorized staff review before wastage occurs."),
    ("🚨", "Emergency Escalation", "Adaptive 6-stage emergency orchestration — searches inventory, matches donors, expands radius, stops when fulfilled."),
    ("🧬", "Rare Blood Intelligence", "Dedicated network tracking verified rare-group donors and identifying regional availability gaps."),
    ("🤖", "BloodLife AI Assistant", "Operational AI copilot answering platform questions, summarising alerts, and guiding staff — never making clinical decisions."),
]

for row_start in range(0, len(feats), 3):
    cols = st.columns(3)
    for col, (icon, title, desc) in zip(cols, feats[row_start:row_start+3]):
        with col:
            st.markdown(f"""
<div class="bl-card" style="min-height:120px;">
  <div style="font-size:1.5rem;">{icon}</div>
  <div style="font-weight:700;color:{NAVY};font-size:.9rem;margin:6px 0 4px 0;">{title}</div>
  <div style="font-size:.8rem;color:{GREY};line-height:1.5;">{desc}</div>
</div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br/>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center;padding:24px;border-top:1px solid #E5E7EB;">
  <div style="font-size:.85rem;color:{GREY};">🩸 <strong>BloodLife</strong> · Intelligent Blood-Life Coordination & Prediction Platform</div>
  <div style="font-size:.78rem;color:#9DA8B0;margin-top:6px;">
    Demo Environment — All data shown is simulated. Not for clinical use.<br/>
    BloodLife does not make independent clinical transfusion decisions. All operational decisions remain with authorized healthcare professionals.
  </div>
</div>
""", unsafe_allow_html=True)
