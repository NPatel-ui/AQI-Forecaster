
import pandas as pd

# Load the original dataset
df = pd.read_csv("data/raw/city_day.csv")

# Convert Date into a real datetime column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

print("\n========== 1. MISSING VALUES ==========")

missing = pd.DataFrame({
    "Missing_Count": df.isna().sum(),
    "Missing_Percent": (df.isna().mean() * 100).round(2)
})

print(missing.sort_values("Missing_Percent", ascending=False))

print("\n========== 2. DUPLICATE ROWS ==========")

print("Exact duplicate rows:", df.duplicated().sum())

print("\n========== 3. CITY COVERAGE ==========")

city_coverage = (
    df.groupby("City")
    .agg(
        Total_Rows=("Date", "size"),
        First_Date=("Date", "min"),
        Last_Date=("Date", "max"),
        Days_With_AQI=("AQI", "count"),
        Missing_AQI=("AQI", lambda s: s.isna().sum())
    )
    .sort_values("Days_With_AQI")
)

print(city_coverage.to_string())

print("\n========== 4. AQI ABOVE 500 ==========")

extreme = df.loc[
    df["AQI"] > 500,
    ["City", "Date", "AQI", "AQI_Bucket"]
]

print("Rows with AQI above 500:", len(extreme))
print(extreme.to_string(index=False))

print("\n========== 5. AQI CATEGORY COUNTS ==========")

print(df["AQI_Bucket"].value_counts(dropna=False))

print("\n========== 6. NEGATIVE POLLUTANT VALUES ==========")

pollutants = [
    "PM2.5", "PM10", "NO", "NO2", "NOx", "NH3",
    "CO", "SO2", "O3", "Benzene", "Toluene", "Xylene"
]

print((df[pollutants] < 0).sum().sort_values(ascending=False))
