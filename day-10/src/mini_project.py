
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def create_dataset(path):
    """Create a reproducible synthetic student performance dataset."""
    rng = np.random.default_rng(42)
    n = 400

    study_hours = rng.uniform(0.5, 8, n).round(1)
    attendance = rng.uniform(40, 100, n).round(1)
    department = rng.choice(
        ["AI", "Data Science", "Machine Learning"], n
    )

    probability = 1 / (
        1 + np.exp(-(
            -5 + 0.45 * study_hours + 0.045 * attendance
        ))
    )
    passed = rng.binomial(1, probability)

    df = pd.DataFrame({
        "study_hours": study_hours,
        "attendance": attendance,
        "department": department,
        "passed": passed,
    })

    # Introduce a few missing values for preprocessing practice
    df.loc[rng.choice(n, 12, replace=False), "study_hours"] = np.nan
    df.loc[rng.choice(n, 10, replace=False), "department"] = np.nan

    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df


def main():
    root = Path(__file__).resolve().parents[2]
    data_path = root / "day-10" / "data" / "students.csv"
    reports = root / "day-10" / "reports"
    models_dir = root / "day-10" / "models"

    reports.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load data
    if data_path.exists():
        df = pd.read_csv(data_path)
    else:
        df = create_dataset(data_path)

    print("========== DATA QUALITY ==========")
    print("Shape:", df.shape)
    print("\nMissing values:")
    print(df.isnull().sum())
    print("Duplicate rows:", df.duplicated().sum())

    quality = pd.DataFrame({
        "column": df.columns,
        "data_type": [str(t) for t in df.dtypes],
        "missing_values": df.isnull().sum().values,
        "unique_values": df.nunique().values,
    })
    quality.to_csv(reports / "data_quality.csv", index=False)

    # Remove exact duplicate rows before splitting
    df = df.drop_duplicates().reset_index(drop=True)

    X = df.drop(columns="passed")
    y = df["passed"]

    numeric_features = ["study_hours", "attendance"]
    categorical_features = ["department"]

    # 2. Split data before fitting preprocessing
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=42,
    )

    # 3. Reusable preprocessing
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor = ColumnTransformer([
        ("numeric", numeric_pipeline, numeric_features),
        ("categorical", categorical_pipeline, categorical_features),
    ])

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(
            n_estimators=150,
            max_depth=8,
            random_state=42,
            class_weight="balanced",
        ),
    }

    cv = StratifiedKFold(
        n_splits=5, shuffle=True, random_state=42
    )
    results = []
    fitted = {}

    # 4. Cross-validation and model comparison
    for name, classifier in models.items():
        pipeline = Pipeline([
            ("preprocessing", preprocessor),
            ("classifier", classifier),
        ])

        cv_scores = cross_val_score(
            pipeline,
            X_train,
            y_train,
            cv=cv,
            scoring="f1",
        )

        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)

        fitted[name] = pipeline

        results.append({
            "model": name,
            "cv_f1_mean": cv_scores.mean(),
            "cv_f1_std": cv_scores.std(),
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

    results_df = pd.DataFrame(results).sort_values(
        "cv_f1_mean", ascending=False
    )
    results_df.to_csv(reports / "model_comparison.csv", index=False)

    print("\n========== MODEL COMPARISON ==========")
    print(results_df.round(3).to_string(index=False))

    # 5. Select using CV, then inspect the held-out test set
    best_name = results_df.iloc[0]["model"]
    best_model = fitted[best_name]
    predictions = best_model.predict(X_test)

    print("\nSelected model:", best_name)
    print("\nClassification report:")
    print(classification_report(
        y_test, predictions, zero_division=0
    ))
    print("Confusion matrix:")
    print(confusion_matrix(y_test, predictions))

    # 6. Export misclassified examples
    errors = X_test.copy()
    errors["actual"] = y_test
    errors["predicted"] = predictions
    errors["error_type"] = np.select(
        [
            (errors["actual"] == 0) & (errors["predicted"] == 1),
            (errors["actual"] == 1) & (errors["predicted"] == 0),
        ],
        ["False Positive", "False Negative"],
        default="Correct",
    )

    errors[errors["error_type"] != "Correct"].to_csv(
        reports / "misclassified_examples.csv", index=False
    )

    # 7. Save the entire pipeline, including preprocessing
    joblib.dump(best_model, models_dir / "best_model.joblib")

    print("\nFiles saved:")
    print("- day-10/reports/data_quality.csv")
    print("- day-10/reports/model_comparison.csv")
    print("- day-10/reports/misclassified_examples.csv")
    print("- day-10/models/best_model.joblib")


if __name__ == "__main__":
    main()
