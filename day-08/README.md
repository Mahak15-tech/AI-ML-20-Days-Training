# Day 08 – Classification Evaluation Metrics

## Overview
Evaluated classification model performance using common classification metrics and a confusion matrix. This day focuses on understanding model predictions beyond accuracy alone.

## Objectives
- Evaluate classification predictions.
- Understand accuracy, precision, recall, and F1-score.
- Generate a confusion matrix.
- Compare evaluation metrics across models.
- Save evaluation results.

## Technologies
- Python 3.10
- Pandas
- Scikit-learn
- Matplotlib

## Project Structure
```text
day-08/
├── reports/
│   ├── confusion_matrix.png
│   └── metrics_comparison.csv
├── src/
│   └── evaluation_metrics.py
├── requirements.txt
└── README.md
```

## Implementation
The script calculates classification evaluation metrics, creates a confusion-matrix visualization, and exports a metrics comparison report.

### Metrics
- **Accuracy:** proportion of all predictions that are correct.
- **Precision:** proportion of predicted positive cases that are actually positive.
- **Recall:** proportion of actual positive cases correctly identified.
- **F1-score:** harmonic mean of precision and recall.

## Run the Project
From the `day-08` directory:

```bash
pip install -r requirements.txt
python src/evaluation_metrics.py
```

Ensure the input data or model outputs expected by the script are available.

## Outputs
- `reports/confusion_matrix.png`
- `reports/metrics_comparison.csv`

## Key Learnings
- Evaluating classification models with multiple metrics.
- Reading and interpreting a confusion matrix.
- Understanding precision and recall trade-offs.
- Comparing model performance systematically.

## Conclusion
Successfully generated classification evaluation metrics and a confusion-matrix visualization to examine model performance.

**Status: Completed**
