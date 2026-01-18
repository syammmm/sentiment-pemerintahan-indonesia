from sqlalchemy import create_engine, text
import os

def call_stored_procedure():
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    with engine.begin() as conn:
        conn.execute(text("CALL production.sp_load_stg_to_fact();"))