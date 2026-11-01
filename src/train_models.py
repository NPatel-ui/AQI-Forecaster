
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import (
    RandomForestRegressor,
    HistGradientBoostingRegressor,
)
from sklearn.model_selection import GroupKFold, cross_val_score

TRAIN_PATH = "data/processed/splits/train.csv"
RESULTS_PATH = "data/processed/model_cv_results.csv"

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

# Load the training dataset.
df = pd.read_csv(TRAIN_PATH)

# Both the target and today's AQI must be available
# for a fair comparison with the persistence baseline.
df = df.dropna(subset=["target", "aqi_today"]).copy()

X = df[FEATURES]
y = df["target"]
groups = df["City"]

cv = GroupKFold(n_splits=5)

print("========== TRAINING DATA ==========")
print("Rows used:", len(df))
print("Cities:", groups.nunique())
print("Features:", len(FEATURES))

# --------------------------------------------------
# 1. PERSISTENCE BASELINE
# Predict tomorrow's AQI using today's AQI.
# --------------------------------------------------

persistence_maes = []

for train_idx, val_idx in cv.split(X, y, groups):
    X_val = X.iloc[val_idx]
    y_val = y.iloc[val_idx]

    predictions = X_val["aqi_today"]

    mae = (y_val - predictions).abs().mean()
    persistence_maes.append(mae)

baseline_mean = sum(persistence_maes) / len(persistence_maes)
baseline_std = pd.Series(persistence_maes).std(ddof=0)

print("\n========== PERSISTENCE BASELINE ==========")
print("Fold MAEs:", [round(score, 3) for score in persistence_maes])
print("Mean CV MAE:", round(baseline_mean, 3))

results = [{
    "Model": "Persistence Baseline",
    "Mean_CV_MAE": baseline_mean,
    "Std_CV_MAE": baseline_std,
}]

# --------------------------------------------------
# 2. MACHINE LEARNING MODELS
# --------------------------------------------------

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

for name, model in models.items():
    scores = cross_val_score(
        model,
        X,
        y,
        groups=groups,
        cv=cv,
        scoring="neg_mean_absolute_error",
        n_jobs=None,
    )

    mae_scores = -scores

    results.append({
        "Model": name,
        "Mean_CV_MAE": mae_scores.mean(),
        "Std_CV_MAE": mae_scores.std(),
    })

    print(f"\n{name}")
    print("Fold MAEs:", mae_scores.round(3).tolist())
    print("Mean CV MAE:", round(mae_scores.mean(), 3))
    print("Std CV MAE:", round(mae_scores.std(), 3))

# --------------------------------------------------
# 3. COMPARE AND SAVE RESULTS
# --------------------------------------------------

results_df = pd.DataFrame(results).sort_values("Mean_CV_MAE")

results_df.to_csv(RESULTS_PATH, index=False)

print("\n========== MODEL COMPARISON ==========")
print(results_df.to_string(index=False))
print(f"\nSaved results to {RESULTS_PATH}")
