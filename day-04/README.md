# Day 04 – Dataset Splitting

## Overview
Implemented a data-splitting workflow to prepare data for machine learning. Separating data into training and testing subsets helps evaluate how well a model performs on data it has not seen during training.

## Objectives
- Understand why datasets are split.
- Separate features and target labels.
- Create training and testing subsets.
- Record the split details in a report.
- Prepare data for baseline model development.

## Technologies
- Python 3.10
- Pandas
- Scikit-learn

## Project Structure
```text
day-04/
├── reports/
│   └── split_summary.csv
├── src/
│   └── data_splitting.py
├── requirements.txt
└── README.md
```

## Implementation
The script performs the dataset-splitting workflow and saves a summary of the split. The exact split ratio and record counts should be read from the generated report rather than assumed.

## Run the Project
From the `day-04` directory:

```bash
pip install -r requirements.txt
python src/data_splitting.py
```

If the script reads a dataset from an earlier day, ensure that the expected dataset path is available.

## Output
`reports/split_summary.csv` – records the dataset split summary.

## Key Learnings
- Understanding training and testing datasets.
- Separating input features from target labels.
- Preparing data for model training and evaluation.
- Recording preprocessing steps for reproducibility.

## Conclusion
Successfully implemented a dataset-splitting step and generated a summary report for the machine learning workflow.

**Status: Completed**
