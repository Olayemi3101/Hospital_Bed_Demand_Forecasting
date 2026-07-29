# 🏥 Hospital Bed Demand Forecasting System

## Overview

The Hospital Bed Demand Forecasting System is an end-to-end predictive analytics solution developed for **Albion Care Network** to support proactive hospital capacity planning.

The project forecasts future bed occupancy across multiple hospitals and wards using time-series forecasting and machine learning models, helping operational teams manage capacity, staffing, and patient flow more effectively.

The solution includes:

- Data preprocessing
- Statistical checks
- Forecasting model development
- Model evaluation and selection
- Scenario analysis
- Staffing feasibility analysis
- Interactive Streamlit dashboard
- FastAPI REST API for system integration

---


# Objectives

The system aims to:

- Forecast future hospital bed occupancy
- Compare multiple forecasting models
- Automatically select the best-performing model for each ward
- Simulate future demand under stress scenarios
- Evaluate staffing feasibility
- Monitor overcapacity risk
- Provide operational decision support through dashboards and APIs

---

# Dataset

The project uses historical operational hospital data including:

### Bed Inventory & Occupancy

- Hospital
- Ward
- Bed Type
- Total Beds
- Staffed Beds
- Occupied Beds
- Closed Beds
- Occupancy Rate

---

### Admissions & Discharges

- Admission Date
- Discharge Date
- Hospital
- Ward
- Length of Stay

---

### Staffing

- Planned Staff
- Actual Staff
- Staff Role
- Safe Staffing Ratio

---
## 🏥 Hospitals Included

- Horizon Birmingham (HHN-BIR-01)
- Horizon Edinburgh (HHN-EDI-01)
- Horizon London Central (HHN-LON-01)
- Horizon London South (HHN-LON-02)
- Horizon Manchester (HHN-MAN-01)

---

## 🏨 Wards Included

- Cardiology Ward
- General Medicine Ward A
- General Medicine Ward B
- ICU
- Oncology Ward
- Orthopaedics Ward A
- Orthopaedics Ward B
- Day Case Unit

---

# Forecasting Models

Several forecasting techniques were developed and evaluated.

## Baseline Models

- Holt-Winters
- SARIMA

## Advanced Models

- SARIMAX
- XGBoost

Each ward is automatically assigned the model with the lowest forecasting error.

---

# Model Evaluation

Models were evaluated using:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Mean Absolute Percentage Error (MAPE)

The best-performing model for each ward is stored in:

```
Models/
    Best Models/
        Best Models Results/
```

---

# Scenario Analysis

Demand stress testing evaluates future occupancy under increasing demand.

Scenarios include:

- Baseline
- +10% Demand
- +20% Demand
- +30% Demand

Outputs include:

- Forecast Demand
- Occupancy Percentage
- Capacity Breach Flags

---

# Staffing Alignment

Forecast demand is compared against staffing capacity.

Measures include:

- Planned Staff
- Actual Staff
- Beds per Staff Member
- Safe Staffing Ratio
- Operational Feasibility

Possible outcomes:

- Safe
- Monitor
- Critical

---

# Continuous Learning

Model performance is continuously monitored using:

- MAE
- RMSE
- MAPE

Additional functionality includes:

- Prediction vs Actual monitoring
- Drift Detection
- Retraining Recommendation

---

# Streamlit Dashboard

The dashboard provides interactive operational monitoring.

## Features

- Current Ward Status
- Historical Occupancy
- Forecast vs Actual
- Admissions & Discharges
- Capacity Risk
- Occupancy Alerts
- Scenario Analysis
- Staffing Alignment
- Planner Workflow
- Continuous Learning
- Drift Detection
- Retraining Recommendations
- Planner Summary

### Filters

- Hospital
- Ward
- Bed Type
- Forecast Horizon

---

# FastAPI

Forecasts are exposed through REST APIs for integration with other hospital systems.

## Available Endpoints

### Forecast

```
GET /forecast
```

Returns best model predictions.

---

### Scenario Analysis

```
GET /scenario
```

Returns stress-testing results.

---

### Staffing

```
GET /staffing
```

Returns staffing feasibility results.

---

### Best Models

```
GET /best_models
```

Returns the selected model for every hospital ward.

---

# Running the Streamlit Dashboard

Navigate to the App folder:

```bash
cd App
```

Run:

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser.

---

# Running the API

Navigate to the API folder:

```bash
cd API
```

Start the server:

```bash
uvicorn api:app --reload
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

# Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Statsmodels
- XGBoost
- Plotly
- Streamlit
- FastAPI
- Joblib

---

# Key Outputs

The project generates:

- Forecasted Bed Demand
- Best Model Predictions
- Scenario Analysis Results
- Staffing Alignment Results
- Capacity Risk Indicators
- Interactive Dashboard
- REST API

---

# Future Improvements

Potential future enhancements include:

- Real-time hospital data integration
- Automated scheduled retraining
- Live API deployment
- Cloud deployment
- Integration with electronic health records (EHR)
- Explainable AI for forecasting decisions
---

# Author

**Olayemi Balogun**

MSc Data Science Project

Hospital Bed Demand Forecasting System

2026

---

# 📄 License

This project is provided for educational and portfolio purposes.