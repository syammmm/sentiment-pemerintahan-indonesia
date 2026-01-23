import pandas as pd
import joblib

from nlp_pipeline.config.settings import RAW_DATA_DIR, LABELLED_DATA_DIR,DATE_TEXT


# Input path
excel_path_raw = RAW_DATA_DIR / f"media_elektronik_{DATE_TEXT}.xlsx"
# Output paths
excel_path_low_conf = LABELLED_DATA_DIR / f"[labeled_lowconfidence]media_elektronik_{DATE_TEXT}.xlsx"
excel_path_high_conf = LABELLED_DATA_DIR / f"[labeled_highconfidence]media_elektronik_{DATE_TEXT}.xlsx"
excel_path_all = LABELLED_DATA_DIR / f"[labeled_all]media_elektronik_{DATE_TEXT}.xlsx"

# Load data baru
df = pd.read_excel(excel_path_raw)

# Convert to datetime
df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")

# Delete rows with invalid published_date
df = df.dropna(subset=["published_date"])

df["published_date"] = df["published_date"].dt.strftime("%Y-%m-%d")

# Load model & vectorizer
model = joblib.load("nlp_pipeline/models/logistic_model_optimized.pkl")
tfidf = joblib.load("nlp_pipeline/models/tfidf_vectorizer_optimized.pkl")

# Pastikan kolom content ada
texts = df["content"].astype(str)

# Transform pakai TF-IDF lama
# X = tfidf.transform(texts)

# Predict sentiment + confidence
proba = model.predict_proba(texts)              # shape: (n_sample, 3)
confidence = proba.max(axis=1)              # ambil probabilitas tertinggi
pred = proba.argmax(axis=1)                  # ambil label prediksi (tertinggi)

# Mapping label numerik ke teks
label_map = {
    0: "Negatif",
    1: "Netral",
    2: "Positif"
}

df["sentiment"] = [label_map[p] for p in pred]
df["confidence"] = confidence

# =============================
# Filtering confidence
# =============================
THRESHOLD = 0.8
df_high_conf = df[df["confidence"] >= THRESHOLD].copy()
# Low Confidence
df_low_conf = df[df["confidence"] < THRESHOLD].copy()

# Simpan hasil auto labeling
df.to_excel(excel_path_all, index=False)

#high confidence
# df_high_conf.to_excel(
#     excel_path_high_conf,
#     index=False
# )

#low confidence
df_low_conf.to_excel(
    excel_path_low_conf,
    index=False
)

print("Total data           :", len(df))
print("High confidence data :", len(df_high_conf))
print("Threshold confidence :", THRESHOLD)
