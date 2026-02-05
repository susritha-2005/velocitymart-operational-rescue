import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="VelocityMart | Warehouse Intelligence",
    page_icon="📦",
    layout="wide"
)

# =========================
# LOAD DATA (UNCHANGED)
# =========================
sku = pd.read_csv("sku_master_clean.csv")
temp_violations = pd.read_csv("temperature_violations.csv")
high_risk_temp = pd.read_csv("high_risk_temperature_violations.csv")
weight_violations = pd.read_csv("weight_violations.csv")
avg_picker_load = pd.read_csv("average_picker_load.csv")

estimated_spoilage_value = len(temp_violations) * 500

# =========================
# GLOBAL UI STYLES (ONLY UI)
# =========================
st.markdown("""
<style>
.main { background-color: #f9fafb; }

.page {
    max-width: 1200px;
    margin: auto;
}

.header {
    padding: 20px 0 30px 0;
}

.title {
    font-size: 36px;
    font-weight: 700;
    color: #020617;
}

.subtitle {
    font-size: 16px;
    color: #475569;
    max-width: 900px;
}

.divider {
    height: 1px;
    background: #e5e7eb;
    margin: 45px 0 35px 0;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    color: #020617;
    margin-bottom: 20px;
}

.card {
    background: white;
    padding: 26px;
    border-radius: 18px;
    box-shadow: 0px 8px 22px rgba(0,0,0,0.05);
    height: 100%;
}

.kpi-value {
    font-size: 34px;
    font-weight: 700;
    color: #020617;
}

.kpi-label {
    font-size: 14px;
    color: #64748b;
}

.insight {
    margin-top: 12px;
    font-size: 14px;
    color: #475569;
    line-height: 1.6;
}

.footer-note {
    margin-top: 35px;
    padding: 18px;
    background-color: #f1f5f9;
    border-left: 4px solid #2563eb;
    border-radius: 10px;
    font-size: 14px;
    color: #334155;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div class="page">
<div class="header">
    <div class="title">VelocityMart Warehouse Operations Dashboard</div>
    <div class="subtitle">
        Executive-level operational intelligence designed to surface
        systemic inefficiencies, safety risks, and fulfillment bottlenecks.
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI SECTION (SAME VALUES)
# =========================
st.markdown('<div class="page">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Key Operational Indicators</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)

def kpi(label, value):
    return f"""
    <div class="card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """

with c1: st.markdown(kpi("Total SKUs", len(sku)), unsafe_allow_html=True)
with c2: st.markdown(kpi("Temperature Violations", len(temp_violations)), unsafe_allow_html=True)
with c3: st.markdown(kpi("High-Risk SKUs", len(high_risk_temp)), unsafe_allow_html=True)
with c4: st.markdown(kpi("Weight Violations", len(weight_violations)), unsafe_allow_html=True)
with c5: st.markdown(kpi("Estimated Spoilage Risk", f"₹{estimated_spoilage_value:,}"), unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================
# TEMPERATURE ANALYSIS (UNCHANGED LOGIC)
# =========================
st.markdown('<div class="section-title">Temperature Compliance Analysis</div>', unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.bar(
        ["Compliant", "Violation"],
        [len(sku) - len(temp_violations), len(temp_violations)],
        color=["#c7d2fe", "#2563eb"]
    )
    ax.set_ylabel("SKU Count")
    ax.set_title("Temperature Placement Overview")
    st.pyplot(fig)

    st.markdown(
        "<div class='insight'>"
        "A majority of SKUs are stored outside their required temperature zones, "
        "introducing spoilage risk and operational rework."
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    cat_counts = high_risk_temp.groupby("temp_req").size().reset_index(name="count")

    fig, ax = plt.subplots()
    ax.bar(cat_counts["temp_req"], cat_counts["count"], color="#2563eb")
    ax.set_ylabel("Violations")
    ax.set_title("High-Risk Violations by Temperature Type")
    st.pyplot(fig)

    st.markdown(
        "<div class='insight'>"
        "High-velocity SKUs dominate temperature violations, magnifying their impact "
        "on daily fulfillment performance."
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================
# OPERATIONAL CONSTRAINTS (UNCHANGED)
# =========================
st.markdown('<div class="section-title">Operational & Safety Constraints</div>', unsafe_allow_html=True)

a, b = st.columns(2)

with a:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.bar(weight_violations["current_slot"], weight_violations["weight_kg"], color="#94a3b8")
    if len(weight_violations) > 0:
        ax.axhline(weight_violations["max_weight_kg"].mean(), linestyle="--")
    ax.set_ylabel("Weight (kg)")
    ax.set_title("Slot Weight Capacity Breaches")
    st.pyplot(fig)

    st.markdown(
        "<div class='insight'>"
        "While limited in count, weight violations pose direct safety and compliance risks."
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with b:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.bar(avg_picker_load["aisle_id"], avg_picker_load["avg_pickers"], color="#2563eb")
    ax.set_ylabel("Average Picker Load")
    ax.set_title("Picker Load by Aisle")
    st.pyplot(fig)

    st.markdown(
        "<div class='insight'>"
        "Aisle B consistently shows higher picker load, making it sensitive to "
        "forklift access constraints during peak periods."
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# EXECUTIVE SUMMARY (TEXT ONLY)
# =========================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-note">
<b>Key Takeaway:</b> Warehouse performance degradation is primarily driven by
misplaced high-velocity SKUs and localized labor congestion.
A targeted re-slotting strategy focused on temperature compliance and aisle
constraints can stabilize operations with minimal disruption.
<br><br>
<b>Operational Constraint:</b> Forklifts are restricted from entering Aisle B
when more than two pickers are present, creating a temporary movement dead-zone.
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
