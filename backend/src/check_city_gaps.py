
import pandas as pd

INPUT_PATH = "data/processed/city_day_stage1.csv"

df = pd.read_csv(INPUT_PATH, parse_dates=["Date"])

print("========== CITY DATA COMPLETENESS ==========")

results = []

for city, group in df.groupby("City"):
    group = group.sort_values("Date")

    first_date = group["Date"].min()
    last_date = group["Date"].max()

    # Number of calendar days between first and last observation
    expected_days = (last_date - first_date).days + 1

    # Number of distinct dates actually present
    observed_days = group["Date"].nunique()

    missing_calendar_days = expected_days - observed_days

    results.append({
        "City": city,
        "First_Date": first_date.date(),
        "Last_Date": last_date.date(),
        "Observed_Days": observed_days,
        "Expected_Days": expected_days,
        "Missing_Calendar_Days": missing_calendar_days,
        "Calendar_Coverage_Percent": round(
            observed_days / expected_days * 100, 2
        ),
        "Days_With_AQI": group["AQI"].notna().sum()
    })

report = pd.DataFrame(results).sort_values(
    "Calendar_Coverage_Percent",
    ascending=False
)

print(report.to_string(index=False))

print("\nTotal missing calendar days across city ranges:",
      report["Missing_Calendar_Days"].sum())

report.to_csv(
    "data/processed/city_completeness.csv",
    index=False
)

print("\nSaved report to data/processed/city_completeness.csv")
