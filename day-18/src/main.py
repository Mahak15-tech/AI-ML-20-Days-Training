from pathlib import Path
from io import BytesIO
from time import perf_counter
from uuid import uuid4
import os

import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = BASE_DIR.parent

MODEL_PATH = (
    ROOT_DIR
    / "day-14"
    / "outputs"
    / "yolov8n_finetuned"
    / "weights"
    / "best.pt"
)

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# MODEL
# --------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

print("Loading fine-tuned YOLOv8n model...")
model = YOLO(str(MODEL_PATH))
print("Model loaded successfully!")


# --------------------------------------------------
# APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="YOLOv8 Object Detection API",
    description="Integrated Day 18 capstone backend",
    version="1.0.0"
)

# Local development and deployed frontend origins
origins = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5173,"
    "http://127.0.0.1:5173,"
    "http://localhost:5174,"
    "http://127.0.0.1:5174"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in origins.split(",")
        if origin.strip()
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

app.mount(
    "/outputs",
    StaticFiles(directory=str(OUTPUT_DIR)),
    name="outputs"
)


# --------------------------------------------------
# HEALTH
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "YOLOv8 Capstone API is running",
        "model": "Fine-tuned YOLOv8n",
        "documentation": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": True,
        "model_name": "YOLOv8n"
    }


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    conf: float = Query(0.25, ge=0.0, le=1.0)
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image file."
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    try:
        image = Image.open(BytesIO(contents)).convert("RGB")
    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="Unable to decode the uploaded image."
        )

    image_array = np.array(image)

    start_time = perf_counter()

    results = model.predict(
        source=image_array,
        conf=conf,
        verbose=False
    )

    inference_time = (perf_counter() - start_time) * 1000

    result = results[0]
    detections = []

    if result.boxes is not None:
        for box in result.boxes:
            class_id = int(box.cls.item())
            confidence = float(box.conf.item())
            coordinates = box.xyxy[0].tolist()

            detections.append({
                "class_id": class_id,
                "class_name": model.names[class_id],
                "confidence": round(confidence, 4),
                "bounding_box": {
                    "x1": round(coordinates[0], 2),
                    "y1": round(coordinates[1], 2),
                    "x2": round(coordinates[2], 2),
                    "y2": round(coordinates[3], 2)
                }
            })

    annotated_image = result.plot()

    filename = f"detection_{uuid4().hex[:10]}.jpg"
    output_path = OUTPUT_DIR / filename

    if not cv2.imwrite(str(output_path), annotated_image):
        raise HTTPException(
            status_code=500,
            detail="Unable to save annotated image."
        )

    return {
        "success": True,
        "filename": file.filename,
        "image_width": image.width,
        "image_height": image.height,
        "confidence_threshold": conf,
        "inference_time_ms": round(inference_time, 2),
        "objects_detected": len(detections),
        "detections": detections,
        "annotated_image_url": f"/outputs/{filename}"
    }
