
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

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 1. Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 2. Edge detection
edges = cv2.Canny(blurred, 100, 200)

# 3. Binary thresholding
_, threshold = cv2.threshold(
    blurred, 127, 255, cv2.THRESH_BINARY
)

# 4. Contour detection
contours, _ = cv2.findContours(
    threshold.copy(),
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

contour_image = image.copy()
cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

# Save results
cv2.imwrite(str(OUTPUT_DIR / "blurred.jpg"), blurred)
cv2.imwrite(str(OUTPUT_DIR / "edges.jpg"), edges)
cv2.imwrite(str(OUTPUT_DIR / "threshold.jpg"), threshold)
cv2.imwrite(str(OUTPUT_DIR / "contours.jpg"), contour_image)

# Display results
fig, axes = plt.subplots(2, 3, figsize=(14, 8))

images = [
    (cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "Original"),
    (blurred, "Gaussian Blur"),
    (edges, "Canny Edges"),
    (threshold, "Binary Threshold"),
    (cv2.cvtColor(contour_image, cv2.COLOR_BGR2RGB), "Contours"),
]

for ax, (img, title) in zip(axes.flat, images):
    ax.imshow(img, cmap="gray" if img.ndim == 2 else None)
    ax.set_title(title)
    ax.axis("off")

axes.flat[5].axis("off")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "transformations.png", dpi=150)
plt.show()

print("Contours detected:", len(contours))
print("All transformations completed successfully!")
