"""BloodLife — centralised demo data store.

All data is clearly simulated.  Nothing here represents real patient, donor,
hospital or blood-bank information.
"""

from __future__ import annotations
import random
from datetime import datetime, timedelta
import pandas as pd

BLOOD_GROUPS = ["O+", "O−", "A+", "A−", "B+", "B−", "AB+", "AB−"]
COMPONENTS   = ["RBC", "Platelets", "FFP", "Cryoprecipitate", "Whole Blood"]

# ── Donors ──────────────────────────────────────────────────────────────────

DONORS: list[dict] = [
    {"id": f"D{1000+i}", "name": n, "blood_group": bg, "city": c,
     "availability": av, "verified": v, "last_donation": ld,
     "distance_km": round(random.uniform(1.2, 18.5), 1),
     "score": s, "donations": d, "phone_masked": "XXXXXX" + str(6000+i)[-4:],
     "response_rate": rr}
    for i, (n, bg, c, av, v, ld, s, d, rr) in enumerate([
        ("Arjun Sharma",      "O+",  "Chennai Central",  "Available Now",          True,  "2024-11-20",  94, 8,  0.92),
        ("Priya Nair",        "A+",  "T. Nagar",         "Available Today",        True,  "2024-10-15",  88, 5,  0.85),
        ("Karthik Rajan",     "O−",  "Velachery",        "Available Now",          True,  "2025-01-05",  96, 12, 0.95),
        ("Meena Subramanian", "B+",  "Anna Nagar",       "Available Later",        True,  "2024-12-01",  79, 4,  0.78),
        ("Rajesh Kumar",      "AB+", "Adyar",            "Available Today",        True,  "2024-09-10",  82, 6,  0.81),
        ("Sunita Patel",      "O+",  "Mylapore",         "Unavailable",            True,  "2025-02-14",  0,  9,  0.90),
        ("Vikram Iyer",       "A−",  "Porur",            "Temporarily Unavailable",True,  "2024-08-22",  0,  3,  0.72),
        ("Ananya Singh",      "B−",  "Sholinganallur",   "Available Now",          True,  "2025-03-01",  91, 7,  0.88),
        ("Deepak Menon",      "O−",  "Egmore",           "Available Now",          True,  "2025-03-10",  97, 15, 0.97),
        ("Lavanya Krishnan",  "AB−", "Nungambakkam",     "Available Today",        False, "2024-07-18",  0,  2,  0.60),
        ("Suresh Balaji",     "O+",  "Guindy",           "Available Now",          True,  "2024-12-20",  90, 10, 0.91),
        ("Divya Ranganathan", "A+",  "Pallavaram",       "Available Later",        True,  "2025-01-28",  75, 3,  0.74),
        ("Ravi Chandrasekar", "B+",  "Chromepet",        "Available Now",          True,  "2025-02-05",  85, 6,  0.83),
        ("Nithya Venkat",     "O−",  "Perungudi",        "Temporarily Unavailable",True,  "2025-02-28",  0,  11, 0.94),
        ("Arun Mohan",        "A+",  "Ambattur",         "Available Today",        True,  "2024-11-11",  80, 4,  0.79),
    ])
]

# ── Hospitals ───────────────────────────────────────────────────────────────

HOSPITALS: list[dict] = [
    {"id": "H001", "name": "Apollo Hospitals",         "city": "Chennai",    "verified": True,  "beds": 1200, "distance_km": 2.1},
    {"id": "H002", "name": "Fortis Malar Hospital",    "city": "Chennai",    "verified": True,  "beds": 450,  "distance_km": 4.3},
    {"id": "H003", "name": "MIOT International",       "city": "Chennai",    "verified": True,  "beds": 1000, "distance_km": 7.8},
    {"id": "H004", "name": "Sri Ramachandra Hospital", "city": "Chennai",    "verified": True,  "beds": 800,  "distance_km": 11.2},
    {"id": "H005", "name": "AIIMS Madurai",            "city": "Madurai",    "verified": True,  "beds": 960,  "distance_km": 462.0},
    {"id": "H006", "name": "Vijaya Hospital",          "city": "Chennai",    "verified": False, "beds": 300,  "distance_km": 5.6},
    {"id": "H007", "name": "Kauvery Hospital",         "city": "Trichy",     "verified": True,  "beds": 700,  "distance_km": 330.0},
]

# ── Blood Banks ─────────────────────────────────────────────────────────────

BLOOD_BANKS: list[dict] = [
    {"id": "BB001", "name": "Indian Red Cross Blood Bank",     "city": "Chennai",  "verified": True,  "distance_km": 3.2},
    {"id": "BB002", "name": "Apollo Blood Bank",               "city": "Chennai",  "verified": True,  "distance_km": 2.1},
    {"id": "BB003", "name": "Rotary TTK Blood Bank",           "city": "Chennai",  "verified": True,  "distance_km": 5.7},
    {"id": "BB004", "name": "Life Line Blood Bank",            "city": "Chennai",  "verified": True,  "distance_km": 8.3},
    {"id": "BB005", "name": "Government Blood Bank Kilpauk",   "city": "Chennai",  "verified": True,  "distance_km": 6.1},
    {"id": "BB006", "name": "Sankara Blood Bank",              "city": "Chennai",  "verified": False, "distance_km": 9.4},
    {"id": "BB007", "name": "Fortis Blood Bank",               "city": "Chennai",  "verified": True,  "distance_km": 4.3},
]

# ── Blood Inventory ──────────────────────────────────────────────────────────

def _inv_row(bg: str, rbc: int, plt: int, ffp: int, cryo: int, wb: int,
             rbc_exp: int = 0, plt_exp: int = 0) -> dict:
    return {
        "blood_group": bg, "RBC": rbc, "Platelets": plt, "FFP": ffp,
        "Cryoprecipitate": cryo, "Whole Blood": wb,
        "rbc_expiring": rbc_exp, "plt_expiring": plt_exp,
    }

INVENTORY: list[dict] = [
    _inv_row("O+",  142, 28, 41, 12, 8,  4, 3),
    _inv_row("O−",  18,  4,  7,  3,  2,  2, 1),
    _inv_row("A+",  96,  21, 38, 9,  5,  1, 0),
    _inv_row("A−",  14,  3,  6,  2,  1,  1, 0),
    _inv_row("B+",  87,  19, 29, 7,  4,  0, 2),
    _inv_row("B−",  9,   2,  4,  1,  0,  1, 0),
    _inv_row("AB+", 31,  8,  15, 4,  2,  0, 1),
    _inv_row("AB−", 6,   1,  3,  1,  0,  2, 0),
]

INVENTORY_THRESHOLDS = {"RBC": 20, "Platelets": 5, "FFP": 8, "Cryoprecipitate": 3, "Whole Blood": 3}

def inventory_status(val: int, threshold: int) -> str:
    if val == 0:       return "CRITICAL"
    if val < threshold: return "LOW STOCK"
    return "AVAILABLE"

# ── Blood Requests ───────────────────────────────────────────────────────────

REQUESTS: list[dict] = [
    {"id": "BL-1042", "blood_group": "O−", "component": "RBC",        "units": 4, "urgency": "Critical",
     "hospital": "Apollo Hospitals",      "status": "Searching",          "verification": "Hospital Verified",
     "created": "2025-07-10 08:14",       "patient_age": 42,              "notes": "Post-operative"},
    {"id": "BL-1043", "blood_group": "AB+","component": "FFP",         "units": 2, "urgency": "Urgent",
     "hospital": "Fortis Malar Hospital", "status": "Partially Fulfilled","verification": "Hospital Verified",
     "created": "2025-07-10 09:32",       "patient_age": 67,              "notes": "Cardiac surgery"},
    {"id": "BL-1044", "blood_group": "B+", "component": "Platelets",   "units": 6, "urgency": "Critical",
     "hospital": "MIOT International",    "status": "Donor Contacted",    "verification": "Blood Bank Verified",
     "created": "2025-07-10 10:05",       "patient_age": 28,              "notes": "Dengue — thrombocytopenia"},
    {"id": "BL-1045", "blood_group": "A+", "component": "RBC",         "units": 3, "urgency": "Routine",
     "hospital": "Apollo Hospitals",      "status": "Fulfilled",          "verification": "Hospital Verified",
     "created": "2025-07-09 14:22",       "patient_age": 55,              "notes": "Elective surgery"},
    {"id": "BL-1046", "blood_group": "O+", "component": "Whole Blood",  "units": 2, "urgency": "Urgent",
     "hospital": "Sri Ramachandra Hospital","status": "Pending",          "verification": "Pending Verification",
     "created": "2025-07-10 11:40",       "patient_age": 19,              "notes": "Trauma"},
    {"id": "BL-1047", "blood_group": "O−", "component": "RBC",         "units": 5, "urgency": "Critical",
     "hospital": "Apollo Hospitals",      "status": "Searching",          "verification": "Hospital Verified",
     "created": "2025-07-10 12:10",       "patient_age": 35,              "notes": "Accident"},
    {"id": "BL-1048", "blood_group": "A−", "component": "Platelets",   "units": 3, "urgency": "Urgent",
     "hospital": "Kauvery Hospital",      "status": "Donor Contacted",    "verification": "Hospital Verified",
     "created": "2025-07-10 12:55",       "patient_age": 61,              "notes": "Chemotherapy support"},
    {"id": "BL-1049", "blood_group": "AB−","component": "FFP",         "units": 2, "urgency": "Critical",
     "hospital": "MIOT International",    "status": "Escalated",          "verification": "Blood Bank Verified",
     "created": "2025-07-10 13:20",       "patient_age": 74,              "notes": "Liver failure"},
]

# ── Platform Statistics ──────────────────────────────────────────────────────

PLATFORM_STATS = {
    "active_donors":      8_742,
    "verified_blood_banks": 284,
    "partner_hospitals":  1_136,
    "requests_fulfilled": 52_480,
    "active_emergencies":     8,
    "pending_requests":      23,
    "avg_response_min":    18.4,
    "shortage_alerts":        3,
}

# ── Demand Forecasting ────────────────────────────────────────────────────────

DEMAND_FORECAST: list[dict] = [
    {"blood_group": "O+",  "component": "RBC",        "current": 42, "forecast": 57, "risk": "Elevated",    "confidence": 0.84},
    {"blood_group": "O−",  "component": "RBC",        "current": 18, "forecast": 26, "risk": "High",        "confidence": 0.79},
    {"blood_group": "A+",  "component": "RBC",        "current": 31, "forecast": 38, "risk": "Moderate",    "confidence": 0.88},
    {"blood_group": "B+",  "component": "Platelets",  "current": 14, "forecast": 19, "risk": "Moderate",    "confidence": 0.76},
    {"blood_group": "O+",  "component": "Platelets",  "current": 22, "forecast": 31, "risk": "Elevated",    "confidence": 0.82},
    {"blood_group": "AB−", "component": "FFP",        "current": 3,  "forecast": 5,  "risk": "High",        "confidence": 0.71},
    {"blood_group": "A−",  "component": "Platelets",  "current": 7,  "forecast": 8,  "risk": "Low",         "confidence": 0.90},
    {"blood_group": "B−",  "component": "RBC",        "current": 5,  "forecast": 9,  "risk": "Elevated",    "confidence": 0.77},
]

# ── Expiry Risk ───────────────────────────────────────────────────────────────

EXPIRY_RISK: list[dict] = [
    {"blood_group": "O+",  "component": "RBC",       "units": 4,  "expiry_days": 2, "risk_level": "High"},
    {"blood_group": "O−",  "component": "RBC",       "units": 2,  "expiry_days": 1, "risk_level": "High"},
    {"blood_group": "O+",  "component": "Platelets", "units": 3,  "expiry_days": 1, "risk_level": "High"},
    {"blood_group": "A+",  "component": "RBC",       "units": 1,  "expiry_days": 3, "risk_level": "Attention"},
    {"blood_group": "B+",  "component": "Platelets", "units": 2,  "expiry_days": 2, "risk_level": "Attention"},
    {"blood_group": "AB+", "component": "Platelets", "units": 1,  "expiry_days": 2, "risk_level": "Attention"},
    {"blood_group": "AB−", "component": "RBC",       "units": 2,  "expiry_days": 4, "risk_level": "Low"},
    {"blood_group": "A−",  "component": "FFP",       "units": 1,  "expiry_days": 5, "risk_level": "Low"},
]

# ── Historical time series (last 12 months) ───────────────────────────────────

def monthly_series(base: int, trend: float = 1.0, noise: float = 0.08) -> list[int]:
    rng = random.Random(base)
    return [
        max(0, int(base * (trend ** m) * (1 + rng.uniform(-noise, noise))))
        for m in range(12)
    ]

MONTHS = ["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]

DONOR_GROWTH      = monthly_series(620,  trend=1.04)
REQUEST_TREND     = monthly_series(410,  trend=1.03)
FULFILMENT_TREND  = monthly_series(385,  trend=1.03, noise=0.06)
INVENTORY_TREND   = {
    "O+":  monthly_series(135, trend=0.99),
    "O−":  monthly_series(22,  trend=0.97),
    "A+":  monthly_series(100, trend=1.01),
    "B+":  monthly_series(90,  trend=1.0),
}

# ── Audit Log ─────────────────────────────────────────────────────────────────

AUDIT_LOG: list[dict] = [
    {"timestamp": "2025-07-10 13:45", "actor": "Hospital:Apollo",          "event": "REQUEST_CREATED",   "entity": "BL-1047", "detail": "Critical O− RBC — 5 units"},
    {"timestamp": "2025-07-10 13:46", "actor": "System",                   "event": "VERIFICATION_SENT",  "entity": "BL-1047", "detail": "Awaiting hospital verification"},
    {"timestamp": "2025-07-10 13:47", "actor": "Hospital:Apollo",          "event": "REQUEST_VERIFIED",   "entity": "BL-1047", "detail": "Verified by Dr. R. Anand"},
    {"timestamp": "2025-07-10 13:48", "actor": "Engine",                   "event": "INVENTORY_SEARCHED", "entity": "BL-1047", "detail": "BB001: 1u, BB003: 2u found"},
    {"timestamp": "2025-07-10 13:49", "actor": "Engine",                   "event": "DONOR_MATCHED",      "entity": "BL-1047", "detail": "8 donors scored; top 3 notified"},
    {"timestamp": "2025-07-10 13:52", "actor": "Donor:D1002",              "event": "DONOR_ACCEPTED",     "entity": "BL-1047", "detail": "Karthik Rajan accepted"},
    {"timestamp": "2025-07-10 13:58", "actor": "Donor:D1008",              "event": "DONOR_ACCEPTED",     "entity": "BL-1047", "detail": "Deepak Menon accepted"},
    {"timestamp": "2025-07-10 14:10", "actor": "BloodBank:BB001",          "event": "INVENTORY_RESERVED", "entity": "BL-1047", "detail": "1 unit reserved at Indian Red Cross"},
    {"timestamp": "2025-07-10 08:14", "actor": "Hospital:MIOT",            "event": "REQUEST_CREATED",    "entity": "BL-1042", "detail": "Critical O− RBC — 4 units"},
    {"timestamp": "2025-07-10 08:16", "actor": "System",                   "event": "ESCALATION_STAGE2",  "entity": "BL-1042", "detail": "Donor pool expanded — radius 15 km"},
    {"timestamp": "2025-07-10 09:32", "actor": "Hospital:Fortis",          "event": "REQUEST_CREATED",    "entity": "BL-1043", "detail": "Urgent AB+ FFP — 2 units"},
    {"timestamp": "2025-07-09 14:22", "actor": "Hospital:Apollo",          "event": "REQUEST_FULFILLED",  "entity": "BL-1045", "detail": "3 units A+ RBC fulfilled"},
    {"timestamp": "2025-07-10 12:05", "actor": "Admin:Janaani",            "event": "USER_VERIFIED",      "entity": "D1000",   "detail": "Donor Arjun Sharma verified"},
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_donors_df() -> pd.DataFrame:
    return pd.DataFrame(DONORS)

def get_inventory_df() -> pd.DataFrame:
    return pd.DataFrame(INVENTORY)

def get_requests_df() -> pd.DataFrame:
    return pd.DataFrame(REQUESTS)

def get_forecast_df() -> pd.DataFrame:
    return pd.DataFrame(DEMAND_FORECAST)

def get_expiry_df() -> pd.DataFrame:
    return pd.DataFrame(EXPIRY_RISK)

def score_label(s: int) -> str:
    if s >= 90: return "Excellent"
    if s >= 75: return "Good"
    if s >= 50: return "Fair"
    return "Unavailable"
