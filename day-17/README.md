
# Day 17: API Testing and Performance

## Objective
Test the YOLOv8 FastAPI application, validate API behavior, and measure prediction performance.

## Project Structure

```text
day-17/
├── src/
│   └── benchmark_api.py
├── tests/
│   └── test_api.py
├── outputs/
├── reports/
│   ├── performance_report.csv
│   └── performance_report.md
├── requirements.txt
└── README.md
```

## Testing

Automated tests were performed using Pytest and FastAPI TestClient.

| Test Case | Result |
|---|---|
| Valid image prediction | PASSED |
| Prediction response schema | PASSED |
| Invalid file handling | PASSED |
| Empty detection result | PASSED |

**Total: 4 passed, 0 failed.**

## Performance Benchmark

- Model: Fine-tuned YOLOv8n
- Dataset: COCO128
- Test image: `000000000009.jpg`
- Warm-up requests: 1
- Measured requests: 5

| Metric | Result |
|---|---:|
| Average API response | 161.41 ms |
| Minimum API response | 156.15 ms |
| Maximum API response | 167.18 ms |
| Average inference time | 92.60 ms |
| Detections per request | 5 |

## Error Handling

- Invalid file uploads are rejected.
- Empty detection results are returned successfully.
- Prediction responses are checked for the expected fields.

## Performance Notes

The benchmark was performed locally on CPU. Results represent warmed-up requests and do not include model cold-start time. Memory consumption was not directly measured.

## Files

- `tests/test_api.py`: Automated API tests.
- `src/benchmark_api.py`: Performance benchmark.
- `reports/performance_report.csv`: Benchmark metrics.
- `reports/performance_report.md`: Detailed performance analysis.

## Conclusion

The FastAPI application passed all four automated tests. Five measured prediction requests completed successfully, with an average API response time of 161.41 ms.

Day 17 successfully validates the API's core behavior and establishes a performance baseline for capstone integration.
