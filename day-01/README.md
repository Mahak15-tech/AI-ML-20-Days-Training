# Day 01 – Python Project Setup and CSV Row Counter

## Overview
Set up the Python project structure and created a simple program to read a CSV file and count its data rows. This day establishes the project organization and basic file-handling workflow used throughout the training.

## Objectives
- Set up a structured Python project.
- Understand basic CSV file handling.
- Read a CSV file using Python.
- Count the number of data rows in a CSV file.

## Technologies
- Python 3.10
- CSV module
- VS Code
- pip

## Project Structure
```text
day-01/
├── data/
│   └── sample.csv
├── src/
│   └── main.py
├── requirements.txt
└── README.md
```

## Implementation
The program reads `data/sample.csv`, processes its rows, and reports the number of data records. The sample dataset contains **5 data rows**.

## Run the Project
Open a terminal in the `day-01` directory and run:

```bash
python src/main.py
```

If the project has dependencies listed, install them first:

```bash
pip install -r requirements.txt
```

## Output
- Input file: `data/sample.csv`
- Result: **5 data rows**

## Key Learnings
- Organizing a Python project into data and source-code folders.
- Reading CSV files.
- Counting records while handling a header row.
- Running Python scripts from the terminal.

## Conclusion
Successfully configured the first training-day project and implemented a CSV row counter.

**Status: Completed**
