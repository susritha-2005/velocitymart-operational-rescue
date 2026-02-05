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
# LOAD DATA (ROOT FILES)
# =========================
sku = pd.read_csv("sku_master_clean.csv")
temp_violations = pd.read_csv("temperature_violations.csv")
high_risk_temp = pd.read_csv("high_risk_temperature_violations.csv")
weight_violations = pd.read_csv("weight_violations.csv")
avg_picker_load = pd.read_csv("average_picker_load.csv")

# =========================
# GLOBAL STYLES (UI/UX)
# =========================
st.markdown("""
<style>
.main { background-color: #f6f8fc; }

.hero {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    padding: 40px;
    border-radius: 20px;
    color: white;
    margin-bottom: 35px;
}

.hero-badge {
    display: inline-block;
    background: #22c55e;
    color: #052e16;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 10px;
}

.hero-title {
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 16px;
    color: #cbd5e1;
    max-width: 950px;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    margin: 40px 0 18px 0;
    color: #0f172a;
}

.section-subtitle {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 20px;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 8px 22px rgba(0,0,0,0.06);
}

.metric-label {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
}

.card {
    background: white;
    padding: 26px;
    border-radius: 20px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.06);
}

.insight {
    background: #f1f5f9;
    border-left: 6px solid #3b82f6;
    padding: 14px 18px;
    border-radius: 12px;
    font-size: 14px;
    color: #0f172a;
    margin-top: 14px;
}

.footer {
    margin-top: 50px;
    padding: 20px;
    text-align: center;
    font-size: 13px;
    color: #64748b;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HERO HEADER
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-badge">Operational Diagnostic Dashboard</div>
    <div class="hero-title">VelocityMart Warehouse Intelligence</div>
    <div class="hero-subtitle">
        A decision-support system built to diagnose warehouse chaos, identify
        operational bottlenecks, and recommend high-impact corrective actions
        under real-world constraints.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI SECTION
# =========================
st.markdown('<div class="section-title">Key Risk Indicators</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">High-level metrics highlighting operational instability</div>', unsafe_allow_html=True)

estimated_spoilage_value = len(temp_violations) * 500

c1, c2, c3, c4, c5, c6 = st.columns(6)

def metric(label, value, color):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{color};">{value}</div>
    </div>
    """

with c1: st.markdown(metric("Total SKUs", len(sku), "#0f172a"), unsafe_allow_html=True)
with c2: st.markdown(metric("Temp Violations", len(temp_violations), "#dc2626"), unsafe_allow_html=True)
with c3: st.markdown(metric("High-Risk SKUs", len(high_risk_temp), "#f97316"), unsafe_allow_html=True)
with c4: st.markdown(metric("Weight Violations", len(weight_violations), "#eab308"), unsafe_allow_html=True)
with c5: st.markdown(metric("Ghost Inventory", 0, "#16a34a"), unsafe_allow_html=True)
with c6: st.markdown(metric("Spoilage Risk (₹)", f"{estimated_spoilage_value:,}", "#991b1b"), unsafe_allow_html=True)

# =========================
# ROOT CAUSE ANALYSIS
# =========================
st.markdown('<div class="section-title">Root Cause Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Why fulfillment delays and spoilage are occurring</div>', unsafe_allow_html=True)

left, right = st.columns([1.3, 1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    correct = len(sku) - len(temp_violations)
    incorrect = len(temp_violations)

    fig, ax = plt.subplots(figsize=(5,4))
    ax.bar(["Correct", "Incorrect"], [correct, incorrect], color=["#22c55e", "#ef4444"])
    ax.set_ylabel("SKUs")
    ax.set_title("Temperature Compliance Overview")
    st.pyplot(fig)

    st.markdown("""
    <div class="insight">
    <b>Insight:</b> Temperature misplacement affects a majority of SKUs,
    driving spoilage risk and repeated picker re-routing.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    cat_counts = high_risk_temp.groupby("temp_req").size().reset_index(name="count")

    fig, ax = plt.subplots(figsize=(5,4))
    ax.bar(cat_counts["temp_req"], cat_counts["count"], color="#fb923c")
    ax.set_title("High-Risk Violations by Temperature Type")
    ax.set_ylabel("SKUs")
    st.pyplot(fig)

    st.markdown("""
    <div class="insight">
    <b>Insight:</b> High-velocity SKUs dominate violations, amplifying
    downstream fulfillment delays.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# OPERATIONAL CONSTRAINTS
# =========================
st.markdown('<div class="section-title">Operational & Safety Constraints</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Physical and labor constraints limiting throughput</div>', unsafe_allow_html=True)

a, b = st.columns(2)

with a:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(5,4))
    ax.bar(weight_violations["current_slot"], weight_violations["weight_kg"], color="#fde047")
    if len(weight_violations) > 0:
        ax.axhline(weight_violations["max_weight_kg"].mean(), linestyle="--", color="red")
    ax.set_title("Slot Weight Capacity Breaches")
    ax.set_ylabel("Weight (kg)")
    st.pyplot(fig)

    st.markdown("""
    <div class="insight">
    <b>Insight:</b> Even limited safety violations pose disproportionate risk
    to operations and worker safety.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with b:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    colors = ["#ef4444" if aisle == "B" else "#60a5fa" for aisle in avg_picker_load["aisle_id"]]
    fig, ax = plt.subplots(figsize=(5,4))
    ax.bar(avg_picker_load["aisle_id"], avg_picker_load["avg_pickers"], color=colors)
    ax.set_title("Average Picker Load by Aisle")
    ax.set_ylabel("Pickers")
    st.pyplot(fig)

    st.markdown("""
    <div class="insight">
    <b>Insight:</b> Aisle B behaves as a bottleneck and forklift dead-zone
    under peak picker density.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# EXECUTIVE CONCLUSION
# =========================
st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)

st.success(
    "VelocityMart’s operational instability is primarily driven by temperature misplacement "
    "of high-velocity SKUs. Corrective re-slotting, constrained by safety and forklift rules, "
    "offers the highest ROI path to stabilization."
)

st.warning(
    "Forklift Constraint: Forklifts are restricted from entering Aisle B when more than "
    "two pickers are present, creating a throughput dead-zone during peak periods."
)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
    Built for the VelocityMart Warehouse Chaos Challenge • Data-driven • Constraint-aware • Action-oriented
</div>
""", unsafe_allow_html=True)
