
import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_FILE = PROJECT_ROOT / "day-16" / "src" / "main.py"

spec = importlib.util.spec_from_file_location("day16_main", APP_FILE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

client = TestClient(module.app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"] is True


def test_predict_rejects_invalid_file():
    response = client.post(
        "/predict",
        files={"file": ("invalid.txt", b"not an image", "text/plain")}
    )
    assert response.status_code in (400, 415, 422)
