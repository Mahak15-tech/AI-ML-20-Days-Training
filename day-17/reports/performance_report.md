@'
# Day 17: API Testing and Performance Report

## 1. Objective
Test the YOLOv8 FastAPI application and measure its prediction performance.

## 2. Automated Testing

Test file: `tests/test_api.py`

| Test case | Result |
|---|---|
| Valid image prediction | PASSED |
| Prediction response schema | PASSED |
| Invalid file handling | PASSED |
| Empty detection result | PASSED |

**Total: 4 passed, 0 failed.**

## 3. Performance Benchmark

Benchmark script: `src/benchmark_api.py`

Test configuration:
- Model: Fine-tuned YOLOv8n
- Input: COCO128 image `000000000009.jpg`
- Warm-up requests: 1
- Measured requests: 5
- Successful requests: 5

### Results

| Metric | Result |
|---|---:|
| Average API response time | 161.41 ms |
| Minimum API response time | 156.15 ms |
| Maximum API response time | 167.18 ms |
| Average model inference time | 92.60 ms |
| Detections per request | 5 |

## 4. Performance Analysis

The API successfully processed all five measured requests.

Average model inference time was approximately 92.60 ms, while average total API response time was 161.41 ms.

The benchmark included one warm-up request before measurements. Therefore, these results represent warmed-up performance and do not measure cold-start time.

## 5. Error Handling

The API was tested with an invalid text file instead of an image. The request was rejected successfully.

The API also returned a valid response with an empty detection list when confidence was set to 1.0.

## 6. Limitations

- Benchmarking was performed on a local CPU environment.
- Results may differ on other hardware and deployment platforms.
- Only one sample image was used for the performance benchmark.
- Memory consumption was not directly measured.
- Cold-start latency was not included in the benchmark.

## 7. Conclusion

The YOLOv8 FastAPI application passed all four automated tests. Five consecutive benchmark requests completed successfully, with an average API response time of 161.41 ms.

The API is functioning correctly for the tested scenarios and is ready for further capstone integration.
'@ | Set-Content .\day-17\reports\performance_report.md