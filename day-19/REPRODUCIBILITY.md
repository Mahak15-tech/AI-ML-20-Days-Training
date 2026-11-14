# Reproducibility Guide

## 1. Project Overview

This guide describes the environment, dataset preparation, training configuration, and model artifact used in the YOLOv8n fine-tuning project.

The objective is to make the experiment easier to inspect and reproduce.

## 2. Project Environment

| Component | Configuration |
|---|---|
| Operating system | Windows |
| Python version used during training | 3.10.11 |
| Deep learning framework | PyTorch |
| Object detection framework | Ultralytics YOLO |
| Model architecture | YOLOv8n |
| Training device | CPU |
| Image size | 640 × 640 |
| Batch size | 8 |
| Random seed | 42 |

The exact installed package versions used for Day 14 training were not recorded in the available project documentation.

## 3. Dataset

Dataset: COCO128

| Split | Images |
|---|---:|
| Training | 101 |
| Validation | 25 |
| Total matched pairs | 126 |

Dataset configuration:

`day-14/dataset/data.yaml`

The dataset must be available in the expected directory structure before training.

## 4. Initial Model

The Day 14 training process used pretrained YOLOv8n weights from Day 12.

Model path:

`day-14/models/yolov8n.pt`

## 5. Dependencies

Day 14 dependencies are listed in:

`day-14/requirements.txt`

They include:

- ultralytics
- pandas
- matplotlib
- PyYAML

Install them using:

```powershell
pip install -r .\day-14\requirements.txt
```

For exact environment reproduction, use a recorded package lock or `pip freeze` output from the original training environment. Such a lock file was not preserved in the current documentation.

## 6. Dataset Preparation

From the repository root, run:

```powershell
python .\day-14\src\prepare_dataset.py
```

This prepares the dataset structure and training/validation splits.

## 7. Model Training

Run:

```powershell
python .\day-14\src\train_yolo.py
```

Recorded training configuration:

| Parameter | Value |
|---|---:|
| Maximum epochs | 30 |
| Completed epochs | 12 |
| Best epoch | 2 |
| Image size | 640 |
| Batch size | 8 |
| Patience | 10 |
| Seed | 42 |
| Device | CPU |
| Workers | 0 |

Training output:

`day-14/outputs/yolov8n_finetuned/`

Best checkpoint:

`day-14/outputs/yolov8n_finetuned/weights/best.pt`

## 8. Model Evaluation

Run:

```powershell
python .\day-14\src\evaluate_yolo.py
```

The recorded validation metrics were:

| Metric | Value |
|---|---:|
| Precision | 0.7366 |
| Recall | 0.6397 |
| mAP@50 | 0.7755 |
| mAP@50–95 | 0.5894 |

Results are documented in:

`day-14/reports/evaluation_metrics.csv`

## 9. Application Model Artifact

The Day 18 application uses the fine-tuned model at:

`day-18/backend/models/best.pt`

This is the application model artifact. It is distinct from the original pretrained weights and the Day 14 training checkpoint.

To verify the artifact's integrity, calculate its SHA-256 checksum:

```powershell
Get-FileHash .\day-18\backend\models\best.pt -Algorithm SHA256
```

Record the resulting hash alongside the model version when publishing a release.

## 10. API Testing