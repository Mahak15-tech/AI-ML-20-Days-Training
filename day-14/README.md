# Day 14: YOLO Model Fine-Tuning

## Objective
Fine-tune a pretrained YOLOv8n object detection model using the COCO128 dataset, evaluate its performance, and generate predictions on test images.

## Technologies Used
- Python 3.10.11
- Ultralytics YOLOv8
- PyTorch
- OpenCV
- PyYAML
- Pandas
- Matplotlib

## Dataset
**Dataset:** COCO128

- Total matched image-label pairs: 126
- Training images: 101
- Validation images: 25
- Number of classes: 80
- Validation objects: 156

The dataset was prepared using the Day 13 dataset quality and annotation QA outputs. The original Day 13 dataset was not modified.

## Implementation

1. Prepared the COCO128 dataset and created training and validation splits.
2. Loaded pretrained YOLOv8n weights from Day 12.
3. Fine-tuned the model using the prepared dataset.
4. Used early stopping to prevent unnecessary training.
5. Evaluated the best checkpoint on the validation dataset.
6. Generated predictions on the Day 12 test images.
7. Exported evaluation metrics and prediction details into CSV reports.

## Training Configuration
- Model: YOLOv8n
- Maximum epochs: 30
- Epochs completed: 12
- Best epoch: 2
- Image size: 640 × 640
- Batch size: 8
- Device: CPU
- Random seed: 42
- Early stopping patience: 10

Training stopped early because validation performance did not improve sufficiently.

## Model Evaluation Results

| Metric | Result |
|---|---:|
| Precision | 0.7366 |
| Recall | 0.6397 |
| mAP@50 | 0.7755 |
| mAP@50–95 | 0.5894 |

The fine-tuned model achieved 77.55% mAP@50 on the validation split.

## Prediction Results

Predictions were generated on two test images:

**input.png**
- Persons: 5
- Bicycle: 1
- Bus: 1
- Handbags: 2

**test_image.png**
- Persons: 6
- Bicycle: 1
- Cars: 7
- Bus: 1
- Traffic light: 1
- Dog: 1
- Handbag: 1

Annotated prediction images were saved successfully.

## Project Structure

```text
day-14/
│
├── dataset/
│   ├── coco128/
│   │   ├── images/
│   │   │   ├── train/
│   │   │   └── val/
│   │   └── labels/
│   │       ├── train/
│   │       └── val/
│   └── data.yaml
│
├── models/
│   └── yolov8n.pt
│
├── outputs/
│   ├── data.yaml
│   ├── yolov8n_finetuned/
│   │   └── weights/
│   │       ├── best.pt
│   │       └── last.pt
│   └── predictions/
│       ├── input.png
│       └── test_image.png
│
├── reports/
│   ├── evaluation_metrics.csv
│   ├── prediction_results.csv
│   └── validation/
│
├── src/
│   ├── prepare_dataset.py
│   ├── train_yolo.py
│   └── evaluate_yolo.py
│
├── requirements.txt
└── README.md
```

## How to Run

Install dependencies:

```bash
pip install -r day-14/requirements.txt
```

Prepare the dataset:

```bash
python day-14/src/prepare_dataset.py
```

Train the model:

```bash
python day-14/src/train_yolo.py
```

Evaluate the model and generate predictions:

```bash
python day-14/src/evaluate_yolo.py
```

## Output Files

- `best.pt`: Best fine-tuned YOLOv8n model.
- `last.pt`: Final training checkpoint.
- `evaluation_metrics.csv`: Validation performance metrics.
- `prediction_results.csv`: Detected classes, confidence scores, and bounding box coordinates.
- `outputs/predictions/`: Annotated prediction images.
- `reports/validation/`: Validation results and plots.

## Conclusion

Successfully fine-tuned a pretrained YOLOv8n object detection model using the COCO128 dataset. Evaluated its performance using precision, recall, mAP@50, and mAP@50–95. Generated object detection predictions on two test images and saved the results for further analysis.

**Day 14 completed successfully.**
