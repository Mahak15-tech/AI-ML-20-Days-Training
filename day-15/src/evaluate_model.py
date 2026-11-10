from pathlib import Path
from ultralytics import YOLO
import pandas as pd

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
OUTPUT_DIR = BASE_DIR / "outputs"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 55)
print("DAY 15: DETECTION MODEL EVALUATION")
print("=" * 55)

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

if not DATA_YAML.exists():
    raise FileNotFoundError(f"Dataset configuration not found: {DATA_YAML}")

print("\nLoading fine-tuned YOLO model...")
model = YOLO(str(MODEL_PATH))

print("\nRunning validation...")
metrics = model.val(
    data=str(DATA_YAML),
    split="val",
    imgsz=640,
    batch=8,
    conf=0.001,
    plots=True,
    project=str(OUTPUT_DIR),
    name="model_evaluation",
    exist_ok=True
)

results = {
    "Metric": [
        "Precision",
        "Recall",
        "mAP50",
        "mAP50-95"
    ],
    "Score": [
        float(metrics.box.mp),
        float(metrics.box.mr),
        float(metrics.box.map50),
        float(metrics.box.map)
    ]
}

df = pd.DataFrame(results)
df.to_csv(REPORT_DIR / "evaluation_metrics.csv", index=False)

print("\nEVALUATION RESULTS")
print("-" * 40)

for metric, score in zip(results["Metric"], results["Score"]):
    print(f"{metric:<15}: {score:.4f}")

print("\nSaved report:")
print(REPORT_DIR / "evaluation_metrics.csv")

print("\nEvaluation plots saved in:")
print(OUTPUT_DIR / "model_evaluation")

print("\nDay 15 model evaluation completed!")
