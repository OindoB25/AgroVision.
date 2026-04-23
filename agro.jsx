import { useState, useEffect, useCallback } from "react";

// ─── THEME COLORS ────────────────────────────────────────────────────────────
const C = {
  bg: "#0a1508",
  bgCard: "#111e0e",
  bgCard2: "#162114",
  border: "#243d1f",
  border2: "#2d4a28",
  green: "#7bc452",
  greenDim: "#4a7a30",
  greenText: "#a8d87a",
  muted: "#6a8f5a",
  text: "#e8f5e0",
  textDim: "#a8c898",
  amber: "#EF9F27",
  red: "#E24B4A",
  teal: "#5DCAA5",
};

// ─── GLOBAL STYLES ───────────────────────────────────────────────────────────
const globalStyles = `
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { background: #0a1508; color: #e8f5e0; font-family: 'DM Sans', sans-serif; }
  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: #0a1508; }
  ::-webkit-scrollbar-thumb { background: #2d4a28; border-radius: 4px; }

  @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.45;transform:scale(1.5)} }
  @keyframes fadeUp { from{opacity:0;transform:translateY(18px)} to{opacity:1;transform:translateY(0)} }
  @keyframes spin { to{transform:rotate(360deg)} }
  @keyframes shimmer { 0%{background-position:-200% 0} 100%{background-position:200% 0} }

  .fade-up { animation: fadeUp .45s ease both; }
  .fade-up-d1 { animation: fadeUp .45s .08s ease both; }
  .fade-up-d2 { animation: fadeUp .45s .16s ease both; }
  .fade-up-d3 { animation: fadeUp .45s .24s ease both; }

  .live-dot {
    display: inline-block; width: 7px; height: 7px; background: #7bc452;
    border-radius: 50%; animation: pulse 2s infinite; margin-right: 6px; flex-shrink: 0;
  }

  input:-webkit-autofill,
  input:-webkit-autofill:focus {
    -webkit-box-shadow: 0 0 0 1000px #111e0e inset !important;
    -webkit-text-fill-color: #e8f5e0 !important;
    caret-color: #7bc452;
  }

  .tab-btn { transition: background .2s, color .2s; }
  .tab-btn:hover { background: #1a2e18 !important; }
  .tab-btn.active { background: #1f3a1b !important; color: #7bc452 !important; }

  .nav-item { transition: background .18s, color .18s; cursor: pointer; }
  .nav-item:hover { background: rgba(123,196,82,0.07) !important; }
  .nav-item.active { background: rgba(123,196,82,0.12) !important; color: #7bc452 !important; }

  .btn-primary {
    background: #7bc452; color: #0a1508; border: none; border-radius: 10px;
    font-weight: 600; font-family: 'DM Sans', sans-serif; cursor: pointer;
    transition: background .18s, transform .15s; letter-spacing: 0.01em;
  }
  .btn-primary:hover { background: #8fd45e; transform: translateY(-1px); }
  .btn-primary:active { transform: translateY(0); }
  .btn-primary:disabled { opacity: .5; cursor: default; transform: none; }

  .btn-ghost {
    background: transparent; color: #a8c898; border: 1px solid #2d4a28;
    border-radius: 10px; font-family: 'DM Sans', sans-serif; cursor: pointer;
    transition: border-color .18s, color .18s;
  }
  .btn-ghost:hover { border-color: #7bc452; color: #7bc452; }

  .input-field {
    background: #111e0e; border: 1px solid #243d1f; color: #e8f5e0;
    border-radius: 10px; font-family: 'DM Sans', sans-serif; font-size: 14px;
    outline: none; transition: border-color .2s;
    width: 100%; padding: 11px 14px;
  }
  .input-field:focus { border-color: #7bc452; }
  .input-field::placeholder { color: #4a6a3a; }

  .card {
    background: #111e0e; border: 1px solid #243d1f; border-radius: 14px;
    transition: border-color .2s;
  }
  .card:hover { border-color: #2d4a28; }
  .card.alert { border-left: 3px solid #E24B4A; }
  .card.warn  { border-left: 3px solid #EF9F27; }
  .card.good  { border-left: 3px solid #7bc452; }

  .badge {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600;
    letter-spacing: 0.06em; text-transform: uppercase;
  }
  .badge-green { background: rgba(99,153,34,.14); color: #97C459; border: 1px solid rgba(99,153,34,.28); }
  .badge-amber { background: rgba(186,117,23,.14); color: #FAC775; border: 1px solid rgba(186,117,23,.28); }
  .badge-red   { background: rgba(226,75,74,.14);  color: #F09595; border: 1px solid rgba(226,75,74,.28); }
  .badge-teal  { background: rgba(93,202,165,.12); color: #5DCAA5; border: 1px solid rgba(93,202,165,.25); }

  .progress-bar { background: #0a1508; border-radius: 4px; overflow: hidden; }
  .progress-fill { height: 100%; border-radius: 4px; transition: width .6s ease; }

  .chat-bubble-user { background: #1a2e18; border: 1px solid #2d4a28; border-radius: 14px 14px 4px 14px; }
  .chat-bubble-ai   { background: #111e0e; border: 1px solid #243d1f; border-radius: 14px 14px 14px 4px; }

  .metric-card {
    background: #111e0e; border: 1px solid #243d1f; border-radius: 12px;
    padding: 16px; text-align: center;
  }
  .metric-value { font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 800; line-height: 1; }
  .metric-label { font-size: 11px; text-transform: uppercase; letter-spacing: .07em; color: #6a8f5a; margin-top: 4px; }

  .sidebar { width: 260px; min-width: 260px; }
  @media(max-width: 768px) { .sidebar { display: none; } }

  .chart-bar-wrap { display: flex; flex-direction: column; gap: 10px; }
  .chart-bar-row { display: flex; align-items: center; gap: 10px; }
  .chart-bar-label { width: 110px; font-size: 12px; color: #a8c898; flex-shrink: 0; }
  .chart-bar-track { flex: 1; height: 24px; background: #0a1508; border-radius: 6px; overflow: hidden; position: relative; }
  .chart-bar-fill  { height: 100%; border-radius: 6px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; font-size: 11px; font-weight: 600; color: #0a1508; transition: width .8s cubic-bezier(.4,0,.2,1); }
`;

// ─── MOCK DATA ────────────────────────────────────────────────────────────────
const CROPS = {
  "🌽 Maize":    { field: "A", area: 2.4, health: 86, stage: "Tasseling",  daysLeft: 42, status: "good" },
  "🍅 Tomatoes": { field: "B", area: 1.1, health: 64, stage: "Flowering",  daysLeft: 28, status: "warn" },
  "🫘 Beans":    { field: "C", area: 0.8, health: 41, stage: "Vegetative", daysLeft: 55, status: "alert" },
  "🥬 Kale":     { field: "D", area: 0.6, health: 91, stage: "Mature",     daysLeft: 14, status: "good" },
};

const PESTS = {
  "Fall Armyworm": {
    severity: "HIGH", affected: ["🌽 Maize"], confidence: 89,
    symptoms: "Ragged holes in leaves, frass deposits, damaged tassels",
    action: "Spray immediately in early morning or evening. Wear PPE.",
    pesticides: [
      { name: "Emamectin Benzoate 1.9% EC", dose: "200ml/20L water", freq: "Every 7 days", cost: 650 },
      { name: "Chlorpyrifos 48% EC", dose: "30ml/20L water", freq: "Every 10 days", cost: 480 },
    ],
  },
  "Early Blight": {
    severity: "MEDIUM", affected: ["🍅 Tomatoes"], confidence: 74,
    symptoms: "Dark brown spots with yellow halos on lower leaves",
    action: "Remove infected leaves, improve air circulation.",
    pesticides: [
      { name: "Mancozeb 80% WP", dose: "40g/20L water", freq: "Every 7 days", cost: 320 },
      { name: "Copper Oxychloride 50% WP", dose: "60g/20L water", freq: "Every 10 days", cost: 280 },
    ],
  },
  "Bean Stem Maggot": {
    severity: "HIGH", affected: ["🫘 Beans"], confidence: 82,
    symptoms: "Yellowing seedlings, wilted shoots, maggots at stem base",
    action: "Apply soil drench at base of plants.",
    pesticides: [
      { name: "Dimethoate 40% EC", dose: "20ml/20L water", freq: "Every 7 days", cost: 380 },
    ],
  },
  "Aphids": {
    severity: "LOW", affected: ["🥬 Kale", "🍅 Tomatoes"], confidence: 61,
    symptoms: "Clusters of small green/black insects on young shoots",
    action: "Use yellow sticky traps. Spray neem extract first.",
    pesticides: [
      { name: "Cypermethrin 10% EC", dose: "30ml/20L water", freq: "Every 7 days", cost: 250 },
    ],
  },
};

const SPRAY_SCHEDULE = [
  { crop: "🌽 Maize", pesticide: "Emamectin Benzoate 1.9% EC", dose: "200ml/20L", daysUntil: 0, cost: 650, status: "OVERDUE" },
  { crop: "🍅 Tomatoes", pesticide: "Mancozeb 80% WP", dose: "40g/20L", daysUntil: 2, cost: 320, status: "UPCOMING" },
  { crop: "🫘 Beans", pesticide: "Dimethoate 40% EC", dose: "20ml/20L", daysUntil: 1, cost: 380, status: "UPCOMING" },
  { crop: "🌽 Maize", pesticide: "Chlorpyrifos 48% EC", dose: "30ml/20L", daysUntil: 5, cost: 480, status: "SCHEDULED" },
];

const HARDWARE = [
  { name: "Raspberry Pi 4 (4GB)", icon: "🖥️", cost: "KSh 12,000", role: "AI Controller", port: "Primary" },
  { name: "Arduino Mega 2560", icon: "🔌", cost: "KSh 3,500", role: "Sensor I/O Hub", port: "/dev/ttyUSB0" },
  { name: "Arduino Uno", icon: "⚙️", cost: "KSh 2,500", role: "Mechanical Control", port: "/dev/ttyUSB1" },
  { name: "Soil Moisture Sensor", icon: "💧", cost: "KSh 800", role: "Soil Water Content", port: "A0 (Mega)" },
  { name: "Soil pH Sensor", icon: "🧪", cost: "KSh 4,000", role: "Soil Acidity", port: "A1 (Mega)" },
  { name: "DHT11 Temp/Humidity", icon: "🌡️", cost: "KSh 800", role: "Air Temp & Humidity", port: "D2 (Mega)" },
  { name: "Ultrasonic HC-SR04", icon: "📡", cost: "KSh 500", role: "Obstacle Detection", port: "D22 (Mega)" },
  { name: "GPS Neo-6M/7M", icon: "🛰️", cost: "KSh 3,000", role: "Field Navigation", port: "Serial1" },
  { name: "Raspberry Pi Camera", icon: "📷", cost: "KSh 4,000", role: "CV Crop Detection", port: "CSI" },
  { name: "ESP8266 WiFi Module", icon: "📶", cost: "KSh 1,000", role: "Robot ↔ SaaS Link", port: "D10 (Mega)" },
  { name: "DC Gear Motors ×4", icon: "⚡", cost: "KSh 14,000", role: "Field Navigation", port: "L298N Driver" },
  { name: "Servo Motors ×2", icon: "🔧", cost: "KSh 2,000", role: "Camera Positioning", port: "D9/D10 Uno" },
  { name: "Solar Panel + Battery", icon: "🔋", cost: "KSh 7,000", role: "Power System", port: "Buck Converter" },
  { name: "Chassis + Wheels", icon: "🏗️", cost: "KSh 11,000", role: "Robot Frame", port: "Assembly" },
  { name: "Motor Drivers L298N×2", icon: "🚗", cost: "KSh 2,000", role: "Motor Control", port: "Mega GPIO" },
];

// ─── SENSOR SIMULATION ────────────────────────────────────────────────────────
function readSensors() {
  const t = Date.now() / 1000;
  return {
    temperature:   +(22 + 5 * Math.sin(t / 3600) + (Math.random() - .5)).toFixed(1),
    humidity:      +(60 + 15 * Math.sin(t / 7200) + (Math.random() * 2 - 1)).toFixed(1),
    soilMoisture:  +(45 + 20 * Math.sin(t / 5000) + (Math.random() * 4 - 2)).toFixed(1),
    soilPh:        +(6.2 + .8 * Math.sin(t / 10000) + (Math.random() * .2 - .1)).toFixed(1),
    lightIntensity:+(600 + 300 * Math.abs(Math.sin(t / 3600)) + (Math.random() * 40 - 20)).toFixed(0),
    obstacleDist:  +(30 + Math.random() * 170).toFixed(1),
    gpsLat:        +(-1.2921 + (Math.random() * .002 - .001)).toFixed(4),
    gpsLon:        +(36.8219 + (Math.random() * .002 - .001)).toFixed(4),
    batteryPct:    +(85 + 5 * Math.sin(t / 20000)).toFixed(1),
  };
}

function predictYield(cropName, health, sensors) {
  const base = { "🌽 Maize": 3.5, "🍅 Tomatoes": 25.0, "🫘 Beans": 1.2, "🥬 Kale": 8.0 }[cropName] || 2.0;
  const mf = sensors.soilMoisture >= 50 && sensors.soilMoisture <= 70 ? 1 : .8;
  const pf = sensors.soilPh >= 6 && sensors.soilPh <= 7 ? 1 : .85;
  const tf = sensors.temperature >= 18 && sensors.temperature <= 30 ? 1 : .85;
  return { pred: +(base * (health / 100) * mf * pf * tf).toFixed(2), opt: base };
}

function generateRecs(sensors) {
  const recs = [];
  if (sensors.soilMoisture < 40) recs.push({ priority: "URGENT", cat: "Irrigation", title: "Irrigate Fields B & C Now", detail: `Soil moisture critically low at ${sensors.soilMoisture}% (optimal 50–70%). Apply 25mm immediately.`, time: "Within 2 hours", hw: "Soil Moisture Sensor → Arduino Mega" });
  else if (sensors.soilMoisture > 75) recs.push({ priority: "IMPORTANT", cat: "Drainage", title: "Reduce Irrigation — Waterlogging Risk", detail: `Soil moisture at ${sensors.soilMoisture}% — promotes root rot. Suspend irrigation 48 hours.`, time: "Within 6 hours", hw: "Soil Moisture Sensor → Arduino Mega" });
  if (sensors.soilPh < 5.8) recs.push({ priority: "IMPORTANT", cat: "Soil Amendment", title: "Apply Agricultural Lime to Field C", detail: `Soil pH at ${sensors.soilPh} (optimal 6.0–7.0). Apply 2 tonnes/ha agricultural lime.`, time: "Within 1 week", hw: "Soil pH Sensor → Arduino Mega" });
  if (sensors.temperature > 32) recs.push({ priority: "IMPORTANT", cat: "Heat Management", title: "Apply Shade Nets — Heat Stress Alert", detail: `Temperature at ${sensors.temperature}°C. Tomatoes and beans at risk. Erect shade nets over Fields B & C.`, time: "Today", hw: "DHT11 → Arduino Mega" });
  if (sensors.humidity > 85) recs.push({ priority: "URGENT", cat: "Disease Prevention", title: "Spray Fungicide — High Humidity Risk", detail: `Humidity at ${sensors.humidity}% creates ideal fungal disease conditions. Apply Mancozeb 80% WP.`, time: "Within 24 hours", hw: "DHT11 → Arduino Mega" });
  recs.push({ priority: "ROUTINE", cat: "Fertilisation", title: "Top-Dress Maize with CAN Fertiliser", detail: "Field A maize at tasseling — apply CAN at 150kg/ha to boost grain filling.", time: "This week", hw: "GPS Module → Field mapping" });
  recs.push({ priority: "ROUTINE", cat: "Scouting", title: "Deploy Robot for Field Scouting", detail: "Schedule autonomous robot scouting across all 4 fields for AI pest/disease analysis.", time: "Tomorrow 6:00 AM", hw: "Raspberry Pi Camera + GPS + DC Motors" });
  return recs;
}

function aiAdvisorResponse(question, sensors) {
  const q = question.toLowerCase();
  if (/water|irrigat|moisture|dry/.test(q)) {
    return sensors.soilMoisture < 40
      ? `🚿 **Irrigation Needed Urgently!**\n\nSoil moisture is at **${sensors.soilMoisture}%** (optimal: 50–70%). Irrigate Fields B and C immediately with at least **25mm of water**. The robot can activate the irrigation relay via Arduino Mega (relay on D30). Re-check in **2 hours**.`
      : `💧 Soil moisture is currently **${sensors.soilMoisture}%** — within acceptable range (50–70%). No irrigation needed. Schedule next check in **6 hours**.`;
  }
  if (/spray|pest|disease|armyworm|blight|aphid/.test(q)) {
    return `🌿 **Pest & Disease Management:**\n\nCurrently detected threats:\n- **Fall Armyworm** (Field A - Maize, 89% confidence) → Spray **Emamectin Benzoate 1.9% EC** at 200ml/20L. Best time: **early morning or evening**.\n- **Early Blight** (Field B - Tomatoes, 74%) → Apply **Mancozeb 80% WP** at 40g/20L every 7 days.\n- **Bean Stem Maggot** (Field C - Beans, 82%) → Drench with **Dimethoate 40% EC** at 20ml/20L.\n\n⚠️ Always wear PPE and observe pre-harvest intervals.`;
  }
  if (/yield|harvest|predict|production/.test(q)) {
    const lines = ["📊 **Yield Predictions (current conditions):**\n"];
    Object.entries(CROPS).forEach(([crop, info]) => {
      const { pred, opt } = predictYield(crop, info.health, sensors);
      lines.push(`- **${crop}**: ${pred} tonnes/ha (${Math.round((pred / opt) * 100)}% of optimal ${opt})`);
    });
    lines.push("\n💡 Improving soil moisture and pH will boost yields by an estimated **8–15%**.");
    return lines.join("\n");
  }
  if (/ph|acid|alkalin|lime|soil/.test(q)) {
    return `🧪 **Soil Analysis:**\n\nCurrent pH: **${sensors.soilPh}** (optimal: 6.0–7.0)\n\n${sensors.soilPh < 5.8 ? "⚠️ pH is LOW — apply **2 tonnes/ha agricultural lime** and retest in 4 weeks." : sensors.soilPh > 7.0 ? "⚠️ pH is HIGH — apply **elemental sulphur at 200kg/ha**." : "✅ pH is within optimal range."}\n\nSoil moisture: **${sensors.soilMoisture}%**`;
  }
  if (/temp|hot|cold|heat|weather/.test(q)) {
    return `🌡️ **Environmental Conditions:**\n\nTemperature: **${sensors.temperature}°C** (optimal crops: 18–30°C)\nHumidity: **${sensors.humidity}%** (optimal: 50–75%)\n\n${sensors.temperature > 32 ? "⚠️ High temperature — risk of heat stress on tomatoes. Apply shade nets.\n" : ""}${sensors.humidity > 80 ? "⚠️ High humidity — fungal disease risk. Apply preventive fungicide.\n" : ""}${sensors.temperature <= 32 && sensors.humidity <= 80 ? "✅ Conditions are within optimal range for all crops." : ""}`;
  }
  if (/robot|motor|camera|gps|autonom/.test(q)) {
    return `🤖 **Robot Operations:**\n\nThe agri-robot is **online** with all systems nominal:\n- 📷 Camera: Active — last scan 45 mins ago\n- 🛰️ GPS: Signal acquired (${sensors.gpsLat}, ${sensors.gpsLon})\n- ⚡ Motors: Ready — battery at ${sensors.batteryPct}%\n- 📶 ESP8266: Connected to SaaS platform\n\n**Available Commands:**\n- Initiate field scan across all 4 fields\n- Target spray to GPS coordinates\n- Return to base for recharging`;
  }
  return `👋 I'm your **AgroVision AI Advisor**. Current farm status:\n\n- 🌡️ Temp: ${sensors.temperature}°C | 💧 Humidity: ${sensors.humidity}%\n- 🌱 Soil Moisture: ${sensors.soilMoisture}% | 🧪 pH: ${sensors.soilPh}\n- 🔋 Robot Battery: ${sensors.batteryPct}%\n\nAsk me about: **watering**, **pesticides**, **yield prediction**, **soil pH**, **fertilisation**, or **robot control**.`;
}

// ─── FORMATTING HELPERS ───────────────────────────────────────────────────────
function formatDate(daysAhead) {
  const d = new Date(); d.setDate(d.getDate() + daysAhead);
  return d.toLocaleDateString("en-KE", { year: "numeric", month: "short", day: "numeric" });
}
function Syne(props) { return <span style={{ fontFamily: "'Syne', sans-serif", ...props.style }} className={props.className}>{props.children}</span>; }
function Badge({ children, variant = "green" }) { return <span className={`badge badge-${variant}`}>{children}</span>; }

// ─── SIMPLE RECHARTS-FREE BAR CHART ──────────────────────────────────────────
function BarChart({ data }) {
  const max = Math.max(...data.map(d => d.value));
  return (
    <div className="chart-bar-wrap">
      {data.map((d, i) => (
        <div className="chart-bar-row" key={i}>
          <div className="chart-bar-label">{d.label}</div>
          <div className="chart-bar-track">
            <div className="chart-bar-fill" style={{ width: `${(d.value / max) * 100}%`, background: d.color || C.green }}>
              {d.suffix ? d.value + d.suffix : d.value}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

// ─── LINE SPARK CHART (SVG) ───────────────────────────────────────────────────
function SparkLine({ data, color, height = 60, width = 200 }) {
  if (!data || data.length < 2) return null;
  const min = Math.min(...data); const max = Math.max(...data);
  const range = max - min || 1;
  const pts = data.map((v, i) => {
    const x = (i / (data.length - 1)) * width;
    const y = height - ((v - min) / range) * (height - 8) - 4;
    return `${x},${y}`;
  }).join(" ");
  return (
    <svg viewBox={`0 0 ${width} ${height}`} style={{ width: "100%", height }}>
      <polyline points={pts} fill="none" stroke={color} strokeWidth="2" strokeLinejoin="round" strokeLinecap="round" />
      <circle cx={pts.split(" ").pop().split(",")[0]} cy={pts.split(" ").pop().split(",")[1]} r="3" fill={color} />
    </svg>
  );
}

// ─── AUTH SCREENS ─────────────────────────────────────────────────────────────
function AuthScreen({ onAuth }) {
  const [mode, setMode] = useState("login"); // login | register
  const [form, setForm] = useState({ name: "", email: "", phone: "", farm: "", password: "", confirm: "" });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState(() => {
    try { return JSON.parse(localStorage.getItem("av_users") || "[]"); } catch { return []; }
  });

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  function validate() {
    const e = {};
    if (mode === "register") {
      if (!form.name.trim()) e.name = "Full name is required";
      if (!form.farm.trim()) e.farm = "Farm name is required";
      if (!form.phone.trim()) e.phone = "Phone number is required";
      if (form.password !== form.confirm) e.confirm = "Passwords do not match";
    }
    if (!form.email.includes("@")) e.email = "Valid email required";
    if (form.password.length < 6) e.password = "Password must be at least 6 characters";
    return e;
  }

  function handleSubmit() {
    const e = validate();
    if (Object.keys(e).length) { setErrors(e); return; }
    setErrors({});
    setLoading(true);
    setTimeout(() => {
      if (mode === "register") {
        if (users.find(u => u.email === form.email)) {
          setErrors({ email: "Email already registered" }); setLoading(false); return;
        }
        const user = { id: Date.now(), name: form.name, email: form.email, phone: form.phone, farm: form.farm, createdAt: new Date().toISOString() };
        const next = [...users, { ...user, password: form.password }];
        localStorage.setItem("av_users", JSON.stringify(next));
        setUsers(next);
        localStorage.setItem("av_session", JSON.stringify(user));
        onAuth(user);
      } else {
        const user = users.find(u => u.email === form.email && u.password === form.password);
        if (!user) { setErrors({ password: "Invalid email or password" }); setLoading(false); return; }
        const { password: _, ...safe } = user;
        localStorage.setItem("av_session", JSON.stringify(safe));
        onAuth(safe);
      }
      setLoading(false);
    }, 900);
  }

  const Field = ({ label, name, type = "text", placeholder }) => (
    <div style={{ marginBottom: 16 }}>
      <label style={{ fontSize: 12, color: C.muted, textTransform: "uppercase", letterSpacing: ".06em", display: "block", marginBottom: 6 }}>{label}</label>
      <input
        className="input-field"
        type={type}
        placeholder={placeholder}
        value={form[name]}
        onChange={e => set(name, e.target.value)}
        onKeyDown={e => e.key === "Enter" && handleSubmit()}
      />
      {errors[name] && <div style={{ color: C.red, fontSize: 12, marginTop: 4 }}>{errors[name]}</div>}
    </div>
  );

  return (
    <div style={{ minHeight: "100vh", background: C.bg, display: "flex", alignItems: "center", justifyContent: "center", padding: 20, position: "relative", overflow: "hidden" }}>
      {/* Atmospheric background */}
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse 60% 50% at 50% 0%, rgba(74,122,48,.18) 0%, transparent 70%)", pointerEvents: "none" }} />
      <div style={{ position: "absolute", inset: 0, backgroundImage: "radial-gradient(rgba(123,196,82,.04) 1px, transparent 1px)", backgroundSize: "32px 32px", pointerEvents: "none" }} />

      <div className="fade-up" style={{ width: "100%", maxWidth: 420, position: "relative", zIndex: 1 }}>
        {/* Logo */}
        <div style={{ textAlign: "center", marginBottom: 36 }}>
          <div style={{ fontSize: 40, marginBottom: 8 }}>🌿</div>
          <Syne style={{ fontSize: "2rem", fontWeight: 800, color: C.text, letterSpacing: "-.03em" }}>AgroVision</Syne>
          <div style={{ color: C.muted, fontSize: 13, marginTop: 4 }}>Crop Intelligence Platform · Kenya</div>
        </div>

        {/* Card */}
        <div className="card" style={{ padding: 32 }}>
          {/* Tab toggle */}
          <div style={{ display: "flex", gap: 4, background: "#0a1508", borderRadius: 10, padding: 4, marginBottom: 28 }}>
            {["login", "register"].map(m => (
              <button key={m} className={`tab-btn ${mode === m ? "active" : ""}`}
                onClick={() => { setMode(m); setErrors({}); }}
                style={{ flex: 1, padding: "8px 0", border: "none", borderRadius: 7, cursor: "pointer", fontSize: 14, fontFamily: "'DM Sans', sans-serif", color: mode === m ? C.green : C.muted, background: "transparent" }}>
                {m === "login" ? "Sign In" : "Create Account"}
              </button>
            ))}
          </div>

          {mode === "register" && (
            <>
              <Field label="Full Name" name="name" placeholder="e.g. John Mwangi" />
              <Field label="Farm Name" name="farm" placeholder="e.g. Mwangi Family Farm" />
              <Field label="Phone Number" name="phone" placeholder="e.g. +254 712 345 678" />
            </>
          )}
          <Field label="Email Address" name="email" type="email" placeholder="you@example.com" />
          <Field label="Password" name="password" type="password" placeholder="Min. 6 characters" />
          {mode === "register" && <Field label="Confirm Password" name="confirm" type="password" placeholder="Repeat your password" />}

          <button className="btn-primary" onClick={handleSubmit} disabled={loading}
            style={{ width: "100%", padding: "13px 0", fontSize: 15, marginTop: 8 }}>
            {loading ? "Please wait…" : mode === "login" ? "Sign In →" : "Create Account →"}
          </button>

          {mode === "login" && (
            <div style={{ marginTop: 20, padding: "14px 16px", background: "#0a1508", borderRadius: 10, border: `1px solid ${C.border}` }}>
              <div style={{ fontSize: 12, color: C.muted, marginBottom: 4 }}>🔑 Demo Account</div>
              <div style={{ fontSize: 13, color: C.textDim }}>Register a new account above, then sign in with those credentials.</div>
            </div>
          )}
        </div>

        <div style={{ textAlign: "center", color: C.muted, fontSize: 12, marginTop: 20 }}>
          Built for precision farming in Kenya 🌿 · KSh 67,800 prototype
        </div>
      </div>
    </div>
  );
}

// ─── SIDEBAR ──────────────────────────────────────────────────────────────────
function Sidebar({ sensors, activeTab, setActiveTab, user, onLogout }) {
  const navItems = [
    { id: "overview", icon: "🏠", label: "Overview" },
    { id: "crop-health", icon: "🌱", label: "Crop Health" },
    { id: "pest-disease", icon: "🔬", label: "Pest & Disease" },
    { id: "yield", icon: "📊", label: "Yield Prediction" },
    { id: "recommendations", icon: "💡", label: "Recommendations" },
    { id: "ai-advisor", icon: "🤖", label: "AI Advisor" },
    { id: "hardware", icon: "🔌", label: "Hardware Monitor" },
  ];

  return (
    <div className="sidebar" style={{ background: "#080f07", borderRight: `1px solid ${C.border}`, display: "flex", flexDirection: "column", height: "100vh", position: "sticky", top: 0 }}>
      {/* Logo */}
      <div style={{ padding: "24px 20px 16px" }}>
        <Syne style={{ fontSize: "1.4rem", fontWeight: 800, color: C.text }}>🌿 AgroVision</Syne>
        <div style={{ fontSize: 11, color: C.muted, marginTop: 2 }}>Crop Intelligence Platform</div>
      </div>

      {/* Live indicator */}
      <div style={{ padding: "0 20px 16px" }}>
        <div style={{ display: "flex", alignItems: "center", fontSize: 12, color: C.green }}>
          <span className="live-dot" />
          LIVE SENSORS
        </div>
      </div>

      {/* Sensor quick stats */}
      <div style={{ padding: "0 16px 16px", display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
        {[
          { icon: "🌡️", label: "Temp", val: `${sensors.temperature}°C` },
          { icon: "💧", label: "Humidity", val: `${sensors.humidity}%` },
          { icon: "🌱", label: "Moisture", val: `${sensors.soilMoisture}%` },
          { icon: "🧪", label: "pH", val: sensors.soilPh },
          { icon: "🔋", label: "Battery", val: `${sensors.batteryPct}%` },
          { icon: "☀️", label: "Light", val: `${sensors.lightIntensity}lx` },
        ].map(s => (
          <div key={s.label} style={{ background: C.bgCard, border: `1px solid ${C.border}`, borderRadius: 8, padding: "8px 10px" }}>
            <div style={{ fontSize: 14 }}>{s.icon}</div>
            <div style={{ fontSize: 15, fontFamily: "'Syne',sans-serif", fontWeight: 700, color: C.green, lineHeight: 1.1 }}>{s.val}</div>
            <div style={{ fontSize: 10, color: C.muted, textTransform: "uppercase", letterSpacing: ".06em" }}>{s.label}</div>
          </div>
        ))}
      </div>

      {/* GPS */}
      <div style={{ padding: "0 16px 12px" }}>
        <div style={{ background: C.bgCard, border: `1px solid ${C.border}`, borderRadius: 8, padding: "8px 10px", fontSize: 12, color: C.textDim }}>
          🛰️ <span style={{ color: C.muted }}>GPS:</span> {sensors.gpsLat}, {sensors.gpsLon}
        </div>
        <div style={{ marginTop: 6, background: C.bgCard, border: `1px solid ${C.border}`, borderRadius: 8, padding: "8px 10px", fontSize: 12, color: sensors.obstacleDist < 50 ? C.amber : C.teal }}>
          {sensors.obstacleDist < 50 ? `⚠️ Obstacle at ${sensors.obstacleDist}cm` : `✅ Clear — ${sensors.obstacleDist.toFixed(0)}cm ahead`}
        </div>
      </div>

      <div style={{ height: 1, background: C.border, margin: "0 16px 12px" }} />

      {/* Nav */}
      <nav style={{ flex: 1, padding: "0 8px", overflowY: "auto" }}>
        {navItems.map(item => (
          <div key={item.id}
            className={`nav-item ${activeTab === item.id ? "active" : ""}`}
            onClick={() => setActiveTab(item.id)}
            style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 12px", borderRadius: 8, marginBottom: 2, fontSize: 14, color: activeTab === item.id ? C.green : C.textDim }}>
            <span style={{ fontSize: 16 }}>{item.icon}</span>
            {item.label}
          </div>
        ))}
      </nav>

      <div style={{ height: 1, background: C.border, margin: "12px 16px" }} />

      {/* User */}
      <div style={{ padding: "0 16px 20px" }}>
        <div style={{ background: C.bgCard, border: `1px solid ${C.border}`, borderRadius: 10, padding: "12px 14px", marginBottom: 10 }}>
          <div style={{ fontSize: 13, fontWeight: 500, color: C.text }}>{user.name}</div>
          <div style={{ fontSize: 11, color: C.muted, marginTop: 2 }}>{user.farm || "My Farm"}</div>
          <div style={{ fontSize: 11, color: C.muted }}>{user.email}</div>
        </div>
        <button className="btn-ghost" onClick={onLogout} style={{ width: "100%", padding: "9px 0", fontSize: 13 }}>
          Sign Out
        </button>
      </div>
    </div>
  );
}

// ─── TAB: OVERVIEW ────────────────────────────────────────────────────────────
function TabOverview({ sensors, user }) {
  const avgHealth = Math.round(Object.values(CROPS).reduce((a, c) => a + c.health, 0) / Object.keys(CROPS).length);
  const alerts = Object.values(CROPS).filter(c => c.status === "alert").length;

  return (
    <div className="fade-up">
      <div style={{ marginBottom: 24 }}>
        <Syne style={{ fontSize: "1.8rem", fontWeight: 800, color: C.text }}>Good morning, {user.name.split(" ")[0]} 👋</Syne>
        <div style={{ color: C.muted, marginTop: 4, fontSize: 14 }}>Here's your farm status for {new Date().toLocaleDateString("en-KE", { weekday: "long", day: "numeric", month: "long" })}</div>
      </div>

      {/* KPIs */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(150px, 1fr))", gap: 12, marginBottom: 28 }}>
        {[
          { label: "Avg Health", val: `${avgHealth}%`, color: avgHealth > 70 ? C.green : C.amber, icon: "🌱" },
          { label: "Active Fields", val: "4", color: C.teal, icon: "🗺️" },
          { label: "Alerts", val: alerts, color: alerts > 0 ? C.red : C.green, icon: "⚠️" },
          { label: "Temperature", val: `${sensors.temperature}°C`, color: C.text, icon: "🌡️" },
          { label: "Soil Moisture", val: `${sensors.soilMoisture}%`, color: sensors.soilMoisture < 40 ? C.red : sensors.soilMoisture > 75 ? C.amber : C.green, icon: "💧" },
          { label: "Battery", val: `${sensors.batteryPct}%`, color: C.green, icon: "🔋" },
        ].map(k => (
          <div key={k.label} className="metric-card fade-up-d1">
            <div style={{ fontSize: 22, marginBottom: 4 }}>{k.icon}</div>
            <div className="metric-value" style={{ color: k.color }}>{k.val}</div>
            <div className="metric-label">{k.label}</div>
          </div>
        ))}
      </div>

      {/* Crops quick grid */}
      <Syne style={{ fontSize: "1rem", fontWeight: 700, color: C.text, display: "block", marginBottom: 12 }}>Field Status</Syne>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 12, marginBottom: 28 }}>
        {Object.entries(CROPS).map(([name, info]) => {
          const color = info.status === "good" ? C.green : info.status === "warn" ? C.amber : C.red;
          return (
            <div key={name} className={`card ${info.status}`} style={{ padding: 16 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", marginBottom: 10 }}>
                <Syne style={{ fontSize: "1rem", fontWeight: 700 }}>{name}</Syne>
                <Badge variant={info.status === "good" ? "green" : info.status === "warn" ? "amber" : "red"}>
                  {info.status === "good" ? "HEALTHY" : info.status === "warn" ? "WATCH" : "ALERT"}
                </Badge>
              </div>
              <div className="metric-value" style={{ color, fontSize: "1.6rem" }}>{info.health}</div>
              <div style={{ fontSize: 11, color: C.muted, marginBottom: 8 }}>Health Score</div>
              <div className="progress-bar" style={{ height: 4, marginBottom: 8 }}>
                <div className="progress-fill" style={{ width: `${info.health}%`, background: color }} />
              </div>
              <div style={{ fontSize: 12, color: C.textDim }}>Field {info.field} · {info.area}ha · {info.daysLeft}d to harvest</div>
            </div>
          );
        })}
      </div>

      {/* Pest alerts */}
      <Syne style={{ fontSize: "1rem", fontWeight: 700, color: C.text, display: "block", marginBottom: 12 }}>Active Pest Alerts</Syne>
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {Object.entries(PESTS).slice(0, 3).map(([name, p]) => (
          <div key={name} className={`card ${p.severity === "HIGH" ? "alert" : p.severity === "MEDIUM" ? "warn" : "good"}`} style={{ padding: 14, display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 8 }}>
            <div>
              <div style={{ fontWeight: 500, marginBottom: 2 }}>{name}</div>
              <div style={{ fontSize: 12, color: C.muted }}>{p.affected.join(", ")} · {p.confidence}% confidence</div>
            </div>
            <Badge variant={p.severity === "HIGH" ? "red" : p.severity === "MEDIUM" ? "amber" : "green"}>{p.severity}</Badge>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── TAB: CROP HEALTH ─────────────────────────────────────────────────────────
function TabCropHealth({ sensors }) {
  return (
    <div className="fade-up">
      <Syne style={{ fontSize: "1.4rem", fontWeight: 800, marginBottom: 4, display: "block" }}>Field Health Overview</Syne>
      <div style={{ color: C.muted, fontSize: 13, marginBottom: 20 }}>Sensor data from Soil Moisture, pH, DHT11, GPS, Camera</div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 14, marginBottom: 28 }}>
        {Object.entries(CROPS).map(([name, info]) => {
          const color = info.status === "good" ? C.green : info.status === "warn" ? C.amber : C.red;
          return (
            <div key={name} className={`card ${info.status}`} style={{ padding: 20 }}>
              <Badge variant={info.status === "good" ? "green" : info.status === "warn" ? "amber" : "red"}>
                {info.status === "good" ? "HEALTHY" : info.status === "warn" ? "WATCH" : "ALERT"}
              </Badge>
              <Syne style={{ fontSize: "1.05rem", fontWeight: 700, display: "block", marginTop: 12 }}>{name}</Syne>
              <div style={{ fontSize: 11, color: C.muted, textTransform: "uppercase", letterSpacing: ".06em", marginBottom: 10 }}>Field {info.field} · {info.area}ha</div>
              <div className="metric-value" style={{ color, fontSize: "2.4rem" }}>{info.health}</div>
              <div style={{ fontSize: 11, color: C.muted, marginBottom: 8 }}>Health Score</div>
              <div className="progress-bar" style={{ height: 5 }}>
                <div className="progress-fill" style={{ width: `${info.health}%`, background: color }} />
              </div>
              <div style={{ marginTop: 10, fontSize: 13, color: C.textDim }}>
                📅 Stage: {info.stage}<br />⏳ {info.daysLeft} days to harvest
              </div>
            </div>
          );
        })}
      </div>

      <div style={{ height: 1, background: C.border, marginBottom: 20 }} />
      <Syne style={{ fontSize: "1.1rem", fontWeight: 700, display: "block", marginBottom: 16 }}>📈 Health Trend (Last 7 Days)</Syne>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(230px, 1fr))", gap: 14, marginBottom: 28 }}>
        {Object.entries(CROPS).map(([name, info]) => {
          const colors2 = { "🌽 Maize": C.green, "🍅 Tomatoes": C.amber, "🫘 Beans": C.red, "🥬 Kale": C.teal };
          const trend = Array.from({ length: 7 }, (_, i) =>
            Math.max(10, Math.min(100, info.health + Math.round(Math.random() * 13 - 8) - i * .3))
          ).reverse();
          trend[6] = info.health;
          const color = colors2[name] || C.green;
          return (
            <div key={name} className="card" style={{ padding: 16 }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                <Syne style={{ fontSize: "0.9rem", fontWeight: 700 }}>{name}</Syne>
                <span style={{ fontSize: 18, fontFamily: "'Syne',sans-serif", fontWeight: 800, color }}>{info.health}</span>
              </div>
              <SparkLine data={trend} color={color} height={55} width={200} />
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: C.muted, marginTop: 4 }}>
                <span>7 days ago</span><span>Today</span>
              </div>
            </div>
          );
        })}
      </div>

      <div style={{ height: 1, background: C.border, marginBottom: 20 }} />
      <Syne style={{ fontSize: "1.1rem", fontWeight: 700, display: "block", marginBottom: 14 }}>🌍 Environmental Conditions</Syne>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))", gap: 12 }}>
        {[
          { icon: "🌡️", label: "Temperature", val: `${sensors.temperature}°C`, note: "Optimal: 18–30°C", color: sensors.temperature > 32 ? C.amber : C.green },
          { icon: "💧", label: "Humidity", val: `${sensors.humidity}%`, note: "Optimal: 50–75%", color: sensors.humidity > 85 ? C.red : C.green },
          { icon: "🌱", label: "Soil Moisture", val: `${sensors.soilMoisture}%`, note: "Optimal: 50–70%", color: sensors.soilMoisture < 40 ? C.red : C.green },
          { icon: "🧪", label: "Soil pH", val: sensors.soilPh, note: "Optimal: 6.0–7.0", color: sensors.soilPh < 5.8 || sensors.soilPh > 7.5 ? C.amber : C.green },
          { icon: "☀️", label: "Light", val: `${sensors.lightIntensity}lx`, note: "Good for crops", color: C.teal },
        ].map(m => (
          <div key={m.label} className="metric-card">
            <div style={{ fontSize: 24 }}>{m.icon}</div>
            <div className="metric-value" style={{ color: m.color, fontSize: "1.5rem" }}>{m.val}</div>
            <div className="metric-label">{m.label}</div>
            <div style={{ fontSize: 11, color: C.muted, marginTop: 4 }}>{m.note}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── TAB: PEST & DISEASE ──────────────────────────────────────────────────────
function TabPestDisease() {
  const [expanded, setExpanded] = useState(null);
  return (
    <div className="fade-up">
      <Syne style={{ fontSize: "1.4rem", fontWeight: 800, display: "block", marginBottom: 4 }}>🔬 Pest & Disease Detection</Syne>
      <div style={{ fontSize: 13, color: C.muted, marginBottom: 20 }}>Powered by Raspberry Pi Camera Module + Computer Vision AI</div>

      {/* Upload zone */}
      <div className="card" style={{ padding: 20, marginBottom: 24, border: `1.5px dashed ${C.border2}`, textAlign: "center" }}>
        <div style={{ fontSize: 32, marginBottom: 8 }}>📷</div>
        <Syne style={{ fontSize: "1rem", fontWeight: 700, display: "block", marginBottom: 4 }}>Upload Crop Photo for AI Analysis</Syne>
        <div style={{ fontSize: 13, color: C.muted, marginBottom: 16 }}>Drop a crop leaf or field photo for instant detection</div>
        <button className="btn-primary" style={{ padding: "10px 24px", fontSize: 13 }}>
          Choose Image →
        </button>
      </div>

      <Syne style={{ fontSize: "1.1rem", fontWeight: 700, display: "block", marginBottom: 14 }}>🦠 Active Detections</Syne>

      {Object.entries(PESTS).map(([name, pest]) => {
        const isOpen = expanded === name;
        const sevClass = pest.severity === "HIGH" ? "alert" : pest.severity === "MEDIUM" ? "warn" : "good";
        const badgeV = pest.severity === "HIGH" ? "red" : pest.severity === "MEDIUM" ? "amber" : "green";
        return (
          <div key={name} className={`card ${sevClass}`} style={{ marginBottom: 10, overflow: "hidden" }}>
            <div onClick={() => setExpanded(isOpen ? null : name)}
              style={{ padding: "16px 18px", cursor: "pointer", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <span style={{ fontWeight: 600, fontSize: 15 }}>{name}</span>
                <span style={{ color: C.muted, fontSize: 13, marginLeft: 10 }}>{pest.affected.join(", ")} · {pest.confidence}% confidence</span>
              </div>
              <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
                <Badge variant={badgeV}>{pest.severity}</Badge>
                <span style={{ color: C.muted, fontSize: 16 }}>{isOpen ? "▲" : "▼"}</span>
              </div>
            </div>
            {isOpen && (
              <div style={{ padding: "0 18px 18px", display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
                <div>
                  <div style={{ color: C.muted, fontSize: 12, textTransform: "uppercase", letterSpacing: ".06em", marginBottom: 8 }}>Symptoms</div>
                  <div style={{ color: C.textDim, fontSize: 14, marginBottom: 12 }}>{pest.symptoms}</div>
                  <div style={{ color: C.red, fontSize: 13, marginBottom: 8 }}>⚡ {pest.action}</div>
                  <div style={{ fontSize: 12, color: C.muted }}>Detected in: {pest.affected.join(", ")}</div>
                </div>
                <div>
                  <div style={{ color: C.muted, fontSize: 12, textTransform: "uppercase", letterSpacing: ".06em", marginBottom: 8 }}>Recommended Pesticides</div>
                  {pest.pesticides.map((p, i) => (
                    <div key={i} style={{ background: "#0a1508", border: `1px solid ${C.border}`, borderRadius: 10, padding: "10px 12px", marginBottom: 8 }}>
                      <div style={{ fontWeight: 500, fontSize: 14, marginBottom: 4 }}>{p.name}</div>
                      <div style={{ fontSize: 12, color: C.textDim }}>📏 {p.dose} · 📅 {p.freq}</div>
                      <div style={{ fontSize: 12, color: C.green, marginTop: 2 }}>💰 ~KSh {p.cost.toLocaleString()}/application</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

// ─── TAB: YIELD PREDICTION ────────────────────────────────────────────────────
function TabYield({ sensors }) {
  const risks = [
    { name: "Drought Stress", prob: sensors.soilMoisture < 45 ? 72 : 20, impact: "HIGH", mit: "Increase irrigation frequency" },
    { name: "Fall Armyworm", prob: 65, impact: "HIGH", mit: "Spray Emamectin within 48h" },
    { name: "Fungal Disease", prob: sensors.humidity > 70 ? 58 : 25, impact: "MEDIUM", mit: "Apply Mancozeb preventively" },
    { name: "Nutrient Deficiency", prob: 40, impact: "MEDIUM", mit: "Top-dress with CAN and DAP" },
    { name: "Heat Stress", prob: sensors.temperature > 30 ? 35 : 15, impact: "MEDIUM", mit: "Shade nets + morning irrigation" },
  ];

  return (
    <div className="fade-up">
      <Syne style={{ fontSize: "1.4rem", fontWeight: 800, display: "block", marginBottom: 20 }}>📊 Yield Prediction & Risk Analysis</Syne>

      {/* Bar chart */}
      <div className="card" style={{ padding: 20, marginBottom: 20 }}>
        <Syne style={{ fontSize: "1rem", fontWeight: 700, display: "block", marginBottom: 16 }}>Predicted vs Optimal Yield (tonnes/ha)</Syne>
        {Object.entries(CROPS).map(([name, info]) => {
          const { pred, opt } = predictYield(name, info.health, sensors);
          return (
            <div key={name} style={{ marginBottom: 16 }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 6 }}>
                <span>{name}</span>
                <span style={{ color: C.muted }}>{pred} / {opt} t/ha</span>
              </div>
              <div className="progress-bar" style={{ height: 20, borderRadius: 6 }}>
                <div className="progress-fill" style={{
                  width: `${(pred / opt) * 100}%`,
                  background: (pred / opt) >= .8 ? C.green : (pred / opt) >= .6 ? C.amber : C.red,
                  borderRadius: 6, display: "flex", alignItems: "center", paddingLeft: 8, fontSize: 11, fontWeight: 600, color: "#0a1508"
                }}>{Math.round((pred / opt) * 100)}%</div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Per-crop cards */}
      <Syne style={{ fontSize: "1rem", fontWeight: 700, display: "block", marginBottom: 12 }}>Per-Crop Forecast</Syne>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(170px, 1fr))", gap: 12, marginBottom: 24 }}>
        {Object.entries(CROPS).map(([name, info]) => {
          const { pred, opt } = predictYield(name, info.health, sensors);
          const pct = Math.round((pred / opt) * 100);
          const color = pct >= 80 ? C.green : pct >= 60 ? C.amber : C.red;
          return (
            <div key={name} className="card" style={{ padding: 16 }}>
              <Syne style={{ fontSize: ".9rem", fontWeight: 700, display: "block", marginBottom: 8 }}>{name}</Syne>
              <div className="metric-value" style={{ color, fontSize: "1.8rem" }}>{pred}</div>
              <div style={{ fontSize: 11, color: C.muted, marginBottom: 8 }}>tonnes/ha</div>
              <div className="progress-bar" style={{ height: 4, marginBottom: 6 }}>
                <div className="progress-fill" style={{ width: `${pct}%`, background: color }} />
              </div>
              <div style={{ fontSize: 12, color: C.textDim }}>{pct}% of optimal<br />Gap: {(opt - pred).toFixed(2)} t/ha</div>
            </div>
          );
        })}
      </div>

      {/* Risk factors */}
      <Syne style={{ fontSize: "1rem", fontWeight: 700, display: "block", marginBottom: 12 }}>⚠️ Risk Factors</Syne>
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {risks.map(r => {
          const col = r.prob > 60 ? C.red : r.prob > 40 ? C.amber : C.green;
          return (
            <div key={r.name} className="card" style={{ padding: "14px 18px", display: "flex", alignItems: "center", gap: 16 }}>
              <div style={{ width: 52, height: 52, borderRadius: "50%", border: `3px solid ${col}`, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                <Syne style={{ fontSize: "1.1rem", color: col }}>{r.prob}%</Syne>
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 500, marginBottom: 2 }}>{r.name}</div>
                <div style={{ fontSize: 12, color: C.muted }}>Impact: {r.impact} · 💡 {r.mit}</div>
              </div>
              <div className="progress-bar" style={{ width: 100, height: 6, flexShrink: 0 }}>
                <div className="progress-fill" style={{ width: `${r.prob}%`, background: col }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─── TAB: RECOMMENDATIONS ─────────────────────────────────────────────────────
function TabRecommendations({ sensors }) {
  const recs = generateRecs(sensors);
  return (
    <div className="fade-up">
      <Syne style={{ fontSize: "1.4rem", fontWeight: 800, display: "block", marginBottom: 4 }}>💡 Smart Recommendations</Syne>
      <div style={{ fontSize: 13, color: C.muted, marginBottom: 20 }}>Generated from sensor data · Soil Moisture, pH, DHT11, GPS, Camera</div>

      {recs.map((rec, i) => {
        const isUrgent = rec.priority === "URGENT";
        const isImportant = rec.priority === "IMPORTANT";
        const cardClass = isUrgent ? "alert" : isImportant ? "warn" : "good";
        const badgeV = isUrgent ? "red" : isImportant ? "amber" : "green";
        const emoji = isUrgent ? "🔴" : isImportant ? "🟡" : "🟢";
        return (
          <div key={i} className={`card ${cardClass}`} style={{ padding: "18px 20px", marginBottom: 12 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", flexWrap: "wrap", gap: 8 }}>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 11, color: C.muted, textTransform: "uppercase", letterSpacing: ".07em", marginBottom: 4 }}>{rec.cat}</div>
                <Syne style={{ fontSize: "1.05rem", fontWeight: 700, display: "block", marginBottom: 6 }}>{emoji} {rec.title}</Syne>
                <div style={{ color: C.textDim, fontSize: 14, lineHeight: 1.7, marginBottom: 10 }}>{rec.detail}</div>
                <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
                  <span style={{ fontSize: 12, color: C.muted }}>⏰ {rec.time}</span>
                  <span style={{ fontSize: 12, color: C.muted }}>🔌 {rec.hw}</span>
                </div>
              </div>
              <Badge variant={badgeV}>{rec.priority}</Badge>
            </div>
          </div>
        );
      })}

      <div style={{ height: 1, background: C.border, margin: "20px 0" }} />
      <Syne style={{ fontSize: "1.1rem", fontWeight: 700, display: "block", marginBottom: 14 }}>📅 Spray Schedule</Syne>

      <div className="card" style={{ overflow: "hidden" }}>
        <div style={{ display: "grid", gridTemplateColumns: "auto 1fr auto auto auto", gap: 0 }}>
          {["Crop", "Pesticide · Dose", "Next Due", "Cost", "Status"].map(h => (
            <div key={h} style={{ padding: "10px 14px", background: "#0a1508", fontSize: 11, textTransform: "uppercase", letterSpacing: ".06em", color: C.muted, borderBottom: `1px solid ${C.border}` }}>{h}</div>
          ))}
          {SPRAY_SCHEDULE.map((row, i) => (
            [
              <div key={`${i}a`} style={{ padding: "12px 14px", fontSize: 14, borderBottom: `1px solid ${C.border}` }}>{row.crop}</div>,
              <div key={`${i}b`} style={{ padding: "12px 14px", fontSize: 13, color: C.textDim, borderBottom: `1px solid ${C.border}` }}>{row.pesticide} · {row.dose}</div>,
              <div key={`${i}c`} style={{ padding: "12px 14px", fontSize: 13, borderBottom: `1px solid ${C.border}` }}>{formatDate(row.daysUntil)}</div>,
              <div key={`${i}d`} style={{ padding: "12px 14px", fontSize: 13, color: C.green, borderBottom: `1px solid ${C.border}` }}>KSh {row.cost}</div>,
              <div key={`${i}e`} style={{ padding: "12px 14px", borderBottom: `1px solid ${C.border}` }}>
                <Badge variant={row.status === "OVERDUE" ? "red" : row.status === "UPCOMING" ? "amber" : "green"}>{row.status}</Badge>
              </div>,
            ]
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── TAB: AI ADVISOR ──────────────────────────────────────────────────────────
function TabAiAdvisor({ sensors }) {
  const [chat, setChat] = useState([
    { role: "ai", text: `👋 Hello! I'm your **AgroVision AI Advisor**. I have live data from all your sensors.\n\nCurrent: 🌡️ ${sensors.temperature}°C · 💧 ${sensors.humidity}% humidity · 🌱 Soil moisture ${sensors.soilMoisture}% · 🧪 pH ${sensors.soilPh}\n\nHow can I help you today?` }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const endRef = useCallback(el => el?.scrollIntoView({ behavior: "smooth" }), []);

  const QUICK = [
    ["💧 Should I water?", "Should I water my crops today?"],
    ["🦠 Any pests?", "What pests are affecting my crops?"],
    ["📊 Yield forecast?", "What is my yield prediction?"],
    ["🌿 Spray schedule?", "What should I spray and when?"],
    ["🤖 Robot status?", "What is the status of the field robot?"],
  ];

  function send(text) {
    if (!text.trim() || loading) return;
    setChat(c => [...c, { role: "user", text }]);
    setInput("");
    setLoading(true);
    setTimeout(() => {
      setChat(c => [...c, { role: "ai", text: aiAdvisorResponse(text, sensors) }]);
      setLoading(false);
    }, 700);
  }

  function renderMsg(text) {
    return text.split("\n").map((line, i) => {
      const bold = line.replace(/\*\*(.+?)\*\*/g, (_, m) => `<strong>${m}</strong>`);
      return <div key={i} dangerouslySetInnerHTML={{ __html: bold }} style={{ marginBottom: line === "" ? 6 : 0 }} />;
    });
  }

  return (
    <div className="fade-up" style={{ display: "flex", flexDirection: "column", height: "calc(100vh - 80px)" }}>
      <Syne style={{ fontSize: "1.4rem", fontWeight: 800, display: "block", marginBottom: 4 }}>🤖 AI Farm Advisor</Syne>
      <div style={{ fontSize: 13, color: C.muted, marginBottom: 16 }}>Ask anything about crops, pests, irrigation, fertilisation, or robot control</div>

      {/* Quick prompts */}
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 16 }}>
        {QUICK.map(([label, prompt]) => (
          <button key={label} className="btn-ghost" onClick={() => send(prompt)} style={{ padding: "7px 14px", fontSize: 12 }}>{label}</button>
        ))}
      </div>

      {/* Chat messages */}
      <div style={{ flex: 1, overflowY: "auto", display: "flex", flexDirection: "column", gap: 12, paddingRight: 4, marginBottom: 16 }}>
        {chat.map((msg, i) => (
          <div key={i} style={{ display: "flex", justifyContent: msg.role === "user" ? "flex-end" : "flex-start" }}>
            <div style={{ maxWidth: "78%", display: "flex", gap: 10, alignItems: "flex-start" }}>
              {msg.role === "ai" && <div style={{ fontSize: 22, flexShrink: 0, marginTop: 2 }}>🌿</div>}
              <div className={msg.role === "user" ? "chat-bubble-user" : "chat-bubble-ai"} style={{ padding: "12px 16px", fontSize: 14, lineHeight: 1.7, color: C.textDim }}>
                {renderMsg(msg.text)}
              </div>
              {msg.role === "user" && <div style={{ fontSize: 22, flexShrink: 0, marginTop: 2 }}>👨‍🌾</div>}
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
            <div style={{ fontSize: 22 }}>🌿</div>
            <div className="chat-bubble-ai" style={{ padding: "12px 16px", color: C.muted, fontSize: 14 }}>Thinking…</div>
          </div>
        )}
        <div ref={endRef} />
      </div>

      {/* Input */}
      <div style={{ display: "flex", gap: 10 }}>
        <input className="input-field" value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && send(input)}
          placeholder="Ask your AI advisor…" style={{ flex: 1 }} />
        <button className="btn-primary" onClick={() => send(input)} style={{ padding: "0 20px", flexShrink: 0 }} disabled={loading || !input.trim()}>
          Send
        </button>
        <button className="btn-ghost" onClick={() => setChat([chat[0]])} style={{ padding: "0 14px", flexShrink: 0, fontSize: 13 }}>
          Clear
        </button>
      </div>
    </div>
  );
}

// ─── TAB: HARDWARE ────────────────────────────────────────────────────────────
function TabHardware({ sensors }) {
  const serialLog = Array.from({ length: 8 }, (_, i) => {
    const t = new Date(Date.now() - i * 5000).toTimeString().slice(0, 8);
    return `[${t}] SOIL_MOIST:${(sensors.soilMoisture + Math.random() - .5).toFixed(1)}% | PH:${(sensors.soilPh + (Math.random() * .1 - .05)).toFixed(2)} | TEMP:${(sensors.temperature + (Math.random() * .4 - .2)).toFixed(1)}C | HUM:${(sensors.humidity + Math.random() - .5).toFixed(1)}%`;
  });

  return (
    <div className="fade-up">
      <Syne style={{ fontSize: "1.4rem", fontWeight: 800, display: "block", marginBottom: 4 }}>🔌 Hardware System Monitor</Syne>
      <div style={{ fontSize: 13, color: C.muted, marginBottom: 16 }}>All components from the AgroVision BOM · KSh 67,800 total</div>

      {/* Summary banner */}
      <div className="card" style={{ padding: 20, marginBottom: 20, display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 12 }}>
        <div>
          <Syne style={{ fontSize: "1.8rem", fontWeight: 800, color: C.green }}>KSh 67,800</Syne>
          <div style={{ fontSize: 11, color: C.muted, textTransform: "uppercase", letterSpacing: ".07em", marginTop: 2 }}>Total Hardware Budget</div>
        </div>
        <div style={{ textAlign: "right" }}>
          <Syne style={{ fontSize: "1.1rem", color: C.teal }}>{HARDWARE.length} Components</Syne>
          <div style={{ marginTop: 4 }}><Badge variant="green">ALL SYSTEMS ONLINE</Badge></div>
        </div>
      </div>

      {/* Hardware list */}
      <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 24 }}>
        {HARDWARE.map(hw => (
          <div key={hw.name} className="card" style={{ padding: "12px 16px", display: "flex", alignItems: "center", gap: 14, flexWrap: "wrap" }}>
            <span style={{ fontSize: 22, flexShrink: 0 }}>{hw.icon}</span>
            <div style={{ flex: 1, minWidth: 160 }}>
              <div style={{ fontWeight: 500, fontSize: 14 }}>{hw.name}</div>
              <div style={{ fontSize: 11, color: C.muted }}>{hw.port}</div>
            </div>
            <div style={{ fontSize: 13, color: C.textDim, flex: 1, minWidth: 120 }}>{hw.role}</div>
            <div style={{ fontSize: 13, color: C.green, fontWeight: 500, minWidth: 90, textAlign: "right" }}>{hw.cost}</div>
            <Badge variant="green">● ONLINE</Badge>
          </div>
        ))}
      </div>

      {/* Serial monitor */}
      <Syne style={{ fontSize: "1.1rem", fontWeight: 700, display: "block", marginBottom: 10 }}>📟 Serial Monitor (Arduino)</Syne>
      <div style={{ background: "#050c04", border: `1px solid ${C.border}`, borderRadius: 10, padding: 16, fontFamily: "monospace", fontSize: 12, color: "#7bc452", lineHeight: 1.8, marginBottom: 20, overflowX: "auto" }}>
        {serialLog.map((line, i) => <div key={i}>{line}</div>)}
      </div>

      {/* Code sample */}
      <Syne style={{ fontSize: "1rem", fontWeight: 700, display: "block", marginBottom: 10 }}>🔧 Python Serial Integration</Syne>
      <div style={{ background: "#050c04", border: `1px solid ${C.border}`, borderRadius: 10, padding: 16, fontFamily: "monospace", fontSize: 12, color: "#a8d87a", lineHeight: 1.8, overflowX: "auto" }}>
        {`# pip install pyserial
import serial, time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

def read_sensors():
    line = ser.readline().decode('utf-8').strip()
    data = dict(p.split(':') for p in line.split('|') if ':' in line)
    return {k: float(v) for k, v in data.items()}

while True:
    print(read_sensors())
    time.sleep(1)`}
      </div>
    </div>
  );
}

// ─── MAIN APP ─────────────────────────────────────────────────────────────────
export default function AgroVision() {
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem("av_session") || "null"); } catch { return null; }
  });
  const [activeTab, setActiveTab] = useState("overview");
  const [sensors, setSensors] = useState(readSensors);

  useEffect(() => {
    const id = setInterval(() => setSensors(readSensors()), 10000);
    return () => clearInterval(id);
  }, []);

  function handleLogout() {
    localStorage.removeItem("av_session");
    setUser(null);
  }

  const CONTENT = {
    overview: <TabOverview sensors={sensors} user={user} />,
    "crop-health": <TabCropHealth sensors={sensors} />,
    "pest-disease": <TabPestDisease />,
    yield: <TabYield sensors={sensors} />,
    recommendations: <TabRecommendations sensors={sensors} />,
    "ai-advisor": <TabAiAdvisor sensors={sensors} />,
    hardware: <TabHardware sensors={sensors} />,
  };

  return (
    <>
      <style>{globalStyles}</style>
      {!user ? (
        <AuthScreen onAuth={setUser} />
      ) : (
        <div style={{ display: "flex", height: "100vh", overflow: "hidden" }}>
          <Sidebar sensors={sensors} activeTab={activeTab} setActiveTab={setActiveTab} user={user} onLogout={handleLogout} />
          <main style={{ flex: 1, overflowY: "auto", padding: "28px 28px" }}>
            {CONTENT[activeTab]}
          </main>
        </div>
      )}
    </>
  );
}