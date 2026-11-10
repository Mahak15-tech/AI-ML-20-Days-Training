from pathlib import Path
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

DATA_YAML = BASE_DIR / "dataset.yaml"
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

THRESHOLDS = [0.10, 0.25, 0.50, 0.75]

print("=" * 55)
print("DAY 15: CONFIDENCE THRESHOLD COMPARISON")
print("=" * 55)

model = YOLO(str(MODEL_PATH))
rows = []

for threshold in THRESHOLDS:
    print(f"\nEvaluating confidence threshold: {threshold}")

    metrics = model.val(
        data=str(DATA_YAML),
        split="val",
        imgsz=640,
        batch=8,
        conf=threshold,
        plots=False,
        verbose=False
    )

    rows.append({
        "confidence_threshold": threshold,
        "precision": float(metrics.box.mp),
        "recall": float(metrics.box.mr),
        "mAP50": float(metrics.box.map50),
        "mAP50_95": float(metrics.box.map)
    })

df = pd.DataFrame(rows)

output_file = REPORT_DIR / "threshold_comparison.csv"
df.to_csv(output_file, index=False)

print("\nTHRESHOLD COMPARISON")
print("-" * 75)
print(df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

print("\nReport saved:", output_file)
print("\nThreshold comparison completed!")
