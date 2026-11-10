
# Day 15: Detection Evaluation and Thresholding

## Objective
Evaluate the fine-tuned YOLO object detection model, compare confidence thresholds, analyze per-class performance, and inspect detection errors.

**Learning outcome:** Evaluate detection performance and inspect real model failures.

## 1. Dataset and Model

- **Model:** Fine-tuned YOLOv8n
- **Model weights:** `../day-14/outputs/yolov8n_finetuned/weights/best.pt`
- **Validation dataset:** COCO128
- **Validation images:** 25
- **Ground-truth objects:** 156
- **Classes represented in validation:** 36
- **Framework:** Ultralytics 8.4.204
- **Execution:** Python 3.10.11, CPU

Day 15 uses the model and dataset from Day 14 for evaluation. The original Day 14 files are not modified.

## 2. Overall Evaluation Results

| Metric | Result |
|---|---:|
| Precision | 72.38% |
| Recall | 63.85% |
| mAP@50 | 76.97% |
| mAP@50-95 | 58.72% |

The model demonstrates reasonable detection performance on the validation set. The difference between mAP@50 and mAP@50-95 indicates that stricter localization requirements reduce the measured performance.

Detailed results are saved in `reports/evaluation_metrics.csv`.

## 3. Per-Class Performance

Per-class evaluation was performed for 36 classes represented in the validation set.

The analysis includes:
- Class ID and class name
- Precision
- Recall
- AP@50
- AP@50-95

Some classes show weaker detection results, including cell phone, knife, handbag, truck, and teddy bear.

Classes with very few validation examples may show unstable or unusually high scores. Therefore, per-class metrics should be interpreted alongside the number of available examples.

**Output:** `reports/per_class_performance.csv`

## 4. Confidence Threshold Comparison

The model was evaluated using four confidence thresholds.

| Confidence | Precision | Recall | mAP@50 | mAP@50-95 |
|---:|---:|---:|---:|---:|
| 0.10 | 0.6145 | 0.6387 | 0.6702 | 0.5192 |
| 0.25 | 0.6241 | 0.6239 | 0.6170 | 0.4817 |
| 0.50 | 0.6993 | 0.4993 | 0.4950 | 0.4007 |
| 0.75 | 0.5833 | 0.3559 | 0.3535 | 0.3173 |

### Observations

- Confidence 0.10 produced the highest recall among the tested thresholds.
- Confidence 0.50 produced the highest precision.
- Higher confidence thresholds generally reduced recall.
- Confidence 0.75 produced substantially lower recall.

For this experiment, 0.10 provided the highest recall, while 0.50 provided the highest precision among the tested settings.

**Output:** `reports/threshold_comparison.csv`

Note: These are validation metrics obtained under the tested confidence settings. Conventional mAP is generally calculated across confidence rankings, so these threshold-specific mAP values should not be interpreted as a replacement for the baseline mAP evaluation.

## 5. Detection Error Analysis

A custom error-analysis script inspected predictions against ground-truth annotations.

| Error category | Records |
|---|---:|
| False negatives | 53 |
| False positives | 38 |
| Poor localization | 15 |
| **Total error records** | **106** |

The analysis processed 25 validation images, with errors recorded across 18 images.

Classes with comparatively high error counts included:
- Person
- Car
- Chair
- Cup
- Kite
- Knife
- Dining table
- Teddy bear
- Cell phone
- Sports ball

These results identify areas that may benefit from further training, improved data coverage, or threshold tuning.

**Outputs:**
- `reports/detection_error_examples.csv`
- `outputs/error_examples/`

The error categories are records produced by the custom matching procedure; they should not automatically be interpreted as 106 unique failed objects.

## 6. Evaluation Visualizations

The following visual outputs were generated:

- `confusion_matrix.png`
- `confusion_matrix_normalized.png`
- `BoxP_curve.png`
- `BoxR_curve.png`
- `BoxF1_curve.png`
- `BoxPR_curve.png`
- `val_batch0_labels.jpg`
- `val_batch0_pred.jpg`
- `val_batch1_labels.jpg`
- `val_batch1_pred.jpg`
- `val_batch2_labels.jpg`
- `val_batch2_pred.jpg`

Location: `outputs/model_evaluation/`

These visualizations help inspect class-level predictions, missed objects, incorrect detections, and model performance curves.

## 7. Limitations

- The validation set contains only 25 images.
- Only 36 of the 80 COCO classes are represented in this validation subset.
- Several classes have limited examples, making their individual metrics less reliable.
- Confidence threshold selection involves a precision-recall trade-off.
- The error-analysis results depend on the custom IoU-based matching procedure.
- Further evaluation on a larger and more representative dataset is recommended.

## 8. Project Structure

```text
day-15/
├── src/
│   ├── evaluate_model.py
│   ├── analyze_class_performance.py
│   ├── compare_thresholds.py
│   └── analyze_detection_errors.py
├── reports/
│   ├── evaluation_metrics.csv
│   ├── per_class_performance.csv
│   ├── threshold_comparison.csv
│   └── detection_error_examples.csv
├── outputs/
│   ├── model_evaluation/
│   └── error_examples/
├── dataset.yaml
├── requirements.txt
└── README.md
```

## 9. Conclusion

Day 15 completed the evaluation of the fine-tuned YOLO object detection model. Overall metrics, per-class performance, confidence threshold comparisons, confusion matrices, performance curves, and detection error examples were generated.

The experiment demonstrated the importance of evaluating both overall model performance and individual detection failures. It also showed that confidence threshold selection affects the balance between precision and recall.

**Status: Day 15 evaluation and analysis completed.**
