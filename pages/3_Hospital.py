"""
BloodLife — Hospital Command Centre
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.theme import (
    inject_global_css, demo_banner, NAVY, BLUE, BLOOD_RED, GREEN, AMBER, GREY,
    LIGHT_BLUE, BLOOD_GROUPS, COMPONENTS, section_heading,
)
from data.demo_data import (
    REQUESTS, BLOOD_BANKS, DONORS, INVENTORY, AUDIT_LOG,
    MONTHS, REQUEST_TREND, FULFILMENT_TREND, PLATFORM_STATS,
)

st.set_page_config(page_title="Hospital Command Centre — BloodLife", page_icon="🏥", layout="wide")
inject_global_css()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="text-align:center;padding:12px 0;">
  <span style="font-size:1.8rem;">🏥</span>
  <div style="font-size:1.2rem;font-weight:800;color:#FFF;">BloodLife</div>
  <div style="font-size:.7rem;color:#90CAF9;">Hospital Command Centre</div>
</div><hr/>""", unsafe_allow_html=True)

    nav = st.radio("Module", [
        "🏠 Overview",
        "🚨 Emergency Requests",
        "📋 All Requests",
        "🩸 Blood Availability",
        "👥 Donor Responses",
        "🏦 Nearby Blood Banks",
        "📈 Analytics",
        "🤖 AI Copilot",
        "📝 Audit Log",
    ], label_visibility="collapsed")

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:.75rem;color:#90CAF9;">Apollo Hospitals, Chennai</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.7rem;color:#607D8B;margin-top:2px;">Dr. R. Anand · Blood Bank Coordinator</div>', unsafe_allow_html=True)
    st.markdown("<hr/><a href='/' style='color:#90CAF9;font-size:.8rem;'>← Home</a>", unsafe_allow_html=True)

demo_banner()

# ═══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if nav == "🏠 Overview":
    st.markdown(f"""
<div style="background:{NAVY};border-radius:14px;padding:24px 32px;margin-bottom:24px;color:#FFF;">
  <div style="font-size:1.6rem;font-weight:800;">🏥 Hospital Command Centre</div>
  <div style="font-size:.9rem;color:#90CAF9;">Apollo Hospitals, Chennai · BloodLife Coordination Platform</div>
</div>
""", unsafe_allow_html=True)

    # Top KPI cards
    kpis = [
        ("8",  "Active Emergencies",  BLOOD_RED),
        ("23", "Pending Requests",    AMBER),
        ("41", "Fulfilled Today",     GREEN),
        ("3",  "Critical Shortages",  BLOOD_RED),
        ("12", "Donor Responses",     BLUE),
    ]
    cols = st.columns(5)
    for col, (val, lbl, clr) in zip(cols, kpis):
        with col:
            st.markdown(f'<div class="bl-stat" style="border-top:3px solid {clr};"><div class="num" style="color:{clr};">{val}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    left, right = st.columns([3, 2])

    with left:
        section_heading("🚨 Active Emergency Requests")
        critical_reqs = [r for r in REQUESTS if r["urgency"] == "Critical"]
        for req in critical_reqs:
            sc = {"Searching": BLOOD_RED, "Escalated": BLOOD_RED, "Donor Contacted": AMBER}.get(req["status"], GREY)
            st.markdown(f"""
<div style="background:#FFF;border-radius:10px;padding:14px 18px;margin-bottom:10px;
     border-left:5px solid {BLOOD_RED};box-shadow:0 1px 5px rgba(0,0,0,.08);">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <div style="display:flex;gap:14px;align-items:center;">
      <div style="background:#B71C1C22;border:2px solid {BLOOD_RED};border-radius:8px;
           padding:8px 12px;font-weight:800;color:{BLOOD_RED};font-size:1.1rem;">{req['blood_group']}</div>
      <div>
        <div style="font-weight:700;color:{NAVY};">{req['id']} · {req['component']} · {req['units']} units</div>
        <div style="font-size:.8rem;color:{GREY};">🏥 {req['hospital']} · 🕐 {req['created']}</div>
      </div>
    </div>
    <div style="text-align:right;">
      <div style="font-weight:600;color:{sc};font-size:.9rem;">● {req['status']}</div>
      <span class="badge {'badge-green' if 'Hospital' in req['verification'] else 'badge-amber'}">{req['verification']}</span>
    </div>
  </div>
  <div style="margin-top:8px;font-size:.78rem;color:{GREY};">📝 {req.get('notes','—')}</div>
</div>
""", unsafe_allow_html=True)

    with right:
        section_heading("🩸 Quick Inventory Snapshot")
        for inv in INVENTORY[:5]:
            rbc = inv["RBC"]
            thr = 20
            clr = GREEN if rbc >= thr else AMBER if rbc >= thr//2 else BLOOD_RED
            pct = min(100, int(rbc / 150 * 100))
            st.markdown(f"""
<div style="background:#FFF;border-radius:8px;padding:10px 14px;margin-bottom:8px;
     box-shadow:0 1px 3px rgba(0,0,0,.06);">
  <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
    <span style="font-weight:700;color:{NAVY};">{inv['blood_group']}</span>
    <span style="font-weight:600;color:{clr};">{rbc} RBC units</span>
  </div>
  <div style="background:#F0F4F8;border-radius:4px;height:6px;">
    <div style="background:{clr};height:6px;border-radius:4px;width:{pct}%;"></div>
  </div>
</div>""", unsafe_allow_html=True)

        section_heading("⚡ Operational Alerts")
        alerts = [
            (BLOOD_RED, "🚨", "O− RBC critically low",        "Only 18 units remaining"),
            (AMBER,     "⚠️", "3 pending requests unverified", "Awaiting hospital confirmation"),
            (BLUE,      "📡", "7 donor notifications sent",    "2 responses received"),
            (GREEN,     "✅", "BL-1045 fulfilled",             "A+ RBC — 3 units"),
        ]
        for clr, icon, title, detail in alerts:
            st.markdown(f"""
<div style="background:{clr}11;border-left:3px solid {clr};border-radius:6px;padding:8px 12px;margin-bottom:6px;">
  <div style="font-size:.85rem;font-weight:600;color:{NAVY};">{icon} {title}</div>
  <div style="font-size:.75rem;color:{GREY};">{detail}</div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# EMERGENCY REQUESTS
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "🚨 Emergency Requests":
    st.markdown(f'<div class="bl-header"><h1>🚨 Emergency Coordination</h1><p>Live emergency request tracking and escalation management.</p></div>', unsafe_allow_html=True)

    # Emergency escalation visualization
    section_heading("🔄 Emergency Escalation Engine — Request BL-1042")

    stages = [
        (GREEN,  "✅", "Request Created",    "Critical O− RBC · 4 units · Apollo Hospitals", "08:14"),
        (GREEN,  "✅", "Verified",           "Hospital verification confirmed by Dr. R. Anand", "08:15"),
        (GREEN,  "✅", "Inventory Search",   "BB001: 1u found · BB003: 2u found · Deficit: 1 unit", "08:16"),
        (GREEN,  "✅", "Donor Matching",     "8 donors scored · 3 top candidates selected", "08:17"),
        (AMBER,  "⏳", "Notifications Sent", "Stage 1: 3 donors notified within 5 km radius", "08:18"),
        (AMBER,  "⏳", "Response Tracking",  "2 of 3 donors responded · 1 accepted", "08:22"),
        (GREY,   "⚪", "Fulfilment",         "Pending 1 additional unit", "—"),
        (GREY,   "⚪", "Request Closed",     "—", "—"),
    ]
    for i, (clr, icon, stage, detail, ts) in enumerate(stages):
        st.markdown(f"""
<div style="display:flex;gap:16px;margin-bottom:6px;">
  <div style="display:flex;flex-direction:column;align-items:center;width:24px;flex-shrink:0;">
    <div style="width:20px;height:20px;border-radius:50%;background:{clr};display:flex;align-items:center;
         justify-content:center;font-size:.7rem;color:#FFF;flex-shrink:0;">{icon}</div>
    {'<div style="width:2px;flex:1;background:#E0E7EF;margin-top:2px;min-height:16px;"></div>' if i < len(stages)-1 else ''}
  </div>
  <div style="background:#FFF;border-radius:8px;padding:10px 14px;flex:1;margin-bottom:2px;
       box-shadow:0 1px 3px rgba(0,0,0,.05);border-left:3px solid {clr};">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <div style="font-weight:600;color:{NAVY};font-size:.9rem;">{stage}</div>
      <span style="font-size:.75rem;color:{GREY};">{ts}</span>
    </div>
    <div style="font-size:.78rem;color:{GREY};margin-top:2px;">{detail}</div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    section_heading("All Emergency Requests")
    em_reqs = [r for r in REQUESTS if r["urgency"] == "Critical"]

    with st.container():
        # Table header
        h1,h2,h3,h4,h5,h6 = st.columns([1.2,1.2,0.8,1.5,1.5,1])
        for col, hdr in zip([h1,h2,h3,h4,h5,h6], ["Request ID","Component","Units","Priority","Status","Action"]):
            col.markdown(f'<div style="font-size:.75rem;font-weight:700;color:{GREY};text-transform:uppercase;">{hdr}</div>', unsafe_allow_html=True)
        st.markdown('<hr style="margin:4px 0 10px 0;"/>', unsafe_allow_html=True)
        for req in em_reqs:
            sc = {"Searching": BLOOD_RED, "Escalated": BLOOD_RED, "Donor Contacted": AMBER}.get(req["status"], GREY)
            c1,c2,c3,c4,c5,c6 = st.columns([1.2,1.2,0.8,1.5,1.5,1])
            c1.markdown(f'<span style="font-weight:700;color:{NAVY};">{req["id"]}</span><br/><span style="font-size:.75rem;color:{GREY};">{req["blood_group"]}</span>', unsafe_allow_html=True)
            c2.markdown(f'<span style="font-size:.85rem;color:{NAVY};">{req["component"]}</span>', unsafe_allow_html=True)
            c3.markdown(f'<span style="font-weight:600;color:{NAVY};">{req["units"]}</span>', unsafe_allow_html=True)
            c4.markdown(f'<span class="badge badge-red">🔴 Critical</span>', unsafe_allow_html=True)
            c5.markdown(f'<span style="font-weight:600;color:{sc};">● {req["status"]}</span>', unsafe_allow_html=True)
            c6.button("View →", key=f"em_{req['id']}")

# ═══════════════════════════════════════════════════════════════════════════════
# ALL REQUESTS
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "📋 All Requests":
    st.markdown(f'<div class="bl-header"><h1>📋 All Blood Requests</h1><p>Complete request registry for Apollo Hospitals.</p></div>', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        f_status = st.selectbox("Status", ["All", "Searching", "Escalated", "Donor Contacted", "Partially Fulfilled", "Fulfilled", "Pending"])
    with col_f2:
        f_urgency = st.selectbox("Urgency", ["All", "Critical", "Urgent", "Routine"])
    with col_f3:
        f_bg = st.selectbox("Blood Group", ["All"] + BLOOD_GROUPS)

    filtered = REQUESTS
    if f_status != "All":  filtered = [r for r in filtered if r["status"] == f_status]
    if f_urgency != "All": filtered = [r for r in filtered if r["urgency"] == f_urgency]
    if f_bg != "All":      filtered = [r for r in filtered if r["blood_group"] == f_bg]

    st.markdown(f'<div style="font-size:.82rem;color:{GREY};margin-bottom:12px;">{len(filtered)} request(s) found</div>', unsafe_allow_html=True)

    for req in filtered:
        sc = {"Fulfilled": GREEN, "Searching": BLOOD_RED, "Pending": AMBER,
              "Escalated": BLOOD_RED, "Donor Contacted": BLUE, "Partially Fulfilled": AMBER}.get(req["status"], GREY)
        vc = "badge-green" if "Hospital" in req["verification"] else "badge-blue" if "Blood Bank" in req["verification"] else "badge-amber"
        with st.expander(f"{req['id']}  ·  {req['blood_group']} {req['component']}  ·  {req['urgency']}  ·  {req['status']}"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Units Required", req["units"])
            c2.metric("Hospital",       req["hospital"])
            c3.metric("Created",        req["created"])
            st.markdown(f"""
<div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;">
  <span class="badge {'badge-red' if req['urgency']=='Critical' else 'badge-amber' if req['urgency']=='Urgent' else 'badge-grey'}">{req['urgency']}</span>
  <span class="badge {vc}">{req['verification']}</span>
  <span style="font-size:.8rem;color:{GREY};">Notes: {req.get('notes','—')}</span>
</div>""", unsafe_allow_html=True)
            action_col1, action_col2, action_col3 = st.columns(3)
            action_col1.button("✅ Verify Request", key=f"ver_{req['id']}")
            action_col2.button("🔄 Update Status",  key=f"upd_{req['id']}")
            action_col3.button("✖️ Close Request",   key=f"cls_{req['id']}")

# ═══════════════════════════════════════════════════════════════════════════════
# BLOOD AVAILABILITY
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "🩸 Blood Availability":
    st.markdown(f'<div class="bl-header"><h1>🩸 Blood Availability</h1><p>Inventory overview from linked blood banks.</p></div>', unsafe_allow_html=True)

    df = pd.DataFrame(INVENTORY)
    thresholds = {"RBC": 20, "Platelets": 5, "FFP": 8, "Cryoprecipitate": 3, "Whole Blood": 3}

    # Inventory matrix
    section_heading("Inventory Matrix — All Components")
    header_cols = st.columns([1.5, 1, 1, 1, 1, 1])
    for col, hdr in zip(header_cols, ["Blood Group", "RBC", "Platelets", "FFP", "Cryo", "Whole Blood"]):
        col.markdown(f'<div style="font-size:.75rem;font-weight:700;color:{GREY};text-transform:uppercase;padding:4px 0;">{hdr}</div>', unsafe_allow_html=True)
    st.markdown('<hr style="margin:4px 0 8px 0;"/>', unsafe_allow_html=True)

    for _, row in df.iterrows():
        cols = st.columns([1.5, 1, 1, 1, 1, 1])
        cols[0].markdown(f'<span style="font-weight:700;color:{NAVY};">{row["blood_group"]}</span>', unsafe_allow_html=True)
        for i, comp in enumerate(["RBC", "Platelets", "FFP", "Cryoprecipitate", "Whole Blood"]):
            val = row[comp]
            thr = thresholds[comp]
            clr = GREEN if val >= thr else AMBER if val >= thr // 2 else BLOOD_RED
            label = "OK" if val >= thr else "LOW" if val >= thr // 2 else "CRIT"
            cols[i+1].markdown(f'<span style="font-weight:600;color:{clr};">{val}</span> <span style="font-size:.7rem;color:{clr};">[{label}]</span>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    # Charts
    c1, c2 = st.columns(2)
    with c1:
        section_heading("RBC Units by Blood Group")
        fig = go.Figure(go.Bar(
            x=[r["blood_group"] for r in INVENTORY],
            y=[r["RBC"] for r in INVENTORY],
            marker_color=[GREEN if r["RBC"] >= 20 else AMBER if r["RBC"] >= 10 else BLOOD_RED for r in INVENTORY],
        ))
        fig.update_layout(height=260, margin=dict(t=10,b=10,l=10,r=10),
                          plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                          yaxis_title="Units", xaxis_title="Blood Group")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        section_heading("Component Distribution")
        total_by_comp = {c: sum(r[c] for r in INVENTORY) for c in ["RBC","Platelets","FFP","Cryoprecipitate","Whole Blood"]}
        fig2 = go.Figure(go.Pie(
            labels=list(total_by_comp.keys()),
            values=list(total_by_comp.values()),
            hole=0.45,
            marker_colors=[BLUE, GREEN, AMBER, BLOOD_RED, GREY],
        ))
        fig2.update_layout(height=260, margin=dict(t=10,b=10,l=10,r=10),
                           paper_bgcolor="#FFFFFF", showlegend=True)
        st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DONOR RESPONSES
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "👥 Donor Responses":
    st.markdown(f'<div class="bl-header"><h1>👥 Donor Response Network</h1><p>Track donor notifications and responses.</p></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, (val, lbl, clr) in zip([c1,c2,c3,c4], [
        ("12","Notifications Sent", BLUE), ("5","Responded", AMBER),
        ("3", "Accepted",           GREEN),("2","Donations Confirmed", BLOOD_RED)
    ]):
        with col:
            st.markdown(f'<div class="bl-stat" style="border-top:3px solid {clr};"><div class="num" style="color:{clr};">{val}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    section_heading("Notified Donors — BL-1042 (O− Critical)")

    for donor in DONORS[:6]:
        resp = ["Accepted", "Accepted", "Declined", "Pending", "Pending", "Pending"][DONORS.index(donor)]
        rc   = GREEN if resp == "Accepted" else BLOOD_RED if resp == "Declined" else GREY
        av_clr = {"Available Now": GREEN, "Available Today": AMBER, "Available Later": BLUE,
                  "Unavailable": GREY, "Temporarily Unavailable": BLOOD_RED}.get(donor["availability"], GREY)
        st.markdown(f"""
<div style="background:#FFF;border-radius:10px;padding:12px 18px;margin-bottom:8px;
     box-shadow:0 1px 4px rgba(0,0,0,.07);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
  <div style="display:flex;gap:14px;align-items:center;">
    <div style="background:{LIGHT_BLUE};border-radius:50%;width:40px;height:40px;
         display:flex;align-items:center;justify-content:center;font-weight:700;color:{NAVY};">{donor['blood_group']}</div>
    <div>
      <div style="font-weight:600;color:{NAVY};">Anonymous Donor · {donor['blood_group']}</div>
      <div style="font-size:.78rem;color:{GREY};">~{donor['distance_km']} km · {'✅ Verified' if donor['verified'] else '⏳ Pending'}</div>
    </div>
  </div>
  <div style="display:flex;gap:10px;align-items:center;">
    <span style="font-size:.8rem;color:{av_clr};font-weight:500;">{donor['availability']}</span>
    <span style="font-weight:700;color:{rc};">● {resp}</span>
    <div style="font-size:.8rem;color:{GREY};">Score: <strong>{donor['score']}</strong></div>
  </div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# NEARBY BLOOD BANKS
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "🏦 Nearby Blood Banks":
    st.markdown(f'<div class="bl-header"><h1>🏦 Nearby Blood Banks</h1><p>Verified blood bank network in your region.</p></div>', unsafe_allow_html=True)

    for bb in BLOOD_BANKS:
        vc = GREEN if bb["verified"] else AMBER
        st.markdown(f"""
<div class="bl-card" style="border-left:4px solid {vc};">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <div>
      <div style="font-weight:700;color:{NAVY};font-size:1rem;">{bb['name']}</div>
      <div style="font-size:.82rem;color:{GREY};">📍 {bb['city']} · ~{bb['distance_km']} km away</div>
    </div>
    <div style="display:flex;gap:8px;align-items:center;">
      <span class="badge {'badge-green' if bb['verified'] else 'badge-amber'}">{'✅ Verified' if bb['verified'] else '⏳ Pending'}</span>
      <button style="background:{BLUE};color:#FFF;border:none;border-radius:6px;padding:6px 14px;font-size:.8rem;font-weight:600;cursor:pointer;">Contact</button>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "📈 Analytics":
    st.markdown(f'<div class="bl-header"><h1>📈 Hospital Analytics</h1><p>Operational insights and trends.</p></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        section_heading("Requests vs Fulfilment (12 months)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=MONTHS, y=REQUEST_TREND, name="Requests",
                                  line=dict(color=BLOOD_RED, width=2), mode="lines+markers"))
        fig.add_trace(go.Scatter(x=MONTHS, y=FULFILMENT_TREND, name="Fulfilled",
                                  line=dict(color=GREEN, width=2), mode="lines+markers"))
        fig.update_layout(height=280, margin=dict(t=10,b=10,l=10,r=10),
                          plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                          legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        section_heading("Blood Group Demand Distribution")
        bg_demand = {"O+": 42, "O−": 18, "A+": 31, "A−": 8, "B+": 24, "B−": 5, "AB+": 12, "AB−": 3}
        fig2 = px.bar(x=list(bg_demand.keys()), y=list(bg_demand.values()),
                      color=list(bg_demand.values()), color_continuous_scale=["#E8F2FA","#C62828"])
        fig2.update_layout(height=280, margin=dict(t=10,b=10,l=10,r=10),
                           plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                           coloraxis_showscale=False, showlegend=False,
                           yaxis_title="Units", xaxis_title="Blood Group")
        st.plotly_chart(fig2, use_container_width=True)

    section_heading("Average Response Time Trend")
    resp_times = [24, 22, 20, 19, 21, 18, 17, 16, 18, 19, 17, 16]
    fig3 = go.Figure(go.Scatter(x=MONTHS, y=resp_times, fill="tozeroy",
                                 line=dict(color=BLUE, width=2),
                                 fillcolor=f"{LIGHT_BLUE}"))
    fig3.update_layout(height=220, margin=dict(t=10,b=10,l=10,r=10),
                       plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                       yaxis_title="Minutes")
    st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# AI COPILOT
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "🤖 AI Copilot":
    st.markdown(f'<div class="bl-header"><h1>🤖 BloodLife Clinical Operations Assistant</h1><p>Operational AI copilot — summarises data, guides navigation. Does not make clinical decisions.</p></div>', unsafe_allow_html=True)

    # Operational summary card
    st.markdown(f"""
<div style="background:{LIGHT_BLUE};border:2px solid {BLUE};border-radius:12px;padding:20px 24px;margin-bottom:20px;">
  <div style="font-size:.9rem;font-weight:700;color:{NAVY};margin-bottom:8px;">🧠 Current Operational Summary</div>
  <div style="font-size:.9rem;color:#0D47A1;line-height:1.7;">
    There are <strong>8 active emergency requests</strong>, including 5 critical O− RBC requirements.
    <strong>2 nearby blood centres</strong> have reported relevant inventory (Indian Red Cross: 1 unit; Rotary TTK: 2 units).
    <strong>7 donor notifications</strong> have been sent — 3 responses received so far (2 accepted).
    There are <strong>3 requests pending hospital verification</strong>.
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div style="background:#FFF3E0;border:1px solid {AMBER};border-radius:8px;padding:12px 16px;margin-bottom:16px;font-size:.82rem;color:#7B5E00;">
  ⚕️ <strong>Important:</strong> BloodLife AI provides operational information only. It does not diagnose, prescribe or make transfusion decisions.
  All clinical decisions remain with qualified healthcare professionals.
</div>""", unsafe_allow_html=True)

    # Chat interface
    if "hosp_chat" not in st.session_state:
        st.session_state.hosp_chat = [
            {"role": "assistant", "content": "Hello. I'm the BloodLife Clinical Operations Assistant. I can summarize operational data, help you navigate the platform, and answer questions about current requests and inventory. How can I help?"}
        ]

    for msg in st.session_state.hosp_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    HOSPITAL_RESPONSES = {
        "o-":      "There are currently 18 units of O− RBC in the coordinated inventory across linked blood banks. 5 active critical requests are being fulfilled. The system has identified 3 eligible donors within 10 km.",
        "critical":"There are 8 active emergency requests. 5 are classified Critical, including 3 O− RBC and 1 AB− FFP. All have hospital verification. Stage 2 escalation is active for 2 of these.",
        "donor":   "7 donor notifications have been sent for current critical requests. 3 donors have responded — 2 accepted, 1 declined. 4 are awaiting response. The system will expand search radius if responses are insufficient.",
        "inventory":"The inventory across linked blood banks shows O− RBC at 18 units (below threshold), Platelets at 28 units (O+), and AB− at 6 units. 26 units across all groups are approaching expiry.",
        "fulfil":  "Today, 41 blood requests have been fulfilled. The current fulfilment rate this week is 89.4%. Average response time is 18.4 minutes.",
        "blood bank":"There are 7 blood banks in the coordinated network. 6 are verified. The nearest is Apollo Blood Bank at 2.1 km. All verified blood banks report last inventory update within the past 2 hours.",
    }

    user_input = st.chat_input("Ask about requests, inventory, donors, escalation...")
    if user_input:
        st.session_state.hosp_chat.append({"role": "user", "content": user_input})
        lower = user_input.lower()
        reply = "I can provide operational summaries for requests, inventory, donor responses and escalation. For specific clinical questions, please consult your medical team."
        for key, resp in HOSPITAL_RESPONSES.items():
            if key in lower:
                reply = resp
                break
        st.session_state.hosp_chat.append({"role": "assistant", "content": reply})
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT LOG
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "📝 Audit Log":
    st.markdown(f'<div class="bl-header"><h1>📝 Audit Log</h1><p>Complete audit trail for all platform actions.</p></div>', unsafe_allow_html=True)

    EVENT_COLOURS = {
        "REQUEST_CREATED":   (BLUE,      "🆕"),
        "REQUEST_VERIFIED":  (GREEN,     "✅"),
        "REQUEST_FULFILLED": (GREEN,     "🎉"),
        "ESCALATION_STAGE2": (BLOOD_RED, "🚨"),
        "DONOR_MATCHED":     (BLUE,      "🎯"),
        "DONOR_ACCEPTED":    (GREEN,     "✔️"),
        "INVENTORY_SEARCHED":(GREY,      "🔍"),
        "INVENTORY_RESERVED":(AMBER,     "📦"),
        "VERIFICATION_SENT": (AMBER,     "📨"),
        "USER_VERIFIED":     (GREEN,     "🛡️"),
    }

    for log in AUDIT_LOG:
        clr, icon = EVENT_COLOURS.get(log["event"], (GREY, "📋"))
        st.markdown(f"""
<div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:8px;">
  <div style="min-width:130px;font-size:.75rem;color:{GREY};padding-top:2px;">{log['timestamp']}</div>
  <div style="width:28px;height:28px;border-radius:50%;background:{clr}22;border:1px solid {clr};
       display:flex;align-items:center;justify-content:center;font-size:.8rem;flex-shrink:0;">{icon}</div>
  <div style="background:#FFF;border-radius:8px;padding:8px 14px;flex:1;
       box-shadow:0 1px 3px rgba(0,0,0,.05);border-left:3px solid {clr};">
    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;">
      <span style="font-weight:600;color:{NAVY};font-size:.85rem;">{log['event'].replace('_',' ')}</span>
      <span class="badge badge-navy" style="font-size:.68rem;">{log['entity']}</span>
      <span style="font-size:.75rem;color:{GREY};">by {log['actor']}</span>
    </div>
    <div style="font-size:.78rem;color:{GREY};margin-top:2px;">{log['detail']}</div>
  </div>
</div>""", unsafe_allow_html=True)
