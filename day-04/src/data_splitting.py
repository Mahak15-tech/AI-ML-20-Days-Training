from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification


def main():
    project_root = Path(__file__).resolve().parents[2]
    reports_dir = project_root / "day-04" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Create a reproducible example dataset
    X, y = make_classification(
        n_samples=1000,
        n_features=8,
        n_informative=5,
        n_redundant=1,
        weights=[0.75, 0.25],
        random_state=42,
    )

    feature_names = [f"feature_{i}" for i in range(1, 9)]
    df = pd.DataFrame(X, columns=feature_names)
    df["target"] = y

    print("Original dataset shape:", df.shape)
    print("\nClass distribution:")
    print(df["target"].value_counts(normalize=True).round(3))

    # 60% training, 20% validation, 20% test
    X_train, X_temp, y_train, y_temp = train_test_split(
        df[feature_names],
        df["target"],
        test_size=0.40,
        stratify=df["target"],
        random_state=42,
    )

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        stratify=y_temp,
        random_state=42,
    )

    split_summary = pd.DataFrame({
        "split": ["Train", "Validation", "Test"],
        "rows": [len(X_train), len(X_val), len(X_test)],
        "positive_class_rate": [
            y_train.mean(), y_val.mean(), y_test.mean()
        ],
    })

    print("\n========== SPLIT SUMMARY ==========")
    print(split_summary.round(3).to_string(index=False))

    split_summary.to_csv(
        reports_dir / "split_summary.csv", index=False
    )

    # Demonstrate a common leakage mistake
    print("\n========== LEAKAGE CHECKLIST ==========")
    checks = [
        "Split data before fitting preprocessing steps.",
        "Fit imputation/scaling only on training data.",
        "Keep duplicate or related records across splits in check.",
        "Do not use information unavailable at prediction time.",
        "Use the test set only for final evaluation.",
    ]

    for check in checks:
        print(f"- {check}")

    print("\nSaved split summary to day-04/reports/split_summary.csv")


if __name__ == "__main__":
    main()
