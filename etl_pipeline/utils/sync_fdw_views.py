from sqlalchemy import create_engine, text
import os

RAW_DB = os.getenv("DB_NAME")
VIEW_DB = "gov_view_db"

engine_raw = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{RAW_DB}"
)

engine_view = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{VIEW_DB}"
)

def sync_materialized_views():
    with engine_raw.connect() as raw:
        mv_list = raw.execute(text("""
            SELECT matviewname
            FROM pg_matviews
            WHERE schemaname = 'analytics'
        """)).fetchall()

    with engine_view.begin() as view:
        existing = view.execute(text("""
            SELECT foreign_table_name
            FROM information_schema.foreign_tables
            WHERE foreign_table_schema = 'analytics'
        """)).fetchall()

        existing_set = {r[0] for r in existing}

        for (mv_name,) in mv_list:
            if mv_name not in existing_set:
                view.execute(text(f"""
                    IMPORT FOREIGN SCHEMA analytics
                    LIMIT TO ({mv_name})
                    FROM SERVER raw_db_server
                    INTO analytics;
                """))
                print(f"Imported FDW: {mv_name}")

    print("FDW sync completed")
#run : python -m etl_pipeline.utils.sync_fdw_views 
