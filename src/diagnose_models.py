
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import (
    RandomForestRegressor,
    HistGradientBoostingRegressor,
)
from sklearn.model_selection import GroupKFold, cross_val_predict
from sklearn.metrics import mean_absolute_error

TRAIN_PATH = "data/processed/splits/train.csv"

FEATURES = [
    "aqi_today",
    "aqi_1d_ago",
    "aqi_2d_ago",
    "aqi_7d_ago",
    "roll3_mean",
    "roll7_mean",
    "roll7_std",
    "change_1d",
    "PM2.5_today",
    "PM10_today",
    "NO2_today",
    "CO_today",
    "SO2_today",
    "O3_today",
    "month_sin",
    "month_cos",
    "day_of_week",
]

df = pd.read_csv(TRAIN_PATH)
df = df.dropna(subset=["target", "aqi_today"]).copy()
df = df.reset_index(drop=True)

X = df[FEATURES]
y = df["target"]
groups = df["City"]

cv = GroupKFold(n_splits=5)

models = {
    "Ridge Regression": Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("model", Ridge(alpha=1.0)),
    ]),
    "Random Forest": Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("model", RandomForestRegressor(
            n_estimators=300,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
        )),
    ]),
    "HistGradientBoosting": Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("model", HistGradientBoostingRegressor(
            max_iter=200,
            learning_rate=0.08,
            max_leaf_nodes=15,
            l2_regularization=1.0,
            random_state=42,
        )),
    ]),
}

# Identify which cities belong to each validation fold.
fold_id = pd.Series(index=df.index, dtype="int64")

for fold, (_, val_idx) in enumerate(cv.split(X, y, groups), start=1):
    fold_id.iloc[val_idx] = fold
    cities = sorted(groups.iloc[val_idx].unique())
    print(f"Fold {fold} validation cities: {cities}")

# Calculate out-of-fold predictions for each model.
df["Baseline_Prediction"] = X["aqi_today"]

for name, model in models.items():
    df[name] = cross_val_predict(
        model,
        X,
        y,
        groups=groups,
        cv=cv,
        n_jobs=None,
    )

df["Fold"] = fold_id.astype(int)

# Overall and per-fold comparison.
print("\n========== MAE BY FOLD ==========")

for fold in sorted(df["Fold"].unique()):
    part = df[df["Fold"] == fold]

    print(f"\nFold {fold} | Cities: {sorted(part['City'].unique())}")

    for name in ["Baseline_Prediction", *models.keys()]:
        mae = mean_absolute_error(part["target"], part[name])
        print(f"{name}: {mae:.3f}")

# City-level comparison.
print("\n========== MAE BY CITY ==========")

city_results = []

for city, part in df.groupby("City"):
    row = {"City": city, "Rows": len(part)}

    for name in ["Baseline_Prediction", *models.keys()]:
        row[name] = mean_absolute_error(part["target"], part[name])

    city_results.append(row)

city_results_df = pd.DataFrame(city_results).sort_values(
    "Baseline_Prediction",
    ascending=False,
)

print(city_results_df.round(3).to_string(index=False))

city_results_df.to_csv(
    "data/processed/city_level_cv_mae.csv",
    index=False,
)

print("\nSaved city results to data/processed/city_level_cv_mae.csv")
