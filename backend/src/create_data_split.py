
import os
import pandas as pd

INPUT_PATH = "data/processed/daily_features.csv"
OUTPUT_DIR = "data/processed/splits"

TRAIN_CITIES = [
    "Ahmedabad",
    "Amaravati",
    "Amritsar",
    "Bengaluru",
    "Brajrajnagar",
    "Delhi",
    "Gurugram",
    "Jaipur",
    "Jorapokhar",
    "Mumbai",
    "Patna",
    "Talcher",
    "Thiruvananthapuram",
]

TEST_CITIES = [
    "Chennai",
    "Hyderabad",
    "Kolkata",
    "Lucknow",
    "Visakhapatnam",
]

df = pd.read_csv(
    INPUT_PATH,
    parse_dates=["Date", "target_date"]
)

# Supervised learning requires a genuine observed target.
df = df.dropna(subset=["target"]).copy()

# Training examples must have their target date before 2020.
train_mask = (
    df["City"].isin(TRAIN_CITIES)
    & (df["target_date"] < "2020-01-01")
)

# Test A: held-out cities, historical target dates.
test_a_mask = (
    df["City"].isin(TEST_CITIES)
    & (df["target_date"] < "2020-01-01")
)

# Test B: held-out cities, target dates in 2020.
test_b_mask = (
    df["City"].isin(TEST_CITIES)
    & (df["target_date"] >= "2020-01-01")
    & (df["target_date"] <= "2020-07-01")
)

train = df.loc[train_mask].copy()
test_a = df.loc[test_a_mask].copy()
test_b = df.loc[test_b_mask].copy()

# Confirm that no city is shared between training and test sets.
assert set(train["City"]).isdisjoint(set(test_a["City"]))
assert set(train["City"]).isdisjoint(set(test_b["City"]))

# Confirm the target dates obey the intended time boundaries.
assert (train["target_date"] < "2020-01-01").all()
assert (test_a["target_date"] < "2020-01-01").all()
assert (test_b["target_date"] >= "2020-01-01").all()

os.makedirs(OUTPUT_DIR, exist_ok=True)

train.to_csv(f"{OUTPUT_DIR}/train.csv", index=False)
test_a.to_csv(f"{OUTPUT_DIR}/test_a.csv", index=False)
test_b.to_csv(f"{OUTPUT_DIR}/test_b.csv", index=False)

print("========== DATA SPLIT SUMMARY ==========")

for name, part in [
    ("TRAIN", train),
    ("TEST A - UNSEEN CITIES, HISTORICAL", test_a),
    ("TEST B - UNSEEN CITIES, 2020", test_b),
]:
    print(f"\n{name}")
    print("Rows:", len(part))
    print("Cities:", sorted(part["City"].unique().tolist()))
    print("Target date range:",
          part["target_date"].min(), "to", part["target_date"].max())

print("\nTraining/test city overlap:",
      set(train["City"]) & (set(test_a["City"]) | set(test_b["City"])))

print("\nSaved split files to:", OUTPUT_DIR)
