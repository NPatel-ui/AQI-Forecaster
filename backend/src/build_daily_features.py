
import os
import numpy as np
import pandas as pd

INPUT_PATH = "data/processed/city_day_stage1.csv"
OUTPUT_PATH = "data/processed/daily_features.csv"

df = pd.read_csv(INPUT_PATH, parse_dates=["Date"])
df = df.sort_values(["City", "Date"]).copy()

# Confirm that each city has at most one row per date.
if df.duplicated(["City", "Date"]).any():
    raise ValueError("Duplicate city-date records found.")

# Build a complete daily calendar for every city.
# This ensures that a one-row lag represents one calendar day.
city_frames = []

for city, group in df.groupby("City"):
    group = group.set_index("Date").sort_index()

    full_dates = pd.date_range(
        start=group.index.min(),
        end=group.index.max(),
        freq="D"
    )

    group = group.reindex(full_dates)
    group.index.name = "Date"
    group["City"] = city

    city_frames.append(group.reset_index())

df = pd.concat(city_frames, ignore_index=True)
df = df.sort_values(["City", "Date"]).reset_index(drop=True)

# Save the original observed AQI for target creation.
# We must never fill missing target labels.
df["AQI_observed"] = df["AQI"]

# Features may use short forward-filled gaps from past observations.
# This is done separately from the untouched target labels.
pollutants = ["PM2.5", "PM10", "NO2", "CO", "SO2", "O3"]
fill_columns = ["AQI"] + pollutants

df[fill_columns] = (
    df.groupby("City")[fill_columns]
    .transform(lambda group: group.ffill(limit=3))
)

# Create historical AQI features within each city.
g = df.groupby("City", sort=False)["AQI"]

df["aqi_today"] = df["AQI"]
df["aqi_1d_ago"] = g.shift(1)
df["aqi_2d_ago"] = g.shift(2)
df["aqi_7d_ago"] = g.shift(7)

df["roll3_mean"] = g.transform(
    lambda s: s.rolling(window=3, min_periods=3).mean()
)

df["roll7_mean"] = g.transform(
    lambda s: s.rolling(window=7, min_periods=7).mean()
)

df["roll7_std"] = g.transform(
    lambda s: s.rolling(window=7, min_periods=7).std()
)

df["change_1d"] = df["aqi_today"] - df["aqi_1d_ago"]

# Today's pollutant measurements.
# Missing values that remain will be handled later in the ML pipeline.
for column in pollutants:
    df[f"{column}_today"] = df[column]

# Calendar features.
month = df["Date"].dt.month
df["month_sin"] = np.sin(2 * np.pi * month / 12)
df["month_cos"] = np.cos(2 * np.pi * month / 12)
df["day_of_week"] = df["Date"].dt.dayofweek

# Target: the actual, observed AQI on the next calendar day.
# Do not use the forward-filled AQI to create the target.
df["target"] = (
    df.groupby("City", sort=False)["AQI_observed"]
    .shift(-1)
)

# Mark rows whose next-day target is genuinely observed.
df["target_date"] = df["Date"] + pd.Timedelta(days=1)

# Keep the source AQI and original columns for auditing, plus features.
feature_columns = [
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

output_columns = [
    "City", "Date", "target_date", "AQI_observed",
    *feature_columns, "target"
]

result = df[output_columns].copy()

os.makedirs("data/processed", exist_ok=True)
result.to_csv(OUTPUT_PATH, index=False)

print("========== DAILY FEATURE DATASET ==========")
print("Rows and columns:", result.shape)
print("Unique cities:", result["City"].nunique())
print("Date range:", result["Date"].min(), "to", result["Date"].max())
print("Missing target labels:", result["target"].isna().sum())
print("Rows with observed next-day AQI:", result["target"].notna().sum())
print("Duplicate city-date rows:", result.duplicated(["City", "Date"]).sum())

print("\nMissing values in features:")
print(result[feature_columns].isna().sum().to_string())

print("\nSample rows:")
print(result[["City", "Date", "target_date",
              "aqi_today", "aqi_1d_ago", "target"]].head(10).to_string(index=False))

print("\nSaved to:", OUTPUT_PATH)
