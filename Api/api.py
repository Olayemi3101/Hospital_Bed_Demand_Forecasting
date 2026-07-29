from pathlib import Path

import pandas as pd

from fastapi import FastAPI

app = FastAPI(
    title="Hospital Bed Forecast API",
    version="1.0"
)

PROJECT = Path(__file__).resolve().parent.parent

forecast_file = (
    PROJECT /
    "Models" /
    "Best Models" /
    "Best Models Predictions" /
    "best_models_predictions.csv"
)

forecast = pd.read_csv(forecast_file)

forecast["date"] = pd.to_datetime(
    forecast["date"]
)

@app.get("/")
def home():

    return {

        "message":
        "Albion Care Network Forecast API"

    }

@app.get("/forecast")
def get_forecasts():

    return forecast.to_dict(
        orient="records"
    )

@app.get("/forecast/{hospital}")
def hospital_forecast(hospital: str):

    data = forecast[

        forecast["hospital_id"] == hospital

    ]

    return data.to_dict(
        orient="records"
    )

@app.get("/forecast/{hospital}/{unit}")
def ward_forecast(
    hospital: str,
    unit: str
):

    unit_name = hospital + "_" + unit

    data = forecast[

        forecast["unit"] == unit_name

    ]

    return data.to_dict(
        orient="records"
    )

best_model_file = (
    PROJECT /
    "Models" /
    "Best Models" /
    "Best Models Results" /
    "best_models.csv"
)

best_models = pd.read_csv(
    best_model_file
)

@app.get("/models")
def models():

    return best_models.to_dict(
        orient="records"
    )

scenario_file = (
    PROJECT /
    "Scenario Analysis" /
    "scenario_analysis.csv"
)

scenario = pd.read_csv(
    scenario_file
)

@app.get("/scenario")
def scenario_results():

    return scenario.to_dict(
        orient="records"
    )

staffing_file = (
    PROJECT /
    "Staffing Analysis" /
    "staffing_alignment_detailed.csv"
)

staffing = pd.read_csv(
    staffing_file
)

@app.get("/staffing")
def staffing_results():

    return staffing.to_dict(
        orient="records"
    )