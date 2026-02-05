import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="VelocityMart | Warehouse Operations Intelligence",
    page_icon="📦",
    layout="wide"
)

# =========================
# LOAD DATA (DEPLOY-SAFE PATHS)
# =========================
sku = pd.read_csv("sku_master_clean.csv")
temp_violations = pd.read_csv("temperature_violations.csv")
high_risk_temp = pd.read_csv("high_risk_temperature_violations.csv")
weight_violations = pd.read_csv("weight_violations.csv")
avg_picker_load = pd.read_csv("average_picker_load.csv")

# =========================
# GLOBAL STYLES
# =========================
st.markdown("""
<style>
.main { background-color: #f5f7fb; }
.hero {
    background: linear-gradient(90deg, #0f172a, #1e293b);
    padding: 35px;
    border-radius: 18px;
    color: white;
    margin-bottom: 30px;
}
.hero-title { font-size: 34px; font-weight: 700; }
.hero-subtitle { font-size: 16px; color: #cbd5e1; max-width: 900px; }
.section-title { font-size: 22px; font-weight: 600; margin: 30px 0 15px 0; color: #0f172a; }
.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.06);
}
.metric-label { font-size: 14px; color: #64748b; }
.metric-value { font-size: 30px; font-weight: 700; }
.card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.06);
}
.caption { font-size: 13px; color: #64748b; margin-top: 8px; }
</style>
""", unsafe_allow_html=True)

# =========================
# HERO HEADER
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-title">VelocityMart Warehouse Operations Intelligence</div>
    <div class="hero-subtitle">
        A data-driven diagnostic dashboard to identify root causes of warehouse
        inefficiencies, operational risk, and fulfillment delays.
        <br><br>
        Powered by validated data forensics outputs and focused on actionable insights.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI SECTION
# =========================
st.markdown('<div class="section-title">Key Operational Risk Indicators</div>', unsafe_allow_html=True)

estimated_spoilage_value = len(temp_violations) * 500

c1, c2, c3, c4, c5, c6 = st.columns(6)

def metric(label, value, color=None):
    style = f"color:{color};" if color else ""
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="{style}">{value}</div>
    </div>
    """

with c1: st.markdown(metric("Total SKUs", len(sku)), unsafe_allow_html=True)
with c2: st.markdown(metric("Temperature Violations", len(temp_violations), "#dc2626"), unsafe_allow_html=True)
with c3: st.markdown(metric("High-Risk Violations", len(high_risk_temp), "#f97316"), unsafe_allow_html=True)
with c4: st.markdown(metric("Weight Violations", len(weight_violations), "#eab308"), unsafe_allow_html=True)
with c5: st.markdown(metric("Ghost Inventory", 0, "#16a34a"), unsafe_allow_html=True)
with c6: st.markdown(metric("Estimated Spoilage Risk", f"₹{estimated_spoilage_value:,}", "#991b1b"), unsafe_allow_html=True)

# =========================
# ROOT CAUSE ANALYSIS
# =========================
st.markdown('<div class="section-title">Root Cause Analysis — Temperature Misplacement</div>', unsafe_allow_html=True)

left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    correct = len(sku) - len(temp_violations)
    incorrect = len(temp_violations)

    fig, ax = plt.subplots()
    ax.bar(["Correct", "Incorrect"], [correct, incorrect], color=["#22c55e", "#ef4444"])
    ax.set_ylabel("Number of SKUs")
    st.pyplot(fig)
    st.markdown("<div class='caption'><b>Insight:</b> Over 60% of SKUs violate temperature rules.</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    cat_counts = high_risk_temp.groupby("temp_req").size().reset_index(name="count")
    fig, ax = plt.subplots()
    ax.bar(cat_counts["temp_req"], cat_counts["count"], color="#fb923c")
    ax.set_xlabel("Required Temperature Zone")
    ax.set_ylabel("Violations")
    st.pyplot(fig)
    st.markdown("<div class='caption'><b>Insight:</b> High-velocity SKUs dominate violations.</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# OPERATIONAL CONSTRAINTS
# =========================
st.markdown('<div class="section-title">Operational & Safety Constraints</div>', unsafe_allow_html=True)

a, b = st.columns(2)

with a:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.bar(weight_violations["current_slot"], weight_violations["weight_kg"], color="#fde047")
    if len(weight_violations) > 0:
        ax.axhline(weight_violations["max_weight_kg"].mean(), linestyle="--", color="red")
    ax.set_ylabel("Weight (kg)")
    ax.set_xlabel("Slot")
    st.pyplot(fig)
    st.markdown("<div class='caption'><b>Insight:</b> Localized slot capacity risks detected.</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with b:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    colors = ["#ef4444" if aisle == "B" else "#60a5fa" for aisle in avg_picker_load["aisle_id"]]
    fig, ax = plt.subplots()
    ax.bar(avg_picker_load["aisle_id"], avg_picker_load["avg_pickers"], color=colors)
    ax.set_xlabel("Aisle")
    ax.set_ylabel("Average Picker Load")
    ax.set_title("Aisle Load Heatmap (Relative)")
    st.pyplot(fig)
    st.markdown("<div class='caption'><b>Insight:</b> Aisle B is treated as a constrained aisle.</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# FINAL CONCLUSION
# =========================
st.markdown('<div class="section-title">Executive Conclusion</div>', unsafe_allow_html=True)

st.success(
    "Warehouse inefficiency is primarily driven by incorrect temperature placement "
    "of high-velocity SKUs. Strategic re-slotting will significantly reduce spoilage, "
    "picker congestion, and fulfillment delays."
)

st.warning(
    "Forklift Constraint: Forklifts are restricted from entering Aisle B when more than "
    "two pickers are present, creating a dead-zone under peak load conditions."
)
