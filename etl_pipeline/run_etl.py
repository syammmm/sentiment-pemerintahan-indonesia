from pathlib import Path
from dotenv import load_dotenv

from etl_pipeline.extract.read_excel import read_excel
from etl_pipeline.transform.validate_schema import validate_schema
from etl_pipeline.load.load_to_staging import load_to_staging
from etl_pipeline.load.call_procedure import call_stored_procedure
from etl_pipeline.load.refresh_materialized_views import refresh_materialized_views
from etl_pipeline.utils.sync_fdw_views import sync_materialized_views

load_dotenv()

EXCEL_PATH = Path(
    "nlp_pipeline/data/labeled/(ALL DATA)media_elektronik_2025.xlsx"
)

def main():
    df = read_excel(EXCEL_PATH)
    df = validate_schema(df)
    load_to_staging(df)
    call_stored_procedure()
    refresh_materialized_views()
    # sync_materialized_views()
    print("ETL SUCCESS")

if __name__ == "__main__":
    main()