title: CV Intelligence Recommender
emoji: 🎯
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false📋 Table of ContentsAbout The ProjectKey FeaturesSystem ArchitectureTech StackFolder StructureInstallation Guide (Windows)How to RunAPI DocumentationDatasetModel PerformanceDevelopment TeamLicense💡 About The ProjectCV-Intelligence Recommender (CV-IR) is an AI-powered application that helps job seekers find the most suitable job opportunities based on their qualifications — simply by uploading a CV in PDF format.🎯 Problem StatementJob seekers waste excessive time and effort manually filtering through job postings that are often irrelevant, while also struggling to determine objective salary expectations based on their CV skills.💊 Our SolutionCV-IR acts as a "painkiller" for job seekers by:Automatically parsing CVs — Text extraction from PDF using PyMuPDFIdentifying skills — 150+ skill keywords + Named Entity Recognition (spaCy)Predicting job roles — Machine Learning classifier (TF-IDF + Random Forest)Recommending job postings — Cosine similarity matching against 110,000+ LinkedIn job listingsProviding salary estimates — Based on job category and skill count (global estimates)✨ Key FeaturesFeatureDescription📄 Upload CV (PDF)Drag & drop or browse CV files in PDF format (max 10MB)🛠️ Skill DetectionAutomatic extraction of technical and non-technical skills from CV text🎯 Job PredictionPrediction across 25 job categories with confidence scores💼 Job RecommendationsTop 5 job openings from LinkedIn dataset with match scores💰 Salary EstimationGlobal salary range estimation based on candidate profile🔗 Direct LinksDirect links to job postings on LinkedIn🌙 Dark Mode UIModern interface with a premium dark theme⚠️ Note: The system currently supports 25 job categories and English CVs only.🏗️ System Architecture┌──────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                  │
│  • Upload CV (PDF)           • Display Skill Badges      │
│  • Display Job Prediction    • Display Recommendations   │
│  • Display Salary Estimate   • Dark Theme Premium        │
└────────────────────────┬─────────────────────────────────┘
                         │ HTTP POST /api/v1/predict
                         ▼
┌──────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                     │
│  • Validate PDF file         • Pipeline orchestration    │
│  • Error handling            • CORS middleware           │
└───┬──────────┬──────────┬──────────┬─────────────────────┘
    │          │          │          │
    ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────────┐
│  PDF   │ │ Skill  │ │  Job   │ │    Job     │
│Extract │→│Extract │→│Predict │ │  Matcher   │
│(PyMuPDF)│ │(spaCy) │ │(RF+    │ │(TF-IDF     │
│        │ │        │ │TF-IDF) │ │Cosine Sim) │
└────────┘ └────────┘ └────────┘ └────────────┘
                                     │
                          ┌──────────▼────────────┐
                          │  Dataset LinkedIn Jobs│
                          │  (110,000+ listings)  │
                          └───────────────────────┘
🛠️ Tech StackLayerTechnologyUsageFrontendStreamlitInteractive web interfaceBackendFastAPI + UvicornREST API serverPDF ParsingPyMuPDF (fitz)Text extraction from PDFNLP / NERspaCy (en_core_web_sm)Named Entity RecognitionML ClassifierScikit-Learn (Random Forest)Job category predictionFeature EngineeringTF-IDF VectorizerText representation as numerical featuresJob MatchingCosine Similarity (TF-IDF)Matching CVs with job postingsData ProcessingPandas, NumPyData manipulation and analysisVersion ControlGit + GitHub + Git LFSCollaboration, versioning, and large file storage📁 Folder StructureCV-Intelligence-Recommender-PJK-GM075/
├── 📂 backend/
│   ├── main.py                     # FastAPI entry point
│   ├── routers/
│   │   └── predict.py             # Endpoint POST /api/v1/predict
│   └── modules/
│       ├── pdf_extractor.py       # Text extraction from PDF
│       ├── skill_extractor.py     # Skill detection (150+ keywords + NER)
│       ├── job_matcher.py         # TF-IDF cosine similarity matching
│       └── job_predictor.py       # Random Forest job classifier
│
├── 📂 frontend/
│   └── app.py                     # Streamlit UI (premium dark theme)
│
├── 📂 data/
│   ├── raw/                       # Raw dataset from Kaggle
│   │   ├── UpdatedResumeDataSet.csv
│   │   └── postings.csv           # 123,849 LinkedIn job postings
│   └── processed/
│       └── job_listings.csv       # 110,837 cleaned job postings (via Git LFS)
│
├── 📂 models/
│   ├── job_classifier.pkl         # Trained Random Forest model (via Git LFS)
│   └── tfidf_vectorizer.pkl       # Trained TF-IDF vectorizer (via Git LFS)
│
├── 📂 notebooks/
│   ├── 01_preprocess_data.py      # Dataset preprocessing script
│   └── 02_train_model.py          # ML model training script
│
├── 📂 tests/
│   └── test_predict.py            # Unit tests (pytest)
│
├── 📂 .streamlit/
│   └── config.toml                # Streamlit configuration (max upload 10MB)
│
├── Dockerfile                     # Docker configuration (Hugging Face Spaces)
├── start.sh                       # Docker startup script
├── requirements.txt               # Python dependencies
└── README.md                      # Documentation (this file)
🚀 Installation Guide (Windows)✅ Tested on Windows 10/11 with Python 3.10+PrerequisitesBefore starting, ensure you have installed:SoftwareVersionDownload LinkPython3.10 or newerpython.org/downloadsGitLatestgit-scm.comGit LFSLatestgit-lfs.github.com⚠️ Important during Python installation: Check the "Add Python to PATH" option at the start of installation!Option A — Download via Git Clone (Recommended)Using PowerShell or Command Prompt:PowerShell# 1. Enable Git LFS (required so model files are downloaded properly)
git lfs install

# 2. Clone the repository
git clone https://github.com/lyynx123/CV-Intelligence-Recommender-PJK-GM075.git

# 3. Navigate into the project folder
cd CV-Intelligence-Recommender-PJK-GM075

# 4. Create a virtual environment
python -m venv venv

# 5. Activate the virtual environment
.\venv\Scripts\activate

# 6. Install all dependencies
pip install -r requirements.txt

# 7. Download spaCy language model
python -m spacy download en_core_web_sm
Option B — Download via ZIPIf you do not use Git, you can download directly from GitHub:Open the repo page: github.com/lyynx123/CV-Intelligence-Recommender-PJK-GM075Click the Code button → Download ZIPExtract the ZIP into your directory of choiceOpen PowerShell inside the extracted directory⚠️ Important note for ZIP downloads: Model files (.pkl) and datasets are managed via Git LFS and are not included in standard ZIP downloads. You will need to retrain the model after installation, or use Option A (Git Clone) to get pre-trained weights.PowerShell# Inside the extracted ZIP directory:

# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
.\venv\Scripts\activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Download spaCy language model
python -m spacy download en_core_web_sm

# 5. (ZIP download only) Run preprocessing and retrain the model
python notebooks/01_preprocess_data.py
python notebooks/02_train_model.py
Windows Installation Troubleshooting❌ Error: python is not recognizedPowerShell# Try using 'py' instead of 'python'
py -m venv venv
py -m spacy download en_core_web_sm
❌ Error: .\venv\Scripts\activate cannot be loaded (Execution Policy)PowerShell# Run this command first, then try activating again
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
❌ Error during pip install (SSL / timeout)PowerShell# Use a more stable pip mirror or increase timeout
pip install -r requirements.txt -i https://pypi.org/simple/ --timeout=120
❌ Error: No module named 'backend'PowerShell# Ensure you are running the command from the root folder of the project (not a subfolder)
# Correct example:
cd CV-Intelligence-Recommender-PJK-GM075
uvicorn backend.main:app --port 8000
❌ Error: .pkl model file not foundPowerShell# If downloaded via ZIP, run model retraining:
python notebooks/02_train_model.py
# Or re-clone using Git + Git LFS (Option A)
🖥️ How to RunAfter installation, open two terminals simultaneously:Terminal 1 — Run BackendPowerShell# Activate virtual environment
.\venv\Scripts\activate

# Run FastAPI server
uvicorn backend.main:app --port 8000
Wait until you see: Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000)Terminal 2 — Run FrontendPowerShell# Activate virtual environment
.\venv\Scripts\activate

# Run Streamlit app
streamlit run frontend/app.py --server.port 8501
Accessing the ApplicationServiceURL🎯 Frontend (Main App)http://localhost:8501⚡ Backend APIhttp://localhost:8000📚 API Docs (Swagger)http://localhost:8000/docsHow to UseOpen http://localhost:8501 in your browserUpload CV in PDF format (max 10MB, English CVs only)Click the "🚀 Analyze My CV" buttonView results:🎯 Job prediction + confidence score (from 25 categories)🛠️ Extracted skills💼 Top 5 recommended job postings💰 Global salary range estimate📡 API DocumentationPOST /api/v1/predictUpload a PDF CV and receive a full analysis.Request:Bashcurl -X POST http://localhost:8000/api/v1/predict \
  -F "file=@path/to/cv.pdf"
Response:JSON{
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
📊 DatasetDatasetSourceData CountPurposeUpdated Resume DatasetKaggle962 resumes, 25 categoriesClassifier model trainingLinkedIn Job PostingsKaggle123,849 postingsJob matching & recommendations25 Supported Job Categories#Category1Java Developer2Testing3DevOps Engineer4Python Developer5Web Designing6HR7Hadoop8Data Science9Mechanical Engineer#Category10Sales11Operations Manager12ETL Developer13Blockchain14Arts15Database16Health and Fitness17Electrical Engineering#Category18PMO19Business Analyst20DotNet Developer21Automation Testing22Network Security Engineer23Civil Engineer24SAP Developer25Advocate📈 Model PerformanceModel trained using TF-IDF + Random Forest on 962 resumes across 25 categories.MetricScoreAccuracy99.5%Precision (macro avg)0.99Recall (macro avg)1.00F1-Score (macro avg)0.99MethodologyCV Text → Text Cleaning → TF-IDF Vectorization → Random Forest → Predicted Job Category
           (lowercase,      (5000 features,        (200 trees,
            remove URLs,     bigrams)               balanced weights)
            remove special
            chars)
🧪 TestingPowerShell# Activate virtual environment first
.\venv\Scripts\activate

# Run all unit tests
pytest tests/ -v --tb=short

# Run specific test
pytest tests/test_predict.py -v
👥 Development Team📄 LicenseThis project was developed as part of the Capstone Project for the Pijak in collaboration with IBM SkillsBuild program.Theme: AI for Smart Recommendation Systems
