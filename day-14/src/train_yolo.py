
from pathlib import Path
import yaml
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "models" / "yolov8n.pt"
DATASET_DIR = BASE_DIR / "dataset" / "coco128"
SOURCE_CONFIG = BASE_DIR / "dataset" / "data.yaml"

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Check required files and folders
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

if not SOURCE_CONFIG.exists():
    raise FileNotFoundError(f"Dataset config not found: {SOURCE_CONFIG}")

for split in ["train", "val"]:
    image_dir = DATASET_DIR / "images" / split
    label_dir = DATASET_DIR / "labels" / split

    if not image_dir.exists() or not label_dir.exists():
        raise FileNotFoundError(f"Missing {split} dataset folders")

# Load dataset configuration
with open(SOURCE_CONFIG, "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

# Correct the dataset path
data["path"] = str(DATASET_DIR.resolve())

# Save a resolved YAML file for Ultralytics
RESOLVED_CONFIG = OUTPUT_DIR / "data.yaml"

with open(RESOLVED_CONFIG, "w", encoding="utf-8") as file:
    yaml.safe_dump(data, file, sort_keys=False)

print("=" * 50)
print("YOLO MODEL FINE-TUNING")
print("=" * 50)
print("Model:", MODEL_PATH)
print("Dataset:", DATASET_DIR)
print("Classes:", data["nc"])
print("Training images:", 101)
print("Validation images:", 25)

# Load pretrained YOLOv8n
model = YOLO(str(MODEL_PATH))

# Start fine-tuning
results = model.train(
    data=str(RESOLVED_CONFIG),
    epochs=30,
    imgsz=640,
    batch=8,
    patience=10,
    project=str(OUTPUT_DIR),
    name="yolov8n_finetuned",
    exist_ok=True,
    plots=True,
    save=True,
    seed=42,
    device="cpu",
    workers=0
)

print("\nTraining completed!")
print("Results:", OUTPUT_DIR / "yolov8n_finetuned")
print("Best model:", OUTPUT_DIR / "yolov8n_finetuned" / "weights" / "best.pt")
