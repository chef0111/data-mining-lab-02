# Data Mining Practical Lab 02 - UIT

This project contains two market basket analysis exercises implemented in Python.

## What Runs Where

- [scripts/run_ex1.py](scripts/run_ex1.py) and [scripts/run_ex2.py](scripts/run_ex2.py) are thin wrappers.
- Core exercises logics live in:
  - [src/exercises/ex1.py](src/exercises/ex1.py)
  - [src/exercises/ex2.py](src/exercises/ex2.py)
- Shared helpers live in:
  - [src/io](src/io)
  - [src/mining](src/mining)

## Prerequisites

- Python 3.10+
- pip

## Local Setup

### 1) Open terminal in project root

### 2) Create and activate virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

## Run Exercises

### Exercise 1

```bash
python scripts/run_ex1.py
```

Outputs:
- [Exercise 1 output log](outputs/logs/ex1_output.txt)
- [Exercise 1 threshold effects plot](outputs/plots/ex1_q14_thresholds.png)

### Exercise 2

```bash
python scripts/run_ex2.py
```

Outputs:
- [Exercise 2 output log](outputs/logs/ex2_output.txt)
- [Exercise 2 support plot](outputs/plots/ex2_q15_support_plot.png)

## Lab Content Reference

Read the official lab handout at [Lab2.pdf](docs/Lab2.pdf).

## Notes

- Input datasets are expected at:
  - [data/raw/groceries.csv](data/raw/groceries.csv)
  - [data/raw/Online_Retail.xlsx](data/raw/Online_Retail.xlsx)
- To force log regeneration, clear the corresponding file in [outputs/logs](outputs/logs).
