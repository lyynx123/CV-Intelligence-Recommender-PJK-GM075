import streamlit as st
import requests
import json
import time

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="CV-IR | CV-Intelligence Recommender",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS — Premium Dark Theme
# ============================================================
st.markdown("""
<style>
    /* ── Import Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global Styles ── */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ── Main Header ── */
    .main-header {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
    }
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }
    .main-header p {
        font-size: 1.1rem;
        color: #94a3b8;
        font-weight: 300;
    }

    /* ── Upload Area ── */
    .upload-section {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 2px dashed #334155;
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.3s ease;
        margin: 1.5rem 0;
    }
    .upload-section:hover {
        border-color: #667eea;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.15);
    }
    .upload-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .upload-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #e2e8f0;
    }
    .upload-subtitle {
        font-size: 0.9rem;
        color: #64748b;
        margin-top: 0.3rem;
    }

    /* ── Result Cards ── */
    .result-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .result-card:hover {
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    }

    /* ── Prediction Hero Card ── */
    .prediction-hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    .prediction-hero h2 {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    .prediction-hero .confidence {
        color: rgba(255,255,255,0.85);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    .prediction-hero .icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    /* ── Skill Badges ── */
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, #1e3a5f, #1e293b);
        border: 1px solid #334155;
        color: #93c5fd;
        padding: 0.4rem 0.9rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.25rem;
        transition: all 0.2s ease;
    }
    .skill-badge:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white;
        transform: scale(1.05);
    }

    /* ── Job Card ── */
    .job-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
    }
    .job-card:hover {
        border-color: #22d3ee;
        box-shadow: 0 4px 20px rgba(34, 211, 238, 0.1);
    }
    .job-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.3rem;
    }
    .job-company {
        font-size: 0.9rem;
        color: #94a3b8;
    }
    .job-location {
        font-size: 0.85rem;
        color: #64748b;
    }
    .match-score {
        display: inline-block;
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 0.2rem 0.7rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* ── Section Header ── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin: 1.5rem 0 1rem 0;
    }
    .section-header .icon {
        font-size: 1.4rem;
    }
    .section-header h3 {
        font-size: 1.2rem;
        font-weight: 600;
        color: #e2e8f0;
        margin: 0;
    }

    /* ── Stats Row ── */
    .stats-row {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    .stat-card {
        flex: 1;
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #22d3ee, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    .sidebar-header {
        text-align: center;
        padding: 1rem 0;
    }
    .sidebar-header h2 {
        font-size: 1.3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sidebar-info {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.8rem 0;
        font-size: 0.85rem;
        color: #94a3b8;
    }

    /* ── Progress Animation ── */
    .analyzing-animation {
        text-align: center;
        padding: 2rem;
    }
    .analyzing-animation .spinner {
        font-size: 3rem;
        animation: spin 2s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* ── Button Override ── */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }

    /* ── Divider ── */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #334155, transparent);
        margin: 1.5rem 0;
    }

    /* ── Hide Streamlit Defaults ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2>🎯 CV-IR</h2>
        <p style="color: #94a3b8; font-size: 0.85rem;">CV-Intelligence Recommender</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-info">
        <strong>📋 Cara Penggunaan:</strong><br><br>
        1. Upload CV dalam format PDF<br>
        2. Klik tombol "🚀 Analisis CV Saya"<br>
        3. Lihat hasil rekomendasi pekerjaan<br>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-info">
        <strong>🛠️ Tech Stack:</strong><br><br>
        • NLP: spaCy + SBERT<br>
        • ML: Scikit-Learn<br>
        • Backend: FastAPI<br>
        • Frontend: Streamlit<br>
        • PDF: PyMuPDF<br>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0;">
        <p style="color: #64748b; font-size: 0.75rem;">
            Capstone Project PJK-GM075<br>
            Pijak × IBM SkillsBuild
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Backend URL Configuration
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    backend_url = st.text_input(
        "🔗 Backend API URL",
        value="http://localhost:8000",
        help="URL dimana backend FastAPI berjalan"
    )

# ============================================================
# MAIN CONTENT
# ============================================================

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 CV-Intelligence Recommender</h1>
    <p>Upload CV kamu dan dapatkan rekomendasi pekerjaan yang sesuai dengan skill-mu!</p>
</div>
<div class="custom-divider"></div>
""", unsafe_allow_html=True)

# Upload Section
st.markdown("""
<div class="upload-section">
    <div class="upload-icon">📄</div>
    <div class="upload-title">Upload CV Kamu</div>
    <div class="upload-subtitle">Mendukung format PDF • Maksimal 10MB</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload CV (PDF)",
    type=["pdf"],
    label_visibility="collapsed",
    help="Upload CV dalam format PDF. Hanya mendukung PDF digital (bukan hasil scan)."
)

if uploaded_file:
    file_size_mb = uploaded_file.size / (1024 * 1024)
    st.markdown(f"""
    <div class="result-card" style="border-color: #22d3ee;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 1.2rem;">📎</span>
                <strong style="color: #e2e8f0; margin-left: 0.5rem;">{uploaded_file.name}</strong>
            </div>
            <span style="color: #64748b; font-size: 0.85rem;">{file_size_mb:.2f} MB</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Analyze Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_clicked = st.button("🚀 Analisis CV Saya", use_container_width=True, disabled=not uploaded_file)

# ============================================================
# ANALYSIS LOGIC
# ============================================================
if analyze_clicked and uploaded_file:
    # Show analyzing animation
    with st.spinner("🔍 Menganalisis CV kamu... Mohon tunggu sebentar."):
        try:
            # Call backend API
            response = requests.post(
                f"{backend_url}/api/v1/predict",
                files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                timeout=120,
            )

            if response.status_code == 200:
                data = response.json()
            else:
                st.error(f"❌ Error dari server: {response.status_code} — {response.text}")
                data = None

        except requests.exceptions.ConnectionError:
            st.warning("⚠️ Tidak dapat terhubung ke backend. Menampilkan hasil dengan **mode demo**...")
            # Demo/dummy data for when backend isn't running
            data = {
                "extracted_text": "Tidak terhubung ke backend — ini adalah data demo.",
                "skills": ["Python", "Machine Learning", "SQL", "Data Analysis", "TensorFlow",
                           "Pandas", "NumPy", "Deep Learning", "NLP", "Git"],
                "predicted_job": "Data Scientist",
                "confidence": 0.87,
                "salary_estimate": {
                    "min": 8000000,
                    "max": 15000000,
                    "currency": "IDR"
                },
                "job_recommendations": [
                    {
                        "title": "Data Scientist",
                        "company": "Tokopedia",
                        "location": "Jakarta, Indonesia",
                        "link": "https://linkedin.com/jobs/data-scientist-tokopedia",
                        "match_score": 0.94
                    },
                    {
                        "title": "Machine Learning Engineer",
                        "company": "Gojek",
                        "location": "Jakarta, Indonesia",
                        "link": "https://linkedin.com/jobs/ml-engineer-gojek",
                        "match_score": 0.89
                    },
                    {
                        "title": "AI Research Engineer",
                        "company": "Bukalapak",
                        "location": "Bandung, Indonesia",
                        "link": "https://linkedin.com/jobs/ai-engineer-bukalapak",
                        "match_score": 0.85
                    },
                    {
                        "title": "Data Analyst",
                        "company": "Shopee",
                        "location": "Jakarta, Indonesia",
                        "link": "https://linkedin.com/jobs/data-analyst-shopee",
                        "match_score": 0.81
                    },
                    {
                        "title": "NLP Engineer",
                        "company": "Traveloka",
                        "location": "Jakarta, Indonesia",
                        "link": "https://linkedin.com/jobs/nlp-engineer-traveloka",
                        "match_score": 0.78
                    }
                ]
            }
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {str(e)}")
            data = None

    # ============================================================
    # DISPLAY RESULTS
    # ============================================================
    if data:
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # ── Prediction Hero Card ──
        confidence_pct = data["confidence"] * 100
        st.markdown(f"""
        <div class="prediction-hero">
            <div class="icon">🎯</div>
            <h2>{data["predicted_job"]}</h2>
            <div class="confidence">Tingkat Kepercayaan: {confidence_pct:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Stats Row ──
        skills_count = len(data["skills"])
        jobs_count = len(data["job_recommendations"])
        top_match = data["job_recommendations"][0]["match_score"] * 100 if data["job_recommendations"] else 0

        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-value">{skills_count}</div>
                <div class="stat-label">Skill Terdeteksi</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{jobs_count}</div>
                <div class="stat-label">Lowongan Cocok</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{top_match:.0f}%</div>
                <div class="stat-label">Top Match Score</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Two Column Layout ──
        col_left, col_right = st.columns([1, 1])

        # ── Skills Section ──
        with col_left:
            st.markdown("""
            <div class="section-header">
                <span class="icon">🛠️</span>
                <h3>Skill yang Terdeteksi</h3>
            </div>
            """, unsafe_allow_html=True)

            skills_html = ""
            for skill in data["skills"]:
                skills_html += f'<span class="skill-badge">{skill}</span>'

            st.markdown(f"""
            <div class="result-card">
                <div style="line-height: 2.2;">
                    {skills_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Salary Estimate (if available) ──
            if "salary_estimate" in data and data["salary_estimate"]:
                sal = data["salary_estimate"]
                sal_min = sal.get("min", 0)
                sal_max = sal.get("max", 0)
                currency = sal.get("currency", "IDR")

                def format_currency(amount, curr):
                    if curr == "IDR":
                        return f"Rp {amount:,.0f}"
                    return f"${amount:,.0f}"

                st.markdown("""
                <div class="section-header">
                    <span class="icon">💰</span>
                    <h3>Estimasi Gaji</h3>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="result-card">
                    <div style="text-align: center;">
                        <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.5rem;">Rentang Gaji Bulanan</div>
                        <div style="font-size: 1.4rem; font-weight: 700; color: #22d3ee;">
                            {format_currency(sal_min, currency)} — {format_currency(sal_max, currency)}
                        </div>
                        <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.5rem;">
                            Berdasarkan skill dan pengalaman yang terdeteksi
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # ── Job Recommendations Section ──
        with col_right:
            st.markdown("""
            <div class="section-header">
                <span class="icon">💼</span>
                <h3>Rekomendasi Lowongan</h3>
            </div>
            """, unsafe_allow_html=True)

            for i, job in enumerate(data["job_recommendations"]):
                score_pct = job["match_score"] * 100
                score_color = "#10b981" if score_pct >= 85 else "#f59e0b" if score_pct >= 70 else "#ef4444"

                st.markdown(f"""
                <div class="job-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div class="job-title">{job["title"]}</div>
                            <div class="job-company">🏢 {job["company"]}</div>
                            <div class="job-location">📍 {job["location"]}</div>
                        </div>
                        <span class="match-score" style="background: linear-gradient(135deg, {score_color}, {score_color}cc);">
                            {score_pct:.0f}%
                        </span>
                    </div>
                    <div style="margin-top: 0.8rem;">
                        <a href="{job["link"]}" target="_blank"
                           style="color: #667eea; text-decoration: none; font-size: 0.85rem; font-weight: 500;">
                            🔗 Lihat Lowongan →
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # ── Extracted Text Preview ──
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        with st.expander("📝 Preview Teks yang Diekstrak dari CV"):
            st.text(data.get("extracted_text", "Tidak tersedia"))

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="custom-divider"></div>
<div style="text-align: center; padding: 1rem; color: #475569; font-size: 0.8rem;">
    <p>
        <strong>CV-Intelligence Recommender (CV-IR)</strong> v1.0.0<br>
        Capstone Project PJK-GM075 | Pijak × IBM SkillsBuild<br>
        © 2026 Tim PJK-GM075. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)
