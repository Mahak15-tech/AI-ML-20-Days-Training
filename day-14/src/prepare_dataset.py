
from pathlib import Path
import random
import shutil

BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = BASE_DIR.parent / "day-13" / "dataset" / "coco128"

DEST_DIR = BASE_DIR / "dataset" / "coco128"

IMAGE_SOURCE = SOURCE_DIR / "images" / "train2017"
LABEL_SOURCE = SOURCE_DIR / "labels" / "train2017"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
RANDOM_SEED = 42
VALIDATION_RATIO = 0.20

random.seed(RANDOM_SEED)

pairs = []

for image_path in IMAGE_SOURCE.iterdir():
    if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
        continue

    label_path = LABEL_SOURCE / f"{image_path.stem}.txt"

    if label_path.exists():
        pairs.append((image_path, label_path))

if len(pairs) < 2:
    raise RuntimeError("Not enough matching image-label pairs.")

random.shuffle(pairs)

validation_count = round(len(pairs) * VALIDATION_RATIO)

val_pairs = pairs[:validation_count]
train_pairs = pairs[validation_count:]

for split, split_pairs in [
    ("train", train_pairs),
    ("val", val_pairs)
]:
    image_dir = DEST_DIR / "images" / split
    label_dir = DEST_DIR / "labels" / split

    image_dir.mkdir(parents=True, exist_ok=True)
    label_dir.mkdir(parents=True, exist_ok=True)

    for image_path, label_path in split_pairs:
        shutil.copy2(image_path, image_dir / image_path.name)
        shutil.copy2(label_path, label_dir / label_path.name)

print("=" * 45)
print("YOLO DATASET PREPARATION")
print("=" * 45)
print(f"Matched pairs: {len(pairs)}")
print(f"Training images: {len(train_pairs)}")
print(f"Validation images: {len(val_pairs)}")
print("Random seed:", RANDOM_SEED)
print("Dataset preparation completed!")
