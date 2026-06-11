import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import time
import numpy as np
from datetime import datetime, timedelta
import math
import json

# ============================================================
# PAGE CONFIG & GLOBAL CSS
# ============================================================
st.set_page_config(
    page_title="Baku MetroTwin Pro v5.0",
    layout="wide",
    page_icon="🚇",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #080b10; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080b10 0%, #0d1117 100%);
        border-right: 1px solid #1c2333;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        border: 1px solid #21262d;
        padding: 14px 18px;
        border-radius: 10px;
        color: white;
        transition: all 0.25s ease;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #388bfd;
        box-shadow: 0 0 12px rgba(56,139,253,0.15);
        transform: translateY(-1px);
    }
    div[data-testid="stMetric"] label { color: #8b949e !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 0.08em; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #e6edf3 !important; font-family: 'JetBrains Mono', monospace; }

    .ai-box {
        background: linear-gradient(135deg, #0d1117 0%, #111820 100%);
        border-left: 5px solid #388bfd;
        padding: 20px 24px;
        border-radius: 10px;
        margin: 10px 0;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .rec-item {
        background: rgba(13,17,23,0.9);
        border-left: 3px solid #388bfd;
        border-radius: 6px;
        padding: 10px 14px;
        margin: 6px 0;
        font-size: 13.5px;
        color: #cdd9e5;
        line-height: 1.5;
        transition: background 0.2s;
    }
    .rec-item:hover { background: #161b22; }

    .kpi-critical { border-color: #f85149 !important; box-shadow: 0 0 15px rgba(248,81,73,0.2) !important; }
    .kpi-warning  { border-color: #d29922 !important; box-shadow: 0 0 15px rgba(210,153,34,0.2) !important; }
    .kpi-ok       { border-color: #3fb950 !important; }

    .status-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .badge-red   { background: rgba(248,81,73,0.15); color: #f85149; border: 1px solid #f85149; }
    .badge-yellow{ background: rgba(210,153,34,0.15); color: #d29922; border: 1px solid #d29922; }
    .badge-green { background: rgba(63,185,80,0.15);  color: #3fb950; border: 1px solid #3fb950; }
    .badge-blue  { background: rgba(56,139,253,0.15); color: #388bfd; border: 1px solid #388bfd; }
    .badge-purple{ background: rgba(188,140,255,0.15);color: #bc8cff; border: 1px solid #bc8cff; }

    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 2.8em;
        background: linear-gradient(135deg, #238636, #2ea043);
        color: white;
        font-weight: 600;
        font-size: 13px;
        border: 1px solid #3fb950;
        letter-spacing: 0.02em;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2ea043, #3fb950);
        box-shadow: 0 0 10px rgba(63,185,80,0.3);
        transform: translateY(-1px);
    }

    .incident-row {
        background: #0d1117;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 6px 0;
        border: 1px solid #21262d;
    }
    .sensor-card {
        background: #0d1117;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        margin: 4px;
    }
    .timeline-step {
        border-left: 2px solid #21262d;
        padding: 8px 16px;
        margin: 4px 0;
        position: relative;
    }
    .timeline-step::before {
        content: '';
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #388bfd;
        position: absolute;
        left: -5px;
        top: 12px;
    }
    div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; border: 1px solid #21262d; }
    .stSelectbox label, .stSlider label, .stNumberInput label { color: #8b949e !important; font-size: 12px !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; background: #0d1117; border-radius: 10px; padding: 4px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 7px;
        color: #8b949e;
        font-size: 13px;
        font-weight: 500;
        padding: 6px 14px;
    }
    .stTabs [aria-selected="true"] {
        background: #161b22 !important;
        color: #e6edf3 !important;
    }
    .section-header {
        font-size: 14px;
        font-weight: 600;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 16px 0 8px 0;
        padding-bottom: 6px;
        border-bottom: 1px solid #21262d;
    }
    .live-pulse {
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: #3fb950;
        animation: pulse 1.5s infinite;
        margin-right: 6px;
    }
    @keyframes pulse {
        0%   { box-shadow: 0 0 0 0 rgba(63,185,80,0.6); }
        70%  { box-shadow: 0 0 0 8px rgba(63,185,80,0); }
        100% { box-shadow: 0 0 0 0 rgba(63,185,80,0); }
    }
    .maintenance-card {
        background: #0d1117;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 14px;
        margin: 6px 0;
    }
    .progress-bar-container {
        background: #21262d;
        border-radius: 4px;
        height: 6px;
        overflow: hidden;
        margin: 4px 0;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# STATION DATABASE  (23 stations + detailed metadata)
# ============================================================
metro_stations = {
    "İçərişəhər":         {"lat": 40.3661, "lon": 49.8311, "area": 850,  "line": "Qırmızı",   "platform_len": 102, "escalators": 4,  "exits": 2, "opened": 1967, "daily_avg": 18000, "type": "Underground", "depth_m": 14, "architect": "Ye. Renne", "cctv_count": 24, "wifi": True},
    "Sahil":              {"lat": 40.3705, "lon": 49.8464, "area": 800,  "line": "Qırmızı",   "platform_len": 102, "escalators": 4,  "exits": 3, "opened": 1967, "daily_avg": 22000, "type": "Underground", "depth_m": 18, "architect": "Renne&Koşkarev", "cctv_count": 28, "wifi": True},
    "28 May":             {"lat": 40.3798, "lon": 49.8486, "area": 1300, "line": "Q/Y",        "platform_len": 102, "escalators": 8,  "exits": 5, "opened": 1967, "daily_avg": 55000, "type": "Underground", "depth_m": 22, "architect": "A. Salamzadə", "cctv_count": 56, "wifi": True, "is_transfer": True},
    "Gənclik":            {"lat": 40.4001, "lon": 49.8512, "area": 1150, "line": "Qırmızı",   "platform_len": 102, "escalators": 6,  "exits": 4, "opened": 1967, "daily_avg": 35000, "type": "Underground", "depth_m": 20, "architect": "Baku Metro Dept", "cctv_count": 34, "wifi": True},
    "Nərimanov":          {"lat": 40.4161, "lon": 49.8712, "area": 1100, "line": "Qırmızı",   "platform_len": 102, "escalators": 6,  "exits": 3, "opened": 1967, "daily_avg": 28000, "type": "Underground", "depth_m": 19, "architect": "Baku Metro Dept", "cctv_count": 30, "wifi": True},
    "Ulduz":              {"lat": 40.4151, "lon": 49.8928, "area": 900,  "line": "Qırmızı",   "platform_len": 102, "escalators": 4,  "exits": 2, "opened": 1967, "daily_avg": 19000, "type": "Underground", "depth_m": 16, "architect": "Baku Metro Dept", "cctv_count": 22, "wifi": False},
    "Koroğlu":            {"lat": 40.4203, "lon": 49.9180, "area": 1600, "line": "Qırmızı",   "platform_len": 102, "escalators": 6,  "exits": 4, "opened": 1979, "daily_avg": 32000, "type": "Underground", "depth_m": 25, "architect": "Baku Metro Dept", "cctv_count": 38, "wifi": True},
    "Qara Qarayev":       {"lat": 40.4173, "lon": 49.9351, "area": 950,  "line": "Qırmızı",   "platform_len": 102, "escalators": 4,  "exits": 3, "opened": 1979, "daily_avg": 20000, "type": "Underground", "depth_m": 17, "architect": "Baku Metro Dept", "cctv_count": 24, "wifi": False},
    "Neftçilər":          {"lat": 40.4111, "lon": 49.9430, "area": 1000, "line": "Qırmızı",   "platform_len": 102, "escalators": 4,  "exits": 3, "opened": 1985, "daily_avg": 21000, "type": "Underground", "depth_m": 18, "architect": "Baku Metro Dept", "cctv_count": 26, "wifi": False},
    "Xalqlar Dostluğu":   {"lat": 40.3978, "lon": 49.9525, "area": 1000, "line": "Qırmızı",   "platform_len": 102, "escalators": 4,  "exits": 2, "opened": 1985, "daily_avg": 18000, "type": "Underground", "depth_m": 16, "architect": "Baku Metro Dept", "cctv_count": 22, "wifi": False},
    "Əhmədli":            {"lat": 40.3855, "lon": 49.9542, "area": 1000, "line": "Qırmızı",   "platform_len": 102, "escalators": 4,  "exits": 3, "opened": 1985, "daily_avg": 22000, "type": "Underground", "depth_m": 17, "architect": "Baku Metro Dept", "cctv_count": 24, "wifi": False},
    "Həzi Aslanov":       {"lat": 40.3732, "lon": 49.9538, "area": 1100, "line": "Qırmızı",   "platform_len": 102, "escalators": 4,  "exits": 2, "opened": 1985, "daily_avg": 16000, "type": "Underground", "depth_m": 15, "architect": "Baku Metro Dept", "cctv_count": 20, "wifi": False},
    "Xətai":              {"lat": 40.3835, "lon": 49.8732, "area": 850,  "line": "Yaşıl",     "platform_len": 102, "escalators": 4,  "exits": 3, "opened": 1967, "daily_avg": 24000, "type": "Underground", "depth_m": 16, "architect": "Baku Metro Dept", "cctv_count": 26, "wifi": True},
    "Nizami":             {"lat": 40.3789, "lon": 49.8301, "area": 900,  "line": "Yaşıl",     "platform_len": 102, "escalators": 6,  "exits": 4, "opened": 1967, "daily_avg": 38000, "type": "Underground", "depth_m": 20, "architect": "Baku Metro Dept", "cctv_count": 40, "wifi": True},
    "Elmlər Akademiyası": {"lat": 40.3748, "lon": 49.8154, "area": 950,  "line": "Yaşıl",     "platform_len": 102, "escalators": 4,  "exits": 3, "opened": 1967, "daily_avg": 25000, "type": "Underground", "depth_m": 19, "architect": "Baku Metro Dept", "cctv_count": 28, "wifi": True},
    "İnşaatçılar":        {"lat": 40.3892, "lon": 49.8028, "area": 950,  "line": "Yaşıl",     "platform_len": 102, "escalators": 4,  "exits": 3, "opened": 1985, "daily_avg": 20000, "type": "Underground", "depth_m": 17, "architect": "Baku Metro Dept", "cctv_count": 24, "wifi": False},
    "20 Yanvar":          {"lat": 40.4031, "lon": 49.8068, "area": 1100, "line": "Yaşıl",     "platform_len": 102, "escalators": 4,  "exits": 3, "opened": 1993, "daily_avg": 18000, "type": "Underground", "depth_m": 21, "architect": "Baku Metro Dept", "cctv_count": 26, "wifi": True},
    "Memar Əcəmi":        {"lat": 40.4111, "lon": 49.8115, "area": 1200, "line": "Y/B",        "platform_len": 102, "escalators": 8,  "exits": 5, "opened": 1993, "daily_avg": 42000, "type": "Underground", "depth_m": 23, "architect": "Baku Metro Dept", "cctv_count": 50, "wifi": True, "is_transfer": True},
    "Nəsimi":             {"lat": 40.4272, "lon": 49.8153, "area": 900,  "line": "Yaşıl",     "platform_len": 102, "escalators": 4,  "exits": 2, "opened": 2002, "daily_avg": 17000, "type": "Underground", "depth_m": 18, "architect": "AZMETRO", "cctv_count": 22, "wifi": True},
    "Azadlıq Prospekti":  {"lat": 40.4328, "lon": 49.8319, "area": 1100, "line": "Yaşıl",     "platform_len": 102, "escalators": 4,  "exits": 3, "opened": 2002, "daily_avg": 24000, "type": "Underground", "depth_m": 20, "architect": "AZMETRO", "cctv_count": 28, "wifi": True},
    "Dərnəgül":           {"lat": 40.4252, "lon": 49.8519, "area": 1000, "line": "Yaşıl",     "platform_len": 102, "escalators": 4,  "exits": 2, "opened": 2002, "daily_avg": 19000, "type": "Underground", "depth_m": 17, "architect": "AZMETRO", "cctv_count": 22, "wifi": True},
    "Avtovağzal":         {"lat": 40.4201, "lon": 49.7941, "area": 1400, "line": "Bənövşəyi", "platform_len": 102, "escalators": 6,  "exits": 4, "opened": 2016, "daily_avg": 28000, "type": "Underground", "depth_m": 26, "architect": "AZMETRO+MHD", "cctv_count": 44, "wifi": True},
    "8 Noyabr":           {"lat": 40.3989, "lon": 49.8213, "area": 1300, "line": "Bənövşəyi", "platform_len": 102, "escalators": 6,  "exits": 4, "opened": 2016, "daily_avg": 30000, "type": "Underground", "depth_m": 24, "architect": "AZMETRO+MHD", "cctv_count": 46, "wifi": True},
}

station_neighbors = {
    "İçərişəhər": ["Sahil"],
    "Sahil": ["İçərişəhər", "28 May"],
    "28 May": ["Sahil", "Gənclik", "Xətai"],
    "Gənclik": ["28 May", "Nərimanov"],
    "Nərimanov": ["Gənclik", "Ulduz"],
    "Ulduz": ["Nərimanov", "Koroğlu"],
    "Koroğlu": ["Ulduz", "Qara Qarayev"],
    "Qara Qarayev": ["Koroğlu", "Neftçilər"],
    "Neftçilər": ["Qara Qarayev", "Xalqlar Dostluğu"],
    "Xalqlar Dostluğu": ["Neftçilər", "Əhmədli"],
    "Əhmədli": ["Xalqlar Dostluğu", "Həzi Aslanov"],
    "Həzi Aslanov": ["Əhmədli"],
    "Xətai": ["28 May", "Nizami"],
    "Nizami": ["Xətai", "Elmlər Akademiyası"],
    "Elmlər Akademiyası": ["Nizami", "İnşaatçılar"],
    "İnşaatçılar": ["Elmlər Akademiyası", "20 Yanvar"],
    "20 Yanvar": ["İnşaatçılar", "Memar Əcəmi"],
    "Memar Əcəmi": ["20 Yanvar", "Nəsimi", "8 Noyabr"],
    "Nəsimi": ["Memar Əcəmi", "Azadlıq Prospekti"],
    "Azadlıq Prospekti": ["Nəsimi", "Dərnəgül"],
    "Dərnəgül": ["Azadlıq Prospekti"],
    "Avtovağzal": ["8 Noyabr"],
    "8 Noyabr": ["Avtovağzal", "Memar Əcəmi"],
}

# ============================================================
# MAINTENANCE & EQUIPMENT DATABASE
# ============================================================
def get_maintenance_schedule(station_data):
    """Generate realistic maintenance schedule based on station age and usage."""
    age = 2025 - station_data["opened"]
    usage_factor = station_data["daily_avg"] / 30000
    base_score = max(20, 100 - (age * 0.8) - (usage_factor * 15))
    items = [
        {"Avadanlıq": "Eskalator sistemi", "Son Baxış": f"{random.randint(1,90)} gün əvvəl",
         "Növbəti Baxış": f"{random.randint(10,120)} gün sonra",
         "Vəziyyət": random.choices(["Əla ✅","Yaxşı 🟢","Qənaətbəxş 🟡","Diqqət 🟠","Kritik 🔴"],
                                    weights=[30,35,20,10,5])[0],
         "Qalıq Ömür %": max(15, int(base_score + random.randint(-15,15)))},
        {"Avadanlıq": "Turniket sistemi", "Son Baxış": f"{random.randint(1,60)} gün əvvəl",
         "Növbəti Baxış": f"{random.randint(7,60)} gün sonra",
         "Vəziyyət": random.choices(["Əla ✅","Yaxşı 🟢","Qənaətbəxş 🟡","Diqqət 🟠","Kritik 🔴"],
                                    weights=[25,40,20,10,5])[0],
         "Qalıq Ömür %": max(20, int(base_score + random.randint(-10,20)))},
        {"Avadanlıq": f"CCTV Sistemi ({station_data['cctv_count']} kamera)", "Son Baxış": f"{random.randint(1,45)} gün əvvəl",
         "Növbəti Baxış": f"{random.randint(14,90)} gün sonra",
         "Vəziyyət": random.choices(["Əla ✅","Yaxşı 🟢","Qənaətbəxş 🟡","Diqqət 🟠"],
                                    weights=[40,35,15,10])[0],
         "Qalıq Ömür %": max(30, int(base_score + random.randint(-5,25)))},
        {"Avadanlıq": "Ventilyasiya sistemi", "Son Baxış": f"{random.randint(10,120)} gün əvvəl",
         "Növbəti Baxış": f"{random.randint(30,180)} gün sonra",
         "Vəziyyət": random.choices(["Əla ✅","Yaxşı 🟢","Qənaətbəxş 🟡","Diqqət 🟠","Kritik 🔴"],
                                    weights=[20,30,30,15,5])[0],
         "Qalıq Ömür %": max(25, int(base_score + random.randint(-20,10)))},
        {"Avadanlıq": "Yanğınsöndürmə sistemi", "Son Baxış": f"{random.randint(5,180)} gün əvvəl",
         "Növbəti Baxış": f"{random.randint(7,365)} gün sonra",
         "Vəziyyət": random.choices(["Əla ✅","Yaxşı 🟢","Qənaətbəxş 🟡"],
                                    weights=[50,35,15])[0],
         "Qalıq Ömür %": max(40, int(base_score + random.randint(0,30)))},
        {"Avadanlıq": "Elektrik paylama paneli", "Son Baxış": f"{random.randint(1,30)} gün əvvəl",
         "Növbəti Baxış": f"{random.randint(30,90)} gün sonra",
         "Vəziyyət": random.choices(["Əla ✅","Yaxşı 🟢","Qənaətbəxş 🟡","Diqqət 🟠"],
                                    weights=[35,40,15,10])[0],
         "Qalıq Ömür %": max(35, int(base_score + random.randint(-5,20)))},
        {"Avadanlıq": "Sərnişin informasiya ekranları", "Son Baxış": f"{random.randint(2,60)} gün əvvəl",
         "Növbəti Baxış": f"{random.randint(14,120)} gün sonra",
         "Vəziyyət": random.choices(["Əla ✅","Yaxşı 🟢","Qənaətbəxş 🟡","Diqqət 🟠"],
                                    weights=[45,35,12,8])[0],
         "Qalıq Ömür %": max(40, int(base_score + random.randint(0,25)))},
        {"Avadanlıq": "Su drenaj sistemi", "Son Baxış": f"{random.randint(30,180)} gün əvvəl",
         "Növbəti Baxış": f"{random.randint(60,365)} gün sonra",
         "Vəziyyət": random.choices(["Əla ✅","Yaxşı 🟢","Qənaətbəxş 🟡","Diqqət 🟠","Kritik 🔴"],
                                    weights=[25,30,25,15,5])[0],
         "Qalıq Ömür %": max(20, int(base_score + random.randint(-25,5)))},
    ]
    return items

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def get_los(passengers, area):
    if passengers <= 0:
        return ("A", "#3fb950", "Boş / Azad hərəkət")
    density = area / passengers
    if density >= 1.2:    return ("A", "#3fb950",  "Azad hərəkət — Tam rahat")
    elif density >= 0.9:  return ("B", "#56d364",  "Normal axın — Rahat")
    elif density >= 0.6:  return ("C", "#d29922",  "Məhdud hərəkət — Normal")
    elif density >= 0.35: return ("D", "#db6d28",  "Ciddi sıxlıq — Narahat")
    elif density >= 0.2:  return ("E", "#f85149",  "Kritik hədd — Təhlükəli")
    else:                 return ("F", "#bc8cff",  "ƏZAB SIXLIĞI — FÖVQƏLADƏ")

def apply_modifiers(base, weather, event, tod, special_mul=1.0):
    w = {"Aydın ☀️": 1.0, "Yağışlı 🌧️": 1.18, "Qarlı ❄️": 1.32,
         "İsti 🌡️ (+35°C)": 1.14, "Küləkli 💨": 1.12, "Duman 🌫️": 1.09,
         "Tufan ⛈️": 1.25, "İsti yay 🌞": 1.08}
    e = {"Hadisə yoxdur": 1.0,
         "Futbol oyunu ⚽ (Tofiq Bəhramov)": 1.55, "Konsert 🎵 (Crystal Hall)": 1.40,
         "Dövlət tədiri 🏛️": 1.28, "Bayram 🎉 (Novruz/Müstəqillik)": 1.38,
         "İş günü pik saatı ⏰": 1.25, "Həftəsonu 🛍️": 0.82,
         "Formula 1 🏎️ (Bakı küçə pisti)": 1.70,
         "UEFA Oyunu ⚽🏆": 1.80, "Beynəlxalq konfrans 🎤": 1.22,
         "Bazar günü axşamı 🌇": 1.10, "Məktəb başlangıcı 📚": 1.35}
    t = {"Gecə (00–05)": 0.08, "Erkən səhər (05–07)": 0.22,
         "Səhər pik (07–09) 🔴": 1.92, "Gündüz (09–12)": 0.95,
         "Nahar vaxtı (12–14)": 1.12, "Öğlə (14–17)": 0.85,
         "Axşam pik (17–20) 🔴": 1.82, "Axşam (20–22)": 0.60,
         "Gecə yarısı (22–00)": 0.30}
    return int(base * w.get(weather, 1.0) * e.get(event, 1.0) * t.get(tod, 1.0) * special_mul)

def throughput_capacity(interval, cap, track_mode="Hər iki istiqamət"):
    multiplier = {"Hər iki istiqamət": 1.0, "Yalnız giriş": 0.5, "Yalnız çıxış": 0.5}
    return int((60 / interval) * cap * 0.87 * multiplier.get(track_mode, 1.0))

def energy_kw(interval, load, escalators, escalator_mode, lighting_mode, hvac_mode):
    trains_ph = 60 / interval
    base_train = trains_ph * 14
    esc_power  = escalators * (2.2 if escalator_mode == "Normal" else 2.8 if "yukarı" in escalator_mode or "aşağı" in escalator_mode else 0.3)
    lighting   = {"Tam": 18, "Yarı": 10, "Minimal": 4, "Fövqəladə": 2}.get(lighting_mode, 12)
    hvac       = {"Yaz/Payız": 22, "Yay tam": 45, "Qış isitmə": 38, "Minimal": 8}.get(hvac_mode, 22)
    load_power = max(5, load / 75)
    return round(base_train + esc_power + lighting + hvac + load_power, 1)

def predict_curve(load, interval, cap, inflow, steps=12, scenario_mul=1.0):
    out_per_step = (5 / interval) * cap * 0.85
    curve = [load]
    trend = random.uniform(-0.02, 0.04)
    for i in range(steps):
        seasonal = math.sin(i * 0.5) * 0.08
        noise    = random.uniform(-0.12, 0.12)
        new_inflow = max(0, inflow * (1 + trend + seasonal + noise) * scenario_mul)
        new = max(0, curve[-1] + new_inflow - out_per_step)
        curve.append(int(new))
    return curve

def congestion_color(pct):
    if pct < 40:    return "#3fb950"
    elif pct < 60:  return "#56d364"
    elif pct < 75:  return "#d29922"
    elif pct < 90:  return "#db6d28"
    elif pct < 100: return "#f85149"
    else:           return "#bc8cff"

def sensor_sim(area, load, station_data, ambient_temp=25):
    esc_load = random.randint(45, min(99, int(50 + load/30)))
    co2      = random.randint(400, min(2500, int(600 + load * 0.8)))
    noise_db = random.randint(55, min(95, int(60 + load * 0.012)))
    return {
        "Giriş A":          max(0, int(load * random.uniform(0.32, 0.42))),
        "Giriş B":          max(0, int(load * random.uniform(0.27, 0.37))),
        "Giriş C":          max(0, int(load * random.uniform(0.14, 0.24))),
        "Platform":         max(0, int(load * random.uniform(0.88, 1.12))),
        "Çıxış":            -max(0, int(load * random.uniform(0.20, 0.35))),
        "Eskalator %":      esc_load,
        "Temp (°C)":        round(ambient_temp + random.uniform(-3, 5), 1),
        "Rütubət %":        random.randint(35, 75),
        "CO₂ (ppm)":        co2,
        "Səs-küy (dB)":     noise_db,
        "CCTV Aktiv":       f"{random.randint(station_data['cctv_count']-3, station_data['cctv_count'])}/{station_data['cctv_count']}",
        "WiFi İstifadəçi":  random.randint(20, 180) if station_data.get("wifi") else 0,
    }

def predict_dwell_time(load, platform_len, train_cap):
    """Predict train dwell time in seconds based on crowd conditions."""
    base_dwell = 25
    crowd_penalty = max(0, (load / train_cap) - 0.5) * 40
    return int(base_dwell + crowd_penalty + random.randint(-3, 5))

def calc_evacuation_time(passengers, exits, escalators, staff):
    """Calculate evacuation time in minutes."""
    flow_per_exit = 120  # persons/minute
    flow_per_esc  = 80
    total_capacity = (exits * flow_per_exit) + (escalators * flow_per_esc)
    staff_factor   = min(1.3, 1 + staff * 0.02)
    return round(passengers / (total_capacity * staff_factor), 1)

def passenger_flow_model(entries_list, interval, train_cap, scenario_mul=1.0):
    """Advanced queuing model with accumulation."""
    load = 0
    results = []
    for entry in entries_list:
        out = (5 / interval) * train_cap * 0.85
        load = max(0, load + int(entry * scenario_mul) - out)
        results.append(int(load))
    return results

# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    "incident_log":   [],
    "live_history":   [],
    "live_tick":      0,
    "maintenance_data": {},
    "shift_log":      [],
    "energy_history": [],
    "manual_entries": [
        {"Saat": "07:00", "Giriş": 280, "Əl İlə Daxil": False},
        {"Saat": "07:30", "Giriş": 540, "Əl İlə Daxil": False},
        {"Saat": "08:00", "Giriş": 920, "Əl İlə Daxil": False},
        {"Saat": "08:30", "Giriş": 1050,"Əl İlə Daxil": False},
        {"Saat": "09:00", "Giriş": 760, "Əl İlə Daxil": False},
        {"Saat": "09:30", "Giriş": 480, "Əl İlə Daxil": False},
        {"Saat": "10:00", "Giriş": 330, "Əl İlə Daxil": False},
    ],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# SIDEBAR — ADVANCED CONFIGURATION
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
        <span style="font-size:28px">🚇</span>
        <div>
            <div style="color:#e6edf3;font-weight:700;font-size:15px">MetroTwin Pro</div>
            <div style="color:#388bfd;font-size:11px;font-weight:600">v5.0 · Digital Twin Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Station Selection ────────────────────────────────────
    st.markdown('<div class="section-header">🎯 Stansiya</div>', unsafe_allow_html=True)
    stansiya_adi = st.selectbox("Stansiya:", sorted(metro_stations.keys()), index=2, label_visibility="collapsed")
    st_data = metro_stations[stansiya_adi]

    LINE_COLORS = {"Qırmızı": "#f85149", "Yaşıl": "#3fb950", "Bənövşəyi": "#bc8cff",
                   "Q/Y": "#f85149", "Y/B": "#3fb950"}
    LINE_ICON   = {"Qırmızı": "🔴", "Yaşıl": "🟢", "Bənövşəyi": "🟣", "Q/Y": "🔴🟢", "Y/B": "🟢🟣"}
    line_icon   = LINE_ICON.get(st_data["line"], "⚪")
    is_transfer = st_data.get("is_transfer", False)

    line_color = LINE_COLORS.get(st_data["line"], "#8b949e")
    st.markdown(f"""
    <div style="background:#0d1117;border:1px solid #21262d;border-left:4px solid {line_color};border-radius:8px;padding:12px 14px;margin:6px 0">
        <div style="color:{line_color};font-weight:700;font-size:13px">{line_icon} {st_data['line']} Xətt {'| 🔀 Transfer' if is_transfer else ''}</div>
        <div style="color:#8b949e;font-size:12px;margin-top:6px">
            📅 {st_data['opened']} | 📏 {st_data['area']} m² | 🚪 {st_data['exits']} çıxış<br>
            📊 Gündəlik ort: <span style="color:#e6edf3;font-weight:600">{st_data['daily_avg']:,}</span> nəfər<br>
            🏗️ Dərinlik: {st_data['depth_m']} m | 📹 CCTV: {st_data['cctv_count']}<br>
            🌐 WiFi: {'✅ Var' if st_data.get('wifi') else '❌ Yoxdur'} | 🏛️ {st_data.get('architect','N/A')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Train & Operations ───────────────────────────────────
    st.markdown('<div class="section-header">🚃 Qatarlar & Cədvəl</div>', unsafe_allow_html=True)

    train_type = st.selectbox("Qatar Növü:", [
        "81-714 Ər (Köhnə, 1967)", "81-765 Ər (Modernizasiya)", "Stadler KISS (2022)",
        "CAF Urbos 3 (2024)", "Siemens Inspiro (2025)", "Bombardier Movia (Test)"
    ])
    TRAIN_CAP   = {"81-714 Ər (Köhnə, 1967)": 480, "81-765 Ər (Modernizasiya)": 550,
                   "Stadler KISS (2022)": 680, "CAF Urbos 3 (2024)": 740,
                   "Siemens Inspiro (2025)": 800, "Bombardier Movia (Test)": 760}
    TRAIN_SPEED = {"81-714 Ər (Köhnə, 1967)": 60, "81-765 Ər (Modernizasiya)": 70,
                   "Stadler KISS (2022)": 90, "CAF Urbos 3 (2024)": 90,
                   "Siemens Inspiro (2025)": 100, "Bombardier Movia (Test)": 95}
    TRAIN_AC    = {"81-714 Ər (Köhnə, 1967)": False, "81-765 Ər (Modernizasiya)": False,
                   "Stadler KISS (2022)": True, "CAF Urbos 3 (2024)": True,
                   "Siemens Inspiro (2025)": True, "Bombardier Movia (Test)": True}
    qatar_tutumu = TRAIN_CAP[train_type]
    qatar_sureeti = TRAIN_SPEED[train_type]
    qatar_kondisioner = TRAIN_AC[train_type]

    tc1, tc2, tc3 = st.columns(3)
    tc1.metric("Tutum", f"{qatar_tutumu}")
    tc2.metric("Sürət", f"{qatar_sureeti}km/h")
    tc3.metric("A/C", "✅" if qatar_kondisioner else "❌")

    interval = st.select_slider("⏱️ Qatar İntervalı:",
        options=[1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0],
        value=4.0, format_func=lambda x: f"{x} dəq")

    train_count_on_line = st.slider("🚃 Xəttdə Aktiv Qatar:", 4, 20, 10)
    platform_doors = st.selectbox("🚪 Platform Qapıları:", ["Açıq plaforma", "Yarı qapalı PSD", "Tam qapalı PSD"])

    active_tracks = st.radio("Aktiv İstiqamət:",
        ["Hər iki istiqamət", "Yalnız giriş", "Yalnız çıxış"], horizontal=True)

    trains_ph   = int(60 / interval)
    theory_cap  = throughput_capacity(interval, qatar_tutumu, active_tracks)
    st.caption(f"📊 Saatda **{trains_ph}** qatar | Nəzəri: **{theory_cap:,}** nəfər/saat")

    st.divider()

    # ── Environment ──────────────────────────────────────────
    st.markdown('<div class="section-header">🌍 Mühit & Şərait</div>', unsafe_allow_html=True)

    weather = st.selectbox("🌤️ Hava:", ["Aydın ☀️", "Yağışlı 🌧️", "Qarlı ❄️",
        "İsti 🌡️ (+35°C)", "Küləkli 💨", "Duman 🌫️", "Tufan ⛈️", "İsti yay 🌞"])
    ambient_temp = st.slider("🌡️ Xarici Temperatur (°C):", -5, 42, 22)
    humidity_out = st.slider("💧 Xarici Rütubət (%):", 20, 95, 55)

    event_nearby = st.selectbox("🎪 Yaxın Tədrir:", [
        "Hadisə yoxdur", "Futbol oyunu ⚽ (Tofiq Bəhramov)", "Konsert 🎵 (Crystal Hall)",
        "Dövlət tədiri 🏛️", "Bayram 🎉 (Novruz/Müstəqillik)", "İş günü pik saatı ⏰",
        "Həftəsonu 🛍️", "Formula 1 🏎️ (Bakı küçə pisti)", "UEFA Oyunu ⚽🏆",
        "Beynəlxalq konfrans 🎤", "Bazar günü axşamı 🌇", "Məktəb başlangıcı 📚"
    ])

    time_of_day = st.selectbox("🕐 Günün Vaxtı:", [
        "Gecə (00–05)", "Erkən səhər (05–07)", "Səhər pik (07–09) 🔴",
        "Gündüz (09–12)", "Nahar vaxtı (12–14)", "Öğlə (14–17)",
        "Axşam pik (17–20) 🔴", "Axşam (20–22)", "Gecə yarısı (22–00)"
    ])

    day_type = st.radio("📅 Gün Növü:", ["İş Günü", "Şənbə", "Bazar", "Bayram"], horizontal=True)
    DAY_MULTIPLIER = {"İş Günü": 1.0, "Şənbə": 0.88, "Bazar": 0.72, "Bayram": 1.25}
    day_mul = DAY_MULTIPLIER[day_type]

    st.divider()

    # ── Infrastructure ───────────────────────────────────────
    st.markdown('<div class="section-header">🔧 İnfrastruktur</div>', unsafe_allow_html=True)

    escalator_mode = st.selectbox("⬆️ Eskalator Rejimi:",
        ["Normal (ikisi giriş, ikisi çıxış)", "Hamısı yukarı (boşaltma)",
         "Hamısı aşağı (doluşma)", "Avari (manual)", "Tam dayandırılmış ⛔"])

    lighting_mode = st.selectbox("💡 İşıqlandırma:", ["Tam", "Yarı", "Minimal", "Fövqəladə"])
    hvac_mode     = st.selectbox("❄️ Kondisioner/Isıtma:",
        ["Yaz/Payız", "Yay tam", "Qış isitmə", "Minimal"])

    psd_status = st.selectbox("🚉 Platform Qapı Sistemi:", ["Normal", "Qapı sıradan çıxma", "Texniki baxış"])

    st.divider()

    # ── Safety & Staffing ────────────────────────────────────
    st.markdown('<div class="section-header">⚠️ Təhlükəsizlik & Personal</div>', unsafe_allow_html=True)

    safety_std = st.selectbox("Standart:", [
        "NFPA 130 — 0.5 m²/nəfər", "EN 13816 — 0.4 m²/nəfər",
        "Azərb. Norması — 0.6 m²/nəfər", "Yüksək Sıxlıq — 0.3 m²/nəfər",
        "Tokyo Standartı — 0.25 m²/nəfər"
    ])
    STD_MAP = {
        "NFPA 130 — 0.5 m²/nəfər": 0.5, "EN 13816 — 0.4 m²/nəfər": 0.4,
        "Azərb. Norması — 0.6 m²/nəfər": 0.6, "Yüksək Sıxlıq — 0.3 m²/nəfər": 0.3,
        "Tokyo Standartı — 0.25 m²/nəfər": 0.25
    }
    std_val    = STD_MAP[safety_std]
    auto_limit = int(st_data["area"] / std_val)
    limit      = st.number_input("👥 Kritik Limit (nəfər):", value=auto_limit, step=50, min_value=100)
    warn_pct   = st.slider("🟡 Xəbərdarlıq həddi (%):", 40, 95, 75, step=5)

    staff_on_duty     = st.number_input("👷 Növbədə Personal:", min_value=2, max_value=30, value=8)
    security_officers = st.number_input("🚔 Təhlükəsizlik Zabitləri:", min_value=0, max_value=10, value=2)
    active_turnstiles = st.slider("🚪 Aktiv Turniket:", 2, 20, 10)
    turnstile_speed   = st.select_slider("⚡ Turniket Sürəti (nəf/dəq):",
                                          options=[15, 20, 25, 30, 35, 40], value=25)

    st.divider()

    # ── Scenario ─────────────────────────────────────────────
    st.markdown('<div class="section-header">🚨 Fövqəladə Ssenari</div>', unsafe_allow_html=True)

    scenario = st.selectbox("Ssenari:", [
        "Normal İstismar ✅", "Qatar Sıradan Çıxma 🔧", "Yanğın Siqnalı 🔥",
        "Güc Kəsilməsi ⚡", "Təhlükəsizlik Hadisəsi 🚨",
        "Kütləvi Axın (Hadisə) 👥", "Sel/Daşqın Xəbərdarlığı 🌊",
        "Tibbi Fövqəladə 🚑", "Bomba Təhdidi ⚠️", "Sürüşmə/Torpaq sürüşməsi 🏔️",
        "IT Sistemi Çöküşü 💻", "Turniket Xərabəsi 🔩",
    ])
    SCENARIO_MUL = {
        "Normal İstismar ✅": 1.0, "Qatar Sıradan Çıxma 🔧": 1.88,
        "Yanğın Siqnalı 🔥": 0.0, "Güc Kəsilməsi ⚡": 1.70,
        "Təhlükəsizlik Hadisəsi 🚨": 1.45, "Kütləvi Axın (Hadisə) 👥": 2.40,
        "Sel/Daşqın Xəbərdarlığı 🌊": 2.20, "Tibbi Fövqəladə 🚑": 1.15,
        "Bomba Təhdidi ⚠️": 0.0, "Sürüşmə/Torpaq sürüşməsi 🏔️": 1.30,
        "IT Sistemi Çöküşü 💻": 1.50, "Turniket Xərabəsi 🔩": 1.35,
    }
    scen_mul = SCENARIO_MUL.get(scenario, 1.0)

    SCENARIO_SEVERITY = {
        "Normal İstismar ✅": "INFO", "Qatar Sıradan Çıxma 🔧": "WARNING",
        "Yanğın Siqnalı 🔥": "EVACUATION", "Güc Kəsilməsi ⚡": "CRITICAL",
        "Təhlükəsizlik Hadisəsi 🚨": "WARNING", "Kütləvi Axın (Hadisə) 👥": "CRITICAL",
        "Sel/Daşqın Xəbərdarlığı 🌊": "CRITICAL", "Tibbi Fövqəladə 🚑": "WARNING",
        "Bomba Təhdidi ⚠️": "EVACUATION", "Sürüşmə/Torpaq sürüşməsi 🏔️": "WARNING",
        "IT Sistemi Çöküşü 💻": "WARNING", "Turniket Xərabəsi 🔩": "INFO",
    }
    scenario_severity = SCENARIO_SEVERITY.get(scenario, "INFO")

    st.divider()

    # ── Live Mode ────────────────────────────────────────────
    live_mode    = st.toggle("📡 LIVE IoT REJİMİ", value=False)
    noise_level  = st.select_slider("📊 Sensor Səs-küy Səviyyəsi:",
                                     options=["Aşağı", "Normal", "Yüksək"], value="Normal")
    if live_mode:
        refresh_rate = st.select_slider("🔄 Yenilənmə:", options=[2, 3, 4, 5, 6, 8, 10], value=4)
        st.markdown(f'<span class="live-pulse"></span><span style="color:#3fb950;font-size:12px;font-weight:600">AKTİV · Hər {refresh_rate}s</span>', unsafe_allow_html=True)

# ============================================================
# CORE COMPUTATION
# ============================================================
stansiya_sahesi = st_data["area"]

# Adjust for noise level
NOISE_FACTOR = {"Aşağı": 0.05, "Normal": 0.12, "Yüksək": 0.22}
nf = NOISE_FACTOR[noise_level]

if live_mode:
    base_live  = random.randint(250, 1400)
    live_entry = apply_modifiers(base_live, weather, event_nearby, time_of_day, day_mul)
    live_entry = int(live_entry * scen_mul * (1 + random.uniform(-nf, nf)))
    now_str    = datetime.now().strftime("%H:%M:%S")
    sensors    = sensor_sim(stansiya_sahesi, live_entry, st_data, ambient_temp)
    entry_data = {"time": now_str, "entry": live_entry, **sensors}
    st.session_state.live_history.append(entry_data)
    if len(st.session_state.live_history) > 60:
        st.session_state.live_history = st.session_state.live_history[-60:]
    input_df = pd.DataFrame([{"Saat": h["time"], "Giriş": h["entry"]} for h in st.session_state.live_history])
else:
    base_entries = [280, 540, 920, 1050, 760, 480, 330]
    base_times   = ["07:00","07:30","08:00","08:30","09:00","09:30","10:00"]
    entries_mod  = [apply_modifiers(e, weather, event_nearby, time_of_day, day_mul)
                    for e in base_entries]
    entries_scen = [int(e * scen_mul * (1 + random.uniform(-nf*0.5, nf*0.5)))
                    if scenario not in ["Yanğın Siqnalı 🔥", "Bomba Təhdidi ⚠️"]
                    else 0 for e in entries_mod]
    input_df = pd.DataFrame({"Saat": base_times, "Giriş": entries_scen})

# Queuing model
flow_results = passenger_flow_model(input_df["Giriş"].tolist(), interval, qatar_tutumu, 1.0)
input_df["Sıxlıq"] = flow_results

son_vaziyyat  = flow_results[-1] if flow_results else 0
doluluq_faizi = (son_vaziyyat / limit) * 100 if limit > 0 else 0
los_grade, los_color, los_desc = get_los(son_vaziyyat, stansiya_sahesi)
status_color  = congestion_color(doluluq_faizi)
energy        = energy_kw(interval, son_vaziyyat, st_data["escalators"], escalator_mode, lighting_mode, hvac_mode)
predicted     = predict_curve(son_vaziyyat, interval, qatar_tutumu, input_df["Giriş"].mean(), scenario_mul=scen_mul)
evac_time     = calc_evacuation_time(son_vaziyyat, st_data["exits"], st_data["escalators"], staff_on_duty)
dwell_time    = predict_dwell_time(son_vaziyyat, st_data["platform_len"], qatar_tutumu)
turnstile_cap = active_turnstiles * turnstile_speed
sensors_now   = sensor_sim(stansiya_sahesi, son_vaziyyat, st_data, ambient_temp)

# Energy tracking
st.session_state.energy_history.append({"time": datetime.now().strftime("%H:%M:%S"), "energy": energy, "load": son_vaziyyat})
if len(st.session_state.energy_history) > 50:
    st.session_state.energy_history = st.session_state.energy_history[-50:]

# Auto-incident logging
def log_incident(level, msg, auto=True):
    if auto:
        recent = st.session_state.incident_log[:3]
        if any(i["station"] == stansiya_adi and i["level"] == level and i["message"] == msg for i in recent):
            return
    st.session_state.incident_log.insert(0, {
        "time":     datetime.now().strftime("%H:%M:%S"),
        "station":  stansiya_adi,
        "level":    level,
        "message":  msg,
        "load_pct": round(doluluq_faizi, 1),
        "scenario": scenario,
        "weather":  weather,
    })

if scenario in ["Yanğın Siqnalı 🔥", "Bomba Təhdidi ⚠️"]:
    log_incident("EVAKUASİYA", f"{scenario} — Tam boşaltma başladıldı")
elif doluluq_faizi > 100:
    log_incident("KRİTİK", f"{son_vaziyyat} nəfər — Limit {limit} keçdi ({doluluq_faizi:.0f}%)")
elif doluluq_faizi > warn_pct:
    log_incident("XƏBƏRDARLIQ", f"Doluluq {doluluq_faizi:.1f}% — Xəbərdarlıq həddi keçildi")
if scen_mul > 1.3 and scenario != "Normal İstismar ✅":
    log_incident("SSENARI", f"Aktiv: {scenario} | Çarpan: ×{scen_mul}")
if sensors_now["CO₂ (ppm)"] > 1500:
    log_incident("MÜHİT", f"CO₂ səviyyəsi yüksək: {sensors_now['CO₂ (ppm)']} ppm — Ventilyasiya artırılsın")

# ============================================================
# MAIN HEADER
# ============================================================
col_h1, col_h2, col_h3, col_h4 = st.columns([3, 1, 1, 1])
with col_h1:
    transfer_badge = " <span class='status-badge badge-blue'>🔀 TRANSFER</span>" if is_transfer else ""
    st.markdown(f"<h2 style='margin:0;color:#e6edf3'>🚇 {stansiya_adi}{transfer_badge}</h2>", unsafe_allow_html=True)
    st.caption(f"{st_data['line']} Xətt  |  {scenario}  |  {weather}  |  {time_of_day}  |  {day_type}")

with col_h2:
    if scenario in ["Yanğın Siqnalı 🔥", "Bomba Təhdidi ⚠️"]:
        st.error("🔥 EVAKUASİYA")
    elif doluluq_faizi > 100:
        st.error(f"🚨 KRİTİK {doluluq_faizi:.0f}%")
    elif doluluq_faizi > warn_pct:
        st.warning(f"⚠️ DİQQƏT {doluluq_faizi:.0f}%")
    else:
        st.success(f"✅ NORMAL {doluluq_faizi:.0f}%")

with col_h3:
    st.metric("LOS", f"{los_grade}", delta=los_desc.split("—")[-1].strip())

with col_h4:
    st.metric("Tahliye", f"{evac_time} dəq", delta="Boşaltma vaxtı")

# ============================================================
# TABS
# ============================================================
tab_names = [
    "📊 Dashboard", "📡 Real-Time Monitor", "🗺️ Şəbəkə",
    "🤖 AI Dispetçer", "📈 Proqnostika",
    "🔧 Texniki Baxım", "⚡ Enerji & CO₂", "🚨 Hadisə Jurnalı"
]
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(tab_names)

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 1 — DASHBOARD                                       ║
# ╚══════════════════════════════════════════════════════════╝
with tab1:
    k1, k2, k3, k4, k5, k6, k7, k8 = st.columns(8)
    k1.metric("👥 Mövcud Yük",      f"{son_vaziyyat:,}",   delta=f"+{input_df['Giriş'].iloc[-1]:,}")
    k2.metric("🔴 Kritik Limit",    f"{limit:,}")
    k3.metric("📊 Doluluq",         f"{doluluq_faizi:.1f}%",
              delta=f"{doluluq_faizi-warn_pct:.1f}%" if doluluq_faizi > warn_pct else None,
              delta_color="inverse")
    k4.metric("🏆 LOS",             f"LOS {los_grade}")
    k5.metric("⚡ Enerji (kW)",      f"{energy}")
    k6.metric("🚃 Qatar/Saat",       f"{trains_ph}")
    k7.metric("⏱️ Dwell (san.)",     f"{dwell_time}s")
    k8.metric("🚪 Turniket Kap.",    f"{turnstile_cap}/dəq")

    st.divider()

    col_left, col_right = st.columns([1, 1.3])

    with col_left:
        st.subheader("📍 Stansiya Lokal Xəritəsi")
        all_lats  = [v["lat"] for v in metro_stations.values()]
        all_lons  = [v["lon"] for v in metro_stations.values()]
        all_names = list(metro_stations.keys())
        all_lines = [v["line"] for v in metro_stations.values()]

        fig_map = px.scatter_mapbox(
            pd.DataFrame({"lat": [st_data["lat"]], "lon": [st_data["lon"]],
                          "sz": [max(40, son_vaziyyat / 5)], "name": [stansiya_adi],
                          "pct": [round(doluluq_faizi, 1)]}),
            lat="lat", lon="lon", size="sz",
            hover_name="name", hover_data={"pct": True},
            color_discrete_sequence=[status_color], zoom=13, height=380
        )
        lc_map = {"Qırmızı": "#f85149", "Yaşıl": "#3fb950", "Bənövşəyi": "#bc8cff",
                  "Q/Y": "#f85149", "Y/B": "#3fb950"}
        fig_map.add_scattermapbox(
            lat=all_lats, lon=all_lons, mode="markers",
            marker=dict(size=8, color=[lc_map.get(l, "#888") for l in all_lines], opacity=0.6),
            text=all_names, name="Stansiyalar"
        )
        fig_map.update_layout(mapbox_style="carto-darkmatter",
                               margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
        st.plotly_chart(fig_map, use_container_width=True)

        ic1, ic2, ic3, ic4, ic5 = st.columns(5)
        ic1.metric("📏 Platform", f"{st_data['platform_len']} m")
        ic2.metric("⬆️ Eskalator", f"{st_data['escalators']}")
        ic3.metric("🚪 Çıxış",    f"{st_data['exits']}")
        ic4.metric("🏗️ Dərinlik", f"{st_data['depth_m']} m")
        ic5.metric("📹 CCTV",     f"{st_data['cctv_count']}")

    with col_right:
        st.subheader("📈 Sıxlıq Dinamikası")
        fill_rgba = f"rgba{tuple(int(status_color.lstrip('#')[i:i+2],16) for i in (0,2,4))+(0.12,)}"
        fig_den = go.Figure()
        fig_den.add_trace(go.Scatter(
            x=input_df["Saat"], y=input_df["Sıxlıq"],
            fill="tozeroy", mode="lines+markers",
            line=dict(color=status_color, width=2.5),
            fillcolor=fill_rgba, name="Mövcud Sıxlıq", marker=dict(size=5)
        ))
        fig_den.add_trace(go.Scatter(
            x=input_df["Saat"], y=input_df["Giriş"],
            mode="lines", line=dict(color="#388bfd", width=1.5, dash="dot"),
            name="Giriş axını"
        ))
        fig_den.add_hline(y=limit, line_dash="dash", line_color="#f85149",
                          annotation_text=f"Kritik ({limit:,})", annotation_position="top right",
                          annotation_font_color="#f85149")
        fig_den.add_hline(y=limit * warn_pct / 100, line_dash="dot", line_color="#d29922",
                          annotation_text=f"Xəbərdarlıq ({warn_pct}%)",
                          annotation_font_color="#d29922")
        fig_den.update_layout(template="plotly_dark", height=210,
                               margin=dict(t=15, b=15, l=0, r=0),
                               xaxis_title="Vaxt", yaxis_title="Nəfər",
                               legend=dict(orientation="h", y=1.02),
                               plot_bgcolor="#0d1117", paper_bgcolor="#0d1117")
        st.plotly_chart(fig_den, use_container_width=True)

        st.subheader("📊 Giriş & Sıxlıq Müqayisəsi")
        bar_colors = [congestion_color((v / limit) * 100) if limit > 0 else "#555" for v in input_df["Sıxlıq"]]
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=input_df["Saat"], y=input_df["Giriş"],
            name="Giriş", marker_color=bar_colors,
            text=input_df["Giriş"].astype(str), textposition="outside", opacity=0.85
        ))
        fig_bar.add_trace(go.Scatter(
            x=input_df["Saat"], y=input_df["Sıxlıq"],
            mode="lines+markers", name="Akkumulyasiya",
            line=dict(color="#bc8cff", width=2),
            yaxis="y2"
        ))
        fig_bar.update_layout(
            template="plotly_dark", height=210,
            margin=dict(t=10, b=15, l=0, r=0),
            yaxis=dict(title="Giriş/interval"),
            yaxis2=dict(title="Akkumulyasiya", overlaying="y", side="right", showgrid=False),
            legend=dict(orientation="h", y=1.02),
            plot_bgcolor="#0d1117", paper_bgcolor="#0d1117"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Detailed data editor
    st.divider()
    col_edit1, col_edit2 = st.columns([2, 1])
    with col_edit1:
        st.subheader("✏️ Giriş Məlumatlarını Redaktə Et")
        edit_df = pd.DataFrame(st.session_state.manual_entries)
        edited  = st.data_editor(edit_df, num_rows="dynamic", use_container_width=True, key="data_editor",
                                  column_config={
                                      "Giriş": st.column_config.NumberColumn("Giriş (nəfər)", min_value=0, max_value=5000, step=10),
                                      "Əl İlə Daxil": st.column_config.CheckboxColumn("Manual?"),
                                  })
        st.session_state.manual_entries = edited.to_dict("records")

    with col_edit2:
        st.subheader("📊 Cari Vəziyyət Xülasəsi")
        density_m2 = stansiya_sahesi / max(1, son_vaziyyat)
        st.metric("📐 Sıxlıq (m²/nəfər)", f"{density_m2:.2f}")
        st.metric("🚃 Tutum İstifadəsi", f"{(son_vaziyyat/max(1,theory_cap)*100):.1f}%")
        st.metric("⏳ Boşaltma Vaxtı", f"{evac_time} dəq")
        st.metric("🚪 Turniket Gücü", f"{turnstile_cap} nəf/dəq")

        # Simple progress bars using plotly
        fig_progress = go.Figure()
        fig_progress.add_trace(go.Bar(
            x=[min(100, doluluq_faizi)], y=["Doluluq"],
            orientation="h", marker_color=status_color,
            text=[f"{doluluq_faizi:.0f}%"], textposition="inside"
        ))
        fig_progress.add_trace(go.Bar(
            x=[min(100, (son_vaziyyat/max(1,theory_cap))*100)], y=["Kapasite"],
            orientation="h", marker_color="#388bfd",
            text=[f"{(son_vaziyyat/max(1,theory_cap)*100):.0f}%"], textposition="inside"
        ))
        fig_progress.update_layout(
            template="plotly_dark", height=130, barmode="overlay",
            margin=dict(t=5,b=5,l=0,r=0),
            xaxis=dict(range=[0,100], showticklabels=False),
            showlegend=False, plot_bgcolor="#0d1117", paper_bgcolor="#0d1117"
        )
        st.plotly_chart(fig_progress, use_container_width=True)

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 2 — REAL-TIME MONITOR                               ║
# ╚══════════════════════════════════════════════════════════╝
with tab2:
    if not live_mode:
        st.info("📡 Sol paneldən **LIVE IoT REJİMİ** düyməsini aktivləşdirin. Demo rejimi aktiv.")
        demo_load = st.slider("🎛️ Demo Yük (nəfər):", 0, limit * 2, son_vaziyyat, step=10)
        sensors   = sensor_sim(stansiya_sahesi, demo_load, st_data, ambient_temp)
    else:
        demo_load = son_vaziyyat
        sensors   = sensors_now

    st.subheader(f"📡 IoT Sensor Paneli — {stansiya_adi}")

    col_gauge, col_sensors_area = st.columns([1, 2])

    with col_gauge:
        # Main gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=demo_load if not live_mode else son_vaziyyat,
            delta={"reference": limit, "valueformat": "d",
                   "increasing": {"color": "#f85149"}, "decreasing": {"color": "#3fb950"}},
            title={"text": f"Platform Yükü<br><span style='font-size:0.65em;color:#8b949e'>Limit: {limit:,} | LOS: {los_grade}</span>"},
            gauge={
                "axis": {"range": [0, limit * 1.5], "tickwidth": 1, "tickcolor": "#8b949e"},
                "bar":  {"color": status_color},
                "bgcolor": "#0d1117",
                "bordercolor": "#21262d",
                "steps": [
                    {"range": [0,              limit * 0.4],  "color": "#0a1a0a"},
                    {"range": [limit * 0.4,    limit * 0.6],  "color": "#141a00"},
                    {"range": [limit * 0.6,    limit * 0.75], "color": "#1a1500"},
                    {"range": [limit * 0.75,   limit],        "color": "#1a0a0a"},
                    {"range": [limit,           limit * 1.5], "color": "#200000"},
                ],
                "threshold": {"line": {"color": "#f85149", "width": 4},
                               "thickness": 0.85, "value": limit},
            },
            number={"font": {"color": status_color, "size": 36}, "suffix": " nəf."}
        ))
        fig_gauge.update_layout(template="plotly_dark", height=310,
                                 margin=dict(t=25, b=15, l=10, r=10),
                                 paper_bgcolor="#080b10")
        st.plotly_chart(fig_gauge, use_container_width=True)

        # Secondary meters
        fig_temp = go.Figure(go.Indicator(
            mode="gauge+number",
            value=sensors.get("Temp (°C)", 22),
            title={"text": "Stansiya Temp (°C)"},
            gauge={"axis": {"range": [15, 45]},
                   "bar": {"color": "#f39c12" if sensors.get("Temp (°C)",22) > 30 else "#388bfd"},
                   "steps": [{"range": [15,25],"color":"#0a1a2a"},{"range": [25,35],"color":"#1a1000"},{"range": [35,45],"color":"#1a0500"}],
                   "bgcolor":"#0d1117","bordercolor":"#21262d"},
            number={"font":{"color":"#e6edf3"}}
        ))
        fig_temp.update_layout(template="plotly_dark", height=200, margin=dict(t=25,b=10,l=10,r=10),
                                paper_bgcolor="#080b10")
        st.plotly_chart(fig_temp, use_container_width=True)

    with col_sensors_area:
        st.markdown("**Sensor Oxunuşları — Canlı**")
        s_cols = st.columns(4)
        sensor_icons = {
            "Giriş A": "🚪", "Giriş B": "🚪", "Giriş C": "🚪",
            "Platform": "📊", "Çıxış": "📤", "Eskalator %": "⬆️",
            "Temp (°C)": "🌡️", "Rütubət %": "💧", "CO₂ (ppm)": "🫁",
            "Səs-küy (dB)": "🔊", "CCTV Aktiv": "📹", "WiFi İstifadəçi": "📶"
        }
        co2_val    = sensors.get("CO₂ (ppm)", 600)
        noise_db   = sensors.get("Səs-küy (dB)", 65)
        for idx, (name, val) in enumerate(sensors.items()):
            icon = sensor_icons.get(name, "📡")
            col  = s_cols[idx % 4]
            if name == "Çıxış":
                col.metric(f"{icon} Çıxış", f"{abs(val)} nəf.", delta=str(val))
            elif name == "CO₂ (ppm)":
                delta_co2 = "⚠️ Yüksək!" if co2_val > 1500 else ("Normal" if co2_val < 1000 else "Diqqət")
                col.metric(f"{icon} CO₂", f"{val} ppm", delta=delta_co2,
                           delta_color="inverse" if co2_val > 1000 else "normal")
            elif name == "Səs-küy (dB)":
                col.metric(f"{icon} Səs", f"{val} dB",
                           delta="⚠️ Yüksək" if noise_db > 80 else "Normal",
                           delta_color="inverse" if noise_db > 80 else "normal")
            elif "%" in name:
                col.metric(f"{icon} {name}", f"{val}%")
            elif "Temp" in name:
                col.metric(f"{icon} Temp", f"{val}°C")
            elif "CCTV" in name:
                col.metric(f"{icon} CCTV", str(val))
            elif "WiFi" in name:
                col.metric(f"{icon} WiFi", f"{val} istif.")
            else:
                col.metric(f"{icon} {name}", f"{val} nəf.")

        st.divider()

        # Multi-sensor chart
        if len(st.session_state.live_history) > 3:
            ldf = pd.DataFrame(st.session_state.live_history)
            fig_ms = go.Figure()
            fig_ms.add_trace(go.Scatter(
                x=ldf["time"], y=ldf["entry"],
                mode="lines", name="Giriş", line=dict(color="#388bfd", width=2),
                fill="tozeroy", fillcolor="rgba(56,139,253,0.06)"
            ))
            if "Platform" in ldf.columns:
                fig_ms.add_trace(go.Scatter(
                    x=ldf["time"], y=ldf["Platform"],
                    mode="lines", name="Platform", line=dict(color="#f39c12", width=1.5, dash="dot")
                ))
            if "CO₂ (ppm)" in ldf.columns:
                fig_ms.add_trace(go.Scatter(
                    x=ldf["time"], y=ldf["CO₂ (ppm)"],
                    mode="lines", name="CO₂ (ppm)", line=dict(color="#bc8cff", width=1.5),
                    yaxis="y2"
                ))
            fig_ms.add_hline(y=limit, line_dash="dash", line_color="#f85149",
                              annotation_text="Limit", annotation_font_color="#f85149")
            fig_ms.update_layout(
                template="plotly_dark", height=270,
                margin=dict(t=15,b=15,l=0,r=40),
                title="Son 60 Canlı Oxunuş — Çox Kanal",
                yaxis2=dict(title="CO₂ (ppm)", overlaying="y", side="right", showgrid=False),
                legend=dict(orientation="h", y=1.02),
                plot_bgcolor="#0d1117", paper_bgcolor="#0d1117"
            )
            st.plotly_chart(fig_ms, use_container_width=True)

    st.divider()
    col_stream, col_anom = st.columns([1.6, 1])

    with col_stream:
        st.subheader("📊 Canlı Axın Cədvəli")
        if st.session_state.live_history:
            live_df = pd.DataFrame(st.session_state.live_history).tail(20)
            cols_show = ["time","entry","Platform","CO₂ (ppm)","Temp (°C)","Eskalator %"]
            cols_show = [c for c in cols_show if c in live_df.columns]
            live_df2  = live_df[cols_show].copy()
            live_df2.columns = [c.replace("entry","Giriş").replace("time","Vaxt") for c in cols_show]
            st.dataframe(live_df2, use_container_width=True, hide_index=True)
        else:
            st.info("Live məlumat gözlənilir...")

    with col_anom:
        st.subheader("🔍 Anomaliya Detektoru")
        hist_entries = [h["entry"] for h in st.session_state.live_history[-20:]] if st.session_state.live_history else [son_vaziyyat]
        avg_e = float(np.mean(hist_entries))
        std_e = float(np.std(hist_entries)) if len(hist_entries) > 1 else 1.0
        last_e = hist_entries[-1]
        z_score = abs(last_e - avg_e) / max(1.0, std_e)

        if z_score > 3.0:
            st.error(f"🚨 **KRİTİK ANOMALİYA!** Z={z_score:.2f}\nOrt: {avg_e:.0f} → Cari: {last_e}")
        elif z_score > 2.0:
            st.error(f"⚠️ **ANOMALİYA!** Z={z_score:.2f}")
        elif z_score > 1.5:
            st.warning(f"🟡 Şübhəli axın. Z={z_score:.2f}")
        else:
            st.success(f"✅ Normal axın. Z={z_score:.2f}")

        col_anom1, col_anom2 = st.columns(2)
        col_anom1.metric("Ort. Giriş",    f"{avg_e:.0f}")
        col_anom2.metric("Std. Sapma",    f"±{std_e:.0f}")
        col_anom1.metric("Z-skor",        f"{z_score:.2f}")
        col_anom2.metric("Nümunə sayı",   str(len(hist_entries)))

        if len(hist_entries) > 5:
            trend_val = hist_entries[-1] - hist_entries[-5]
            trend_dir = "📈 Artım" if trend_val > 0 else ("📉 Azalma" if trend_val < 0 else "➡️ Sabit")
            st.metric("Trend (son 5)", trend_dir, delta=str(trend_val))

        st.divider()
        st.subheader("⚡ Ani Əmrlər")

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🔴 Turniketi BAĞLA"):
                log_incident("ƏMƏLIYYAT", f"Operator: {active_turnstiles} turniketin yarısı bağlandı", auto=False)
                st.warning(f"⚠️ {active_turnstiles//2} turniket bağlandı!")
            if st.button("📢 Anons AKTİV"):
                log_incident("ƏMƏLIYYAT", "Sərnişin yönlendirmə anosu aktivdir", auto=False)
                st.info("📢 Anons sistemi işə salındı")
        with btn_col2:
            if st.button("🆘 Fövqəladə"):
                log_incident("FÖVQƏLADƏDİ", "Operator fövqəladə protokol başlatdı", auto=False)
                st.error("🚨 Fövqəladə protokol aktiv!")
            if st.button("🔄 Tarix Sıfırla"):
                st.session_state.live_history = []
                st.success("Sıfırlandı")

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 3 — NETWORK MAP                                     ║
# ╚══════════════════════════════════════════════════════════╝
with tab3:
    st.subheader("🗺️ Baku Metro Tam Şəbəkə Xəritəsi")

    TOD_FACTORS = {
        "Gecə (00–05)": 0.06, "Erkən səhər (05–07)": 0.15,
        "Səhər pik (07–09) 🔴": 0.44, "Gündüz (09–12)": 0.20,
        "Nahar vaxtı (12–14)": 0.25, "Öğlə (14–17)": 0.18,
        "Axşam pik (17–20) 🔴": 0.42, "Axşam (20–22)": 0.14,
        "Gecə yarısı (22–00)": 0.08
    }
    tod_f = TOD_FACTORS.get(time_of_day, 0.20)

    net_records = []
    for nm, nd in metro_stations.items():
        if nm == stansiya_adi:
            approx = son_vaziyyat
        else:
            approx = int(nd["daily_avg"] * tod_f / 12 * day_mul * random.uniform(0.75, 1.25))
        nm_limit = int(nd["area"] / std_val)
        pct      = (approx / nm_limit) * 100 if nm_limit > 0 else 0
        los_g, _, _ = get_los(approx, nd["area"])
        congestion_index = min(10, round(pct / 10, 1))
        net_records.append({
            "İstasiya": nm, "lat": nd["lat"], "lon": nd["lon"],
            "Xətt": nd["line"], "Sıxlıq": approx,
            "Doluluq_%": round(pct, 1), "LOS": los_g,
            "Günlük_Ort": nd["daily_avg"],
            "Tıxac İndeksi": congestion_index,
            "Dərinlik": nd["depth_m"],
        })
    net_df = pd.DataFrame(net_records)

    map_col, legend_col = st.columns([3, 1])
    with map_col:
        fig_net = px.scatter_mapbox(
            net_df, lat="lat", lon="lon",
            size="Sıxlıq", color="Doluluq_%",
            hover_name="İstasiya",
            hover_data={"Doluluq_%": ":.1f", "Sıxlıq": True, "Xətt": True, "LOS": True, "Günlük_Ort": True},
            color_continuous_scale=[[0,"#3fb950"],[0.4,"#56d364"],[0.6,"#d29922"],[0.75,"#db6d28"],[0.9,"#f85149"],[1,"#bc8cff"]],
            range_color=[0, 130], size_max=40, zoom=11, height=520,
        )
        fig_net.update_layout(mapbox_style="carto-darkmatter",
                               margin={"r":0,"t":10,"l":0,"b":0},
                               coloraxis_colorbar=dict(title="Doluluq %", tickfont=dict(color="#8b949e")))
        st.plotly_chart(fig_net, use_container_width=True)

    with legend_col:
        st.markdown("### 🗺️ Rəng Skalaları")
        for label, color, descr in [
            ("0–40%",   "#3fb950", "Azad, rahat"),
            ("40–60%",  "#56d364", "Normal"),
            ("60–75%",  "#d29922", "Məhdud"),
            ("75–90%",  "#db6d28", "Sıxlıq"),
            ("90–100%", "#f85149", "Kritik"),
            (">100%",   "#bc8cff", "Həddindən artıq"),
        ]:
            st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;margin:4px 0">
            <div style="width:16px;height:16px;border-radius:3px;background:{color}"></div>
            <div><span style="color:#e6edf3;font-size:12px;font-weight:600">{label}</span>
            <br><span style="color:#8b949e;font-size:11px">{descr}</span></div></div>""", unsafe_allow_html=True)

        st.divider()
        st.markdown("### 📊 Şəbəkə Statistikası")
        total_pass = net_df["Sıxlıq"].sum()
        critical_stns = len(net_df[net_df["Doluluq_%"] > 100])
        warn_stns = len(net_df[(net_df["Doluluq_%"] > warn_pct) & (net_df["Doluluq_%"] <= 100)])
        st.metric("🚇 Ümumi Yük", f"{total_pass:,}")
        st.metric("🔴 Kritik Stansiya", str(critical_stns))
        st.metric("🟡 Xəbərdarlıq", str(warn_stns))
        st.metric("🟢 Normal", str(len(net_df) - critical_stns - warn_stns))

    # Comparison chart
    st.subheader("📊 Stansiyalar Arası Müqayisə — Top 12")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_line = st.multiselect("Xəttə görə filtr:", sorted(net_df["Xətt"].unique()),
                                      default=sorted(net_df["Xətt"].unique()))
    with col_f2:
        sort_col = st.selectbox("Sıralama:", ["Doluluq_%","Sıxlıq","Günlük_Ort","İstasiya","Tıxac İndeksi"])

    disp = net_df[net_df["Xətt"].isin(filter_line)][
        ["İstasiya","Xətt","Sıxlıq","Doluluq_%","LOS","Günlük_Ort","Tıxac İndeksi","Dərinlik"]
    ].sort_values(sort_col, ascending=False)
    st.dataframe(disp, use_container_width=True, hide_index=True)

    top12 = net_df.nlargest(12, "Doluluq_%")
    fig_cmp = go.Figure()
    fig_cmp.add_trace(go.Bar(
        x=top12["İstasiya"], y=top12["Doluluq_%"],
        marker_color=[congestion_color(p) for p in top12["Doluluq_%"]],
        text=[f"{p:.0f}%" for p in top12["Doluluq_%"]], textposition="outside",
        name="Doluluq %"
    ))
    fig_cmp.add_trace(go.Scatter(
        x=top12["İstasiya"], y=top12["Tıxac İndeksi"],
        mode="lines+markers", name="Tıxac İndeksi",
        line=dict(color="#bc8cff", width=2), yaxis="y2",
        marker=dict(size=6, symbol="diamond")
    ))
    fig_cmp.add_hline(y=100, line_dash="dash", line_color="#f85149",
                       annotation_text="Kritik Limit", annotation_font_color="#f85149")
    fig_cmp.add_hline(y=warn_pct, line_dash="dot", line_color="#d29922",
                       annotation_font_color="#d29922")
    fig_cmp.update_layout(
        template="plotly_dark", height=350,
        title="Top 12 — Ən Yüksək Doluluq %",
        xaxis_tickangle=-30, margin=dict(t=40, b=60),
        yaxis2=dict(title="Tıxac İndeksi", overlaying="y", side="right", range=[0,12], showgrid=False),
        legend=dict(orientation="h", y=1.02),
        plot_bgcolor="#0d1117", paper_bgcolor="#0d1117"
    )
    st.plotly_chart(fig_cmp, use_container_width=True)

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 4 — AI DISPATCHER                                   ║
# ╚══════════════════════════════════════════════════════════╝
with tab4:
    st.subheader("🤖 AI Smart Dispetçer v3.0 — Kontekstual Analiz & Real Tövsiyələr")

    if scenario != "Normal İstismar ✅":
        st.error(f"⚡ Aktiv Ssenari: **{scenario}** | Şiddət: **{scenario_severity}** | Çarpan: ×{scen_mul}")

    neighbors = station_neighbors.get(stansiya_adi, [])
    overflow  = max(0, son_vaziyyat - limit)
    opt_int   = max(1.5, round(interval * 0.55, 1))
    warn_int  = max(1.5, round(interval * 0.72, 1))
    spare_cap = max(0, limit - son_vaziyyat)

    # Determine alert level
    if scenario in ["Yanğın Siqnalı 🔥", "Bomba Təhdidi ⚠️"]:
        alert = "EVACUATION"
    elif son_vaziyyat > limit or scen_mul >= 2.0:
        alert = "CRITICAL"
    elif doluluq_faizi > warn_pct or scen_mul > 1.3:
        alert = "WARNING"
    else:
        alert = "NORMAL"

    # ────────────── CRITICAL ────────────────────────────────
    if alert == "CRITICAL":
        st.markdown(f"""
        <div class="ai-box" style="border-left-color:#f85149;background:#100505;">
        <h3 style="color:#f85149;margin:0 0 10px 0">🚨 SEVİYYƏ QIRMIZI — TƏCİLİ MÜDAXİLƏ TƏLƏBİ</h3>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;font-size:13px;color:#cdd9e5">
            <div><b style="color:#8b949e">Mövcud yük</b><br><span style="color:#f85149;font-size:18px;font-weight:700">{son_vaziyyat:,} nəfər</span></div>
            <div><b style="color:#8b949e">Həddindən artıq</b><br><span style="color:#f85149;font-size:18px;font-weight:700">+{overflow:,} nəfər</span></div>
            <div><b style="color:#8b949e">Boşaltma vaxtı</b><br><span style="color:#d29922;font-size:18px;font-weight:700">{evac_time} dəq</span></div>
        </div>
        <div style="margin-top:12px;font-size:12px;color:#8b949e">
            Stansiya: {stansiya_adi} | Sahə: {stansiya_sahesi} m² | Standart: {safety_std}<br>
            Ssenari: {scenario} | Hava: {weather} | Temperatur: {ambient_temp}°C | Tədrir: {event_nearby}
        </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("#### ⚡ 0–5 Dəqiqə — Dərhal Addımlar")
            imm = [
                f"🚪 **Girişi kəs:** {active_turnstiles} aktiv turniketdən **{max(1, active_turnstiles//2)}**-ni bağla. Qalan {active_turnstiles - active_turnstiles//2} yalnız çıxış üçün. Giriş axınını ~{int(overflow/5)+1} nəfər/dəq-ə endir",
                f"🚃 **İntervalı dərhal dəyiş:** {interval} dəq → **{opt_int} dəq** (saatda +{int(60/opt_int) - trains_ph} əlavə qatar). Depo ilə əlaqə qur",
                f"📢 **Anons sistemi:** 'Hörmətli sərnişinlər! {stansiya_adi} stansiyasının platforması tutub. Zəhmət olmasa növbəti qatarı gözləyin. Giriş sahəsini boşaldın' — 30 san-dakın bir",
                f"⬆️ **Eskalator rejiminə bax:** Cari rejim '{escalator_mode}' — BÜTÜN eskalatorları ÇIXIŞ istiqamətinə keçir",
                f"👷 **Personal yerləşdirmə:** {staff_on_duty} personalın bölgüsü: Giriş nəzarəti (3 nəfər), platform axını (2 nəfər), eskalator başı (2 nəfər), çıxış yolu ({st_data['exits']} çıxış × 1 nəfər)",
                f"📡 **Qonşu stansiyalara alert:** {', '.join(neighbors) if neighbors else 'Terminal stansiya'} — 'Qonşu stansiyaya axın artacaq, hazır olun'",
                f"🔍 **CCTV:** {st_data['cctv_count']} kameranın hamısını aktiv monitora al, zəif yer aşkar et",
            ]
            for a in imm:
                st.markdown(f'<div class="rec-item" style="border-left-color:#f85149">{a}</div>', unsafe_allow_html=True)

        with c2:
            st.markdown("#### 🕐 5–30 Dəqiqə — Operativ Tədbirlər")
            shortage_trains = int(overflow / qatar_tutumu) + 1
            short = [
                f"🚃 **Depodan {shortage_trains} əlavə qatar cəlb et:** Həddindən artıq {overflow} nəfər ÷ {qatar_tutumu} tutum = **{shortage_trains} qatar**. ETA hesabla",
                f"🚌 **Səthi nəqliyyat aktivləşdir:** {stansiya_adi} yaxınlığındakı avtobus dayanacaqlarında əlavə avtobus cəlb et. Yük = {int(overflow*0.4)} nəfər",
                f"📱 **Rəqəmsal kanallar:** Metro tətbiqinə push-bildiriş göndər: 'Alternativ marşrutdan istifadə edin'. Real-time xəritədə stansiya 'Dolu' kimi işarələ",
                f"🔧 **Platform qapılarını yoxla:** PSD statusu '{psd_status}' — Xərabə varsa texniki heyəti dərhal çağır",
                f"📊 **Yük bölgüsü hesabla:** Platform uzunluğu {st_data['platform_len']}m / {son_vaziyyat} nəfər = {st_data['platform_len']/max(1,son_vaziyyat):.2f} m/nəfər. NFPA 130 min. 0.5 m²",
                f"⚡ **Enerji:** Cari {energy} kW. Kritik rejimdə + ~{int(energy*0.25)} kW gözlənilir — UPS yoxla",
                f"🌡️ **İqlim nəzarəti:** {ambient_temp}°C, rütubət {humidity_out}% — Ventilyasiya maksimuma qaldır (CO₂: {sensors_now.get('CO₂ (ppm)', 'N/A')} ppm)",
            ]
            for a in short:
                st.markdown(f'<div class="rec-item" style="border-left-color:#f85149">{a}</div>', unsafe_allow_html=True)

        with c3:
            st.markdown("#### 📋 30+ Dəqiqə — Normalizasiya")
            lng = [
                f"📉 **Boşaltma meyarı:** Yük < **{int(limit*0.72):,}** nəfərə endikdə ({warn_pct-5}%) turniket məhdudiyyətini tədricən qaldır",
                f"📝 **Hesabat:** NFPA 130 tələbi ilə 2 saat ərzində hadisə hesabatı hazırla. Akt nömrəsi, vaxt, max yük ({son_vaziyyat}), tətbiq edilən tədbirlər",
                f"🔧 **Post-hadisə baxış:** {st_data['escalators']} eskalator + {active_turnstiles} turniketin tam yoxlaması. Aşınma qeydə al",
                f"📈 **Analiz:** Bu hadisənin baş vermə səbəbi — {event_nearby} + {weather} + {time_of_day}. Növbəti dəfə üçün profilaktik interval: {warn_int} dəq",
                f"💾 **Arxiv:** Bütün sensor loglarını, CCTV yazılarını, radio danışıqlarını 30 günlük arxivdə saxla",
                f"🔄 **Qaydaya qayış planı:** İnterval {opt_int} → {warn_int} → {interval} dəq, hər 15 dəqiqədən bir yük < 60% olduqda",
                f"📚 **Öyrənmə dövrü:** Hadisə 48 saat içində şöbə müşavirəsinə gətirilsin. Ssenari anbarına əlavə et",
            ]
            for a in lng:
                st.markdown(f'<div class="rec-item" style="border-left-color:#f85149">{a}</div>', unsafe_allow_html=True)

        # Detailed staff allocation table
        st.divider()
        st.markdown("#### 👷 Personal Bölgüsü — Kritik Rejim")
        staff_table = pd.DataFrame([
            {"Mövqe": "Giriş nəzarəti (turniket)", "Tələb": 3, "Mövcud": min(3, staff_on_duty), "Çatmaz": max(0, 3 - staff_on_duty), "Status": "✅" if staff_on_duty >= 3 else "❌ Çatmaz", "Prioritet": "⬆️ Yüksək"},
            {"Mövqe": "Platform axın idarəsi",      "Tələb": 2, "Mövcud": min(2, max(0, staff_on_duty-3)), "Çatmaz": max(0, 2-(staff_on_duty-3)), "Status": "✅" if staff_on_duty >= 5 else "⚠️", "Prioritet": "⬆️ Yüksək"},
            {"Mövqe": "Eskalator nəzarəti",         "Tələb": 2, "Mövcud": min(2, max(0, staff_on_duty-5)), "Çatmaz": max(0, 2-(staff_on_duty-5)), "Status": "✅" if staff_on_duty >= 7 else "⚠️", "Prioritet": "🟡 Orta"},
            {"Mövqe": f"Çıxış ({st_data['exits']} nöqtə)", "Tələb": st_data['exits'], "Mövcud": min(st_data['exits'], max(0, staff_on_duty-7)), "Çatmaz": max(0, st_data['exits']-(staff_on_duty-7)), "Status": "✅" if staff_on_duty >= 7+st_data['exits'] else "❌", "Prioritet": "⬆️ Yüksək"},
            {"Mövqe": "Tibbi hazırlıq (ilk yardım)","Tələb": 1, "Mövcud": 1 if security_officers > 0 else 0, "Çatmaz": 0 if security_officers > 0 else 1, "Status": "✅" if security_officers > 0 else "❌", "Prioritet": "⬆️ Kritik"},
            {"Mövqe": "İnformasiya & yönlendirmə",  "Tələb": 1, "Mövcud": 1, "Çatmaz": 0, "Status": "✅", "Prioritet": "🟡 Orta"},
        ])
        st.dataframe(staff_table, use_container_width=True, hide_index=True)

        total_req  = staff_table["Tələb"].sum()
        total_avail = staff_table["Mövcud"].sum()
        st.markdown(f"**Personal bəzisi:** {total_avail}/{total_req} mövqe örtülüb. {'✅ Kafi' if total_avail >= total_req else f'❌ {total_req - total_avail} nəfər çatmır — növbəyə kənardan çağır'}")

    # ────────────── WARNING ──────────────────────────────────
    elif alert == "WARNING":
        st.markdown(f"""
        <div class="ai-box" style="border-left-color:#d29922;background:#100f00;">
        <h3 style="color:#d29922;margin:0 0 10px 0">⚠️ SEVİYYƏ SARI — QABAQLAYICI MÜDAXİLƏ</h3>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:12px;font-size:13px;color:#cdd9e5">
            <div><b style="color:#8b949e">Cari yük</b><br><span style="font-size:16px;font-weight:700;color:#d29922">{son_vaziyyat:,}</span></div>
            <div><b style="color:#8b949e">Doluluq</b><br><span style="font-size:16px;font-weight:700;color:#d29922">{doluluq_faizi:.1f}%</span></div>
            <div><b style="color:#8b949e">Kritik heddə qalır</b><br><span style="font-size:16px;font-weight:700;color:#3fb950">{spare_cap:,} nəf.</span></div>
            <div><b style="color:#8b949e">Proqnoz (20 dəq)</b><br><span style="font-size:16px;font-weight:700;color:#d29922">{predicted[4] if len(predicted)>4 else '?':,}</span></div>
        </div>
        <div style="margin-top:12px;font-size:12px;color:#8b949e">
            Ssenari: {scenario} | Hava: {weather} | Tədrir: {event_nearby} | CO₂: {sensors_now.get('CO₂ (ppm)','?')} ppm
        </div>
        </div>
        """, unsafe_allow_html=True)

        cw1, cw2, cw3 = st.columns(3)
        with cw1:
            st.markdown("#### 🟡 Preventiv Tədbirlər")
            prev = [
                f"⏱️ **İntervalı azalt:** {interval} dəq → **{warn_int} dəq** (saatda {int(60/warn_int)-trains_ph} əlavə qatar = +{int((60/warn_int - trains_ph)*qatar_tutumu*0.7):.0f} nəf. kapasite)",
                f"📢 **Profilaktik anons:** '...Yaxın dəqiqələrdə sıxlıq gözlənilir. Alternativ marşrutdan istifadəyi tövsiyə edirik...'",
                f"👷 **Personal alert:** {staff_on_duty} personal 'Hazır' rejiminə keçsin. {max(1, staff_on_duty//3)} nəfəri giriş nöqtəsinə yönləndir",
                f"🚪 **Turniket optimi:** {active_turnstiles} aktiv / {turnstile_speed} nəf/dəq = **{turnstile_cap}** nəf/dəq. Yük artarsa 2 əlavə turniket aç",
                f"📊 **Yenilənmə dövr:** Sensor yenilənməsini 30s → **10s** intervalına endir",
                f"🌡️ **Mühit:** {ambient_temp}°C xarici. Platform hava conditioner {hvac_mode} rejimindədir — Sıxlıq artırsa 'Yay tam' rejiminə keç",
            ]
            for p in prev:
                st.markdown(f'<div class="rec-item" style="border-left-color:#d29922">{p}</div>', unsafe_allow_html=True)

        with cw2:
            st.markdown("#### 🔗 Şəbəkə Koordinasiyası")
            if neighbors:
                net_r = [
                    f"📡 **{', '.join(neighbors)}** stansiyalarına xəbərdarlıq: 'Sıxlıq artımı gözlənilir, ehtiyatlı olun'",
                    f"🔄 **Axın yönlendirmə:** Mümkünsə {neighbors[0]} üzərindən alternativ marşrut elan et. Fərq: {abs(metro_stations.get(neighbors[0],{}).get('daily_avg',0) - st_data['daily_avg']):,} nəf/gün",
                    f"⚡ **Avtomatik blok:** Yük {int(limit*0.90):,} nəfər keçərsə turniket avtomatik bağlansın — sistem hazırlığını yoxla",
                    f"🕐 **Gözlənilən pik vaxt:** {time_of_day} + {event_nearby}. Proqnoz maksimum: {max(predicted):,} nəfər ({future_times[predicted.index(max(predicted))] if predicted else '?'})",
                    f"🚌 **Səthi nəqliyyat qoşulması:** Tənzimləmə mərkəzini xəbərdar et — ola bilər {int(spare_cap*0.3)} nəfər yönlendirmə tələb olsun",
                ]
            else:
                net_r = [
                    f"ℹ️ **Terminal stansiya:** {stansiya_adi} terminal stansiyasıdır. Alternativ cəhəti yoxdur",
                    f"🚌 **Səthi alternativ:** Səthi nəqliyyatı (avtobus/taksi) aktiv saxla. Ehtiyac varsa gücləndir",
                    f"📢 **Anons:** Sərnişinləri növbəti qatar vaxta qədər dayanacaq zonasında saxla",
                ]
            for r in net_r:
                st.markdown(f'<div class="rec-item" style="border-left-color:#d29922">{r}</div>', unsafe_allow_html=True)

        with cw3:
            st.markdown("#### 📅 Növbəti Pik Hazırlığı")
            peak_prep = [
                f"🔮 **Proqnoz:** Cari trend ilə {int(doluluq_faizi + 12):.0f}% olma ehtimalı. Kritik heddə: {max(0, int((limit - son_vaziyyat) / max(1, input_df['Giriş'].mean()) * 5)):.0f} dəq",
                f"🚃 **Qatar növü:** {train_type} — {qatar_tutumu} nəf. tutum. Daha böyük (CAF/Siemens) mövcuddursa dövriyyəyə al",
                f"👷 **Növbə çağırışı:** {max(0, 10 - staff_on_duty)} əlavə personal tələb olunarsa depo növbəsindən çağır",
                f"📋 **Checklist hazırlığı:** Turniket ({active_turnstiles}✓) | Eskalator ({st_data['escalators']}✓) | CCTV ({st_data['cctv_count']}✓) | Anons ✓",
                f"⚡ **Enerji ehtiyatı:** UPS şarjını yoxla. Cari yük {energy} kW — pik rejimdə ~{int(energy*1.3)} kW",
            ]
            for p in peak_prep:
                st.markdown(f'<div class="rec-item" style="border-left-color:#d29922">{p}</div>', unsafe_allow_html=True)

    # ────────────── EVACUATION ───────────────────────────────
    elif alert == "EVACUATION":
        is_bomb = "Bomba" in scenario
        evac_color = "#ff0000" if not is_bomb else "#ff6600"
        evac_title = "🔥 YANĞIN EVAKUASİYA PROTOKOlu" if not is_bomb else "⚠️ BOMBA TƏHDİDİ — GİZLİ EVAKUASİYA"

        st.markdown(f"""
        <div class="ai-box" style="border-left-color:{evac_color};border-width:8px;background:#1a0000;">
        <h2 style="color:{evac_color};margin:0">{evac_title}</h2>
        <h3 style="color:#ffaaaa;margin:6px 0 0 0">{stansiya_adi.upper()} — Bütün Personal Prosedura Başlamalıdır</h3>
        <div style="color:#ff8888;font-size:13px;margin-top:8px">
            Boşaltma vaxtı: <b>{evac_time} dəq</b> | 
            Çıxış sayı: <b>{st_data['exits']}</b> | 
            Eskalator: <b>{st_data['escalators']}</b> | 
            Personal: <b>{staff_on_duty + security_officers}</b>
        </div>
        </div>
        """, unsafe_allow_html=True)

        ce1, ce2, ce3 = st.columns(3)
        with ce1:
            st.error("**📋 Dərhal (0–2 dəq)**")
            evac_steps = [
                "🔕 Bütün turniketlər → AÇIQ rejim",
                "🚨 Fövqəladə həyəcan siqnalı → AKTİV",
                "📢 Evakuasiya anosu → BAŞLAT (davamlı)",
                f"⬆️ {st_data['escalators']} eskalatorun hamısı → YUXARIYA",
                "🚃 Bütün qatarlar → SAXLA (platformada)",
                "💡 Fövqəladə işıqlandırma → AKTİV",
                "📵 Platformaya yeni giriş → TAMAMILƏ KƏS",
            ]
            for s in evac_steps:
                st.markdown(f"**{s}**")

        with ce2:
            st.warning("**📏 Boşaltma Hesablaması**")
            flow_exit = 120
            flow_esc  = 80
            total_flow = st_data['exits'] * flow_exit + st_data['escalators'] * flow_esc
            real_evac_t = round(son_vaziyyat / total_flow, 1)
            st.markdown(f"""
            | Parametr | Dəyər |
            |----------|-------|
            | Stansiyada nəfər | **{son_vaziyyat:,}** |
            | Aktiv çıxış | **{st_data['exits']}** |
            | Axın/çıxış | **{flow_exit} nəfər/dəq** |
            | Eskalator axını | **{flow_esc} nəfər/dəq** |
            | Ümumi kapasite | **{total_flow} nəfər/dəq** |
            | **Boşaltma vaxtı** | **{real_evac_t} dəq** |
            | Personal/zona | **{st_data['area']//max(1, staff_on_duty+security_officers):.0f} m²** |
            """)
            if not is_bomb:
                st.error(f"⚠️ Duman dərinlik: {st_data['depth_m']}m — Ventilyasiya kritikdir!")

        with ce3:
            st.info("**📞 Əlaqə Protokolu**")
            st.markdown("""
            | Xidmət | Nömrə | Prioritet |
            |--------|-------|-----------|
            | 🚒 Yanğınsöndürmə | **101** | ⬆️ 1-ci |
            | 🚔 Polis | **102** | ⬆️ 1-ci |
            | 🚑 Təcili Yardım | **103** | ⬆️ 1-ci |
            | 📡 Metro Mərkəzi | **int. 555** | 2-ci |
            | 🏛️ Baş Dispetçer | **int. 100** | 2-ci |
            | 🔐 Mülki Müdafiə | **112** | 1-ci |
            """)
            if is_bomb:
                st.error("⚠️ BOMBA TƏHDİDİ: Sərnişinlərə məlumat verməyin. Sakitcə boşaldın. Polis gəlməmiş içəri girməyin!")

    # ────────────── NORMAL ───────────────────────────────────
    else:
        st.markdown(f"""
        <div class="ai-box" style="border-left-color:#3fb950;background:#030f05;">
        <h3 style="color:#3fb950;margin:0 0 10px 0">✅ SEVİYYƏ YAŞIL — SİSTEM OPTİMAL İŞLƏYİR</h3>
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;font-size:13px;color:#cdd9e5">
            <div><b style="color:#8b949e">Cari yük</b><br><span style="color:#3fb950;font-size:16px;font-weight:700">{son_vaziyyat:,}</span></div>
            <div><b style="color:#8b949e">Doluluq</b><br><span style="color:#3fb950;font-size:16px;font-weight:700">{doluluq_faizi:.1f}%</span></div>
            <div><b style="color:#8b949e">LOS</b><br><span style="color:#3fb950;font-size:16px;font-weight:700">{los_grade}</span></div>
            <div><b style="color:#8b949e">Enerji</b><br><span style="color:#3fb950;font-size:16px;font-weight:700">{energy} kW</span></div>
            <div><b style="color:#8b949e">Boş kapasite</b><br><span style="color:#3fb950;font-size:16px;font-weight:700">{spare_cap:,}</span></div>
        </div>
        </div>
        """, unsafe_allow_html=True)

        cn1, cn2, cn3 = st.columns(3)
        with cn1:
            st.markdown("#### 💡 Enerji & Xərc Optimi")
            opt_interval_new = min(12.0, interval + 2.0)
            energy_save = round(energy * 0.18, 1)
            cost_save   = round(energy_save * 0.12, 2)
            opts = [
                f"⚡ **İntervalı artır:** {interval} → {opt_interval_new} dəq = **~{energy_save} kW** qənaət/saat (~{cost_save} AZN/saat). Cari yük {son_vaziyyat} nəf. ilə optimal",
                f"💡 **İşıqlandırma:** Cari '{lighting_mode}' rejimindən 'Yarı' rejiminə keç — ~{int(energy*0.08)} kW qənaət. LOS {los_grade} şəraitdə tam işıq lazım deyil",
                f"❄️ **HVAC:** Cari '{hvac_mode}'. Dışarıda {ambient_temp}°C — platformaya lazım olan temperatur 22°C-dir. Tənzimləmə lazım: {'Evet' if abs(ambient_temp-22)>5 else 'Xeyr'}",
                f"⬆️ **Eskalator:** {st_data['escalators']} ədəddən 1-ni texniki baxışa çıxar (indi uyğun vaxt, axın azdır). Qalan {st_data['escalators']-1} kifayətdir",
                f"🌡️ **CO₂:** {sensors_now.get('CO₂ (ppm)', 'N/A')} ppm. {'Normal' if int(str(sensors_now.get('CO₂ (ppm)', 600)).replace(' ppm','')) < 1000 else 'Ventilyasiya artır'} — LOS {los_grade} üçün 1000 ppm hedd",
            ]
            for o in opts:
                st.markdown(f'<div class="rec-item" style="border-left-color:#3fb950">{o}</div>', unsafe_allow_html=True)

        with cn2:
            st.markdown("#### 🔧 Profilaktik Texniki İşlər")
            maint = [
                f"🔩 **Turniket baxışı:** {active_turnstiles} aktiv turniketi növbəli şəkildə yoxla. Saatda {turnstile_cap} nəf. keçir — sürtünmə yoxlanması",
                f"📹 **CCTV:** {st_data['cctv_count']} kameranın görüntü keyfiyyətini yoxla. Son baxış tarixini sistemdə yeniləyin",
                f"🚪 **Platform qapıları:** PSD statusu '{psd_status}' — Tam qapalı PSD varsa contaları, hava sızdırmazlığını yoxla",
                f"🧹 **Platforma təmizliyi:** Aşağı trafik vaxtı platform, eskalator, tualet təmizliyi. Sanitasiya normaları",
                f"📡 **İnformasiya ekranları:** Bütün ekranların məzmununu yeniləyin. {'WiFi aktiv — bağlantını yoxla' if st_data.get('wifi') else 'WiFi yoxdur — kabel bağlantısını yoxla'}",
            ]
            for m in maint:
                st.markdown(f'<div class="rec-item" style="border-left-color:#3fb950">{m}</div>', unsafe_allow_html=True)

        with cn3:
            st.markdown("#### 📅 Növbəti Pik Planlaması")
            next_peak = "Axşam pik (17–20)" if "Gündüz" in time_of_day or "Nahar" in time_of_day else "Sabah səhər pik (07–09)"
            plan = [
                f"📈 **Növbəti pik:** {next_peak}. Gözlənilən yük: ~{int(st_data['daily_avg'] * 0.44 / 12):,} nəfər/interval",
                f"🚃 **Qatar hazırlığı:** {train_type} — pik üçün {min(3.0, interval-0.5):.1f} dəq intervalı tövsiyə edilir",
                f"👷 **Personal:** Cari {staff_on_duty} — pik üçün {min(20, staff_on_duty + 3)} tövsiyə edilir (+{min(3, 20-staff_on_duty)} əlavə)",
                f"📋 **{safety_std}:** Tam uyğunluq. Gündəlik ortalama {st_data['daily_avg']:,} nəf. — limit {limit:,} nəf.",
                f"💾 **Son yoxlama:** {datetime.now().strftime('%d.%m.%Y %H:%M')} — Sistem statusu: ✅ HAZIR",
            ]
            for p in plan:
                st.markdown(f'<div class="rec-item" style="border-left-color:#3fb950">{p}</div>', unsafe_allow_html=True)

    # Cascade Analysis
    st.divider()
    st.markdown("### 🔗 Qonşu Stansiyalara Kaskad Təsir Analizi")
    if neighbors:
        future_times_pred = [(datetime.now() + timedelta(minutes=5*i)).strftime("%H:%M") for i in range(len(predicted))]
        crows = []
        for nb in neighbors:
            nd2 = metro_stations.get(nb, {})
            if nd2:
                spill_pct = 0.35 if son_vaziyyat > limit else (0.15 if doluluq_faizi > warn_pct else 0.05)
                spill     = max(0, (son_vaziyyat - limit) * spill_pct) if son_vaziyyat > limit else 0
                nb_est    = int(nd2["daily_avg"] * tod_f / 12 * day_mul * random.uniform(0.8,1.2) + spill)
                nb_lim    = int(nd2["area"] / std_val)
                nb_pct    = (nb_est / nb_lim) * 100 if nb_lim > 0 else 0
                nb_los_g, _, _ = get_los(nb_est, nd2["area"])
                risk  = "🔴 Yüksək" if nb_pct > 80 else ("🟡 Orta" if nb_pct > 50 else "🟢 Aşağı")
                spill_load = f"+{int(spill):,} kaskad" if spill > 0 else "Yoxdur"
                crows.append({
                    "Stansiya": nb, "Xətt": nd2["line"],
                    "Sahə (m²)": nd2["area"], "Təxmini Yük": nb_est,
                    "Kaskad Yükü": spill_load, "Limit": nb_lim,
                    "Doluluq %": f"{nb_pct:.1f}%", "LOS": nb_los_g, "Risk": risk,
                    "Tövsiyə": f"İntervalı {max(1.5, interval-0.5):.1f} dəq-ə endir" if nb_pct > 70 else "Normal izlə",
                })
        st.dataframe(pd.DataFrame(crows), use_container_width=True, hide_index=True)
    else:
        st.info(f"ℹ️ {stansiya_adi} terminal stansiyasıdır — kaskad analiz tətbiq edilmir.")

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 5 — PREDICTIVE ANALYTICS                            ║
# ╚══════════════════════════════════════════════════════════╝
with tab5:
    st.subheader("📈 Proqnostik Analitika — Çoxlu Model Müqayisəsi")

    future_times = [(datetime.now() + timedelta(minutes=5*i)).strftime("%H:%M") for i in range(len(predicted))]
    upper = [int(p * 1.20) for p in predicted]
    lower = [int(p * 0.80) for p in predicted]

    # Scenario comparison
    pred_normal   = predict_curve(son_vaziyyat, interval, qatar_tutumu, input_df["Giriş"].mean(), scenario_mul=1.0)
    pred_optimist = predict_curve(son_vaziyyat, interval*0.8, qatar_tutumu, input_df["Giriş"].mean()*0.85, scenario_mul=1.0)
    pred_pessimist= predict_curve(son_vaziyyat, interval, qatar_tutumu, input_df["Giriş"].mean()*1.25, scenario_mul=scen_mul)

    col_p1, col_p2 = st.columns([1.8, 1])

    with col_p1:
        fig_pred = go.Figure()
        # Confidence band
        fig_pred.add_trace(go.Scatter(
            x=future_times + future_times[::-1],
            y=upper + lower[::-1],
            fill="toself", fillcolor="rgba(56,139,253,0.06)",
            line=dict(color="rgba(0,0,0,0)"), name="Güvən Zolağı (±20%)", showlegend=True
        ))
        # Historical
        fig_pred.add_trace(go.Scatter(
            x=input_df["Saat"].tolist(), y=input_df["Sıxlıq"].tolist(),
            mode="lines+markers", name="Tarixi məlumat",
            line=dict(color="#388bfd", width=2.5), marker=dict(size=5)
        ))
        # Forecast scenarios
        fig_pred.add_trace(go.Scatter(
            x=future_times, y=pred_optimist,
            mode="lines", name="Optimist (interval azalma)",
            line=dict(color="#3fb950", width=1.5, dash="dot")
        ))
        fig_pred.add_trace(go.Scatter(
            x=future_times, y=predicted,
            mode="lines+markers", name="Əsas Proqnoz",
            line=dict(color="#d29922", width=2, dash="dash"),
            marker=dict(symbol="diamond", size=6, color="#d29922")
        ))
        fig_pred.add_trace(go.Scatter(
            x=future_times, y=pred_pessimist,
            mode="lines", name="Pessimist (ssenari ilə)",
            line=dict(color="#f85149", width=1.5, dash="dashdot")
        ))
        fig_pred.add_hline(y=limit, line_dash="dash", line_color="#f85149",
                            annotation_text="Kritik Limit", annotation_position="top right",
                            annotation_font_color="#f85149")
        fig_pred.add_hline(y=limit * warn_pct / 100, line_dash="dot", line_color="#d29922",
                            annotation_text=f"Xəbərdarlıq {warn_pct}%", annotation_font_color="#d29922")
        fig_pred.update_layout(
            template="plotly_dark", height=420,
            title="Sıxlıq Proqnozu — 3 Ssenari Müqayisəsi",
            xaxis_title="Vaxt", yaxis_title="Nəfər",
            legend=dict(orientation="h", y=1.02),
            plot_bgcolor="#0d1117", paper_bgcolor="#0d1117"
        )
        st.plotly_chart(fig_pred, use_container_width=True)

        # Hourly profile + heatmap
        col_hp1, col_hp2 = st.columns(2)
        with col_hp1:
            st.subheader("🕐 Gündəlik Profil")
            HOURLY = {
                "00–06": 0.04, "06–07": 0.10, "07–08": 0.32, "08–09": 0.42,
                "09–12": 0.20, "12–14": 0.25, "14–17": 0.22,
                "17–18": 0.40, "18–19": 0.38, "19–20": 0.26, "20–24": 0.08
            }
            hourly_vals = {k: int(v * st_data["daily_avg"] / 12 * day_mul) for k, v in HOURLY.items()}
            fig_hourly = go.Figure(go.Bar(
                x=list(hourly_vals.keys()), y=list(hourly_vals.values()),
                marker_color=[congestion_color((v/limit)*100) if limit>0 else "#555" for v in hourly_vals.values()],
                text=[f"{v:,}" for v in hourly_vals.values()], textposition="outside"
            ))
            fig_hourly.add_hline(y=limit, line_dash="dash", line_color="#f85149")
            fig_hourly.update_layout(template="plotly_dark", height=250, margin=dict(t=10,b=20),
                                      plot_bgcolor="#0d1117", paper_bgcolor="#0d1117")
            st.plotly_chart(fig_hourly, use_container_width=True)

        with col_hp2:
            st.subheader("📅 Həftəlik Heatmap")
            days  = ["Bazar ertəsi","Çərşənbə axşamı","Çərşənbə","Cümə axşamı","Cümə","Şənbə","Bazar"]
            hours = ["07–08", "08–09", "12–13", "17–18", "18–19"]
            DAY_MULT = [1.0, 1.0, 1.0, 1.0, 1.05, 0.85, 0.72]
            heat_data = []
            for di, (day, dm) in enumerate(zip(days, DAY_MULT)):
                row = []
                for hi, h in enumerate(hours):
                    base_h = HOURLY.get(h.split("–")[0]+"-"+str(int(h.split("–")[0])+1), 0.22)
                    val = int(st_data["daily_avg"] * base_h / 12 * dm)
                    row.append(int(min(130, (val/limit)*100) if limit>0 else 0))
                heat_data.append(row)
            fig_heat = go.Figure(go.Heatmap(
                z=heat_data, x=hours, y=days,
                colorscale=[[0,"#0a1a0a"],[0.4,"#1a2a00"],[0.6,"#2a1a00"],[0.8,"#3a0a00"],[1.0,"#5a0000"]],
                text=[[f"{v}%" for v in row] for row in heat_data],
                texttemplate="%{text}", colorbar=dict(title="Doluluq %")
            ))
            fig_heat.update_layout(template="plotly_dark", height=250, margin=dict(t=10,b=20),
                                    paper_bgcolor="#0d1117")
            st.plotly_chart(fig_heat, use_container_width=True)

    with col_p2:
        st.markdown("### 📊 Proqnoz Xülasəsi")
        max_pred  = max(predicted)
        min_pred  = min(predicted)
        avg_pred  = int(np.mean(predicted))
        max_opt   = max(pred_optimist)
        max_pess  = max(pred_pessimist)

        st.metric("🔺 Maks. (Əsas)",     f"{max_pred:,}", delta=f"+{max_pred-son_vaziyyat:,}")
        st.metric("🔺 Maks. (Pessimist)", f"{max_pess:,}", delta=f"+{max_pess-max_pred:,}", delta_color="inverse")
        st.metric("🔺 Maks. (Optimist)",  f"{max_opt:,}", delta=f"{max_opt-max_pred:,}", delta_color="normal")
        st.metric("📊 Orta Proqnoz",      f"{avg_pred:,}")
        st.metric("🔝 Teorik Tutum",      f"{theory_cap:,} nəf/saat")

        will_exceed = any(p > limit for p in predicted)
        exceed_idx  = next((i for i, p in enumerate(predicted) if p > limit), None)
        will_warn   = any(p > limit * warn_pct / 100 for p in predicted)

        st.divider()
        if will_exceed and exceed_idx is not None:
            st.error(f"⚠️ **Limit {future_times[exceed_idx]}-da keçiləcək!**\nTəxmini: {predicted[exceed_idx]:,} nəfər")
        elif will_warn:
            st.warning(f"⚠️ Xəbərdarlıq həddi {warn_pct}% keçiləcək")
        else:
            st.success("✅ Növbəti 60 dəq. limit keçilməyəcək")

        st.divider()
        st.markdown("### 🎯 Effektivlik İndeksləri")
        utilization     = (son_vaziyyat / max(1, theory_cap)) * 100
        hw_efficiency   = (1 - interval / 15.0) * 100
        ener_per_pass   = (energy / max(1, son_vaziyyat)) * 1000
        los_score       = {"A": 100,"B": 85,"C": 65,"D": 45,"E": 25,"F": 5}.get(los_grade, 50)
        co2_score       = max(0, 100 - (sensors_now.get("CO₂ (ppm)", 600) - 400) / 20)
        staff_eff       = min(100, (staff_on_duty / max(1, int(son_vaziyyat/200))) * 100)

        e1, e2 = st.columns(2)
        e1.metric("🎯 Kapasite İstif.",  f"{utilization:.1f}%")
        e2.metric("⏱️ Headway Eff.",     f"{hw_efficiency:.0f}%")
        e1.metric("⚡ Enerji/Nəfər",     f"{ener_per_pass:.1f} Wh")
        e2.metric("🏆 LOS Balı",         f"{los_score}/100")
        e1.metric("🌿 CO₂ Balı",         f"{co2_score:.0f}/100")
        e2.metric("👷 Personal Eff.",    f"{staff_eff:.0f}%")

        # Radar
        categories = ["Təhlükəsizlik","Enerji","Axın","LOS","Kapasite","CO₂","Personal"]
        r_values   = [
            max(0, 100 - doluluq_faizi),
            max(0, 100 - (energy / 100) * 100),
            min(100, utilization * 1.2),
            los_score,
            min(100, (theory_cap / max(1, st_data["daily_avg"])) * 50),
            co2_score,
            staff_eff,
        ]
        fig_radar = go.Figure(go.Scatterpolar(
            r=r_values + [r_values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(56,139,253,0.12)",
            line=dict(color="#388bfd", width=2)
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(range=[0,100], showticklabels=False,
                                       gridcolor="#21262d"),
                       angularaxis=dict(gridcolor="#21262d")),
            template="plotly_dark", height=300,
            title="Stansiya Sağlamlıq İndeksi (7 Göstərici)",
            margin=dict(t=40, b=20),
            paper_bgcolor="#0d1117"
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 6 — MAINTENANCE                                     ║
# ╚══════════════════════════════════════════════════════════╝
with tab6:
    st.subheader(f"🔧 Texniki Baxım & Avadanlıq Vəziyyəti — {stansiya_adi}")

    # Generate or cache maintenance data
    cache_key = f"maint_{stansiya_adi}"
    if cache_key not in st.session_state.maintenance_data:
        st.session_state.maintenance_data[cache_key] = get_maintenance_schedule(st_data)
    maint_items = st.session_state.maintenance_data[cache_key]

    # Summary metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    critical_items = sum(1 for i in maint_items if "Kritik" in i["Vəziyyət"])
    warning_items  = sum(1 for i in maint_items if "Diqqət" in i["Vəziyyət"])
    ok_items       = len(maint_items) - critical_items - warning_items
    avg_life       = int(np.mean([i["Qalıq Ömür %"] for i in maint_items]))

    m1.metric("🔧 Avadanlıq sayı",  str(len(maint_items)))
    m2.metric("🔴 Kritik",          str(critical_items))
    m3.metric("🟡 Diqqət",          str(warning_items))
    m4.metric("🟢 Normal",          str(ok_items))
    m5.metric("📊 Ort. Qalıq Ömür", f"{avg_life}%")

    st.divider()

    col_maint1, col_maint2 = st.columns([1.5, 1])

    with col_maint1:
        st.markdown("### 📋 Avadanlıq Vəziyyəti Cədvəli")

        # Color-coded equipment table
        for item in maint_items:
            status = item["Vəziyyət"]
            life   = item["Qalıq Ömür %"]
            if "Kritik" in status:
                border_color = "#f85149"
            elif "Diqqət" in status:
                border_color = "#db6d28"
            elif "Qənaətbəxş" in status:
                border_color = "#d29922"
            else:
                border_color = "#3fb950"

            bar_width = max(5, min(100, life))
            bar_color = "#f85149" if life < 30 else ("#d29922" if life < 60 else "#3fb950")

            st.markdown(f"""
            <div class="maintenance-card" style="border-left:4px solid {border_color}">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <span style="color:#e6edf3;font-weight:600;font-size:13px">{item['Avadanlıq']}</span>
                    <span class="status-badge" style="background:rgba(0,0,0,0.3);color:{border_color};border:1px solid {border_color}">{status}</span>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px;font-size:12px;color:#8b949e">
                    <span>📅 Son: {item['Son Baxış']}</span>
                    <span>📅 Növbəti: {item['Növbəti Baxış']}</span>
                </div>
                <div style="margin-top:8px">
                    <div style="display:flex;justify-content:space-between;font-size:11px;color:#8b949e;margin-bottom:3px">
                        <span>Qalıq Ömür</span><span style="color:{bar_color}">{life}%</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width:{bar_width}%;background:{bar_color}"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_maint2:
        st.markdown("### 📊 Vəziyyət Analizi")

        # Pie chart for equipment status
        status_counts = {}
        for item in maint_items:
            s = item["Vəziyyət"].split()[0]
            status_counts[s] = status_counts.get(s, 0) + 1

        fig_maint_pie = go.Figure(go.Pie(
            labels=list(status_counts.keys()),
            values=list(status_counts.values()),
            hole=0.5,
            marker_colors=["#3fb950","#56d364","#d29922","#db6d28","#f85149"],
            textinfo="label+percent"
        ))
        fig_maint_pie.update_layout(template="plotly_dark", height=250,
                                     margin=dict(t=10,b=10), showlegend=False,
                                     paper_bgcolor="#0d1117")
        st.plotly_chart(fig_maint_pie, use_container_width=True)

        # Bar chart for remaining life
        fig_life = go.Figure(go.Bar(
            x=[i["Qalıq Ömür %"] for i in maint_items],
            y=[i["Avadanlıq"].split()[0] + " " + " ".join(i["Avadanlıq"].split()[1:3]) for i in maint_items],
            orientation="h",
            marker_color=[("#f85149" if i["Qalıq Ömür %"] < 30 else
                           "#d29922" if i["Qalıq Ömür %"] < 60 else "#3fb950") for i in maint_items],
            text=[f"{i['Qalıq Ömür %']}%" for i in maint_items], textposition="outside"
        ))
        fig_life.add_vline(x=30, line_dash="dash", line_color="#f85149",
                            annotation_text="Kritik")
        fig_life.add_vline(x=60, line_dash="dot", line_color="#d29922",
                            annotation_text="Diqqət")
        fig_life.update_layout(template="plotly_dark", height=280, xaxis=dict(range=[0,115]),
                                margin=dict(t=10,b=10,l=0,r=50),
                                title="Avadanlıq Qalıq Ömrü (%)",
                                paper_bgcolor="#0d1117", plot_bgcolor="#0d1117")
        st.plotly_chart(fig_life, use_container_width=True)

        st.divider()
        st.markdown("### ⏰ Yaxın Vaxtda Baxış Tələb Edənlər")
        urgent = sorted(maint_items, key=lambda x: x["Qalıq Ömür %"])[:3]
        for u in urgent:
            life = u["Qalıq Ömür %"]
            color = "#f85149" if life < 30 else "#d29922"
            st.markdown(f"""
            <div style="background:#0d1117;border:1px solid {color};border-radius:6px;padding:10px;margin:4px 0">
                <span style="color:{color};font-weight:600">⚠️ {u['Avadanlıq']}</span>
                <br><span style="color:#8b949e;font-size:12px">Qalıq ömür: {life}% | Növbəti: {u['Növbəti Baxış']}</span>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🔄 Baxım Məlumatlarını Yenilə"):
            del st.session_state.maintenance_data[cache_key]
            st.success("Yeniləndi!")
            st.rerun()

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 7 — ENERGY & CO₂                                   ║
# ╚══════════════════════════════════════════════════════════╝
with tab7:
    st.subheader("⚡ Enerji İdarəetmə & Karbon İzi Monitorinqi")

    # Energy KPIs
    e1, e2, e3, e4, e5, e6 = st.columns(6)
    daily_energy   = round(energy * 18, 1)
    monthly_energy = round(daily_energy * 30, 0)
    co2_per_kwh    = 0.45  # AZE grid: kg CO2/kWh
    daily_co2      = round(daily_energy * co2_per_kwh, 1)
    cost_per_kwh   = 0.088  # AZN/kWh
    daily_cost     = round(daily_energy * cost_per_kwh, 2)
    energy_per_pass = round((energy / max(1, son_vaziyyat)) * 1000, 1)

    e1.metric("⚡ Anlıq (kW)",       f"{energy}")
    e2.metric("📅 Günlük (kWh)",     f"{daily_energy:,}")
    e3.metric("💰 Günlük Xərc",      f"{daily_cost} AZN")
    e4.metric("🌿 Günlük CO₂",       f"{daily_co2} kg")
    e5.metric("👤 kWh/Nəfər",        f"{energy_per_pass:.1f} Wh")
    e6.metric("📊 Aylıq (kWh)",      f"{monthly_energy:,}")

    st.divider()

    col_en1, col_en2 = st.columns([1.6, 1])

    with col_en1:
        # Energy breakdown
        st.subheader("🔋 Enerji İstehlakı Analizi")

        trains_ph_local = int(60 / interval)
        esc_mode_mult   = {"Normal (ikisi giriş, ikisi çıxış)": 1.0, "Hamısı yukarı (boşaltma)": 1.3,
                           "Hamısı aşağı (doluşma)": 1.3, "Avari (manual)": 0.5, "Tam dayandırılmış ⛔": 0.1}
        esc_mul = esc_mode_mult.get(escalator_mode, 1.0)

        comp_labels = ["Qatarlar","Eskalatorlar","İşıqlandırma","HVAC","Yük (turniket/digər)"]
        comp_vals   = [
            round(trains_ph_local * 14, 1),
            round(st_data["escalators"] * 2.2 * esc_mul, 1),
            {"Tam": 18, "Yarı": 10, "Minimal": 4, "Fövqəladə": 2}.get(lighting_mode, 12),
            {"Yaz/Payız": 22, "Yay tam": 45, "Qış isitmə": 38, "Minimal": 8}.get(hvac_mode, 22),
            round(max(5, son_vaziyyat / 75), 1),
        ]

        fig_energy_pie = go.Figure(go.Pie(
            labels=comp_labels, values=comp_vals,
            hole=0.4,
            marker_colors=["#388bfd","#3fb950","#d29922","#f85149","#bc8cff"],
            textinfo="label+percent+value",
            hovertemplate="<b>%{label}</b><br>%{value} kW<br>%{percent}<extra></extra>"
        ))
        fig_energy_pie.update_layout(template="plotly_dark", height=320, margin=dict(t=20,b=10),
                                      title="Enerji Komponent Bölgüsü (kW)",
                                      paper_bgcolor="#0d1117")
        st.plotly_chart(fig_energy_pie, use_container_width=True)

        # Energy history chart
        if len(st.session_state.energy_history) > 2:
            en_df = pd.DataFrame(st.session_state.energy_history)
            fig_en_hist = go.Figure()
            fig_en_hist.add_trace(go.Scatter(
                x=en_df["time"], y=en_df["energy"],
                mode="lines+markers", name="Enerji (kW)",
                line=dict(color="#388bfd", width=2),
                fill="tozeroy", fillcolor="rgba(56,139,253,0.06)"
            ))
            fig_en_hist.add_trace(go.Scatter(
                x=en_df["time"], y=[e * 0.45 for e in en_df["energy"]],
                mode="lines", name="CO₂ ekvivalent (kg/saat)",
                line=dict(color="#3fb950", width=1.5, dash="dot"), yaxis="y2"
            ))
            fig_en_hist.update_layout(
                template="plotly_dark", height=250,
                title="Enerji & CO₂ Tarixi",
                yaxis2=dict(title="CO₂ (kg/saat)", overlaying="y", side="right", showgrid=False),
                margin=dict(t=30,b=15,l=0,r=40),
                legend=dict(orientation="h"),
                plot_bgcolor="#0d1117", paper_bgcolor="#0d1117"
            )
            st.plotly_chart(fig_en_hist, use_container_width=True)

    with col_en2:
        st.subheader("🌿 Enerji Qənaəti Ssenariləri")

        scenarios_energy = {
            f"Cari ({lighting_mode} işıq, {hvac_mode})": energy,
            "Yarı işıq + Yaz/Payız HVAC": energy_kw(interval, son_vaziyyat, st_data["escalators"], escalator_mode, "Yarı", "Yaz/Payız"),
            "Minimal işıq + Minimal HVAC": energy_kw(interval, son_vaziyyat, st_data["escalators"], "Normal (ikisi giriş, ikisi çıxış)", "Minimal", "Minimal"),
            f"İnterval +2 dəq ({interval+2:.0f} dəq)": energy_kw(interval+2, son_vaziyyat, st_data["escalators"], escalator_mode, lighting_mode, hvac_mode),
        }

        fig_en_comp = go.Figure(go.Bar(
            x=list(scenarios_energy.keys()),
            y=list(scenarios_energy.values()),
            marker_color=["#388bfd","#3fb950","#56d364","#d29922"],
            text=[f"{v:.1f} kW" for v in scenarios_energy.values()],
            textposition="outside"
        ))
        fig_en_comp.update_layout(
            template="plotly_dark", height=280,
            title="Ssenari Müqayisəsi",
            xaxis_tickangle=-15, margin=dict(t=30,b=50),
            plot_bgcolor="#0d1117", paper_bgcolor="#0d1117"
        )
        st.plotly_chart(fig_en_comp, use_container_width=True)

        best_case  = min(scenarios_energy.values())
        worst_case = max(scenarios_energy.values())
        save_kw    = round(worst_case - best_case, 1)
        save_cost  = round(save_kw * cost_per_kwh * 18, 2)
        save_co2   = round(save_kw * co2_per_kwh * 18, 1)

        st.metric("💡 Maks. Qənaət potensialı", f"{save_kw} kW/saat")
        st.metric("💰 Günlük xərc qənaəti", f"{save_cost} AZN")
        st.metric("🌿 Günlük CO₂ azalması", f"{save_co2} kg")

        st.divider()
        st.subheader("📊 CO₂ Tapşırığı Monitorinqi")

        # Monthly CO2 target
        monthly_target_co2 = 5000  # kg
        monthly_actual_co2 = round(daily_co2 * 30, 0)
        co2_pct = (monthly_actual_co2 / monthly_target_co2) * 100

        fig_co2_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=monthly_actual_co2,
            delta={"reference": monthly_target_co2},
            title={"text": "Aylıq CO₂ (kg)<br><span style='font-size:0.7em'>Hədəf: 5,000 kg</span>"},
            gauge={
                "axis": {"range": [0, 8000]},
                "bar": {"color": "#3fb950" if monthly_actual_co2 < monthly_target_co2 else "#f85149"},
                "steps": [{"range": [0,3000],"color":"#0a1a0a"},{"range": [3000,5000],"color":"#141a00"},{"range": [5000,8000],"color":"#1a0a0a"}],
                "threshold": {"line": {"color": "#f85149","width": 3}, "thickness": 0.8, "value": monthly_target_co2},
                "bgcolor": "#0d1117", "bordercolor": "#21262d"
            },
            number={"font": {"color": "#3fb950" if monthly_actual_co2 < monthly_target_co2 else "#f85149"}}
        ))
        fig_co2_gauge.update_layout(template="plotly_dark", height=250, margin=dict(t=30,b=15),
                                     paper_bgcolor="#0d1117")
        st.plotly_chart(fig_co2_gauge, use_container_width=True)

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 8 — INCIDENT LOG                                    ║
# ╚══════════════════════════════════════════════════════════╝
with tab8:
    st.subheader("🚨 Hadisə Jurnalı — Avtomatik & Manual")

    LEVEL_COLOR = {
        "KRİTİK":      "#f85149",
        "XƏBƏRDARLIQ": "#d29922",
        "EVAKUASİYA":  "#bc8cff",
        "ƏMƏLIYYAT":   "#388bfd",
        "SSENARI":     "#d29922",
        "FÖVQƏLADƏDİ": "#bc8cff",
        "MÜHİT":       "#3fb950",
    }

    # Filter controls
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        filter_levels = st.multiselect("Səviyyəyə görə filtr:",
            options=["KRİTİK","XƏBƏRDARLIQ","EVAKUASİYA","ƏMƏLIYYAT","SSENARI","FÖVQƏLADƏDİ","MÜHİT"],
            default=["KRİTİK","XƏBƏRDARLIQ","EVAKUASİYA","ƏMƏLIYYAT","SSENARI","FÖVQƏLADƏDİ","MÜHİT"])
    with filter_col2:
        filter_station = st.selectbox("Stansiyaya görə:", ["Hamısı"] + sorted(metro_stations.keys()))
    with filter_col3:
        show_count = st.select_slider("Göstər:", options=[10,25,50,100], value=25)

    col_log, col_stats = st.columns([1.7, 1])

    with col_log:
        filtered_log = st.session_state.incident_log
        if filter_levels:
            filtered_log = [i for i in filtered_log if i["level"] in filter_levels]
        if filter_station != "Hamısı":
            filtered_log = [i for i in filtered_log if i["station"] == filter_station]

        if filtered_log:
            for inc in filtered_log[:show_count]:
                lc      = LEVEL_COLOR.get(inc["level"], "#555")
                weather_badge = f'<span style="color:#8b949e;font-size:11px;margin-left:8px">🌤️ {inc.get("weather","")}</span>' if inc.get("weather") else ""
                st.markdown(f"""
                <div class="incident-row" style="border-left:4px solid {lc}">
                    <div style="display:flex;align-items:center;flex-wrap:wrap;gap:6px">
                        <span style="color:{lc};font-weight:700;font-size:12px">[{inc['level']}]</span>
                        <span style="color:#8b949e;font-size:11px">🕐 {inc['time']}</span>
                        <span style="color:#388bfd;font-size:12px">📍 {inc['station']}</span>
                        <span style="color:#8b949e;font-size:11px">({inc['load_pct']:.1f}%)</span>
                        {weather_badge}
                        <span style="color:#8b949e;font-size:11px">⚡ {inc.get('scenario','')}</span>
                    </div>
                    <div style="color:#cdd9e5;font-size:13px;margin-top:5px">{inc['message']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Seçilmiş filtrlərə uyğun hadisə yoxdur")

        st.divider()
        btn1, btn2, btn3, btn4 = st.columns(4)
        with btn1:
            if st.button("🗑️ Sıfırla"):
                st.session_state.incident_log = []
                st.rerun()
        with btn2:
            if st.session_state.incident_log:
                log_df2 = pd.DataFrame(st.session_state.incident_log)
                csv_data = log_df2.to_csv(index=False).encode("utf-8")
                st.download_button("📥 CSV İxrac", csv_data,
                                    f"metro_log_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                                    "text/csv")
        with btn3:
            if st.button("🔴 Yalnız Kritik"):
                st.session_state.incident_log = [i for i in st.session_state.incident_log
                                                   if i["level"] in ["KRİTİK","EVAKUASİYA","FÖVQƏLADƏDİ"]]
                st.rerun()
        with btn4:
            if st.session_state.incident_log:
                log_json = json.dumps(st.session_state.incident_log, ensure_ascii=False, indent=2)
                st.download_button("📥 JSON İxrac", log_json.encode("utf-8"),
                                    f"metro_log_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                                    "application/json")

    with col_stats:
        st.markdown("### 📊 Hadisə Statistikası")

        if st.session_state.incident_log:
            log_df3      = pd.DataFrame(st.session_state.incident_log)
            lc_counts    = log_df3["level"].value_counts()

            fig_pie = go.Figure(go.Pie(
                labels=lc_counts.index, values=lc_counts.values,
                hole=0.48,
                marker_colors=[LEVEL_COLOR.get(l, "#555") for l in lc_counts.index],
                textinfo="label+percent"
            ))
            fig_pie.update_layout(template="plotly_dark", height=220,
                                   margin=dict(t=10,b=10,l=5,r=5),
                                   showlegend=False, paper_bgcolor="#0d1117")
            st.plotly_chart(fig_pie, use_container_width=True)

            s1, s2 = st.columns(2)
            s1.metric("📋 Ümumi",    len(st.session_state.incident_log))
            s2.metric("🔴 Kritik",   len(log_df3[log_df3["level"] == "KRİTİK"]))
            if "station" in log_df3.columns and not log_df3.empty:
                most_aff = log_df3["station"].value_counts().index[0]
                s1.metric("📍 Ən çox təsirlənən", most_aff[:12])
                s2.metric("📊 Ort. Yük %", f"{log_df3['load_pct'].mean():.1f}%")

            # Time distribution if enough data
            if len(log_df3) > 5:
                station_counts = log_df3["station"].value_counts().head(5)
                fig_stn = go.Figure(go.Bar(
                    x=station_counts.values,
                    y=station_counts.index,
                    orientation="h",
                    marker_color="#388bfd",
                    text=station_counts.values, textposition="outside"
                ))
                fig_stn.update_layout(template="plotly_dark", height=200,
                                       margin=dict(t=10,b=10,l=0,r=30),
                                       title="Top 5 Stansiya",
                                       paper_bgcolor="#0d1117", plot_bgcolor="#0d1117")
                st.plotly_chart(fig_stn, use_container_width=True)
        else:
            st.info("Statistika üçün hadisə yoxdur")

        st.divider()
        st.markdown("### ➕ Manual Hadisə Əlavə Et")
        manual_stn   = st.selectbox("Stansiya:", sorted(metro_stations.keys()), key="manual_stn")
        manual_level = st.selectbox("Səviyyə:", ["XƏBƏRDARLIQ","KRİTİK","ƏMƏLIYYAT","SSENARI","MÜHİT"])
        manual_msg   = st.text_area("Hadisə təsviri:", height=70, placeholder="Nə baş verdi?")
        manual_load  = st.number_input("Yük (%):", min_value=0.0, max_value=200.0, value=doluluq_faizi, step=0.1)

        if st.button("📝 Hadisəni Qeydə Al"):
            if manual_msg.strip():
                st.session_state.incident_log.insert(0, {
                    "time":     datetime.now().strftime("%H:%M:%S"),
                    "station":  manual_stn,
                    "level":    manual_level,
                    "message":  manual_msg,
                    "load_pct": round(manual_load, 1),
                    "scenario": "Manual",
                    "weather":  weather,
                })
                st.success("✅ Hadisə qeydə alındı!")
                st.rerun()
            else:
                st.warning("Zəhmət olmasa hadisə təsvirini daxil edin")

# ============================================================
# LIVE MODE AUTO REFRESH
# ============================================================
if live_mode:
    st.session_state.live_tick += 1
    time.sleep(refresh_rate)
    st.rerun()

# ============================================================
# FOOTER
# ============================================================
st.divider()
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.caption(f"🚇 **Baku MetroTwin Pro v5.0** | Digital Twin Platform")
    st.caption(f"Standards: NFPA 130 · EN 13816 · HCM · ISO 50001")
with col_f2:
    st.caption(f"📊 Stansiya: **{stansiya_adi}** | LOS: **{los_grade}** | Doluluq: **{doluluq_faizi:.1f}%**")
    st.caption(f"⚡ Enerji: {energy} kW | 🌿 CO₂: {round(energy*co2_per_kwh,1)} kg/saat")
with col_f3:
    st.caption(f"🕐 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    st.caption(f"🔄 {'LIVE MODE' if live_mode else 'Static Mode'} | 🚃 {train_type.split('(')[0].strip()}")
