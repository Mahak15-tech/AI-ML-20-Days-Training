# AI/ML Intern Training — 20-Day Practical Roadmap

**Track:** Artificial Intelligence and Machine Learning  
**Duration:** 20 training days  
**Focus:** Python, data analysis, machine learning, computer vision, model evaluation, API development, and capstone delivery.

## About This Repository

This repository documents my hands-on journey through a structured 20-day AI/ML training program. Each day focuses on a practical learning objective, implementation task, and documented deliverable.

The program progresses from Python project development and tabular data analysis to machine learning pipelines, YOLO-based object detection, API development, testing, and a final integrated capstone.

## Learning Objectives

- Write maintainable Python code and organize reproducible projects.
- Clean, inspect, visualize, and validate datasets.
- Train and evaluate classification models using appropriate metrics.
- Identify data leakage, analyze errors, and understand model limitations.
- Run and fine-tune YOLO-based object detection models.
- Build a documented inference API using FastAPI.
- Test model behavior, evaluate robustness, and document responsible use.
- Present a complete capstone with reproducible results.

## 20-Day Curriculum

### Phase 1 — Python and Data Foundations

| Day | Topic | Practical Task | Expected Submission |
|---|---|---|---|
| 01 | Python Project Setup and Git | Create a repository with a CLI script that reads a CSV and reports its row count. | Repository, requirements file, README, meaningful Git commit |
| 02 | NumPy and Pandas Foundations | Load, inspect, filter, group, and summarize a tabular dataset. | Notebook or script and data-quality report |
| 03 | Exploratory Data Analysis (EDA) | Analyze distributions and class counts, create visualizations, and write five evidence-based observations. | EDA notebook with at least four useful plots |
| 04 | Statistics, Data Splits, and Leakage | Examine summary statistics, design data splits, and audit potential leakage. | Split-strategy note and leakage checklist |

### Phase 2 — Machine Learning

| Day | Topic | Practical Task | Expected Submission |
|---|---|---|---|
| 05 | First Baseline Model | Train a baseline classifier and record its performance before tuning. | Baseline script/notebook, saved metrics, mentor review |
| 06 | Preprocessing and Feature Engineering | Handle missing values, scale numerical features, encode categories, and build a pipeline. | Reusable preprocessing pipeline |
| 07 | Classification Models | Compare suitable algorithms using consistent data splits and evaluation metrics. | Model comparison table and model-selection rationale |
| 08 | Metrics and Imbalanced Data | Evaluate precision, recall, F1, confusion matrices, and relevant threshold choices. | Metrics report and threshold rationale |
| 09 | Error Analysis and Explainability | Inspect false positives, false negatives, group-level performance, and feature importance limitations. | Error-analysis table and two proposed improvements |
| 10 | Tabular ML Mini-Project Review | Integrate the data-to-metrics workflow into a reproducible project. | Mini-project demo, README, metrics, mentor review |

### Phase 3 — Computer Vision and Object Detection

| Day | Topic | Practical Task | Expected Submission |
|---|---|---|---|
| 11 | Computer Vision Foundations | Inspect image dimensions, channels, bounding boxes, and labels; review annotations visually. | Image inventory and annotation-quality notes |
| 12 | YOLO Inference and Outputs | Run a pretrained or approved YOLO model on sample images and inspect detections. | Inference script, sample outputs, observations |
| 13 | Dataset Quality and Annotation QA | Validate dataset paths, label formats, class IDs, split counts, and possible image leakage. | Dataset validation script and QA checklist |
| 14 | YOLO Fine-Tuning | Run a small, approved training experiment and track its configuration. | Training configuration, logs, best checkpoint |
| 15 | Detection Evaluation and Thresholding | Evaluate precision, recall, mAP, per-class results, and difficult detection cases. | Evaluation report and mentor review |

### Phase 4 — API, Testing, and Capstone

| Day | Topic | Practical Task | Expected Submission |
|---|---|---|---|
| 16 | Serve Inference with FastAPI | Create an API endpoint that accepts an approved image and returns detections as JSON. | Runnable API, example request, response schema |
| 17 | Testing and Performance | Test valid images, invalid files, empty results, response structure, and basic latency. | Automated tests and latency note |
| 18 | Capstone Integration | Integrate the dataset workflow, inference, evaluation, and API into a coherent application. | Integrated capstone branch |
| 19 | Robustness, Ethics, and Documentation | Document intended use, limitations, data provenance, privacy, bias, and failure modes. | Model card, README, reproducibility instructions |
| 20 | Final Demo and Technical Review | Demonstrate the capstone, walk through the code, explain failures and trade-offs, and propose a next experiment. | Demo, code, README, model card, individual reflection |

## Mentor Checkpoints

| Checkpoint | Review Focus |
|---|---|
| Day 5 | Fundamentals, repository structure, and ability to explain the implementation |
| Day 10 | Integrated tabular ML mini-project and corrective feedback |
| Day 15 | Advanced implementation, evaluation, tests, and edge cases |
| Day 20 | Live demonstration, code walkthrough, documentation, limitations, and reflection |

## Capstone Project

The final capstone will bring together the skills developed throughout the training. The training plan suggests an approved project such as hygiene-image detection or a public object-detection dataset.

### Required components

- Dataset quality assurance and validation
- Reproducible training and evaluation workflow
- Sample model inference and saved results
- An inference API
- Automated tests
- Model card covering intended use, metrics, limitations, and data provenance
- Clear setup and reproducibility instructions

A model running successfully does not, by itself, establish that it is production-ready.

## Assessment Criteria

| Assessment Area | Weight |
|---|---:|
| Problem framing and data quality | 20 points |
| Implementation and reproducibility | 25 points |
| Evaluation and error analysis | 25 points |
| API, tests, and robustness | 15 points |
| Communication and documentation | 15 points |
| **Total** | **100 points** |

## Tools and Technologies

- **Programming:** Python
- **Data analysis:** NumPy, Pandas, Matplotlib
- **Machine learning:** scikit-learn
- **Computer vision:** OpenCV, Ultralytics YOLO
- **API development:** FastAPI
- **Testing:** pytest
- **Development environment:** VS Code or Jupyter
- **Version control:** Git and GitHub

The recommended environment in the training plan is Python 3.11 or a mentor-approved version. Dependencies will be added as needed for individual tasks.

## Repository Structure

```text
ai-ml-20-day-training/
├── day-01/
│   ├── data/
│   ├── src/
│   ├── requirements.txt
│   └── README.md
├── day-02/
│   └── README.md
├── day-03/
│   └── README.md
├── ...
├── day-20/
│   └── README.md
├── capstone/
├── .gitignore
└── README.md
```

Each daily folder will contain its own implementation and documentation. The root README serves as the master roadmap for the entire program.

## Daily Working Practices

- Begin each day with a short implementation plan.
- Prefer hands-on coding over watching tutorials alone.
- Use official documentation as the primary reference.
- Commit work daily using meaningful Git commit messages.
- Record what worked, what failed, and what should happen next.
- Keep credentials, passwords, API keys, personal data, and sensitive datasets out of Git.
- Use approved datasets and avoid uploading confidential images to public tools.
- Document assumptions, limitations, and reproducibility steps.

## Progress Tracker

- [x] Day 01 — Python project setup and CSV row-counting CLI
- [ ] Day 02 — NumPy and Pandas
- [ ] Day 03 — Exploratory data analysis
- [ ] Day 04 — Statistics, splits, and leakage
- [ ] Day 05 — Baseline model and checkpoint
- [ ] Day 06 — Preprocessing and feature engineering
- [ ] Day 07 — Classification models
- [ ] Day 08 — Evaluation metrics and imbalanced data
- [ ] Day 09 — Error analysis and explainability
- [ ] Day 10 — Tabular ML mini-project
- [ ] Day 11 — Computer vision foundations
- [ ] Day 12 — YOLO inference
- [ ] Day 13 — Dataset quality assurance
- [ ] Day 14 — YOLO fine-tuning
- [ ] Day 15 — Detection evaluation and checkpoint
- [ ] Day 16 — FastAPI inference
- [ ] Day 17 — Testing and performance
- [ ] Day 18 — Capstone integration
- [ ] Day 19 — Robustness, ethics, and model card
- [ ] Day 20 — Final demo and technical review

## References

- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- [Pandas Getting Started](https://pandas.pydata.org/docs/getting_started/)
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/)
- [scikit-learn Documentation](https://scikit-learn.org/stable/)
- [OpenCV Tutorials](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html)
- [Ultralytics YOLO Documentation](https://docs.ultralytics.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [pytest Documentation](https://docs.pytest.org/en/stable/)
- [Google Model Cards](https://modelcards.withgoogle.com/about)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

---

**Program:** 20-Day AI/ML Intern Training  
**Repository:** `ai-ml-20-day-training`  
**Approach:** Learn, implement, evaluate, document, and demonstrate.
