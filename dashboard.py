import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="VelocityMart | Operations War Room",
    page_icon="🚨",
    layout="wide"
)

# =========================
# LOAD DATA (ROOT)
# =========================
sku = pd.read_csv("sku_master_clean.csv")
temp_violations = pd.read_csv("temperature_violations.csv")
high_risk_temp = pd.read_csv("high_risk_temperature_violations.csv")
weight_violations = pd.read_csv("weight_violations.csv")
avg_picker_load = pd.read_csv("average_picker_load.csv")

# =========================
# CHAOS SCORE (EXECUTIVE METRIC)
# =========================
chaos_score = (
    0.5 * len(temp_violations) +
    0.3 * avg_picker_load["avg_pickers"].mean() * 10 +
    0.2 * len(weight_violations)
)

estimated_spoilage_value = len(temp_violations) * 500

# =========================
# GLOBAL STYLES (WAR ROOM)
# =========================
st.markdown("""
<style>
.main { background-color: #0b1220; color: #e5e7eb; }

.hero {
    background: linear-gradient(135deg, #7f1d1d, #1e293b);
    padding: 45px;
    border-radius: 22px;
    margin-bottom: 35px;
    border: 2px solid #ef4444;
}

.hero-title {
    font-size: 42px;
    font-weight: 900;
    color: #fee2e2;
}

.hero-subtitle {
    font-size: 17px;
    color: #fecaca;
    max-width: 1000px;
}

.alert {
    background: #7f1d1d;
    padding: 14px 20px;
    border-radius: 14px;
    font-weight: 700;
    color: #fee2e2;
    margin-top: 20px;
}

.section-title {
    font-size: 26px;
    font-weight: 800;
    margin: 45px 0 15px 0;
    color: #f9fafb;
}

.card {
    background: #111827;
    padding: 28px;
    border-radius: 20px;
    border: 1px solid #1f2937;
}

.metric {
    font-size: 42px;
    font-weight: 900;
}

.label {
    font-size: 14px;
    color: #9ca3af;
}

.insight {
    background: #020617;
    border-left: 6px solid #ef4444;
    padding: 16px;
    border-radius: 12px;
    margin-top: 14px;
}

.command {
    background: #052e16;
    border-left: 6px solid #22c55e;
    padding: 16px;
    border-radius: 12px;
    margin-top: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HERO — COMMAND CENTER
# =========================
st.markdown(f"""
<div class="hero">
    <div class="hero-title">🚨 VelocityMart Operations War Room</div>
    <div class="hero-subtitle">
        This command center visualizes real-time operational instability inside
        the VelocityMart warehouse. The objective is not reporting —
        it is <b>rapid decision-making under constraint</b>.
    </div>
    <div class="alert">
        CURRENT STATUS: OPERATIONALLY UNSTABLE — IMMEDIATE ACTION REQUIRED
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# EXECUTIVE SNAPSHOT
# =========================
st.markdown('<div class="section-title">Executive Snapshot</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"<div class='card'><div class='label'>Chaos Score</div><div class='metric' style='color:#ef4444'>{int(chaos_score)}</div></div>", unsafe_allow_html=True)

with c2:
    st.markdown(f"<div class='card'><div class='label'>Spoilage Risk</div><div class='metric' style='color:#fca5a5'>₹{estimated_spoilage_value:,}</div></div>", unsafe_allow_html=True)

with c3:
    st.markdown(f"<div class='card'><div class='label'>High-Risk SKUs</div><div class='metric' style='color:#fdba74'>{len(high_risk_temp)}</div></div>", unsafe_allow_html=True)

with c4:
    st.markdown(f"<div class='card'><div class='label'>Safety Violations</div><div class='metric' style='color:#fde047'>{len(weight_violations)}</div></div>", unsafe_allow_html=True)

# =========================
# FAILURE MECHANISM
# =========================
st.markdown('<div class="section-title">Failure Mechanism</div>', unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.bar(
        ["Compliant", "Temperature Violations"],
        [len(sku)-len(temp_violations), len(temp_violations)],
        color=["#22c55e", "#ef4444"]
    )
    ax.set_title("Temperature Compliance Breakdown")
    st.pyplot(fig)

    st.markdown("""
    <div class="insight">
    <b>Root Cause:</b> High-velocity SKUs are stored in incorrect temperature zones,
    forcing re-handling, spoilage, and picker re-routing.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    colors = ["#ef4444" if a == "B" else "#60a5fa" for a in avg_picker_load["aisle_id"]]
    fig, ax = plt.subplots()
    ax.bar(avg_picker_load["aisle_id"], avg_picker_load["avg_pickers"], color=colors)
    ax.set_title("Labor Pressure by Aisle")
    st.pyplot(fig)

    st.markdown("""
    <div class="insight">
    <b>Bottleneck:</b> Aisle B repeatedly enters a forklift dead-zone
    when picker density exceeds 2.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# WHAT HAPPENS IF WE DO NOTHING
# =========================
st.markdown('<div class="section-title">What Happens If We Do Nothing?</div>', unsafe_allow_html=True)

st.error("""
• Spoilage losses increase linearly  
• Picker congestion turns nonlinear  
• Forklift dead-zones compound delays  
• Fulfillment SLAs collapse under +20% demand
""")

# =========================
# EXECUTIVE ORDERS PANEL
# =========================
st.markdown('<div class="section-title">Immediate Executive Actions (Phase-1)</div>', unsafe_allow_html=True)

st.markdown("""
<div class="command">
1️⃣ Re-slot top 50 high-velocity SKUs into compliant temperature zones  
<br>2️⃣ Treat Aisle B as a restricted corridor during peak picker load  
<br>3️⃣ Prioritize safety-compliant bins over travel distance optimization  
<br>4️⃣ Stabilize operations before attempting throughput maximization
</div>
""", unsafe_allow_html=True)

# =========================
# FINAL MESSAGE
# =========================
st.success(
    "This is not a capacity problem. It is a placement and constraint-awareness problem. "
    "Corrective slotting yields the highest immediate ROI with minimal labor cost."
)
