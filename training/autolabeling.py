import pandas as pd
import joblib

# Load data baru
df = pd.read_excel("data/raw/media_elektronik_2024_2025_March.xlsx")

# Load model & vectorizer
model = joblib.load("models/logistic_model_optimized.pkl")
tfidf = joblib.load("models/tfidf_vectorizer_optimized.pkl")

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

# Simpan hasil auto labeling
df.to_excel("data/labeled/[labeled]media_elektronik_2024_2025_MAR.xlsx", index=False)

#high confidence
df_high_conf.to_excel(
    "data/labeled/[labeled_highconfidence]media_elektronik_2024_2025_MAR.xlsx",
    index=False
)

print("Total data           :", len(df))
print("High confidence data :", len(df_high_conf))
print("Threshold confidence :", THRESHOLD)
