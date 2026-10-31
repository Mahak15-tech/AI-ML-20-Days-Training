
from pathlib import Path

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def main():
    project_root = Path(__file__).resolve().parents[2]
    reports_dir = project_root / "day-05" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Generate a reproducible binary classification dataset
    X, y = make_classification(
        n_samples=1000,
        n_features=10,
        n_informative=6,
        n_redundant=2,
        weights=[0.70, 0.30],
        random_state=42,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=42,
    )

    # Baseline: always predicts the most frequent class
    dummy_model = DummyClassifier(strategy="most_frequent")
    dummy_model.fit(X_train, y_train)
    dummy_predictions = dummy_model.predict(X_test)

    # Real model: scaling is fitted only on training data
    logistic_model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000, random_state=42),
    )
    logistic_model.fit(X_train, y_train)
    logistic_predictions = logistic_model.predict(X_test)

    results = []

    for model_name, predictions in [
        ("Dummy Classifier", dummy_predictions),
        ("Logistic Regression", logistic_predictions),
    ]:
        results.append({
            "model": model_name,
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(
                y_test, predictions, zero_division=0
            ),
            "recall": recall_score(
                y_test, predictions, zero_division=0
            ),
            "f1_score": f1_score(
                y_test, predictions, zero_division=0
            ),
        })

    results_df = pd.DataFrame(results)
    print("\n========== BASELINE MODEL COMPARISON ==========")
    print(results_df.round(3).to_string(index=False))

    results_df.to_csv(
        reports_dir / "baseline_metrics.csv", index=False
    )

    print("\nTraining rows:", len(X_train))
    print("Test rows:", len(X_test))
    print("Saved metrics to day-05/reports/baseline_metrics.csv")


if __name__ == "__main__":
    main()
