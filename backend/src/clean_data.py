
from pathlib import Path
import pandas as pd

# File locations
RAW_PATH = Path("data/raw/city_day.csv")
OUTPUT_PATH = Path("data/processed/city_day_stage1.csv")

# Pollutant columns
POLLUTANTS = [
    "PM2.5", "PM10", "NO", "NO2", "NOx", "NH3",
    "CO", "SO2", "O3", "Benzene", "Toluene", "Xylene"
]

# 1. Load the original dataset
df = pd.read_csv(RAW_PATH)

print("Original shape:", df.shape)

# 2. Parse dates
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# 3. Remove rows with invalid dates
df = df.dropna(subset=["Date"])

# 4. Remove exact duplicate rows
df = df.drop_duplicates()

# 5. Check for duplicate city-date combinations
duplicate_city_dates = df.duplicated(
    subset=["City", "Date"], keep=False
)

print(
    "Rows involved in duplicate city-date pairs:",
    duplicate_city_dates.sum()
)

if duplicate_city_dates.any():
    raise ValueError(
        "Duplicate city-date records found. "
        "Investigate them before continuing."
    )

# 6. Remove pollutant columns with excessive missingness
# Xylene has 61.32% missing values in the audit.
if "Xylene" in df.columns:
    df = df.drop(columns=["Xylene"])

# 7. Remove impossible negative pollutant readings.
# Keep missing values unchanged.
pollutants_to_check = [
    col for col in POLLUTANTS if col in df.columns
]

for col in pollutants_to_check:
    df.loc[df[col] < 0, col] = float("nan")

# 8. Preserve extreme AQI values for investigation.
extreme_count = (df["AQI"] > 500).sum()
print("AQI values above 500 retained:", extreme_count)

# 9. Sort chronologically within each city.
df = df.sort_values(
    ["City", "Date"]
).reset_index(drop=True)

# 10. Save an intermediate cleaned copy.
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print("\n========== CLEANING SUMMARY ==========")
print("Final shape:", df.shape)
print("Cities:", df["City"].nunique())
print("Date range:", df["Date"].min(), "to", df["Date"].max())
print("Missing AQI values retained:", df["AQI"].isna().sum())
print("Missing AQI_Bucket values:", df["AQI_Bucket"].isna().sum())
print("Saved to:", OUTPUT_PATH)
