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

Sebelum menjalankan script, edit file [nlp_pipeline/main.py](nlp_pipeline/main.py#L9-L10) untuk mengatur rentang tanggal yang ingin di-scraping:

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

- **File Excel**: `media_elektronik_2025_December.xlsx`
- **File CSV**: `media_elektronik_2025_December.csv`

Penamaan file mengikuti format: `media_elektronik_[TAHUN]_[BULAN].xlsx`

**Struktur data:**
- Kombinasi artikel dari 3 media: Tempo, Detik, CNN
- Duplikat link otomatis dihapus
- Kolom: title, link, date, media source, dll

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
