
from pathlib import Path
from io import BytesIO
from time import perf_counter
from uuid import uuid4

import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO


# --------------------------------------------------
# PROJECT PATHS
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
# LOAD YOLO MODEL
# --------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

print("Loading fine-tuned YOLOv8n model...")

model = YOLO(str(MODEL_PATH))

print("YOLO model loaded successfully!")


# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="YOLOv8 Object Detection API",
    description=(
        "Object detection API powered by a fine-tuned YOLOv8n model."
    ),
    version="1.0.0"
)

app.mount(
    "/outputs",
    StaticFiles(directory=str(OUTPUT_DIR)),
    name="outputs"
)


# --------------------------------------------------
# ROOT ENDPOINT
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "YOLOv8 Object Detection API is running!",
        "model": "Fine-tuned YOLOv8n",
        "documentation": "/docs",
        "prediction_endpoint": "/predict"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": True,
        "model_name": "YOLOv8n"
    }


# --------------------------------------------------
# OBJECT DETECTION ENDPOINT
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

    # Save annotated prediction image
    annotated_image = result.plot()

    output_filename = f"detection_{uuid4().hex[:10]}.jpg"
    output_path = OUTPUT_DIR / output_filename

    cv2.imwrite(str(output_path), annotated_image)

    return {
        "success": True,
        "filename": file.filename,
        "image_width": image.width,
        "image_height": image.height,
        "confidence_threshold": conf,
        "inference_time_ms": round(inference_time, 2),
        "objects_detected": len(detections),
        "detections": detections,
        "annotated_image_url": f"/outputs/{output_filename}"
    }
