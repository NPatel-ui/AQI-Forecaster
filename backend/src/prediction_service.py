
from pathlib import Path

import joblib
import pandas as pd

try:
    from .data_service import get_city_features
except ImportError:
    from data_service import get_city_features


# Project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Saved model and feature names
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


def load_model():
    """Load the already-trained Random Forest pipeline."""

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


# Load the model once when this module is imported
MODEL, MODEL_FEATURES = load_model()


def predict_city_aqi(city: str, selected_date=None):
    """
    Predict next-day AQI for a selected city
    using historical dataset features.
    """

    # Retrieve city-specific features
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

    # Convert features into a DataFrame
    input_data = pd.DataFrame([feature_values])

    # Generate prediction
    prediction = MODEL.predict(input_data)[0]

    return {
        "city": city_data["city"],
        "feature_date": city_data["feature_date"],
        "prediction_for_date": city_data["prediction_for_date"],
        "observed_aqi_on_feature_date": (
            city_data["observed_aqi_on_feature_date"]
        ),
        "predicted_next_day_aqi": round(float(prediction), 2),
        "model": "Random Forest Regressor",
        "data_mode": "historical"
    }
