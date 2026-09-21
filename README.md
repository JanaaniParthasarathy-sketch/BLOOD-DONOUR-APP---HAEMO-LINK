# 🩸 BloodLife — Intelligent Blood-Life Coordination & Prediction Platform

> **"Connecting Every Drop to the Right Need."**

A production-quality, role-based healthcare coordination platform built with Streamlit, connecting **blood donors, patients, hospitals, blood banks, and administrators** through one intelligent system.

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 🧠 What is BloodLife?

BloodLife is a **predictive blood-resource coordination platform** — not just a blood donor app.

At its core is the **BloodLife Intelligent Coordination Engine**, which continuously evaluates:

- Donor availability & verification status
- Blood bank inventory & component levels
- Hospital blood requirements & urgency
- Geographic proximity (privacy-preserving)
- Emergency escalation stages
- Demand forecasting signals
- Expiry risk indicators

---

## 👥 Role-Based Experiences

| Role | Portal | Key Features |
|------|--------|--------------|
| 👤 **Donor** | My BloodLife | Registration, nearby requests, Impact Passport, availability toggle, smart notifications |
| 🧑‍🦽 **Patient** | Find Blood | Blood request form, real-time status tracking, verification display |
| 🏥 **Hospital** | Command Centre | Emergency coordination, inventory matrix, donor responses, AI copilot, audit log |
| 🩸 **Blood Bank** | Operations Centre | Inventory intelligence, expiry risk monitor, demand forecasting, rare blood network |
| 🛡️ **Admin** | Network Control | Platform analytics, verification management, regional demand, system health |
| 🤖 **AI** | BloodLife AI | Operational assistant — FAQs, summaries, navigation (no clinical decisions) |

---

## 🗂️ Project Structure

```
├── app.py                      ← Landing page + role selector
├── requirements.txt
├── .streamlit/
│   ├── config.toml             ← Theme configuration
│   └── pages.toml              ← Multipage navigation
├── utils/
│   └── theme.py                ← CSS, colour constants, UI helpers
├── data/
│   └── demo_data.py            ← Simulated data layer (all collections)
└── pages/
    ├── 1_Donor.py              ← Donor portal
    ├── 2_Patient.py            ← Patient / Requester
    ├── 3_Hospital.py           ← Hospital Command Centre
    ├── 4_BloodBank.py          ← Blood Bank Operations Centre
    ├── 5_Admin.py              ← Admin Network Control
    └── 6_AI_Assistant.py       ← BloodLife AI Chat
```

---

## 🧪 Intelligence Features

- **Emergency Escalation Engine** — 8-stage adaptive orchestration
- **Multi-factor Donor Matching** — suitability scores (compatibility + availability + distance + history)
- **Demand Forecasting** — per blood-group/component with confidence intervals
- **Expiry Risk Monitor** — flags units for authorized staff review before wastage
- **Rare Blood Intelligence Network** — regional gap analysis for rare groups
- **Verified Request System** — Hospital / Blood Bank / Pending / Expired verification states
- **Privacy-Preserving Location** — approximate km only, never exact addresses

---

## 🎨 Design Language

- **Deep Medical Navy** `#0B1F33` — navigation, headers
- **Medical Blue** `#1769AA` — primary actions, links
- **Blood Red** `#C62828` — blood accents, critical indicators
- **Success Green** `#2E7D32` — verified, fulfilled, available
- **Warning Amber** `#F9A825` — attention required, expiry risk

---

## ⚕️ Important Disclaimer

> BloodLife is a **coordination and decision-support platform**.
> It does **not** make independent clinical transfusion decisions, diagnose patients, prescribe treatment, or override authorized blood-bank screening.
> All clinical decisions remain with qualified healthcare professionals.
> All data in this demo is **simulated** — it does not represent real patient, donor, or institution information.

---

## 🛠️ Tech Stack

- **Frontend & App**: [Streamlit](https://streamlit.io) 1.32+
- **Charts**: [Plotly](https://plotly.com/python/)
- **Data**: [Pandas](https://pandas.pydata.org/) + [NumPy](https://numpy.org/)
- **AI Assistant**: Rule-based knowledge engine (IBM watsonx/Granite integration ready)

---

*BloodLife · Intelligent Blood-Life Coordination & Prediction Platform*
