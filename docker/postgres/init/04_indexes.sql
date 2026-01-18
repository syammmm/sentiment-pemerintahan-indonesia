-- ============================
-- INDEX FOR BI PERFORMANCE
-- ============================

CREATE INDEX IF NOT EXISTS idx_fact_published_date
ON production.fact_sentiment_article (published_date);

CREATE INDEX IF NOT EXISTS idx_fact_sentiment
ON production.fact_sentiment_article (sentiment);

CREATE INDEX IF NOT EXISTS idx_fact_media_date
ON production.fact_sentiment_article (media, published_date);