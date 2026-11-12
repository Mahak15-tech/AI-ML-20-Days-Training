
from pathlib import Path
import importlib.util
import statistics
import csv

from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[2]

API_FILE = ROOT_DIR / "day-16" / "src" / "main.py"
IMAGE_FILE = (
    ROOT_DIR
    / "day-14"
    / "dataset"
    / "coco128"
    / "images"
    / "train"
    / "000000000009.jpg"
)

OUTPUT_DIR = ROOT_DIR / "day-17" / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location("day16_api", API_FILE)
api_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_module)

client = TestClient(api_module.app)


def send_request():
    with open(IMAGE_FILE, "rb") as image:
        return client.post(
            "/predict",
            files={"file": ("benchmark.jpg", image, "image/jpeg")},
        )


if not IMAGE_FILE.exists():
    raise FileNotFoundError(f"Image not found: {IMAGE_FILE}")

print("=" * 55)
print("DAY 17 - API PERFORMANCE BENCHMARK")
print("=" * 55)

# Warm-up request; excluded from measurements
warmup = send_request()
if warmup.status_code != 200:
    raise RuntimeError(f"Warm-up failed: {warmup.text}")

response_times = []
inference_times = []
successful_requests = 0

# Run 5 measured requests
for run in range(1, 6):
    import time

    start = time.perf_counter()
    response = send_request()
    elapsed_ms = (time.perf_counter() - start) * 1000

    if response.status_code == 200:
        data = response.json()
        response_times.append(elapsed_ms)
        inference_times.append(data["inference_time_ms"])
        successful_requests += 1

        print(
            f"Run {run}: API = {elapsed_ms:.2f} ms | "
            f"Inference = {data['inference_time_ms']:.2f} ms | "
            f"Detections = {data['objects_detected']}"
        )
    else:
        print(f"Run {run} failed: {response.status_code} - {response.text}")

if not successful_requests:
    raise RuntimeError("All benchmark requests failed.")

results = {
    "successful_requests": successful_requests,
    "average_api_response_ms": statistics.mean(response_times),
    "minimum_api_response_ms": min(response_times),
    "maximum_api_response_ms": max(response_times),
    "average_model_inference_ms": statistics.mean(inference_times),
}

report_file = OUTPUT_DIR / "performance_report.csv"

with open(report_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Metric", "Value"])
    for metric, value in results.items():
        writer.writerow([metric, round(value, 2) if isinstance(value, float) else value])

print("\n" + "=" * 55)
print("PERFORMANCE SUMMARY")
print("=" * 55)

for metric, value in results.items():
    print(f"{metric}: {value:.2f}" if isinstance(value, float) else f"{metric}: {value}")

print(f"\nReport saved: {report_file}")
