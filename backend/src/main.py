
from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

# Support both package imports and direct script execution
try:
    from .prediction_service import predict_city_aqi
except ImportError:
    from prediction_service import predict_city_aqi


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT / "models" / "random_forest_aqi.joblib"
)

FEATURE_PATH = (
    PROJECT_ROOT / "models" / "feature_names.txt"
)


# Load the trained model and feature order
model = joblib.load(MODEL_PATH)

FEATURES = FEATURE_PATH.read_text(
    encoding="utf-8"
).splitlines()


# Create FastAPI application
app = FastAPI(
    title="AQI Forecaster API",
    description=(
        "Predict next-day AQI using a trained Random Forest model "
        "and historical city-level air-quality data."
    ),
    version="1.1.0",
)


# Validate manual prediction data
class AQIInput(BaseModel):
    aqi_today: float = Field(ge=0)
    aqi_1d_ago: float = Field(ge=0)
    aqi_2d_ago: float = Field(ge=0)
    aqi_7d_ago: float = Field(ge=0)
    roll3_mean: float = Field(ge=0)
    roll7_mean: float = Field(ge=0)
    roll7_std: float = Field(ge=0)
    change_1d: float

    PM2_5_today: float | None = Field(
        default=None,
        ge=0,
        alias="PM2.5_today"
    )

    PM10_today: float | None = Field(default=None, ge=0)
    NO2_today: float | None = Field(default=None, ge=0)
    CO_today: float | None = Field(default=None, ge=0)
    SO2_today: float | None = Field(default=None, ge=0)
    O3_today: float | None = Field(default=None, ge=0)

    month_sin: float = Field(ge=-1, le=1)
    month_cos: float = Field(ge=-1, le=1)
    day_of_week: int = Field(ge=0, le=6)


@app.get("/")
def home():
    return {
        "message": "AQI Forecaster API is running.",
        "docs": "/docs",
        "available_endpoints": [
            "/health",
            "/predict",
            "/forecast/{city}",
        ],
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "feature_count": len(FEATURES),
    }


# Existing manual prediction endpoint
@app.post("/predict")
def predict_aqi(data: AQIInput):

    try:
        values = data.model_dump(by_alias=True)

        input_df = pd.DataFrame(
            [values],
            columns=FEATURES
        )

        prediction = float(
            model.predict(input_df)[0]
        )

        return {
            "predicted_next_day_aqi": round(prediction, 2),
            "model": "RandomForestRegressor",
            "unit": "AQI points",
            "note": (
                "This is a model estimate, not an official monitoring-station "
                "measurement or medical assessment."
            ),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(exc)}",
        ) from exc


# New automatic city-based forecasting endpoint
@app.get("/forecast/{city}")
def forecast_city(
    city: str,
    date: str | None = Query(
        default=None,
        description=(
            "Optional historical feature date in YYYY-MM-DD format. "
            "If omitted, the latest usable historical record is selected."
        )
    )
):

    try:
        result = predict_city_aqi(
            city=city,
            selected_date=date
        )

        result["unit"] = "AQI points"

        result["note"] = (
            "Historical demonstration forecast. "
            "This is not a current live AQI forecast."
        )

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"City forecasting failed: {str(exc)}"
        ) from exc
