
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "random_forest_aqi.joblib"
TRAIN_PATH = PROJECT_ROOT / "data" / "processed" / "splits" / "train.csv"
TEST_A_PATH = PROJECT_ROOT / "data" / "processed" / "splits" / "test_a.csv"
TEST_B_PATH = PROJECT_ROOT / "data" / "processed" / "splits" / "test_b.csv"

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


def calculate_metrics(y_true, y_pred):
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R2": r2_score(y_true, y_pred),
    }


def evaluate_split(model, df, split_name):
    # Keep rows with actual targets and current AQI.
    # This makes the persistence baseline comparison fair.
    df = df.dropna(subset=[TARGET, "aqi_today"]).copy()

    if df.empty:
        print(f"\n{split_name}: No eligible rows.")
        return None

    X = df[FEATURES]
    y_true = df[TARGET]

    # Random Forest predictions
    y_rf = model.predict(X)

    # Persistence baseline: tomorrow's AQI is estimated as today's AQI
    y_baseline = df["aqi_today"].to_numpy()

    rf_metrics = calculate_metrics(y_true, y_rf)
    baseline_metrics = calculate_metrics(y_true, y_baseline)

    print(f"\n========== {split_name} ==========")
    print(f"Evaluation rows: {len(df)}")
    print(f"Cities: {df['City'].nunique()}")
    print(f"Target dates: {df['target_date'].min()} to "
          f"{df['target_date'].max()}")

    print("\nRandom Forest:")
    for name, value in rf_metrics.items():
        print(f"{name}: {value:.4f}")

    print("\nPersistence baseline:")
    for name, value in baseline_metrics.items():
        print(f"{name}: {value:.4f}")

    difference = baseline_metrics["MAE"] - rf_metrics["MAE"]

    print(f"\nBaseline MAE - Random Forest MAE: {difference:.4f}")

    if difference > 0:
        print("Result: Random Forest has lower MAE on this test set.")
    elif difference < 0:
        print("Result: Persistence baseline has lower MAE on this test set.")
    else:
        print("Result: Both have equal MAE on this test set.")

    return {
        "split": split_name,
        "rows": len(df),
        "cities": df["City"].nunique(),
        "rf_mae": rf_metrics["MAE"],
        "rf_rmse": rf_metrics["RMSE"],
        "rf_r2": rf_metrics["R2"],
        "baseline_mae": baseline_metrics["MAE"],
        "baseline_rmse": baseline_metrics["RMSE"],
        "baseline_r2": baseline_metrics["R2"],
    }


def main():
    print("Loading the saved model...")
    model = joblib.load(MODEL_PATH)

    # Test files are opened only now, for final evaluation.
    test_a = pd.read_csv(TEST_A_PATH)
    test_b = pd.read_csv(TEST_B_PATH)

    results = []

    result_a = evaluate_split(model, test_a, "TEST A - UNSEEN CITIES")
    result_b = evaluate_split(model, test_b, "TEST B - FUTURE DATES")

    if result_a is not None:
        results.append(result_a)

    if result_b is not None:
        results.append(result_b)

    results_path = PROJECT_ROOT / "report" / "final_evaluation.csv"
    results_path.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(results).to_csv(results_path, index=False)

    print(f"\nEvaluation summary saved to: {results_path}")


if __name__ == "__main__":
    main()
