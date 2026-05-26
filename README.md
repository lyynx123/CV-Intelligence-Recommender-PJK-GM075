<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white" alt="spaCy">
</p>

<h1 align="center">🎯 CV-Intelligence Recommender</h1>

<p align="center">
  <strong>Sistem Rekomendasi Pekerjaan Berbasis AI — Cukup Upload CV, Dapatkan Karir Impianmu!</strong>
</p>

<p align="center">
  <em>Capstone Project PJK-GM075 | Pijak × IBM SkillsBuild</em>
</p>

---

## 📋 Daftar Isi

- [Tentang Proyek](#-tentang-proyek)
- [Fitur Utama](#-fitur-utama)
- [Arsitektur Sistem](#-arsitektur-sistem)
- [Tech Stack](#-tech-stack)
- [Struktur Folder](#-struktur-folder)
- [Cara Instalasi](#-cara-instalasi)
- [Cara Menjalankan](#-cara-menjalankan)
- [API Documentation](#-api-documentation)
- [Dataset](#-dataset)
- [Performa Model](#-performa-model)
- [Tim Pengembang](#-tim-pengembang)
- [Lisensi](#-lisensi)

---

## 💡 Tentang Proyek

**CV-Intelligence Recommender (CV-IR)** adalah aplikasi berbasis AI yang membantu pencari kerja menemukan pekerjaan yang paling sesuai dengan kualifikasi mereka — hanya dengan mengunggah CV dalam format PDF.

### 🎯 Masalah yang Diselesaikan

> *Pencari kerja membuang terlalu banyak waktu dan tenaga untuk menyaring lowongan secara manual yang seringkali tidak relevan, serta kesulitan menentukan ekspektasi gaji yang objektif berdasarkan kompetensi pada CV mereka.*

### 💊 Solusi Kami

CV-IR bertindak sebagai **"painkiller"** bagi pencari kerja dengan:

1. **Membaca CV secara otomatis** — Ekstraksi teks dari PDF menggunakan PyMuPDF
2. **Mengidentifikasi skill** — 150+ skill keywords + Named Entity Recognition (spaCy)
3. **Memprediksi pekerjaan yang cocok** — Machine Learning classifier (TF-IDF + Random Forest)
4. **Merekomendasikan lowongan** — Cosine similarity matching terhadap 10,000+ lowongan LinkedIn
5. **Memberikan estimasi gaji** — Berdasarkan kategori pekerjaan dan jumlah skill

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 📄 **Upload CV (PDF)** | Drag & drop atau browse file CV dalam format PDF |
| 🛠️ **Skill Detection** | Deteksi otomatis skill teknis dan non-teknis dari teks CV |
| 🎯 **Job Prediction** | Prediksi kategori pekerjaan yang paling sesuai dengan confidence score |
| 💼 **Job Recommendations** | Top 5 lowongan kerja dari dataset LinkedIn dengan match score |
| 💰 **Salary Estimation** | Estimasi rentang gaji bulanan berdasarkan profil |
| 🔗 **Direct Links** | Link langsung ke posting lowongan di LinkedIn |
| 🌙 **Dark Mode UI** | Antarmuka modern dengan dark theme premium |

---

## 🏗️ Arsitektur Sistem

```
┌──────────────────────────────────────────────────────────┐
│                   FRONTEND (Streamlit)                     │
│  • Upload CV (PDF)           • Tampil Skill Badges        │
│  • Tampil Prediksi Pekerjaan • Tampil Rekomendasi         │
│  • Tampil Estimasi Gaji      • Dark Theme Premium         │
└────────────────────────┬─────────────────────────────────┘
                         │ HTTP POST /api/v1/predict
                         ▼
┌──────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                        │
│  • Validasi file PDF        • Pipeline orchestration      │
│  • Error handling           • CORS middleware             │
└───┬──────────┬──────────┬──────────┬─────────────────────┘
    │          │          │          │
    ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────────┐
│  PDF   │ │ Skill  │ │  Job   │ │    Job     │
│Extract │→│Extract │→│Predict │ │  Matcher   │
│(PyMuPDF)│ │(spaCy) │ │(RF+   │ │(TF-IDF    │
│        │ │        │ │TF-IDF)│ │Cosine Sim) │
└────────┘ └────────┘ └────────┘ └────────────┘
                                       │
                          ┌────────────▼────────────┐
                          │  Dataset LinkedIn Jobs   │
                          │  (10,000+ lowongan)      │
                          └─────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Teknologi | Kegunaan |
|-------|-----------|----------|
| **Frontend** | Streamlit | Antarmuka web interaktif |
| **Backend** | FastAPI + Uvicorn | REST API server |
| **PDF Parsing** | PyMuPDF (`fitz`) | Ekstraksi teks dari PDF |
| **NLP / NER** | spaCy (`en_core_web_sm`) | Named Entity Recognition |
| **ML Classifier** | Scikit-Learn (Random Forest) | Prediksi kategori pekerjaan |
| **Feature Engineering** | TF-IDF Vectorizer | Representasi teks sebagai fitur numerik |
| **Job Matching** | Cosine Similarity (TF-IDF) | Pencocokan CV dengan lowongan |
| **Data Processing** | Pandas, NumPy | Manipulasi dan analisis data |
| **Version Control** | Git & GitHub | Kolaborasi dan version control |

---

## 📁 Struktur Folder

```
cv-ir/
├── 📂 backend/
│   ├── main.py                    # FastAPI entry point
│   ├── routers/
│   │   └── predict.py             # Endpoint POST /api/v1/predict
│   └── modules/
│       ├── pdf_extractor.py       # Ekstraksi teks dari PDF
│       ├── skill_extractor.py     # Deteksi skill (150+ keywords + NER)
│       ├── job_matcher.py         # TF-IDF cosine similarity matching
│       └── job_predictor.py       # Random Forest job classifier
│
├── 📂 frontend/
│   └── app.py                     # Streamlit UI (dark theme premium)
│
├── 📂 data/
│   ├── raw/                       # Dataset mentah dari Kaggle
│   │   ├── UpdatedResumeDataSet.csv
│   │   ├── postings.csv           # 123,849 LinkedIn job postings
│   │   ├── companies/             # Data perusahaan
│   │   └── jobs/                  # Data skill, gaji, industri
│   └── processed/
│       └── job_listings.csv       # 10,000 lowongan bersih
│
├── 📂 models/
│   ├── job_classifier.pkl         # Trained Random Forest model
│   └── tfidf_vectorizer.pkl       # Trained TF-IDF vectorizer
│
├── 📂 notebooks/
│   ├── 01_preprocess_data.py      # Script preprocessing dataset
│   └── 02_train_model.py          # Script training model ML
│
├── 📂 tests/
│   └── test_predict.py            # Unit tests (pytest)
│
├── requirements.txt               # Dependencies
├── .env.example                   # Template environment variables
├── .gitignore                     # Git ignore configuration
└── README.md                      # Dokumentasi (file ini)
```

---

## 🚀 Cara Instalasi

### Prasyarat

- **Python** 3.10 atau lebih baru
- **pip** (package manager Python)
- **Git**

### Langkah Instalasi

```bash
# 1. Clone repository
git clone https://github.com/[org]/cv-ir.git
cd cv-ir

# 2. Buat virtual environment
python -m venv venv

# 3. Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download model spaCy
python -m spacy download en_core_web_sm
```

### Download Dataset (Opsional — jika ingin retrain model)

```bash
# Install Kaggle CLI
pip install kaggle

# Set Kaggle API token
# Windows PowerShell:
$env:KAGGLE_TOKEN='your_kaggle_token'

# Download datasets
kaggle datasets download -d jillanisofttech/updated-resume-dataset -p data/raw --unzip
kaggle datasets download -d arshkon/linkedin-job-postings -p data/raw --unzip

# Preprocessing dataset
python notebooks/01_preprocess_data.py

# Training model
python notebooks/02_train_model.py
```

---

## 🖥️ Cara Menjalankan

### 1. Jalankan Backend (Terminal 1)

```bash
cd "d:\Project\Project Capstone"
.\venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload --port 8000
```

### 2. Jalankan Frontend (Terminal 2)

```bash
cd "d:\Project\Project Capstone"
.\venv\Scripts\Activate.ps1
streamlit run frontend/app.py --server.port 8501
```

### 3. Akses Aplikasi

| Service | URL |
|---------|-----|
| 🎯 **Frontend** | [http://localhost:8501](http://localhost:8501) |
| ⚡ **Backend API** | [http://localhost:8000](http://localhost:8000) |
| 📚 **API Docs (Swagger)** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| 📖 **API Docs (ReDoc)** | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

### 4. Cara Menggunakan

1. Buka **http://localhost:8501** di browser
2. Upload CV dalam format **PDF**
3. Klik tombol **"🚀 Analisis CV Saya"**
4. Lihat hasil:
   - 🎯 Prediksi pekerjaan + confidence score
   - 🛠️ Skill yang terdeteksi
   - 💼 Top 5 rekomendasi lowongan kerja
   - 💰 Estimasi rentang gaji

---

## 📡 API Documentation

### `POST /api/v1/predict`

Upload CV dalam format PDF dan dapatkan analisis lengkap.

**Request:**

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -F "file=@path/to/cv.pdf"
```

**Response:**

```json
{
  "extracted_text": "John Doe Software Engineer with 5 years...",
  "skills": ["Python", "Machine Learning", "SQL", "TensorFlow", "Docker"],
  "predicted_job": "Data Science",
  "confidence": 0.8734,
  "salary_estimate": {
    "min": 12000000,
    "max": 27000000,
    "currency": "IDR"
  },
  "job_recommendations": [
    {
      "title": "Data Scientist",
      "company": "Tech Corp",
      "location": "Jakarta, Indonesia",
      "link": "https://www.linkedin.com/jobs/view/12345",
      "match_score": 0.8912
    }
  ]
}
```

### `GET /`

Health check endpoint.

```json
{
  "status": "CV-IR API is running 🚀",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

## 📊 Dataset

| Dataset | Sumber | Jumlah Data | Kegunaan |
|---------|--------|-------------|----------|
| **Updated Resume Dataset** | [Kaggle](https://www.kaggle.com/datasets/jillanisofttech/updated-resume-dataset) | 962 resumes, 25 kategori | Training model classifier |
| **LinkedIn Job Postings** | [Kaggle](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings) | 123,849 postings | Job matching & recommendations |

### 25 Kategori Pekerjaan yang Didukung

<table>
<tr>
<td>

| # | Kategori |
|---|----------|
| 1 | Java Developer |
| 2 | Testing |
| 3 | DevOps Engineer |
| 4 | Python Developer |
| 5 | Web Designing |
| 6 | HR |
| 7 | Hadoop |
| 8 | Data Science |
| 9 | Mechanical Engineer |

</td>
<td>

| # | Kategori |
|---|----------|
| 10 | Sales |
| 11 | Operations Manager |
| 12 | ETL Developer |
| 13 | Blockchain |
| 14 | Arts |
| 15 | Database |
| 16 | Health and Fitness |
| 17 | Electrical Engineering |

</td>
<td>

| # | Kategori |
|---|----------|
| 18 | PMO |
| 19 | Business Analyst |
| 20 | DotNet Developer |
| 21 | Automation Testing |
| 22 | Network Security Engineer |
| 23 | Civil Engineer |
| 24 | SAP Developer |
| 25 | Advocate |

</td>
</tr>
</table>

---

## 📈 Performa Model

Model dilatih menggunakan **TF-IDF + Random Forest** pada 962 resume dengan 25 kategori.

| Metrik | Skor |
|--------|------|
| **Accuracy** | **99.5%** |
| **Precision** (macro avg) | 0.99 |
| **Recall** (macro avg) | 1.00 |
| **F1-Score** (macro avg) | 0.99 |

### Metodologi

```
CV Text → Text Cleaning → TF-IDF Vectorization → Random Forest → Predicted Job Category
           (lowercase,      (5000 features,        (200 trees,
            remove URLs,     bigrams)               balanced weights)
            remove special
            chars)
```

---

## 🧪 Testing

```bash
# Jalankan semua unit tests
pytest tests/ -v --tb=short

# Test spesifik
pytest tests/test_predict.py -v
```

### Variasi CV untuk Testing Manual

- [ ] CV fresh graduate (sedikit pengalaman)
- [ ] CV senior engineer (banyak skill teknis)
- [ ] CV desainer (skill non-teknis)
- [ ] CV multibahasa (Indonesia + Inggris)
- [ ] CV dengan format beragam (1 kolom, 2 kolom)

---

## 👥 Tim Pengembang

<table>
<tr>
<td align="center">
<strong>Ahmad Izzuddin Ulinnuha</strong><br>
<sub>🔵 Project Leader & AI Integration</sub><br>
<sub>APC902D6Y0383</sub>
</td>
<td align="center">
<strong>Azka Nur Fadel</strong><br>
<sub>🟢 Data Engineer</sub><br>
<sub>APC347D6Y0353</sub>
</td>
<td align="center">
<strong>Alif Khusain Bilfaqih</strong><br>
<sub>🟡 Machine Learning Engineer</sub><br>
<sub>APC659D6Y0204</sub>
</td>
</tr>
<tr>
<td align="center">
<strong>Muhammad Za'im Shidqi</strong><br>
<sub>🟠 Backend & API Developer</sub><br>
<sub>APC324D6Y0185</sub>
</td>
<td align="center">
<strong>Muhammad Zaenal Arifin</strong><br>
<sub>🔴 Frontend & UI Developer</sub><br>
<sub>APC338D6Y0449</sub>
</td>
<td align="center">
</td>
</tr>
</table>

---

## 📄 Lisensi

Proyek ini dikembangkan sebagai bagian dari **Capstone Project** program **Pijak in collaboration with IBM SkillsBuild**.

**Tema**: AI for Smart Recommendation Systems

---

<p align="center">
  <strong>🎯 CV-Intelligence Recommender (CV-IR)</strong><br>
  <em>Upload CV. Temukan Karir. Raih Masa Depan.</em><br><br>
  <sub>© 2026 Tim PJK-GM075 — Pijak × IBM SkillsBuild</sub>
</p>