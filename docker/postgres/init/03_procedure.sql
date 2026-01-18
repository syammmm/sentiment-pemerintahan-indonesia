CREATE OR REPLACE PROCEDURE production.sp_load_stg_to_fact()
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO production.fact_sentiment_article (
        media, title, published_date, link, content, sentiment, confidence
    )
    SELECT
        media, title, published_date, link, content, sentiment, confidence
    FROM staging.stg_sentiment_article s
    WHERE NOT EXISTS (
        SELECT 1
        FROM production.fact_sentiment_article p
        WHERE p.media = s.media
          AND p.title = s.title
          AND p.published_date = s.published_date
    );

    TRUNCATE TABLE staging.stg_sentiment_article;
END;
$$;