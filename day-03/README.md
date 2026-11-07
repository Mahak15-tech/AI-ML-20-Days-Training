# Day 03 – Exploratory Data Analysis (EDA)

## Overview
Performed exploratory data analysis on the student dataset to understand distributions, relationships, and patterns in the available data. Visualizations were generated to support interpretation.

## Objectives
- Explore a structured student dataset.
- Summarize numerical and categorical information.
- Study relationships between study hours and marks.
- Compare average marks across departments.
- Visualize marks distribution and pass/fail counts.
- Examine correlations between numerical features.

## Technologies
- Python 3.10
- Pandas
- Matplotlib
- Seaborn (if included in the project requirements)

## Project Structure
```text
day-03/
├── data/
│   └── students.csv
├── reports/
│   ├── correlation_heatmap.png
│   ├── department_average_marks.png
│   ├── marks_distribution.png
│   ├── pass_fail_counts.png
│   └── study_hours_vs_marks.png
├── src/
│   └── eda.py
├── requirements.txt
└── README.md
```

## Implementation
The EDA script loads the student dataset, explores its features, and creates visual reports.

### Visualizations Generated
- **Correlation heatmap:** displays correlations between numerical variables.
- **Department average marks:** compares average marks across departments.
- **Marks distribution:** shows how marks are distributed.
- **Pass/fail counts:** summarizes the pass and fail categories.
- **Study hours vs. marks:** explores the relationship between study time and marks.

## Run the Project
From the `day-03` directory:

```bash
pip install -r requirements.txt
python src/eda.py
```

## Outputs
All generated visualizations are stored in `reports/`.

## Key Learnings
- Performing exploratory data analysis.
- Understanding distributions and feature relationships.
- Creating charts to communicate patterns.
- Using correlation analysis to explore numerical features.
- Saving plots for reporting and later reference.

## Conclusion
Successfully explored the student dataset and generated five visualizations to understand its characteristics and relationships.

**Status: Completed**
