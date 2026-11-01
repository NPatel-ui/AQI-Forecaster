
import pandas as pd

# Load the cleaned dataset and parse dates.
df = pd.read_csv(
    "data/processed/city_day_stage1.csv",
    parse_dates=["Date"]
)

# Keep the 18 cities that passed our preliminary screen.
eligible = pd.read_csv("data/processed/eligible_cities.csv")
df = df[df["City"].isin(eligible["City"])].copy()

# Separate the historical period from the 2020 test period.
df["Period"] = df["Date"].apply(
    lambda date: "Historical_2015_2019"
    if date.year <= 2019
    else "Test_2020"
)

# Summarize coverage for each city and period.
summary = (
    df.groupby(["City", "Period"])
    .agg(
        Recorded_Days=("Date", "nunique"),
        Valid_AQI_Days=("AQI", "count")
    )
    .reset_index()
)

# Put both periods side by side for easier comparison.
coverage = summary.pivot(
    index="City",
    columns="Period",
    values=["Recorded_Days", "Valid_AQI_Days"]
)

coverage.columns = [
    f"{metric}_{period}"
    for metric, period in coverage.columns
]
coverage = coverage.reset_index().fillna(0)

# Add simple eligibility flags for further investigation.
coverage["Historical_Eligible"] = (
    coverage["Valid_AQI_Days_Historical_2015_2019"] >= 300
)

coverage["2020_Eligible"] = (
    coverage["Valid_AQI_Days_Test_2020"] >= 100
)

coverage["Candidate_For_Holdout"] = (
    coverage["Historical_Eligible"]
    & coverage["2020_Eligible"]
)

coverage = coverage.sort_values("City")

print("========== TRAIN/TEST CITY COVERAGE ==========")
print(coverage.to_string(index=False))

print(
    "\nCities meeting both preliminary coverage thresholds:",
    int(coverage["Candidate_For_Holdout"].sum())
)

coverage.to_csv(
    "data/processed/split_city_coverage.csv",
    index=False
)

print("\nSaved to data/processed/split_city_coverage.csv")
