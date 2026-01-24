# Sentiment Pemerintahan Indonesia

Project untuk menganalisis sentimen berita terkait pemerintahan Indonesia melalui web scraping dari berbagai media elektronik dan pemrosesan NLP.

---

## 📋 Table of Contents

- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Part 1: Data Collection (Web Scraping)](#part-1-data-collection-web-scraping)
  - [Konfigurasi](#konfigurasi)
  - [Cara Menjalankan](#cara-menjalankan)
  - [Output](#output)
- [Part 2: Model Training (Logistic Regression)](#part-2-model-training-logistic-regression)
  - [Persiapan Dataset](#persiapan-dataset)
  - [Cara Menjalankan Training](#cara-menjalankan-training)
  - [Output Training](#output-training)
  - [Output Model](#output-model)
  - [Tips & Troubleshooting](#tips--troubleshooting)
- [Part 3: Auto-Labeling dengan Model Terlatih](#part-3-auto-labeling-dengan-model-terlatih)
  - [Prasyarat](#prasyarat)
  - [Konfigurasi](#konfigurasi-1)
  - [Cara Menjalankan Auto-Labeling](#cara-menjalankan-auto-labeling)
  - [Output Auto-Labeling](#output-auto-labeling)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Persyaratan Sistem

- **Python**: 3.8 atau lebih tinggi
- **pip**: Package manager untuk Python
- **Git**: Untuk clone project

---

## 📥 Instalasi

### 1. Clone/Pull Project

```bash
git clone <repository-url>
cd sentiment-pemerintahan-indonesia
```

atau jika sudah ada folder project:

```bash
cd sentiment-pemerintahan-indonesia
git pull
```

### 2. Setup Python Environment (Opsional tapi Recommended)

Disarankan menggunakan virtual environment untuk menghindari konflik dependencies:

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Untuk macOS/Linux:
source venv/bin/activate

# Untuk Windows:
# venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

Atau jika menggunakan requirements khusus untuk NLP pipeline:

```bash
cd nlp_pipeline
pip install -r requirements.txt
cd ..
```

---

## 🚀 Part 1: Data Collection (Web Scraping)

### 📝 Konfigurasi

Sebelum menjalankan script, edit file [nlp_pipeline/config/settings.py] untuk mengatur rentang tanggal yang ingin di-scraping:

```python
START_DATE = date(2025, 12, 1)  # Edit as needed - Format: (YYYY, MM, DD)
END_DATE = date(2025, 12, 31)   # Edit as needed - Format: (YYYY, MM, DD)
```

**Contoh penggunaan:**

```python
# Scraping berita Januari 2025
START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 1, 31)

# Scraping berita satu hari
START_DATE = date(2025, 1, 15)
END_DATE = date(2025, 1, 15)

# Scraping berita tiga bulan
START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 3, 31)
```

### 🏃 Cara Menjalankan

#### Opsi 1: Menjalankan dari root project directory

```bash
cd nlp_pipeline
python main.py
```

#### Opsi 2: Menjalankan dengan Python secara langsung

```bash
python nlp_pipeline/main.py
```

#### Output yang Diharapkan

Ketika script berjalan, Anda akan melihat output seperti berikut:

```
Start Time : 2025-01-23 14:30:45
Finish Time Tempo: 2025-01-23 14:35:12
Finish Time Detik: 2025-01-23 14:40:28
Finish Time CNN: 2025-01-23 14:42:15
Finish Time ALL: 2025-01-23 14:42:20
✅ Total artikel Tempo: 245
✅ Total artikel Detik: 189
✅ Total artikel CNN: 156
✅ Total artikel: 590
📁 File tersimpan: nlp_pipeline/data/raw
```

### 📂 Output Data

Setelah script selesai, data akan tersimpan di `nlp_pipeline/data/raw/` dalam dua format:

- **File Excel**: `media_elektronik_[range date].xlsx`
- **File CSV**: `media_elektronik_[range date].csv`

Penamaan file mengikuti format: `media_elektronik_[range date].xlsx`

**Struktur data:**
- Kombinasi artikel dari 3 media: Tempo, Detik, CNN
- Duplikat link otomatis dihapus
- Kolom: title, link, date, media source, dll

---

## 🤖 Part 2: Model Training (Logistic Regression)

### 📋 Persiapan Dataset

Sebelum melakukan training model, pastikan file dataset tersedia di folder `nlp_pipeline/data/labeled/`. 

**File Dataset yang Tersedia:**
- `base_data_sentimen_pemerintahan.xlsx` - Dataset dasar hasil manual labeling
- `manual_labeled_sentimen_pemerintahan.xlsx` - Dataset hasil manual labeling
- `[labeled_all]media_elektronik_2025_*.xlsx` - Dataset terklasifikasi untuk berbagai bulan

**Catatan Dataset:**
- ✅ File berformat **Excel (.xlsx)**
- ✅ Sudah terisi **sentiment label** secara manual
- ✅ Kolom utama: `content` (teks berita) dan `sentiment` (label: Positif/Netral/Negatif)
- ✅ Duplikat dan data kosong akan dihapus secara otomatis saat training

### 🏃 Cara Menjalankan Training

#### Opsi 1: Menjalankan dari root project directory

```bash
cd nlp_pipeline/training
python train_logistic_optimized.py
```

#### Opsi 2: Menjalankan dengan Python secara langsung

```bash
python nlp_pipeline/training/train_logistic_optimized.py
```

### 📊 Output Training

Ketika script berjalan, Anda akan melihat output seperti berikut:

```
Training model...
[CV iteration info...]

Best Params: {'clf__C': 1.0, 'clf__solver': 'saga'}

Accuracy: 0.7832

Classification Report:
              precision    recall  f1-score   support

           0       0.75      0.78      0.76       250
           1       0.78      0.76      0.77       245
           2       0.81      0.82      0.81       255

    accuracy                           0.78       750
   macro avg       0.78      0.79      0.78       750
weighted avg       0.78      0.78      0.78       750

Confusion Matrix:
 [[195  35  20]
  [ 28 186  31]
  [ 18  25 212]]

Model saved to models/logistic_model_optimized_final.pkl
```

### 📂 Output Model

Setelah training selesai, model dan vectorizer akan tersimpan di `nlp_pipeline/models/`:

#### File yang Dihasilkan:

1. **`logistic_model_optimized_final.pkl`**
   - Model Logistic Regression terlatih
   - Ukuran: ~50-100 MB (tergantung ukuran training set)
   - Digunakan untuk: Prediksi sentiment pada data baru

2. **`tfidf_vectorizer_optimized_final.pkl`**
   - TF-IDF Vectorizer yang sudah fitted
   - Ukuran: ~20-30 MB
   - Digunakan untuk: Transformasi teks baru ke fitur numerik sebelum prediksi
   - Konfigurasi: ngram_range=(1,2), max_features=20000, min_df=3, max_df=0.9

### 🔍 Penjelasan Model Training

**Model Architecture:**
```python
Pipeline:
├── TF-IDF Vectorizer
│   ├── Bigram & Unigram (ngram_range=(1,2))
│   ├── Max 20,000 features
│   └── Min document frequency: 3, Max: 90%
│
└── Logistic Regression Classifier
    ├── Max iterations: 1000
    ├── Class weight: balanced
    └── Multi-processing: enabled (-1 cores)
```

**Hyperparameter Tuning:**
- Grid Search dengan 5-fold Cross-Validation
- Parameter C: [0.1, 0.5, 1, 2, 5, 10]
- Solver: [lbfgs, saga]
- Scoring metric: F1-macro

**Label Mapping:**
```python
Positif  → 2
Netral   → 1
Negatif  → 0
```

### 💡 Tips & Troubleshooting

| Issue | Solusi |
|-------|--------|
| `FileNotFoundError: No such file` | Pastikan file excel ada di `nlp_pipeline/data/labeled/` |
| `KeyError: 'content' or 'sentiment'` | Cek nama kolom di file excel, harus tepat: `content` dan `sentiment` |
| Script berjalan lama | Normal, GridSearch membutuhkan waktu untuk tuning. Tunggu sampai selesai. |
| Memory error / Out of memory | Kurangi `max_features` di TfidfVectorizer atau `test_size` di train_test_split |
| Model pkl tidak tersimpan | Pastikan folder `nlp_pipeline/models/` ada dan writable |

---

## 🏷️ Part 3: Auto-Labeling dengan Model Terlatih

### ✅ Prasyarat

Sebelum menjalankan autolabeling, pastikan:

1. ✅ **Part 1 sudah selesai** - Data scraping dari berbagai media sudah tersimpan di `nlp_pipeline/data/raw/`
2. ✅ **Part 2 sudah selesai** - Model terlatih sudah ada:
   - `nlp_pipeline/models/logistic_model_optimized_final.pkl`
   - `nlp_pipeline/models/tfidf_vectorizer_optimized_final.pkl`

**Jika model pkl belum ada**, lakukan Part 2 terlebih dahulu karena membutuhkan sample data training yang sudah dilabelisasi secara manual.

### 📝 Konfigurasi

Edit file [nlp_pipeline/config/settings.py] untuk mengatur tanggal yang sesuai dengan data scraping dari Part 1:

```python
DATE_TEXT = "2025_December"  # Harus sesuai dengan nama file hasil scraping
```

**Contoh:**
```python
# Jika file raw data bernama: media_elektronik_2025_December.xlsx
DATE_TEXT = "2025_December"

# Jika file raw data bernama: media_elektronik_2025_January.xlsx
DATE_TEXT = "2025_January"
```

### 🏃 Cara Menjalankan Auto-Labeling

#### Opsi 1: Menjalankan dari root project directory

```bash
cd nlp_pipeline/training
python autolabeling.py
```

#### Opsi 2: Menjalankan dengan Python secara langsung

```bash
python nlp_pipeline/training/autolabeling.py
```

### 📊 Output Auto-Labeling

Ketika script berjalan, Anda akan melihat output seperti berikut:

```
Total data            : 590
High confidence data  : 487
Threshold confidence  : 0.8
```

**Output Explanation:**
- **Total data**: Jumlah seluruh artikel dari Part 1 yang berhasil diproses
- **High confidence data**: Artikel dengan confidence score ≥ 80%
- **Threshold**: Batasan confidence untuk memfilter hasil labeling

### 📂 Output Auto-Labeling Data

Setelah script selesai, hasil autolabeling akan tersimpan di **`nlp_pipeline/data/labeled/`** dalam 3 file Excel:

#### 1. **`[labeled_all]media_elektronik_{DATE_TEXT}.xlsx`** ⭐ (File Lengkap)
   - Berisi **semua** artikel dengan sentiment prediction
   - Kolom tambahan: `sentiment` dan `confidence`
   - Label: Positif, Netral, Negatif
   - Confidence: 0.0 - 1.0 (semakin tinggi = semakin yakin model)
   - **Ukuran**: Sama dengan jumlah artikel dari Part 1

   **Contoh struktur:**
   ```
   | title | link | published_date | sentiment | confidence |
   |-------|------|-----------------|-----------|------------|
   | Berita 1... | https://... | 2025-12-15 | Positif | 0.92 |
   | Berita 2... | https://... | 2025-12-16 | Negatif | 0.78 |
   | Berita 3... | https://... | 2025-12-17 | Netral | 0.65 |
   ```

#### 2. **`[labeled_highconfidence]media_elektronik_{DATE_TEXT}.xlsx`** ⭐ (Rekomendasi Utama)
   - Berisi **hanya artikel dengan confidence ≥ 80%**
   - Hasil prediksi paling akurat dan dapat dipercaya
   - **Direkomendasikan** untuk analisis lanjutan atau publikasi
   - **Ukuran**: 70-90% dari total data (tergantung kualitas model)

#### 3. **`[labeled_lowconfidence]media_elektronik_{DATE_TEXT}.xlsx`**
   - Berisi **artikel dengan confidence < 80%**
   - Hasil prediksi kurang pasti, perlu review manual
   - **Gunakan untuk**: Data improvement atau training set baru
   - **Ukuran**: 10-30% dari total data

### 🔍 Penjelasan Proses Auto-Labeling

**Workflow:**

```
1. Load Raw Data (dari Part 1)
   ↓
2. Load Model & Vectorizer (dari Part 2)
   ↓
3. Transform Teks → Numerik (TF-IDF)
   ↓
4. Predict Sentiment + Confidence Score
   ↓
5. Filter by Confidence Threshold (0.8)
   ↓
6. Simpan 3 File Output
   ├─ [labeled_all]          → Semua data
   ├─ [labeled_highconfidence] → Confidence ≥ 80%
   └─ [labeled_lowconfidence]  → Confidence < 80%
```

**Confidence Score:**
- **0.95 - 1.00**: Prediksi sangat yakin ✅
- **0.85 - 0.95**: Prediksi yakin ✅
- **0.75 - 0.85**: Prediksi cukup yakin ⚠️
- **0.65 - 0.75**: Prediksi kurang yakin ⚠️
- **< 0.65**: Prediksi tidak yakin ❌

### 💡 Tips & Troubleshooting

| Issue | Solusi |
|-------|--------|
| `FileNotFoundError: logistic_model_optimized.pkl` | Jalankan Part 2 (train model) terlebih dahulu |
| `FileNotFoundError: media_elektronik_2025_December.xlsx` | Cek file di `nlp_pipeline/data/raw/` dan sesuaikan `DATE_TEXT` di settings.py |
| File `.pkl` tidak ditemukan | Pastikan nama file pkl di settings.py sesuai dengan nama file yang disimpan di Part 2 |
| Output file tidak tersimpan | Pastikan folder `nlp_pipeline/data/labeled/` ada dan writable |
| Confidence score terlalu rendah | Model mungkin perlu training ulang dengan dataset yang lebih besar/berkualitas |

---

## 🐛 Debugging

### Jika Ada Error saat Install Requirements

```bash
# Upgrade pip terlebih dahulu
pip install --upgrade pip

# Install ulang requirements
pip install -r requirements.txt --force-reinstall
```

### Jika Script Tidak Berjalan

1. **Pastikan berada di directory yang tepat:**

```bash
pwd  # Cek current directory
ls   # Lihat file di folder
```

2. **Check Python version:**

```bash
python --version
```

3. **Check installed packages:**

```bash
pip list
```

4. **Jalankan dengan verbose mode untuk melihat error detail:**

```bash
python -u nlp_pipeline/main.py
```

### Common Issues

| Issue | Solusi |
|-------|--------|
| `ModuleNotFoundError: No module named 'bs4'` | Jalankan: `pip install beautifulsoup4` |
| `ModuleNotFoundError: No module named 'pandas'` | Jalankan: `pip install pandas` |
| Script lama berjalan (tanpa output) | Script sedang scraping. Tunggu sampai selesai. |
| File tidak tersimpan di data/raw | Cek permission folder atau jalankan dari directory yang tepat |

---

## 📌 Catatan Penting

- ✅ Tanggal dalam script menggunakan format: `date(TAHUN, BULAN, TANGGAL)`
- ✅ Output file akan menimpa file dengan nama yang sama
- ✅ Proses scraping bisa memakan waktu tergantung jumlah artikel
- ✅ Virtual environment sangat disarankan untuk production
