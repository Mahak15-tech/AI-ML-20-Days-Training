
from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_PATH = BASE_DIR / "images" / "input.jpg"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Load image
image = cv2.imread(str(IMAGE_PATH))

if image is None:
    raise FileNotFoundError(
        f"Image not found: {IMAGE_PATH}\n"
        "Place input.jpg inside the day-11/images folder."
    )

# 2. Image fundamentals
height, width, channels = image.shape

print("Image loaded successfully")
print("Height:", height)
print("Width:", width)
print("Channels:", channels)
print("Data type:", image.dtype)
print("Pixel range:", image.min(), "to", image.max())

# 3. Convert BGR to RGB
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 4. Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 5. Resize image
resized_image = cv2.resize(image, (256, 256))

# 6. Normalize pixel values to 0–1
normalized_image = rgb_image.astype(np.float32) / 255.0
print("Normalized range:",
      normalized_image.min(), "to", normalized_image.max())

# 7. Save processed images
cv2.imwrite(
    str(OUTPUT_DIR / "grayscale.jpg"),
    gray_image
)

cv2.imwrite(
    str(OUTPUT_DIR / "resized.jpg"),
    resized_image
)

# 8. Display results
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.imshow(rgb_image)
plt.title("Original RGB Image")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(gray_image, cmap="gray")
plt.title("Grayscale Image")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
plt.title("Resized: 256 × 256")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(rgb_image[:, :, 0], cmap="Reds")
plt.title("Red Channel")
plt.axis("off")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "image_analysis.png", dpi=150)
plt.show()

print("Processing complete!")
print("Check the day-11/outputs folder.")
