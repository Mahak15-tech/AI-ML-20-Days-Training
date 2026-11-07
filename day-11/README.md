# Day 11 – Image Processing, Transformations and Augmentation

## Overview
Explored fundamental image-processing operations using Python and OpenCV. The implementation includes image analysis, transformations, edge and contour detection, and image augmentation.

## Objectives
- Load and inspect an image.
- Understand image dimensions and color channels.
- Convert images to grayscale.
- Apply resizing, rotation, and flipping.
- Explore brightness and blur operations.
- Perform edge detection, thresholding, and contour detection.
- Generate image augmentation examples.

## Technologies
- Python 3.10
- OpenCV
- NumPy
- Matplotlib (if included in the installed requirements)

## Project Structure
```text
day-11/
├── images/
│   └── input.jpg
├── outputs/
│   ├── augmentation.png
│   ├── blurred.jpg
│   ├── bright.jpg
│   ├── contours.jpg
│   ├── dark.jpg
│   ├── edges.jpg
│   ├── flipped.jpg
│   ├── grayscale.jpg
│   ├── image_analysis.png
│   ├── resized.jpg
│   ├── rotated.jpg
│   ├── threshold.jpg
│   └── transformations.png
└── src/
    ├── image_augmentation.py
    ├── image_fundamentals.py
    └── image_transformations.py
```

## Implementation

### Image Fundamentals
- Loaded and inspected the input image.
- Examined image dimensions, channels, and pixel representation.
- Converted the image to grayscale.
- Applied thresholding and edge detection.
- Detected contours.

### Image Transformations
- Resized the image.
- Rotated and flipped the image.
- Adjusted brightness.
- Applied blur.

### Image Augmentation
Generated augmented image examples and visual summaries to understand how image variations can be used in computer vision workflows.

## Run the Project
The folder listing does not currently show a `requirements.txt` file. Install the required packages if they are not already available:

```bash
pip install opencv-python numpy matplotlib
```

Run each script from the `day-11` directory:

```bash
python src/image_fundamentals.py
python src/image_transformations.py
python src/image_augmentation.py
```

## Recorded Results
- Input image dimensions: 800 × 500 pixels.
- Image representation: RGB.
- Data type: `uint8`.
- Contours detected: 314.

## Outputs
Generated images and visual summaries are saved in `outputs/`.

## Key Learnings
- Understanding image dimensions, channels, and pixel data.
- Applying basic image transformations.
- Converting images to grayscale.
- Using thresholding and edge detection.
- Detecting contours with OpenCV.
- Creating image augmentation examples.

## Conclusion
Successfully explored image fundamentals, transformations, contour detection, and augmentation using OpenCV.

**Status: Completed**
