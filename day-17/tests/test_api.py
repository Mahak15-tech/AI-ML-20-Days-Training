
from pathlib import Path
import importlib.util

from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[2]

API_FILE = ROOT_DIR / "day-16" / "src" / "main.py"
TEST_IMAGE = (
    ROOT_DIR
    / "day-14"
    / "dataset"
    / "coco128"
    / "images"
    / "train"
    / "000000000009.jpg"
)

spec = importlib.util.spec_from_file_location("day16_api", API_FILE)
api_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_module)

client = TestClient(api_module.app)


def test_valid_image_prediction():
    assert TEST_IMAGE.exists(), f"Test image not found: {TEST_IMAGE}"

    with open(TEST_IMAGE, "rb") as image:
        response = client.post(
            "/predict",
            files={"file": ("test.jpg", image, "image/jpeg")},
        )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["detections"], list)
    assert data["image_width"] > 0
    assert data["image_height"] > 0
    assert data["objects_detected"] == len(data["detections"])


def test_prediction_response_schema():
    with open(TEST_IMAGE, "rb") as image:
        response = client.post(
            "/predict",
            files={"file": ("test.jpg", image, "image/jpeg")},
        )

    data = response.json()

    required_fields = [
        "success",
        "filename",
        "image_width",
        "image_height",
        "confidence_threshold",
        "inference_time_ms",
        "objects_detected",
        "detections",
        "annotated_image_url",
    ]

    for field in required_fields:
        assert field in data

    for detection in data["detections"]:
        assert "class_id" in detection
        assert "class_name" in detection
        assert "confidence" in detection
        assert "bounding_box" in detection


def test_invalid_file():
    response = client.post(
        "/predict",
        files={"file": ("test.txt", b"not an image", "text/plain")},
    )

    assert response.status_code in [400, 415, 422]


def test_empty_result_at_max_confidence():
    with open(TEST_IMAGE, "rb") as image:
        response = client.post(
            "/predict?conf=1.0",
            files={"file": ("test.jpg", image, "image/jpeg")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["objects_detected"] == 0
    assert data["detections"] == []
