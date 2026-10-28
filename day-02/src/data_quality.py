from pathlib import Path

import numpy as np
import pandas as pd


def create_data_quality_report(csv_path: Path) -> pd.DataFrame:
    """Load a CSV and summarize its data quality."""
    df = pd.read_csv(csv_path)

    print("\n========== DATASET OVERVIEW ==========")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Total cells: {df.size}")

    print("\n========== FIRST 5 ROWS ==========")
    print(df.head())

    print("\n========== DATA TYPES ==========")
    print(df.dtypes)

    print("\n========== NUMERICAL SUMMARY ==========")
    print(df.describe(include="all").transpose())

    print("\n========== MISSING VALUES ==========")
    print(df.isnull().sum())

    print("\n========== DUPLICATE ROWS ==========")
    print(f"Duplicate rows: {df.duplicated().sum()}")

    # Demonstrate NumPy on the marks column.
    marks = df["marks"].dropna().to_numpy()
    print("\n========== NUMPY MARKS SUMMARY ==========")
    print(f"Mean marks: {np.mean(marks):.2f}")
    print(f"Minimum marks: {np.min(marks)}")
    print(f"Maximum marks: {np.max(marks)}")

    report = pd.DataFrame({
        "column": df.columns,
        "data_type": [str(dtype) for dtype in df.dtypes],
        "missing_values": df.isnull().sum().values,
        "missing_percentage": (
            df.isnull().mean().values * 100
        ).round(2),
        "unique_values": df.nunique().values,
    })

    return report


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    csv_path = project_root / "day-02" / "data" / "students.csv"
    report_path = project_root / "day-02" / "reports" / "data_quality_report.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    df_report = create_data_quality_report(csv_path)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    df_report.to_csv(report_path, index=False)

    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
