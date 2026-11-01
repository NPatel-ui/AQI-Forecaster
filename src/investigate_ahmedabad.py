
import pandas as pd

DATA_PATH = "data/processed/splits/train.csv"

df = pd.read_csv(DATA_PATH, parse_dates=["Date", "target_date"])

ahmedabad = df[df["City"] == "Ahmedabad"].copy()
ahmedabad = ahmedabad.sort_values("Date")

print("========== AHMEDABAD DATA ==========")
print("Rows:", len(ahmedabad))
print("Date range:", ahmedabad["Date"].min(), "to", ahmedabad["Date"].max())

print("\n========== AQI DISTRIBUTION ==========")
print(ahmedabad["aqi_today"].describe())

print("\n========== HIGHEST AQI VALUES ==========")
columns = [
    "Date",
    "target_date",
    "aqi_today",
    "aqi_1d_ago",
    "aqi_2d_ago",
    "target",
]

print(
    ahmedabad.sort_values("aqi_today", ascending=False)[columns]
    .head(15)
    .to_string(index=False)
)

print("\n========== LARGEST DAY-TO-DAY CHANGES ==========")
ahmedabad["absolute_change"] = ahmedabad["change_1d"].abs()

print(
    ahmedabad.sort_values("absolute_change", ascending=False)[
        ["Date", "aqi_today", "change_1d", "target"]
    ]
    .head(15)
    .to_string(index=False)
)

print("\n========== MISSING FEATURE COUNTS ==========")
features = [
    "aqi_today",
    "aqi_1d_ago",
    "aqi_2d_ago",
    "aqi_7d_ago",
    "roll7_mean",
    "PM2.5_today",
    "PM10_today",
    "NO2_today",
    "CO_today",
    "SO2_today",
    "O3_today",
]

print(ahmedabad[features].isna().sum().to_string())
