# Day 09 – Model Error Analysis and Interpretability

## Overview
Performed deeper analysis of model predictions to understand where classification errors occur, how performance varies across groups, and which features influence model predictions.

## Objectives
- Inspect misclassified examples.
- Examine model performance across groups.
- Estimate feature importance using permutation importance.
- Generate structured error-analysis reports.

## Technologies
- Python 3.10
- Pandas
- Scikit-learn

## Project Structure
```text
day-09/
├── reports/
│   ├── group_metrics.csv
│   ├── misclassified_examples.csv
│   └── permutation_importance.csv
├── src/
│   └── error_analysis.py
├── requirements.txt
└── README.md
```

## Implementation
The error-analysis script generates three reports:

- **Group metrics:** summarizes model performance across the groups defined in the analysis.
- **Misclassified examples:** records examples where predicted labels differ from actual labels.
- **Permutation importance:** estimates how model performance changes when individual features are shuffled.

The exact grouping fields, model, and importance scores are defined by the implementation and generated reports.

## Run the Project
From the `day-09` directory:

```bash
pip install -r requirements.txt
python src/error_analysis.py
```

Ensure the input dataset and model artifacts expected by the script are available.

## Outputs
- `reports/group_metrics.csv`
- `reports/misclassified_examples.csv`
- `reports/permutation_importance.csv`

## Key Learnings
- Looking beyond overall accuracy to understand model errors.
- Inspecting incorrect predictions.
- Comparing performance across data groups.
- Understanding permutation-based feature importance.
- Using error analysis to identify possible improvements.

## Conclusion
Successfully performed a deeper analysis of classification results and generated reports covering group performance, incorrect predictions, and feature importance.

**Status: Completed**
