
from pathlib import Path
import cv2
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_PATH = BASE_DIR / "images" / "input.jpg"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

image = cv2.imread(str(IMAGE_PATH))

if image is None:
    raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

# Convert BGR to RGB for correct display
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 1. Horizontal flip
flipped = cv2.flip(image, 1)

# 2. Rotate by 30 degrees
height, width = image.shape[:2]
matrix = cv2.getRotationMatrix2D(
    (width // 2, height // 2), 30, 1.0
)
rotated = cv2.warpAffine(image, matrix, (width, height))

# 3. Increase brightness
bright = cv2.convertScaleAbs(image, alpha=1.0, beta=40)

# 4. Reduce brightness
dark = cv2.convertScaleAbs(image, alpha=1.0, beta=-40)

# Save augmented images
cv2.imwrite(
    str(OUTPUT_DIR / "flipped.jpg"),
    cv2.cvtColor(flipped, cv2.COLOR_RGB2BGR)
)
cv2.imwrite(
    str(OUTPUT_DIR / "rotated.jpg"),
    cv2.cvtColor(rotated, cv2.COLOR_RGB2BGR)
)
cv2.imwrite(
    str(OUTPUT_DIR / "bright.jpg"),
    cv2.cvtColor(bright, cv2.COLOR_RGB2BGR)
)
cv2.imwrite(
    str(OUTPUT_DIR / "dark.jpg"),
    cv2.cvtColor(dark, cv2.COLOR_RGB2BGR)
)

# Display comparison
images = [
    (image, "Original"),
    (flipped, "Horizontal Flip"),
    (rotated, "Rotation: 30 degrees"),
    (bright, "Increased Brightness"),
    (dark, "Reduced Brightness"),
]

fig, axes = plt.subplots(2, 3, figsize=(13, 8))

for ax, (img, title) in zip(axes.flat, images):
    ax.imshow(img)
    ax.set_title(title)
    ax.axis("off")

axes.flat[5].axis("off")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "augmentation.png", dpi=150)
plt.show()

print("Image augmentation completed successfully!")
print("Augmented images saved in:", OUTPUT_DIR)
