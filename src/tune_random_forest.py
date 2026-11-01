
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GroupKFold, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error

TRAIN_PATH = "data/processed/splits/train.csv"
RESULTS_PATH = "data/processed/random_forest_tuning_results.csv"

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

# Load training data only.
df = pd.read_csv(TRAIN_PATH)

# Use the same eligible rows for a fair comparison
# against the persistence baseline.
df = df.dropna(subset=["target", "aqi_today"]).copy()
df = df.reset_index(drop=True)

X = df[FEATURES]
y = df["target"]
groups = df["City"]

cv = GroupKFold(n_splits=5)

print("========== RANDOM FOREST TUNING ==========")
print("Training rows:", len(df))
print("Training cities:", groups.nunique())
print("Features:", len(FEATURES))

# Calculate the persistence baseline on the same folds.
baseline_maes = []

for _, val_idx in cv.split(X, y, groups):
    predictions = X.iloc[val_idx]["aqi_today"]
    actual = y.iloc[val_idx]

    baseline_maes.append(
        mean_absolute_error(actual, predictions)
    )

baseline_mae = sum(baseline_maes) / len(baseline_maes)

print("\nPersistence baseline CV MAE:", round(baseline_mae, 3))

# Preprocessing is fitted separately inside each training fold.
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("model", RandomForestRegressor(
        random_state=42,
        n_jobs=1,
    )),
])

# Candidate settings to investigate.
param_distributions = {
    "model__n_estimators": [200, 300, 400],
    "model__max_depth": [None, 10, 20, 30],
    "model__min_samples_split": [2, 5, 10],
    "model__min_samples_leaf": [2, 5, 10],
    "model__max_features": [1.0, 0.8, "sqrt"],
}

search = RandomizedSearchCV(
    estimator=pipeline,
    param_distributions=param_distributions,
    n_iter=10,
    scoring="neg_mean_absolute_error",
    cv=cv,
    random_state=42,
    n_jobs=-1,
    verbose=2,
    return_train_score=True,
)

# GroupKFold ensures validation cities are not used
# to fit the corresponding fold's model.
search.fit(X, y, groups=groups)

best_mae = -search.best_score_

print("\n========== BEST RANDOM FOREST ==========")
print("Best CV MAE:", round(best_mae, 3))
print("Best parameters:")

for parameter, value in search.best_params_.items():
    print(f"{parameter}: {value}")

print("\nBaseline CV MAE:", round(baseline_mae, 3))
print("Improvement over baseline:",
      round(baseline_mae - best_mae, 3), "AQI points")

# Save all tested configurations, best first.
results = pd.DataFrame(search.cv_results_)
results["Mean_CV_MAE"] = -results["mean_test_score"]
results["Std_CV_MAE"] = results["std_test_score"]

results = results.sort_values("Mean_CV_MAE")

results.to_csv(RESULTS_PATH, index=False)

print("\n========== TOP 10 CONFIGURATIONS ==========")
print(
    results[
        [
            "rank_test_score",
            "Mean_CV_MAE",
            "Std_CV_MAE",
            "params",
        ]
    ].to_string(index=False)
)

print(f"\nSaved tuning results to {RESULTS_PATH}")
