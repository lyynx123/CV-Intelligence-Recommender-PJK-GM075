# 🎯 CV-Intelligence Recommender (CV-IR)

### Sistem Rekomendasi Pekerjaan Berbasis AI
**Capstone Project PJK-GM075 | Pijak × IBM SkillsBuild**

**Tema:** AI for Smart Recommendation Systems

---

## 📌 Slide 1 — Latar Belakang Masalah

### Masalah yang Dihadapi Pencari Kerja

Pencari kerja di Indonesia menghadapi **3 masalah utama**:

| No | Masalah | Dampak |
|----|---------|--------|
| 1 | Menyaring lowongan secara manual sangat membuang waktu | Rata-rata pencari kerja menghabiskan **11 jam/minggu** hanya untuk *scrolling* lowongan |
| 2 | Tidak tahu profesi apa yang cocok dengan skill mereka | Banyak lulusan baru yang bingung arah karir |
| 3 | Sulit menentukan ekspektasi gaji yang realistis | Sering menerima gaji di bawah standar karena tidak punya data pembanding |

### Solusi Kami: CV-Intelligence Recommender

> **"Cukup upload CV dalam format PDF, AI kami akan membaca skill Anda, memprediksi profesi yang cocok, dan mencarikan 5 lowongan kerja LinkedIn yang paling relevan — semuanya dalam hitungan detik."**

---

## 📌 Slide 2 — Fitur Utama Aplikasi

| Fitur | Deskripsi |
|-------|-----------|
| 📄 **Upload CV (PDF)** | Drag & drop file CV, sistem langsung membaca teksnya |
| 🛠️ **Skill Detection** | Deteksi otomatis 150+ skill teknis & non-teknis menggunakan NLP (spaCy) |
| 🎯 **Job Prediction** | AI memprediksi kategori pekerjaan yang cocok beserta *confidence score* |
| 💼 **Job Matching** | Top 5 rekomendasi lowongan kerja dari 110.000+ data LinkedIn |
| 💰 **Salary Estimation** | Estimasi rentang gaji bulanan berdasarkan profil & skill |
| 🔗 **Direct Link** | Link langsung ke halaman lowongan di LinkedIn |
| 🌙 **Dark Mode UI** | Tampilan premium dengan dark theme modern |

---

## 📌 Slide 3 — Arsitektur Sistem

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
│(PyMuPDF)│ │(spaCy) │ │(RF +  │ │(TF-IDF    │
│        │ │        │ │TF-IDF)│ │Cosine Sim) │
└────────┘ └────────┘ └────────┘ └────────────┘
                                       │
                          ┌────────────▼────────────┐
                          │  Dataset LinkedIn Jobs   │
                          │  (110,000+ lowongan)     │
                          └─────────────────────────┘
```

### Alur Kerja Sistem:
1. **User** upload CV (PDF) melalui antarmuka Streamlit
2. **PyMuPDF** mengekstrak seluruh teks dari file PDF
3. **spaCy NLP** mendeteksi skill menggunakan 150+ keywords + Named Entity Recognition
4. **Random Forest + TF-IDF** memprediksi kategori pekerjaan yang cocok
5. **Cosine Similarity** mencocokkan teks CV dengan 110.000+ deskripsi lowongan LinkedIn
6. Hasil ditampilkan: prediksi pekerjaan, skill terdeteksi, 5 rekomendasi lowongan, dan estimasi gaji

---

## 📌 Slide 4 — Tech Stack

| Layer | Teknologi | Kegunaan |
|-------|-----------|----------|
| **Frontend** | Streamlit | Antarmuka web interaktif |
| **Backend** | FastAPI + Uvicorn | REST API server |
| **PDF Parsing** | PyMuPDF (`fitz`) | Ekstraksi teks dari PDF |
| **NLP / NER** | spaCy (`en_core_web_sm`) | Named Entity Recognition untuk deteksi skill |
| **ML Classifier** | Scikit-Learn (Random Forest) | Prediksi kategori pekerjaan |
| **Feature Engineering** | TF-IDF Vectorizer (5000 fitur, bigram) | Representasi teks sebagai vektor numerik |
| **Job Matching** | Cosine Similarity (TF-IDF) | Pencocokan CV dengan lowongan kerja |
| **Data Processing** | Pandas, NumPy | Manipulasi dan analisis data |
| **Deployment** | Docker, Hugging Face Spaces | Hosting aplikasi |
| **Version Control** | Git & GitHub | Kolaborasi dan version control |

---

## 📌 Slide 5 — Dataset

Proyek ini menggunakan **2 dataset** dari Kaggle dengan fungsi yang berbeda:

### Dataset 1: Resume Dataset (Untuk Training AI)

| Aspek | Detail |
|-------|--------|
| **Nama** | UpdatedResumeDataSet.csv |
| **Sumber** | [Kaggle - jillanisofttech](https://www.kaggle.com/datasets/jillanisofttech/updated-resume-dataset) |
| **Jumlah Data** | 962 CV |
| **Jumlah Kategori** | 25 kategori pekerjaan |
| **Fungsi** | Melatih model Machine Learning (Random Forest) agar bisa memprediksi profesi berdasarkan teks CV |

**25 Kategori Pekerjaan yang Didukung:**
Java Developer, Testing, DevOps Engineer, Python Developer, Web Designing, HR, Hadoop, Data Science, Mechanical Engineer, Sales, Operations Manager, ETL Developer, Blockchain, Arts, Database, Health & Fitness, PMO, Electrical Engineering, Business Analyst, DotNet Developer, Automation Testing, Network Security Engineer, Civil Engineer, SAP Developer, Advocate

### Dataset 2: LinkedIn Job Postings (Untuk Rekomendasi)

| Aspek | Detail |
|-------|--------|
| **Nama** | LinkedIn Job Postings (postings.csv + companies.csv) |
| **Sumber** | [Kaggle - arshkon](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings) |
| **Data Mentah** | 123.849 lowongan kerja |
| **Data Setelah Preprocessing** | 110.837 lowongan kerja aktif |
| **Fungsi** | Sebagai bank data (knowledge base) untuk dicocokkan dengan CV pengguna menggunakan Cosine Similarity |

### Pipeline Preprocessing Data

```
postings.csv (123.849 rows, 31 kolom)
        │
        ├── Gabungkan dengan companies.csv (nama perusahaan)
        ├── Hapus lowongan dengan deskripsi kosong / terlalu pendek
        ├── Seleksi 5 kolom: title, company, location, description, link
        │
        ▼
job_listings.csv (110.837 rows, 5 kolom) ← File bersih siap pakai
```

---

## 📌 Slide 6 — Metodologi Machine Learning

### Pipeline Training Model

```
    CV Text (Raw)
        │
        ▼
┌─────────────────────┐
│    Text Cleaning     │  → Lowercase, hapus URL, email, karakter khusus, HTML tags
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  TF-IDF Vectorizer   │  → 5000 fitur, unigram + bigram, stop words removal
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│   Train/Test Split   │  → 80% training (769 sampel), 20% testing (193 sampel)
│   (Stratified)       │    Stratified split menjaga proporsi setiap kategori
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│   Random Forest      │  → 200 decision trees, class_weight="balanced"
│   Classifier         │
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│   Evaluation         │  → Accuracy, Precision, Recall, F1-Score
└─────────────────────┘
```

### Hyperparameter Model

| Parameter | Nilai | Alasan |
|-----------|-------|--------|
| `n_estimators` | 200 | Jumlah pohon keputusan, semakin banyak semakin stabil |
| `max_depth` | None | Tidak dibatasi, agar pohon bisa mempelajari pola detail |
| `min_samples_split` | 2 | Minimum sampel untuk membagi node |
| `class_weight` | balanced | Menangani ketidakseimbangan jumlah data antar kategori |
| `random_state` | 42 | Reproducibility (hasil bisa diulang) |
| `n_jobs` | -1 | Gunakan semua core CPU untuk mempercepat training |

### Mengapa Random Forest?
1. **Anti-Overfitting**: Menggunakan metode *ensemble* (200 pohon independen), masing-masing membuat keputusan sendiri lalu hasil akhirnya ditentukan berdasarkan *voting* mayoritas
2. **Robust**: Tidak memerlukan normalisasi fitur dan tahan terhadap noise
3. **Interpretable**: Bisa menampilkan fitur-fitur (kata kunci) yang paling berpengaruh
4. **Fast Training**: Cocok untuk dataset berukuran kecil-menengah seperti milik kami

---

## 📌 Slide 7 — Hasil Evaluasi Model

### Metrik Utama

| Metrik | Skor |
|--------|------|
| **Accuracy** | **99.5%** (193 data testing) |
| **Precision** (macro avg) | 0.99 |
| **Recall** (macro avg) | 1.00 |
| **F1-Score** (macro avg) | 0.99 |

### Apakah Model Ini Overfitting?

**Tidak.** Berikut argumentasinya:

| Aspek | Penjelasan |
|-------|------------|
| **Skor Testing vs Training** | Akurasi 99.5% diukur pada **data testing** (20% data yang disembunyikan saat training). Jika overfitting, skor testing seharusnya jauh lebih rendah dari training |
| **Stratified Split** | Pembagian data menggunakan `stratify=y`, memastikan setiap kategori pekerjaan memiliki proporsi yang sama di data training dan testing |
| **Ensemble Method** | Random Forest menggunakan 200 pohon independen yang saling "mengoreksi", secara alami mencegah overfitting |
| **Balanced Class Weight** | Parameter `class_weight="balanced"` mencegah model bias ke kategori dengan data terbanyak |

### Mengapa Akurasi Sangat Tinggi?

Akurasi 99.5% bukan karena data bocor (*data leakage*), melainkan karena **vocabulary antar kategori pekerjaan di dataset ini sangat distinct** (berbeda nyata). Contoh:

| Kategori | Kata Kunci Dominan |
|----------|-------------------|
| Data Science | python, machine learning, tensorflow, neural network |
| Java Developer | java, spring, hibernate, microservices |
| HR | recruitment, payroll, employee, onboarding |
| Civil Engineer | structural, construction, autocad, concrete |

Perbedaan kosakata yang sangat tajam antar profesi membuat model TF-IDF + Random Forest dapat memisahkan kategori dengan sangat akurat.

---

## 📌 Slide 8 — Sistem Rekomendasi (Job Matching)

### Metode: TF-IDF Cosine Similarity

```
            CV User (Teks)                    110.837 Lowongan LinkedIn
                 │                                     │
                 ▼                                     ▼
        ┌─────────────────┐                  ┌─────────────────┐
        │ TF-IDF Vectorize │                  │ TF-IDF Vectorize │
        └────────┬────────┘                  └────────┬────────┘
                 │                                     │
                 │         ┌─────────────────┐         │
                 └────────→│ Cosine Similarity │←───────┘
                           └────────┬────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ Top 5 Lowongan   │
                           │ dengan Match     │
                           │ Score Tertinggi  │
                           └─────────────────┘
```

### Cara Kerja:
1. Teks CV pengguna dikonversi menjadi vektor numerik menggunakan TF-IDF
2. Seluruh 110.837 deskripsi lowongan LinkedIn juga dikonversi menjadi vektor TF-IDF
3. Dihitung **Cosine Similarity** antara vektor CV dan setiap vektor lowongan
4. 5 lowongan dengan skor kecocokan tertinggi ditampilkan ke pengguna
5. Setiap rekomendasi dilengkapi: judul pekerjaan, nama perusahaan, lokasi, dan link LinkedIn

---

## 📌 Slide 9 — Deployment

### Infrastruktur

| Komponen | Platform |
|----------|----------|
| **Source Code** | [GitHub](https://github.com/lyynx123/CV-Intelligence-Recommender-PJK-GM075) |
| **Live Demo** | [Hugging Face Spaces](https://muzafin-cv-intelligence-recommender.hf.space) |
| **Containerization** | Docker |

### Arsitektur Deployment (Hugging Face Spaces)

```
┌─────────────────────────────────────────────┐
│          Hugging Face Spaces (Docker)         │
│                                               │
│   ┌──────────────┐    ┌───────────────────┐  │
│   │   FastAPI     │    │    Streamlit      │  │
│   │   Backend     │◄───│    Frontend       │  │
│   │   Port 8000   │    │    Port 7860      │  │
│   │   (internal)  │    │    (public)       │  │
│   └──────────────┘    └───────────────────┘  │
│                                               │
│   Dataset + Model tersimpan dalam container   │
└─────────────────────────────────────────────┘
                    │
                    ▼
            Akses Publik via
    https://muzafin-cv-intelligence-recommender.hf.space
```

---

## 📌 Slide 10 — Demo Aplikasi

### Cara Menggunakan:
1. Buka **https://muzafin-cv-intelligence-recommender.hf.space**
2. Upload CV dalam format **PDF**
3. Klik tombol **"🚀 Analisis CV Saya"**
4. Lihat hasil:
   - 🎯 **Prediksi pekerjaan** + confidence score
   - 🛠️ **Skill** yang terdeteksi dari CV
   - 💼 **Top 5 rekomendasi** lowongan kerja LinkedIn
   - 💰 **Estimasi rentang gaji** bulanan

---

## 📌 Slide 11 — Kesimpulan & Pengembangan Selanjutnya

### Kesimpulan
1. ✅ Berhasil membangun sistem rekomendasi pekerjaan berbasis AI yang **end-to-end** (dari upload PDF hingga rekomendasi lowongan)
2. ✅ Model ML mencapai akurasi **99.5%** pada 25 kategori pekerjaan
3. ✅ Sistem rekomendasi mampu mencocokkan CV dengan **110.000+ lowongan** LinkedIn secara real-time
4. ✅ Aplikasi telah berhasil di-deploy secara **publik** di Hugging Face Spaces

### Pengembangan Selanjutnya (Future Work)
| No | Pengembangan | Deskripsi |
|----|-------------|-----------|
| 1 | Memperbanyak dataset CV | Menambah jumlah dan variasi CV untuk meningkatkan generalisasi model |
| 2 | Deep Learning (BERT) | Mengganti TF-IDF + Random Forest dengan model transformer seperti BERT untuk pemahaman konteks lebih baik |
| 3 | Multi-bahasa | Mendukung CV dalam Bahasa Indonesia, bukan hanya Bahasa Inggris |
| 4 | Lowongan real-time | Mengintegrasikan API LinkedIn untuk data lowongan yang selalu terbaru |
| 5 | Feedback loop | Pengguna bisa memberikan rating pada rekomendasi untuk terus meningkatkan akurasi |

---

## 📌 Slide 12 — Tim Pengembang

| Nama | Peran | ID |
|------|-------|----|
| **Ahmad Izzuddin Ulinnuha** | 🔵 Project Leader & AI Integration | APC902D6Y0383 |
| **Azka Nur Fadel** | 🟢 Data Engineer | APC347D6Y0353 |
| **Alif Khusain Bilfaqih** | 🟡 Machine Learning Engineer | APC659D6Y0204 |
| **Muhammad Za'im Shidqi** | 🟠 Backend & API Developer | APC324D6Y0185 |
| **Muhammad Zaenal Arifin** | 🔴 Frontend & UI Developer | APC338D6Y0449 |

---

<p align="center">
  <strong>🎯 CV-Intelligence Recommender</strong><br>
  <em>Upload CV. Temukan Karir. Raih Masa Depan.</em><br><br>
  © 2026 Tim PJK-GM075 — Pijak × IBM SkillsBuild
</p>
