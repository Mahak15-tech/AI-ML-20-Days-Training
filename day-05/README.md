# Day 05 – Baseline Classification Model

## Overview
Developed a baseline classification model to establish an initial performance reference before trying more advanced models or tuning strategies.

## Objectives
- Understand the classification workflow.
- Train an initial classifier.
- Generate predictions.
- Evaluate baseline performance.
- Save model metrics in a structured report.

## Technologies
- Python 3.10
- Pandas
- Scikit-learn

## Project Structure
```text
day-05/
├── reports/
│   └── baseline_metrics.csv
├── src/
│   └── baseline_classifier.py
├── requirements.txt
└── README.md
```

## Implementation
The script builds and evaluates a baseline classifier using the prepared student dataset. Its evaluation results are exported to a CSV file.

The exact algorithm, train/test configuration, and metric values should be taken from `src/baseline_classifier.py` and `reports/baseline_metrics.csv`.

## Run the Project
From the `day-05` directory:

```bash
pip install -r requirements.txt
python src/baseline_classifier.py
```

Ensure any dataset path expected by the script is available.

## Output
`reports/baseline_metrics.csv` – contains the baseline model's evaluation metrics.

## Key Learnings
- Understanding supervised classification.
- Establishing a baseline before model comparison.
- Generating predictions from a trained classifier.
- Evaluating and recording model performance.
- Using baseline results as a reference for later experiments.

## Conclusion
Successfully implemented a baseline classification workflow and saved its evaluation metrics for comparison with subsequent models.

**Status: Completed**
