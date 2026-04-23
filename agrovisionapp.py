"""
╔══════════════════════════════════════════════════════════════╗
║          AgroVision — Crop Intelligence Platform             ║
║   Streamlit app integrating Raspberry Pi 4, Arduino,        ║
║   soil sensors, DHT11, camera, GPS & more                    ║
╚══════════════════════════════════════════════════════════════╝

HARDWARE CONNECTED (from project BOM):
  • Raspberry Pi 4 (4GB)    — main AI/SaaS controller
  • Arduino Mega 2560        — expanded I/O & sensor management
  • Arduino Uno              — mechanical control
  • Soil Moisture Sensor     — real-time soil moisture reading
  • Soil pH Sensor           — precision soil pH
  • DHT11                    — humidity & temperature
  • Ultrasonic Sensor HC-SR04— obstacle detection
  • GPS Module Neo-6M/7M     — field mapping
  • Raspberry Pi Camera      — computer-vision crop/weed detection
  • ESP8266 WiFi Module      — robot ↔ SaaS connectivity
  • DC Gear Motors (×4)      — navigation
  • Servo Motors (×2)        — camera positioning

SETUP:
  pip install streamlit plotly pandas numpy requests pillow pyserial

RUN:
  streamlit run agrovision_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import random
import json
import base64
from io import BytesIO

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AgroVision — Crop Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

  /* Dark green theme */
  .stApp { background-color: #0d1a0a; color: #e8f5e0; }
  [data-testid="stSidebar"] { background-color: #122010 !important; border-right: 1px solid #2d4a28; }
  [data-testid="stSidebar"] * { color: #a8c898 !important; }

  /* Metric cards */
  [data-testid="metric-container"] {
    background: #1f3a1b; border: 1px solid #2d4a28;
    border-radius: 12px; padding: 16px !important;
  }
  [data-testid="metric-container"] label { color: #6a8f5a !important; font-size: 12px; text-transform: uppercase; letter-spacing: 0.07em; }
  [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #7bc452 !important; font-family: 'Syne', sans-serif; font-size: 2rem; }

  /* Headers */
  h1, h2, h3 { font-family: 'Syne', sans-serif !important; color: #e8f5e0 !important; }
  h1 { font-size: 2.4rem !important; font-weight: 800 !important; letter-spacing: -0.03em; }

  /* Cards */
  .agro-card {
    background: #1f3a1b; border: 1px solid #2d4a28; border-radius: 14px;
    padding: 20px; margin-bottom: 12px;
  }
  .agro-card.alert { border-left: 4px solid #E24B4A; background: rgba(226,75,74,0.05); }
  .agro-card.warn  { border-left: 4px solid #EF9F27; background: rgba(186,117,23,0.05); }
  .agro-card.good  { border-left: 4px solid #7bc452; }

  /* Badges */
  .badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; letter-spacing: 0.05em; }
  .badge-green { background: rgba(99,153,34,0.15); color: #97C459; border: 1px solid rgba(99,153,34,0.3); }
  .badge-amber { background: rgba(186,117,23,0.15); color: #FAC775; border: 1px solid rgba(186,117,23,0.3); }
  .badge-red   { background: rgba(226,75,74,0.15);  color: #F09595; border: 1px solid rgba(226,75,74,0.3); }

  /* Buttons */
  .stButton > button {
    background: #7bc452 !important; color: #0d1a0a !important; border: none !important;
    border-radius: 10px !important; font-weight: 500 !important; font-family: 'DM Sans', sans-serif !important;
    transition: all .2s !important;
  }
  .stButton > button:hover { background: #8fd45e !important; transform: translateY(-1px); }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] { background: #1f3a1b; border-radius: 12px; border: 1px solid #2d4a28; padding: 4px; gap: 4px; }
  .stTabs [data-baseweb="tab"] { background: transparent; color: #a8c898; border-radius: 8px; }
  .stTabs [aria-selected="true"] { background: #253f21 !important; color: #7bc452 !important; }

  /* Input fields */
  .stTextInput input, .stSelectbox select, .stTextArea textarea {
    background: #1f3a1b !important; border: 1px solid #2d4a28 !important;
    color: #e8f5e0 !important; border-radius: 10px !important;
  }

  /* Divider */
  hr { border-color: #2d4a28 !important; }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #0d1a0a; }
  ::-webkit-scrollbar-thumb { background: #3a5e34; border-radius: 4px; }

  /* Status indicator */
  .live-dot { display: inline-block; width: 8px; height: 8px; background: #7bc452; border-radius: 50%; animation: pulse 2s infinite; margin-right: 6px; }
  @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(1.4)} }
</style>
""", unsafe_allow_html=True)

# ─── HARDWARE CONFIG ──────────────────────────────────────────────────────────
HARDWARE = {
    "Raspberry Pi 4 (4GB)":         {"icon": "🖥️", "role": "AI Controller & SaaS Hub",        "port": "Primary",  "status": "online"},
    "Arduino Mega 2560":            {"icon": "🔌", "role": "Sensor Management I/O",            "port": "/dev/ttyUSB0", "status": "online"},
    "Arduino Uno":                  {"icon": "⚙️", "role": "Mechanical Control",               "port": "/dev/ttyUSB1", "status": "online"},
    "Soil Moisture Sensor":         {"icon": "💧", "role": "Soil Water Content",               "port": "A0 (Mega)", "status": "online"},
    "Soil pH Sensor":               {"icon": "🧪", "role": "Soil Acidity/Alkalinity",          "port": "A1 (Mega)", "status": "online"},
    "DHT11 Temp/Humidity":          {"icon": "🌡️", "role": "Air Temp & Humidity",              "port": "D2 (Mega)", "status": "online"},
    "Ultrasonic HC-SR04":           {"icon": "📡", "role": "Obstacle Detection",               "port": "D22 (Mega)", "status": "online"},
    "GPS Neo-6M/7M":                {"icon": "🛰️", "role": "Field Mapping & Navigation",       "port": "Serial1 (Mega)", "status": "online"},
    "Raspberry Pi Camera":          {"icon": "📷", "role": "Vision / Weed & Disease Detect",  "port": "CSI",      "status": "online"},
    "ESP8266 WiFi Module":          {"icon": "📶", "role": "Robot ↔ SaaS Connectivity",       "port": "D10 (Mega)", "status": "online"},
    "DC Gear Motors (×4)":          {"icon": "⚡", "role": "Field Navigation",                 "port": "L298N Driver", "status": "online"},
    "Servo Motors (×2)":            {"icon": "🔧", "role": "Camera & Arm Positioning",         "port": "D9/D10 (Uno)", "status": "online"},
}

# ─── SENSOR SIMULATION ───────────────────────────────────────────────────────
def read_sensors():
    """
    In production, replace these with actual reads via:
      - pyserial: serial.Serial('/dev/ttyUSB0', 9600)
      - RPi.GPIO: GPIO.input(pin)
      - picamera2: camera capture
    """
    t = time.time()
    return {
        "temperature":    round(22 + 5 * np.sin(t / 3600) + random.uniform(-0.5, 0.5), 1),
        "humidity":       round(60 + 15 * np.sin(t / 7200) + random.uniform(-1, 1), 1),
        "soil_moisture":  round(45 + 20 * np.sin(t / 5000) + random.uniform(-2, 2), 1),
        "soil_ph":        round(6.2 + 0.8 * np.sin(t / 10000) + random.uniform(-0.1, 0.1), 1),
        "light_intensity":round(600 + 300 * abs(np.sin(t / 3600)) + random.uniform(-20, 20), 0),
        "obstacle_dist":  round(random.uniform(30, 200), 1),
        "gps_lat":        -1.2921 + random.uniform(-0.001, 0.001),
        "gps_lon":         36.8219 + random.uniform(-0.001, 0.001),
        "battery_pct":    round(85 + 5 * np.sin(t / 20000), 1),
        "timestamp":      datetime.now().strftime("%H:%M:%S"),
    }

# ─── CROP DATA ────────────────────────────────────────────────────────────────
CROPS = {
    "🌽 Maize":    {"field": "A", "area": 2.4, "health": 86, "stage": "Tasseling",   "days_left": 42, "status": "good"},
    "🍅 Tomatoes": {"field": "B", "area": 1.1, "health": 64, "stage": "Flowering",   "days_left": 28, "status": "warn"},
    "🫘 Beans":    {"field": "C", "area": 0.8, "health": 41, "stage": "Vegetative",  "days_left": 55, "status": "alert"},
    "🥬 Kale":     {"field": "D", "area": 0.6, "health": 91, "stage": "Mature",      "days_left": 14, "status": "good"},
}

# ─── PEST DATABASE ────────────────────────────────────────────────────────────
PEST_DB = {
    "Fall Armyworm": {
        "severity": "HIGH", "affected": ["🌽 Maize"], "confidence": 89,
        "symptoms": "Ragged holes in leaves, frass deposits, damaged tassels",
        "pesticides": [
            {"name": "Emamectin Benzoate 1.9% EC", "dose": "200ml/20L water", "frequency": "Every 7 days", "cost_ksh": 650},
            {"name": "Chlorpyrifos 48% EC",         "dose": "30ml/20L water",  "frequency": "Every 10 days","cost_ksh": 480},
            {"name": "Spinosad 48 SC",              "dose": "10ml/20L water",  "frequency": "Every 14 days","cost_ksh": 900},
        ],
        "action": "Spray immediately in early morning or evening. Wear PPE.",
    },
    "Early Blight": {
        "severity": "MEDIUM", "affected": ["🍅 Tomatoes"], "confidence": 74,
        "symptoms": "Dark brown spots with yellow halos on lower leaves, concentric rings",
        "pesticides": [
            {"name": "Mancozeb 80% WP",            "dose": "40g/20L water",   "frequency": "Every 7 days", "cost_ksh": 320},
            {"name": "Copper Oxychloride 50% WP",  "dose": "60g/20L water",   "frequency": "Every 10 days","cost_ksh": 280},
            {"name": "Chlorothalonil 75% WP",      "dose": "30g/20L water",   "frequency": "Every 14 days","cost_ksh": 450},
        ],
        "action": "Remove infected leaves, improve air circulation, avoid overhead irrigation.",
    },
    "Bean Stem Maggot": {
        "severity": "HIGH", "affected": ["🫘 Beans"], "confidence": 82,
        "symptoms": "Yellowing seedlings, wilted shoots, maggots at stem base",
        "pesticides": [
            {"name": "Imidacloprid 70% WS",        "dose": "Seed treatment 5g/kg seed", "frequency": "Once (planting)", "cost_ksh": 700},
            {"name": "Dimethoate 40% EC",           "dose": "20ml/20L water",  "frequency": "Every 7 days", "cost_ksh": 380},
            {"name": "Thiamethoxam 25% WG",        "dose": "12g/20L water",   "frequency": "Every 10 days","cost_ksh": 550},
        ],
        "action": "Apply soil drench at base of plants. Uproot and destroy severely affected plants.",
    },
    "Aphids": {
        "severity": "LOW", "affected": ["🥬 Kale", "🍅 Tomatoes"], "confidence": 61,
        "symptoms": "Clusters of small green/black insects on young shoots, sticky honeydew",
        "pesticides": [
            {"name": "Cypermethrin 10% EC",        "dose": "30ml/20L water",  "frequency": "Every 7 days", "cost_ksh": 250},
            {"name": "Pymetrozine 50% WG",         "dose": "20g/20L water",   "frequency": "Every 14 days","cost_ksh": 620},
        ],
        "action": "Use yellow sticky traps. Spray with neem extract (50ml/20L) as a first step.",
    },
}

# ─── RECOMMENDATIONS ENGINE ───────────────────────────────────────────────────
def generate_recommendations(sensors):
    recs = []

    if sensors["soil_moisture"] < 40:
        recs.append({
            "priority": "🔴 URGENT", "category": "Irrigation",
            "title": "Irrigate Fields B & C Now",
            "detail": f"Soil moisture is critically low at {sensors['soil_moisture']}% (optimal: 50–70%). "
                      f"Apply 25mm of water to Field B (tomatoes) and Field C (beans) immediately. "
                      f"Use drip irrigation if available to conserve water.",
            "time": "Within 2 hours",
            "hardware": "Soil Moisture Sensor (A0) → Arduino Mega → Water Pump Relay",
        })
    elif sensors["soil_moisture"] > 75:
        recs.append({
            "priority": "🟡 IMPORTANT", "category": "Drainage",
            "title": "Reduce Irrigation — Waterlogging Risk",
            "detail": f"Soil moisture at {sensors['soil_moisture']}% — excessive moisture promotes root rot and fungal disease. "
                      f"Suspend irrigation for 48 hours. Check drainage channels.",
            "time": "Within 6 hours",
            "hardware": "Soil Moisture Sensor → Arduino Mega",
        })

    if sensors["soil_ph"] < 5.8:
        recs.append({
            "priority": "🟡 IMPORTANT", "category": "Soil Amendment",
            "title": "Apply Agricultural Lime to Field C",
            "detail": f"Soil pH at {sensors['soil_ph']} (optimal: 6.0–7.0). Apply 2 tonnes/ha of agricultural lime. "
                      f"Incorporate into soil and re-test after 4 weeks.",
            "time": "Within 1 week",
            "hardware": "Soil pH Sensor (A1) → Arduino Mega",
        })
    elif sensors["soil_ph"] > 7.5:
        recs.append({
            "priority": "🟡 IMPORTANT", "category": "Soil Amendment",
            "title": "Apply Sulphur to Lower pH",
            "detail": f"Soil pH at {sensors['soil_ph']} — too alkaline. Apply elemental sulphur at 200kg/ha. "
                      f"Retest after 3 weeks.",
            "time": "Within 1 week",
            "hardware": "Soil pH Sensor (A1) → Arduino Mega",
        })

    if sensors["temperature"] > 32:
        recs.append({
            "priority": "🟡 IMPORTANT", "category": "Heat Management",
            "title": "Apply Shade Nets — Heat Stress Alert",
            "detail": f"Temperature at {sensors['temperature']}°C (threshold: 32°C). Tomatoes and beans at risk of blossom drop. "
                      f"Erect shade nets (50% shading) over Fields B & C. Increase irrigation frequency.",
            "time": "Today",
            "hardware": "DHT11 (D2) → Arduino Mega",
        })

    if sensors["humidity"] > 85:
        recs.append({
            "priority": "🔴 URGENT", "category": "Disease Prevention",
            "title": "Spray Fungicide — High Humidity Risk",
            "detail": f"Humidity at {sensors['humidity']}% creates ideal conditions for fungal diseases (early blight, powdery mildew). "
                      f"Apply Mancozeb 80% WP (40g/20L) as a preventive spray on all fields.",
            "time": "Within 24 hours",
            "hardware": "DHT11 (D2) → Arduino Mega",
        })

    recs.append({
        "priority": "🟢 ROUTINE", "category": "Fertilisation",
        "title": "Top-Dress Maize with CAN Fertiliser",
        "detail": "Field A maize is at tasseling stage — apply CAN (Calcium Ammonium Nitrate) at 150kg/ha "
                  "to boost grain filling. Apply when soil is moist, avoid leaf contact.",
        "time": "This week",
        "hardware": "GPS Module → Field mapping",
    })

    recs.append({
        "priority": "🟢 ROUTINE", "category": "Scouting",
        "title": "Deploy Robot for Field Scouting",
        "detail": "Schedule autonomous robot scouting mission across all 4 fields. "
                  "Camera module will capture images for AI pest/disease analysis. "
                  "GPS will map crop health zones.",
        "time": "Tomorrow 6:00 AM",
        "hardware": "Raspberry Pi Camera + GPS + DC Motors + ESP8266",
    })

    return recs

# ─── YIELD PREDICTION ─────────────────────────────────────────────────────────
def predict_yield(crop_name, health_score, sensors):
    base_yields = {
        "🌽 Maize":    {"base": 3.5, "unit": "tonnes/ha"},
        "🍅 Tomatoes": {"base": 25.0, "unit": "tonnes/ha"},
        "🫘 Beans":    {"base": 1.2,  "unit": "tonnes/ha"},
        "🥬 Kale":     {"base": 8.0,  "unit": "tonnes/ha"},
    }
    info = base_yields.get(crop_name, {"base": 2.0, "unit": "tonnes/ha"})
    health_factor   = health_score / 100
    moisture_factor = 1.0 if 50 <= sensors["soil_moisture"] <= 70 else 0.8
    ph_factor       = 1.0 if 6.0 <= sensors["soil_ph"] <= 7.0 else 0.85
    temp_factor     = 1.0 if 18 <= sensors["temperature"] <= 30 else 0.85
    predicted = info["base"] * health_factor * moisture_factor * ph_factor * temp_factor
    optimal   = info["base"]
    return round(predicted, 2), round(optimal, 2), info["unit"]

# ─── AI ADVISOR ──────────────────────────────────────────────────────────────
def ai_advisor_response(question, sensors, crops):
    """
    Simple rule-based AI advisor.
    Replace or augment with OpenAI / Gemini / Anthropic API call for production use.
    """
    q = question.lower()

    if any(w in q for w in ["water", "irrigat", "moisture", "dry"]):
        if sensors["soil_moisture"] < 40:
            return (f"🚿 **Irrigation Needed Urgently!**\n\nSoil moisture is at **{sensors['soil_moisture']}%** "
                    f"(optimal: 50–70%). Irrigate Fields B and C immediately with at least **25mm of water**. "
                    f"The robot can activate the irrigation relay via Arduino Mega (relay connected to D30). "
                    f"After irrigation, re-check soil moisture in **2 hours**.")
        else:
            return (f"💧 Soil moisture is currently **{sensors['soil_moisture']}%** — within acceptable range (50–70%). "
                    f"No irrigation needed at this time. Schedule next check in **6 hours**.")

    elif any(w in q for w in ["spray", "pesticide", "pest", "disease", "armyworm", "blight", "aphid"]):
        return ("🌿 **Pest & Disease Management:**\n\n"
                "Currently detected threats:\n"
                "- **Fall Armyworm** (Field A - Maize, 89% confidence) → Spray **Emamectin Benzoate 1.9% EC** at 200ml/20L. "
                "Best time: **early morning or evening**. Wear PPE.\n"
                "- **Early Blight** (Field B - Tomatoes, 74%) → Apply **Mancozeb 80% WP** at 40g/20L every 7 days.\n"
                "- **Bean Stem Maggot** (Field C - Beans, 82%) → Drench with **Dimethoate 40% EC** at 20ml/20L.\n\n"
                "⚠️ Always follow label instructions and observe pre-harvest intervals.")

    elif any(w in q for w in ["yield", "harvest", "predict", "production"]):
        lines = ["📊 **Yield Predictions (current conditions):**\n"]
        for crop, info in crops.items():
            pred, opt, unit = predict_yield(crop, info["health"], sensors)
            pct = round((pred / opt) * 100)
            lines.append(f"- **{crop}**: {pred} {unit} ({pct}% of optimal {opt})")
        lines.append(f"\n💡 Improving soil moisture and pH will boost yields by an estimated **8–15%**.")
        return "\n".join(lines)

    elif any(w in q for w in ["ph", "acid", "alkalin", "lime", "soil"]):
        return (f"🧪 **Soil Analysis:**\n\nCurrent pH: **{sensors['soil_ph']}** (optimal: 6.0–7.0)\n\n"
                f"{'⚠️ pH is LOW — apply **2 tonnes/ha agricultural lime** and retest in 4 weeks.' if sensors['soil_ph'] < 5.8 else ''}"
                f"{'✅ pH is within optimal range.' if 5.8 <= sensors['soil_ph'] <= 7.0 else ''}"
                f"{'⚠️ pH is HIGH — apply **elemental sulphur at 200kg/ha**.' if sensors['soil_ph'] > 7.0 else ''}\n\n"
                f"Soil moisture: **{sensors['soil_moisture']}%**")

    elif any(w in q for w in ["temp", "hot", "cold", "heat", "weather"]):
        return (f"🌡️ **Environmental Conditions:**\n\n"
                f"Temperature: **{sensors['temperature']}°C** (optimal crops: 18–30°C)\n"
                f"Humidity: **{sensors['humidity']}%** (optimal: 50–75%)\n\n"
                f"{'⚠️ High temperature — risk of heat stress on tomatoes. Apply shade nets.' if sensors['temperature'] > 32 else ''}"
                f"{'⚠️ High humidity — fungal disease risk. Apply preventive fungicide.' if sensors['humidity'] > 80 else ''}"
                f"{'✅ Conditions are within optimal range for all crops.' if sensors['temperature'] <= 32 and sensors['humidity'] <= 80 else ''}")

    elif any(w in q for w in ["fertiliz", "npk", "can", "dap", "urea", "nutrient"]):
        return ("🌱 **Fertilisation Schedule:**\n\n"
                "- **🌽 Maize (Field A)** — Tasseling stage: Top-dress with CAN at **150 kg/ha** this week.\n"
                "- **🍅 Tomatoes (Field B)** — Apply NPK 17:17:17 at **200 kg/ha** + foliar feed with calcium nitrate.\n"
                "- **🫘 Beans (Field C)** — Beans fix nitrogen; apply **Phosphorus (SSP)** at 100 kg/ha only.\n"
                "- **🥬 Kale (Field D)** — Approaching harvest: apply **foliar nitrogen spray** for quality.\n\n"
                "Always apply fertiliser when soil is moist to avoid burn.")

    elif any(w in q for w in ["robot", "motor", "camera", "gps", "autonomous"]):
        return ("🤖 **Robot Operations:**\n\n"
                "The agri-robot is **online** with all systems nominal:\n"
                "- 📷 Camera: Active — last scan 45 mins ago\n"
                "- 🛰️ GPS: Signal acquired (lat/lon logged)\n"
                "- ⚡ Motors: Ready — battery at 85%\n"
                "- 📶 ESP8266: Connected to SaaS platform\n\n"
                "**Commands available:**\n"
                "- *Initiate field scan* — navigate all 4 fields for health check\n"
                "- *Target spray* — move to GPS coordinates and trigger spray nozzle\n"
                "- *Return to base* — autonomous return for recharging")

    else:
        return (f"👋 I'm your **AgroVision AI Advisor**. Current farm status:\n\n"
                f"- 🌡️ Temp: {sensors['temperature']}°C | 💧 Humidity: {sensors['humidity']}%\n"
                f"- 🌱 Soil Moisture: {sensors['soil_moisture']}% | 🧪 pH: {sensors['soil_ph']}\n"
                f"- 🔋 Robot Battery: {sensors['battery_pct']}%\n\n"
                f"Ask me about: **watering**, **pesticides**, **yield prediction**, **soil pH**, "
                f"**fertilisation**, **temperature**, or **robot control**.")

# ═════════════════════════════════════════════════════════════════════════════
#                               SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🌿 AgroVision")
    st.markdown("**Crop Intelligence Platform**")
    st.markdown("---")

    # Live sensor readings
    sensors = read_sensors()

    st.markdown(f"<div style='color:#7bc452;font-size:12px;margin-bottom:8px'>"
                f"<span class='live-dot'></span>LIVE — {sensors['timestamp']}</div>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🌡️ Temp", f"{sensors['temperature']}°C")
        st.metric("🌱 Moisture", f"{sensors['soil_moisture']}%")
        st.metric("🔋 Battery", f"{sensors['battery_pct']}%")
    with col2:
        st.metric("💧 Humidity", f"{sensors['humidity']}%")
        st.metric("🧪 pH", f"{sensors['soil_ph']}")
        st.metric("☀️ Light", f"{int(sensors['light_intensity'])}lx")

    st.markdown("---")
    st.markdown("**🛰️ GPS Location**")
    st.caption(f"Lat: {sensors['gps_lat']:.4f}  Lon: {sensors['gps_lon']:.4f}")

    st.markdown("---")
    st.markdown("**🤖 Robot Status**")
    if sensors["obstacle_dist"] < 50:
        st.warning(f"⚠️ Obstacle at {sensors['obstacle_dist']}cm")
    else:
        st.success(f"✅ Clear — {sensors['obstacle_dist']:.0f}cm ahead")

    st.markdown("---")
    auto_refresh = st.checkbox("Auto-refresh sensors (30s)", value=False)
    if auto_refresh:
        time.sleep(30)
        st.rerun()

    if st.button("🔄 Refresh Now"):
        st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
#                           MAIN CONTENT
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("# 🌿 AgroVision")
st.markdown("**Agricultural Robotic & SaaS Intelligence Platform** — Raspberry Pi 4 · Arduino Mega · Sensors")
st.markdown("---")

# ─── TOP KPI ROW ──────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
avg_health = int(np.mean([v["health"] for v in CROPS.values()]))
alert_count = sum(1 for v in CROPS.values() if v["status"] == "alert")
warn_count  = sum(1 for v in CROPS.values() if v["status"] == "warn")
total_area  = sum(v["area"] for v in CROPS.values())

with c1: st.metric("🌱 Active Fields", 4)
with c2: st.metric("📊 Avg Health", f"{avg_health}%", delta=f"+3% this week")
with c3: st.metric("🔴 Alerts", alert_count, delta=f"{alert_count} critical", delta_color="inverse")
with c4: st.metric("🟡 Warnings", warn_count)
with c5: st.metric("🦠 Pests Detected", 3, delta="2 new")
with c6: st.metric("🌍 Total Area", f"{total_area}ha")

st.markdown("---")

# ─── TABS ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌱 Crop Health",
    "🔬 Pest & Disease",
    "📊 Yield Prediction",
    "💡 Recommendations",
    "🤖 AI Advisor",
    "🔌 Hardware Monitor",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CROP HEALTH
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Field Health Overview")

    cols = st.columns(4)
    for idx, (name, info) in enumerate(CROPS.items()):
        with cols[idx]:
            color = "#7bc452" if info["status"] == "good" else "#EF9F27" if info["status"] == "warn" else "#E24B4A"
            badge_cls = "badge-green" if info["status"] == "good" else "badge-amber" if info["status"] == "warn" else "badge-red"
            badge_txt = "HEALTHY" if info["status"] == "good" else "WATCH" if info["status"] == "warn" else "ALERT"
            st.markdown(f"""
            <div class="agro-card {info['status']}">
                <span class="badge {badge_cls}">{badge_txt}</span><br><br>
                <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700">{name}</div>
                <div style="color:#6a8f5a;font-size:12px;text-transform:uppercase;letter-spacing:.06em;margin:4px 0 12px">
                    Field {info['field']} · {info['area']}ha
                </div>
                <div style="font-family:'Syne',sans-serif;font-size:2.5rem;font-weight:800;color:{color};line-height:1">
                    {info['health']}
                </div>
                <div style="color:#6a8f5a;font-size:11px;margin-bottom:10px">Health Score</div>
                <div style="background:#0d1a0a;border-radius:4px;height:5px;overflow:hidden">
                    <div style="width:{info['health']}%;height:100%;background:{color};border-radius:4px"></div>
                </div>
                <div style="margin-top:10px;font-size:12px;color:#a8c898">
                    📅 Stage: {info['stage']}<br>
                    ⏳ {info['days_left']} days to harvest
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📈 Health Trend (Last 7 Days)")

    days = [(datetime.now() - timedelta(days=i)).strftime("%b %d") for i in range(6, -1, -1)]
    fig = go.Figure()
    colors_map = {"🌽 Maize": "#7bc452", "🍅 Tomatoes": "#EF9F27", "🫘 Beans": "#E24B4A", "🥬 Kale": "#5DCAA5"}

    for crop, info in CROPS.items():
        base = info["health"]
        trend = [max(10, min(100, base + random.randint(-8, 5) - (i * 0.3))) for i in range(6, -1, -1)]
        trend[-1] = base
        fig.add_trace(go.Scatter(
            x=days, y=trend, name=crop,
            line=dict(color=colors_map[crop], width=2.5),
            mode="lines+markers", marker=dict(size=6),
        ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a8c898"), legend=dict(bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#2d4a28"), yaxis=dict(gridcolor="#2d4a28", range=[0, 100]),
        margin=dict(l=0, r=0, t=20, b=0), height=280,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🌍 Environmental Conditions")
    e1, e2, e3, e4, e5 = st.columns(5)
    with e1: st.metric("🌡️ Temperature", f"{sensors['temperature']}°C", "Optimal: 18–30°C")
    with e2: st.metric("💧 Humidity", f"{sensors['humidity']}%", "Optimal: 50–75%")
    with e3: st.metric("🌱 Soil Moisture", f"{sensors['soil_moisture']}%", "Optimal: 50–70%")
    with e4: st.metric("🧪 Soil pH", f"{sensors['soil_ph']}", "Optimal: 6.0–7.0")
    with e5: st.metric("☀️ Light", f"{int(sensors['light_intensity'])}lx", "Good for crops")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PEST & DISEASE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("🔬 Pest & Disease Detection")
    st.caption("Powered by Raspberry Pi Camera Module + Computer Vision AI")

    # Upload image for analysis
    st.markdown("#### 📷 Upload Crop Photo for AI Analysis")
    uploaded = st.file_uploader("Drop a crop leaf / field photo", type=["jpg", "jpeg", "png", "webp"])

    if uploaded:
        img_col, result_col = st.columns([1, 1])
        with img_col:
            st.image(uploaded, caption="Uploaded Image", use_column_width=True)
        with result_col:
            with st.spinner("🤖 AI analysing image..."):
                time.sleep(2)
            st.markdown("""
            <div class="agro-card warn">
                <span class="badge badge-amber">AI DETECTION RESULT</span><br><br>
                <b style="font-size:1.1rem">Early Blight Detected</b><br>
                <span style="color:#6a8f5a;font-size:12px">Confidence: 78% · Severity: MEDIUM</span><br><br>
                <b>Symptoms identified:</b> Dark concentric lesions with yellow halos on lower leaves.<br><br>
                <b>Recommended action:</b> Spray Mancozeb 80% WP at 40g/20L water every 7 days.
                Remove and destroy infected leaves immediately.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🦠 Active Detections")

    for pest_name, pest in PEST_DB.items():
        sev_cls = "alert" if pest["severity"] == "HIGH" else "warn" if pest["severity"] == "MEDIUM" else "good"
        badge_cls = "badge-red" if pest["severity"] == "HIGH" else "badge-amber" if pest["severity"] == "MEDIUM" else "badge-green"

        with st.expander(f"{pest_name} — {', '.join(pest['affected'])} ({pest['confidence']}% confidence)"):
            col_a, col_b = st.columns([1.2, 1])
            with col_a:
                st.markdown(f"""
                <div class="agro-card {sev_cls}">
                    <span class="badge {badge_cls}">{pest['severity']} SEVERITY</span>
                    <p style="margin-top:12px;color:#a8c898;font-size:14px"><b>Symptoms:</b><br>{pest['symptoms']}</p>
                    <p style="color:#E24B4A;font-size:13px;margin-top:8px"><b>⚡ Action:</b> {pest['action']}</p>
                    <p style="color:#6a8f5a;font-size:12px">Detected in: {', '.join(pest['affected'])}</p>
                </div>
                """, unsafe_allow_html=True)

            with col_b:
                st.markdown("**💊 Recommended Pesticides:**")
                for p in pest["pesticides"]:
                    st.markdown(f"""
                    <div style="background:#1f3a1b;border:1px solid #2d4a28;border-radius:10px;padding:12px;margin-bottom:8px">
                        <b style="color:#e8f5e0">{p['name']}</b><br>
                        <span style="color:#a8c898;font-size:13px">📏 Dose: {p['dose']}</span><br>
                        <span style="color:#a8c898;font-size:13px">📅 Frequency: {p['frequency']}</span><br>
                        <span style="color:#7bc452;font-size:13px">💰 ~KSh {p['cost_ksh']:,}/application</span>
                    </div>
                    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — YIELD PREDICTION
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("📊 Yield Prediction & Risk Analysis")

    # Yield comparison chart
    crops_list, predicted_vals, optimal_vals, units_list = [], [], [], []
    for crop, info in CROPS.items():
        pred, opt, unit = predict_yield(crop, info["health"], sensors)
        crops_list.append(crop)
        predicted_vals.append(pred)
        optimal_vals.append(opt)
        units_list.append(unit)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name="Predicted Yield", x=crops_list, y=predicted_vals,
                          marker_color="#7bc452", text=[f"{v}" for v in predicted_vals],
                          textposition="outside", textfont=dict(color="#e8f5e0", size=11)))
    fig2.add_trace(go.Bar(name="Optimal Yield", x=crops_list, y=optimal_vals,
                          marker_color="rgba(123,196,82,0.2)",
                          marker_line=dict(color="#7bc452", width=1.5),
                          text=[f"{v}" for v in optimal_vals],
                          textposition="outside", textfont=dict(color="#6a8f5a", size=11)))

    fig2.update_layout(
        barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a8c898"), legend=dict(bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#2d4a28"), yaxis=dict(gridcolor="#2d4a28", title="Yield (tonnes/ha)"),
        margin=dict(l=0, r=0, t=20, b=0), height=320,
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Per-crop yield cards
    st.markdown("#### Per-Crop Forecast")
    y_cols = st.columns(4)
    for idx, (crop, info) in enumerate(CROPS.items()):
        pred, opt, unit = predict_yield(crop, info["health"], sensors)
        pct = int((pred / opt) * 100)
        gap = round(opt - pred, 2)
        color = "#7bc452" if pct >= 80 else "#EF9F27" if pct >= 60 else "#E24B4A"
        with y_cols[idx]:
            st.markdown(f"""
            <div class="agro-card">
                <div style="font-family:'Syne',sans-serif;font-weight:700">{crop}</div>
                <div style="font-family:'Syne',sans-serif;font-size:2rem;color:{color};line-height:1.2;margin:8px 0">
                    {pred}
                </div>
                <div style="color:#6a8f5a;font-size:11px">{unit}</div>
                <div style="background:#0d1a0a;border-radius:4px;height:5px;overflow:hidden;margin:10px 0">
                    <div style="width:{pct}%;height:100%;background:{color};border-radius:4px"></div>
                </div>
                <div style="font-size:12px;color:#a8c898">{pct}% of optimal<br>Gap: {gap} {unit}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("⚠️ Risk Factors")

    risks = [
        {"name": "Drought Stress", "prob": 72 if sensors["soil_moisture"] < 45 else 20,
         "impact": "HIGH", "mitigation": "Increase irrigation frequency"},
        {"name": "Fall Armyworm Spread", "prob": 65, "impact": "HIGH",
         "mitigation": "Spray Emamectin Benzoate within 48h"},
        {"name": "Fungal Disease (Blight)", "prob": 58 if sensors["humidity"] > 70 else 25,
         "impact": "MEDIUM", "mitigation": "Apply Mancozeb preventively"},
        {"name": "Nutrient Deficiency", "prob": 40, "impact": "MEDIUM",
         "mitigation": "Top-dress with CAN and DAP"},
        {"name": "Heat Stress", "prob": 35 if sensors["temperature"] > 30 else 15,
         "impact": "MEDIUM", "mitigation": "Shade nets and morning irrigation"},
    ]

    r_cols = st.columns(len(risks))
    for idx, risk in enumerate(risks):
        p = risk["prob"]
        col = "#E24B4A" if p > 60 else "#EF9F27" if p > 40 else "#7bc452"
        with r_cols[idx]:
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number", value=p,
                title={"text": risk["name"], "font": {"size": 11, "color": "#a8c898"}},
                number={"suffix": "%", "font": {"color": col, "size": 22}},
                gauge={
                    "axis": {"range": [0, 100], "tickfont": {"size": 9, "color": "#6a8f5a"}},
                    "bar":  {"color": col, "thickness": 0.3},
                    "bgcolor": "#1f3a1b",
                    "bordercolor": "#2d4a28",
                    "steps": [{"range": [0, 40], "color": "#122010"}, {"range": [40, 70], "color": "#1a2e18"}],
                }
            ))
            fig_g.update_layout(height=150, paper_bgcolor="rgba(0,0,0,0)",
                                font=dict(color="#a8c898"), margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_g, use_container_width=True)
            st.caption(f"💡 {risk['mitigation']}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("💡 Smart Recommendations")
    st.caption("Generated from sensor data · Soil Moisture, pH, DHT11, GPS, Camera")

    recs = generate_recommendations(sensors)

    for rec in recs:
        priority = rec["priority"]
        if "URGENT" in priority:
            card_class, bg_color = "alert", "#E24B4A"
        elif "IMPORTANT" in priority:
            card_class, bg_color = "warn", "#EF9F27"
        else:
            card_class, bg_color = "good", "#7bc452"

        st.markdown(f"""
        <div class="agro-card {card_class}" style="margin-bottom:12px">
            <div style="display:flex;justify-content:space-between;align-items:start">
                <div>
                    <span style="font-size:11px;color:#6a8f5a;text-transform:uppercase;letter-spacing:.07em">
                        {rec['category']}
                    </span>
                    <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;margin:4px 0">
                        {priority} — {rec['title']}
                    </div>
                    <div style="color:#a8c898;font-size:14px;line-height:1.7">{rec['detail']}</div>
                    <div style="margin-top:10px;display:flex;gap:12px">
                        <span style="font-size:12px;color:#6a8f5a">⏰ {rec['time']}</span>
                        <span style="font-size:12px;color:#6a8f5a">🔌 {rec['hardware']}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📅 Spray Schedule")
    spray_data = {
        "Crop":      ["🌽 Maize", "🍅 Tomatoes", "🫘 Beans", "🌽 Maize"],
        "Pesticide": ["Emamectin Benzoate 1.9% EC", "Mancozeb 80% WP", "Dimethoate 40% EC", "Chlorpyrifos 48% EC"],
        "Dose":      ["200ml/20L", "40g/20L", "20ml/20L", "30ml/20L"],
        "Next Due":  [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in [0, 2, 1, 5]],
        "Cost (KSh)": [650, 320, 380, 480],
        "Status":    ["🔴 OVERDUE", "🟡 UPCOMING", "🟡 UPCOMING", "🟢 SCHEDULED"],
    }
    df_spray = pd.DataFrame(spray_data)
    st.dataframe(df_spray, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — AI ADVISOR
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("🤖 AI Farm Advisor")
    st.caption("Ask anything about your crops, pests, irrigation, fertilisation, or robot control")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant",
             "content": f"👋 Hello! I'm your AgroVision AI Advisor. I have live data from all your sensors.\n\n"
                        f"Current conditions: 🌡️ {sensors['temperature']}°C · 💧 {sensors['humidity']}% humidity · "
                        f"🌱 Soil moisture {sensors['soil_moisture']}% · 🧪 pH {sensors['soil_ph']}\n\n"
                        f"How can I help you today? Try asking about **watering**, **pests**, **yield**, or **spraying**."}
        ]

    # Quick prompt buttons
    st.markdown("**Quick Prompts:**")
    qp_cols = st.columns(5)
    quick_prompts = [
        ("💧 Should I water?", "Should I water my crops today?"),
        ("🦠 Any pests?", "What pests are affecting my crops?"),
        ("📊 Yield forecast?", "What is my yield prediction for this season?"),
        ("🌿 Spray schedule?", "What should I spray and when?"),
        ("🤖 Robot status?", "What is the status of the field robot?"),
    ]
    for i, (label, prompt) in enumerate(quick_prompts):
        with qp_cols[i]:
            if st.button(label, key=f"qp_{i}"):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                response = ai_advisor_response(prompt, sensors, CROPS)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

    st.markdown("---")

    # Chat display
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="👨‍🌾"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant", avatar="🌿"):
                    st.markdown(msg["content"])

    # Input
    user_input = st.chat_input("Ask your AI advisor...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("🤖 Thinking..."):
            response = ai_advisor_response(user_input, sensors, CROPS)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — HARDWARE MONITOR
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.subheader("🔌 Hardware System Monitor")
    st.caption("All components from the AgroVision project BOM — KSh 67,800 total")

    total_cost = 67800
    st.markdown(f"""
    <div style="background:#1f3a1b;border:1px solid #3a5e34;border-radius:12px;padding:16px;margin-bottom:20px;
                display:flex;justify-content:space-between;align-items:center">
        <div>
            <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;color:#7bc452">
                KSh {total_cost:,}
            </div>
            <div style="color:#6a8f5a;font-size:12px;text-transform:uppercase;letter-spacing:.07em">
                Total Hardware Budget
            </div>
        </div>
        <div style="text-align:right">
            <div style="font-family:'Syne',sans-serif;color:#5DCAA5;font-size:1.1rem">{len(HARDWARE)} Components</div>
            <span class="badge badge-green">ALL SYSTEMS ONLINE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    hw_rows = [
        ("Raspberry Pi 4 (4GB)", "🖥️", "KSh 12,000", "AI/SaaS Controller", "/dev/ttyAMA0", "online"),
        ("Arduino Mega 2560",    "🔌", "KSh ~3,500", "Sensor I/O Hub",     "/dev/ttyUSB0", "online"),
        ("Arduino Uno",          "⚙️", "KSh 2,500",  "Mechanical Control", "/dev/ttyUSB1", "online"),
        ("DC Gear Motors ×4",    "⚡", "KSh 14,000", "Field Navigation",   "L298N Driver", "online"),
        ("Servo Motors ×2",      "🔧", "KSh 2,000",  "Camera Positioning", "D9/D10 Uno",   "online"),
        ("Solar Panel + Battery","🔋", "KSh 7,000",  "Power System",       "Buck Converter","online"),
        ("Soil Moisture Sensor", "💧", "KSh 800",    f"{sensors['soil_moisture']}% moisture", "A0 Mega", "online"),
        ("Soil pH Sensor",       "🧪", "KSh 4,000",  f"pH {sensors['soil_ph']}",              "A1 Mega", "online"),
        ("DHT11 Temp/Humidity",  "🌡️", "KSh 800",    f"{sensors['temperature']}°C · {sensors['humidity']}%", "D2 Mega", "online"),
        ("Ultrasonic HC-SR04",   "📡", "KSh 500",    f"{sensors['obstacle_dist']:.0f}cm ahead","D22 Mega","online"),
        ("GPS Neo-6M/7M",        "🛰️", "KSh 3,000",  f"{sensors['gps_lat']:.4f}, {sensors['gps_lon']:.4f}", "Serial1", "online"),
        ("Raspberry Pi Camera",  "📷", "KSh 4,000",  "CV crop detection",  "CSI port",     "online"),
        ("ESP8266 WiFi Module",  "📶", "KSh 1,000",  "Robot ↔ SaaS Link",  "D10 Mega",     "online"),
        ("Motor Drivers L298N×2","🚗", "KSh 2,000",  "Motor Control",      "Mega GPIO",    "online"),
        ("Chassis + Offroad Wheels","🏗️","KSh 11,000","Robot Frame",       "Assembly",     "online"),
    ]

    hw_df = pd.DataFrame(hw_rows, columns=["Component", "Icon", "Cost", "Reading/Role", "Connection", "Status"])

    for _, row in hw_df.iterrows():
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:space-between;
                    background:#1f3a1b;border:1px solid #2d4a28;border-radius:10px;
                    padding:12px 16px;margin-bottom:6px">
            <div style="display:flex;align-items:center;gap:12px;min-width:220px">
                <span style="font-size:20px">{row['Icon']}</span>
                <div>
                    <div style="font-weight:500;font-size:14px;color:#e8f5e0">{row['Component']}</div>
                    <div style="font-size:11px;color:#6a8f5a">{row['Connection']}</div>
                </div>
            </div>
            <div style="flex:1;padding:0 16px;font-size:13px;color:#a8c898">{row['Reading/Role']}</div>
            <div style="min-width:90px;text-align:right;font-size:12px;color:#7bc452;font-weight:500">{row['Cost']}</div>
            <div style="min-width:80px;text-align:right">
                <span class="badge badge-green">● ONLINE</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📟 Serial Monitor (Arduino)")
    st.caption("Live data stream from Arduino Mega → Raspberry Pi")

    serial_log = []
    for i in range(8):
        ts = (datetime.now() - timedelta(seconds=i * 5)).strftime("%H:%M:%S")
        serial_log.append(f"[{ts}] SOIL_MOIST:{sensors['soil_moisture'] + random.uniform(-1,1):.1f}% | "
                          f"PH:{sensors['soil_ph'] + random.uniform(-0.05,0.05):.2f} | "
                          f"TEMP:{sensors['temperature'] + random.uniform(-0.2,0.2):.1f}C | "
                          f"HUM:{sensors['humidity'] + random.uniform(-1,1):.1f}% | "
                          f"DIST:{sensors['obstacle_dist'] + random.uniform(-2,2):.0f}cm")

    st.code("\n".join(serial_log), language="text")

    st.markdown("---")
    st.subheader("🔧 Serial Connection Setup (Python)")
    st.code("""
# Install: pip install pyserial
import serial, json, time

# Connect to Arduino Mega
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

def read_sensors():
    line = ser.readline().decode('utf-8').strip()
    # Expected format: SOIL_MOIST:45.2|PH:6.3|TEMP:24.1|HUM:67.5|DIST:120
    data = dict(pair.split(':') for pair in line.split('|') if ':' in line)
    return {k: float(v) for k, v in data.items()}

while True:
    sensors = read_sensors()
    print(sensors)
    time.sleep(1)
""", language="python")

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#3a5e34;font-size:12px;padding:20px 0">
    <span style="color:#7bc452;font-family:'Syne',sans-serif;font-weight:700">AgroVision</span>
    · Agricultural Robotic & SaaS Intelligence Platform ·
    Raspberry Pi 4 · Arduino Mega 2560 · Arduino Uno · 10 Sensors · ESP8266 WiFi<br>
    Built for precision farming in Kenya 🌿 · KSh 67,800 prototype budget
</div>
""", unsafe_allow_html=True)