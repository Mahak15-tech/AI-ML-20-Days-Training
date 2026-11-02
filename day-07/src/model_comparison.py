
from pathlib import Path

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def main():
    project_root = Path(__file__).resolve().parents[2]
    reports_dir = project_root / "day-07" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Generate a reproducible classification dataset
    X, y = make_classification(
        n_samples=1200,
        n_features=12,
        n_informative=7,
        n_redundant=2,
        weights=[0.65, 0.35],
        random_state=42,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=42,
    )

    models = {
        "Logistic Regression": make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=1000, random_state=42),
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=5, random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=150,
            max_depth=8,
            random_state=42,
            n_jobs=-1,
        ),
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    results = []

    for name, model in models.items():
        cv_scores = cross_val_score(
            model, X_train, y_train, cv=cv, scoring="accuracy"
        )

        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        results.append({
            "model": name,
            "cv_accuracy_mean": cv_scores.mean(),
            "cv_accuracy_std": cv_scores.std(),
            "test_accuracy": accuracy_score(y_test, predictions),
            "test_precision": precision_score(
                y_test, predictions, zero_division=0
            ),
            "test_recall": recall_score(
                y_test, predictions, zero_division=0
            ),
            "test_f1": f1_score(
                y_test, predictions, zero_division=0
            ),
        })

        print(f"\n{name}")
        print(f"CV accuracy: {cv_scores.mean():.3f} "
              f"+/- {cv_scores.std():.3f}")
        print(f"Test accuracy: {accuracy_score(y_test, predictions):.3f}")

    results_df = pd.DataFrame(results).sort_values(
        "cv_accuracy_mean", ascending=False
    )

    print("\n========== MODEL COMPARISON ==========")
    print(results_df.round(3).to_string(index=False))

    results_df.to_csv(
        reports_dir / "model_comparison.csv", index=False
    )

    print("\nResults saved to day-07/reports/model_comparison.csv")


if __name__ == "__main__":
    main()
