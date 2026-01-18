from sqlalchemy import create_engine, text
import os

def refresh_materialized_views():
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    with engine.begin() as conn:
        conn.execute(text("CALL analytics.sp_refresh_mv();"))
    # with engine.begin() as conn:
    #     conn.execute(
    #         text("REFRESH MATERIALIZED VIEW analytics.mv_sentiment_daily;")
    #     )
    #     conn.execute(
    #         text("REFRESH MATERIALIZED VIEW analytics.mv_sentiment;")
    #     )
    #     # conn.execute(
    #     #     text("REFRESH MATERIALIZED VIEW analytics.mv_confidence_media;")
    #     # )
    #     # conn.execute(
    #     #     text("REFRESH MATERIALIZED VIEW analytics.mv_dim_media;")
    #     # )
    #     # conn.execute(
    #     #     text("REFRESH MATERIALIZED VIEW analytics.mv_dim_sentiment;")
    #     # )
    #     conn.execute(
    #         text("REFRESH MATERIALIZED VIEW analytics.mv_sentiment_monthly;")
    #     )
    #     # conn.execute(
    #     #     text("REFRESH MATERIALIZED VIEW analytics.mv_sentiment_monthly_wide ;")
    #     # )
    #     conn.execute(
    #         text("REFRESH MATERIALIZED VIEW analytics.mv_sentiment_weekly;")
    #     )
    #     # conn.execute(
    #     #     text("REFRESH MATERIALIZED VIEW analytics.mv_sentiment_media;")
    #     # )
    #     # kalau nanti ada MV lain, tambahkan di sini
    #     # conn.execute(text("REFRESH MATERIALIZED VIEW analytics.mv_confidence_media;"))

    print("Materialized view refreshed")