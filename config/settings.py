from datetime import datetime
from pathlib import Path

# =========================
# DATE RANGE
# =========================
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)

# =========================
# PATH
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)