from pathlib import Path
import csv
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    BASE_DIR / "outputs" / "yolov8n_finetuned"
    / "weights" / "best.pt"
)

DATA_CONFIG = BASE_DIR / "outputs" / "data.yaml"

REPORT_DIR = BASE_DIR / "reports"
PREDICTION_DIR = BASE_DIR / "outputs" / "predictions"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
PREDICTION_DIR.mkdir(parents=True, exist_ok=True)

# Load fine-tuned model
model = YOLO(str(MODEL_PATH))

print("=" * 50)
print("FINE-TUNED YOLO MODEL EVALUATION")
print("=" * 50)

# Validate model
metrics = model.val(
    data=str(DATA_CONFIG),
    split="val",
    plots=True,
    project=str(REPORT_DIR),
    name="validation",
    exist_ok=True
)

precision = metrics.box.mp
recall = metrics.box.mr
map50 = metrics.box.map50
map5095 = metrics.box.map

# Export evaluation metrics
with open(
    REPORT_DIR / "evaluation_metrics.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:
    writer = csv.writer(file)
    writer.writerow(["Metric", "Value"])
    writer.writerow(["Precision", precision])
    writer.writerow(["Recall", recall])
    writer.writerow(["mAP50", map50])
    writer.writerow(["mAP50-95", map5095])

# Run predictions on Day 12 test images
IMAGE_DIR = BASE_DIR.parent / "day-12" / "images"

image_paths = [
    p for p in IMAGE_DIR.iterdir()
    if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
]

if not image_paths:
    raise FileNotFoundError("No test images found in Day 12 images folder.")

prediction_results = model.predict(
    source=[str(p) for p in image_paths],
    conf=0.25,
    save=True,
    project=str(BASE_DIR / "outputs"),
    name="predictions",
    exist_ok=True
)

# Export prediction details
with open(
    REPORT_DIR / "prediction_results.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:
    writer = csv.writer(file)

    writer.writerow([
        "Image",
        "Class ID",
        "Class Name",
        "Confidence",
        "X1", "Y1", "X2", "Y2"
    ])

    for result in prediction_results:
        if result.boxes is None:
            continue

        for box in result.boxes:
            class_id = int(box.cls.item())
            class_name = result.names[class_id]
            confidence = float(box.conf.item())
            coordinates = box.xyxy[0].tolist()

            writer.writerow([
                Path(result.path).name,
                class_id,
                class_name,
                round(confidence, 4),
                *[round(value, 2) for value in coordinates]
            ])

print("\nEVALUATION RESULTS")
print("-" * 40)
print(f"Precision:  {precision:.4f}")
print(f"Recall:     {recall:.4f}")
print(f"mAP50:      {map50:.4f}")
print(f"mAP50-95:   {map5095:.4f}")

print("\nEvaluation completed!")
print("Reports:", REPORT_DIR)
print("Predictions:", PREDICTION_DIR)
