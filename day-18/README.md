# Day 18: YOLO Object Detection Studio

A full-stack AI-powered object detection application built using **YOLOv8n, FastAPI, React, TypeScript, and Vite**. The application allows users to upload images, detect objects, visualize bounding boxes, adjust detection confidence, and download annotated results.

## Project Overview

YOLO Object Detection Studio provides an interactive interface for running real-time image inference using a fine-tuned YOLOv8n model.

### Key Features

- Image upload with preview.
- Fine-tuned YOLOv8n object detection.
- Bounding-box visualization with class labels and confidence scores.
- Adjustable confidence threshold.
- Detection count and object-wise statistics.
- Inference time measurement.
- Original and annotated image comparison.
- Download annotated detection images.
- Backend health monitoring.
- Responsive interface with light and dark themes.

## Tech Stack

| Component | Technology |
|---|---|
| Object Detection | YOLOv8n |
| Deep Learning | PyTorch |
| Backend | FastAPI |
| Frontend | React + TypeScript |
| Build Tool | Vite |
| Styling | CSS |
| API Communication | REST API |
| Server | Uvicorn |

## Project Structure

```text
day-18/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── index.css
│   │   └── styles.css
│   ├── dist/
│   ├── package.json
│   └── vite.config.ts
│
├── src/
│   └── main.py
│
├── outputs/
│   └── Annotated detection images
│
└── README.md
```

The fine-tuned model is loaded from:

```text
day-14/outputs/yolov8n_finetuned/weights/best.pt
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Mahak15-tech/AI-ML-20-Days-Training.git
cd AI-ML-20-Days-Training/day-18
```

### 2. Backend Setup

Install the required Python dependencies using the project's configured Python environment.

```bash
pip install fastapi uvicorn ultralytics python-multipart pillow
```

Start the FastAPI server:

```bash
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

Backend URL:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

The frontend uses the following default API URL:

```typescript
import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
```

## API Endpoints

### GET `/health`

Checks backend availability and model loading status.

Example response:

```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "YOLOv8n"
}
```

### POST `/predict`

Performs object detection on an uploaded image.

**Parameters:**
- `file`: Image file uploaded through multipart form data.
- `conf`: Confidence threshold (default: 0.25).

Example request:

```text
POST /predict?conf=0.25
```

Example response structure:

```json
{
  "success": true,
  "filename": "test.jpg",
  "image_width": 640,
  "image_height": 480,
  "confidence_threshold": 0.25,
  "inference_time_ms": 45.2,
  "objects_detected": 2,
  "detections": [],
  "annotated_image_url": "/outputs/detected_image.jpg"
}
```

*The values above are illustrative; actual results depend on the uploaded image and model inference.*

## Application Workflow

1. Launch the FastAPI backend.
2. Start the React frontend.
3. Upload an image through the detection workspace.
4. Adjust the confidence threshold if required.
5. Run object detection.
6. View detected objects and their bounding boxes.
7. Compare the original and annotated images.
8. Download the annotated image.

## Model Information

- **Model:** YOLOv8n
- **Model Type:** Fine-tuned object detection model
- **Model Source:** Day 14 training outputs
- **Model Weights:** `best.pt`

The application uses the trained weights rather than relying on a simulated detection response.

## Learning Outcomes

Through this project, I learned:

- Integrating a trained deep learning model into a web application.
- Building REST APIs using FastAPI.
- Connecting React frontend components with Python backend services.
- Handling image uploads and inference responses.
- Visualizing object detection results.
- Managing model outputs and downloadable files.
- Building a complete AI application workflow.

## Author

**Mahak Kamble**

GitHub: [Mahak15-tech](https://github.com/Mahak15-tech)

---
