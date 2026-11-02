
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "daily_features.csv"
)

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

df = pd.read_csv(DATA_PATH)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

print("\n========== FORECAST DATA INSPECTION ==========")

for city in sorted(df["City"].dropna().unique()):

    city_df = (
        df[df["City"] == city]
        .sort_values("Date")
        .copy()
    )

    # Records with an observed AQI
    valid_aqi = city_df.dropna(subset=["AQI_observed"])

    # Records with at least one available current AQI value
    usable = city_df.dropna(subset=["aqi_today"])

    # Latest record with a usable current AQI value
    if usable.empty:
        print(f"\n{city}: NO USABLE RECORD")
        continue

    latest = usable.iloc[-1]

    missing_features = latest[FEATURES].isna().sum()

    print(f"\nCITY: {city}")
    print("Latest usable date:", latest["Date"].date())
    print("Latest observed AQI:", latest["AQI_observed"])
    print("Valid historical AQI readings:", len(valid_aqi))
    print("Missing model features:", missing_features)

    if missing_features == 0:
        print("Forecast feature status: COMPLETE")
    else:
        print("Forecast feature status: MODEL IMPUTER REQUIRED")

print("\n========== INSPECTION COMPLETED ==========")
