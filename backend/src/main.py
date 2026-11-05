
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


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "random_forest_aqi.joblib"
FEATURE_PATH = PROJECT_ROOT / "models" / "feature_names.txt"
BENCHMARK_PATH = PROJECT_ROOT / "report" / "final_evaluation.csv"


# --------------------------------------------------
# LOAD TRAINED MODEL
# --------------------------------------------------

model = joblib.load(MODEL_PATH)

FEATURES = FEATURE_PATH.read_text(
    encoding="utf-8"
).splitlines()


# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="AQI Forecaster API",
    description=(
        "Predict next-day AQI using a trained Random Forest model "
        "and historical city-level air-quality data."
    ),
    version="1.2.0",
)


# --------------------------------------------------
# INPUT VALIDATION
# --------------------------------------------------

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


# --------------------------------------------------
# HOME ENDPOINT
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "AQI Forecaster API is running.",
        "docs": "/docs",
        "available_endpoints": [
            "/health",
            "/predict",
            "/forecast/{city}",
            "/benchmarks",
        ],
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "feature_count": len(FEATURES),
    }


# --------------------------------------------------
# MODEL BENCHMARKS
# --------------------------------------------------

@app.get("/benchmarks")
def get_model_benchmarks():

    if not BENCHMARK_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Model evaluation report not found."
        )

    try:
        df = pd.read_csv(BENCHMARK_PATH)

        required_columns = [
            "split",
            "rows",
            "cities",
            "rf_mae",
            "rf_rmse",
            "rf_r2",
            "baseline_mae",
            "baseline_rmse",
            "baseline_r2",
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Evaluation report is missing required columns.",
                    "missing_columns": missing_columns,
                }
            )

        benchmarks = {}

        for _, row in df.iterrows():

            split_name = str(row["split"]).strip().upper()

            if "TEST A" in split_name:
                result_key = "test_a_unseen_cities"

            elif "TEST B" in split_name:
                result_key = "test_b_future_dates"

            else:
                continue

            benchmarks[result_key] = {
                "split": str(row["split"]),
                "evaluation_rows": int(row["rows"]),
                "cities": int(row["cities"]),

                "random_forest": {
                    "mae": round(float(row["rf_mae"]), 2),
                    "rmse": round(float(row["rf_rmse"]), 2),
                    "r2": round(float(row["rf_r2"]), 4),
                },

                "persistence_baseline": {
                    "mae": round(float(row["baseline_mae"]), 2),
                    "rmse": round(float(row["baseline_rmse"]), 2),
                    "r2": round(float(row["baseline_r2"]), 4),
                },
            }

        if not benchmarks:
            raise HTTPException(
                status_code=500,
                detail="No valid benchmark results found."
            )

        return {
            "model": "RandomForestRegressor",
            "evaluation_source": "final_evaluation.csv",
            "unit": "AQI points for MAE and RMSE",

            "metrics_explanation": {
                "MAE": "Mean Absolute Error. Lower is better.",
                "RMSE": "Root Mean Squared Error. Lower is better.",
                "R2": "Coefficient of determination. Higher is better.",
            },

            "benchmarks": benchmarks,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to load model benchmarks: {str(exc)}"
        ) from exc


# --------------------------------------------------
# MANUAL PREDICTION ENDPOINT
# --------------------------------------------------

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


# --------------------------------------------------
# AUTOMATIC CITY-BASED FORECASTING
# --------------------------------------------------

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
