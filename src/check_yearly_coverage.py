
import pandas as pd

# Load the cleaned intermediate dataset.
df = pd.read_csv(
    "data/processed/city_day_stage1.csv",
    parse_dates=["Date"]
)

# Load the list of preliminarily eligible cities.
eligible = pd.read_csv("data/processed/eligible_cities.csv")
eligible_cities = eligible["City"].tolist()

# Keep only the cities that passed the initial screen.
df = df[df["City"].isin(eligible_cities)].copy()

# Extract the calendar year from each date.
df["Year"] = df["Date"].dt.year

# Count recorded dates and valid AQI readings for each city and year.
yearly = (
    df.groupby(["City", "Year"])
    .agg(
        Recorded_Days=("Date", "nunique"),
        Valid_AQI_Days=("AQI", "count")
    )
    .reset_index()
)

# Display the years relevant to our training and testing plan.
yearly = yearly[
    yearly["Year"].between(2015, 2020)
].sort_values(["City", "Year"])

print("========== YEARLY AQI COVERAGE ==========")
print(yearly.to_string(index=False))

# Save the results so we can inspect them later.
yearly.to_csv(
    "data/processed/yearly_aqi_coverage.csv",
    index=False
)

print("\nSaved to data/processed/yearly_aqi_coverage.csv")

