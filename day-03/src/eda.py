from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    project_root = Path(__file__).resolve().parents[2]
    data_path = project_root / "day-03" / "data" / "students.csv"
    reports_path = project_root / "day-03" / "reports"
    reports_path.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)

    print("========== DATASET OVERVIEW ==========")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print("\nDataset information:")
    df.info()

    print("\n========== SUMMARY STATISTICS ==========")
    print(df.describe())

    print("\n========== PASS CLASS COUNTS ==========")
    print(df["passed"].value_counts())

    print("\n========== CORRELATION MATRIX ==========")
    print(df[["study_hours", "attendance", "marks"]].corr().round(2))

    sns.set_theme(style="whitegrid")

    # Plot 1: Distribution of marks
    plt.figure(figsize=(8, 5))
    sns.histplot(df["marks"], bins=8, kde=True)
    plt.title("Distribution of Student Marks")
    plt.xlabel("Marks")
    plt.tight_layout()
    plt.savefig(reports_path / "marks_distribution.png")
    plt.close()

    # Plot 2: Pass and fail counts
    plt.figure(figsize=(7, 5))
    sns.countplot(data=df, x="passed")
    plt.title("Pass vs Fail Counts")
    plt.tight_layout()
    plt.savefig(reports_path / "pass_fail_counts.png")
    plt.close()

    # Plot 3: Study hours versus marks
    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        data=df,
        x="study_hours",
        y="marks",
        hue="passed"
    )
    plt.title("Study Hours vs Marks")
    plt.tight_layout()
    plt.savefig(reports_path / "study_hours_vs_marks.png")
    plt.close()

    # Plot 4: Average marks by department
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="department", y="marks", errorbar=None)
    plt.title("Average Marks by Department")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(reports_path / "department_average_marks.png")
    plt.close()

    # Plot 5: Correlation heatmap
    plt.figure(figsize=(7, 5))
    sns.heatmap(
        df[["study_hours", "attendance", "marks"]].corr(),
        annot=True,
        cmap="coolwarm",
        vmin=-1,
        vmax=1
    )
    plt.title("Feature Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(reports_path / "correlation_heatmap.png")
    plt.close()

    print("\nAll five plots saved in day-03/reports/")


if __name__ == "__main__":
    main()
