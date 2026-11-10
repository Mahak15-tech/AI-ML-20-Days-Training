from pathlib import Path
import cv2
import pandas as pd
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    BASE_DIR.parent
    / "day-14"
    / "outputs"
    / "yolov8n_finetuned"
    / "weights"
    / "best.pt"
)

DATASET_DIR = (
    BASE_DIR.parent
    / "day-14"
    / "dataset"
    / "coco128"
)

IMAGE_DIR = DATASET_DIR / "images" / "val"
LABEL_DIR = DATASET_DIR / "labels" / "val"

REPORT_DIR = BASE_DIR / "reports"
OUTPUT_DIR = BASE_DIR / "outputs" / "error_examples"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CONFIDENCE = 0.25
IOU_THRESHOLD = 0.50

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}

def calculate_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)

    area1 = max(0, box1[2] - box1[0]) * max(0, box1[3] - box1[1])
    area2 = max(0, box2[2] - box2[0]) * max(0, box2[3] - box2[1])

    union = area1 + area2 - intersection

    return intersection / union if union > 0 else 0.0


def load_ground_truth(label_path, width, height):
    ground_truth = []

    if not label_path.exists():
        return ground_truth

    for line in label_path.read_text().splitlines():
        parts = line.split()

        if len(parts) != 5:
            continue

        class_id = int(float(parts[0]))
        x_center, y_center, box_width, box_height = map(float, parts[1:])

        x1 = (x_center - box_width / 2) * width
        y1 = (y_center - box_height / 2) * height
        x2 = (x_center + box_width / 2) * width
        y2 = (y_center + box_height / 2) * height

        ground_truth.append({
            "class_id": class_id,
            "box": [x1, y1, x2, y2]
        })

    return ground_truth


print("=" * 60)
print("DAY 15: DETECTION ERROR ANALYSIS")
print("=" * 60)

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

if not IMAGE_DIR.exists():
    raise FileNotFoundError(f"Validation images not found: {IMAGE_DIR}")

if not LABEL_DIR.exists():
    raise FileNotFoundError(f"Validation labels not found: {LABEL_DIR}")

model = YOLO(str(MODEL_PATH))

image_paths = sorted(
    p for p in IMAGE_DIR.iterdir()
    if p.suffix.lower() in IMAGE_EXTENSIONS
)

if not image_paths:
    raise RuntimeError("No validation images found.")

all_errors = []
false_positives = 0
false_negatives = 0

for image_path in image_paths:
    image = cv2.imread(str(image_path))

    if image is None:
        print(f"Skipping unreadable image: {image_path.name}")
        continue

    height, width = image.shape[:2]

    label_path = LABEL_DIR / f"{image_path.stem}.txt"

    ground_truth = load_ground_truth(label_path, width, height)

    result = model.predict(
        source=str(image_path),
        conf=CONFIDENCE,
        iou=0.7,
        verbose=False
    )[0]

    predictions = []

    if result.boxes is not None:
        for box in result.boxes:
            predictions.append({
                "class_id": int(box.cls.item()),
                "confidence": float(box.conf.item()),
                "box": box.xyxy[0].cpu().tolist()
            })

    matched_predictions = set()
    image_errors = []

    # Match each actual object with the best available prediction.
    for gt in ground_truth:
        best_index = None
        best_iou = 0.0

        for index, pred in enumerate(predictions):
            if index in matched_predictions:
                continue

            if pred["class_id"] != gt["class_id"]:
                continue

            overlap = calculate_iou(gt["box"], pred["box"])

            if overlap > best_iou:
                best_iou = overlap
                best_index = index

        if best_index is not None and best_iou >= IOU_THRESHOLD:
            matched_predictions.add(best_index)
        else:
            class_name = model.names[gt["class_id"]]

            error_type = (
                "Poor localization"
                if best_iou > 0
                else "False negative"
            )

            if error_type == "False negative":
                false_negatives += 1

            image_errors.append({
                "image": image_path.name,
                "error_type": error_type,
                "class_id": gt["class_id"],
                "class_name": class_name,
                "confidence": "",
                "IoU": round(best_iou, 4),
                "x1": round(gt["box"][0], 2),
                "y1": round(gt["box"][1], 2),
                "x2": round(gt["box"][2], 2),
                "y2": round(gt["box"][3], 2)
            })

    # Any prediction not matched to a ground-truth object is a false positive.
    for index, pred in enumerate(predictions):
        if index in matched_predictions:
            continue

        false_positives += 1

        image_errors.append({
            "image": image_path.name,
            "error_type": "False positive",
            "class_id": pred["class_id"],
            "class_name": model.names[pred["class_id"]],
            "confidence": round(pred["confidence"], 4),
            "IoU": "",
            "x1": round(pred["box"][0], 2),
            "y1": round(pred["box"][1], 2),
            "x2": round(pred["box"][2], 2),
            "y2": round(pred["box"][3], 2)
        })

    if image_errors:
        all_errors.extend(image_errors)

        # Draw ground-truth boxes in green.
        for gt in ground_truth:
            x1, y1, x2, y2 = map(int, gt["box"])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Draw predictions in red.
        for pred in predictions:
            x1, y1, x2, y2 = map(int, pred["box"])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        output_path = OUTPUT_DIR / f"{image_path.stem}_errors.jpg"
        cv2.imwrite(str(output_path), image)

        print(f"Errors found: {image_path.name} ({len(image_errors)})")


columns = [
    "image", "error_type", "class_id", "class_name",
    "confidence", "IoU", "x1", "y1", "x2", "y2"
]

df = pd.DataFrame(all_errors, columns=columns)

report_path = REPORT_DIR / "detection_error_examples.csv"
df.to_csv(report_path, index=False)

print("\n" + "=" * 60)
print("ERROR ANALYSIS SUMMARY")
print("=" * 60)

print("Validation images processed:", len(image_paths))
print("False positives:", false_positives)
print("False negatives:", false_negatives)
print("Total error examples:", len(df))

if not df.empty:
    print("\nERROR TYPE DISTRIBUTION")
    print(df["error_type"].value_counts().to_string())

    print("\nCLASS-WISE ERROR COUNTS")
    print(df["class_name"].value_counts().head(10).to_string())

print("\nCSV report saved:", report_path)
print("Annotated error images saved:", OUTPUT_DIR)

if len(df) >= 10:
    print("\nRequirement achieved: At least 10 error examples identified.")
else:
    print("\nFewer than 10 errors were found. Do not invent additional examples.")

print("\nDetection error analysis completed!")
