
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split


def main():
    project_root = Path(__file__).resolve().parents[2]
    reports_dir = project_root / "day-09" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Create reproducible data for this exercise
    X, y = make_classification(
        n_samples=1200,
        n_features=8,
        n_informative=5,
        n_redundant=1,
        weights=[0.70, 0.30],
        flip_y=0.08,
        random_state=42,
    )

    feature_names = [f"feature_{i}" for i in range(1, 9)]
    df = pd.DataFrame(X, columns=feature_names)
    df["target"] = y

    X_train, X_test, y_train, y_test = train_test_split(
        df[feature_names],
        df["target"],
        test_size=0.25,
        stratify=df["target"],
        random_state=42,
    )

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    print("========== OVERALL METRICS ==========")
    print("Accuracy:", round(accuracy_score(y_test, predictions), 3))
    print("Precision:", round(
        precision_score(y_test, predictions, zero_division=0), 3
    ))
    print("Recall:", round(
        recall_score(y_test, predictions, zero_division=0), 3
    ))
    print("F1-score:", round(
        f1_score(y_test, predictions, zero_division=0), 3
    ))

    print("\nConfusion matrix:")
    print(confusion_matrix(y_test, predictions))

    # Save individual errors for inspection
    errors = X_test.copy()
    errors["actual"] = y_test
    errors["predicted"] = predictions
    errors["predicted_probability"] = probabilities

    errors["error_type"] = np.select(
        [
            (errors["actual"] == 0) & (errors["predicted"] == 1),
            (errors["actual"] == 1) & (errors["predicted"] == 0),
        ],
        ["False Positive", "False Negative"],
        default="Correct",
    )

    mistakes = errors[errors["error_type"] != "Correct"].copy()
    mistakes.to_csv(reports_dir / "misclassified_examples.csv", index=False)

    print("\n========== ERROR COUNTS ==========")
    print(mistakes["error_type"].value_counts())

    # Illustrative group analysis using feature_1
    # These are synthetic groups, not real demographic groups.
    group_data = errors.copy()
    group_data["group"] = np.where(
        group_data["feature_1"] < group_data["feature_1"].median(),
        "Lower feature_1",
        "Higher feature_1",
    )

    group_results = []
    for group_name, group in group_data.groupby("group"):
        group_results.append({
            "group": group_name,
            "rows": len(group),
            "accuracy": accuracy_score(group["actual"], group["predicted"]),
            "precision": precision_score(
                group["actual"], group["predicted"], zero_division=0
            ),
            "recall": recall_score(
                group["actual"], group["predicted"], zero_division=0
            ),
            "f1_score": f1_score(
                group["actual"], group["predicted"], zero_division=0
            ),
        })

    group_report = pd.DataFrame(group_results)
    group_report.to_csv(reports_dir / "group_metrics.csv", index=False)

    print("\n========== GROUP METRICS ==========")
    print(group_report.round(3).to_string(index=False))

    # Permutation importance measures the effect of shuffling a feature.
    importance = permutation_importance(
        model,
        X_test,
        y_test,
        scoring="f1",
        n_repeats=10,
        random_state=42,
    )

    importance_report = pd.DataFrame({
        "feature": feature_names,
        "importance_mean": importance.importances_mean,
        "importance_std": importance.importances_std,
    }).sort_values("importance_mean", ascending=False)

    importance_report.to_csv(
        reports_dir / "permutation_importance.csv", index=False
    )

    print("\n========== PERMUTATION IMPORTANCE ==========")
    print(importance_report.round(3).to_string(index=False))

    print("\nReports saved in day-09/reports/")


if __name__ == "__main__":
    main()
