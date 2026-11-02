
from pathlib import Path
import pandas as pd

# Find project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dataset location
DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "daily_features.csv"
)

# Check dataset
if not DATA_PATH.exists():
    print("Dataset not found!")
    print("Expected location:", DATA_PATH)
    raise SystemExit(1)

# Load dataset
df = pd.read_csv(DATA_PATH)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

print("\n========== DATASET OVERVIEW ==========")
print("Total records:", len(df))
print("Total cities:", df["City"].nunique())
print("Dataset columns:", len(df.columns))

print("\n========== AVAILABLE CITIES ==========")

cities = sorted(df["City"].dropna().unique())

for city in cities:
    print(city)

print("\n========== CITY-WISE DATE COVERAGE ==========")

summary = df.groupby("City").agg(
    total_records=("Date", "count"),
    first_date=("Date", "min"),
    latest_date=("Date", "max"),
    valid_aqi=("AQI_observed", "count")
)

print(summary.to_string())

print("\n========== MODEL FEATURE CHECK ==========")

features = [
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

for feature in features:
    if feature in df.columns:
        print("[FOUND]", feature)
    else:
        print("[MISSING]", feature)

print("\n========== LATEST CITY RECORDS ==========")

for city in cities:
    city_data = (
        df[df["City"] == city]
        .sort_values("Date")
    )

    latest = city_data.iloc[-1]

    print(
        f"{city} | "
        f"Date: {latest['Date'].date()} | "
        f"AQI: {latest['AQI_observed']}"
    )

print("\n========== INSPECTION COMPLETED ==========")
