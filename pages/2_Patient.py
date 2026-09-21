"""
BloodLife — Patient / Requester Interface ("Find Blood")
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import time
from utils.theme import (
    inject_global_css, demo_banner, NAVY, BLUE, BLOOD_RED, GREEN, AMBER, GREY,
    LIGHT_BLUE, BLOOD_GROUPS, COMPONENTS, section_heading,
)
from data.demo_data import REQUESTS, BLOOD_BANKS, HOSPITALS, DONORS

st.set_page_config(page_title="Find Blood — BloodLife", page_icon="🚨", layout="wide")
inject_global_css()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="text-align:center;padding:12px 0;">
  <span style="font-size:1.8rem;">🚨</span>
  <div style="font-size:1.2rem;font-weight:800;color:#FFF;">BloodLife</div>
  <div style="font-size:.7rem;color:#90CAF9;">Patient Portal</div>
</div><hr/>""", unsafe_allow_html=True)

    nav = st.radio("Menu", [
        "🚨 Request Blood",
        "📊 My Requests",
        "🔍 Track Request",
        "ℹ️ Information",
    ], label_visibility="collapsed")

    st.markdown("<hr/><a href='/' style='color:#90CAF9;font-size:.8rem;'>← Home</a>", unsafe_allow_html=True)

demo_banner()

# ═══════════════════════════════════════════════════════════════════════════════
# REQUEST BLOOD — main form
# ═══════════════════════════════════════════════════════════════════════════════
if nav == "🚨 Request Blood":

    st.markdown(f"""
<div style="background:{BLOOD_RED};border-radius:14px;padding:28px 32px;margin-bottom:24px;color:#FFF;">
  <div style="font-size:2rem;font-weight:900;">🚨 Request Blood</div>
  <div style="font-size:.95rem;color:#FFCDD2;margin-top:6px;">
    BloodLife will search verified blood-bank resources and coordinate eligible donor notifications.
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Step 1: What do you need? ──
    section_heading("Step 1 — What do you need?")

    c1, c2, c3 = st.columns(3)
    with c1:
        blood_group = st.selectbox("🩸 Blood Group *", BLOOD_GROUPS)
    with c2:
        component = st.selectbox("💉 Blood Component *", [
            "Packed Red Blood Cells (RBC)",
            "Platelets",
            "Fresh Frozen Plasma (FFP)",
            "Whole Blood",
            "Cryoprecipitate",
        ])
    with c3:
        units = st.number_input("📦 Units Required *", min_value=1, max_value=20, value=2)

    c4, c5 = st.columns(2)
    with c4:
        urgency = st.selectbox("🔴 Urgency *", ["Critical", "Urgent", "Routine"])
    with c5:
        required_by = st.text_input("⏰ Required By *", placeholder="E.g. Today 6 PM / Within 4 hours")

    section_heading("Step 2 — Where?")
    c6, c7 = st.columns(2)
    with c6:
        hospital_name = st.selectbox("🏥 Hospital *", [h["name"] for h in HOSPITALS])
    with c7:
        ward = st.text_input("Ward / Department", placeholder="E.g. ICU, Surgery Ward 3")

    section_heading("Step 3 — Contact & Verification")
    c8, c9 = st.columns(2)
    with c8:
        contact_name  = st.text_input("Contact Person Name *")
        contact_phone = st.text_input("Contact Phone *", help="Not publicly shown")
    with c9:
        doctor_name   = st.text_input("Attending Doctor (if known)")
        notes         = st.text_area("Additional Notes", height=80, placeholder="E.g. post-operative, dengue thrombocytopenia...")

    st.markdown(f"""
<div style="background:{LIGHT_BLUE};border:1px solid {BLUE};border-radius:8px;padding:12px 16px;margin:12px 0;font-size:.82rem;color:#0D47A1;">
  ℹ️ Requests with hospital verification are prioritised in the BloodLife coordination engine.
  If your hospital is registered with BloodLife, an authorized representative can verify this request.
</div>
""", unsafe_allow_html=True)

    col_btn, col_info = st.columns([1, 2])
    with col_btn:
        find_btn = st.button("🔎 Find Resources", use_container_width=True, type="primary")

    # ── Search results ────────────────────────────────────────────────────────
    if find_btn:
        if not contact_name or not contact_phone:
            st.error("Please fill in all required fields (*).")
        else:
            # Simulate request ID
            import random, string
            req_id = "BL-" + str(random.randint(1050, 1999))
            st.session_state["last_req_id"] = req_id

            # Progress simulation
            progress_bar = st.progress(0)
            status_text  = st.empty()

            stages = [
                (15, "🔍 Verifying request..."),
                (30, "🏥 Checking hospital verification..."),
                (50, "🩸 Searching blood-bank inventory..."),
                (70, "👥 Scoring eligible donor pool..."),
                (90, "📡 Preparing coordination plan..."),
                (100, f"✅ Request {req_id} created!"),
            ]
            for pct, msg in stages:
                progress_bar.progress(pct)
                status_text.markdown(f'<div style="font-size:.9rem;color:{NAVY};font-weight:500;">{msg}</div>', unsafe_allow_html=True)
                time.sleep(0.4)

            st.success(f"✅ Request **{req_id}** has been created and is now being coordinated.")

            # Status tracker
            st.markdown("<br/>", unsafe_allow_html=True)
            section_heading(f"Request Status — {req_id}")

            urgency_clr = BLOOD_RED if urgency == "Critical" else AMBER if urgency == "Urgent" else GREY
            found_bb = [bb for bb in BLOOD_BANKS if bb["verified"]][:2]
            found_donors = [d for d in DONORS if d["blood_group"] == blood_group and d["availability"] == "Available Now"][:3]

            st.markdown(f"""
<div class="bl-card" style="border-left:5px solid {urgency_clr};">
  <div style="font-size:1.1rem;font-weight:700;color:{NAVY};margin-bottom:12px;">{req_id} · {blood_group} {component} · {units} units</div>
  <div style="display:flex;gap:24px;flex-wrap:wrap;">
    <div>
      <div style="font-size:.78rem;color:{GREY};text-transform:uppercase;letter-spacing:.06em;">Urgency</div>
      <span class="badge badge-{'red' if urgency=='Critical' else 'amber' if urgency=='Urgent' else 'grey'}">{urgency}</span>
    </div>
    <div>
      <div style="font-size:.78rem;color:{GREY};text-transform:uppercase;letter-spacing:.06em;">Hospital</div>
      <div style="font-size:.9rem;font-weight:600;color:{NAVY};">{hospital_name}</div>
    </div>
    <div>
      <div style="font-size:.78rem;color:{GREY};text-transform:uppercase;letter-spacing:.06em;">Verification</div>
      <span class="badge badge-amber">⏳ Pending Verification</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

            # Stage tracker
            stages_visual = [
                (GREEN,  "✅", "Request Created",      "Submitted and logged"),
                (BLUE,   "🔵", "Inventory Search",     f"{len(found_bb)} blood banks checked"),
                (BLUE,   "🔵", "Donor Coordination",   f"{len(found_donors)} eligible donors identified"),
                (AMBER,  "⏳", "Notifications Sent",   "Awaiting donor responses"),
                (GREY,   "⚪", "Fulfilment Pending",   "—"),
            ]
            st.markdown('<div style="display:flex;gap:0;flex-wrap:wrap;margin:16px 0;">', unsafe_allow_html=True)
            for i, (clr, icon, stage, detail) in enumerate(stages_visual):
                connector = ' <span style="color:#CBD5E0;font-size:1.2rem;padding:0 4px;">→</span>' if i < len(stages_visual)-1 else ""
                st.markdown(f"""
<span style="display:inline-flex;flex-direction:column;align-items:center;padding:8px 12px;
  background:#F7F8FA;border-radius:8px;margin:4px;min-width:110px;border:1px solid #E5E7EB;">
  <span style="font-size:1.1rem;">{icon}</span>
  <span style="font-size:.75rem;font-weight:600;color:{NAVY};margin-top:2px;text-align:center;">{stage}</span>
  <span style="font-size:.68rem;color:{GREY};text-align:center;">{detail}</span>
</span>{connector}""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Blood bank results
            if found_bb:
                st.markdown(f'<div style="font-weight:600;color:{NAVY};margin:12px 0 8px 0;">🩸 Blood Banks Checked</div>', unsafe_allow_html=True)
                for bb in found_bb:
                    st.markdown(f"""
<div style="background:#F7F8FA;border-radius:8px;padding:10px 14px;margin-bottom:6px;
     border-left:3px solid {BLUE};display:flex;justify-content:space-between;align-items:center;">
  <div>
    <div style="font-weight:600;color:{NAVY};font-size:.88rem;">✅ {bb['name']}</div>
    <div style="font-size:.78rem;color:{GREY};">~{bb['distance_km']} km · Verified</div>
  </div>
  <span class="badge badge-blue">Inventory Available</span>
</div>""", unsafe_allow_html=True)

            st.markdown(f"""
<div style="background:#E8F5E9;border:1px solid #A5D6A7;border-radius:8px;padding:12px 16px;margin-top:12px;font-size:.82rem;color:#1B5E20;">
  ✅ Request active. You will be notified as resources are confirmed.
  Authorized hospital staff can verify this request to give it higher priority in the coordination engine.
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MY REQUESTS
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "📊 My Requests":
    st.markdown(f'<div class="bl-header"><h1>📊 My Requests</h1><p>Track all your blood requests.</p></div>', unsafe_allow_html=True)

    sample_requests = REQUESTS[:5]
    for req in sample_requests:
        st_map = {
            "Fulfilled":          (GREEN,     "✅ Fulfilled"),
            "Searching":          (BLOOD_RED, "🔍 Searching"),
            "Partially Fulfilled":(AMBER,     "⚠️ Partial"),
            "Donor Contacted":    (BLUE,      "📡 Donor Contacted"),
            "Pending":            (GREY,      "⏳ Pending"),
            "Escalated":          (BLOOD_RED, "🚨 Escalated"),
        }
        sc, sl = st_map.get(req["status"], (GREY, req["status"]))
        st.markdown(f"""
<div class="bl-card" style="border-left:5px solid {sc};">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <div>
      <div style="font-weight:700;color:{NAVY};">{req['id']} · {req['blood_group']} {req['component']}</div>
      <div style="font-size:.82rem;color:{GREY};">🏥 {req['hospital']} · {req['units']} units · {req['urgency']}</div>
      <div style="font-size:.78rem;color:{GREY};margin-top:2px;">Created: {req['created']}</div>
    </div>
    <div style="text-align:right;">
      <div style="font-weight:600;color:{sc};font-size:.9rem;">{sl}</div>
      <span class="badge {'badge-green' if 'Hospital' in req['verification'] else 'badge-amber'}" style="margin-top:4px;">{req['verification']}</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TRACK REQUEST
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "🔍 Track Request":
    st.markdown(f'<div class="bl-header"><h1>🔍 Track a Request</h1><p>Enter your BloodLife request ID.</p></div>', unsafe_allow_html=True)

    track_id = st.text_input("Enter Request ID", placeholder="E.g. BL-1042")
    if st.button("Track →", type="primary"):
        matched = next((r for r in REQUESTS if r["id"] == track_id.strip()), None)
        if not matched:
            st.warning("Request not found. Please check the ID and try again.")
        else:
            sc = {"Fulfilled": GREEN, "Searching": BLOOD_RED, "Pending": AMBER, "Escalated": BLOOD_RED}.get(matched["status"], BLUE)
            st.markdown(f"""
<div class="bl-card" style="border-left:5px solid {sc};">
  <div style="font-size:1.05rem;font-weight:700;color:{NAVY};margin-bottom:12px;">{matched['id']}</div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;">
    <div><div style="font-size:.75rem;color:{GREY};text-transform:uppercase;">Blood Group</div>
         <div style="font-weight:600;color:{NAVY};">{matched['blood_group']}</div></div>
    <div><div style="font-size:.75rem;color:{GREY};text-transform:uppercase;">Component</div>
         <div style="font-weight:600;color:{NAVY};">{matched['component']}</div></div>
    <div><div style="font-size:.75rem;color:{GREY};text-transform:uppercase;">Units</div>
         <div style="font-weight:600;color:{NAVY};">{matched['units']}</div></div>
    <div><div style="font-size:.75rem;color:{GREY};text-transform:uppercase;">Hospital</div>
         <div style="font-weight:600;color:{NAVY};">{matched['hospital']}</div></div>
    <div><div style="font-size:.75rem;color:{GREY};text-transform:uppercase;">Urgency</div>
         <span class="badge badge-{'red' if matched['urgency']=='Critical' else 'amber'}">{matched['urgency']}</span></div>
    <div><div style="font-size:.75rem;color:{GREY};text-transform:uppercase;">Status</div>
         <div style="font-weight:700;color:{sc};">{matched['status']}</div></div>
  </div>
  <div style="margin-top:14px;">
    <span class="badge {'badge-green' if 'Hospital' in matched['verification'] else 'badge-blue' if 'Blood Bank' in matched['verification'] else 'badge-amber'}">{matched['verification']}</span>
    <span style="font-size:.78rem;color:{GREY};margin-left:10px;">Created: {matched['created']}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INFORMATION
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "ℹ️ Information":
    st.markdown(f'<div class="bl-header"><h1>ℹ️ Blood Information Guide</h1><p>Common questions about blood donation and transfusion.</p></div>', unsafe_allow_html=True)

    faqs = [
        ("What blood components are available?",
         "BloodLife supports requests for Whole Blood, Packed Red Blood Cells (RBC), Platelets, Fresh Frozen Plasma (FFP), and Cryoprecipitate. The specific component needed depends on clinical requirements determined by your medical team."),
        ("How does BloodLife verify requests?",
         "Requests can be verified by registered hospitals or blood banks. Verified requests receive higher coordination priority. Verification status is always shown on the request."),
        ("Is my request information kept private?",
         "Yes. BloodLife shares only the minimum information necessary for coordination. Donors only see approximate distance and blood group — never patient personal details."),
        ("How long does coordination take?",
         "For critical requests with hospital verification, BloodLife begins coordination immediately. Response time depends on local availability and donor responses. The system continuously updates the request status."),
        ("What if no blood is found immediately?",
         "BloodLife escalates automatically — expanding search radius and checking additional blood banks. You will receive status updates throughout the process."),
        ("Can I cancel a request?",
         "Yes. If blood is no longer needed (e.g. patient has been discharged), please update or close the request so donors and blood banks are not unnecessarily notified."),
    ]
    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(f'<div style="font-size:.88rem;color:{GREY};line-height:1.6;">{a}</div>', unsafe_allow_html=True)

    st.markdown(f"""
<div style="background:#FFEBEE;border:1px solid #EF9A9A;border-radius:8px;padding:14px 18px;margin-top:16px;font-size:.82rem;color:#B71C1C;">
  ⚕️ <strong>Medical Disclaimer:</strong> BloodLife is a coordination platform. It does not provide medical advice,
  diagnose conditions, or make clinical transfusion decisions. All clinical decisions are made by qualified healthcare professionals.
</div>""", unsafe_allow_html=True)
