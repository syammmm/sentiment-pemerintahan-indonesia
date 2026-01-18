import pandas as pd
from pathlib import Path

def read_excel(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_excel(file_path)
    return df