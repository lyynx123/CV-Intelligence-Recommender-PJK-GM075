import os
import tempfile
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.modules.pdf_extractor import extract_text_from_bytes
from backend.modules.skill_extractor import extract_skills
from backend.modules.job_matcher import match_jobs
from backend.modules.job_predictor import predict_job_from_text

router = APIRouter()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint utama: menerima file PDF CV, mengekstrak teks,
    mengidentifikasi skill, memprediksi pekerjaan, dan memberikan rekomendasi.
    """
    # ── Validasi tipe file ──
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Hanya file PDF yang diterima. Silakan upload file dengan ekstensi .pdf"
        )

    # ── Validasi ukuran file (max 10MB) ──
    contents = await file.read()
    max_size = 10 * 1024 * 1024  # 10MB
    if len(contents) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"Ukuran file terlalu besar ({len(contents) / 1024 / 1024:.1f}MB). Maksimal 10MB."
        )

    try:
        # ── 1. Ekstraksi Teks dari PDF ──
        text = extract_text_from_bytes(contents)

        if not text or len(text) < 50:
            raise HTTPException(
                status_code=422,
                detail="Teks yang diekstrak terlalu pendek. Pastikan PDF bukan hasil scan (gambar)."
            )

        # ── 2. Ekstraksi Skill ──
        skills = extract_skills(text)

        # ── 3. Prediksi Pekerjaan (gunakan teks CV penuh, bukan hanya skill) ──
        job_pred = predict_job_from_text(text)

        # ── 4. Rekomendasi Lowongan ──
        recommendations = match_jobs(text, top_k=5)

        # ── 5. Estimasi Gaji (placeholder — bisa diganti model regresi) ──
        salary_estimate = _estimate_salary(job_pred["predicted_job"], skills)

        # ── Response ──
        return {
            "extracted_text": text[:500] + ("..." if len(text) > 500 else ""),
            "skills": skills,
            "predicted_job": job_pred["predicted_job"],
            "confidence": job_pred["confidence"],
            "salary_estimate": salary_estimate,
            "job_recommendations": recommendations,
        }

    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Terjadi kesalahan internal: {str(e)}"
        )


def _estimate_salary(predicted_job: str, skills: list[str]) -> dict:
    """
    Estimasi gaji sederhana berdasarkan pekerjaan dan jumlah skill.
    (Placeholder — bisa diganti dengan model regresi XGBoost)
    """
    # Base salary ranges per job category (IDR/month)
    salary_ranges = {
        "Data Science": {"min": 10_000_000, "max": 25_000_000},
        "Data Scientist": {"min": 10_000_000, "max": 25_000_000},
        "Java Developer": {"min": 8_000_000, "max": 20_000_000},
        "Python Developer": {"min": 8_000_000, "max": 22_000_000},
        "Web Designing": {"min": 6_000_000, "max": 15_000_000},
        "DevOps Engineer": {"min": 12_000_000, "max": 28_000_000},
        "Testing": {"min": 7_000_000, "max": 18_000_000},
        "HR": {"min": 6_000_000, "max": 15_000_000},
        "Sales": {"min": 5_000_000, "max": 15_000_000},
        "Mechanical Engineer": {"min": 7_000_000, "max": 18_000_000},
        "Blockchain": {"min": 12_000_000, "max": 30_000_000},
        "Database": {"min": 8_000_000, "max": 20_000_000},
        "Hadoop": {"min": 10_000_000, "max": 25_000_000},
        "ETL Developer": {"min": 9_000_000, "max": 22_000_000},
        "DotNet Developer": {"min": 8_000_000, "max": 20_000_000},
        "Automation Testing": {"min": 8_000_000, "max": 20_000_000},
        "Network Security Engineer": {"min": 10_000_000, "max": 25_000_000},
        "SAP Developer": {"min": 10_000_000, "max": 28_000_000},
        "Civil Engineer": {"min": 7_000_000, "max": 18_000_000},
        "Arts": {"min": 5_000_000, "max": 12_000_000},
        "Electrical Engineering": {"min": 7_000_000, "max": 18_000_000},
        "Health and Fitness": {"min": 5_000_000, "max": 15_000_000},
        "PMO": {"min": 10_000_000, "max": 25_000_000},
        "Business Analyst": {"min": 8_000_000, "max": 22_000_000},
        "Operations Manager": {"min": 10_000_000, "max": 25_000_000},
        "Advocate": {"min": 8_000_000, "max": 25_000_000},
    }

    # Find best match
    default_range = {"min": 7_000_000, "max": 18_000_000}
    salary = default_range

    predicted_lower = predicted_job.lower()
    for key, value in salary_ranges.items():
        if key.lower() in predicted_lower or predicted_lower in key.lower():
            salary = value
            break

    # Adjust based on skill count
    skill_bonus = min(len(skills) * 500_000, 5_000_000)
    salary["min"] += skill_bonus
    salary["max"] += skill_bonus

    return {
        "min": salary["min"],
        "max": salary["max"],
        "currency": "IDR",
    }
