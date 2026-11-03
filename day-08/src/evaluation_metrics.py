
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    average_precision_score,
    ConfusionMatrixDisplay,
)


def main():
    project_root = Path(__file__).resolve().parents[2]
    reports_dir = project_root / "day-08" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Create an imbalanced binary classification dataset
    X, y = make_classification(
        n_samples=2000,
        n_features=12,
        n_informative=6,
        n_redundant=2,
        weights=[0.90, 0.10],
        class_sep=1.0,
        random_state=42,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        stratify=y,
        random_state=42,
    )

    models = {
        "Default Logistic Regression": make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=1000, random_state=42),
        ),
        "Class-Weighted Logistic Regression": make_pipeline(
            StandardScaler(),
            LogisticRegression(
                class_weight="balanced",
                max_iter=1000,
                random_state=42,
            ),
        ),
    }

    results = []
    fitted_models = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        fitted_models[name] = model

        probabilities = model.predict_proba(X_test)[:, 1]
        predictions = (probabilities >= 0.5).astype(int)

        results.append({
            "model": name,
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
            "roc_auc": roc_auc_score(y_test, probabilities),
            "pr_auc_average_precision": average_precision_score(
                y_test, probabilities
            ),
        })

        print(f"\n========== {name} ==========")
        print(classification_report(
            y_test, predictions, zero_division=0
        ))
        print("Confusion matrix:")
        print(confusion_matrix(y_test, predictions))

    results_df = pd.DataFrame(results)
    results_df.to_csv(
        reports_dir / "metrics_comparison.csv", index=False
    )

    print("\n========== METRICS COMPARISON ==========")
    print(results_df.round(3).to_string(index=False))

    # Explore a lower threshold for the default model
    default_model = fitted_models["Default Logistic Regression"]
    probabilities = default_model.predict_proba(X_test)[:, 1]
    threshold = 0.30
    lower_threshold_predictions = (
        probabilities >= threshold
    ).astype(int)

    print(f"\n========== THRESHOLD: {threshold} ==========")
    print("Accuracy:", round(
        accuracy_score(y_test, lower_threshold_predictions), 3
    ))
    print("Precision:", round(
        precision_score(y_test, lower_threshold_predictions,
                        zero_division=0), 3
    ))
    print("Recall:", round(
        recall_score(y_test, lower_threshold_predictions,
                     zero_division=0), 3
    ))
    print("F1-score:", round(
        f1_score(y_test, lower_threshold_predictions,
                 zero_division=0), 3
    ))

    # Save a confusion matrix plot
    ConfusionMatrixDisplay.from_predictions(
        y_test,
        lower_threshold_predictions,
        display_labels=["Negative", "Positive"],
    )
    plt.title("Confusion Matrix - Threshold 0.30")
    plt.tight_layout()
    plt.savefig(reports_dir / "confusion_matrix.png")
    plt.close()

    print("\nSaved metrics and confusion matrix in day-08/reports/")


if __name__ == "__main__":
    main()
