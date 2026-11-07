# Day 12 – YOLOv8 Object Detection

## Overview
Implemented object detection using the pretrained YOLOv8n model. The inference script processes input images, detects objects, assigns class labels and confidence scores, and saves annotated images and structured reports.

## Objectives
- Load a pretrained YOLO model.
- Run object detection on multiple images.
- Identify detected object classes.
- Read confidence scores for detections.
- Generate annotated images with bounding boxes.
- Export detection details to CSV and text reports.

## Technologies
- Python 3.10
- Ultralytics YOLO
- OpenCV
- Pandas

## Project Structure
```text
day-12/
├── images/
│   ├── input.png
│   └── test_image.png
├── models/
│   └── yolov8n.pt
├── outputs/
│   ├── annotated_images/
│   │   ├── input_detected.jpg
│   │   └── test_image_detected.jpg
│   ├── detections.csv
│   └── detection_summary.txt
├── src/
│   └── yolo_inference.py
├── requirements.txt
└── README.md
```

## Implementation
1. Loaded the pretrained `yolov8n.pt` model.
2. Read the two input images.
3. Ran YOLO inference on each image.
4. Extracted object class names and confidence scores.
5. Saved annotated images with detection boxes and labels.
6. Exported detection records to CSV.
7. Generated a text summary of the inference run.

## Run the Project
From the `day-12` directory:

```bash
pip install -r requirements.txt
python src/yolo_inference.py
```

The script expects the model and input images at the paths configured in the source code.

## Results

| Metric | Result |
|---|---:|
| Images processed | 2 |
| Detections in first image | 8 |
| Detections in second image | 16 |
| Total detections | 24 |
| Annotated images generated | 2 |

### Detected Object Categories
Person, bicycle, bus, car, dog, handbag, and traffic light.

## Output Files
- `outputs/annotated_images/input_detected.jpg`
- `outputs/annotated_images/test_image_detected.jpg`
- `outputs/detections.csv`
- `outputs/detection_summary.txt`

## Key Learnings
- Loading and using a pretrained YOLO model.
- Performing object-detection inference.
- Understanding class labels and confidence scores.
- Interpreting bounding boxes in annotated images.
- Processing multiple images in one workflow.
- Exporting detection results for further analysis.

## Conclusion
Successfully ran YOLOv8n object detection on two images, detected 24 objects in total, and generated annotated images with CSV and text reports.

**Status: Completed**
