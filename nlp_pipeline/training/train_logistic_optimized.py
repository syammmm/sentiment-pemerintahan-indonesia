import pandas as pd
import joblib
import re

from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline
#from preprocessing.utils.preprocessing import clean_text

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ===== Load Dataset =====
df = pd.read_excel("data/labeled/base_data_sentimen_pemerintahan.xlsx")

df = df.dropna(subset=["content", "sentiment"])
# df["clean_text"] = df["content"].astype(str).apply(clean_text)

# Label encoding
label_map = {
    "Positif": 2,
    "Netral": 1,
    "Negatif": 0
}
df["label"] = df["sentiment"].map(label_map)

X = df["content"].astype(str)
y = df["label"]

# ===== Split Data =====
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ===== TF-IDF New Optimized =====
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1,2),
        max_features=20000,
        min_df=3,
        max_df=0.9,
        sublinear_tf=True
    )),
    ("clf", LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        n_jobs=-1
    ))
])


# =========================
# GridSearch
# =========================
param_grid = {
    "clf__C": [0.1, 0.5, 1, 2, 5, 10],
    "clf__solver": ["lbfgs", "saga"]
}

grid = GridSearchCV(
    pipeline,
    param_grid,
    cv=5,
    scoring="f1_macro",
    verbose=2,
    n_jobs=-1
)

# =========================
# Training
# =========================
print("Training model...")
grid.fit(X_train, y_train)

best_model = grid.best_estimator_

print("\nBest Params:", grid.best_params_)

# =========================
# Evaluation
# =========================
y_pred = best_model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# =========================
# Save Model
# =========================
joblib.dump(best_model, "models/logistic_model_optimized_final.pkl")
joblib.dump(pipeline.named_steps["tfidf"], "models/tfidf_vectorizer_optimized_final.pkl")

print("\nModel saved to models/logistic_model_optimized_final.pkl")