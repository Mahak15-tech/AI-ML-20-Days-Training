# Day 15 – Detection Evaluation and Thresholding Report

## 1. Introduction

This report evaluates the fine-tuned YOLOv8n object detection model developed during Day 14. The purpose is to measure detection performance, compare confidence thresholds, analyze class-wise results, and identify real detection errors.

## 2. Evaluation Setup

| Parameter | Details |
|---|---|
| Model | Fine-tuned YOLOv8n |
| Dataset | COCO128 |
| Evaluation split | Validation |
| Validation images | 25 |
| Ground-truth objects | 156 |
| Evaluated classes | 36 |
| Framework | Ultralytics 8.4.204 |
| Python | 3.10.11 |
| Hardware | CPU |

## 3. Overall Evaluation Results

| Metric | Result |
|---|---:|
| Precision | 0.7238 |
| Recall | 0.6385 |
| mAP@50 | 0.7697 |
| mAP@50–95 | 0.5872 |

The model achieved 76.97% mAP@50 and 58.72% mAP@50–95. The recall score indicates that some ground-truth objects were not detected.

## 4. Confidence Threshold Analysis

Four confidence thresholds were compared.

| Confidence | Precision | Recall | mAP@50 | mAP@50–95 |
|---:|---:|---:|---:|---:|
| 0.10 | 0.6145 | 0.6387 | 0.6702 | 0.5192 |
| 0.25 | 0.6241 | 0.6239 | 0.6170 | 0.4817 |
| 0.50 | 0.6993 | 0.4993 | 0.4950 | 0.4007 |
| 0.75 | 0.5833 | 0.3559 | 0.3535 | 0.3173 |

### Findings

- The 0.10 threshold achieved the highest recall.
- The 0.50 threshold achieved the highest precision.
- The 0.75 threshold had the lowest recall.
- A suitable confidence threshold depends on whether reducing false positives or detecting more objects is the priority.

## 5. Per-Class Analysis

The model was evaluated across 36 represented classes.

Examples of strong AP@50 results included train, motorcycle, dog, cat, zebra and remote.

Lower AP@50 results included:

- Cell phone: 0.0990
- Knife: 0.0990
- Handbag: 0.1244
- Truck: 0.1546
- Teddy bear: 0.1760

These classes require further investigation. The small validation set and uneven class representation limit the reliability of individual class scores.

## 6. Detection Error Analysis

The custom error analysis processed 25 validation images.

| Error category | Records |
|---|---:|
| False negatives | 53 |
| False positives | 38 |
| Poor localization | 15 |
| Total error records | 106 |

The analysis recorded errors across 18 images. Person and car were among the classes with the highest recorded error counts.

The annotated images are available in `outputs/error_examples/`, and the detailed records are stored in `detection_error_examples.csv`.

Note: Error records are not guaranteed to represent unique failed objects because the matching procedure can record both a localization issue and an unmatched prediction.

## 7. Generated Evaluation Outputs

The evaluation generated:

1. Overall evaluation metrics.
2. Per-class performance CSV.
3. Confidence threshold comparison CSV.
4. Detection error examples CSV.
5. Precision, recall, F1 and PR curves.
6. Standard and normalized confusion matrices.
7. Validation label and prediction images.
8. Annotated detection error images.

## 8. Limitations

- Evaluation used only 25 validation images.
- Only 36 classes were represented in the validation results.
- Class-wise performance may vary considerably because of limited examples.
- CPU-based inference is slower than GPU-based inference.
- The custom error matching procedure has limitations when categorizing overlapping localization and unmatched-prediction errors.

## 9. Conclusion

The Day 15 evaluation successfully measured the fine-tuned YOLOv8n model using standard object detection metrics. Confidence threshold comparison demonstrated the trade-off between precision and recall. Per-class analysis highlighted categories requiring improvement, while custom error analysis identified missed detections, false positives and localization problems.

The evaluation provides a foundation for improving detection reliability and preparing the model for inference deployment.

**Final outcome:** Detection evaluation, threshold comparison, per-class analysis and real error inspection were completed.
