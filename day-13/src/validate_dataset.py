from pathlib import Path
from collections import Counter
from PIL import Image
import csv

BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_DIR = BASE_DIR / "dataset" / "coco128"
IMAGE_DIR = DATASET_DIR / "images" / "train2017"
LABEL_DIR = DATASET_DIR / "labels" / "train2017"

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NUM_CLASSES = 80

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

issues = []
class_counts = Counter()
total_objects = 0

def add_issue(file_name, problem):
    issues.append({
        "file": file_name,
        "problem": problem
    })

# Check directories
if not IMAGE_DIR.exists() or not LABEL_DIR.exists():
    raise FileNotFoundError("Dataset image or label directory is missing.")

# Collect images and labels
images = {
    file.stem: file
    for file in IMAGE_DIR.iterdir()
    if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
}

labels = {
    file.stem: file
    for file in LABEL_DIR.glob("*.txt")
    if file.name.lower() != "readme.txt"
}

# Check missing and orphan files
missing_labels = sorted(images.keys() - labels.keys())
orphan_labels = sorted(labels.keys() - images.keys())

for name in missing_labels:
    add_issue(images[name].name, "Missing annotation file")

for name in orphan_labels:
    add_issue(labels[name].name, "Annotation has no matching image")

# Validate images
valid_images = 0

for name, image_path in images.items():
    try:
        with Image.open(image_path) as image:
            image.verify()
        valid_images += 1
    except Exception as error:
        add_issue(image_path.name, f"Invalid or corrupted image: {error}")

# Validate annotations
matched_pairs = 0
empty_labels = 0

for name in sorted(images.keys() & labels.keys()):
    matched_pairs += 1
    label_path = labels[name]

    lines = label_path.read_text(encoding="utf-8").splitlines()

    if not any(line.strip() for line in lines):
        empty_labels += 1
        add_issue(label_path.name, "Empty annotation file")
        continue

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        parts = line.split()

        if len(parts) != 5:
            add_issue(
                label_path.name,
                f"Line {line_number}: expected 5 values"
            )
            continue

        try:
            class_id = int(parts[0])
            x, y, width, height = map(float, parts[1:])
        except ValueError:
            add_issue(
                label_path.name,
                f"Line {line_number}: non-numeric value"
            )
            continue

        if not 0 <= class_id < NUM_CLASSES:
            add_issue(
                label_path.name,
                f"Line {line_number}: invalid class ID {class_id}"
            )
            continue

        if not all(
            0 <= value <= 1
            for value in (x, y, width, height)
        ):
            add_issue(
                label_path.name,
                f"Line {line_number}: coordinates outside [0, 1]"
            )
            continue

        if width <= 0 or height <= 0:
            add_issue(
                label_path.name,
                f"Line {line_number}: zero or negative bounding box size"
            )
            continue
        TOLERANCE = 1e-6
        if (
            x - width / 2 < -TOLERANCE 
            or x + width / 2 > 1 + TOLERANCE
            or y - height / 2 < -TOLERANCE
            or y + height / 2 > 1 + TOLERANCE
        ):
            add_issue(
                label_path.name,
                f"Line {line_number}: bounding box exceeds image bounds"
            )
            continue

        class_counts[class_id] += 1
        total_objects += 1

# Save split summary
summary = [{
    "split": "train2017",
    "total_images": len(images),
    "valid_images": valid_images,
    "total_labels": len(labels),
    "matched_pairs": matched_pairs,
    "missing_labels": len(missing_labels),
    "orphan_labels": len(orphan_labels),
    "total_objects": total_objects,
    "empty_labels": empty_labels
}]

with open(OUTPUT_DIR / "split_summary.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=summary[0].keys())
    writer.writeheader()
    writer.writerows(summary)

# Save validation issues
with open(OUTPUT_DIR / "validation_issues.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["file", "problem"]
    )
    writer.writeheader()
    writer.writerows(issues)

# Save class distribution
with open(OUTPUT_DIR / "class_distribution.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["class_id", "object_count"])

    for class_id, count in sorted(class_counts.items()):
        writer.writerow([class_id, count])

# Print final report
print("\n" + "=" * 45)
print("       DATASET QUALITY REPORT")
print("=" * 45)

print(f"Total images       : {len(images)}")
print(f"Valid images       : {valid_images}")
print(f"Total labels       : {len(labels)}")
print(f"Matched pairs      : {matched_pairs}")
print(f"Missing labels     : {len(missing_labels)}")
print(f"Orphan labels      : {len(orphan_labels)}")
print(f"Empty labels       : {empty_labels}")
print(f"Annotated objects  : {total_objects}")
print(f"Unique classes     : {len(class_counts)}")
print(f"Validation issues  : {len(issues)}")

print("\nReports saved in:", OUTPUT_DIR)
print("=" * 45)
