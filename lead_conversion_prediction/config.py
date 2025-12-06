from pathlib import Path
import yaml
import os
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

def load_config():
    config_path = PROJ_ROOT / "config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

CONFIG = load_config()

# Data Paths
DATA_CONFIG = CONFIG.get("data", {})
RAW_DATA_PATH = PROJ_ROOT / DATA_CONFIG.get("raw", "data/raw/raw_data.csv")
INTERIM_DATA_DIR = PROJ_ROOT / DATA_CONFIG.get("interim", "data/interim/")
PROCESSED_DATA_DIR = PROJ_ROOT / DATA_CONFIG.get("processed", "data/processed/")
TRAIN_DATA_PATH = PROJ_ROOT / DATA_CONFIG.get("train", "data/processed/train_data_gold.csv")
TEST_X_PATH = PROJ_ROOT / DATA_CONFIG.get("test", {}).get("X", "data/processed/X_test.csv")
TEST_Y_PATH = PROJ_ROOT / DATA_CONFIG.get("test", {}).get("y", "data/processed/y_test.csv")
EXTERNAL_DATA_DIR = PROJ_ROOT / DATA_CONFIG.get("external", "data/external/")

# Model Paths
MODELS_CONFIG = CONFIG.get("models", {})
MODELS_DIR = PROJ_ROOT / MODELS_CONFIG.get("dir", "models/")

# Reports Paths
REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass
