# Day 10 – Student Performance Prediction and Analytics Dashboard

## Overview
Developed a student-performance classification mini-project and an interactive web dashboard to present dataset insights, model performance, and prediction analysis.

## Objectives
- Build an end-to-end machine learning workflow.
- Inspect and prepare the student dataset.
- Compare classification models.
- Evaluate the selected model.
- Save the trained model and evaluation reports.
- Present project results through a dashboard.

## Technologies
- Python 3.10
- Pandas
- Scikit-learn
- Joblib
- HTML, CSS, JavaScript
- Plotly (where used by the dashboard)

## Project Structure
```text
day-10/
├── dashboard/
│   ├── app.js
│   ├── index.html
│   ├── server.py
│   └── style.css
├── data/
│   └── students.csv
├── models/
│   └── best_model.joblib
├── reports/
│   ├── class_metrics.csv
│   ├── confusion_matrix.json
│   ├── data_quality.csv
│   ├── misclassified_examples.csv
│   └── model_comparison.csv
├── src/
│   └── mini_project.py
├── requirements.txt
├── vercel.json
└── README.md
```

## Implementation
The mini-project covers data inspection, preprocessing, model comparison, model evaluation, and saving the selected model. The dashboard presents the resulting information through sections for overview, model performance, prediction analysis, data intelligence, and project methodology.

### Dataset and Model Notes
- Dataset size used in the training workflow: 400 rows and 4 columns.
- Missing values identified: 12 in `study_hours` and 10 in `department`.
- Logistic Regression was selected over Random Forest in the recorded comparison.

### Recorded Evaluation Results
| Metric | Logistic Regression |
|---|---:|
| Test accuracy | 71.2% |
| Precision | 71.4% |
| Recall | 79.5% |
| F1-score | 75.3% |
| Cross-validation F1 | 72.3% |

Random Forest recorded 67.5% test accuracy and 71.1% F1-score in the comparison.

## Run the Machine Learning Script
From the `day-10` directory:

```bash
pip install -r requirements.txt
python src/mini_project.py
```

## Run the Dashboard
From the `day-10` directory:

```bash
python dashboard/server.py
```

Open the local address printed by the server in a browser. Deployment configuration is included in `vercel.json`; deployment may require the matching Vercel project settings and runtime dependencies.

## Outputs
- Trained model: `models/best_model.joblib`
- Model comparison: `reports/model_comparison.csv`
- Class metrics: `reports/class_metrics.csv`
- Confusion matrix: `reports/confusion_matrix.json`
- Data quality report: `reports/data_quality.csv`
- Misclassified records: `reports/misclassified_examples.csv`
- Interactive dashboard files: `dashboard/`

## Key Learnings
- Building an end-to-end classification mini-project.
- Comparing Logistic Regression and Random Forest.
- Evaluating models with accuracy, precision, recall, and F1-score.
- Saving model artifacts with Joblib.
- Creating a dashboard to communicate ML results.
- Organizing reports and deployment configuration.

## Conclusion
Successfully developed a student-performance prediction workflow, saved the selected model and evaluation reports, and built a dashboard to communicate the results.

**Status: Completed**
