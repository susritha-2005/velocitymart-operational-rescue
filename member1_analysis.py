import pandas as pd
import numpy as np

# =========================
# STEP 1: LOAD DATA
# =========================
sku = pd.read_csv("sku_master.csv")
orders = pd.read_csv("order_transactions.csv")
picker = pd.read_csv("picker_movement.csv")
constraints = pd.read_csv("warehouse_constraints.csv")

print("✅ Data loaded successfully")

# =========================
# STEP 2: CLEAN SKU MASTER
# =========================
sku_clean = sku.drop_duplicates(subset="sku_id")
sku_clean = sku_clean[sku_clean["weight_kg"] > 0]

print("Original SKU count:", len(sku))
print("Clean SKU count:", len(sku_clean))

# =========================
# STEP 3: AUTO-DETECT DIMENSION COLUMNS
# =========================
dim_cols = []

for col in sku_clean.columns:
    if any(x in col.lower() for x in ["length", "width", "height", "depth"]):
        dim_cols.append(col)

if len(dim_cols) < 3:
    print("⚠️ Dimension columns not reliable — skipping volume-based drift detection")
    sku_clean["decimal_drift"] = False
else:
    # Take first 3 detected dimension columns
    l_col, w_col, h_col = dim_cols[:3]

    # Ensure numeric
    sku_clean[l_col] = pd.to_numeric(sku_clean[l_col], errors="coerce")
    sku_clean[w_col] = pd.to_numeric(sku_clean[w_col], errors="coerce")
    sku_clean[h_col] = pd.to_numeric(sku_clean[h_col], errors="coerce")

    sku_clean["volume"] = sku_clean[l_col] * sku_clean[w_col] * sku_clean[h_col]

    sku_clean = sku_clean[sku_clean["volume"] > 0]

    sku_clean["wt_vol_ratio"] = sku_clean["weight_kg"] / sku_clean["volume"]

    Q1 = sku_clean["wt_vol_ratio"].quantile(0.25)
    Q3 = sku_clean["wt_vol_ratio"].quantile(0.75)
    IQR = Q3 - Q1
    upper_limit = Q3 + 1.5 * IQR

    sku_clean["decimal_drift"] = sku_clean["wt_vol_ratio"] > upper_limit
    sku_clean.loc[sku_clean["decimal_drift"], "weight_kg"] /= 10

    print("Decimal drift corrected:", sku_clean["decimal_drift"].sum())

sku_clean.to_csv("sku_master_clean.csv", index=False)

# =========================
# STEP 4: SAFE TIMESTAMP HANDLING (ORDERS)
# =========================
order_time_col = None
for col in orders.columns:
    if "time" in col.lower() or "date" in col.lower():
        order_time_col = col
        break

if order_time_col is None:
    raise ValueError("❌ No timestamp column in order_transactions.csv")

orders["timestamp"] = pd.to_datetime(orders[order_time_col])

# =========================
# STEP 5: TEMPERATURE VIOLATIONS
# =========================
merged = sku_clean.merge(
    constraints,
    left_on="current_slot",
    right_on="slot_id",
    how="left"
)

temp_violations = merged[
    merged["temp_req"] != merged["temp_zone"]
]

temp_violations[
    ["sku_id", "temp_req", "temp_zone", "current_slot"]
].to_csv("temperature_violations.csv", index=False)

print("Temperature Violations:", len(temp_violations))

# =========================
# STEP 6: PRIORITIZE BY DEMAND
# =========================
order_counts = (
    orders.groupby("sku_id")
    .size()
    .reset_index(name="order_count")
)

temp_with_orders = temp_violations.merge(
    order_counts,
    on="sku_id",
    how="left"
).fillna(0)

high_risk_temp = temp_with_orders[temp_with_orders["order_count"] > 10]
high_risk_temp.to_csv("high_risk_temperature_violations.csv", index=False)

print("High-risk temperature violations:", len(high_risk_temp))

# =========================
# STEP 7: WEIGHT VIOLATIONS
# =========================
weight_violations = merged[
    merged["weight_kg"] > merged["max_weight_kg"]
]

weight_violations[
    ["sku_id", "weight_kg", "max_weight_kg", "current_slot"]
].to_csv("weight_violations.csv", index=False)

print("Weight Violations:", len(weight_violations))

# =========================
# STEP 8: GHOST INVENTORY
# =========================
ghost_inventory = sku_clean[
    ~sku_clean["current_slot"].isin(constraints["slot_id"])
]

ghost_inventory.to_csv("ghost_inventory.csv", index=False)
print("Ghost Inventory Count:", len(ghost_inventory))

# =========================
# STEP 9: TOP 20 FAST-MOVING SKUs
# =========================
top_skus = (
    orders.groupby("sku_id")
    .size()
    .reset_index(name="order_count")
    .sort_values("order_count", ascending=False)
    .head(20)
)

top_skus.to_csv("top_20_skus.csv", index=False)
print("Top 20 fast-moving SKUs saved")

# =========================
# STEP 10: PICKER CONGESTION ANALYSIS
# =========================
picker_time_col = None
for col in picker.columns:
    if "time" in col.lower() or "date" in col.lower():
        picker_time_col = col
        break

if picker_time_col is None:
    raise ValueError("❌ No timestamp column in picker_movement.csv")

picker["timestamp"] = pd.to_datetime(picker[picker_time_col])

picker_merged = (
    picker
    .merge(sku_clean[["sku_id", "current_slot"]], on="sku_id", how="left")
    .merge(
        constraints[["slot_id", "aisle_id"]],
        left_on="current_slot",
        right_on="slot_id",
        how="left"
    )
)

picker_counts = (
    picker_merged
    .groupby(["aisle_id", "timestamp"])
    .agg(picker_count=("picker_id", "nunique"))
    .reset_index()
)

aisle_b_violations = picker_counts[
    (picker_counts["aisle_id"] == "B") &
    (picker_counts["picker_count"] > 2)
]

aisle_b_violations.to_csv("aisle_b_congestion.csv", index=False)
print("Aisle B congestion violations:", len(aisle_b_violations))

# =========================
# STEP 11: CHAOS SCORE INPUTS
# =========================
avg_picker_load = (
    picker_merged
    .groupby("aisle_id")
    .agg(avg_pickers=("picker_id", "nunique"))
    .reset_index()
)

avg_picker_load.to_csv("average_picker_load.csv", index=False)

aisle_b_avg = avg_picker_load.loc[
    avg_picker_load["aisle_id"] == "B", "avg_pickers"
]

aisle_b_avg = aisle_b_avg.values[0] if not aisle_b_avg.empty else 0

chaos_inputs = {
    "temperature_violations": len(temp_violations),
    "high_risk_temp_violations": len(high_risk_temp),
    "weight_violations": len(weight_violations),
    "aisle_b_avg_picker_load": aisle_b_avg
}

print("🔥 Chaos Score Inputs:", chaos_inputs)
