# Dataset Card: COCO128

## 1. Dataset Overview

| Field | Details |
|---|---|
| Dataset name | COCO128 |
| Dataset type | Object Detection |
| Annotation format | YOLO bounding-box format |
| Configured classes | 80 |
| Training images | 101 |
| Validation images | 25 |
| Total matched image-label pairs | 126 |
| Project usage | YOLOv8n fine-tuning and validation |

COCO128 was used as the dataset for the Day 14 YOLOv8n fine-tuning experiment.

## 2. Dataset Provenance

The project uses COCO128, a small sample dataset associated with the COCO object detection dataset and distributed for use with Ultralytics YOLO.

The dataset was prepared and organized during Day 13 and used for model training during Day 14.

The original Day 13 dataset was not modified.

**Provenance note:** The exact download URL, download date, and source archive checksum were not recorded in the project documentation.

## 3. Dataset Organization

The prepared dataset contains separate training and validation splits.

```text
dataset/
└── coco128/
    ├── images/
    │   ├── train/
    │   └── val/
    └── labels/
        ├── train/
        └── val/
```

Dataset configuration is maintained in `day-14/dataset/data.yaml`.

## 4. Annotation Information

Annotations use the YOLO object detection format.

Each annotated object is represented using:

- Class ID
- Normalized bounding-box center X
- Normalized bounding-box center Y
- Normalized bounding-box width
- Normalized bounding-box height

The dataset configuration defines 80 object classes, including person, bicycle, car, bus, dog, chair, and other everyday object categories.

## 5. Data Preparation

The dataset preparation process included:

1. Reviewing the Day 13 dataset quality results.
2. Organizing image and label files.
3. Creating training and validation splits.
4. Preparing the YOLO dataset configuration.
5. Verifying the expected image and label directories before training.

The Day 14 training configuration used 101 training images and 25 validation images.

## 6. Data Quality Considerations

The Day 13 quality assurance process identified annotation and image-label consistency issues in the original dataset.

The Day 14 README records 126 matched image-label pairs used for training and validation.

These figures describe the prepared Day 14 dataset. They should not be confused with the original Day 13 QA totals.

A complete revalidation of the final Day 14 split has not been documented here.

## 7. Known Dataset Limitations

- The dataset is small compared with large-scale object detection datasets.
- Some object categories may have fewer examples than others.
- Images may not represent all geographic locations or environmental conditions.
- Camera quality, lighting, image resolution, and object visibility vary.
- Annotation errors may affect model training and evaluation.
- The dataset may not represent specialized industrial or safety-critical environments.

## 8. Privacy and Ethical Considerations

The project should respect the dataset's original licensing and usage conditions.

Images should not be used to identify individuals or infer sensitive personal attributes.

Any additional images collected for experimentation should be obtained with appropriate permission and handled responsibly.

## 9. Recommended Future Improvements

- Record the original dataset download source and version.
- Preserve dataset checksums for reproducibility.
- Perform a fresh image-label integrity check before training.
- Analyze class distribution and annotation quality.
- Evaluate performance on additional representative datasets.
- Document dataset changes between project versions.

## 10. References

- [COCO Dataset](https://cocodataset.org/)
- [Ultralytics COCO Dataset Documentation](https://docs.ultralytics.com/datasets/detect/coco/)

---

**Project:** AI/ML 20-Day Training
**Dataset:** COCO128
**Purpose:** Object detection model training and evaluation