from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# =========================
# DATE RANGE
# =========================
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)

# =========================
# PATH
# =========================
#RAW DATA DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

#LABELLED DATA DIRECTORY
LABELLED_DATA_DIR = BASE_DIR / "data" / "labeled"

LABELLED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# TIMESTAMPS
# =========================
def create_timestamp():
    tz = ZoneInfo("Asia/Jakarta")
    now_jakarta = datetime.now(tz)
    now_jakarta.strftime("%Y-%m-%d %H:%M:%S")
    return now_jakarta