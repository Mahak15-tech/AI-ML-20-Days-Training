
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

print("=" * 55)
print("DAY 15: PER-CLASS PERFORMANCE ANALYSIS")
print("=" * 55)

model = YOLO(str(MODEL_PATH))

print("\nEvaluating model...")

metrics = model.val(
    data=str(DATA_YAML),
    split="val",
    imgsz=640,
    batch=8,
    conf=0.001,
    plots=False,
    verbose=False
)

box = metrics.box

class_ids = box.ap_class_index
precisions = box.p
recalls = box.r
average_precisions = box.ap

rows = []

for i, class_id in enumerate(class_ids):
    class_id = int(class_id)

    rows.append({
        "class_id": class_id,
        "class_name": model.names[class_id],
        "precision": float(precisions[i]),
        "recall": float(recalls[i]),
        "mAP50": float(box.ap50[i]),
        "mAP50_95": float(average_precisions[i])
    })

df = pd.DataFrame(rows)

df = df.sort_values(
    by="mAP50",
    ascending=False
).reset_index(drop=True)

output_file = REPORT_DIR / "per_class_performance.csv"
df.to_csv(output_file, index=False)

print("\nPER-CLASS PERFORMANCE")
print("-" * 75)
print(df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

print("\nClasses evaluated:", len(df))
print("Report saved:", output_file)
print("\nPer-class analysis completed!")
