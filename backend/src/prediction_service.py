
from pathlib import Path

import joblib
import pandas as pd

try:
    from .data_service import get_city_features
except ImportError:
    from data_service import get_city_features


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

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


# --------------------------------------------------
# LOAD TRAINED MODEL
# --------------------------------------------------

def load_model():
    """Load the trained Random Forest model and feature names."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    if not FEATURE_NAMES_PATH.exists():
        raise FileNotFoundError(
            f"Feature names file not found: {FEATURE_NAMES_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    with open(FEATURE_NAMES_PATH, "r", encoding="utf-8") as file:
        feature_names = [
            line.strip()
            for line in file
            if line.strip()
        ]

    if len(feature_names) != 17:
        raise ValueError(
            f"Expected 17 model features, found {len(feature_names)}."
        )

    return model, feature_names


# Load the model once when the module is imported
MODEL, MODEL_FEATURES = load_model()


# --------------------------------------------------
# CITY-BASED AQI PREDICTION
# --------------------------------------------------

def predict_city_aqi(city: str, selected_date=None):
    """
    Predict next-day AQI using historical city data.

    Returns:
        - Predicted AQI
        - Historical observed AQI
        - Actual pollutant readings
        - Forecast dates
        - Model information
    """

    # Retrieve city-specific historical features
    city_data = get_city_features(
        city=city,
        selected_date=selected_date
    )

    features = city_data["features"]

    # Arrange features in the exact training order
    feature_values = {
        name: features[name]
        for name in MODEL_FEATURES
    }

    # Check for missing model inputs
    missing_features = [
        name
        for name, value in feature_values.items()
        if value is None
    ]

    if missing_features:
        raise ValueError(
            "Cannot generate prediction because these model "
            f"features are missing: {missing_features}"
        )

    # Convert model inputs into a DataFrame
    input_data = pd.DataFrame(
        [feature_values],
        columns=MODEL_FEATURES
    )

    # Generate prediction
    prediction = MODEL.predict(input_data)[0]

    # Extract actual historical pollutant readings
    pollutant_features = {
        "PM2.5_today": features.get("PM2.5_today"),
        "PM10_today": features.get("PM10_today"),
        "NO2_today": features.get("NO2_today"),
        "CO_today": features.get("CO_today"),
        "SO2_today": features.get("SO2_today"),
        "O3_today": features.get("O3_today"),
    }

    return {
        "city": city_data["city"],

        "feature_date": city_data["feature_date"],

        "prediction_for_date": city_data["prediction_for_date"],

        "observed_aqi_on_feature_date": (
            city_data["observed_aqi_on_feature_date"]
        ),

        "predicted_next_day_aqi": round(
            float(prediction), 2
        ),

        "features": features,

        "pollutants": pollutant_features,

        "model": "Random Forest Regressor",

        "data_mode": "historical"
    }
