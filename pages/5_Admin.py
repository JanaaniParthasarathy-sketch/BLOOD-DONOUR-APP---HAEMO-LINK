"""
BloodLife — Administrator Network Control Centre
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.theme import (
    inject_global_css, demo_banner, NAVY, BLUE, BLOOD_RED, GREEN, AMBER, GREY,
    LIGHT_BLUE, BLOOD_GROUPS, section_heading,
)
from data.demo_data import (
    DONORS, HOSPITALS, BLOOD_BANKS, REQUESTS, INVENTORY, AUDIT_LOG,
    PLATFORM_STATS, DEMAND_FORECAST, EXPIRY_RISK,
    MONTHS, DONOR_GROWTH, REQUEST_TREND, FULFILMENT_TREND,
)

st.set_page_config(page_title="Admin Network Centre — BloodLife", page_icon="🛡️", layout="wide")
inject_global_css()

with st.sidebar:
    st.markdown("""
<div style="text-align:center;padding:12px 0;">
  <span style="font-size:1.8rem;">🛡️</span>
  <div style="font-size:1.2rem;font-weight:800;color:#FFF;">BloodLife</div>
  <div style="font-size:.7rem;color:#90CAF9;">Network Control Centre</div>
</div><hr/>""", unsafe_allow_html=True)

    nav = st.radio("Module", [
        "🏠 Network Overview",
        "📊 Platform Analytics",
        "👥 Donor Registry",
        "🏥 Hospitals",
        "🩸 Blood Banks",
        "🚨 Active Emergencies",
        "✅ Verification",
        "📈 Regional Demand",
        "🛡️ System Health",
        "📝 Audit Logs",
    ], label_visibility="collapsed")

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:.75rem;color:#90CAF9;">Admin: Janaani Parthasarathy</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.7rem;color:#607D8B;">Platform Administrator</div>', unsafe_allow_html=True)
    st.markdown("<hr/><a href='/' style='color:#90CAF9;font-size:.8rem;'>← Home</a>", unsafe_allow_html=True)

demo_banner()

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if nav == "🏠 Network Overview":
    st.markdown(f"""
<div style="background:{NAVY};border-radius:14px;padding:24px 32px;margin-bottom:24px;color:#FFF;">
  <div style="font-size:1.6rem;font-weight:800;">🛡️ BloodLife Network Control Centre</div>
  <div style="font-size:.9rem;color:#90CAF9;">Platform-wide operational view · All data simulated</div>
</div>""", unsafe_allow_html=True)

    # Top stats
    kpis = [
        (f"{PLATFORM_STATS['active_donors']:,}",         "Active Donors",          BLUE),
        (str(PLATFORM_STATS["verified_blood_banks"]),    "Verified Blood Banks",   GREEN),
        (f"{PLATFORM_STATS['partner_hospitals']:,}",     "Partner Hospitals",      NAVY),
        (f"{PLATFORM_STATS['requests_fulfilled']:,}",    "Requests Fulfilled",     BLOOD_RED),
        (str(PLATFORM_STATS["active_emergencies"]),      "Active Emergencies",     BLOOD_RED),
        (f"{PLATFORM_STATS['avg_response_min']}m",       "Avg. Response Time",     AMBER),
    ]
    cols = st.columns(6)
    for col, (val, lbl, clr) in zip(cols, kpis):
        with col:
            st.markdown(f'<div class="bl-stat" style="border-top:3px solid {clr};"><div class="num" style="color:{clr};">{val}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Network diagram visual
    st.markdown(f"""
<div class="bl-card" style="padding:28px 32px;">
  <div style="font-size:1.05rem;font-weight:700;color:{NAVY};margin-bottom:16px;">🌐 Network Topology — BloodLife Ecosystem</div>
  <div style="display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:16px;text-align:center;">
    <div style="background:{LIGHT_BLUE};border:2px solid {BLUE};border-radius:10px;padding:16px 20px;min-width:120px;">
      <div style="font-size:1.5rem;">👤</div>
      <div style="font-weight:700;color:{NAVY};">Donors</div>
      <div style="font-size:1.2rem;font-weight:800;color:{BLOOD_RED};">{PLATFORM_STATS['active_donors']:,}</div>
    </div>
    <div style="color:{BLUE};font-size:1.8rem;">⇒</div>
    <div style="background:{NAVY};border-radius:12px;padding:20px 24px;min-width:160px;border:2px solid {BLUE};">
      <div style="font-size:1.3rem;">🧠</div>
      <div style="font-weight:800;color:#FFF;font-size:1.05rem;">BloodLife</div>
      <div style="font-size:.8rem;color:#90CAF9;">Intelligence Engine</div>
    </div>
    <div style="color:{BLUE};font-size:1.8rem;">⇒</div>
    <div style="background:{LIGHT_BLUE};border:2px solid {BLUE};border-radius:10px;padding:16px 20px;min-width:120px;">
      <div style="font-size:1.5rem;">🏥</div>
      <div style="font-weight:700;color:{NAVY};">Hospitals</div>
      <div style="font-size:1.2rem;font-weight:800;color:{BLUE};">{PLATFORM_STATS['partner_hospitals']:,}</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:16px;text-align:center;margin-top:12px;">
    <div style="background:{LIGHT_BLUE};border:2px solid {BLOOD_RED};border-radius:10px;padding:16px 20px;min-width:120px;">
      <div style="font-size:1.5rem;">🩸</div>
      <div style="font-weight:700;color:{NAVY};">Blood Banks</div>
      <div style="font-size:1.2rem;font-weight:800;color:{GREEN};">{PLATFORM_STATS['verified_blood_banks']}</div>
    </div>
    <div style="color:{BLUE};font-size:1.8rem;">⇒</div>
    <div style="background:{LIGHT_BLUE};border:2px solid {BLOOD_RED};border-radius:10px;padding:16px 20px;min-width:120px;">
      <div style="font-size:1.5rem;">🧑‍🦽</div>
      <div style="font-weight:700;color:{NAVY};">Patients</div>
      <div style="font-size:1.2rem;font-weight:800;color:{AMBER};">{PLATFORM_STATS['pending_requests']}</div>
      <div style="font-size:.72rem;color:{GREY};">Active requests</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Quick snapshot
    left, right = st.columns(2)
    with left:
        section_heading("🚨 Active Emergencies")
        critical_reqs = [r for r in REQUESTS if r["urgency"] == "Critical"]
        for req in critical_reqs[:4]:
            sc = BLOOD_RED if req["status"] in ("Searching","Escalated") else AMBER
            st.markdown(f"""
<div style="background:#FFF;border-radius:8px;padding:10px 14px;margin-bottom:6px;
     border-left:4px solid {BLOOD_RED};box-shadow:0 1px 3px rgba(0,0,0,.06);">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <div>
      <span style="font-weight:700;color:{NAVY};">{req['id']}</span>
      <span style="font-size:.82rem;color:{GREY};margin-left:6px;">{req['blood_group']} {req['component']} · {req['units']}u</span>
    </div>
    <span style="font-size:.8rem;font-weight:600;color:{sc};">● {req['status']}</span>
  </div>
  <div style="font-size:.75rem;color:{GREY};margin-top:2px;">🏥 {req['hospital']}</div>
</div>""", unsafe_allow_html=True)

    with right:
        section_heading("📊 Pending Actions")
        actions = [
            (BLOOD_RED, "5",  "Requests require verification"),
            (AMBER,     "3",  "New hospitals pending approval"),
            (AMBER,     "2",  "Blood banks pending verification"),
            (BLUE,      "12", "Donor registrations pending review"),
            (GREEN,     "7",  "Requests fulfilled today"),
        ]
        for clr, count, label in actions:
            st.markdown(f"""
<div style="background:#FFF;border-radius:8px;padding:10px 14px;margin-bottom:6px;
     display:flex;align-items:center;gap:12px;box-shadow:0 1px 3px rgba(0,0,0,.06);">
  <div style="font-size:1.3rem;font-weight:800;color:{clr};min-width:36px;text-align:center;">{count}</div>
  <div style="font-size:.85rem;color:{NAVY};">{label}</div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PLATFORM ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "📊 Platform Analytics":
    st.markdown(f'<div class="bl-header"><h1>📊 Platform Analytics</h1><p>Network-wide performance metrics and trends.</p></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        section_heading("Donor Growth (12 months)")
        fig = go.Figure(go.Bar(x=MONTHS, y=DONOR_GROWTH, marker_color=BLUE))
        fig.update_layout(height=260, margin=dict(t=10,b=10,l=10,r=10),
                          plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF", yaxis_title="New Donors")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        section_heading("Requests vs Fulfilment")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=MONTHS, y=REQUEST_TREND,    name="Requests",  line=dict(color=BLOOD_RED, width=2), mode="lines+markers"))
        fig2.add_trace(go.Scatter(x=MONTHS, y=FULFILMENT_TREND, name="Fulfilled", line=dict(color=GREEN,     width=2), mode="lines+markers"))
        fig2.update_layout(height=260, margin=dict(t=10,b=10,l=10,r=10),
                           plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                           legend=dict(orientation="h", y=-0.25))
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        section_heading("Blood Group Demand (Current Month)")
        bg_demand = {"O+": 42, "O−": 18, "A+": 31, "A−": 8, "B+": 24, "B−": 5, "AB+": 12, "AB−": 3}
        fig3 = px.bar(x=list(bg_demand.keys()), y=list(bg_demand.values()),
                      color=list(bg_demand.values()), color_continuous_scale=["#E8F2FA","#C62828"],
                      labels={"x": "Blood Group", "y": "Units"})
        fig3.update_layout(height=260, margin=dict(t=10,b=10,l=10,r=10),
                           plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                           coloraxis_showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        section_heading("Fulfilment Rate Trend")
        fulfilment_rate = [92, 91, 93, 90, 89, 91, 92, 93, 90, 91, 92, 89]
        fig4 = go.Figure(go.Scatter(x=MONTHS, y=fulfilment_rate, fill="tozeroy",
                                     line=dict(color=GREEN, width=2),
                                     fillcolor="rgba(46,125,50,0.1)"))
        fig4.add_hline(y=90, line_dash="dash", line_color=AMBER, annotation_text="Target 90%")
        fig4.update_layout(height=260, margin=dict(t=10,b=10,l=10,r=10),
                           plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                           yaxis=dict(range=[80, 100]), yaxis_title="%")
        st.plotly_chart(fig4, use_container_width=True)

    section_heading("Response Time Trend (minutes)")
    resp_times = [24, 22, 20, 19, 21, 18, 17, 16, 18, 19, 17, 16]
    fig5 = go.Figure(go.Scatter(x=MONTHS, y=resp_times,
                                 line=dict(color=BLUE, width=2), mode="lines+markers",
                                 fill="tozeroy", fillcolor="rgba(23,105,170,0.08)"))
    fig5.update_layout(height=220, margin=dict(t=10,b=10,l=10,r=10),
                       plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF", yaxis_title="Minutes")
    st.plotly_chart(fig5, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DONOR REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "👥 Donor Registry":
    st.markdown(f'<div class="bl-header"><h1>👥 Donor Registry</h1><p>Platform-wide donor management.</p></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, (val, lbl, clr) in zip([c1,c2,c3,c4],[
        (str(len(DONORS)),                                        "Total (demo)",        BLUE),
        (str(len([d for d in DONORS if d["verified"]])),          "Verified",            GREEN),
        (str(len([d for d in DONORS if d["availability"]=="Available Now"])),"Available Now",AMBER),
        (str(len([d for d in DONORS if not d["verified"]])),      "Pending Verification",BLOOD_RED),
    ]):
        with col:
            st.markdown(f'<div class="bl-stat" style="border-top:3px solid {clr};"><div class="num" style="color:{clr};">{val}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    search = st.text_input("Search donor by ID or blood group", placeholder="E.g. D1002, O−")
    displayed_donors = [d for d in DONORS if not search or search.upper() in d["id"] or search.upper() in d["blood_group"]]

    for d in displayed_donors:
        av_clr = {"Available Now": GREEN, "Available Today": AMBER, "Available Later": BLUE,
                  "Unavailable": GREY, "Temporarily Unavailable": BLOOD_RED}.get(d["availability"], GREY)
        with st.expander(f"{d['id']}  ·  {d['blood_group']}  ·  {d['city']}  ·  {d['availability']}"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Blood Group",     d["blood_group"])
            c2.metric("Donations",       d["donations"])
            c3.metric("Response Rate",   f"{int(d['response_rate']*100)}%")
            st.markdown(f"""
<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:8px;">
  <span class="badge {'badge-green' if d['verified'] else 'badge-amber'}">{'✅ Verified' if d['verified'] else '⏳ Pending'}</span>
  <span style="color:{av_clr};font-weight:600;font-size:.85rem;">{d['availability']}</span>
  <span class="badge badge-grey">Last: {d['last_donation']}</span>
</div>""", unsafe_allow_html=True)
            a1, a2 = st.columns(2)
            a1.button("✅ Verify Donor",   key=f"adm_ver_{d['id']}")
            a2.button("⚠️ Flag for Review", key=f"adm_flg_{d['id']}")

# ═══════════════════════════════════════════════════════════════════════════════
# HOSPITALS
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "🏥 Hospitals":
    st.markdown(f'<div class="bl-header"><h1>🏥 Hospital Registry</h1><p>Manage partner hospitals.</p></div>', unsafe_allow_html=True)

    for h in HOSPITALS:
        vc = GREEN if h["verified"] else AMBER
        active = len([r for r in REQUESTS if r["hospital"] == h["name"]])
        st.markdown(f"""
<div class="bl-card" style="border-left:5px solid {vc};">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <div>
      <div style="font-weight:700;color:{NAVY};font-size:1rem;">{h['id']} · {h['name']}</div>
      <div style="font-size:.82rem;color:{GREY};">📍 {h['city']} · ~{h['distance_km']} km · {h['beds']} beds</div>
    </div>
    <div style="display:flex;gap:8px;align-items:center;">
      <span class="badge {'badge-green' if h['verified'] else 'badge-amber'}">{'✅ Verified' if h['verified'] else '⏳ Pending'}</span>
      <span class="badge badge-blue">{active} requests</span>
      <button style="background:{BLUE};color:#FFF;border:none;border-radius:6px;padding:5px 12px;font-size:.78rem;cursor:pointer;">
        {'Revoke' if h['verified'] else 'Verify'}
      </button>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# BLOOD BANKS
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "🩸 Blood Banks":
    st.markdown(f'<div class="bl-header"><h1>🩸 Blood Bank Registry</h1><p>Manage verified blood banks on the network.</p></div>', unsafe_allow_html=True)

    for bb in BLOOD_BANKS:
        vc = GREEN if bb["verified"] else AMBER
        st.markdown(f"""
<div class="bl-card" style="border-left:5px solid {vc};">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <div>
      <div style="font-weight:700;color:{NAVY};font-size:1rem;">{bb['id']} · {bb['name']}</div>
      <div style="font-size:.82rem;color:{GREY};">📍 {bb['city']} · ~{bb['distance_km']} km</div>
    </div>
    <div style="display:flex;gap:8px;align-items:center;">
      <span class="badge {'badge-green' if bb['verified'] else 'badge-amber'}">{'✅ Verified' if bb['verified'] else '⏳ Pending'}</span>
      <button style="background:{BLUE if bb['verified'] else GREEN};color:#FFF;border:none;
              border-radius:6px;padding:5px 12px;font-size:.78rem;cursor:pointer;">
        {'Manage' if bb['verified'] else 'Verify'}
      </button>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ACTIVE EMERGENCIES
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "🚨 Active Emergencies":
    st.markdown(f'<div class="bl-header"><h1>🚨 Active Emergencies</h1><p>Platform-wide emergency request monitoring.</p></div>', unsafe_allow_html=True)

    st.markdown(f"""
<div style="background:#B71C1C;border-radius:8px;padding:12px 20px;margin-bottom:16px;
     color:#FFF;font-weight:600;font-size:.95rem;">
  🔴 {PLATFORM_STATS['active_emergencies']} ACTIVE EMERGENCIES ACROSS NETWORK — {PLATFORM_STATS['shortage_alerts']} CRITICAL SHORTAGE ALERTS
</div>
""", unsafe_allow_html=True)

    for req in REQUESTS:
        if req["urgency"] != "Critical": continue
        sc = {"Searching": BLOOD_RED, "Escalated": BLOOD_RED, "Donor Contacted": AMBER}.get(req["status"], GREY)
        st.markdown(f"""
<div class="bl-card" style="border-left:5px solid {BLOOD_RED};">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <div>
      <div style="font-weight:700;color:{NAVY};">{req['id']} · {req['blood_group']} {req['component']}</div>
      <div style="font-size:.82rem;color:{GREY};">🏥 {req['hospital']} · {req['units']} units · {req['created']}</div>
      <div style="font-size:.78rem;color:{GREY};margin-top:2px;">📝 {req.get('notes','—')}</div>
    </div>
    <div style="text-align:right;">
      <span style="font-weight:700;color:{sc};">● {req['status']}</span><br/>
      <span class="badge {'badge-green' if 'Hospital' in req['verification'] else 'badge-amber'}">{req['verification']}</span>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "✅ Verification":
    st.markdown(f'<div class="bl-header"><h1>✅ Verification Management</h1><p>Review and approve pending platform verifications.</p></div>', unsafe_allow_html=True)

    tabs = st.tabs(["🏥 Hospitals Pending", "🩸 Blood Banks Pending", "👤 Donors Pending", "📋 Requests Pending"])

    with tabs[0]:
        pending_hosp = [h for h in HOSPITALS if not h["verified"]]
        if not pending_hosp:
            st.success("No hospitals pending verification.")
        for h in pending_hosp:
            st.markdown(f"""
<div class="bl-card" style="border-left:4px solid {AMBER};">
  <div style="font-weight:700;color:{NAVY};">{h['name']}</div>
  <div style="font-size:.82rem;color:{GREY};">📍 {h['city']} · {h['beds']} beds</div>
</div>""", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.button("✅ Approve",  key=f"appr_h_{h['id']}", type="primary")
            c2.button("❌ Decline",  key=f"decl_h_{h['id']}")

    with tabs[1]:
        pending_bb = [bb for bb in BLOOD_BANKS if not bb["verified"]]
        for bb in pending_bb:
            st.markdown(f'<div class="bl-card"><b>{bb["name"]}</b> · {bb["city"]} · ~{bb["distance_km"]} km</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.button("✅ Approve", key=f"appr_bb_{bb['id']}", type="primary")
            c2.button("❌ Decline", key=f"decl_bb_{bb['id']}")

    with tabs[2]:
        pending_donors = [d for d in DONORS if not d["verified"]]
        st.markdown(f'<div style="font-size:.85rem;color:{GREY};margin-bottom:10px;">{len(pending_donors)} donor(s) pending verification.</div>', unsafe_allow_html=True)
        for d in pending_donors:
            st.markdown(f"""
<div class="bl-card" style="border-left:4px solid {AMBER};">
  <div style="font-weight:600;color:{NAVY};">{d['id']} · {d['blood_group']} · {d['city']}</div>
</div>""", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.button("✅ Verify", key=f"ver_d_{d['id']}", type="primary")
            c2.button("⚠️ Review", key=f"rev_d_{d['id']}")

    with tabs[3]:
        pending_reqs = [r for r in REQUESTS if "Pending" in r["verification"]]
        st.markdown(f'<div style="font-size:.85rem;color:{GREY};margin-bottom:10px;">{len(pending_reqs)} request(s) pending verification.</div>', unsafe_allow_html=True)
        for req in pending_reqs:
            st.markdown(f"""
<div class="bl-card" style="border-left:4px solid {AMBER};">
  <div style="font-weight:600;color:{NAVY};">{req['id']} · {req['blood_group']} {req['component']} · {req['hospital']}</div>
  <div style="font-size:.8rem;color:{GREY};">Created: {req['created']}</div>
</div>""", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.button("✅ Verify Request", key=f"ver_r_{req['id']}", type="primary")
            c2.button("🚫 Reject",         key=f"rej_r_{req['id']}")

# ═══════════════════════════════════════════════════════════════════════════════
# REGIONAL DEMAND
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "📈 Regional Demand":
    st.markdown(f'<div class="bl-header"><h1>📈 Regional Demand Analysis</h1><p>Blood demand patterns across regions — simulated data.</p></div>', unsafe_allow_html=True)

    section_heading("Demand by Blood Group — Top 5 Cities")
    cities = ["Chennai", "Mumbai", "Delhi", "Bangalore", "Hyderabad"]
    groups = ["O+", "O−", "A+", "B+", "AB+"]
    import random; rng = random.Random(42)
    fig = go.Figure()
    colours = [BLOOD_RED, NAVY, BLUE, GREEN, AMBER]
    for grp, clr in zip(groups, colours):
        fig.add_trace(go.Bar(name=grp, x=cities, y=[rng.randint(20, 80) for _ in cities], marker_color=clr))
    fig.update_layout(barmode="group", height=300, margin=dict(t=10,b=10,l=10,r=10),
                      plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                      legend=dict(orientation="h", y=-0.25), yaxis_title="Requests/month")
    st.plotly_chart(fig, use_container_width=True)

    section_heading("Shortage Prediction — Next 30 Days")
    shortage_data = [
        ("O−",  "Chennai",    "High",     78, GREEN),
        ("AB−", "Mumbai",     "Critical", 92, BLOOD_RED),
        ("B−",  "Delhi",      "Moderate", 54, AMBER),
        ("A−",  "Bangalore",  "High",     71, AMBER),
        ("O+",  "Hyderabad",  "Moderate", 61, AMBER),
    ]
    for bg, city, risk, prob, clr in shortage_data:
        st.markdown(f"""
<div style="background:#FFF;border-radius:8px;padding:10px 14px;margin-bottom:8px;
     border-left:4px solid {clr};box-shadow:0 1px 3px rgba(0,0,0,.06);
     display:flex;justify-content:space-between;align-items:center;">
  <div>
    <span style="font-weight:700;color:{NAVY};">{bg} · {city}</span>
    <span class="badge badge-{'red' if risk=='Critical' else 'amber' if risk=='High' else 'grey'}" style="margin-left:8px;">{risk} Risk</span>
  </div>
  <div style="display:flex;align-items:center;gap:12px;">
    <div style="width:120px;background:#F0F4F8;border-radius:4px;height:8px;">
      <div style="background:{clr};width:{prob}%;height:8px;border-radius:4px;"></div>
    </div>
    <span style="font-size:.82rem;font-weight:600;color:{clr};">{prob}%</span>
  </div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM HEALTH
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "🛡️ System Health":
    st.markdown(f'<div class="bl-header"><h1>🛡️ System Health</h1><p>Platform operational status.</p></div>', unsafe_allow_html=True)

    health_items = [
        ("Coordination Engine",      "Operational", GREEN),
        ("Donor Matching Service",   "Operational", GREEN),
        ("Emergency Escalation",     "Operational", GREEN),
        ("Inventory Sync",           "Operational", GREEN),
        ("Demand Forecasting Engine","Operational", GREEN),
        ("Expiry Risk Monitor",      "Operational", GREEN),
        ("BloodLife AI Assistant",   "Operational", GREEN),
        ("Notification Service",     "Operational", GREEN),
        ("Audit Logging",            "Operational", GREEN),
        ("Verification Workflow",    "Operational", GREEN),
    ]
    cols = st.columns(2)
    for i, (service, status, clr) in enumerate(health_items):
        with cols[i % 2]:
            st.markdown(f"""
<div style="background:#FFF;border-radius:8px;padding:10px 16px;margin-bottom:8px;
     display:flex;justify-content:space-between;align-items:center;
     box-shadow:0 1px 3px rgba(0,0,0,.06);">
  <div style="font-size:.88rem;color:{NAVY};">{service}</div>
  <span class="badge badge-green">● {status}</span>
</div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    section_heading("Database Statistics (Demo)")
    db_stats = [
        ("users",              "5,214"),
        ("donors",             "8,742"),
        ("hospitals",          "1,136"),
        ("blood_banks",          "284"),
        ("blood_requests",    "52,480"),
        ("blood_inventory",    "2,048"),
        ("audit_logs",        "98,341"),
        ("notifications",     "24,100"),
    ]
    cols2 = st.columns(4)
    for i, (table, count) in enumerate(db_stats):
        with cols2[i % 4]:
            st.markdown(f"""
<div style="background:#F7F8FA;border-radius:8px;padding:12px;margin-bottom:8px;text-align:center;">
  <div style="font-size:1.1rem;font-weight:700;color:{NAVY};">{count}</div>
  <div style="font-size:.72rem;color:{GREY};font-family:monospace;">{table}</div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT LOGS
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "📝 Audit Logs":
    st.markdown(f'<div class="bl-header"><h1>📝 System Audit Logs</h1><p>Complete platform audit trail.</p></div>', unsafe_allow_html=True)

    filter_event = st.selectbox("Filter by event type", ["All"] + list({l["event"] for l in AUDIT_LOG}))
    logs = AUDIT_LOG if filter_event == "All" else [l for l in AUDIT_LOG if l["event"] == filter_event]

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

    for log in logs:
        clr, icon = EVENT_COLOURS.get(log["event"], (GREY, "📋"))
        st.markdown(f"""
<div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:8px;">
  <div style="min-width:140px;font-size:.75rem;color:{GREY};padding-top:3px;font-family:monospace;">{log['timestamp']}</div>
  <div style="width:26px;height:26px;border-radius:50%;background:{clr}22;border:1px solid {clr};
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
