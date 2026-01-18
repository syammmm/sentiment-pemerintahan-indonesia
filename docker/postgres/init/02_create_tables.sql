CREATE TABLE IF NOT EXISTS staging.stg_sentiment_article (
    media            TEXT,
    title            TEXT,
    published_date   DATE,
    link             TEXT,
    content          TEXT,
    sentiment        VARCHAR(20),
    confidence       NUMERIC(6,4),
    loaded_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS production.fact_sentiment_article (
    article_id       BIGSERIAL PRIMARY KEY,
    media            TEXT NOT NULL,
    title            TEXT NOT NULL,
    published_date   DATE NOT NULL,
    link             TEXT,
    content          TEXT,
    sentiment        VARCHAR(20) NOT NULL,
    confidence       NUMERIC(6,4),
    inserted_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (media, title, published_date, link)
);