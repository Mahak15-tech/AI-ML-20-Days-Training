# Model Limitations and Failure Analysis

## 1. Overview

This document describes the known limitations and potential failure modes of the fine-tuned YOLOv8n object detection model.

The model was trained using COCO128 and integrated into a FastAPI and React application.

Its predictions should be treated as estimates rather than guaranteed results.

## 2. Dataset Limitations

- The training dataset contains only 101 images.
- The validation dataset contains only 25 images.
- The dataset is a small sample and may not represent all real-world conditions.
- Object categories may have unequal representation.
- Annotation errors can affect model learning and evaluation.
- The dataset's coverage of specialized environments has not been established.

## 3. Model Performance Limitations

The recorded Day 14 validation metrics are:

| Metric | Result |
|---|---:|
| Precision | 0.7366 |
| Recall | 0.6397 |
| mAP@50 | 0.7755 |
| mAP@50–95 | 0.5894 |

These metrics describe performance on the project's validation split only.

They do not guarantee equivalent accuracy on unseen images or different deployment environments.

## 4. Potential Failure Modes

| Condition | Possible Failure |
|---|---|
| Low lighting | Missed or incorrect detections |
| Motion blur | Poor bounding-box localization |
| Small objects | Objects may not be detected |
| Occlusion | Partially hidden objects may be missed |
| Cluttered backgrounds | False positive detections |
| Unusual viewpoints | Incorrect object classification |
| Overlapping objects | Inaccurate bounding boxes |
| Unfamiliar environments | Reduced detection performance |

## 5. Confidence Score Limitations

The model produces confidence scores for detected objects.

These scores should not automatically be interpreted as calibrated probabilities.

A high confidence score does not guarantee a correct prediction, and a low score does not always mean an object is absent.

The application uses a configurable confidence threshold, with a default value of 0.25.

Changing this threshold can affect the number of detections, false positives, and false negatives.

## 6. Operational Limitations

Day 17 measured the API performance locally on CPU.

| Measurement | Result |
|---|---:|
| Average API response | 161.41 ms |
| Average inference time | 92.60 ms |

These measurements used warmed-up requests and excluded cold-start time.

The benchmark used only five measured requests. Memory consumption, concurrent-user performance, and large-scale production throughput were not measured.

## 7. Generalization Limitations

The model may perform differently when processing:

- Images from unfamiliar cameras.
- Outdoor and indoor environments with different lighting.
- Objects with unusual appearances.
- Images with resolutions or quality unlike the training data.
- Specialized industrial or medical imagery.

Performance in these conditions requires additional testing.

## 8. Responsible Deployment Recommendations

Before using the model in a new environment:

1. Test it on representative images.
2. Evaluate false positives and false negatives.
3. Review predictions manually.
4. Check performance across relevant object categories.
5. Avoid safety-critical use without independent validation.
6. Document changes to the model and dataset.
7. Monitor performance after deployment.

## 9. Future Improvements

- Increase dataset size and diversity.
- Improve annotation quality.
- Perform class-wise evaluation.
- Evaluate additional real-world datasets.
- Conduct robustness testing under different image conditions.
- Measure memory usage and concurrent API performance.
- Perform more extensive security and privacy testing.
- Evaluate confidence calibration.

## 10. Conclusion

The fine-tuned YOLOv8n model demonstrates object detection capabilities on the COCO128 validation dataset.

However, its small training dataset, limited validation coverage, and untested real-world conditions restrict the conclusions that can be drawn about generalization.

Responsible use requires human oversight, additional validation, and clear communication of limitations.

---

**Project:** AI/ML 20-Day Training
**Documentation:** Day 19 – Robustness, Ethics, and Documentation