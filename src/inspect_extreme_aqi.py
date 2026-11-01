
import pandas as pd

RAW_PATH = "data/raw/city_day.csv"
CLEAN_PATH = "data/processed/city_day_stage1.csv"

# Dates identified during our previous investigation.
CHECK_DATES = [
    "2016-07-14",
    "2016-07-15",
    "2018-02-10",
    "2018-02-11",
    "2018-02-19",
    "2018-02-20",
]

raw = pd.read_csv(RAW_PATH)
clean = pd.read_csv(CLEAN_PATH)

raw["Date"] = pd.to_datetime(raw["Date"], errors="coerce")
clean["Date"] = pd.to_datetime(clean["Date"], errors="coerce")

check_dates = pd.to_datetime(CHECK_DATES)

columns = [
    "City",
    "Date",
    "AQI",
    "AQI_Bucket",
    "PM2.5",
    "PM10",
    "NO",
    "NO2",
    "NOx",
    "NH3",
    "CO",
    "SO2",
    "O3",
]

print("========== ORIGINAL DATA ==========")

raw_rows = raw[
    (raw["City"] == "Ahmedabad")
    & (raw["Date"].isin(check_dates))
]

print(
    raw_rows[columns]
    .sort_values("Date")
    .to_string(index=False)
)

print("\n========== CLEANED DATA ==========")

clean_rows = clean[
    (clean["City"] == "Ahmedabad")
    & (clean["Date"].isin(check_dates))
]

clean_columns = [c for c in columns if c in clean.columns]

print(
    clean_rows[clean_columns]
    .sort_values("Date")
    .to_string(index=False)
)

print("\n========== EXTREME AQI RECORD COUNTS ==========")

extreme = raw[
    (raw["City"] == "Ahmedabad")
    & (raw["AQI"] > 500)
]

print("Ahmedabad records with AQI > 500:", len(extreme))
print("Highest original AQI:", raw.loc[
    raw["City"] == "Ahmedabad", "AQI"
].max())

print("\n========== COMPLETENESS OF EXTREME RECORDS ==========")

if not extreme.empty:
    pollutants = [
        c for c in
        ["PM2.5", "PM10", "NO", "NO2", "NOx", "NH3",
         "CO", "SO2", "O3", "Benzene", "Toluene", "Xylene"]
        if c in extreme.columns
    ]

    print("Extreme records:", len(extreme))
    print("Missing pollutant readings:")
    print(extreme[pollutants].isna().sum().to_string())

    print("\nSample of extreme records:")
    print(
        extreme[
            ["Date", "AQI", "AQI_Bucket"] + pollutants
        ]
        .sort_values("AQI", ascending=False)
        .head(15)
        .to_string(index=False)
    )
