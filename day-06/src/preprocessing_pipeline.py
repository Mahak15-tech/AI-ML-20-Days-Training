
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report


def main():
    project_root = Path(__file__).resolve().parents[2]
    reports_dir = project_root / "day-06" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Sample dataset with missing values
    df = pd.DataFrame({
        "study_hours": [2, 5, 3, 7, 1, 6, 4, 8, 2, 5, 6, 3,
                        7, 1, 4, 8, 5, 2, 6, 4],
        "attendance": [60, 90, 75, 95, 50, 92, 80, 98, 65, 85,
                       93, 70, 96, 55, 82, 97, 88, 62, 91, 78],
        "department": ["AI", "Data Science", "AI", "ML", "AI",
                       "Data Science", "ML", "AI", "ML", "Data Science",
                       "AI", "ML", "Data Science", "AI", "ML",
                       "Data Science", "AI", "ML", "Data Science", "AI"],
        "marks": [45, 82, None, 95, 35, 90, 70, 98, 48, 80,
                  91, 60, 94, 30, 74, 97, 85, 42, 92, 68],
        "passed": [0, 1, 1, 1, 0, 1, 1, 1, 0, 1,
                   1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    })

    # Add a missing categorical value
    df.loc[3, "department"] = None

    X = df.drop(columns="passed")
    y = df["passed"]

    numeric_features = ["study_hours", "attendance", "marks"]
    categorical_features = ["department"]

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

    model_pipeline = Pipeline([
        ("preprocessing", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000)),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model_pipeline.fit(X_train, y_train)
    predictions = model_pipeline.predict(X_test)

    print("Training rows:", len(X_train))
    print("Testing rows:", len(X_test))
    print("Accuracy:", round(accuracy_score(y_test, predictions), 3))
    print("\nClassification report:")
    print(classification_report(y_test, predictions, zero_division=0))

    # Save a reusable preprocessing pipeline
    from joblib import dump

    dump(model_pipeline, reports_dir / "preprocessing_pipeline.joblib")
    print("\nPipeline saved to day-06/reports/preprocessing_pipeline.joblib")


if __name__ == "__main__":
    main()
