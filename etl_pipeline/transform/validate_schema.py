REQUIRED_COLUMNS = {
    "media",
    "title",
    "published_date",
    "link",
    "content",
    "sentiment",
    "confidence"
}

def validate_schema(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df