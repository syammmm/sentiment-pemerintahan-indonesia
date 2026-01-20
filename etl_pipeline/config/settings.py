import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from google.cloud import storage

# =========================
# ENVIRONMENT
# =========================
ENV = os.getenv("APP_ENV", "local")

# =========================
# BASE DIRECTORY
# =========================
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = Path(__file__).resolve().parents[2]

# =========================
# DATE RANGE
# =========================
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)

# =========================
# LOCAL vs CLOUD PATH MAPPING
# =========================
if ENV == "cloud":
    BASE_DATA_DIR = Path("/tmp")
else:
    BASE_DATA_DIR = BASE_DIR / "nlp_pipeline"


LABELLED_DATA_DIR = BASE_DATA_DIR / "data" / "labeled"

# Create directories
LABELLED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# TIMESTAMP
# =========================
def create_timestamp():
    tz = ZoneInfo("Asia/Jakarta")
    return datetime.now(tz)

# =========================
# GCS SETTINGS
# =========================
BUCKET_NAME = os.getenv("BUCKET_NAME", "sentiment-gov-models")

def download_from_gcs(bucket_name, gcs_path, local_path):
    """
    gcs_path  : data/raw/file.xlsx
    local_path: /tmp/raw/file.xlsx
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)

    local_path = Path(local_path)
    local_path.parent.mkdir(parents=True, exist_ok=True)

    blob.download_to_filename(str(local_path))