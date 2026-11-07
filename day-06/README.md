# Day 06 – Machine Learning Preprocessing Pipeline

## Overview
Built a reusable preprocessing pipeline for preparing dataset features before model training. A pipeline helps keep transformations organized and consistent between training and inference.

## Objectives
- Understand common preprocessing steps.
- Build a Scikit-learn preprocessing pipeline.
- Apply transformations consistently.
- Save the fitted pipeline for reuse.

## Technologies
- Python 3.10
- Pandas
- Scikit-learn
- Joblib

## Project Structure
```text
day-06/
├── reports/
│   └── preprocessing_pipeline.joblib
├── src/
│   └── preprocessing_pipeline.py
├── requirements.txt
└── README.md
```

## Implementation
The script constructs the preprocessing workflow and saves the resulting pipeline using Joblib. The exact transformations and feature handling are defined in `src/preprocessing_pipeline.py`.

## Run the Project
From the `day-06` directory:

```bash
pip install -r requirements.txt
python src/preprocessing_pipeline.py
```

## Output
`reports/preprocessing_pipeline.joblib` – serialized preprocessing pipeline.

## Key Learnings
- Why preprocessing is important in machine learning.
- Building reusable Scikit-learn pipelines.
- Keeping transformations consistent.
- Saving and reloading Python objects with Joblib.
- Preparing a repeatable workflow for future model training.

## Conclusion
Successfully created and saved a reusable preprocessing pipeline for the student-data machine learning workflow.

**Status: Completed**
