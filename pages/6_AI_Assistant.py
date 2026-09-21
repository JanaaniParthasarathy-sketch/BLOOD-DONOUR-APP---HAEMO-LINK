"""
BloodLife AI Assistant — standalone chat page
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from utils.theme import inject_global_css, demo_banner, NAVY, BLUE, BLOOD_RED, GREEN, AMBER, GREY, LIGHT_BLUE, section_heading
from data.demo_data import PLATFORM_STATS

st.set_page_config(page_title="BloodLife AI Assistant", page_icon="🤖", layout="wide")
inject_global_css()

with st.sidebar:
    st.markdown("""
<div style="text-align:center;padding:12px 0;">
  <span style="font-size:1.8rem;">🤖</span>
  <div style="font-size:1.2rem;font-weight:800;color:#FFF;">BloodLife AI</div>
  <div style="font-size:.7rem;color:#90CAF9;">Intelligent Assistant</div>
</div><hr/>""", unsafe_allow_html=True)

    mode = st.radio("Mode", ["💬 General Chat", "🏥 Clinical Operations (Hospital)", "📊 Quick Summaries"], label_visibility="collapsed")
    st.markdown("<hr/>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.pop("ai_chat", None)
        st.rerun()
    st.markdown("<hr/><a href='/' style='color:#90CAF9;font-size:.8rem;'>← Home</a>", unsafe_allow_html=True)

demo_banner()

st.markdown(f"""
<div style="background:{NAVY};border-radius:14px;padding:24px 32px;margin-bottom:20px;color:#FFF;">
  <div style="font-size:1.6rem;font-weight:800;">🤖 BloodLife AI</div>
  <div style="font-size:.9rem;color:#90CAF9;">Operational AI assistant — answers platform questions and summarises operational data.</div>
</div>
""", unsafe_allow_html=True)

# ── Boundaries notice ─────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:#FFF3E0;border:1px solid {AMBER};border-radius:8px;padding:12px 16px;margin-bottom:16px;font-size:.82rem;color:#7B5E00;">
  ⚕️ <strong>Scope of BloodLife AI:</strong> This assistant answers platform questions, summarises operational data, and guides navigation.
  It does NOT diagnose diseases, prescribe treatment, make independent transfusion decisions, override blood-bank screening, guarantee donor eligibility,
  or replace medical professionals. All clinical decisions remain with qualified healthcare staff.
</div>
""", unsafe_allow_html=True)

# ── Knowledge base ────────────────────────────────────────────────────────────
KNOWLEDGE = {
    # Blood requests
    ("request", "blood", "need"): (
        "To create a blood request, use the **Patient / Requester** portal. "
        "Select your blood group, required component (e.g. RBC, Platelets), units needed, urgency, "
        "and the hospital. BloodLife will then search verified blood-bank resources and coordinate "
        "eligible donor notifications. Requests with hospital verification are given higher priority."
    ),
    # Donor registration
    ("register", "donor", "donate", "join"): (
        "To register as a donor, open the **Donor Portal** and select 'Register / Profile'. "
        "You'll provide your blood group, contact details, preferred donation centre, and availability. "
        "Your exact address is never publicly shown — BloodLife uses approximate distance for matching. "
        "After registration, your profile goes through verification by an authorized blood centre."
    ),
    # Blood groups
    ("blood group", "compatible", "match", "type"): (
        "BloodLife supports all eight ABO/Rh blood groups: O+, O−, A+, A−, B+, B−, AB+, AB−. "
        "Compatibility for transfusion is determined clinically — the platform matches requests to "
        "appropriate resources but does not make independent transfusion compatibility decisions. "
        "Rare groups (O−, B−, A−, AB−, AB+) have dedicated monitoring through the Rare Blood Intelligence Network."
    ),
    # Components
    ("component", "rbc", "platelet", "ffp", "plasma", "cryoprecipitate", "whole blood"): (
        "BloodLife supports five blood components: **Whole Blood**, **Packed Red Blood Cells (RBC)**, "
        "**Platelets**, **Fresh Frozen Plasma (FFP)**, and **Cryoprecipitate**. "
        "The required component is specified during the request creation process. "
        "Blood banks manage component-level inventory in the Operations Centre."
    ),
    # Emergency
    ("emergency", "critical", "urgent", "escalat"): (
        "For critical requests, BloodLife activates the Emergency Escalation Engine: "
        "(1) checks verified blood-bank inventory nearby; "
        "(2) scores the eligible donor pool; "
        "(3) notifies the highest-priority donors; "
        "(4) if response is insufficient, expands the search radius; "
        "(5) coordinates with additional blood banks; "
        "(6) automatically stops unnecessary notifications once sufficient fulfilment is confirmed. "
        "Hospital staff can monitor escalation status in the Hospital Command Centre."
    ),
    # Inventory
    ("inventory", "stock", "units", "available"): (
        "Blood bank inventory is managed in the **Blood Bank Operations Centre**. "
        f"The current simulated network total across all groups and components is approximately 403 units. "
        "Inventory status labels: AVAILABLE (above threshold), LOW STOCK (below threshold), CRITICAL (near zero), "
        "EXPIRING SOON (approaching shelf life). Authorized blood-bank staff review and manage inventory."
    ),
    # Verification
    ("verify", "verified", "verification", "trust"): (
        "BloodLife has a multi-level verification system: "
        "🟢 **Hospital Verified** — authenticated by a registered hospital; "
        "🔵 **Blood Bank Verified** — confirmed by a registered blood bank; "
        "🟡 **Pending Verification** — submitted but not yet institutionally confirmed; "
        "🔴 **Expired / Closed** — request is no longer active. "
        "Verified requests receive higher coordination priority. Donors can see verification status before responding."
    ),
    # Expiry
    ("expir", "wast", "shelf life"): (
        "The **Expiry Risk Monitor** (Blood Bank Operations Centre) flags blood components approaching expiry "
        "for authorized staff review. BloodLife does NOT automatically transfer, issue, discard or allocate blood. "
        "All decisions remain with licensed blood-bank professionals. Categories: Low Risk, Attention Required, High Risk."
    ),
    # Forecast
    ("forecast", "predict", "demand", "shortage"): (
        "The **Demand Forecasting** module uses historical request patterns, seasonal trends and inventory depletion "
        "rates to predict future blood-group and component demand. Predictions are operational signals with confidence "
        "intervals — they are NOT guaranteed outcomes. Blood banks use these signals to plan donor drives proactively."
    ),
    # Privacy
    ("privacy", "address", "location", "personal"): (
        "BloodLife uses privacy-preserving location matching. Donor exact addresses are never publicly shown. "
        "Matching displays approximate distance only (e.g. 'approximately 2.8 km away'). "
        "Precise donation/meeting locations are only shared through authorized workflows after a donor accepts. "
        "BloodLife stores only the minimum information necessary for coordination."
    ),
    # Near Chennai
    ("chennai", "near me", "nearby", "location"): (
        "BloodLife can help you create a verified request and identify available blood-bank resources and "
        "eligible donor notifications based on the information you provide. Select your location during request "
        "creation and the coordination engine will prioritise resources nearest to your hospital."
    ),
    # Hospital
    ("hospital", "command", "centre", "dashboard"): (
        "The **Hospital Command Centre** provides: Active Emergencies, Pending & Fulfilled Requests, "
        "Blood Availability matrix, Donor Response tracking, Nearby Blood Banks, Analytics, "
        "AI Copilot, and Audit Log. Hospital staff can create, verify and track requests, "
        "monitor escalation stages, and coordinate with blood banks."
    ),
    # Blood bank portal
    ("blood bank", "operations", "bank"): (
        "The **Blood Bank Operations Centre** provides: Inventory Command, Donor Network with suitability scores, "
        "Request management, Expiry Risk Monitor, Demand Forecasting, Hospital Coordination, Analytics, "
        "and Rare Blood Intelligence Network."
    ),
    # Admin
    ("admin", "administrator", "network control"): (
        "The **Admin Network Control Centre** provides platform-wide analytics: donor growth, request trends, "
        "fulfilment rates, regional demand, shortage predictions, verification management, system health monitoring, "
        "and complete audit logs."
    ),
    # Donor impact
    ("impact", "lives", "contribution", "passport"): (
        "The **Donor Impact Passport** shows your verified donation history, contribution events, camps attended "
        "and requests assisted. BloodLife uses careful language: 'Your verified donations contributed to X "
        "completed blood-support events.' Clinical impact depends on processing and clinical use, as determined "
        "by the receiving institution."
    ),
    # Availability
    ("availab", "status", "online"): (
        "Donors can set five availability states: 🟢 Available Now, 🟡 Available Today, 🔵 Available Later, "
        "⚪ Unavailable, 🔴 Temporarily Unavailable. The coordination engine uses this status to determine "
        "which donors to notify and in what sequence."
    ),
}

def get_ai_response(user_msg: str) -> str:
    lower = user_msg.lower()
    for keywords, response in KNOWLEDGE.items():
        if any(k in lower for k in keywords):
            return response
    # Operational summary fallback
    if any(w in lower for w in ["summary", "status", "what", "how many", "overview"]):
        return (
            f"**Current Operational Summary (Demo Data):**\n\n"
            f"- 🚨 {PLATFORM_STATS['active_emergencies']} active emergency requests\n"
            f"- 📋 {PLATFORM_STATS['pending_requests']} pending requests\n"
            f"- ✅ {PLATFORM_STATS['requests_fulfilled']:,} requests fulfilled to date\n"
            f"- 👤 {PLATFORM_STATS['active_donors']:,} active donors in network\n"
            f"- 🩸 {PLATFORM_STATS['verified_blood_banks']} verified blood banks\n"
            f"- 🏥 {PLATFORM_STATS['partner_hospitals']:,} partner hospitals\n"
            f"- ⚠️ {PLATFORM_STATS['shortage_alerts']} shortage alerts active\n"
            f"- ⏱️ Average response time: {PLATFORM_STATS['avg_response_min']} minutes"
        )
    return (
        "I can answer questions about: blood requests, donor registration, blood groups, components, "
        "emergency coordination, inventory management, verification, expiry risk, demand forecasting, "
        "privacy settings, and all BloodLife dashboard modules.\n\n"
        "Try asking: *'How do I request blood?'*, *'What is the verification system?'*, "
        "*'How does emergency escalation work?'*, or *'What is the expiry risk monitor?'*"
    )

# ── Chat UI ───────────────────────────────────────────────────────────────────
if "ai_chat" not in st.session_state:
    st.session_state.ai_chat = [
        {
            "role": "assistant",
            "content": (
                "Hello! I'm **BloodLife AI**, your operational assistant.\n\n"
                "I can help you with:\n"
                "- 🩸 Blood requests and donor registration\n"
                "- 🏥 Hospital and blood bank dashboard navigation\n"
                "- 📊 Platform features and operational summaries\n"
                "- ⚠️ Inventory, expiry risk and demand forecasting\n"
                "- 🚨 Emergency escalation workflows\n\n"
                "What would you like to know?"
            )
        }
    ]

# Suggested questions
if len(st.session_state.ai_chat) == 1:
    section_heading("💡 Suggested Questions")
    suggestions = [
        "How do I request blood urgently?",
        "How does donor matching work?",
        "What is the emergency escalation process?",
        "How does BloodLife protect donor privacy?",
        "Give me the current operational summary",
        "What blood components does BloodLife support?",
    ]
    cols = st.columns(3)
    for i, sug in enumerate(suggestions):
        with cols[i % 3]:
            if st.button(sug, key=f"sug_{i}", use_container_width=True):
                st.session_state.ai_chat.append({"role": "user", "content": sug})
                st.session_state.ai_chat.append({"role": "assistant", "content": get_ai_response(sug)})
                st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)

# Display chat
for msg in st.session_state.ai_chat:
    with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Ask BloodLife AI...")
if user_input:
    st.session_state.ai_chat.append({"role": "user", "content": user_input})
    reply = get_ai_response(user_input)
    st.session_state.ai_chat.append({"role": "assistant", "content": reply})
    st.rerun()

# ── Quick summary panel ───────────────────────────────────────────────────────
if mode == "📊 Quick Summaries":
    st.markdown("<br/>", unsafe_allow_html=True)
    section_heading("📊 Quick Operational Summary")
    st.markdown(f"""
<div style="background:{LIGHT_BLUE};border:2px solid {BLUE};border-radius:12px;padding:20px 24px;">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
    <div style="background:#FFF;border-radius:8px;padding:12px 16px;">
      <div style="font-size:.75rem;color:{GREY};text-transform:uppercase;">Active Emergencies</div>
      <div style="font-size:1.5rem;font-weight:800;color:{BLOOD_RED};">{PLATFORM_STATS['active_emergencies']}</div>
    </div>
    <div style="background:#FFF;border-radius:8px;padding:12px 16px;">
      <div style="font-size:.75rem;color:{GREY};text-transform:uppercase;">Pending Requests</div>
      <div style="font-size:1.5rem;font-weight:800;color:{AMBER};">{PLATFORM_STATS['pending_requests']}</div>
    </div>
    <div style="background:#FFF;border-radius:8px;padding:12px 16px;">
      <div style="font-size:.75rem;color:{GREY};text-transform:uppercase;">Active Donors</div>
      <div style="font-size:1.5rem;font-weight:800;color:{BLUE};">{PLATFORM_STATS['active_donors']:,}</div>
    </div>
    <div style="background:#FFF;border-radius:8px;padding:12px 16px;">
      <div style="font-size:.75rem;color:{GREY};text-transform:uppercase;">Avg Response</div>
      <div style="font-size:1.5rem;font-weight:800;color:{GREEN};">{PLATFORM_STATS['avg_response_min']}m</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
