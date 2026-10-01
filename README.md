---
title: CV Intelligence Recommender
emoji: 🎯
colorFrom : blue
colorTo : purple
SDK : Docker
pinned: false
---
<p align =" center ">
< img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
< img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt=" FastAPI ">
< img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt=" Streamlit ">
< img src ="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-learn">
< img src="https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white" alt=" spaCy ">
</p>

<h1 align=" center "> 🎯 CV-Intelligence Recommender</h1>

<p align =" center ">
<strong> System Recommendation Work AI -Based — Just Upload CV, Get Career Your dream !</strong>
</p>

<p align =" center ">
< em >Capstone Project PJK-GM075 | Step × IBM SkillsBuild </ em >
</p>

---

## 📋 Table of Contents

- [ About Project ](#-about-project)
- [Main Features](#-main-features)
- [ Architecture System ](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [ Folder Structure ](#-folder-structure)
- [How to Install (Windows)](#-how-to-install-windows)
- [How to Run ](#-how-to-run)
- [API Documentation](#-api-documentation)
- [Dataset](#-dataset)
- [Model Performance](#-model-performance)
- [Development Team](#-development-team)
- [ License ](#-license)

---

## 💡 About Project

**CV-Intelligence Recommender (CV-IR)** is application AI- based that helps seeker Work find the most suitable job with qualification they — only with upload CV in PDF format.

### 🎯 Problems Solved

> * Seeker Work throw away too Lots time and energy For filter vacancy manually which is often No relevant , and difficulty determine expectation objective salary based on competencies on their CV.*

### 💊 Our Solution

CV-IR acts as a **"painkiller"** for seeker Work with :

1. ** Read the CV thoroughly automatic ** — Extraction text from PDF using PyMuPDF
2. ** Identifying skills** — 150+ skill keywords + Named Entity Recognition ( spaCy )
3. ** Predict suitable job ** — Machine Learning classifier ( TF-IDF + Random Forest)
4. ** Recommend ** jobs — Cosine similarity matching against 110,000+ LinkedIn jobs
5. ** Give estimate salary ** — Based on category jobs and number of skills ( global estimate )

---

## ✨ Key Features

| Features | Description |
|-------|-----------|
| 📄 **Upload CV (PDF)** | Drag & drop or browse CV files in PDF format ( max . 10MB) |
| 🛠️ **Skill Detection** | Detection automatic technical and non- technical skills from CV text |
| 🎯 **Job Prediction** | Prediction from 25 categories work with confidence score |
| 💼 **Job Recommendations** | Top 5 vacancies Work from LinkedIn dataset with match score |
| 💰 **Salary Estimation** | Estimate range **global** salary based on profile |
| 🔗 **Direct Links** | Direct links to post a job on LinkedIn |
| 🌙 **Dark Mode UI** | Modern interface with premium dark theme |

> ⚠️ ** Note :** System moment This only supports **25 categories job ** and **English CV ** .

---

## 🏗️ Architecture System

```
┌──────────────────────────────────────────────────┐
│ FRONTEND ( Streamlit ) │
│ • Upload CV (PDF) • Display Skill Badges │
│ • Show Prediction Jobs • Showcase Recommendations │
│ • Show Estimate Salary • Dark Theme Premium │
└─────────────────────────────────────────────────────┘
│ HTTP POST / api /v1/predict
                         ▼
┌──────────────────────────────────────────────────┐
│ BACKEND ( FastAPI ) │
│ • Validation of PDF files • Pipeline orchestration │
│ • Error handling • CORS middleware │
└─── ┬ ─────────── ┬ ───────────── ┬ ────────────────────────────────┘
│ │ │ │
    ▼          ▼          ▼          ▼
┌────────┐ ┌───────┐ ┌─────────┐ ┌──────────┐
│ PDF │ │ Skills │ │ Job │ │ Job │
│Extract │→│Extract │→│Predict │ │ Matcher │
│( PyMuPDF )│ │( spaCy ) │ │(RF+ │ │(TF-IDF │
│ │ │ │ │TF-IDF)│ │Cosine Sim) │
└────────┘ └────────┘ └─────────┘ └────────────┘
│
┌─────────── ▼ ───────────┐
│ LinkedIn Jobs Dataset │
│ (110,000+ vacancies ) │
└────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Uses |
|-------|-----------|----------|
| **Frontend** | Streamlit | Interactive web interface |
| **Backend** | FastAPI + Uvicorn | REST API servers |
| **PDF Parsing** | PyMuPDF (` fitz `) | Extraction text from PDF |
| **NLP / NER** | spaCy (` en_core_web_sm `) | Named Entity Recognition |
| **ML Classifier** | Scikit-Learn (Random Forest) | Prediction category job |
| **Engineering Features** | TF-IDF Vectorizer | Representation text as feature numeric |
| **Job Matching** | Cosine Similarity (TF-IDF) | CV Matching with vacancies |
| **Data Processing** | Pandas, NumPy | Data manipulation and analysis |
| **Version Control** | Git + GitHub + Git LFS | Collaboration , versioning, and large file storage |

---

## 📁 Folder Structure

```
CV-Intelligence-Recommender-PJK-GM075/
├ ── 📂 backend/
│ ├ ── main.py # FastAPI entry point
│ ├ ── routers/
│ │ └── predict.py # Endpoint POST / api /v1/predict
│ └── modules/
│ ├ ── pdf_extractor.py # Extraction text from PDF
│ ├ ── skill_extractor.py # Skill detection (150+ keywords + NER)
│ ├ ── job_matcher.py # TF-IDF cosine similarity matching
│ └── job_predictor.py # Random Forest job classifier
│
├ ── 📂 frontend/
│ └── app.py # Streamlit UI (dark theme premium)
│
├ ── 📂 data/
│ ├ ── raw/ # Raw dataset from Kaggle
│ │ ├ ── UpdatedResumeDataSet.csv
│ │ └── postings.csv # 123,849 LinkedIn job postings
│ └── processed/
│ └── job_listings.csv # 110,837 vacancies clean (via Git LFS)
│
├ ── 📂 models/
│ ├ ── job_classifier.pkl # Trained Random Forest model (via Git LFS)
│ └── tfidf_vectorizer.pkl # Trained TF-IDF vectorizer (via Git LFS)
│
├ ── 📂 notebooks/
│ ├ ── 01_preprocess_data.py # Dataset preprocessing script
│ └── 02_train_model.py # ML model training script
│
├ ── 📂 tests/
│ └── test_predict.py # Unit tests ( pytest )
│
├ ── 📂 . streamlit /
│ └── config.toml # Configuration Streamlit (max upload 10MB)
│
├ ── Dockerfile # Docker Configuration (Hugging Face Spaces)
├ ── start.sh # Docker startup script
├ ── requirements.txt # Python dependencies
└── README.md # Documentation ( this file )
```

---

## 🚀 How to Install (Windows)

> ✅ ** Tested on Windows 10/11 with Python 3.10+ **

### Prerequisites

Before start , make sure you have install :

| Software | Version | Download Link |
|----------|-------|---------------|
| **Python** | 3.10 or more new | [python.org/downloads](https://www.python.org/downloads/) |
| **Git** | Latest | [git-scm.com](https://git-scm.com/downloads) |
| **Git LFS** | Latest | [git-lfs.github.com](https://git-lfs.github.com/) |

> ⚠️ ** Important when installing Python:** Check **"Add Python to PATH"** option at the beginning installation !

---

### Option A — Download via Git Clone ( Recommended )

Use **PowerShell** or **Command Prompt**:

``` powershell
# 1. Enable Git LFS ( mandatory , so that the model files are included) downloaded )
git lfs install

# 2. Clone repository
git clone https://github.com/lyynx123/CV-Intelligence-Recommender-PJK-GM075.git

# 3. Go to the project folder
cd CV-Intelligence-Recommender-PJK-GM075

# 4. Create a virtual environment
python -m venv venv

# 5. Activate the virtual environment
.\ venv \Scripts\activate

# 6. Install all dependencies
pip install -r requirements. txt

# 7. Download the language model spaCy
python -m spacy download en_core_web_sm
```

---

### Option B — Download via ZIP

If you don't using Git, can download directly from GitHub:

1. Go to the repo page : [github.com/lyynx123/CV-Intelligence-Recommender-PJK-GM075](https://github.com/lyynx123/CV-Intelligence-Recommender-PJK-GM075)
2. Click **Code** button → **Download ZIP**
3. Extract the ZIP to a folder of your choice
4. Open **PowerShell** in the results folder extract the

> ⚠️ ** Note important for ZIP:** Model files (`. pkl` ) and datasets are stored via **Git LFS** and ** not follow downloaded ** if using regular ZIP . you need operate re- training after installation, or use ** Option A (Git Clone)** to get the model straight away available .

``` powershell
# After enter to the results folder ZIP extract :

# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
.\ venv \Scripts\activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Download the language model spaCy
python -m spacy download en_core_web_sm

# 5. (Only if downloaded ZIP) Run preprocessing and retraining
python notebooks/01_preprocess_data.py
python notebooks/02_train_model.py
```

---

### Troubleshooting Windows Installation

** ❌ Error: `python` is not recognized **
``` powershell
# Try using ' py ' as substitute for 'python'
py -m venv venv
py -m spacy download en_core_web_sm
```

** ❌ Error: `.\ venv \Scripts\activate` did not work Can executed (Execution Policy)**
``` powershell
# Run order This moreover first , then try Again
Set- ExecutionPolicy - ExecutionPolicy RemoteSigned -Scope CurrentUser
```

** ❌ Error during `pip install` (SSL / timeout)**
``` powershell
# Use more pip mirrors stable
pip install -r requirements.txt - i https://pypi.org/simple/ --timeout=120
```

** ❌ Error: `No module named 'backend'`**
``` powershell
# Make sure you run order from the project root folder ( not from subfolder)
# Correct example :
cd CV-Intelligence-Recommender-PJK-GM075
uvicorn backend.main:app --port 8000
```

** ❌ Error: Model `. pkl` does not exist found **
``` powershell
# If downloaded via ZIP, run the training again :
python notebooks/02_train_model.py
# Or re -clone using Git + Git LFS ( Option A)
```

---

## 🖥️ How to Run

After installation finished , open **two terminals** simultaneously simultaneously :

### Terminal 1 — Run Backend

``` powershell
# Activate virtual environment
.\ venv \Scripts\activate

# Run the FastAPI server
uvicorn backend.main:app --port 8000
```

Wait until appear message : ` Uvicorn running on http://127.0.0.1:8000`

### Terminal 2 — Run Frontend

``` powershell
# Activate virtual environment
.\ venv \Scripts\activate

# Run application Streamlit
streamlit run frontend/app.py -- server.port 8501
```

### Access Application in Browser

| Service | URL |
|---------|-----|
| 🎯 **Frontend ( Main Application )** | [http://localhost:8501](http://localhost:8501) |
| ⚡ **Backend API** | [http://localhost:8000](http://localhost:8000) |
| 📚 **API Docs (Swagger)** | [http://localhost:8000/docs](http://localhost:8000/docs) |

### How to use

1. Open **http://localhost:8501** in a browser
2. **Upload CV** in PDF format ( max . 10MB, English CV only )
3. Click **" button 🚀 My CV Analysis "**
4. Look results :
- 🎯 Prediction job + confidence score ( from 25 categories )
- 🛠️ Detected skills
- 💼 Top 5 recommendations vacancy Work
- 💰 Estimate range global salary

---

## 📡 API Documentation

### `POST / api /v1/predict`

Upload your CV in PDF format and get analysis complete .

**Request:**

```bash
curl -X POST http://localhost:8000/api/v1/predict\
-F "file=@path/to/cv.pdf"
```

**Response:**

``` json
{
" extracted _text ": "John Doe Software Engineer with 5 years...",
"skills": ["Python", "Machine Learning", "SQL", "TensorFlow", "Docker"],
" predicted _job ": "Data Science",
"confidence": 0.8734,
" salary _estimate ": {
"min": 12000000,
"max": 27000000,
"currency": "IDR"
},
" job _recommendations ": [
{
"title": "Data Scientist",
"company": "Tech Corp",
"location": "Jakarta, Indonesia",
"link": "https://www.linkedin.com/jobs/view/12345",
" match _score ": 0.8912
}
]
}
```

---

## 📊 Dataset

| Dataset | Source | Amount of Data | Use |
|---------|--------|-------------|----------|
| **Updated Resume Dataset** | [Kaggle](https://www.kaggle.com/datasets/jillanisofttech/updated-resume-dataset) | 962 resumes, 25 categories | Classifier model training |
| **LinkedIn Job Postings** | [Kaggle](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings) | 123,849 posts | Job matching & recommendations |

### 25 Categories Supported Work

<table>
<tr>
<td>

| # | Category |
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

| # | Category |
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

| # | Category |
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

## 📈 Model Performance

Model trained using **TF-IDF + Random Forest** on 962 resumes with 25 categories .

| Metrics | Score |
|--------|------|
| **Accuracy** | **99.5%** |
| **Precision** (macro avg ) | 0.99 |
| **Recall** (macro avg ) | 1.00 |
| **F1-Score** (macro avg ) | 0.99 |

### Methodology

```
CV Text → Text Cleaning → TF-IDF Vectorization → Random Forest → Predicted Job Category
( lowercase , (5000 features, (200 trees,
remove URLs, bigrams) balanced weights)
remove special
chars)
```

---

## 🧪 Testing

``` powershell
# Activate the virtual environment first formerly
.\ venv \Scripts\activate

# Run all unit tests
pytest tests/ -v --tb=short

# Specific test
pytest tests/test_predict.py -v
```

---

## 👥 Development Team

<table>
<tr>
< td align =" center ">
<strong>Ahmad Izzuddin Ulinnuha</strong>< br >
<sub> 🔵 Project Leader & AI Integration</sub>< br >
<sub>APC902D6Y0383</sub>
</td>
< td align =" center ">
<strong>Azka Nur Fadel</strong>< br >
<sub> 🟢 Data Engineer</sub>< br >
<sub>APC347D6Y0353</sub>
</td>
< td align =" center ">
<strong>Alif Khusain Bilfaqih</strong>< br >
<sub> 🟡 Machine Learning Engineer</sub>< br >
<sub>APC659D6Y0204</sub>
</td>
</tr>
<tr>
< td align =" center ">
Muhammad Za'im Shidqi </strong>< br >
<sub> 🟠 Backend & API Developer</sub>< br >
<sub>APC324D6Y0185</sub>
</td>
< td align =" center ">
<strong>Muhammad Zaenal Arifin</strong>< br >
<sub> 🔴 Frontend & UI Developer</sub>< br >
<sub>APC338D6Y0449</sub>
</td>
< td align =" center ">
</td>
</tr>
</table>

---

## 📄 License

Project This developed as part from the **Capstone Project** program ** Pijak in collaboration with IBM SkillsBuild **.

**Theme**: AI for Smart Recommendation Systems

---

<p align =" center ">
<strong> 🎯 CV-Intelligence Recommender (CV-IR)</strong>< br >
Upload CV . Find Career . Achieve the Future .</ em >< br >< br >
<sub>© 2026 PJK-GM075 Team — Pijak × IBM SkillsBuild </sub>
</p>
