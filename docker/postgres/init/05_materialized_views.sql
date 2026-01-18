CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_sentiment_daily AS
SELECT
    published_date,
    sentiment,
    COUNT(*) AS total_artikel
FROM production.fact_sentiment_article
GROUP BY 1,2;

CREATE INDEX IF NOT EXISTS idx_mv_sentiment_date
ON analytics.mv_sentiment_daily (published_date);

CREATE INDEX IF NOT EXISTS idx_mv_sentiment_type
ON analytics.mv_sentiment_daily (sentiment);