
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned intermediate dataset.
df = pd.read_csv(
    "data/processed/city_day_stage1.csv",
    parse_dates=["Date"]
)

# Create a folder for EDA charts.
os.makedirs("report/eda", exist_ok=True)

sns.set_theme(style="whitegrid")

# --------------------------------------------------
# 1. Missing AQI values by city
# --------------------------------------------------
missing = (
    df.groupby("City")["AQI"]
    .apply(lambda s: s.isna().sum())
    .sort_values(ascending=False)
)

plt.figure(figsize=(12, 7))
missing.plot(kind="bar")
plt.title("Missing AQI Readings by City")
plt.xlabel("City")
plt.ylabel("Number of Missing AQI Readings")
plt.xticks(rotation=70)
plt.tight_layout()
plt.savefig("report/eda/01_missing_aqi_by_city.png", dpi=150)
plt.close()

# --------------------------------------------------
# 2. Distribution of AQI values
# --------------------------------------------------
plt.figure(figsize=(10, 6))
sns.histplot(df["AQI"].dropna(), bins=50, kde=True)
plt.title("Distribution of Daily AQI Values")
plt.xlabel("AQI")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("report/eda/02_aqi_distribution.png", dpi=150)
plt.close()

# --------------------------------------------------
# 3. Average AQI by city
# --------------------------------------------------
city_aqi = (
    df.groupby("City")["AQI"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12, 7))
city_aqi.plot(kind="bar")
plt.title("Average AQI by City")
plt.xlabel("City")
plt.ylabel("Average AQI")
plt.xticks(rotation=70)
plt.tight_layout()
plt.savefig("report/eda/03_average_aqi_by_city.png", dpi=150)
plt.close()

# --------------------------------------------------
# 4. Monthly average AQI
# --------------------------------------------------
df["Month"] = df["Date"].dt.month

monthly = df.groupby("Month")["AQI"].mean()

plt.figure(figsize=(10, 6))
monthly.plot(marker="o")
plt.title("Average AQI by Month")
plt.xlabel("Month")
plt.ylabel("Average AQI")
plt.xticks(range(1, 13))
plt.tight_layout()
plt.savefig("report/eda/04_monthly_aqi.png", dpi=150)
plt.close()

# --------------------------------------------------
# 5. Yearly AQI trend
# --------------------------------------------------
df["Year"] = df["Date"].dt.year

yearly = df.groupby("Year")["AQI"].mean()

plt.figure(figsize=(10, 6))
yearly.plot(marker="o")
plt.title("Average AQI by Year")
plt.xlabel("Year")
plt.ylabel("Average AQI")
plt.tight_layout()
plt.savefig("report/eda/05_yearly_aqi.png", dpi=150)
plt.close()

# --------------------------------------------------
# 6. Correlation between pollutants and AQI
# --------------------------------------------------
numeric_cols = [
    "PM2.5", "PM10", "NO", "NO2", "NOx",
    "NH3", "CO", "SO2", "O3", "Benzene",
    "Toluene", "AQI"
]

correlation = df[numeric_cols].corr()

plt.figure(figsize=(12, 9))
sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)
plt.title("Correlation Between Pollutants and AQI")
plt.tight_layout()
plt.savefig("report/eda/06_correlation_heatmap.png", dpi=150)
plt.close()

# --------------------------------------------------
# 7. AQI category counts
# --------------------------------------------------
category_counts = df["AQI_Bucket"].value_counts()

plt.figure(figsize=(10, 6))
category_counts.plot(kind="bar")
plt.title("Number of Observations in Each AQI Category")
plt.xlabel("AQI Category")
plt.ylabel("Number of Observations")
plt.xticks(rotation=35)
plt.tight_layout()
plt.savefig("report/eda/07_aqi_categories.png", dpi=150)
plt.close()

# --------------------------------------------------
# Print summary statistics
# --------------------------------------------------
print("========== EDA SUMMARY ==========")
print("\nAverage AQI by city:")
print(city_aqi.round(2).to_string())

print("\nAverage AQI by month:")
print(monthly.round(2).to_string())

print("\nAverage AQI by year:")
print(yearly.round(2).to_string())

print("\nPollutant correlation with AQI:")
print(correlation["AQI"].drop("AQI").sort_values(ascending=False).round(3))

print("\nCharts saved in report/eda/")
