import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="VelocityMart | Operations Control",
    page_icon="📦",
    layout="wide"
)

# =========================
# DATA
# =========================
sku = pd.read_csv("sku_master_clean.csv")
temp_violations = pd.read_csv("temperature_violations.csv")
high_risk_temp = pd.read_csv("high_risk_temperature_violations.csv")
weight_violations = pd.read_csv("weight_violations.csv")
avg_picker_load = pd.read_csv("average_picker_load.csv")

spoilage_risk = len(temp_violations) * 500

# =========================
# STYLES (PREMIUM)
# =========================
st.markdown("""
<style>
.main { background: #f9fafb; }

.hero {
    padding: 45px 20px 30px 20px;
    border-bottom: 1px solid #e5e7eb;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    color: #020617;
}

.hero-sub {
    font-size: 17px;
    color: #475569;
    max-width: 900px;
    margin-top: 8px;
}

.section {
    margin-top: 55px;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #020617;
    margin-bottom: 8px;
}

.section-sub {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 18px;
}

.card {
    background: white;
    padding: 26px;
    border-radius: 18px;
    box-shadow: 0px 8px 22px rgba(0,0,0,0.06);
}

.kpi {
    font-size: 36px;
    font-weight: 800;
    color: #020617;
}

.kpi-label {
    font-size: 13px;
    color: #64748b;
}

.divider {
    height: 1px;
    background: #e5e7eb;
    margin: 40px 0;
}

.callout {
    background: #f1f5f9;
    padding: 18px;
    border-left: 5px solid #2563eb;
    border-radius: 10px;
    font-size: 14px;
    color: #334155;
}

.decision {
    background: #ecfeff;
    padding: 18px;
    border-left: 5px solid #0891b2;
    border-radius: 10px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HERO
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-title">VelocityMart Operations Control Dashboard</div>
    <div class="hero-sub">
        This dashboard is designed as an operational control surface — not a report.
        It highlights where the warehouse breaks under pressure and what decisions
        stabilize performance fastest.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# SITUATION SNAPSHOT
# =========================
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Situation Snapshot</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Current operational health indicators</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

def kpi(label, value):
    return f"""
    <div class="card">
        <div class="kpi-label">{label}</div>
        <div class="kpi">{value}</div>
    </div>
    """

with c1: st.markdown(kpi("Total SKUs", len(sku)), unsafe_allow_html=True)
with c2: st.markdown(kpi("Temp Violations", len(temp_violations)), unsafe_allow_html=True)
with c3: st.markdown(kpi("High-Risk SKUs", len(high_risk_temp)), unsafe_allow_html=True)
with c4: st.markdown(kpi("Spoilage Exposure", f"₹{spoilage_risk:,}"), unsafe_allow_html=True)

# =========================
# WHERE IT BREAKS
# =========================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Where the System Breaks</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Primary failure mechanisms driving delays</div>', unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.bar(
        ["Correct", "Incorrect"],
        [len(sku)-len(temp_violations), len(temp_violations)],
        color=["#c7d2fe", "#2563eb"]
    )
    ax.set_title("Temperature Placement Integrity")
    st.pyplot(fig)
    st.markdown(
        "<div class='callout'>"
        "<b>Interpretation:</b> Misplaced high-velocity SKUs force repeated re-handling, "
        "creating cascading picker delays."
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.bar(avg_picker_load["aisle_id"], avg_picker_load["avg_pickers"], color="#2563eb")
    ax.set_title("Labor Load by Aisle")
    st.pyplot(fig)
    st.markdown(
        "<div class='callout'>"
        "<b>Interpretation:</b> Aisle B operates near saturation, amplifying forklift "
        "access restrictions."
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# DECISION ZONE
# =========================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Decision Zone</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">What improves stability fastest</div>', unsafe_allow_html=True)

st.markdown("""
<div class="decision">
<b>Phase-1 Recommendation (Next 7 Days):</b><br><br>
• Re-slot top 50 high-velocity SKUs into compliant temperature zones<br>
• Treat Aisle B as a controlled corridor during peak picker load<br>
• Prioritize safety and temperature compliance over travel distance optimization<br><br>
<b>Expected Outcome:</b> Lower spoilage risk, smoother picker flow, and
measurable fulfillment stability without infrastructure changes.
</div>
""", unsafe_allow_html=True)
