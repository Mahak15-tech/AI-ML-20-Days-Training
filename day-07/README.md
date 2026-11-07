# Day 07 – Machine Learning Model Comparison

## Overview
Compared machine learning models to understand how different algorithms perform on the same classification task. Model comparison helps identify a suitable candidate for further evaluation.

## Objectives
- Train and compare classification algorithms.
- Evaluate models using consistent metrics.
- Organize comparison results.
- Identify promising models for subsequent analysis.

## Technologies
- Python 3.10
- Pandas
- Scikit-learn

## Project Structure
```text
day-07/
├── reports/
│   └── model_comparison.csv
├── src/
│   └── model_comparison.py
├── requirements.txt
└── README.md
```

## Implementation
The script runs the model-comparison workflow and exports the results to a CSV file. The exact algorithms, evaluation metrics, and scores are recorded in the source code and report.

## Run the Project
From the `day-07` directory:

```bash
pip install -r requirements.txt
python src/model_comparison.py
```

Ensure the dataset path expected by the script is available.

## Output
`reports/model_comparison.csv` – contains the model comparison results.

## Key Learnings
- Understanding differences between classification algorithms.
- Comparing models using a consistent evaluation process.
- Interpreting model metrics.
- Using experiment reports to support model selection.

## Conclusion
Successfully implemented a model-comparison workflow and generated a report to support the selection of a candidate classifier.

**Status: Completed**
