
from pathlib import Path

import pandas as pd
import requests


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "daily_features.csv"
API_URL = "http://127.0.0.1:8000/predict"

FEATURES = [
    "aqi_today",
    "aqi_1d_ago",
    "aqi_2d_ago",
    "aqi_7d_ago",
    "roll3_mean",
    "roll7_mean",
    "roll7_std",
    "change_1d",
    "PM2.5_today",
    "PM10_today",
    "NO2_today",
    "CO_today",
    "SO2_today",
    "O3_today",
    "month_sin",
    "month_cos",
    "day_of_week",
]

# The API uses this alias for the PM2.5 feature.
API_FEATURE_NAMES = {
    "PM2.5_today": "PM2.5_today",
}

TARGET = "target"


def main():
    print("Loading historical feature data...")

    df = pd.read_csv(DATA_PATH)

    # Select a real record with a known next-day AQI
    # and complete feature values.
    eligible = df.dropna(subset=FEATURES + [TARGET]).copy()

    if eligible.empty:
        print("No records have complete features and an observed target.")
        return

    # Select a reproducible historical record.
    row = eligible.iloc[len(eligible) // 2]

    # Construct the API request using the model's feature names.
    payload = {}

    for feature in FEATURES:
        api_name = API_FEATURE_NAMES.get(feature, feature)
        value = row[feature]

        # Convert NumPy/Pandas numeric values into JSON-compatible floats.
        if feature == "day_of_week":
            payload[api_name] = int(value)
        else:
            payload[api_name] = float(value)

    print("\n========== HISTORICAL RECORD ==========")
    print(f"City: {row['City']}")
    print(f"Target date: {row['target_date']}")
    print(f"Actual next-day AQI: {float(row[TARGET]):.2f}")

    print("\nSending real feature values to the API...")

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=30,
        )
    except requests.RequestException as exc:
        print(f"Could not connect to the API: {exc}")
        print("Make sure Uvicorn is running in another terminal.")
        return

    print(f"HTTP status code: {response.status_code}")

    if not response.ok:
        print("API returned an error:")
        print(response.text)
        return

    result = response.json()
    predicted = float(result["predicted_next_day_aqi"])
    actual = float(row[TARGET])
    absolute_error = abs(actual - predicted)

    print("\n========== REAL-RECORD VALIDATION ==========")
    print(f"City: {row['City']}")
    print(f"Target date: {row['target_date']}")
    print(f"Actual AQI: {actual:.2f}")
    print(f"Predicted AQI: {predicted:.2f}")
    print(f"Absolute error: {absolute_error:.2f} AQI points")

    print("\nNote:")
    print(
        "This is one historical example, not a measure of overall "
        "model accuracy. The record may belong to a city or date "
        "already represented in training, so this is a functional "
        "check rather than an independent test."
    )


if __name__ == "__main__":
    main()
