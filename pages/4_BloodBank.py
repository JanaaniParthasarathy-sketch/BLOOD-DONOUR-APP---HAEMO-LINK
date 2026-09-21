"""
BloodLife — Blood Bank Operations Centre
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
    INVENTORY, DONORS, REQUESTS, DEMAND_FORECAST, EXPIRY_RISK, HOSPITALS,
    INVENTORY_THRESHOLDS, inventory_status, MONTHS, INVENTORY_TREND, score_label,
)

st.set_page_config(page_title="Blood Bank Operations — BloodLife", page_icon="🩸", layout="wide")
inject_global_css()

with st.sidebar:
    st.markdown("""
<div style="text-align:center;padding:12px 0;">
  <span style="font-size:1.8rem;">🩸</span>
  <div style="font-size:1.2rem;font-weight:800;color:#FFF;">BloodLife</div>
  <div style="font-size:.7rem;color:#90CAF9;">Blood Bank Operations</div>
</div><hr/>""", unsafe_allow_html=True)

    nav = st.radio("Module", [
        "🏠 Overview",
        "🧪 Inventory Command",
        "👥 Donor Network",
        "📋 Requests",
        "⚠️ Expiry Risk Monitor",
        "📈 Demand Forecast",
        "🏥 Hospital Coordination",
        "📊 Analytics",
        "🧬 Rare Blood Network",
    ], label_visibility="collapsed")

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:.75rem;color:#90CAF9;">Indian Red Cross Blood Bank</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.7rem;color:#607D8B;margin-top:2px;">Chennai · Verified Blood Bank</div>', unsafe_allow_html=True)
    st.markdown("<hr/><a href='/' style='color:#90CAF9;font-size:.8rem;'>← Home</a>", unsafe_allow_html=True)

demo_banner()

# ═══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if nav == "🏠 Overview":
    st.markdown(f"""
<div style="background:{NAVY};border-radius:14px;padding:24px 32px;margin-bottom:24px;color:#FFF;">
  <div style="font-size:1.6rem;font-weight:800;">🩸 Blood Bank Operations Centre</div>
  <div style="font-size:.9rem;color:#90CAF9;">Indian Red Cross Blood Bank, Chennai · BloodLife Network</div>
</div>""", unsafe_allow_html=True)

    total_units = sum(sum(r[c] for c in ["RBC","Platelets","FFP","Cryoprecipitate","Whole Blood"]) for r in INVENTORY)
    low_stock   = sum(1 for r in INVENTORY for c in ["RBC","Platelets","FFP"] if r[c] < INVENTORY_THRESHOLDS[c])
    expiring    = sum(e["units"] for e in EXPIRY_RISK)
    critical_comp = sum(1 for r in INVENTORY for c in ["RBC","Platelets"] if r[c] == 0 or r[c] < INVENTORY_THRESHOLDS[c]//2)

    kpis = [
        (str(total_units), "Total Units",        BLUE),
        (str(low_stock),   "Low Stock Items",    AMBER),
        (str(expiring),    "Expiring Soon (units)",BLOOD_RED),
        (str(critical_comp),"Critical Components",BLOOD_RED),
        (str(len([d for d in DONORS if d["verified"]])), "Verified Donors", GREEN),
    ]
    cols = st.columns(5)
    for col, (val, lbl, clr) in zip(cols, kpis):
        with col:
            st.markdown(f'<div class="bl-stat" style="border-top:3px solid {clr};"><div class="num" style="color:{clr};">{val}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    left, right = st.columns([2, 1])

    with left:
        section_heading("🧪 Inventory Matrix")
        header = st.columns([1.5, 1, 1, 1, 1, 1])
        for col, hdr in zip(header, ["Group", "RBC", "Platelets", "FFP", "Cryo", "WB"]):
            col.markdown(f'<div style="font-size:.72rem;font-weight:700;color:{GREY};text-transform:uppercase;">{hdr}</div>', unsafe_allow_html=True)
        st.markdown('<hr style="margin:4px 0 8px 0;"/>', unsafe_allow_html=True)
        for row in INVENTORY:
            cols_row = st.columns([1.5, 1, 1, 1, 1, 1])
            cols_row[0].markdown(f'<strong style="color:{NAVY};">{row["blood_group"]}</strong>', unsafe_allow_html=True)
            for i, comp in enumerate(["RBC", "Platelets", "FFP", "Cryoprecipitate", "Whole Blood"]):
                v = row[comp]
                t = INVENTORY_THRESHOLDS[comp]
                c = GREEN if v >= t else AMBER if v >= t//2 else BLOOD_RED
                cols_row[i+1].markdown(f'<span style="font-weight:600;color:{c};">{v}</span>', unsafe_allow_html=True)

    with right:
        section_heading("⚠️ Intelligence Alerts")
        alerts = [
            (BLOOD_RED, "🚨", "O− shortage approaching",      "18 units — below threshold"),
            (BLOOD_RED, "⚠️", "AB− critically low",           "6 RBC units only"),
            (AMBER,     "⏰", "12 units expiring in 48h",     "Review recommended"),
            (BLUE,      "📈", "O+ demand forecast: +36%",     "Plan donor drive"),
            (GREEN,     "✅", "Platelets stocked adequately", "Most groups above threshold"),
        ]
        for clr, icon, title, detail in alerts:
            st.markdown(f"""
<div style="background:{clr}11;border-left:3px solid {clr};border-radius:6px;padding:8px 12px;margin-bottom:6px;">
  <div style="font-size:.85rem;font-weight:600;color:{NAVY};">{icon} {title}</div>
  <div style="font-size:.75rem;color:{GREY};">{detail}</div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INVENTORY COMMAND
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "🧪 Inventory Command":
    st.markdown(f'<div class="bl-header"><h1>🧪 Inventory Command Centre</h1><p>Real-time blood component inventory management.</p></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        section_heading("Inventory by Blood Group (RBC)")
        fig = go.Figure(go.Bar(
            x=[r["blood_group"] for r in INVENTORY],
            y=[r["RBC"] for r in INVENTORY],
            marker_color=[GREEN if r["RBC"] >= 20 else AMBER if r["RBC"] >= 10 else BLOOD_RED for r in INVENTORY],
            text=[r["RBC"] for r in INVENTORY], textposition="outside",
        ))
        fig.add_hline(y=20, line_dash="dash", line_color=AMBER, annotation_text="Threshold")
        fig.update_layout(height=280, margin=dict(t=20,b=10,l=10,r=10),
                          plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                          yaxis_title="RBC Units")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        section_heading("Component Distribution (All Groups)")
        comp_totals = {c: sum(r[c] for r in INVENTORY) for c in ["RBC","Platelets","FFP","Cryoprecipitate","Whole Blood"]}
        fig2 = go.Figure(go.Bar(
            x=list(comp_totals.keys()),
            y=list(comp_totals.values()),
            marker_color=[BLUE, GREEN, AMBER, BLOOD_RED, GREY],
        ))
        fig2.update_layout(height=280, margin=dict(t=20,b=10,l=10,r=10),
                           plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                           yaxis_title="Total Units")
        st.plotly_chart(fig2, use_container_width=True)

    section_heading("Detailed Inventory with Status")
    for row in INVENTORY:
        bg = row["blood_group"]
        cols = st.columns([1, 1.5, 1.5, 1.5, 1.5, 1.5, 1])
        cols[0].markdown(f'<strong style="color:{NAVY};font-size:1rem;">{bg}</strong>', unsafe_allow_html=True)
        for i, comp in enumerate(["RBC", "Platelets", "FFP", "Cryoprecipitate", "Whole Blood"]):
            v = row[comp]; t = INVENTORY_THRESHOLDS[comp]
            status = inventory_status(v, t)
            clr = GREEN if status == "AVAILABLE" else AMBER if status == "LOW STOCK" else BLOOD_RED
            badge_cls = "badge-green" if status == "AVAILABLE" else "badge-amber" if status == "LOW STOCK" else "badge-red"
            cols[i+1].markdown(f'<span style="font-weight:700;color:{clr};">{v}</span> <span class="badge {badge_cls}" style="font-size:.65rem;">{status}</span>', unsafe_allow_html=True)
        exp = row.get("rbc_expiring", 0)
        cols[6].markdown(f'{"⚠️" if exp > 0 else "✅"} <span style="font-size:.78rem;color:{BLOOD_RED if exp>0 else GREEN};">{exp} expiring</span>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    section_heading("Inventory Trend — O+ RBC (12 months)")
    fig3 = go.Figure()
    for bg, colour in [("O+", BLOOD_RED), ("A+", BLUE), ("B+", GREEN)]:
        fig3.add_trace(go.Scatter(x=MONTHS, y=INVENTORY_TREND[bg],
                                   name=f"{bg} RBC", line=dict(color=colour, width=2), mode="lines+markers"))
    fig3.add_hline(y=20, line_dash="dash", line_color=AMBER, annotation_text="Threshold (20u)")
    fig3.update_layout(height=260, margin=dict(t=20,b=10,l=10,r=10),
                       plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                       legend=dict(orientation="h", y=-0.25), yaxis_title="Units")
    st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DONOR NETWORK
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "👥 Donor Network":
    st.markdown(f'<div class="bl-header"><h1>👥 Donor Network</h1><p>Manage and monitor your registered donor pool.</p></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, (val, lbl, clr) in zip([c1,c2,c3,c4],[
        (str(len(DONORS)), "Registered", BLUE),
        (str(len([d for d in DONORS if d["verified"]])), "Verified", GREEN),
        (str(len([d for d in DONORS if d["availability"] == "Available Now"])), "Available Now", GREEN),
        ("3", "Rare Group", AMBER),
    ]):
        with col:
            st.markdown(f'<div class="bl-stat" style="border-top:3px solid {clr};"><div class="num" style="color:{clr};">{val}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    section_heading("🎯 Donor Matching Engine — Suitability Scores")
    st.markdown(f'<div style="font-size:.8rem;color:{GREY};margin-bottom:10px;">The suitability score is an operational prioritization signal, NOT a medical compatibility decision. Scores factor in availability, verification, distance, history, and response rate.</div>', unsafe_allow_html=True)

    available_donors = [d for d in DONORS if d["score"] > 0]
    available_donors.sort(key=lambda x: x["score"], reverse=True)

    for donor in available_donors[:8]:
        av_clr = {"Available Now": GREEN, "Available Today": AMBER, "Available Later": BLUE}.get(donor["availability"], GREY)
        score_clr = GREEN if donor["score"] >= 90 else BLUE if donor["score"] >= 75 else AMBER
        st.markdown(f"""
<div style="background:#FFF;border-radius:10px;padding:12px 18px;margin-bottom:8px;
     box-shadow:0 1px 4px rgba(0,0,0,.07);display:flex;justify-content:space-between;
     align-items:center;flex-wrap:wrap;gap:10px;border-left:4px solid {score_clr};">
  <div style="display:flex;gap:14px;align-items:center;">
    <div style="background:{score_clr}22;border:2px solid {score_clr};border-radius:8px;
         padding:8px 12px;font-weight:800;color:{score_clr};font-size:1rem;">{donor['blood_group']}</div>
    <div>
      <div style="font-weight:600;color:{NAVY};">Donor ID {donor['id']}</div>
      <div style="font-size:.78rem;color:{GREY};">~{donor['distance_km']} km · Last: {donor['last_donation']}</div>
    </div>
  </div>
  <div style="display:flex;gap:16px;align-items:center;">
    <div>
      <div style="font-size:.7rem;color:{GREY};text-transform:uppercase;">Availability</div>
      <div style="font-size:.85rem;font-weight:600;color:{av_clr};">{donor['availability']}</div>
    </div>
    <div>
      <div style="font-size:.7rem;color:{GREY};text-transform:uppercase;">Suitability</div>
      <div style="font-size:1.1rem;font-weight:800;color:{score_clr};">{donor['score']}</div>
    </div>
    <div>
      <div style="font-size:.7rem;color:{GREY};text-transform:uppercase;">Status</div>
      <span class="badge {'badge-green' if donor['verified'] else 'badge-amber'}">{'✅ Verified' if donor['verified'] else '⏳ Pending'}</span>
    </div>
    <div>
      <div style="font-size:.7rem;color:{GREY};text-transform:uppercase;">Response Rate</div>
      <div style="font-size:.85rem;font-weight:600;color:{NAVY};">{int(donor['response_rate']*100)}%</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# REQUESTS
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "📋 Requests":
    st.markdown(f'<div class="bl-header"><h1>📋 Blood Requests</h1><p>Manage incoming requests and allocations.</p></div>', unsafe_allow_html=True)

    for req in REQUESTS:
        sc = {"Fulfilled": GREEN, "Searching": BLOOD_RED, "Escalated": BLOOD_RED,
              "Donor Contacted": BLUE, "Partially Fulfilled": AMBER, "Pending": GREY}.get(req["status"], GREY)
        vc = "badge-green" if "Hospital" in req["verification"] else "badge-blue" if "Blood Bank" in req["verification"] else "badge-amber"
        st.markdown(f"""
<div class="bl-card" style="border-left:5px solid {sc};">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <div>
      <span style="font-weight:700;color:{NAVY};">{req['id']}</span>
      <span style="font-size:.88rem;color:{GREY};margin-left:8px;">{req['blood_group']} {req['component']} · {req['units']} units</span>
      <span class="badge badge-{'red' if req['urgency']=='Critical' else 'amber' if req['urgency']=='Urgent' else 'grey'}" style="margin-left:6px;">{req['urgency']}</span>
    </div>
    <div style="text-align:right;">
      <span style="font-weight:600;color:{sc};">● {req['status']}</span><br/>
      <span class="badge {vc}" style="font-size:.7rem;">{req['verification']}</span>
    </div>
  </div>
  <div style="font-size:.8rem;color:{GREY};margin-top:6px;">🏥 {req['hospital']} · 🕐 {req['created']} · 📝 {req.get('notes','—')}</div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# EXPIRY RISK MONITOR
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "⚠️ Expiry Risk Monitor":
    st.markdown(f'<div class="bl-header"><h1>⚠️ Expiry Risk Monitor</h1><p>Units approaching expiry requiring authorized staff review.</p></div>', unsafe_allow_html=True)

    st.markdown(f"""
<div style="background:#FFF3E0;border:1px solid {AMBER};border-radius:8px;padding:14px 18px;margin-bottom:16px;font-size:.85rem;color:#7B5E00;">
  ⚕️ <strong>Operational Note:</strong> This monitor flags inventory for authorized blood-bank staff review.
  BloodLife does NOT automatically transfer, issue, discard or allocate blood.
  All operational decisions remain with licensed blood-bank professionals.
</div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    high   = [e for e in EXPIRY_RISK if e["risk_level"] == "High"]
    attn   = [e for e in EXPIRY_RISK if e["risk_level"] == "Attention"]
    low_r  = [e for e in EXPIRY_RISK if e["risk_level"] == "Low"]

    with c1:
        st.markdown(f'<div class="bl-stat" style="border-top:3px solid {BLOOD_RED};"><div class="num" style="color:{BLOOD_RED};">{sum(e["units"] for e in high)}</div><div class="lbl">High Risk Units</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="bl-stat" style="border-top:3px solid {AMBER};"><div class="num" style="color:{AMBER};">{sum(e["units"] for e in attn)}</div><div class="lbl">Attention Required</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="bl-stat" style="border-top:3px solid {GREEN};"><div class="num" style="color:{GREEN};">{sum(e["units"] for e in low_r)}</div><div class="lbl">Low Risk</div></div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    section_heading("High Risk — Immediate Review Required")
    for e in high:
        st.markdown(f"""
<div class="bl-card" style="border-left:5px solid {BLOOD_RED};">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <div>
      <span style="font-weight:700;color:{BLOOD_RED};font-size:1rem;">{e['blood_group']} {e['component']}</span>
      <span class="badge badge-red" style="margin-left:8px;">HIGH RISK</span>
    </div>
    <div style="text-align:right;">
      <div style="font-weight:600;color:{BLOOD_RED};">{e['units']} unit(s)</div>
      <div style="font-size:.78rem;color:{GREY};">Expires in {e['expiry_days']} day(s)</div>
    </div>
  </div>
  <div style="margin-top:10px;font-size:.8rem;color:{GREY};">
    🔍 <strong>Recommended:</strong> Authorized staff review required. Consider whether current requests can be fulfilled using these units, subject to standard screening and clinical protocols.
  </div>
</div>""", unsafe_allow_html=True)

    section_heading("Attention Required")
    for e in attn:
        st.markdown(f"""
<div class="bl-card" style="border-left:5px solid {AMBER};">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <div>
      <span style="font-weight:700;color:{NAVY};">{e['blood_group']} {e['component']}</span>
      <span class="badge badge-amber" style="margin-left:8px;">ATTENTION</span>
    </div>
    <div style="text-align:right;">
      <div style="font-weight:600;color:{AMBER};">{e['units']} unit(s) · {e['expiry_days']} days</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DEMAND FORECAST
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "📈 Demand Forecast":
    st.markdown(f'<div class="bl-header"><h1>📈 Blood Demand Forecasting</h1><p>AI/ML-based predictive demand analysis using historical patterns.</p></div>', unsafe_allow_html=True)

    st.markdown(f"""
<div style="background:{LIGHT_BLUE};border:1px solid {BLUE};border-radius:8px;padding:12px 16px;margin-bottom:16px;font-size:.82rem;color:#0D47A1;">
  🔬 <strong>Methodology:</strong> Predictions are generated from historical request patterns, seasonal trends and inventory depletion rates.
  Confidence intervals are shown where applicable. <strong>These are operational signals, not guaranteed outcomes.</strong>
</div>""", unsafe_allow_html=True)

    section_heading("Predicted Demand — Next 14 Days")
    for fc in DEMAND_FORECAST:
        risk_clr  = BLOOD_RED if fc["risk"] == "High" else AMBER if fc["risk"] == "Elevated" else GREEN if fc["risk"] == "Low" else GREY
        risk_badge= "badge-red" if fc["risk"] == "High" else "badge-amber" if fc["risk"] in ("Elevated","Moderate") else "badge-green"
        delta_pct = round((fc["forecast"] - fc["current"]) / max(fc["current"], 1) * 100)
        conf_pct  = int(fc["confidence"] * 100)
        st.markdown(f"""
<div class="bl-card" style="border-left:5px solid {risk_clr};">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
    <div>
      <div style="display:flex;align-items:center;gap:10px;">
        <span style="font-weight:800;font-size:1.1rem;color:{NAVY};">{fc['blood_group']} {fc['component']}</span>
        <span class="badge {risk_badge}">⚠️ {fc['risk']} Risk</span>
      </div>
      <div style="margin-top:8px;display:flex;gap:24px;">
        <div><div style="font-size:.72rem;color:{GREY};text-transform:uppercase;">Current Demand</div>
             <div style="font-weight:700;color:{NAVY};font-size:1rem;">{fc['current']} units/day</div></div>
        <div><div style="font-size:.72rem;color:{GREY};text-transform:uppercase;">Forecast Demand</div>
             <div style="font-weight:700;color:{risk_clr};font-size:1rem;">{fc['forecast']} units/day</div></div>
        <div><div style="font-size:.72rem;color:{GREY};text-transform:uppercase;">Change</div>
             <div style="font-weight:700;color:{risk_clr};">+{delta_pct}%</div></div>
        <div><div style="font-size:.72rem;color:{GREY};text-transform:uppercase;">Confidence</div>
             <div style="font-weight:600;color:{NAVY};">{conf_pct}%</div></div>
      </div>
    </div>
    <div style="width:120px;">
      <div style="background:#F0F4F8;border-radius:6px;height:8px;">
        <div style="background:{risk_clr};height:8px;border-radius:6px;width:{conf_pct}%;"></div>
      </div>
      <div style="font-size:.72rem;color:{GREY};margin-top:3px;text-align:center;">Confidence: {conf_pct}%</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    section_heading("Demand vs Supply Chart")
    groups = [f["blood_group"]+" "+f["component"] for f in DEMAND_FORECAST]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Current", x=groups, y=[f["current"] for f in DEMAND_FORECAST], marker_color=BLUE))
    fig.add_trace(go.Bar(name="Forecast", x=groups, y=[f["forecast"] for f in DEMAND_FORECAST], marker_color=BLOOD_RED, opacity=0.8))
    fig.update_layout(height=300, barmode="group", margin=dict(t=20,b=10,l=10,r=10),
                      plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                      legend=dict(orientation="h", y=-0.25), yaxis_title="Units/day")
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HOSPITAL COORDINATION
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "🏥 Hospital Coordination":
    st.markdown(f'<div class="bl-header"><h1>🏥 Hospital Coordination</h1><p>Supply coordination with partner hospitals.</p></div>', unsafe_allow_html=True)

    for h in HOSPITALS:
        vc = GREEN if h["verified"] else AMBER
        pending = len([r for r in REQUESTS if r["hospital"] == h["name"] and r["status"] not in ("Fulfilled",)])
        st.markdown(f"""
<div class="bl-card" style="border-left:4px solid {vc};">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <div>
      <div style="font-weight:700;color:{NAVY};">{h['name']}</div>
      <div style="font-size:.82rem;color:{GREY};">📍 {h['city']} · ~{h['distance_km']} km · {h['beds']} beds</div>
    </div>
    <div style="display:flex;gap:10px;align-items:center;">
      <span class="badge {'badge-green' if h['verified'] else 'badge-amber'}">{'✅ Verified' if h['verified'] else '⏳ Pending'}</span>
      {f'<span class="badge badge-red">{pending} pending requests</span>' if pending else '<span class="badge badge-green">No pending requests</span>'}
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "📊 Analytics":
    st.markdown(f'<div class="bl-header"><h1>📊 Blood Bank Analytics</h1><p>Operational performance and trend analysis.</p></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        section_heading("Donation Collection Trend")
        from data.demo_data import DONOR_GROWTH
        fig = go.Figure(go.Scatter(x=MONTHS, y=DONOR_GROWTH, fill="tozeroy",
                                    line=dict(color=BLOOD_RED, width=2),
                                    fillcolor=f"rgba(198,40,40,0.1)"))
        fig.update_layout(height=260, margin=dict(t=10,b=10,l=10,r=10),
                          plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF", yaxis_title="Donations")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        section_heading("Blood Group Distribution in Inventory")
        totals_bg = {r["blood_group"]: sum(r[c] for c in ["RBC","Platelets","FFP"]) for r in INVENTORY}
        fig2 = go.Figure(go.Pie(
            labels=list(totals_bg.keys()),
            values=list(totals_bg.values()),
            hole=0.4,
            marker_colors=[BLUE, "#1565C0", BLOOD_RED, "#C2185B", GREEN, "#388E3C", AMBER, GREY],
        ))
        fig2.update_layout(height=260, margin=dict(t=10,b=10,l=10,r=10), paper_bgcolor="#FFFFFF")
        st.plotly_chart(fig2, use_container_width=True)

    section_heading("Expiry Risk Over Time (Simulated)")
    expiry_trend = [2, 3, 5, 4, 6, 8, 5, 4, 7, 9, 11, 12]
    fig3 = go.Figure(go.Scatter(x=MONTHS, y=expiry_trend, fill="tozeroy",
                                 line=dict(color=AMBER, width=2),
                                 fillcolor="rgba(249,168,37,0.15)", mode="lines+markers"))
    fig3.update_layout(height=220, margin=dict(t=10,b=10,l=10,r=10),
                       plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF", yaxis_title="Units at Risk")
    st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# RARE BLOOD NETWORK
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "🧬 Rare Blood Network":
    st.markdown(f'<div class="bl-header"><h1>🧬 Rare Blood Intelligence Network</h1><p>Verified rare blood group donor coordination.</p></div>', unsafe_allow_html=True)

    st.markdown(f"""
<div style="background:#F3E5F5;border:1px solid #CE93D8;border-radius:8px;padding:12px 16px;margin-bottom:16px;font-size:.82rem;color:#4A148C;">
  🔒 Rare donor personal information is strictly protected. Only authorized staff can initiate contact through verified workflows.
  Donors only see approximate distance — never patient or hospital personal details.
</div>""", unsafe_allow_html=True)

    rare_groups = ["O−", "B−", "A−", "AB−", "AB+"]
    section_heading("Rare Blood Group Donor Network")

    rare_donors = [d for d in DONORS if d["blood_group"] in rare_groups]
    c1, c2, c3 = st.columns(3)
    for col, (val, lbl, clr) in zip([c1,c2,c3],[
        (str(len(rare_donors)), "Rare Group Donors", BLOOD_RED),
        (str(len([d for d in rare_donors if d["verified"]])), "Verified", GREEN),
        (str(len([d for d in rare_donors if d["availability"] == "Available Now"])), "Available Now", AMBER),
    ]):
        with col:
            st.markdown(f'<div class="bl-stat" style="border-top:3px solid {clr};"><div class="num" style="color:{clr};">{val}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    for donor in rare_donors:
        av_clr = {"Available Now": GREEN, "Available Today": AMBER, "Available Later": BLUE,
                  "Unavailable": GREY, "Temporarily Unavailable": BLOOD_RED}.get(donor["availability"], GREY)
        st.markdown(f"""
<div style="background:#FFF;border-radius:10px;padding:12px 18px;margin-bottom:8px;
     box-shadow:0 1px 4px rgba(0,0,0,.07);border-left:4px solid #9C27B0;
     display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
  <div style="display:flex;gap:12px;align-items:center;">
    <div style="background:#F3E5F5;border:2px solid #9C27B0;border-radius:8px;
         padding:8px 12px;font-weight:800;color:#6A1B9A;">{donor['blood_group']}</div>
    <div>
      <div style="font-weight:600;color:{NAVY};">Anonymous Donor · {donor['blood_group']}</div>
      <div style="font-size:.78rem;color:{GREY};">~{donor['distance_km']} km · Donations: {donor['donations']}</div>
    </div>
  </div>
  <div style="display:flex;gap:12px;align-items:center;">
    <span style="color:{av_clr};font-weight:600;font-size:.85rem;">{donor['availability']}</span>
    <span class="badge {'badge-green' if donor['verified'] else 'badge-amber'}">{'✅ Verified' if donor['verified'] else '⏳ Pending'}</span>
    <div style="font-size:.8rem;color:{GREY};">Response: {int(donor['response_rate']*100)}%</div>
  </div>
</div>""", unsafe_allow_html=True)

    section_heading("Regional Availability Gaps")
    gaps = [
        ("B−",  "Southern Chennai", "Only 3 verified donors in region — recruiting recommended"),
        ("AB−", "North Chennai",    "0 verified donors currently available in 10 km radius"),
        ("A−",  "Madurai",          "No linked blood bank has A− stock above threshold"),
    ]
    for bg, region, detail in gaps:
        st.markdown(f"""
<div style="background:#FFF3E0;border:1px solid {AMBER};border-radius:8px;padding:10px 14px;margin-bottom:8px;">
  <div style="font-weight:600;color:{NAVY};">⚠️ {bg} · {region}</div>
  <div style="font-size:.8rem;color:{GREY};margin-top:3px;">{detail}</div>
</div>""", unsafe_allow_html=True)
