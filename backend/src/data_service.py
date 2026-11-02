
from pathlib import Path

import pandas as pd


# Project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Historical dataset
DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "daily_features.csv"
)

# Features expected by our trained Random Forest model
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
    "day_of_week"
]


def load_historical_data():
    """
    Load the processed historical AQI dataset.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Historical dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    required_columns = ["City", "Date"] + FEATURES

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing columns: {missing_columns}"
        )

    return df


def get_city_features(city: str, selected_date=None):
    """
    Retrieve model features for a selected city.

    If selected_date is not provided, the latest date
    with an available aqi_today value is selected.

    Returns the 17 features in the model's expected order.
    """

    if not city or not city.strip():
        raise ValueError("City name cannot be empty.")

    df = load_historical_data()

    # Match city names without case sensitivity
    city_data = df[
        df["City"].str.strip().str.casefold()
        == city.strip().casefold()
    ].copy()

    if city_data.empty:
        available_cities = sorted(df["City"].dropna().unique())

        raise ValueError(
            f"City '{city}' was not found. "
            f"Available cities: {available_cities}"
        )

    # Sort records by date
    city_data = city_data.sort_values("Date")

    if selected_date is not None:

        try:
            selected_date = pd.to_datetime(
                selected_date,
                errors="raise"
            ).normalize()

        except (ValueError, TypeError):
            raise ValueError(
                "Invalid date. Use YYYY-MM-DD format."
            )

        city_data = city_data[
            city_data["Date"] == selected_date
        ]

        if city_data.empty:
            raise ValueError(
                f"No historical record found for "
                f"{city} on {selected_date.date()}."
            )

        # Current AQI is required for a forecast
        city_data = city_data.dropna(
            subset=["aqi_today"]
        )

        if city_data.empty:
            raise ValueError(
                f"No usable current AQI feature found "
                f"for {city} on {selected_date.date()}."
            )

        record = city_data.iloc[-1]

    else:

        # Find the latest record with an available current AQI
        usable_records = city_data.dropna(
            subset=["aqi_today"]
        )

        if usable_records.empty:
            raise ValueError(
                f"No usable AQI records found for {city}."
            )

        record = usable_records.iloc[-1]

    # Extract features in the correct order
    feature_values = {}

    for feature in FEATURES:

        value = record[feature]

        if pd.isna(value):
            feature_values[feature] = None
        else:
            feature_values[feature] = float(value)

    # Metadata is separate from model input features
    feature_date = record["Date"]

    observed_aqi = record.get(
        "AQI_observed",
        None
    )

    if pd.isna(observed_aqi):
        observed_aqi = None
    else:
        observed_aqi = float(observed_aqi)

    return {
        "city": str(record["City"]),
        "feature_date": feature_date.strftime("%Y-%m-%d"),
        "prediction_for_date": (
            feature_date + pd.Timedelta(days=1)
        ).strftime("%Y-%m-%d"),
        "observed_aqi_on_feature_date": observed_aqi,
        "features": feature_values
    }
