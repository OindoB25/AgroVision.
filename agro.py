import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# ─── CONFIG & THEME ───────────────────────────────────────────────────────────
st.set_page_config(page_title="AgroVision AI", page_icon="🌿", layout="wide")

# Injecting your custom CSS from the React project
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;700&display=swap');
    
    :root {
        --bg: #0a1508;
        --bg-card: #111e0e;
        --green: #7bc452;
        --text: #e8f5e0;
        --border: #243d1f;
    }

    .main { background-color: var(--bg); }
    h1, h2, h3, .syne-font { font-family: 'Syne', sans-serif !important; color: var(--text); }
    p, span, div { font-family: 'DM Sans', sans-serif; }

    /* Custom Metric Cards */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-value { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800; color: var(--green); }
    .metric-label { font-size: 11px; text-transform: uppercase; color: #6a8f5a; letter-spacing: 0.1em; }

    /* Live Dot Animation */
    .live-dot {
        display: inline-block; width: 8px; height: 8px; background: #7bc452;
        border-radius: 50%; animation: pulse 2s infinite; margin-right: 8px;
    }
    @keyframes pulse { 0% {opacity: 1;} 50% {opacity: 0.3;} 100% {opacity: 1;} }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #080f07 !important; border-right: 1px solid var(--border); }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ─── MOCK DATA & SENSORS ──────────────────────────────────────────────────────
CROPS = {
    "Maize": {"area": 2.4, "health": 86, "stage": "Tasseling", "status": "good"},
    "Tomatoes": {"area": 1.1, "health": 64, "stage": "Flowering", "status": "warn"},
    "Beans": {"area": 0.8, "health": 41, "stage": "Vegetative", "status": "alert"},
    "Kale": {"area": 0.6, "health": 91, "stage": "Mature", "status": "good"},
}

def get_sensor_data():
    # Simulated sensor drift
    t = time.time()
    return {
        "temp": round(22 + 5 * np.sin(t / 3600), 1),
        "moisture": round(45 + 20 * np.sin(t / 5000), 1),
        "ph": round(6.2 + 0.5 * np.sin(t / 10000), 1),
        "battery": round(85 + 5 * np.sin(t / 20000), 1)
    }

# ─── SESSION STATE (Auth) ─────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login_form():
    st.markdown("<h1 style='text-align: center;'>🌿 AgroVision</h1>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.write("### Sign In")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Sign In →", use_container_width=True):
                st.session_state.authenticated = True
                st.rerun()

# ─── MAIN DASHBOARD ───────────────────────────────────────────────────────────
def main_dashboard():
    sensors = get_sensor_data()
    
    # --- Sidebar ---
    with st.sidebar:
        st.markdown("<h2 class='syne-font'>🌿 AgroVision</h2>", unsafe_allow_html=True)
        st.markdown(f"<div style='color: #7bc452; font-size: 12px;'><span class='live-dot'></span>LIVE SENSORS</div>", unsafe_allow_html=True)
        
        st.divider()
        st.metric("Soil Moisture", f"{sensors['moisture']}%")
        st.metric("Soil pH", sensors['ph'])
        st.metric("Battery", f"{sensors['battery']}%")
        
        st.divider()
        if st.sidebar.button("Sign Out"):
            st.session_state.authenticated = False
            st.rerun()

    # --- Overview Page ---
    st.markdown(f"<h1 class='syne-font'>Good morning, Farmer 👋</h1>", unsafe_allow_html=True)
    st.write(f"Farm status for {datetime.now().strftime('%A, %d %B')}")

    # KPI Row
    cols = st.columns(4)
    kpi_data = [
        ("🌱", "Avg Health", "70.5%"),
        ("🗺️", "Active Fields", "4"),
        ("🌡️", "Temperature", f"{sensors['temp']}°C"),
        ("🔋", "Battery", f"{sensors['battery']}%")
    ]
    
    for i, (icon, label, val) in enumerate(kpi_data):
        with cols[i]:
            st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 24px;'>{icon}</div>
                    <div class='metric-value'>{val}</div>
                    <div class='metric-label'>{label}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("### Crop Health Status")
    
    # Chart Data Preparation
    chart_data = pd.DataFrame({
        'Crop': list(CROPS.keys()),
        'Health %': [v['health'] for v in CROPS.values()]
    })
    
    st.bar_chart(chart_data.set_index('Crop'), color="#7bc452")

    # Details Table
    st.table(pd.DataFrame(CROPS).T)

    # AI Advisor Chat
    st.divider()
    st.markdown("<h3 class='syne-font'>🤖 AI Advisor</h3>", unsafe_allow_html=True)
    prompt = st.chat_input("Ask about irrigation, pests, or yields...")
    if prompt:
        with st.chat_message("assistant"):
            if "water" in prompt.lower():
                st.write(f"💧 Current moisture is {sensors['moisture']}%. Field B needs attention soon.")
            else:
                st.write("I'm scanning your sensors... Everything looks nominal for Field A.")

# ─── ROUTING ──────────────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    login_form()
else:
    main_dashboard()