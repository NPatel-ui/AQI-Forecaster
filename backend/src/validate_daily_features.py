
import pandas as pd

df = pd.read_csv(
    "data/processed/daily_features.csv",
    parse_dates=["Date", "target_date"]
)

# Load the observed AQI from the cleaned source.
source = pd.read_csv(
    "data/processed/city_day_stage1.csv",
    parse_dates=["Date"]
)

# Keep only the actual recorded AQI values.
observed = source[["City", "Date", "AQI"]].copy()

# Rename the date to the date the target should refer to.
observed = observed.rename(
    columns={"Date": "target_date", "AQI": "expected_target"}
)

# Match each feature row with the actual AQI on its target date.
check = df.merge(
    observed,
    on=["City", "target_date"],
    how="left",
    validate="many_to_one"
)

# Compare target values only where both are observed.
valid = check["target"].notna() & check["expected_target"].notna()

mismatches = (
    check.loc[valid, "target"] - check.loc[valid, "expected_target"]
).abs()

print("========== TARGET VALIDATION ==========")
print("Total feature rows:", len(check))
print("Rows with observed targets:", int(check["target"].notna().sum()))
print("Rows matched to actual next-day AQI:", int(valid.sum()))
print("Target mismatches:", int((mismatches > 1e-9).sum()))
print("Rows with target date after source coverage:",
      int(check["expected_target"].isna().sum()))

if (mismatches > 1e-9).any():
    raise ValueError("Target alignment failed. Investigate before training.")

print("\nTarget alignment check passed.")
