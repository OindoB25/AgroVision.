"""
AgroVision – Crop Intelligence Platform
Python / Streamlit port of agrovision.jsx
"""

import math
import time
import random
import datetime
import streamlit as st

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AgroVision",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── THEME COLORS (used in markdown / inline HTML) ────────────────────────────
C = {
    "bg":        "#0a1508",
    "bgCard":    "#111e0e",
    "bgCard2":   "#162114",
    "border":    "#243d1f",
    "border2":   "#2d4a28",
    "green":     "#7bc452",
    "greenDim":  "#4a7a30",
    "greenText": "#a8d87a",
    "muted":     "#6a8f5a",
    "text":      "#e8f5e0",
    "textDim":   "#a8c898",
    "amber":     "#EF9F27",
    "red":       "#E24B4A",
    "teal":      "#5DCAA5",
}

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    background-color: #0a1508 !important;
    color: #e8f5e0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stApp { background-color: #0a1508 !important; }
section[data-testid="stSidebar"] {
    background-color: #080f07 !important;
    border-right: 1px solid #243d1f !important;
}
.stButton>button {
    background: #7bc452; color: #0a1508; border: none; border-radius: 10px;
    font-weight: 600; font-family: 'DM Sans', sans-serif; cursor: pointer;
    transition: background .18s; letter-spacing: 0.01em;
}
.stButton>button:hover { background: #8fd45e !important; color: #0a1508 !important; }
.stTextInput>div>div>input, .stTextArea textarea {
    background: #111e0e !important; border: 1px solid #243d1f !important;
    color: #e8f5e0 !important; border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput>div>div>input:focus, .stTextArea textarea:focus {
    border-color: #7bc452 !important; box-shadow: none !important;
}
.metric-card {
    background: #111e0e; border: 1px solid #243d1f; border-radius: 12px;
    padding: 16px; text-align: center; margin-bottom: 8px;
}
.card {
    background: #111e0e; border: 1px solid #243d1f; border-radius: 14px;
    padding: 18px 20px; margin-bottom: 12px;
}
.card-alert { border-left: 4px solid #E24B4A !important; }
.card-warn  { border-left: 4px solid #EF9F27 !important; }
.card-good  { border-left: 4px solid #7bc452 !important; }
.badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 11px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase;
}
.badge-green { background: rgba(99,153,34,.14); color: #97C459; border: 1px solid rgba(99,153,34,.28); }
.badge-amber { background: rgba(186,117,23,.14); color: #FAC775; border: 1px solid rgba(186,117,23,.28); }
.badge-red   { background: rgba(226,75,74,.14);  color: #F09595; border: 1px solid rgba(226,75,74,.28); }
.badge-teal  { background: rgba(93,202,165,.12); color: #5DCAA5; border: 1px solid rgba(93,202,165,.25); }
h1, h2, h3 { font-family: 'Syne', sans-serif !important; color: #e8f5e0 !important; }
.stTabs [data-baseweb="tab-list"] {
    background: #0a1508 !important; border-radius: 10px; padding: 4px; gap: 4px;
    border: 1px solid #243d1f;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 7px !important;
    color: #6a8f5a !important; font-family: 'DM Sans', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: #1f3a1b !important; color: #7bc452 !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stProgress > div > div { background-color: #0a1508; border-radius: 4px; }
.stChatMessage { background: #111e0e !important; border: 1px solid #243d1f !important; border-radius: 14px !important; }
div[data-testid="stChatMessageContent"] p { color: #a8c898 !important; }
.stSidebar .stMarkdown p, .stSidebar .stMarkdown span { color: #a8c898 !important; }
div[data-testid="metric-container"] {
    background: #111e0e; border: 1px solid #243d1f; border-radius: 12px; padding: 16px;
}
div[data-testid="metric-container"] label { color: #6a8f5a !important; }
div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: #7bc452 !important; font-family: 'Syne', sans-serif !important; }
div[data-testid="stExpander"] {
    background: #111e0e !important; border: 1px solid #243d1f !important; border-radius: 10px !important;
}
div[data-testid="stExpander"] summary { color: #e8f5e0 !important; }
</style>
""", unsafe_allow_html=True)

# ─── MOCK DATA ────────────────────────────────────────────────────────────────
CROPS = {
    "🌽 Maize":    {"field": "A", "area": 2.4, "health": 86, "stage": "Tasseling",  "daysLeft": 42, "status": "good"},
    "🍅 Tomatoes": {"field": "B", "area": 1.1, "health": 64, "stage": "Flowering",  "daysLeft": 28, "status": "warn"},
    "🫘 Beans":    {"field": "C", "area": 0.8, "health": 41, "stage": "Vegetative", "daysLeft": 55, "status": "alert"},
    "🥬 Kale":     {"field": "D", "area": 0.6, "health": 91, "stage": "Mature",     "daysLeft": 14, "status": "good"},
}

PESTS = {
    "Fall Armyworm": {
        "severity": "HIGH", "affected": ["🌽 Maize"], "confidence": 89,
        "symptoms": "Ragged holes in leaves, frass deposits, damaged tassels",
        "action": "Spray immediately in early morning or evening. Wear PPE.",
        "pesticides": [
            {"name": "Emamectin Benzoate 1.9% EC", "dose": "200ml/20L water", "freq": "Every 7 days", "cost": 650},
            {"name": "Chlorpyrifos 48% EC", "dose": "30ml/20L water", "freq": "Every 10 days", "cost": 480},
        ],
    },
    "Early Blight": {
        "severity": "MEDIUM", "affected": ["🍅 Tomatoes"], "confidence": 74,
        "symptoms": "Dark brown spots with yellow halos on lower leaves",
        "action": "Remove infected leaves, improve air circulation.",
        "pesticides": [
            {"name": "Mancozeb 80% WP", "dose": "40g/20L water", "freq": "Every 7 days", "cost": 320},
            {"name": "Copper Oxychloride 50% WP", "dose": "60g/20L water", "freq": "Every 10 days", "cost": 280},
        ],
    },
    "Bean Stem Maggot": {
        "severity": "HIGH", "affected": ["🫘 Beans"], "confidence": 82,
        "symptoms": "Yellowing seedlings, wilted shoots, maggots at stem base",
        "action": "Apply soil drench at base of plants.",
        "pesticides": [
            {"name": "Dimethoate 40% EC", "dose": "20ml/20L water", "freq": "Every 7 days", "cost": 380},
        ],
    },
    "Aphids": {
        "severity": "LOW", "affected": ["🥬 Kale", "🍅 Tomatoes"], "confidence": 61,
        "symptoms": "Clusters of small green/black insects on young shoots",
        "action": "Use yellow sticky traps. Spray neem extract first.",
        "pesticides": [
            {"name": "Cypermethrin 10% EC", "dose": "30ml/20L water", "freq": "Every 7 days", "cost": 250},
        ],
    },
}

SPRAY_SCHEDULE = [
    {"crop": "🌽 Maize",    "pesticide": "Emamectin Benzoate 1.9% EC", "dose": "200ml/20L", "daysUntil": 0, "cost": 650,  "status": "OVERDUE"},
    {"crop": "🍅 Tomatoes", "pesticide": "Mancozeb 80% WP",            "dose": "40g/20L",   "daysUntil": 2, "cost": 320,  "status": "UPCOMING"},
    {"crop": "🫘 Beans",    "pesticide": "Dimethoate 40% EC",           "dose": "20ml/20L",  "daysUntil": 1, "cost": 380,  "status": "UPCOMING"},
    {"crop": "🌽 Maize",    "pesticide": "Chlorpyrifos 48% EC",         "dose": "30ml/20L",  "daysUntil": 5, "cost": 480,  "status": "SCHEDULED"},
]

HARDWARE = [
    {"name": "Raspberry Pi 4 (4GB)",   "icon": "🖥️",  "cost": "KSh 12,000", "role": "AI Controller",        "port": "Primary"},
    {"name": "Arduino Mega 2560",       "icon": "🔌",  "cost": "KSh 3,500",  "role": "Sensor I/O Hub",       "port": "/dev/ttyUSB0"},
    {"name": "Arduino Uno",             "icon": "⚙️",  "cost": "KSh 2,500",  "role": "Mechanical Control",   "port": "/dev/ttyUSB1"},
    {"name": "Soil Moisture Sensor",    "icon": "💧",  "cost": "KSh 800",    "role": "Soil Water Content",   "port": "A0 (Mega)"},
    {"name": "Soil pH Sensor",          "icon": "🧪",  "cost": "KSh 4,000",  "role": "Soil Acidity",         "port": "A1 (Mega)"},
    {"name": "DHT11 Temp/Humidity",     "icon": "🌡️", "cost": "KSh 800",    "role": "Air Temp & Humidity",  "port": "D2 (Mega)"},
    {"name": "Ultrasonic HC-SR04",      "icon": "📡",  "cost": "KSh 500",    "role": "Obstacle Detection",   "port": "D22 (Mega)"},
    {"name": "GPS Neo-6M/7M",           "icon": "🛰️", "cost": "KSh 3,000",  "role": "Field Navigation",     "port": "Serial1"},
    {"name": "Raspberry Pi Camera",     "icon": "📷",  "cost": "KSh 4,000",  "role": "CV Crop Detection",    "port": "CSI"},
    {"name": "ESP8266 WiFi Module",     "icon": "📶",  "cost": "KSh 1,000",  "role": "Robot ↔ SaaS Link",   "port": "D10 (Mega)"},
    {"name": "DC Gear Motors ×4",       "icon": "⚡",  "cost": "KSh 14,000", "role": "Field Navigation",     "port": "L298N Driver"},
    {"name": "Servo Motors ×2",         "icon": "🔧",  "cost": "KSh 2,000",  "role": "Camera Positioning",   "port": "D9/D10 Uno"},
    {"name": "Solar Panel + Battery",   "icon": "🔋",  "cost": "KSh 7,000",  "role": "Power System",         "port": "Buck Converter"},
    {"name": "Chassis + Wheels",        "icon": "🏗️", "cost": "KSh 11,000", "role": "Robot Frame",          "port": "Assembly"},
    {"name": "Motor Drivers L298N×2",   "icon": "🚗",  "cost": "KSh 2,000",  "role": "Motor Control",        "port": "Mega GPIO"},
]

# ─── SENSOR SIMULATION ────────────────────────────────────────────────────────
def read_sensors():
    t = time.time()
    return {
        "temperature":    round(22 + 5 * math.sin(t / 3600) + (random.random() - 0.5), 1),
        "humidity":       round(60 + 15 * math.sin(t / 7200) + (random.random() * 2 - 1), 1),
        "soilMoisture":   round(45 + 20 * math.sin(t / 5000) + (random.random() * 4 - 2), 1),
        "soilPh":         round(6.2 + 0.8 * math.sin(t / 10000) + (random.random() * 0.2 - 0.1), 1),
        "lightIntensity": round(600 + 300 * abs(math.sin(t / 3600)) + (random.random() * 40 - 20)),
        "obstacleDist":   round(30 + random.random() * 170, 1),
        "gpsLat":         round(-1.2921 + (random.random() * 0.002 - 0.001), 4),
        "gpsLon":         round(36.8219 + (random.random() * 0.002 - 0.001), 4),
        "batteryPct":     round(85 + 5 * math.sin(t / 20000), 1),
    }

def predict_yield(crop_name, health, sensors):
    base = {"🌽 Maize": 3.5, "🍅 Tomatoes": 25.0, "🫘 Beans": 1.2, "🥬 Kale": 8.0}.get(crop_name, 2.0)
    mf = 1 if 50 <= sensors["soilMoisture"] <= 70 else 0.8
    pf = 1 if 6 <= sensors["soilPh"] <= 7 else 0.85
    tf = 1 if 18 <= sensors["temperature"] <= 30 else 0.85
    return round(base * (health / 100) * mf * pf * tf, 2), base

def generate_recs(sensors):
    recs = []
    if sensors["soilMoisture"] < 40:
        recs.append({"priority": "URGENT", "cat": "Irrigation", "title": "Irrigate Fields B & C Now",
                     "detail": f"Soil moisture critically low at {sensors['soilMoisture']}% (optimal 50–70%). Apply 25mm immediately.",
                     "time": "Within 2 hours", "hw": "Soil Moisture Sensor → Arduino Mega"})
    elif sensors["soilMoisture"] > 75:
        recs.append({"priority": "IMPORTANT", "cat": "Drainage", "title": "Reduce Irrigation — Waterlogging Risk",
                     "detail": f"Soil moisture at {sensors['soilMoisture']}% — promotes root rot. Suspend irrigation 48 hours.",
                     "time": "Within 6 hours", "hw": "Soil Moisture Sensor → Arduino Mega"})
    if sensors["soilPh"] < 5.8:
        recs.append({"priority": "IMPORTANT", "cat": "Soil Amendment", "title": "Apply Agricultural Lime to Field C",
                     "detail": f"Soil pH at {sensors['soilPh']} (optimal 6.0–7.0). Apply 2 tonnes/ha agricultural lime.",
                     "time": "Within 1 week", "hw": "Soil pH Sensor → Arduino Mega"})
    if sensors["temperature"] > 32:
        recs.append({"priority": "IMPORTANT", "cat": "Heat Management", "title": "Apply Shade Nets — Heat Stress Alert",
                     "detail": f"Temperature at {sensors['temperature']}°C. Tomatoes and beans at risk. Erect shade nets over Fields B & C.",
                     "time": "Today", "hw": "DHT11 → Arduino Mega"})
    if sensors["humidity"] > 85:
        recs.append({"priority": "URGENT", "cat": "Disease Prevention", "title": "Spray Fungicide — High Humidity Risk",
                     "detail": f"Humidity at {sensors['humidity']}% creates ideal fungal disease conditions. Apply Mancozeb 80% WP.",
                     "time": "Within 24 hours", "hw": "DHT11 → Arduino Mega"})
    recs.append({"priority": "ROUTINE", "cat": "Fertilisation", "title": "Top-Dress Maize with CAN Fertiliser",
                 "detail": "Field A maize at tasseling — apply CAN at 150kg/ha to boost grain filling.",
                 "time": "This week", "hw": "GPS Module → Field mapping"})
    recs.append({"priority": "ROUTINE", "cat": "Scouting", "title": "Deploy Robot for Field Scouting",
                 "detail": "Schedule autonomous robot scouting across all 4 fields for AI pest/disease analysis.",
                 "time": "Tomorrow 6:00 AM", "hw": "Raspberry Pi Camera + GPS + DC Motors"})
    return recs

def ai_advisor_response(question, sensors):
    q = question.lower()
    if any(w in q for w in ["water", "irrigat", "moisture", "dry"]):
        if sensors["soilMoisture"] < 40:
            return (f"🚿 **Irrigation Needed Urgently!**\n\nSoil moisture is at **{sensors['soilMoisture']}%** "
                    f"(optimal: 50–70%). Irrigate Fields B and C immediately with at least **25mm of water**. "
                    f"The robot can activate the irrigation relay via Arduino Mega (relay on D30). Re-check in **2 hours**.")
        return (f"💧 Soil moisture is currently **{sensors['soilMoisture']}%** — within acceptable range (50–70%). "
                f"No irrigation needed. Schedule next check in **6 hours**.")
    if any(w in q for w in ["spray", "pest", "disease", "armyworm", "blight", "aphid"]):
        return ("🌿 **Pest & Disease Management:**\n\nCurrently detected threats:\n"
                "- **Fall Armyworm** (Field A - Maize, 89% confidence) → Spray **Emamectin Benzoate 1.9% EC** at 200ml/20L. Best time: **early morning or evening**.\n"
                "- **Early Blight** (Field B - Tomatoes, 74%) → Apply **Mancozeb 80% WP** at 40g/20L every 7 days.\n"
                "- **Bean Stem Maggot** (Field C - Beans, 82%) → Drench with **Dimethoate 40% EC** at 20ml/20L.\n\n"
                "⚠️ Always wear PPE and observe pre-harvest intervals.")
    if any(w in q for w in ["yield", "harvest", "predict", "production"]):
        lines = ["📊 **Yield Predictions (current conditions):**\n"]
        for crop, info in CROPS.items():
            pred, opt = predict_yield(crop, info["health"], sensors)
            lines.append(f"- **{crop}**: {pred} tonnes/ha ({round((pred/opt)*100)}% of optimal {opt})")
        lines.append("\n💡 Improving soil moisture and pH will boost yields by an estimated **8–15%**.")
        return "\n".join(lines)
    if any(w in q for w in ["ph", "acid", "alkalin", "lime", "soil"]):
        ph = sensors["soilPh"]
        if ph < 5.8:
            ph_note = "⚠️ pH is LOW — apply **2 tonnes/ha agricultural lime** and retest in 4 weeks."
        elif ph > 7.0:
            ph_note = "⚠️ pH is HIGH — apply **elemental sulphur at 200kg/ha**."
        else:
            ph_note = "✅ pH is within optimal range."
        return (f"🧪 **Soil Analysis:**\n\nCurrent pH: **{ph}** (optimal: 6.0–7.0)\n\n{ph_note}\n\n"
                f"Soil moisture: **{sensors['soilMoisture']}%**")
    if any(w in q for w in ["temp", "hot", "cold", "heat", "weather"]):
        notes = []
        if sensors["temperature"] > 32:
            notes.append("⚠️ High temperature — risk of heat stress on tomatoes. Apply shade nets.")
        if sensors["humidity"] > 80:
            notes.append("⚠️ High humidity — fungal disease risk. Apply preventive fungicide.")
        if not notes:
            notes.append("✅ Conditions are within optimal range for all crops.")
        return (f"🌡️ **Environmental Conditions:**\n\nTemperature: **{sensors['temperature']}°C** (optimal crops: 18–30°C)\n"
                f"Humidity: **{sensors['humidity']}%** (optimal: 50–75%)\n\n" + "\n".join(notes))
    if any(w in q for w in ["robot", "motor", "camera", "gps", "autonom"]):
        return (f"🤖 **Robot Operations:**\n\nThe agri-robot is **online** with all systems nominal:\n"
                f"- 📷 Camera: Active — last scan 45 mins ago\n"
                f"- 🛰️ GPS: Signal acquired ({sensors['gpsLat']}, {sensors['gpsLon']})\n"
                f"- ⚡ Motors: Ready — battery at {sensors['batteryPct']}%\n"
                f"- 📶 ESP8266: Connected to SaaS platform\n\n"
                f"**Available Commands:**\n- Initiate field scan across all 4 fields\n"
                f"- Target spray to GPS coordinates\n- Return to base for recharging")
    return (f"👋 I'm your **AgroVision AI Advisor**. Current farm status:\n\n"
            f"- 🌡️ Temp: {sensors['temperature']}°C | 💧 Humidity: {sensors['humidity']}%\n"
            f"- 🌱 Soil Moisture: {sensors['soilMoisture']}% | 🧪 pH: {sensors['soilPh']}\n"
            f"- 🔋 Robot Battery: {sensors['batteryPct']}%\n\n"
            f"Ask me about: **watering**, **pesticides**, **yield prediction**, **soil pH**, **fertilisation**, or **robot control**.")

def format_date(days_ahead):
    d = datetime.date.today() + datetime.timedelta(days=days_ahead)
    return d.strftime("%d %b %Y")

def badge(text, variant="green"):
    return f'<span class="badge badge-{variant}">{text}</span>'

def health_color(status):
    return {"good": C["green"], "warn": C["amber"], "alert": C["red"]}.get(status, C["green"])

def progress_bar_html(pct, color, height=6):
    return (f'<div style="background:#0a1508;border-radius:4px;overflow:hidden;height:{height}px;">'
            f'<div style="width:{pct}%;height:100%;background:{color};border-radius:4px;transition:width .6s ease;"></div></div>')

# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None
if "sensors" not in st.session_state:
    st.session_state.sensors = read_sensors()
if "chat" not in st.session_state:
    st.session_state.chat = []
if "users_db" not in st.session_state:
    st.session_state.users_db = []

# ─── AUTH ─────────────────────────────────────────────────────────────────────
# Inline SVG logo string (no f-string needed — static)
_LOGO_SVG_INLINE = (
    '<svg width="64" height="64" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<polygon points="28,3 51,16 51,40 28,53 5,40 5,16" stroke="#2d4a28" stroke-width="1.5" fill="none"/>'
    '<polygon points="28,10 46,20 46,36 28,46 10,36 10,20" stroke="#3a5e34" stroke-width="1" fill="none"/>'
    '<path d="M28 13 C40 18 42 30 28 43 C14 30 16 18 28 13Z" fill="#7bc452"/>'
    '<line x1="28" y1="13" x2="28" y2="43" stroke="#0d1a0a" stroke-width="1.4" stroke-linecap="round"/>'
    '<line x1="28" y1="22" x2="35" y2="27" stroke="#0d1a0a" stroke-width="0.9" stroke-linecap="round" opacity="0.55"/>'
    '<line x1="28" y1="22" x2="21" y2="27" stroke="#0d1a0a" stroke-width="0.9" stroke-linecap="round" opacity="0.55"/>'
    '<line x1="28" y1="30" x2="36" y2="34" stroke="#0d1a0a" stroke-width="0.9" stroke-linecap="round" opacity="0.55"/>'
    '<line x1="28" y1="30" x2="20" y2="34" stroke="#0d1a0a" stroke-width="0.9" stroke-linecap="round" opacity="0.55"/>'
    '<line x1="10" y1="28" x2="46" y2="28" stroke="#5DCAA5" stroke-width="0.9" opacity="0.55"/>'
    '<circle cx="38" cy="28" r="2.8" fill="#5DCAA5"/>'
    '<circle cx="28" cy="3" r="2" fill="#3a5e34"/>'
    '<circle cx="51" cy="28" r="2" fill="#3a5e34"/>'
    '<circle cx="28" cy="53" r="2" fill="#3a5e34"/>'
    '<circle cx="5" cy="28" r="2" fill="#3a5e34"/>'
    '</svg>'
)

_LOGO_SMALL_SVG = (
    '<svg width="38" height="38" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<polygon points="28,3 51,16 51,40 28,53 5,40 5,16" stroke="#2d4a28" stroke-width="1.5" fill="none"/>'
    '<polygon points="28,10 46,20 46,36 28,46 10,36 10,20" stroke="#3a5e34" stroke-width="1" fill="none"/>'
    '<path d="M28 13 C40 18 42 30 28 43 C14 30 16 18 28 13Z" fill="#7bc452"/>'
    '<line x1="28" y1="13" x2="28" y2="43" stroke="#0d1a0a" stroke-width="1.4" stroke-linecap="round"/>'
    '<line x1="28" y1="22" x2="35" y2="27" stroke="#0d1a0a" stroke-width="0.9" stroke-linecap="round" opacity="0.55"/>'
    '<line x1="28" y1="22" x2="21" y2="27" stroke="#0d1a0a" stroke-width="0.9" stroke-linecap="round" opacity="0.55"/>'
    '<line x1="28" y1="30" x2="36" y2="34" stroke="#0d1a0a" stroke-width="0.9" stroke-linecap="round" opacity="0.55"/>'
    '<line x1="28" y1="30" x2="20" y2="34" stroke="#0d1a0a" stroke-width="0.9" stroke-linecap="round" opacity="0.55"/>'
    '<line x1="10" y1="28" x2="46" y2="28" stroke="#5DCAA5" stroke-width="0.9" opacity="0.55"/>'
    '<circle cx="38" cy="28" r="2.8" fill="#5DCAA5"/>'
    '<circle cx="28" cy="3" r="2" fill="#3a5e34"/>'
    '<circle cx="51" cy="28" r="2" fill="#3a5e34"/>'
    '<circle cx="28" cy="53" r="2" fill="#3a5e34"/>'
    '<circle cx="5" cy="28" r="2" fill="#3a5e34"/>'
    '</svg>'
)

def auth_screen():
    # Extra CSS just for the auth page — polished tab pills, no Streamlit radio
    st.markdown("""
    <style>
    /* ── Auth page overrides ── */
    .auth-page-wrap {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px 20px 60px;
    }
    /* Subtle grid overlay */
    .auth-page-wrap::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(45,74,40,.12) 1px, transparent 1px),
            linear-gradient(90deg, rgba(45,74,40,.12) 1px, transparent 1px);
        background-size: 48px 48px;
        pointer-events: none;
        z-index: 0;
    }
    /* Radial glow */
    .auth-page-wrap::after {
        content: '';
        position: fixed;
        width: 600px; height: 400px;
        top: -100px; left: 50%;
        transform: translateX(-50%);
        background: radial-gradient(ellipse, rgba(123,196,82,.07) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }
    .auth-inner { position: relative; z-index: 1; width: 100%; max-width: 440px; }

    /* Logo lockup — no border/frame */
    .auth-logo-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 18px;
        margin-bottom: 10px;
    }
    .auth-wordmark-agro {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 2.6rem;
        color: #e8f5e0;
        letter-spacing: -2px;
        line-height: 1;
    }
    .auth-wordmark-vision {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 2.6rem;
        color: #7bc452;
        letter-spacing: -2px;
        line-height: 1;
    }
    .auth-tagline {
        font-size: 10px;
        letter-spacing: 4px;
        color: #8ab870;
        text-transform: uppercase;
        margin-top: 5px;
    }
    /* Divider line below logo */
    .auth-divider {
        width: 48px; height: 1px;
        background: linear-gradient(90deg, transparent, #2d4a28, transparent);
        margin: 18px auto 28px;
    }

    /* Tab toggle pills */
    .auth-tabs {
        display: flex;
        gap: 0;
        background: #0d150a;
        border: 1px solid #1f3a1b;
        border-radius: 12px;
        padding: 4px;
        margin-bottom: 24px;
    }
    .auth-tab {
        flex: 1;
        text-align: center;
        padding: 10px 0;
        font-family: 'DM Sans', sans-serif;
        font-size: 13px;
        font-weight: 500;
        color: #4a6a3a;
        border-radius: 9px;
        cursor: pointer;
        border: none;
        background: transparent;
        transition: all .2s;
        letter-spacing: .02em;
    }
    .auth-tab.active {
        background: #1a2e14;
        color: #7bc452;
        box-shadow: 0 1px 6px rgba(0,0,0,.35);
    }
    .auth-tab:hover:not(.active) { color: #a8c898; }

    /* Card */
    .auth-card {
        background: #0d150a;
        border: 1px solid #1f3a1b;
        border-radius: 16px;
        padding: 32px 36px 28px;
    }

    /* Demo hint */
    .auth-hint {
        background: transparent;
        border: 1px solid #1a2c16;
        border-radius: 10px;
        padding: 12px 16px;
        margin-top: 14px;
        font-size: 12px;
        color: #4a6a3a;
        display: flex;
        align-items: flex-start;
        gap: 8px;
    }
    /* Footer */
    .auth-footer {
        text-align: center;
        margin-top: 22px;
        font-size: 11px;
        color: #6a8f5a;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Mode toggle stored in session state ──
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "signin"

    # ── Logo header ──
    st.markdown(
        '<div class="auth-page-wrap"><div class="auth-inner">'
        '<div class="auth-logo-wrap">'
        + _LOGO_SVG_INLINE +
        '<div>'
        '<div><span class="auth-wordmark-agro">Agro</span>'
        '<span class="auth-wordmark-vision">Vision</span></div>'
        '<div class="auth-tagline">Farm Smarter, Grow Further</div>'
        '</div></div>'
        '<div class="auth-divider"></div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    # ── Tab toggle buttons ──
    signin_bg  = "#1a2e14" if st.session_state.auth_mode == "signin"   else "#0d150a"
    signin_col = "#7bc452" if st.session_state.auth_mode == "signin"   else "#6a8f5a"
    signup_bg  = "#1a2e14" if st.session_state.auth_mode == "register" else "#0d150a"
    signup_col = "#7bc452" if st.session_state.auth_mode == "register" else "#6a8f5a"

    st.markdown(f"""
    <style>
    /* Sign In pill */
    div[data-testid="column"]:nth-of-type(2) div[data-testid="column"]:nth-of-type(1) .stButton > button {{
        background: {signin_bg} !important;
        color: {signin_col} !important;
        border: 1px solid #1f3a1b !important;
        border-right: none !important;
        border-radius: 10px 0 0 10px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        padding: 10px 0 !important;
        letter-spacing: 0.02em !important;
        transition: all .2s !important;
    }}
    div[data-testid="column"]:nth-of-type(2) div[data-testid="column"]:nth-of-type(1) .stButton > button:hover {{
        color: #a8d87a !important;
        background: #1f3a1b !important;
    }}
    /* Create Account pill */
    div[data-testid="column"]:nth-of-type(2) div[data-testid="column"]:nth-of-type(2) .stButton > button {{
        background: {signup_bg} !important;
        color: {signup_col} !important;
        border: 1px solid #1f3a1b !important;
        border-left: none !important;
        border-radius: 0 10px 10px 0 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        padding: 10px 0 !important;
        letter-spacing: 0.02em !important;
        transition: all .2s !important;
    }}
    div[data-testid="column"]:nth-of-type(2) div[data-testid="column"]:nth-of-type(2) .stButton > button:hover {{
        color: #a8d87a !important;
        background: #1f3a1b !important;
    }}
    /* Submit button */
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stVerticalBlock"] > div:last-child .stButton > button,
    button[kind="primary"] {{
        background: #7bc452 !important;
        color: #0a1508 !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        padding: 12px 0 !important;
    }}
    /* Input labels — light green so they're readable */
    .stTextInput label, .stTextInput label p {{
        color: #c8e6b0 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        margin-bottom: 2px !important;
    }}
    /* Placeholder text — lighter so it's visible */
    .stTextInput input::placeholder {{
        color: #6a9a54 !important;
        opacity: 1 !important;
    }}
    /* Typed text inside inputs */
    .stTextInput input {{
        color: #dff0d0 !important;
    }}
    /* Crush the giant gaps Streamlit adds between each input */
    .stTextInput {{
        margin-bottom: -14px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        t1, t2 = st.columns(2)
        with t1:
            if st.button("Sign In", use_container_width=True, key="tab_signin"):
                st.session_state.auth_mode = "signin"
                st.rerun()
        with t2:
            if st.button("Create Account", use_container_width=True, key="tab_register"):
                st.session_state.auth_mode = "register"
                st.rerun()

    mode = st.session_state.auth_mode

    # ── Form ──
    _, mid2, _ = st.columns([1, 2, 1])
    with mid2:
        # Wrap in a subtle card
        st.markdown('<div style="background:#0d150a;border:1px solid #1f3a1b;border-radius:16px;padding:16px 32px 18px;margin-top:6px;">', unsafe_allow_html=True)

        if mode == "register":
            name  = st.text_input("Full Name",        placeholder="e.g. John Mwangi")
            farm  = st.text_input("Farm Name",        placeholder="e.g. Mwangi Family Farm")
            phone = st.text_input("Phone Number",     placeholder="e.g. +254 712 345 678")
        email    = st.text_input("Email Address",     placeholder="you@example.com")
        password = st.text_input("Password",          type="password", placeholder="Min. 6 characters")
        if mode == "register":
            confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat your password")

        btn_label = "Sign In →" if mode == "signin" else "Create Account →"
        if st.button(btn_label, use_container_width=True, key="auth_submit"):
            errors = []
            if mode == "register":
                if not name.strip():  errors.append("Full name is required")
                if not farm.strip():  errors.append("Farm name is required")
                if not phone.strip(): errors.append("Phone number is required")
                if password != confirm: errors.append("Passwords do not match")
            if "@" not in email:     errors.append("Valid email required")
            if len(password) < 6:   errors.append("Password must be at least 6 characters")

            if errors:
                for e in errors:
                    st.error(e)
            elif mode == "register":
                if any(u["email"] == email for u in st.session_state.users_db):
                    st.error("Email already registered")
                else:
                    user = {"id": int(time.time()), "name": name, "email": email,
                            "phone": phone, "farm": farm}
                    st.session_state.users_db.append({**user, "password": password})
                    st.session_state.user = user
                    st.rerun()
            else:
                match = next((u for u in st.session_state.users_db
                              if u["email"] == email and u["password"] == password), None)
                if not match:
                    st.error("Invalid email or password")
                else:
                    st.session_state.user = {k: v for k, v in match.items() if k != "password"}
                    st.rerun()

        if mode == "signin":
            st.markdown("""
            <div style="margin-top:16px;padding:11px 14px;border:1px solid #2d4a28;
                 border-radius:10px;display:flex;align-items:flex-start;gap:8px;background:rgba(45,74,40,.08);">
              <span style="font-size:14px;flex-shrink:0;">🔑</span>
              <div style="font-size:12px;color:#a8c898;line-height:1.6;">
                Register a new account first, then sign in with those credentials.
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div style="text-align:center;margin-top:20px;font-size:11px;'
            'color:#6a8f5a;letter-spacing:1px;">'
            '"Farm Smarter, Grow Further." &middot; Kenya &middot; KSh 67,800 prototype'
            '</div>',
            unsafe_allow_html=True,
        )

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
def render_sidebar(sensors, user):
    with st.sidebar:
        st.markdown(
            '<div style="padding:12px 0 8px;display:flex;align-items:center;gap:12px;">'
            + _LOGO_SMALL_SVG +
            '<div>'
            '<div style="line-height:1.1;">'
            '<span style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:1.25rem;color:#e8f5e0;letter-spacing:-0.5px;">Agro</span>'
            '<span style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:1.25rem;color:#7bc452;letter-spacing:-0.5px;">Vision</span>'
            '</div>'
            '<div style="font-size:9px;letter-spacing:2.5px;color:#6a8f5a;text-transform:uppercase;margin-top:3px;">Farm Smarter, Grow Further</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown("""
        <div style="display:flex;align-items:center;font-size:12px;color:#7bc452;margin:12px 0 8px;">
            <span style="display:inline-block;width:7px;height:7px;background:#7bc452;border-radius:50%;margin-right:6px;"></span>
            LIVE SENSORS
        </div>
        """, unsafe_allow_html=True)

        # Sensor quick stats grid
        col1, col2 = st.columns(2)
        stats = [
            ("🌡️", "Temp", f"{sensors['temperature']}°C"),
            ("💧", "Humidity", f"{sensors['humidity']}%"),
            ("🌱", "Moisture", f"{sensors['soilMoisture']}%"),
            ("🧪", "pH", str(sensors["soilPh"])),
            ("🔋", "Battery", f"{sensors['batteryPct']}%"),
            ("☀️", "Light", f"{sensors['lightIntensity']}lx"),
        ]
        for i, (icon, label, val) in enumerate(stats):
            col = col1 if i % 2 == 0 else col2
            with col:
                st.markdown(f"""
                <div style="background:#111e0e;border:1px solid #243d1f;border-radius:8px;padding:8px 10px;margin-bottom:6px;">
                    <div style="font-size:14px;">{icon}</div>
                    <div style="font-size:15px;font-family:'Syne',sans-serif;font-weight:700;color:#7bc452;line-height:1.1;">{val}</div>
                    <div style="font-size:10px;color:#6a8f5a;text-transform:uppercase;letter-spacing:.06em;">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        obs = sensors["obstacleDist"]
        obs_color = C["amber"] if obs < 50 else C["teal"]
        obs_text = f"⚠️ Obstacle at {obs}cm" if obs < 50 else f"✅ Clear — {obs:.0f}cm ahead"
        gps_icon = "\U0001f6f0\ufe0f"
        st.markdown(f"""
        <div style="background:#111e0e;border:1px solid #243d1f;border-radius:8px;padding:8px 10px;font-size:12px;color:#a8c898;margin-bottom:4px;">
            {gps_icon} <span style="color:#6a8f5a;">GPS:</span> {sensors['gpsLat']}, {sensors['gpsLon']}
        </div>
        <div style="background:#111e0e;border:1px solid #243d1f;border-radius:8px;padding:8px 10px;font-size:12px;color:{obs_color};margin-bottom:12px;">
            {obs_text}
        </div>
        <hr style="border-color:#243d1f;margin:8px 0 12px;">
        """, unsafe_allow_html=True)

        if st.button("🔄 Refresh Sensors", use_container_width=True):
            st.session_state.sensors = read_sensors()
            st.rerun()

        st.markdown("<hr style='border-color:#243d1f;margin:12px 0;'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#111e0e;border:1px solid #243d1f;border-radius:10px;padding:12px 14px;margin-bottom:10px;">
            <div style="font-size:13px;font-weight:500;color:#e8f5e0;">{user['name']}</div>
            <div style="font-size:11px;color:#6a8f5a;margin-top:2px;">{user.get('farm','My Farm')}</div>
            <div style="font-size:11px;color:#6a8f5a;">{user['email']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Sign Out", use_container_width=True):
            st.session_state.user = None
            st.rerun()

# ─── TABS ─────────────────────────────────────────────────────────────────────
def tab_overview(sensors, user):
    first_name = user["name"].split()[0]
    today = datetime.date.today().strftime("%A, %d %B")
    greeting = f"Good morning, {first_name} \U0001f44b"
    status_line = f"Farm status for {today}"
    st.markdown(f"""
    <div style="margin-bottom:24px;">
        <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#e8f5e0;">{greeting}</div>
        <div style="color:#6a8f5a;margin-top:4px;font-size:14px;">{status_line}</div>
    </div>
    """, unsafe_allow_html=True)

    avg_health = round(sum(c["health"] for c in CROPS.values()) / len(CROPS))
    alerts_count = sum(1 for c in CROPS.values() if c["status"] == "alert")

    kpi_color = C["green"] if avg_health > 70 else C["amber"]
    alert_color = C["red"] if alerts_count > 0 else C["green"]
    moist_color = C["red"] if sensors["soilMoisture"] < 40 else (C["amber"] if sensors["soilMoisture"] > 75 else C["green"])

    cols = st.columns(6)
    kpis = [
        ("🌱", "Avg Health",    f"{avg_health}%",              kpi_color),
        ("🗺️","Active Fields", "4",                            C["teal"]),
        ("⚠️","Alerts",        str(alerts_count),              alert_color),
        ("🌡️","Temperature",   f"{sensors['temperature']}°C", C["text"]),
        ("💧","Soil Moisture",  f"{sensors['soilMoisture']}%", moist_color),
        ("🔋","Battery",        f"{sensors['batteryPct']}%",   C["green"]),
    ]
    for col, (icon, label, val, color) in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:22px;margin-bottom:4px;">{icon}</div>
                <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:{color};line-height:1;">{val}</div>
                <div style="font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:#6a8f5a;margin-top:4px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1rem;font-weight:700;margin-bottom:12px;">Field Status</div>', unsafe_allow_html=True)
    cols2 = st.columns(4)
    for col, (name, info) in zip(cols2, CROPS.items()):
        color = health_color(info["status"])
        badge_v = {"good": "green", "warn": "amber", "alert": "red"}[info["status"]]
        badge_label = {"good": "HEALTHY", "warn": "WATCH", "alert": "ALERT"}[info["status"]]
        card_class = f"card card-{info['status']}"
        with col:
            st.markdown(f"""
            <div class="{card_class}">
                <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:10px;">
                    <span style="font-family:'Syne',sans-serif;font-weight:700;">{name}</span>
                    {badge(badge_label, badge_v)}
                </div>
                <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:{color};">{info['health']}</div>
                <div style="font-size:11px;color:#6a8f5a;margin-bottom:8px;">Health Score</div>
                {progress_bar_html(info['health'], color, 4)}
                <div style="font-size:12px;color:#a8c898;margin-top:8px;">Field {info['field']} &middot; {info['area']}ha &middot; {info['daysLeft']}d to harvest</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1rem;font-weight:700;margin-bottom:12px;">Active Pest Alerts</div>', unsafe_allow_html=True)
    for name, p in list(PESTS.items())[:3]:
        sev = p["severity"]
        card_cls = "alert" if sev == "HIGH" else "warn" if sev == "MEDIUM" else "good"
        bdg_v = "red" if sev == "HIGH" else "amber" if sev == "MEDIUM" else "green"
        st.markdown(f"""
        <div class="card card-{card_cls}" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
            <div>
                <div style="font-weight:500;margin-bottom:2px;">{name}</div>
                <div style="font-size:12px;color:#6a8f5a;">{', '.join(p['affected'])} &middot; {p['confidence']}% confidence</div>
            </div>
            {badge(sev, bdg_v)}
        </div>
        """, unsafe_allow_html=True)

def tab_crop_health(sensors):
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.4rem;font-weight:800;margin-bottom:4px;">Field Health Overview</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#6a8f5a;font-size:13px;margin-bottom:20px;">Sensor data from Soil Moisture, pH, DHT11, GPS, Camera</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    for col, (name, info) in zip(cols, CROPS.items()):
        color = health_color(info["status"])
        badge_v = {"good": "green", "warn": "amber", "alert": "red"}[info["status"]]
        badge_label = {"good": "HEALTHY", "warn": "WATCH", "alert": "ALERT"}[info["status"]]
        with col:
            st.markdown(f"""
            <div class="card card-{info['status']}">
                {badge(badge_label, badge_v)}
                <div style="font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700;display:block;margin-top:12px;">{name}</div>
                <div style="font-size:11px;color:#6a8f5a;text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px;">Field {info['field']} &middot; {info['area']}ha</div>
                <div style="font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:{color};">{info['health']}</div>
                <div style="font-size:11px;color:#6a8f5a;margin-bottom:8px;">Health Score</div>
                {progress_bar_html(info['health'], color, 5)}
                <div style="margin-top:10px;font-size:13px;color:#a8c898;">📅 Stage: {info['stage']}<br>⏳ {info['daysLeft']} days to harvest</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:#243d1f;'>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.1rem;font-weight:700;margin-bottom:16px;">📈 Health Trend (Last 7 Days)</div>', unsafe_allow_html=True)

    cols2 = st.columns(4)
    trend_colors = {"🌽 Maize": C["green"], "🍅 Tomatoes": C["amber"], "🫘 Beans": C["red"], "🥬 Kale": C["teal"]}
    for col, (name, info) in zip(cols2, CROPS.items()):
        trend = [max(10, min(100, info["health"] + round(random.random() * 13 - 8) - int(i * 0.3)))
                 for i in range(6, -1, -1)]
        trend[-1] = info["health"]
        color = trend_colors.get(name, C["green"])
        with col:
            # Build simple sparkline SVG
            min_v, max_v = min(trend), max(trend)
            rng = max_v - min_v or 1
            w, h = 200, 55
            pts = " ".join(f"{(i/(len(trend)-1))*w:.1f},{h - ((v-min_v)/rng)*(h-8) - 4:.1f}"
                           for i, v in enumerate(trend))
            last = pts.split()[-1].split(",")
            cx, cy = last[0], last[1]
            svg = f"""<svg viewBox="0 0 {w} {h}" style="width:100%;height:{h}px;">
                <polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"
                    stroke-linejoin="round" stroke-linecap="round"/>
                <circle cx="{cx}" cy="{cy}" r="3" fill="{color}"/>
            </svg>"""
            st.markdown(f"""
            <div class="card">
                <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                    <span style="font-family:'Syne',sans-serif;font-size:.9rem;font-weight:700;">{name}</span>
                    <span style="font-size:18px;font-family:'Syne',sans-serif;font-weight:800;color:{color};">{info['health']}</span>
                </div>
                {svg}
                <div style="display:flex;justify-content:space-between;font-size:11px;color:#6a8f5a;margin-top:4px;">
                    <span>7 days ago</span><span>Today</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:#243d1f;'>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.1rem;font-weight:700;margin-bottom:14px;">🌍 Environmental Conditions</div>', unsafe_allow_html=True)
    env_cols = st.columns(5)
    env_items = [
        ("🌡️", "Temperature",  f"{sensors['temperature']}°C",   "Optimal: 18–30°C",  C["amber"] if sensors["temperature"] > 32 else C["green"]),
        ("💧", "Humidity",     f"{sensors['humidity']}%",         "Optimal: 50–75%",   C["red"] if sensors["humidity"] > 85 else C["green"]),
        ("🌱", "Soil Moisture",f"{sensors['soilMoisture']}%",     "Optimal: 50–70%",   C["red"] if sensors["soilMoisture"] < 40 else C["green"]),
        ("🧪", "Soil pH",      str(sensors["soilPh"]),            "Optimal: 6.0–7.0",  C["amber"] if sensors["soilPh"] < 5.8 or sensors["soilPh"] > 7.5 else C["green"]),
        ("☀️","Light",        f"{sensors['lightIntensity']}lx",  "Good for crops",    C["teal"]),
    ]
    for col, (icon, label, val, note, color) in zip(env_cols, env_items):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:24px;">{icon}</div>
                <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;color:{color};line-height:1;">{val}</div>
                <div style="font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:#6a8f5a;margin-top:4px;">{label}</div>
                <div style="font-size:11px;color:#6a8f5a;margin-top:4px;">{note}</div>
            </div>
            """, unsafe_allow_html=True)

def tab_pest_disease():
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.4rem;font-weight:800;margin-bottom:4px;">🔬 Pest & Disease Detection</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#6a8f5a;font-size:13px;margin-bottom:20px;">Powered by Raspberry Pi Camera Module + Computer Vision AI</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="border:1.5px dashed #2d4a28;text-align:center;">
        <div style="font-size:32px;margin-bottom:8px;">📷</div>
        <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;margin-bottom:4px;">Upload Crop Photo for AI Analysis</div>
        <div style="font-size:13px;color:#6a8f5a;margin-bottom:16px;">Drop a crop leaf or field photo for instant detection</div>
    </div>
    """, unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    if uploaded:
        st.image(uploaded, caption="Uploaded for analysis", use_container_width=True)
        st.info("🔍 Computer vision analysis would run here on the Raspberry Pi.")

    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.1rem;font-weight:700;margin:20px 0 14px;">🦠 Active Detections</div>', unsafe_allow_html=True)

    for name, pest in PESTS.items():
        sev = pest["severity"]
        card_cls = "alert" if sev == "HIGH" else "warn" if sev == "MEDIUM" else "good"
        bdg_v = "red" if sev == "HIGH" else "amber" if sev == "MEDIUM" else "green"
        with st.expander(f"{name} — {', '.join(pest['affected'])} &middot; {pest['confidence']}% confidence"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="color:#6a8f5a;font-size:12px;text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px;">Symptoms</div>
                <div style="color:#a8c898;font-size:14px;margin-bottom:12px;">{pest['symptoms']}</div>
                <div style="color:#E24B4A;font-size:13px;margin-bottom:8px;">⚡ {pest['action']}</div>
                <div style="font-size:12px;color:#6a8f5a;">Detected in: {', '.join(pest['affected'])}</div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown('<div style="color:#6a8f5a;font-size:12px;text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px;">Recommended Pesticides</div>', unsafe_allow_html=True)
                for p in pest["pesticides"]:
                    st.markdown(f"""
                    <div style="background:#0a1508;border:1px solid #243d1f;border-radius:10px;padding:10px 12px;margin-bottom:8px;">
                        <div style="font-weight:500;font-size:14px;margin-bottom:4px;">{p['name']}</div>
                        <div style="font-size:12px;color:#a8c898;">📏 {p['dose']} &middot; 📅 {p['freq']}</div>
                        <div style="font-size:12px;color:#7bc452;margin-top:2px;">💰 ~KSh {p['cost']:,}/application</div>
                    </div>
                    """, unsafe_allow_html=True)

def tab_yield(sensors):
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.4rem;font-weight:800;margin-bottom:20px;">📊 Yield Prediction & Risk Analysis</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;margin-bottom:16px;">Predicted vs Optimal Yield (tonnes/ha)</div>
    """, unsafe_allow_html=True)
    for name, info in CROPS.items():
        pred, opt = predict_yield(name, info["health"], sensors)
        pct = round((pred / opt) * 100)
        color = C["green"] if pct >= 80 else C["amber"] if pct >= 60 else C["red"]
        st.markdown(f"""
        <div style="margin-bottom:16px;">
            <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px;">
                <span>{name}</span>
                <span style="color:#6a8f5a;">{pred} / {opt} t/ha</span>
            </div>
            {progress_bar_html(pct, color, 20)}
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1rem;font-weight:700;margin-bottom:12px;">Per-Crop Forecast</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for col, (name, info) in zip(cols, CROPS.items()):
        pred, opt = predict_yield(name, info["health"], sensors)
        pct = round((pred / opt) * 100)
        color = C["green"] if pct >= 80 else C["amber"] if pct >= 60 else C["red"]
        with col:
            st.markdown(f"""
            <div class="card">
                <div style="font-family:'Syne',sans-serif;font-size:.9rem;font-weight:700;margin-bottom:8px;">{name}</div>
                <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:{color};">{pred}</div>
                <div style="font-size:11px;color:#6a8f5a;margin-bottom:8px;">tonnes/ha</div>
                {progress_bar_html(pct, color, 4)}
                <div style="font-size:12px;color:#a8c898;margin-top:8px;">{pct}% of optimal<br>Gap: {opt - pred:.2f} t/ha</div>
            </div>
            """, unsafe_allow_html=True)

    risks = [
        {"name": "Drought Stress",      "prob": 72 if sensors["soilMoisture"] < 45 else 20, "impact": "HIGH",   "mit": "Increase irrigation frequency"},
        {"name": "Fall Armyworm",        "prob": 65,                                          "impact": "HIGH",   "mit": "Spray Emamectin within 48h"},
        {"name": "Fungal Disease",       "prob": 58 if sensors["humidity"] > 70 else 25,     "impact": "MEDIUM", "mit": "Apply Mancozeb preventively"},
        {"name": "Nutrient Deficiency",  "prob": 40,                                          "impact": "MEDIUM", "mit": "Top-dress with CAN and DAP"},
        {"name": "Heat Stress",          "prob": 35 if sensors["temperature"] > 30 else 15,  "impact": "MEDIUM", "mit": "Shade nets + morning irrigation"},
    ]

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1rem;font-weight:700;margin-bottom:12px;">⚠️ Risk Factors</div>', unsafe_allow_html=True)
    for r in risks:
        col_c = C["red"] if r["prob"] > 60 else C["amber"] if r["prob"] > 40 else C["green"]
        st.markdown(f"""
        <div class="card" style="display:flex;align-items:center;gap:16px;">
            <div style="width:52px;height:52px;border-radius:50%;border:3px solid {col_c};display:flex;align-items:center;
                justify-content:center;flex-shrink:0;font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:{col_c};">
                {r['prob']}%
            </div>
            <div style="flex:1;">
                <div style="font-weight:500;margin-bottom:2px;">{r['name']}</div>
                <div style="font-size:12px;color:#6a8f5a;">Impact: {r['impact']} &middot; 💡 {r['mit']}</div>
            </div>
            <div style="width:100px;">
                {progress_bar_html(r['prob'], col_c, 6)}
            </div>
        </div>
        """, unsafe_allow_html=True)

def tab_recommendations(sensors):
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.4rem;font-weight:800;margin-bottom:4px;">💡 Smart Recommendations</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#6a8f5a;font-size:13px;margin-bottom:20px;">Generated from sensor data &middot; Soil Moisture, pH, DHT11, GPS, Camera</div>', unsafe_allow_html=True)

    for rec in generate_recs(sensors):
        priority = rec["priority"]
        card_cls = "alert" if priority == "URGENT" else "warn" if priority == "IMPORTANT" else "good"
        bdg_v = "red" if priority == "URGENT" else "amber" if priority == "IMPORTANT" else "green"
        emoji = "🔴" if priority == "URGENT" else "🟡" if priority == "IMPORTANT" else "🟢"
        st.markdown(f"""
        <div class="card card-{card_cls}">
            <div style="font-size:11px;color:#6a8f5a;text-transform:uppercase;letter-spacing:.07em;margin-bottom:4px;">{rec['cat']}</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700;margin-bottom:6px;">{emoji} {rec['title']} &nbsp; {badge(priority, bdg_v)}</div>
            <div style="color:#a8c898;font-size:14px;line-height:1.7;margin-bottom:10px;">{rec['detail']}</div>
            <div style="display:flex;gap:16px;flex-wrap:wrap;">
                <span style="font-size:12px;color:#6a8f5a;">⏰ {rec['time']}</span>
                <span style="font-size:12px;color:#6a8f5a;">🔌 {rec['hw']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#243d1f;margin:20px 0;'>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.1rem;font-weight:700;margin-bottom:14px;">📅 Spray Schedule</div>', unsafe_allow_html=True)

    header_cols = st.columns([1.2, 2.5, 1.2, 1, 1])
    headers = ["Crop", "Pesticide &middot; Dose", "Next Due", "Cost", "Status"]
    for col, h in zip(header_cols, headers):
        col.markdown(f'<div style="font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#6a8f5a;padding:10px 0;">{h}</div>', unsafe_allow_html=True)

    for row in SPRAY_SCHEDULE:
        bdg_v = "red" if row["status"] == "OVERDUE" else "amber" if row["status"] == "UPCOMING" else "green"
        r_cols = st.columns([1.2, 2.5, 1.2, 1, 1])
        r_cols[0].markdown(f'<div style="padding:10px 0;font-size:14px;border-top:1px solid #243d1f;">{row["crop"]}</div>', unsafe_allow_html=True)
        r_cols[1].markdown(f'<div style="padding:10px 0;font-size:13px;color:#a8c898;border-top:1px solid #243d1f;">{row["pesticide"]} &middot; {row["dose"]}</div>', unsafe_allow_html=True)
        r_cols[2].markdown(f'<div style="padding:10px 0;font-size:13px;border-top:1px solid #243d1f;">{format_date(row["daysUntil"])}</div>', unsafe_allow_html=True)
        r_cols[3].markdown(f'<div style="padding:10px 0;font-size:13px;color:#7bc452;border-top:1px solid #243d1f;">KSh {row["cost"]}</div>', unsafe_allow_html=True)
        r_cols[4].markdown(f'<div style="padding:10px 0;border-top:1px solid #243d1f;">{badge(row["status"], bdg_v)}</div>', unsafe_allow_html=True)

def tab_ai_advisor(sensors):
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.4rem;font-weight:800;margin-bottom:4px;">🤖 AI Farm Advisor</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#6a8f5a;font-size:13px;margin-bottom:16px;">Ask anything about crops, pests, irrigation, fertilisation, or robot control</div>', unsafe_allow_html=True)

    quick_prompts = [
        ("💧 Should I water?",   "Should I water my crops today?"),
        ("🦠 Any pests?",        "What pests are affecting my crops?"),
        ("📊 Yield forecast?",   "What is my yield prediction?"),
        ("🌿 Spray schedule?",   "What should I spray and when?"),
        ("🤖 Robot status?",     "What is the status of the field robot?"),
    ]

    # Initialise chat history on first load
    if not st.session_state.chat:
        st.session_state.chat = [{
            "role": "assistant",
            "content": (f"👋 Hello! I'm your **AgroVision AI Advisor**. I have live data from all your sensors.\n\n"
                        f"Current: 🌡️ {sensors['temperature']}°C &middot; 💧 {sensors['humidity']}% humidity &middot; "
                        f"🌱 Soil moisture {sensors['soilMoisture']}% &middot; 🧪 pH {sensors['soilPh']}\n\n"
                        f"How can I help you today?")
        }]

    # Quick-prompt buttons
    btn_cols = st.columns(len(quick_prompts))
    for col, (label, prompt) in zip(btn_cols, quick_prompts):
        with col:
            if st.button(label, use_container_width=True, key=f"quick_{label}"):
                st.session_state.chat.append({"role": "user", "content": prompt})
                reply = ai_advisor_response(prompt, sensors)
                st.session_state.chat.append({"role": "assistant", "content": reply})
                st.rerun()

    # Chat display
    for msg in st.session_state.chat:
        with st.chat_message(msg["role"], avatar="🌿" if msg["role"] == "assistant" else "👨‍🌾"):
            st.markdown(msg["content"])

    # Input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.chat_input("Ask your AI advisor…")
    if user_input:
        st.session_state.chat.append({"role": "user", "content": user_input})
        reply = ai_advisor_response(user_input, sensors)
        st.session_state.chat.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.button("Clear Chat", key="clear_chat"):
        st.session_state.chat = []
        st.rerun()

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    if not st.session_state.user:
        auth_screen()
        return

    sensors = st.session_state.sensors
    user = st.session_state.user

    render_sidebar(sensors, user)

    tab_labels = ["🏠 Overview", "🌱 Crop Health", "🔬 Pest & Disease",
                  "📊 Yield", "💡 Recommendations", "🤖 AI Advisor"]
    tabs = st.tabs(tab_labels)

    with tabs[0]: tab_overview(sensors, user)
    with tabs[1]: tab_crop_health(sensors)
    with tabs[2]: tab_pest_disease()
    with tabs[3]: tab_yield(sensors)
    with tabs[4]: tab_recommendations(sensors)
    with tabs[5]: tab_ai_advisor(sensors)


main()