
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


# 1. Define project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

TRAIN_PATH = PROJECT_ROOT / "data" / "processed" / "splits" / "train.csv"
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "random_forest_aqi.joblib"

# 2. Define the features used during model tuning
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

TARGET = "target"


def main():
    # 3. Load training data only
    df = pd.read_csv(TRAIN_PATH)

    # 4. Keep rows with an observed target
    df = df.dropna(subset=[TARGET]).copy()

    X = df[FEATURES]
    y = df[TARGET]

    print("========== FINAL MODEL TRAINING ==========")
    print(f"Training rows: {len(df)}")
    print(f"Number of features: {len(FEATURES)}")
    print(f"Number of cities: {df['City'].nunique()}")
    print(f"Target date range: {df['target_date'].min()} to "
          f"{df['target_date'].max()}")

    # 5. Build the preprocessing and model pipeline
    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=200,
                    max_depth=10,
                    min_samples_split=2,
                    min_samples_leaf=5,
                    max_features="sqrt",
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    # 6. Train using training data only
    model.fit(X, y)

    # 7. Save the fitted pipeline
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    # 8. Save the feature order for future API use
    feature_path = MODEL_DIR / "feature_names.txt"
    feature_path.write_text("\n".join(FEATURES), encoding="utf-8")

    print("\n========== TRAINING COMPLETE ==========")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Feature list saved to: {feature_path}")
    print("Test A and Test B were not loaded or used.")


if __name__ == "__main__":
    main()
