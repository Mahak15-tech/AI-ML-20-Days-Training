
from pathlib import Path
import cv2
import pandas as pd
from ultralytics import YOLO

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "models" / "yolov8n.pt"
IMAGE_DIR = BASE_DIR / "images"
OUTPUT_DIR = BASE_DIR / "outputs" / "annotated_images"

CSV_PATH = BASE_DIR / "outputs" / "detections.csv"
SUMMARY_PATH = BASE_DIR / "outputs" / "detection_summary.txt"

CONFIDENCE_THRESHOLD = 0.25

def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\nYOLO OBJECT DETECTION")
    print("-" * 40)

    # Load pretrained model
    model = YOLO(str(MODEL_PATH))

    print("Model loaded successfully!")

    # Find input images
    extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp"]

    image_paths = []

    for extension in extensions:
        image_paths.extend(IMAGE_DIR.glob(extension))

    if not image_paths:
        print("No images found in images folder.")
        return

    all_detections = []
    total_detections = 0
    summary_lines = []

    # Process each image
    for image_path in image_paths:

        print(f"\nProcessing: {image_path.name}")

        results = model.predict(
            source=str(image_path),
            conf=CONFIDENCE_THRESHOLD,
            verbose=False
        )

        result = results[0]
        boxes = result.boxes

        image_count = len(boxes)
        total_detections += image_count

        print(f"Objects detected: {image_count}")

        # Save annotated image
        annotated_image = result.plot()

        output_path = OUTPUT_DIR / f"{image_path.stem}_detected.jpg"

        cv2.imwrite(str(output_path), annotated_image)

        print(f"Saved: {output_path.name}")

        # Extract detection details
        for box in boxes:

            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            class_name = model.names[class_id]

            all_detections.append({
                "image": image_path.name,
                "class_id": class_id,
                "class_name": class_name,
                "confidence": round(confidence, 4),
                "x1": round(x1, 2),
                "y1": round(y1, 2),
                "x2": round(x2, 2),
                "y2": round(y2, 2)
            })

            print(
                f"  {class_name}: "
                f"{confidence:.2%}"
            )

        summary_lines.append(
            f"{image_path.name}: {image_count} detections"
        )

    # Export CSV
    columns = [
        "image", "class_id", "class_name",
        "confidence", "x1", "y1", "x2", "y2"
    ]

    dataframe = pd.DataFrame(
        all_detections,
        columns=columns
    )

    dataframe.to_csv(CSV_PATH, index=False)

    # Export summary
    summary_lines.extend([
        "",
        f"Images processed: {len(image_paths)}",
        f"Total detections: {total_detections}",
        f"Confidence threshold: {CONFIDENCE_THRESHOLD}"
    ])

    SUMMARY_PATH.write_text(
        "\n".join(summary_lines),
        encoding="utf-8"
    )

    print("\n" + "-" * 40)
    print("INFERENCE COMPLETED")
    print(f"Images processed: {len(image_paths)}")
    print(f"Total detections: {total_detections}")
    print(f"CSV report: {CSV_PATH}")
    print(f"Summary: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
