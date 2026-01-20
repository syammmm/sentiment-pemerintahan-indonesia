import os
import pandas as pd
from pathlib import Path

from etl_pipeline.config.settings import download_from_gcs,BUCKET_NAME

def read_excel(file_path: Path) -> pd.DataFrame:
    ENV = os.getenv("APP_ENV", "local")
    if ENV != "cloud" and not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Load data baru
    if ENV == "cloud" and not file_path.exists():
        download_from_gcs(
            bucket_name=BUCKET_NAME,
            gcs_path="data/labeled/[labeled_all]media_elektronik_2026_January_Test_Cloud.xlsx",
            local_path=file_path
        )
    df = pd.read_excel(file_path)
    return df