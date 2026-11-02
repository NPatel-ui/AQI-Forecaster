
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ==========================================
# PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FEATURE_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "daily_features.csv"
)

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "city_day_stage1.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "random_forest_aqi.joblib"
)

FEATURE_NAMES_PATH = (
    PROJECT_ROOT
    / "models"
    / "feature_names.txt"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "report"
    / "city_forecast_validation.csv"
)


# ==========================================
# HELD-OUT CITIES
# ==========================================

TEST_CITIES = [
    "Chennai",
    "Hyderabad",
    "Kolkata",
    "Lucknow",
    "Visakhapatnam"
]


# ==========================================
# LOAD MODEL AND DATA
# ==========================================

print("\n========== LOADING MODEL AND DATA ==========")

model = joblib.load(MODEL_PATH)

features = [
    line.strip()
    for line in FEATURE_NAMES_PATH.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

feature_data = pd.read_csv(FEATURE_DATA_PATH)
raw_data = pd.read_csv(RAW_DATA_PATH)

feature_data["Date"] = pd.to_datetime(
    feature_data["Date"],
    errors="coerce"
)

raw_data["Date"] = pd.to_datetime(
    raw_data["Date"],
    errors="coerce"
)

print("Model loaded successfully.")
print("Feature dataset:", feature_data.shape)
print("Raw dataset:", raw_data.shape)
print("Model features:", len(features))


# ==========================================
# CHECK REQUIRED COLUMNS
# ==========================================

required_feature_columns = [
    "City",
    "Date"
] + features

missing_feature_columns = [
    column
    for column in required_feature_columns
    if column not in feature_data.columns
]

if missing_feature_columns:
    raise ValueError(
        f"Missing feature dataset columns: "
        f"{missing_feature_columns}"
    )

if not {"City", "Date", "AQI"}.issubset(raw_data.columns):
    raise ValueError(
        "Raw dataset must contain City, Date and AQI columns."
    )


# ==========================================
# PREPARE ACTUAL NEXT-DAY AQI
# ==========================================

print("\n========== PREPARING ACTUAL AQI ==========")

actual_data = raw_data[
    ["City", "Date", "AQI"]
].copy()

actual_data = actual_data.dropna(
    subset=["City", "Date", "AQI"]
)

# Each actual AQI reading becomes the target
# for the previous calendar day's features.
actual_data["feature_date"] = (
    actual_data["Date"] - pd.Timedelta(days=1)
)

actual_data = actual_data.rename(
    columns={
        "Date": "actual_date",
        "AQI": "actual_next_day_aqi"
    }
)

actual_data = actual_data[
    [
        "City",
        "feature_date",
        "actual_date",
        "actual_next_day_aqi"
    ]
]


# ==========================================
# MATCH FEATURES WITH ACTUAL NEXT-DAY AQI
# ==========================================

feature_data = feature_data.rename(
    columns={"Date": "feature_date"}
)

validation_data = feature_data.merge(
    actual_data,
    on=["City", "feature_date"],
    how="inner",
    validate="one_to_one"
)

# Keep only the cities held out during training.
validation_data = validation_data[
    validation_data["City"].isin(TEST_CITIES)
].copy()

# Current AQI is necessary for a forecast.
validation_data = validation_data.dropna(
    subset=["aqi_today", "actual_next_day_aqi"]
)

validation_data = validation_data.sort_values(
    ["City", "feature_date"]
).reset_index(drop=True)

if validation_data.empty:
    raise ValueError(
        "No eligible validation records were found."
    )

print("Eligible validation records:", len(validation_data))
print("Cities:", validation_data["City"].nunique())


# ==========================================
# GENERATE PREDICTIONS
# ==========================================

print("\n========== GENERATING PREDICTIONS ==========")

X = validation_data[features]

actual = validation_data[
    "actual_next_day_aqi"
].to_numpy()

predicted = model.predict(X)

validation_data["predicted_next_day_aqi"] = predicted

validation_data["absolute_error"] = np.abs(
    actual - predicted
)

print("Predictions generated:", len(predicted))


# ==========================================
# OVERALL EVALUATION
# ==========================================

mae = mean_absolute_error(
    actual,
    predicted
)

rmse = np.sqrt(
    mean_squared_error(actual, predicted)
)

r2 = r2_score(
    actual,
    predicted
)

print("\n========== OVERALL RESULTS ==========")

print("Total predictions:", len(actual))
print("MAE:", round(mae, 4))
print("RMSE:", round(rmse, 4))
print("R2 Score:", round(r2, 4))


# ==========================================
# CITY-WISE EVALUATION
# ==========================================

print("\n========== CITY-WISE RESULTS ==========")

for city in TEST_CITIES:

    city_data = validation_data[
        validation_data["City"] == city
    ]

    if city_data.empty:
        print(f"\n{city}: No eligible records")
        continue

    city_actual = city_data[
        "actual_next_day_aqi"
    ]

    city_predicted = city_data[
        "predicted_next_day_aqi"
    ]

    city_mae = mean_absolute_error(
        city_actual,
        city_predicted
    )

    city_rmse = np.sqrt(
        mean_squared_error(
            city_actual,
            city_predicted
        )
    )

    city_r2 = (
        r2_score(city_actual, city_predicted)
        if len(city_data) >= 2
        else float("nan")
    )

    print(f"\nCity: {city}")
    print("Records:", len(city_data))
    print("MAE:", round(city_mae, 4))
    print("RMSE:", round(city_rmse, 4))
    print("R2 Score:", round(city_r2, 4))


# ==========================================
# SAVE VALIDATION RESULTS
# ==========================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

validation_data.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n========== VALIDATION COMPLETED ==========")
print("Results saved to:", OUTPUT_PATH)
