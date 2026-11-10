# Day 15 – Mentor Review

## Training Topic
Detection Evaluation and Thresholding

## 1. Work Completed

The fine-tuned YOLOv8n object detection model was evaluated using the COCO128 validation dataset.

The following activities were completed:

- Evaluated overall detection performance using precision, recall, mAP@50 and mAP@50–95.
- Analyzed performance across 36 represented object classes.
- Compared four confidence thresholds: 0.10, 0.25, 0.50 and 0.75.
- Generated standard and normalized confusion matrices.
- Generated precision, recall, F1 and precision-recall curves.
- Developed a custom script to identify detection errors.
- Generated annotated images showing recorded detection errors.

## 2. Key Evaluation Results

| Metric | Result |
|---|---:|
| Precision | 72.38% |
| Recall | 63.85% |
| mAP@50 | 76.97% |
| mAP@50–95 | 58.72% |
| Validation images | 25 |
| Ground-truth objects | 156 |
| Error records | 106 |

## 3. Important Observations

1. The model achieved a reasonable overall mAP@50 score.
2. Confidence threshold 0.10 produced the highest recall among the tested thresholds.
3. Confidence threshold 0.50 produced the highest precision.
4. Some classes, including cell phone, knife, handbag and truck, showed low AP@50.
5. False negatives, false positives and poor localization were identified during error analysis.

## 4. Challenges and Limitations

- Limited validation data affected the reliability of class-wise comparisons.
- Some object classes had very few validation examples.
- The model missed certain objects and produced unmatched predictions.
- Confidence threshold selection involved a precision-recall trade-off.
- Evaluation was performed using CPU hardware.

## 5. Learning Outcomes

Through this task, I learned:

- How to evaluate an object detection model.
- The difference between precision, recall and mAP.
- How confidence thresholds influence detection results.
- How to interpret per-class performance.
- How to inspect confusion matrices and performance curves.
- How to identify false positives, false negatives and localization errors.

## 6. Future Improvements

- Increase the number of validation examples.
- Improve training data representation for weaker classes.
- Experiment with confidence thresholds based on application requirements.
- Inspect difficult examples and improve model performance.
- Evaluate the model on additional unseen images.

## 7. Final Status

**Day 15: Detection Evaluation and Thresholding – Completed**

The evaluation report, per-class analysis, threshold comparison, confusion matrices, performance curves and detection error examples have been generated.

**Mentor Review Status:** Submitted for mentor feedback.

---

**Student Reflection:**

This task helped me understand that evaluating an object detection model requires more than checking its overall accuracy. Analyzing class-wise performance, confidence thresholds and real detection errors provides a better understanding of model strengths and limitations.
