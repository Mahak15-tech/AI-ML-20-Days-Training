# Day 16: Serve Inference with FastAPI

## Objective
Deploy the fine-tuned YOLOv8n object detection model through a REST API using FastAPI. Allow users to upload images and receive object detection results with confidence scores and bounding boxes.

## Technology Stack
- Python 3.10.11
- FastAPI
- Uvicorn
- Ultralytics YOLOv8n
- OpenCV
- Pillow
- Pytest
- HTTPX

## Project Structure

```text
day-16/
├── src/
│   └── main.py
├── tests/
│   └── test_api.py
├── outputs/
├── requirements.txt
└── README.md
```

## Model
The API uses the fine-tuned model from Day 14:

`day-14/outputs/yolov8n_finetuned/weights/best.pt`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Model health status |
| POST | `/predict` | Upload an image and detect objects |
| GET | `/outputs/{filename}` | View annotated output image |

Interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

## Run the API

From the repository root:

```powershell
python -m uvicorn day-16.src.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to test the endpoints.

## Inference Results

Test image: Sunny Blue Bus Stop Scene.png

- Image dimensions: 1448 × 1086
- Confidence threshold: 0.25
- Objects detected: 7
- Inference time: 6757.72 ms

### Detected Classes

| Class | Count |
|---|---:|
| Person | 5 |
| Bicycle | 1 |
| Bus | 1 |
| **Total** | **7** |

The API returned class IDs, class names, confidence scores, bounding box coordinates, inference time, and an annotated image URL.

## Automated Testing

Run:

```powershell
python -m pytest .\day-16\tests\test_api.py -v
```

Test results:

- Root endpoint: PASSED
- Health endpoint: PASSED
- Invalid file validation: PASSED

**Total: 3 passed, 0 failed**

## Key Learnings

1. Built a REST API using FastAPI.
2. Integrated a trained YOLOv8 model into an API.
3. Implemented image upload and validation.
4. Returned object detection results in JSON format.
5. Generated annotated images and served them through a static endpoint.
6. Used Uvicorn to run the API.
7. Tested API endpoints using Pytest and HTTPX.

## Conclusion

Successfully served the fine-tuned YOLOv8n model through a FastAPI application. The API accepts image uploads, performs object detection, returns structured prediction results, and provides annotated images. All three automated tests passed.