# ==========================================================
# Albion Care Network
# Hospital Bed Demand Forecasting Dashboard
# ==========================================================

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------------

st.set_page_config(
    page_title="Hospital Bed Demand Forecasting",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Hospital Bed Demand Forecasting Dashboard")

st.markdown("""
This dashboard provides:

- Historical bed occupancy
- Best model forecasts
- Scenario analysis
- Staffing feasibility
- Capacity monitoring
""")

# ----------------------------------------------------------
# PROJECT PATH
# ----------------------------------------------------------

PROJECT = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------
# FILE PATHS
# ----------------------------------------------------------

occupancy_file = (
    PROJECT /
    "Data" /
    "Cleaned" /
    "bed_inventory_cleaned.csv"
)

admission_file = (
    PROJECT /
    "Data" /
    "Cleaned" /
    "admission_discharge_cleaned.csv"
)

forecast_file = (
    PROJECT /
    "Models" /
    "Best Models" /
    "Best Models Predictions" /
    "best_models_predictions.csv"
)

scenario_file = (
    PROJECT /
    "Scenario Analysis" /
    "scenario_analysis.csv"
)

staffing_file = (
    PROJECT /
    "Staffing Analysis" /
    "staffing_alignment_detailed.csv"
)

best_model_file = (
    PROJECT /
    "Models" /
    "Best Models" /
    "Best Models Results" /
    "best_models.csv"
)

monitoring_file = (
    PROJECT /
    "Monitoring" /
    "prediction_accuracy_monitoring.csv"
)

drift_file = (
    PROJECT /
    "Monitoring" /
    "drift_detection_results.csv"
)

retraining_file = (
    PROJECT /
    "Monitoring" /
    "retraining_log.csv"
)

# ----------------------------------------------------------
# CHECK FILES
# ----------------------------------------------------------

st.sidebar.header("Data Status")

files = {

    "Occupancy": occupancy_file,

    "Admissions": admission_file,

    "Forecast": forecast_file,

    "Scenario": scenario_file,

    "Staffing": staffing_file,

    "Best Models": best_model_file,

    "Monitoring": monitoring_file,

    "Drift": drift_file,

    "Retraining": retraining_file
}

for name, file in files.items():

    if file.exists():

        st.sidebar.success(f"{name} ✓")

    else:

        st.sidebar.error(f"{name} Missing")

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

@st.cache_data
def load_data():

    occupancy = pd.read_csv(occupancy_file)

    admissions = pd.read_csv(admission_file)

    forecast = pd.read_csv(forecast_file)

    scenario = pd.read_csv(scenario_file)

    staffing = pd.read_csv(staffing_file)

    best_models = pd.read_csv(best_model_file)

    monitoring = pd.read_csv(monitoring_file)

    drift = pd.read_csv(drift_file)

    retraining = pd.read_csv(retraining_file)

    return (

    occupancy,

    admissions,

    forecast,

    scenario,

    staffing,

    best_models,

    monitoring,

    drift,

    retraining

)

try:

    (
    occupancy,

    admissions,

    forecast,

    scenario,

    staffing,

    best_models,

    monitoring,

    drift,

    retraining

) = load_data()

except Exception as e:

    st.error("Unable to load data.")

    st.exception(e)

    st.stop()

# ----------------------------------------------------------
# DATE COLUMNS
# ----------------------------------------------------------

occupancy["datetime"] = pd.to_datetime(
    occupancy["datetime"]
)

forecast["date"] = pd.to_datetime(
    forecast["date"]
)

scenario["date"] = pd.to_datetime(
    scenario["date"]
)

staffing["date"] = pd.to_datetime(
    staffing["date"],
    dayfirst=True
)

admissions["admission_datetime"] = pd.to_datetime(
    admissions["admission_datetime"]
)

admissions["discharge_datetime"] = pd.to_datetime(
    admissions["discharge_datetime"]
)

# ----------------------------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------------------------

st.sidebar.header("Filters")

hospital = st.sidebar.selectbox(

    "Hospital",

    sorted(
        occupancy["hospital_id"].unique()
    )

)

ward = st.sidebar.selectbox(

    "Ward",

    sorted(

        occupancy[
            occupancy["hospital_id"] == hospital
        ]["ward"].unique()

    )

)

bed_type = st.sidebar.selectbox(

    "Patient Type",

    sorted(

        occupancy[
            (occupancy["hospital_id"] == hospital)
            &
            (occupancy["ward"] == ward)
        ]["bed_type"].unique()

    )

)

forecast_horizon = st.sidebar.selectbox(

    "Forecast Horizon",

    [
        7,
        14,
        30
    ]

)

selected_unit = hospital + "_" + ward

# ----------------------------------------------------------
# FILTER DATASETS
# ----------------------------------------------------------

occ = occupancy[

    (occupancy["hospital_id"] == hospital)
    &
    (occupancy["ward"] == ward)
    &
    (occupancy["bed_type"] == bed_type)

].copy()

forecast_df = forecast[

    forecast["unit"] == selected_unit

].copy()

scenario_df = scenario[

    scenario["unit"] == selected_unit

].copy()

staff_df = staffing[

    (staffing["hospital_id"] == hospital)
    &
    (staffing["unit"] == selected_unit)

].copy()

staff_df = staff_df.sort_values("date")

model_df = best_models[

    best_models["unit"] == selected_unit

].copy()

occ = occ.sort_values("datetime")

forecast_df = forecast_df.sort_values("date")

monitor_df = monitoring[

    monitoring["unit"] == selected_unit

].copy()

drift_df = drift[

    drift["unit"] == selected_unit

].copy()

retrain_df = retraining[

    retraining["unit"] == selected_unit

].copy()

# ----------------------------------------------------------
# DEBUG INFO
# ----------------------------------------------------------

with st.expander("Loaded Dataset Sizes"):

    st.write("Occupancy:", occ.shape)

    st.write("Forecast:", forecast_df.shape)

    st.write("Scenario:", scenario_df.shape)

    st.write("Staffing:", staff_df.shape)

    st.write("Model:", model_df.shape)

    # ----------------------------------------------------------
# CURRENT WARD STATUS
# ----------------------------------------------------------

st.header("Current Ward Status")

if occ.empty:

    st.warning("No occupancy data available.")

else:

    latest = occ.iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Occupied Beds",
            int(latest["occupied_beds"])
        )

    with col2:

        st.metric(
            "Total Beds",
            int(latest["total_beds"])
        )

    with col3:

        st.metric(
            "Occupancy Rate",
            f"{latest['occupancy_rate']:.1%}"
        )

    with col4:

        st.metric(
            "Closed Beds",
            int(latest["closed_beds"])
        )

        # ----------------------------------------------------------
# HISTORICAL OCCUPANCY
# ----------------------------------------------------------

st.header("Historical Occupancy")

if not occ.empty:

    fig = px.line(

        occ,

        x="datetime",

        y="occupied_beds",

        title="Historical Occupied Beds"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ----------------------------------------------------------
# FORECAST
# ----------------------------------------------------------

st.header("Forecast")

if forecast_df.empty:

    st.warning("No forecast available.")

else:

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=forecast_df["date"],

            y=forecast_df["actual"],

            mode="lines",

            name="Actual"

        )

    )

    fig.add_trace(

        go.Scatter(

            x=forecast_df["date"],

            y=forecast_df["predicted"],

            mode="lines",

            name="Forecast"

        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ----------------------------------------------------------
# PLANNER WORKFLOW
# ----------------------------------------------------------

st.header("🏥 Planner Workflow")

if forecast_df.empty:

    st.warning("No forecast available.")

else:

    latest_forecast = forecast_df.iloc[-1]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Forecast Beds",
            round(latest_forecast["predicted"], 1)
        )

    with col2:

        st.metric(
            "Current Beds",
            round(latest_forecast["actual"], 1)
        )

    with col3:

        difference = (
            latest_forecast["predicted"]
            - latest_forecast["actual"]
        )

        st.metric(
            "Expected Change",
            round(difference, 1)
        )

# ----------------------------------------------------------
# OCCUPANCY ALERTS
# ----------------------------------------------------------

st.header("🚨 Occupancy Alerts")

if occ.empty:

    st.warning("No occupancy data available.")

else:

    latest = occ.iloc[-1]

    occupancy = latest["occupancy_rate"]

    if occupancy < 0.80:
        st.success(f"Current Occupancy: {occupancy:.1%} (Low Risk)")
    elif occupancy < 0.90:
        st.warning(f"Current Occupancy: {occupancy:.1%} (Moderate Risk)")
    elif occupancy < 0.95:
        st.error(f"Current Occupancy: {occupancy:.1%} (High Risk)")
    else:
        st.error(f"Current Occupancy: {occupancy:.1%} (CRITICAL)")

# ----------------------------------------------------------
# FORECAST OVERCAPACITY
# ----------------------------------------------------------

st.header("📈 Forecast Capacity Risk")

if not scenario_df.empty:

    latest_forecast = scenario_df.iloc[-1]

    if latest_forecast["baseline_breach"]:

        st.error(
            "⚠️ Baseline forecast exceeds ward capacity."
        )

    if latest_forecast["stress_10_breach"]:

        st.warning(
            "⚠️ Capacity breach under +10% demand."
        )

    if latest_forecast["stress_20_breach"]:

        st.warning(
            "⚠️ Capacity breach under +20% demand."
        )

    if latest_forecast["stress_30_breach"]:

        st.error(
            "🚨 Severe breach under +30% demand."
        )

# ----------------------------------------------------------
# STAFFING ALERTS
# ----------------------------------------------------------

st.header("👨‍⚕️ Staffing Status")

if not staff_df.empty:

    latest_staff = staff_df.iloc[-1]

    st.metric(
        "Overall Status",
        latest_staff["overall_status"]
    )

    if latest_staff["overall_status"] != "Operationally Feasible":

        st.error(
            "Additional staff may be required."
        )

    else:

        st.success(
            "Current staffing supports forecast demand."
        )

# ----------------------------------------------------------
# PLANNER RECOMMENDATIONS
# ----------------------------------------------------------

st.header("📋 Operational Recommendations")

recommendations = []

if occupancy >= 0.95:

    recommendations.append(
        "Open escalation beds."
    )

if occupancy >= 0.90:

    recommendations.append(
        "Review discharge plans."
    )

if not staff_df.empty:

    if latest_staff["overall_status"] != "Operationally Feasible":

        recommendations.append(
            "Increase staffing levels."
        )

if not scenario_df.empty:

    if latest_forecast["stress_20_breach"]:

        recommendations.append(
            "Prepare overflow capacity."
        )

if len(recommendations) == 0:

    st.success(
        "No operational actions required."
    )

else:

    for item in recommendations:

        st.write("•", item)                            

    # ----------------------------------------------------------
# ADMISSIONS & DISCHARGES
# ----------------------------------------------------------

st.header("Admissions & Discharges")

adm = admissions[

    (admissions["hospital_id"] == hospital)

    &

    (admissions["ward"] == ward)

].copy()

if adm.empty:

    st.info("No admissions data.")

else:

    col1, col2 = st.columns(2)

    daily_adm = (

        adm.groupby("admission_datetime")

        .size()

        .reset_index(name="Admissions")

    )

    daily_dis = (

        adm.groupby("discharge_datetime")

        .size()

        .reset_index(name="Discharges")

    )

    with col1:

        fig = px.line(

            daily_adm,

            x="admission_datetime",

            y="Admissions",

            title="Daily Admissions"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.line(

            daily_dis,

            x="discharge_datetime",

            y="Discharges",

            title="Daily Discharges"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------------------------
# CAPACITY RISK
# ----------------------------------------------------------

st.header("Capacity Risk")

if occ.empty:

    st.warning("No occupancy data.")

else:

    latest = occ.iloc[-1]

    occupancy_rate = latest["occupancy_rate"]

    if occupancy_rate >= 0.95:

        risk = "🔴 Critical"

    elif occupancy_rate >= 0.90:

        risk = "🟠 High"

    elif occupancy_rate >= 0.80:

        risk = "🟡 Moderate"

    else:

        risk = "🟢 Low"

    st.metric(
        "Current Risk",
        risk
    )

# ----------------------------------------------------------
# SCENARIO ANALYSIS
# ----------------------------------------------------------

st.header("Scenario Analysis")

if scenario_df.empty:

    st.info("No scenario analysis available.")

else:

    st.dataframe(
        scenario_df,
        use_container_width=True
    )

    fig = go.Figure()

    # Baseline
    fig.add_trace(
        go.Scatter(
            x=scenario_df["date"],
            y=scenario_df["baseline_forecast"],
            mode="lines",
            name="Baseline"
        )
    )

    # +10%
    fig.add_trace(
        go.Scatter(
            x=scenario_df["date"],
            y=scenario_df["stress_10"],
            mode="lines",
            name="+10%"
        )
    )

    # +20%
    fig.add_trace(
        go.Scatter(
            x=scenario_df["date"],
            y=scenario_df["stress_20"],
            mode="lines",
            name="+20%"
        )
    )

    # +30%
    fig.add_trace(
        go.Scatter(
            x=scenario_df["date"],
            y=scenario_df["stress_30"],
            mode="lines",
            name="+30%"
        )
    )

    fig.update_layout(

        title="Forecast Demand Under Different Scenarios",

        xaxis_title="Date",

        yaxis_title="Forecast Beds"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Projected Occupancy (%)")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=scenario_df["date"],
        y=scenario_df["baseline_occupancy_pct"],
        name="Baseline"
    )
)

fig.add_trace(
    go.Scatter(
        x=scenario_df["date"],
        y=scenario_df["stress_10_pct"],
        name="+10%"
    )
)

fig.add_trace(
    go.Scatter(
        x=scenario_df["date"],
        y=scenario_df["stress_20_pct"],
        name="+20%"
    )
)

fig.add_trace(
    go.Scatter(
        x=scenario_df["date"],
        y=scenario_df["stress_30_pct"],
        name="+30%"
    )
)

fig.update_layout(
    yaxis_title="Occupancy (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

  # ----------------------------------------------------------
# STAFFING ALIGNMENT
# ----------------------------------------------------------

st.header("👩‍⚕️ Staffing Alignment")

if staff_df.empty:

    st.warning("No staffing information available.")

else:

    latest_staff = staff_df.iloc[-1]

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Planned Staff",
            int(latest_staff["planned_staff"])
        )

    with c2:

        st.metric(
            "Actual Staff",
            int(latest_staff["actual_staff"])
        )

    with c3:

        st.metric(
            "Safe Ratio",
            str(latest_staff["safe_ratio_met"])
        )

    with c4:

        st.metric(
            "Overall Status",
            latest_staff["overall_status"]
        )

    st.markdown("---")

    st.subheader("Forecast Demand vs Planned Staff")

    fig = px.line(

        staff_df,

        x="date",

        y=["predicted", "planned_staff"],

        markers=True,

        title="Forecast Occupancy vs Planned Staff"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Beds per Staff")

    fig = px.line(

        staff_df,

        x="date",

        y=[
            "beds_per_planned_staff",
            "beds_per_actual_staff"
        ],

        markers=True,

        title="Beds per Staff Member"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Operational Feasibility")

    fig = px.bar(

        staff_df,

        x="date",

        y="predicted",

        color="feasibility_flag",

        title="Forecast Demand coloured by Feasibility"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Detailed Staffing Results")

    st.dataframe(

        staff_df[[
            "date",
            "predicted",
            "planned_staff",
            "actual_staff",
            "safe_ratio_met",
            "feasibility_flag",
            "overall_status"
        ]],

        use_container_width=True

    )

# ----------------------------------------------------------
# CONTINUOUS LEARNING
# ----------------------------------------------------------

st.header("🔄 Continuous Learning & Model Monitoring")

if monitor_df.empty:

    st.warning("No monitoring results available.")

else:

    latest_monitor = monitor_df.iloc[0]

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "MAE",

            round(latest_monitor["MAE"],2)

        )

    with c2:

        st.metric(

            "RMSE",

            round(latest_monitor["RMSE"],2)

        )

    with c3:

        st.metric(

            "MAPE",

            f"{latest_monitor['MAPE']:.2f}%"

        )

st.subheader("Prediction Drift")

if drift_df.empty:

    st.info("No drift report available.")

else:

    latest_drift = drift_df.iloc[0]

    if latest_drift["Drift_Status"] == "DRIFT DETECTED":

        st.error("⚠ Prediction drift detected")

    else:

        st.success("Model performance remains stable")

    c1, c2 = st.columns(2)

    with c1:

        st.metric(

            "Rolling MAE",

            round(
                latest_drift["Current_Rolling_MAE"],
                2
            )

        )

    with c2:

        st.metric(

            "Baseline MAE",

            round(
                latest_drift["Baseline_Error"],
                2
            )

        )

st.subheader("Model Retraining")

if retrain_df.empty:

    st.info("No retraining information available.")

else:

    latest = retrain_df.iloc[0]

    if latest["Retraining_Recommendation"] == "RETRAIN MODEL":

        st.error("🔴 Retraining Recommended")

    else:

        st.success("🟢 Model Performing Well")

    st.write(

        "**Recommendation:**",

        latest["Retraining_Recommendation"]

    )

st.subheader("Prediction Error Over Time")

if forecast_df.empty:

    st.info("No prediction data available.")

else:

    errors = forecast_df.copy()

    errors["Absolute Error"] = (

    errors["actual"]

    -

    errors["predicted"]

).abs()

fig = px.line(

    errors,

    x="date",

    y="Absolute Error",

    markers=True,

    title="Prediction Error"

)

st.plotly_chart(

    fig,

    use_container_width=True

)


    # ----------------------------------------------------------
# DASHBOARD SUMMARY
# ----------------------------------------------------------

st.markdown("---")

st.markdown("""

## 📋 Dashboard Summary

This dashboard provides an integrated decision-support system for hospital bed management across Albion Care Network.

### Key Features

- 🏥 Current ward status and live bed occupancy
- 📈 Historical occupancy trends
- 🔮 Forecast vs Actual bed demand
- 🏥 Planner workflow for operational decision-making
- 🚨 Occupancy and overcapacity alerts
- 📊 Capacity risk monitoring
- 📥 Admissions and discharge trends
- 📈 Scenario analysis (+10%, +20%, +30% demand)
- 👩‍⚕️ Staffing alignment and operational feasibility
- 🤖 Best forecasting model selection
- 🔄 Continuous model monitoring using MAE, RMSE and MAPE
- 📉 Prediction drift detection
- 🔁 Automatic model retraining recommendations

### Purpose

The dashboard enables hospital planners to monitor current occupancy, evaluate future demand, identify operational risks, assess staffing adequacy, monitor forecasting performance over time, and determine when predictive models should be retrained to maintain forecasting accuracy.

""")


# ----------------------------------------------------------
# PLANNER SUMMARY
# ----------------------------------------------------------

st.header("📊 Planner Summary")

summary = pd.DataFrame({

    "Metric": [

        "Hospital",

        "Ward",

        "Current Occupancy",

        "Forecast Beds",

        "Best Model",

        "Staffing",

        "Risk",

        "MAE",

        "MAPE",

        "Drift",

        "Retraining"

    ],

    "Value": [

        hospital,

        ward,

        f"{occupancy:.1%}",

        round(latest_forecast["predicted"], 1),

        model_df.iloc[0]["model"] if not model_df.empty else "Unknown",

        latest_staff["overall_status"] if not staff_df.empty else "Unknown",

        "Critical" if occupancy >= 0.95
else "High" if occupancy >= 0.90
else "Moderate" if occupancy >= 0.80
else "Low",

round(latest_monitor["MAE"],2)
if not monitor_df.empty
else "N/A",

f"{latest_monitor['MAPE']:.2f}%"
if not monitor_df.empty
else "N/A",

latest_drift["Drift_Status"]
if not drift_df.empty
else "N/A",

latest["Retraining_Recommendation"]
if not retrain_df.empty
else "N/A"

    ]

})

st.dataframe(
    summary,
    use_container_width=True
)

