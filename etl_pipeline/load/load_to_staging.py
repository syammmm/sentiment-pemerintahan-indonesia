from sqlalchemy import create_engine
import os

def load_to_staging(df, table_name="stg_sentiment_article", schema="staging"):
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    df.to_sql(
        table_name,
        engine,
        schema=schema,
        if_exists="append",
        index=False
    )