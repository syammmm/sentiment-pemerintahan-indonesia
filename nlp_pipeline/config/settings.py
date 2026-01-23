from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# =========================
# DATE RANGE
# =========================
START_DATE = date(2025, 12, 1) # Edit as needed
END_DATE = date(2025, 12, 31) # Edit as needed
DATE_TEXT = (
    f"{START_DATE.year}_"
    f"{START_DATE.strftime('%B')}_"
    f"{START_DATE.day}_-_"
    f"{END_DATE.day}"
)

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