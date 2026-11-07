# Day 02 – Data Quality Analysis

## Overview
Created a data-quality analysis script to inspect a student dataset and identify common data issues before analysis or model development.

## Objectives
- Load a CSV dataset using Pandas.
- Inspect dataset dimensions and columns.
- Identify missing values.
- Detect duplicate records.
- Export a data-quality report.

## Technologies
- Python 3.10
- Pandas
- CSV

## Project Structure
```text
day-02/
├── data/
│   └── students.csv
├── reports/
│   └── data_quality_report.csv
├── src/
│   └── data_quality.py
├── requirements.txt
└── README.md
```

## Implementation
The script examines the student dataset and generates a CSV report describing data-quality issues.

### Recorded Findings
| Check | Result |
|---|---:|
| Records | 8 |
| Columns | 6 |
| Duplicate records | 1 |
| Missing age values | 1 |
| Missing marks values | 1 |

## Run the Project
From the `day-02` directory:

```bash
pip install -r requirements.txt
python src/data_quality.py
```

## Output
The generated report is saved at:

`reports/data_quality_report.csv`

## Key Learnings
- Loading and inspecting tabular data with Pandas.
- Checking dataset dimensions and column information.
- Identifying missing values and duplicate records.
- Exporting analysis results to CSV.
- Understanding why data quality matters before machine learning.

## Conclusion
Successfully performed an initial data-quality assessment and generated a report for the student dataset.

**Status: Completed**
