from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_LOGS_DIR = PROJECT_ROOT / "outputs" / "logs"
OUTPUT_PLOTS_DIR = PROJECT_ROOT / "outputs" / "plots"
DOCS_LAB_DIR = PROJECT_ROOT / "docs"

GROCERIES_PATH = DATA_RAW_DIR / "groceries.csv"
RETAIL_PATH = DATA_RAW_DIR / "Online_Retail.xlsx"

EX1_OUTPUT_PATH = OUTPUT_LOGS_DIR / "ex1_output.txt"
EX2_OUTPUT_PATH = OUTPUT_LOGS_DIR / "ex2_output.txt"

EX1_PLOT_PATH = OUTPUT_PLOTS_DIR / "ex1_q14_thresholds.png"
EX2_PLOT_PATH = OUTPUT_PLOTS_DIR / "ex2_q15_support_plot.png"


def ensure_output_dirs() -> None:
    OUTPUT_LOGS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PLOTS_DIR.mkdir(parents=True, exist_ok=True)
