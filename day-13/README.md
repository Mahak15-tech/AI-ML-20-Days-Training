# Day 13 – Dataset Quality and Annotation QA

## Overview
Performed dataset quality analysis and annotation validation on the COCO128 YOLO object detection dataset. The validation script checks image files, annotation files, matching image-label pairs, bounding box coordinates, and class IDs. A class distribution analysis was also performed to identify frequent and less frequent object categories.

## Objectives
- Validate image files and YOLO annotation files.
- Check matching image-label pairs.
- Identify missing annotations and orphan label files.
- Validate bounding box coordinates.
- Verify class IDs against the dataset configuration.
- Analyze class distribution and class imbalance.
- Generate structured CSV reports and visualizations.

## Technologies
- Python 3.10
- Ultralytics COCO128 Dataset
- Pillow
- Matplotlib
- CSV

## Project Structure
```text
day-13/
├── dataset/
│   └── coco128/
│       ├── images/
│       │   └── train2017/
│       └── labels/
│           └── train2017/
├── outputs/
│   ├── class_distribution.csv
│   ├── class_distribution.png
│   ├── class_imbalance_summary.txt
│   ├── split_summary.csv
│   └── validation_issues.csv
├── src/
│   ├── validate_dataset.py
│   └── analyze_class_distribution.py
├── requirements.txt
└── README.md
```

## Implementation
1. Loaded the COCO128 object detection dataset.
2. Checked image files and annotation files.
3. Validated image-label matching.
4. Checked YOLO bounding box coordinates and class IDs.
5. Applied a small tolerance of `1e-6` for floating-point boundary rounding.
6. Identified missing annotation files and orphan label files.
7. Counted annotated objects and unique classes.
8. Generated class distribution statistics.
9. Created a class distribution chart and imbalance summary.
10. Exported validation results into CSV reports.

## Run the Project
From the `day-13` directory:

```bash
pip install -r requirements.txt
python src/validate_dataset.py
python src/analyze_class_distribution.py
```

The scripts expect the COCO128 dataset to be available inside the `dataset/coco128` directory.

## Results

| Metric | Result |
|---|---:|
| Total images | 128 |
| Valid images | 128 |
| Total annotation files | 128 |
| Matched image-label pairs | 126 |
| Images without labels | 2 |
| Orphan annotation files | 2 |
| Empty annotation files | 0 |
| Annotated objects in matched pairs | 929 |
| Unique classes | 71 |
| Validation issues | 4 |

### Class Distribution Analysis

| Metric | Result |
|---|---:|
| Total annotated objects | 929 |
| Unique classes | 71 |
| Most frequent class | Class 0 |
| Class 0 objects | 254 |
| Class 0 percentage | 27.34% |
| Least frequent class count | 1 object |

### Dataset Issues Identified
- Two images do not have matching annotation files.
- Two annotation files do not have matching images.
- No empty annotation files were found.
- No bounding box validation errors remained after applying the floating-point tolerance.

### Class Imbalance
Class 0 contains 254 objects (27.34%), while several classes contain only one or two objects. This indicates an uneven distribution of annotated object categories.

## Output Files
- `outputs/class_distribution.csv`
- `outputs/class_distribution.png`
- `outputs/class_imbalance_summary.txt`
- `outputs/split_summary.csv`
- `outputs/validation_issues.csv`

## Key Learnings
- Understanding YOLO annotation format.
- Validating image and label consistency.
- Checking normalized bounding box coordinates.
- Identifying missing and orphan annotation files.
- Understanding class distribution and class imbalance.
- Generating dataset quality reports.
- Visualizing annotation statistics.

## Conclusion
Successfully performed dataset quality validation and annotation analysis on the COCO128 dataset. The analysis identified 929 annotated objects across 71 unique classes in matched image-label pairs and reported four image-label consistency issues. A class distribution chart and supporting reports were generated for further dataset analysis.

**Status: Completed**