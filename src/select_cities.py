
import pandas as pd

df = pd.read_csv(
    "data/processed/city_day_stage1.csv",
    parse_dates=["Date"]
)

city_stats = (
    df.groupby("City")
    .agg(
        Recorded_Days=("Date", "nunique"),
        Valid_AQI_Days=("AQI", "count"),
        First_Date=("Date", "min"),
        Last_Date=("Date", "max")
    )
    .reset_index()
)

# Preliminary data-coverage screen
eligible = city_stats[
    (city_stats["Recorded_Days"] >= 730)
    & (city_stats["Valid_AQI_Days"] >= 500)
].copy()

excluded = city_stats[
    ~city_stats["City"].isin(eligible["City"])
].copy()

print("========== PRELIMINARILY ELIGIBLE CITIES ==========")
print(eligible.sort_values("City").to_string(index=False))

print("\nEligible city count:", len(eligible))

print("\n========== CITIES EXCLUDED BY INITIAL SCREEN ==========")
print(excluded.sort_values("City").to_string(index=False))

print("\nExcluded city count:", len(excluded))

eligible.to_csv(
    "data/processed/eligible_cities.csv",
    index=False
)
