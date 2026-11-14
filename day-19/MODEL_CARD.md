@'
# Model Card: Fine-Tuned YOLOv8n Object Detector

## 1. Model Overview

| Field | Details |
|---|---|
| Model name | YOLOv8n Fine-Tuned Object Detector |
| Model architecture | YOLOv8n |
| Model type | Object Detection |
| Framework | Ultralytics YOLO |
| Model weights | `day-18/backend/models/best.pt` |
| Input | Static images |
| Output | Object classes, confidence scores, and bounding boxes |
| Number of configured classes | 80 |

This model was developed as part of a 20-day AI/ML training project. It was fine-tuned using the COCO128 dataset and integrated into a FastAPI backend with a React frontend.

## 2. Intended Use

### Appropriate Uses
- Educational demonstrations of object detection.
- Experimentation with computer vision.
- Detecting supported everyday object categories in images.
- Learning and evaluating YOLO-based detection pipelines.
- Non-critical image analysis and prototyping.

### Uses Outside the Intended Scope
- Medical or clinical decision-making.
- Autonomous driving or vehicle control.
- Safety-critical monitoring.
- Law enforcement or consequential decisions about individuals.
- Identity recognition, facial recognition, or biometric identification.
- Unsupervised surveillance or tracking of people.

The model should not be used as the sole basis for decisions that could affect a person's safety, rights, or opportunities.

## 3. Dataset and Training Information

| Field | Details |
|---|---|
| Dataset | COCO128 |
| Training images | 101 |
| Validation images | 25 |
| Matched image-label pairs | 126 |
| Configured classes | 80 |
| Initial weights | Pretrained YOLOv8n from Day 12 |
| Maximum epochs | 30 |
| Completed epochs | 12 |
| Best epoch | 2 |
| Image size | 640 × 640 |
| Batch size | 8 |
| Device | CPU |
| Random seed | 42 |
| Early stopping patience | 10 |

Training used early stopping. The best checkpoint was selected based on validation performance.

## 4. Evaluation Results

The following metrics were obtained on the Day 14 validation split.

| Metric | Result |
|---|---:|
| Precision | 0.7366 |
| Recall | 0.6397 |
| mAP@50 | 0.7755 |
| mAP@50–95 | 0.5894 |

The model achieved approximately 77.55% mAP@50 on this validation split.

These results describe performance on the recorded validation dataset. They should not be interpreted as a guarantee of performance on unseen real-world environments.

## 5. API Performance

Day 17 evaluated the FastAPI prediction service locally on CPU.

| Measurement | Result |
|---|---:|
| Average API response time | 161.41 ms |
| Minimum API response time | 156.15 ms |
| Maximum API response time | 167.18 ms |
| Average inference time | 92.60 ms |
| Average detections per request | 5 |
| Automated tests passed | 4 / 4 |

The benchmark used one warm-up request followed by five measured requests. It does not include cold-start time, and memory consumption was not measured.

API latency is an operational measurement, not an object-detection accuracy metric.

## 6. Limitations

- The training and validation dataset is small.
- Performance may vary across environments and image conditions.
- Small, distant, blurred, or partially occluded objects may be missed.
- Cluttered scenes can produce false detections.
- The model may produce incorrect class labels or bounding boxes.
- Confidence scores are not guaranteed probabilities of correctness.
- No comprehensive real-world or subgroup fairness evaluation has been documented.
- Performance on domains outside the training dataset has not been established.

## 7. Bias and Fairness Considerations

COCO128 is a limited sample dataset and may not represent the full diversity of real-world environments, objects, cameras, and image conditions.

No dedicated demographic fairness audit or subgroup performance evaluation has been documented for this project.

Users should independently evaluate performance in the specific environments where the model may be used.

## 8. Privacy and Responsible Use

Images uploaded for detection may contain faces, personal information, private locations, or other sensitive content.

Users should:
- Upload only images they have permission to process.
- Avoid uploading confidential or sensitive images.
- Avoid unnecessary storage or sharing of uploaded images.
- Review image outputs before distributing them.
- Follow applicable privacy and data-protection requirements.

This object detector is not an identity recognition system.

## 9. Model Provenance

The model was developed through the following project stages:

1. Day 12: Initial YOLOv8n object detection.
2. Day 13: Dataset quality and annotation checks.
3. Day 14: YOLOv8n fine-tuning and validation.
4. Day 17: API testing and performance benchmarking.
5. Day 18: Full-stack object detection application.

The final application model is stored at:

`day-18/backend/models/best.pt`

## 10. Ethical Considerations

Model predictions are estimates and can be incorrect. Human review is recommended before acting on important predictions.

The model should be used transparently, responsibly, and only within its documented capabilities.

## 11. Documentation References

- [Google Model Cards](https://modelcards.withgoogle.com/about)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

---

**Project:** AI/ML 20-Day Training
**Documentation:** Day 19 – Robustness, Ethics, and Documentation
'@ | Set-Content -Encoding UTF8 .\day-19\MODEL_CARD.md

Write-Host "MODEL_CARD.md created successfully!"