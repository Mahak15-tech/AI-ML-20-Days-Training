from pathlib import Path
import csv
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "outputs" / "class_distribution.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(INPUT_FILE, "r", newline="") as file:
    rows = list(csv.DictReader(file))

rows.sort(key=lambda item: int(item["object_count"]), reverse=True)

class_ids = [row["class_id"] for row in rows]
counts = [int(row["object_count"]) for row in rows]

total_objects = sum(counts)
total_classes = len(rows)

# Plot class distribution
plt.figure(figsize=(16, 7))
plt.bar(class_ids, counts)
plt.title("COCO128 Dataset - Class Distribution")
plt.xlabel("Class ID")
plt.ylabel("Number of Annotated Objects")
plt.xticks(rotation=90)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

chart_path = OUTPUT_DIR / "class_distribution.png"
plt.savefig(chart_path, dpi=300)
plt.close()

# Generate summary
summary_path = OUTPUT_DIR / "class_imbalance_summary.txt"

with open(summary_path, "w") as file:
    file.write("CLASS DISTRIBUTION ANALYSIS\n")
    file.write("=" * 40 + "\n")
    file.write(f"Total annotated objects: {total_objects}\n")
    file.write(f"Unique classes: {total_classes}\n\n")

    file.write("TOP 10 CLASSES\n")
    file.write("-" * 40 + "\n")

    for row in rows[:10]:
        class_id = row["class_id"]
        count = int(row["object_count"])
        percentage = count / total_objects * 100

        file.write(
            f"Class {class_id}: {count} objects "
            f"({percentage:.2f}%)\n"
        )

    file.write("\nLEAST FREQUENT CLASSES\n")
    file.write("-" * 40 + "\n")

    for row in sorted(rows, key=lambda item: int(item["object_count"]))[:10]:
        file.write(
            f"Class {row['class_id']}: {row['object_count']} objects\n"
        )

print("Class distribution analysis completed!")
print(f"Total objects: {total_objects}")
print(f"Unique classes: {total_classes}")
print(f"Chart saved: {chart_path}")
print(f"Summary saved: {summary_path}")
