"""
BloodLife — Donor Dashboard ("My BloodLife")
"""

import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.theme import (
    inject_global_css, demo_banner, NAVY, BLUE, BLOOD_RED, GREEN, AMBER, GREY,
    LIGHT_BLUE, AVAILABILITY_COLOURS, BLOOD_GROUPS, COMPONENTS, section_heading,
)
from data.demo_data import DONORS, REQUESTS, MONTHS

st.set_page_config(page_title="My BloodLife — Donor", page_icon="🩸", layout="wide")
inject_global_css()

# ── Session defaults ──────────────────────────────────────────────────────────
if "donor_registered" not in st.session_state:
    st.session_state.donor_registered = False
if "donor_name" not in st.session_state:
    st.session_state.donor_name = "Janaani"
if "donor_bg" not in st.session_state:
    st.session_state.donor_bg = "O+"
if "donor_avail" not in st.session_state:
    st.session_state.donor_avail = "Available Now"
if "donor_verified" not in st.session_state:
    st.session_state.donor_verified = True

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="text-align:center;padding:12px 0;">
  <span style="font-size:1.8rem;">🩸</span>
  <div style="font-size:1.2rem;font-weight:800;color:#FFF;">BloodLife</div>
  <div style="font-size:.7rem;color:#90CAF9;">Donor Portal</div>
</div><hr/>""", unsafe_allow_html=True)

    donor_tab = st.radio("Menu", [
        "🏠 My Dashboard",
        "📋 Register / Profile",
        "🗺️ Nearby Requests",
        "🏆 Impact Passport",
        "📅 Donation Planner",
        "🔔 Notifications",
        "⚙️ Settings",
    ], label_visibility="collapsed")

    st.markdown("<hr/>", unsafe_allow_html=True)
    # Quick availability toggle
    st.markdown('<div style="font-size:.75rem;color:#90CAF9;margin-bottom:4px;">Quick Availability</div>', unsafe_allow_html=True)
    avail_choice = st.selectbox("Availability",
        list(AVAILABILITY_COLOURS.keys()),
        index=list(AVAILABILITY_COLOURS.keys()).index(st.session_state.donor_avail),
        label_visibility="collapsed",
    )
    if avail_choice != st.session_state.donor_avail:
        st.session_state.donor_avail = avail_choice
        st.success("Availability updated!")

    av_clr, av_icon = AVAILABILITY_COLOURS[st.session_state.donor_avail]
    st.markdown(f'<div style="font-size:.85rem;font-weight:600;color:{av_clr};">{av_icon} {st.session_state.donor_avail}</div>', unsafe_allow_html=True)

    st.markdown("<hr/><a href='/' style='color:#90CAF9;font-size:.8rem;'>← Home</a>", unsafe_allow_html=True)

demo_banner()

# ═══════════════════════════════════════════════════════════════════════════════
# MY DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
if donor_tab == "🏠 My Dashboard":
    av_clr, av_icon = AVAILABILITY_COLOURS[st.session_state.donor_avail]

    st.markdown(f"""
<div style="background:{NAVY};border-radius:14px;padding:28px 32px;margin-bottom:24px;">
  <div style="font-size:.9rem;color:#90CAF9;margin-bottom:4px;">Good evening,</div>
  <div style="font-size:1.9rem;font-weight:800;color:#FFFFFF;">{st.session_state.donor_name} 👋</div>
  <div style="font-size:1rem;color:#B0C4DE;margin-top:6px;">🩸 Your blood can make a difference.</div>
  <div style="margin-top:14px;display:inline-block;background:{av_clr}22;border:1px solid {av_clr};
       border-radius:20px;padding:6px 16px;font-size:.88rem;font-weight:600;color:{av_clr};">
    {av_icon} {st.session_state.donor_avail}
  </div>
  <span style="margin-left:12px;background:#1769AA22;border:1px solid #1769AA;
       border-radius:20px;padding:6px 14px;font-size:.85rem;color:#90CAF9;">
    {'✅ Verified Donor' if st.session_state.donor_verified else '⏳ Verification Pending'}
  </span>
</div>
""", unsafe_allow_html=True)

    # Stats row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="bl-stat" style="border-top:3px solid {BLOOD_RED};"><div class="num" style="color:{BLOOD_RED};">8</div><div class="lbl">Donations</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="bl-stat" style="border-top:3px solid {BLUE};"><div class="num" style="color:{BLUE};">3</div><div class="lbl">Camps Attended</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="bl-stat" style="border-top:3px solid {GREEN};"><div class="num" style="color:{GREEN};">5</div><div class="lbl">Requests Assisted</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="bl-stat" style="border-top:3px solid {AMBER};"><div class="num" style="color:{AMBER};">14 days</div><div class="lbl">Next Eligible*</div></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.72rem;color:#9DA8B0;margin-top:4px;">* Eligibility is determined by the authorized blood centre at the time of donation.</div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    left, right = st.columns([3, 2])

    with left:
        section_heading("🗺️ Nearby Verified Requests")
        nearby = [r for r in REQUESTS if r["status"] in ("Searching", "Escalated", "Pending") and r["urgency"] in ("Critical","Urgent")]
        for req in nearby[:4]:
            urgency_clr = BLOOD_RED if req["urgency"] == "Critical" else AMBER
            st.markdown(f"""
<div class="bl-card" style="border-left:4px solid {urgency_clr};">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;">
    <div>
      <span style="font-weight:700;color:{NAVY};font-size:1rem;">{req['blood_group']}</span>
      <span style="font-size:.85rem;color:{GREY};margin-left:8px;">{req['component']} · {req['units']} units</span>
      <span class="badge badge-{'red' if req['urgency']=='Critical' else 'amber'}" style="margin-left:8px;">{req['urgency']}</span>
    </div>
    <span style="font-size:.8rem;color:{GREY};">~{round(__import__('random').uniform(2.1, 9.8),1)} km</span>
  </div>
  <div style="font-size:.8rem;color:{GREY};margin-top:6px;">🏥 {req['hospital']} · {req['verification']}</div>
  <div style="margin-top:10px;display:flex;gap:8px;">
    <div style="background:{GREEN};color:#FFF;padding:6px 16px;border-radius:6px;font-size:.82rem;font-weight:600;cursor:pointer;">✓ I can help</div>
    <div style="background:#F5F5F5;color:{GREY};padding:6px 14px;border-radius:6px;font-size:.82rem;cursor:pointer;">Decline</div>
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        section_heading("🗓️ Donation History")
        history = [
            ("2025-03-15", "Whole Blood", "Apollo Blood Bank",     "Verified"),
            ("2024-11-20", "RBC",         "Red Cross Blood Bank",  "Verified"),
            ("2024-08-10", "Platelets",   "Rotary TTK Blood Bank", "Verified"),
            ("2024-04-05", "Whole Blood", "Apollo Blood Bank",     "Verified"),
        ]
        for date, comp, bank, status in history:
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;padding:10px 14px;background:#FFFFFF;
     border-radius:8px;margin-bottom:8px;box-shadow:0 1px 3px rgba(0,0,0,.06);">
  <div style="width:10px;height:10px;border-radius:50%;background:{GREEN};flex-shrink:0;"></div>
  <div style="flex:1;">
    <div style="font-size:.85rem;font-weight:600;color:{NAVY};">{comp}</div>
    <div style="font-size:.75rem;color:{GREY};">{bank}</div>
  </div>
  <div style="text-align:right;">
    <div style="font-size:.75rem;color:{GREY};">{date}</div>
    <span class="badge badge-green" style="font-size:.68rem;">{status}</span>
  </div>
</div>""", unsafe_allow_html=True)

        section_heading("🔔 Alerts")
        st.markdown(f"""
<div style="background:#FFF3E0;border:1px solid {AMBER};border-radius:8px;padding:12px 14px;margin-bottom:8px;">
  <div style="font-size:.85rem;font-weight:600;color:#7B5E00;">⚠️ Critical O− request nearby</div>
  <div style="font-size:.78rem;color:#9E7000;margin-top:2px;">Apollo Hospitals · ~2.1 km · 4 units needed</div>
</div>
<div style="background:{LIGHT_BLUE};border:1px solid {BLUE};border-radius:8px;padding:12px 14px;">
  <div style="font-size:.85rem;font-weight:600;color:#0D47A1;">🎉 Donation camp this weekend</div>
  <div style="font-size:.78rem;color:#1565C0;margin-top:2px;">Red Cross Chennai · Sat 9 AM – 2 PM</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# REGISTER / PROFILE
# ═══════════════════════════════════════════════════════════════════════════════
elif donor_tab == "📋 Register / Profile":
    st.markdown(f"""
<div class="bl-header">
  <h1>👤 Donor Registration</h1>
  <p>Join the BloodLife donor network. Your information is kept private and secure.</p>
</div>""", unsafe_allow_html=True)

    with st.form("donor_reg_form"):
        st.markdown('<div class="section-heading">Personal Information</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            full_name  = st.text_input("Full Name *", value=st.session_state.donor_name)
            age        = st.number_input("Age *", min_value=18, max_value=65, value=28)
            blood_group= st.selectbox("Blood Group *", BLOOD_GROUPS)
            rh_factor  = st.selectbox("Rh Factor *", ["Positive (+)", "Negative (−)"])
        with c2:
            phone      = st.text_input("Phone Number *", help="Not publicly shown")
            email      = st.text_input("Email Address *", help="Not publicly shown")
            city       = st.text_input("City / Area *", value="Chennai")
            pref_centre= st.text_input("Preferred Donation Centre", placeholder="E.g. Red Cross Blood Bank")

        st.markdown('<div class="section-heading">Donation Details</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            last_donation = st.date_input("Last Donation Date (if any)")
            availability  = st.selectbox("Current Availability *", list(AVAILABILITY_COLOURS.keys()))
        with c4:
            emergency_notif = st.checkbox("Receive emergency notifications", value=True)
            st.markdown('<div style="font-size:.78rem;color:#607D8B;margin-top:4px;">BloodLife will only notify you for requests that match your blood group and availability window.</div>', unsafe_allow_html=True)

        st.markdown('<div style="background:#E8F5E9;border:1px solid #A5D6A7;border-radius:8px;padding:12px 16px;margin:12px 0;font-size:.82rem;color:#1B5E20;">'
                    '🔒 <strong>Privacy Notice:</strong> Your exact address is never publicly shown. '
                    'BloodLife uses approximate distance for matching. Location is only shared through authorized workflows.</div>',
                    unsafe_allow_html=True)

        submitted = st.form_submit_button("✅ Register as Donor", use_container_width=True, type="primary")
        if submitted:
            st.session_state.donor_registered = True
            st.session_state.donor_name = full_name
            st.session_state.donor_bg   = blood_group
            st.session_state.donor_avail= availability
            st.success(f"✅ Registration submitted! Welcome to BloodLife, {full_name}.")

    if st.session_state.donor_registered:
        st.markdown("<br/>", unsafe_allow_html=True)
        section_heading("🔍 Verification Status")
        st.markdown(f"""
<div class="bl-card" style="border-left:5px solid {AMBER};">
  <div style="display:flex;align-items:center;gap:12px;">
    <span style="font-size:2rem;">⏳</span>
    <div>
      <div style="font-weight:700;color:{NAVY};font-size:1rem;">Verification Pending</div>
      <div style="font-size:.85rem;color:{GREY};margin-top:2px;">
        Your registration has been submitted. Verification is conducted by an authorized blood centre.
        You will be notified once your status is updated.
      </div>
    </div>
  </div>
  <div style="margin-top:14px;display:flex;gap:10px;flex-wrap:wrap;">
    <span class="badge badge-amber">⏳ Verification Pending</span>
    <span class="badge badge-grey">📋 Profile Complete</span>
    <span class="badge badge-blue">🔔 Notifications Enabled</span>
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown(f"""
<div style="background:#F3E5F5;border:1px solid #CE93D8;border-radius:8px;padding:12px 16px;font-size:.82rem;color:#4A148C;margin-top:8px;">
  ℹ️ <strong>Note:</strong> Eligibility for blood donation is determined by the blood centre's screening process at the time of donation.
  BloodLife does not independently certify medical eligibility.
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# NEARBY REQUESTS
# ═══════════════════════════════════════════════════════════════════════════════
elif donor_tab == "🗺️ Nearby Requests":
    st.markdown(f'<div class="bl-header"><h1>🗺️ Nearby Verified Requests</h1><p>Privacy-aware blood request coordination near you.</p></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        filter_bg = st.multiselect("Filter by Blood Group", BLOOD_GROUPS, default=["O+", "O−"])
    with c2:
        filter_urgency = st.selectbox("Urgency", ["All", "Critical", "Urgent", "Routine"])

    active_reqs = [r for r in REQUESTS if r["status"] not in ("Fulfilled",)]
    for req in active_reqs:
        if filter_bg and req["blood_group"] not in filter_bg:
            continue
        if filter_urgency != "All" and req["urgency"] != filter_urgency:
            continue
        dist = round(random.uniform(1.5, 12.0), 1)
        urg_clr = BLOOD_RED if req["urgency"] == "Critical" else AMBER if req["urgency"] == "Urgent" else GREY
        ver_badge = ("badge-green", "✅ Hospital Verified") if "Hospital" in req["verification"] else \
                    ("badge-blue",  "🔵 Blood Bank Verified") if "Blood Bank" in req["verification"] else \
                    ("badge-amber", "⏳ Pending")
        st.markdown(f"""
<div class="bl-card" style="border-left:5px solid {urg_clr};">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <div style="display:flex;align-items:center;gap:12px;">
      <div style="background:{urg_clr}22;border:2px solid {urg_clr};border-radius:8px;padding:8px 14px;
           font-weight:800;font-size:1.15rem;color:{urg_clr};">{req['blood_group']}</div>
      <div>
        <div style="font-weight:700;color:{NAVY};">{req['component']} · {req['units']} units</div>
        <div style="font-size:.82rem;color:{GREY};">🏥 {req['hospital']}</div>
      </div>
    </div>
    <div style="text-align:right;">
      <div style="font-size:.9rem;font-weight:600;color:{GREY};">~{dist} km away</div>
      <span class="badge badge-{'red' if req['urgency']=='Critical' else 'amber' if req['urgency']=='Urgent' else 'grey'}">{req['urgency']}</span>
    </div>
  </div>
  <div style="margin-top:10px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
    <span class="badge {ver_badge[0]}">{ver_badge[1]}</span>
    <span style="font-size:.78rem;color:{GREY};">Created: {req['created']}</span>
  </div>
  <div style="margin-top:12px;font-size:.78rem;color:#9DA8B0;">
    📍 Approximate location only. Exact meeting/donation location shared through authorized workflow after you accept.
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# IMPACT PASSPORT
# ═══════════════════════════════════════════════════════════════════════════════
elif donor_tab == "🏆 Impact Passport":
    st.markdown(f'<div class="bl-header"><h1>🏆 Donor Impact Passport</h1><p>Your verified contribution history.</p></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="bl-stat" style="border-top:3px solid {BLOOD_RED};"><div class="num" style="color:{BLOOD_RED};">8</div><div class="lbl">Verified Donations</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="bl-stat" style="border-top:3px solid {BLUE};"><div class="num" style="color:{BLUE};">5</div><div class="lbl">Blood-Support Events</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="bl-stat" style="border-top:3px solid {GREEN};"><div class="num" style="color:{GREEN};">3</div><div class="lbl">Camps Attended</div></div>', unsafe_allow_html=True)

    st.markdown(f"""
<div style="background:{LIGHT_BLUE};border:1px solid {BLUE};border-radius:10px;padding:16px 20px;margin:16px 0;font-size:.9rem;color:#0D47A1;">
  💙 Your verified donations contributed to <strong>5 completed blood-support events</strong>.
  <br/><span style="font-size:.8rem;color:#1565C0;">Clinical impact of each donation depends on blood processing and clinical use, as determined by the receiving institution.</span>
</div>
""", unsafe_allow_html=True)

    section_heading("Contribution Timeline")
    events = [
        ("2025-03-15", "✅", "Whole Blood donation at Apollo Blood Bank — Verified", GREEN),
        ("2024-12-08", "🎪", "Attended Red Cross donation camp", BLUE),
        ("2024-11-20", "✅", "RBC donation at Red Cross Blood Bank — Verified", GREEN),
        ("2024-09-01", "🎪", "Attended Rotary TTK camp", BLUE),
        ("2024-08-10", "✅", "Platelets donation at Rotary TTK — Verified", GREEN),
        ("2024-05-15", "🎪", "Attended Government Blood Bank camp", BLUE),
        ("2024-04-05", "✅", "Whole Blood donation at Apollo Blood Bank — Verified", GREEN),
    ]
    for date, icon, label, clr in events:
        st.markdown(f"""
<div style="display:flex;gap:14px;align-items:flex-start;margin-bottom:10px;">
  <div style="width:2px;background:{clr}44;margin-left:10px;flex-shrink:0;min-height:40px;"></div>
  <div style="background:#FFFFFF;border-radius:8px;padding:10px 14px;flex:1;
       box-shadow:0 1px 3px rgba(0,0,0,.06);border-left:3px solid {clr};">
    <div style="font-size:.85rem;font-weight:600;color:{NAVY};">{icon} {label}</div>
    <div style="font-size:.75rem;color:{GREY};margin-top:2px;">{date}</div>
  </div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DONATION PLANNER
# ═══════════════════════════════════════════════════════════════════════════════
elif donor_tab == "📅 Donation Planner":
    st.markdown(f'<div class="bl-header"><h1>📅 Donation Planner</h1><p>Track your donation schedule and upcoming opportunities.</p></div>', unsafe_allow_html=True)

    st.markdown(f"""
<div style="background:#FFF3E0;border:1px solid {AMBER};border-radius:10px;padding:16px 20px;margin-bottom:20px;font-size:.88rem;color:#7B5E00;">
  ⚕️ <strong>Important:</strong> Your eligibility to donate blood is always determined by the authorized blood centre's screening
  process at the time of donation. This planner helps you track appointments — it does not certify medical eligibility.
</div>
""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        section_heading("Last Donation")
        st.info("📅 Last donation: **15 March 2025** — Whole Blood at Apollo Blood Bank")
        st.markdown('<div style="font-size:.82rem;color:#607D8B;">Next recommended opportunity (standard guideline: 56 days for whole blood) would be approximately **10 May 2025**. Confirm with your blood centre.</div>', unsafe_allow_html=True)
    with c2:
        section_heading("Upcoming Camps")
        camps = [
            ("19 Jul 2025", "Red Cross Chennai", "9 AM – 2 PM",  "Registered"),
            ("26 Jul 2025", "Apollo Blood Bank", "10 AM – 4 PM", "Open"),
            ("02 Aug 2025", "Rotary TTK",        "8 AM – 1 PM",  "Open"),
        ]
        for date, place, time, status in camps:
            clr = GREEN if status == "Registered" else BLUE
            st.markdown(f"""
<div style="background:#FFFFFF;border-radius:8px;padding:10px 14px;margin-bottom:8px;
     border-left:3px solid {clr};box-shadow:0 1px 3px rgba(0,0,0,.06);">
  <div style="font-weight:600;color:{NAVY};font-size:.88rem;">{date} · {place}</div>
  <div style="font-size:.78rem;color:{GREY};">{time}</div>
  <span class="badge {'badge-green' if status=='Registered' else 'badge-blue'}" style="margin-top:4px;">{status}</span>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════════
elif donor_tab == "🔔 Notifications":
    st.markdown(f'<div class="bl-header"><h1>🔔 Smart Notifications</h1><p>Relevant alerts matched to your blood group and availability.</p></div>', unsafe_allow_html=True)
    notifs = [
        (BLOOD_RED, "🚨", "Critical O− request nearby", "Apollo Hospitals · ~2.1 km · 4 units needed · Hospital Verified", "Just now"),
        (AMBER,     "⚠️", "Urgent A+ request",          "MIOT International · ~7.4 km · 2 units RBC · Pending Verification", "12 min ago"),
        (BLUE,      "📅", "Donation camp this Saturday", "Red Cross Chennai · 9 AM – 2 PM · Pre-register now", "1 hr ago"),
        (GREEN,     "✅", "Your donation verified",      "Apollo Blood Bank confirmed your 15 Mar 2025 donation", "Yesterday"),
    ]
    for clr, icon, title, detail, time in notifs:
        st.markdown(f"""
<div class="bl-card" style="border-left:4px solid {clr};">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;">
    <div style="display:flex;gap:10px;">
      <span style="font-size:1.3rem;">{icon}</span>
      <div>
        <div style="font-weight:600;color:{NAVY};font-size:.92rem;">{title}</div>
        <div style="font-size:.8rem;color:{GREY};margin-top:3px;">{detail}</div>
      </div>
    </div>
    <span style="font-size:.75rem;color:{GREY};white-space:nowrap;">{time}</span>
  </div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════
elif donor_tab == "⚙️ Settings":
    st.markdown(f'<div class="bl-header"><h1>⚙️ Privacy & Settings</h1><p>Control your data and notification preferences.</p></div>', unsafe_allow_html=True)

    section_heading("Privacy Controls")
    st.toggle("Share approximate location for matching", value=True, help="BloodLife never shares your exact address.")
    st.toggle("Receive emergency blood request notifications", value=True)
    st.toggle("Receive donation camp reminders", value=True)
    st.toggle("Appear in donor search results", value=True)

    section_heading("Notification Preferences")
    st.multiselect("Notify me for blood groups", BLOOD_GROUPS, default=["O+", "O−"])
    st.selectbox("Notification method", ["App notification", "SMS", "Both"])
    st.slider("Maximum notification radius (km)", 1, 50, 15)

    st.markdown(f"""
<div style="background:{LIGHT_BLUE};border:1px solid {BLUE};border-radius:8px;padding:14px 18px;margin-top:16px;font-size:.82rem;color:#0D47A1;">
  🔒 <strong>Data Privacy:</strong> BloodLife stores only the minimum information necessary for coordination.
  Your exact address is never publicly visible. You may request deletion of your data at any time.
</div>""", unsafe_allow_html=True)

    if st.button("Save Settings", type="primary"):
        st.success("Settings saved successfully.")
