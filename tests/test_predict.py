"""
Unit Tests untuk CV-IR API
"""
import io
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "running" in data["status"].lower() or "🚀" in data["status"]


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_invalid_file_type():
    """Test that non-PDF files are rejected."""
    fake_txt = io.BytesIO(b"ini bukan PDF")
    response = client.post(
        "/api/v1/predict",
        files={"file": ("cv.txt", fake_txt, "text/plain")},
    )
    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


def test_predict_invalid_file_extension():
    """Test that files without .pdf extension are rejected."""
    fake_doc = io.BytesIO(b"some content")
    response = client.post(
        "/api/v1/predict",
        files={"file": ("cv.docx", fake_doc, "application/octet-stream")},
    )
    assert response.status_code == 400


def test_predict_valid_pdf_structure():
    """Test the response structure with a minimal valid PDF."""
    # Create a minimal valid PDF
    minimal_pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>endobj\n"
        b"xref\n0 4\n"
        b"0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"trailer<</Size 4/Root 1 0 R>>\n"
        b"startxref\n212\n%%EOF"
    )

    response = client.post(
        "/api/v1/predict",
        files={"file": ("cv.pdf", io.BytesIO(minimal_pdf), "application/pdf")},
    )
    # This might return 422 because the PDF has no text,
    # which is the expected behavior
    assert response.status_code in [200, 422]


# ── Module Tests ──

def test_pdf_extractor():
    """Test PDF text cleaning function."""
    from backend.modules.pdf_extractor import clean_text

    raw = "  Hello   World  \n\n  Test   "
    cleaned = clean_text(raw)
    assert "Hello" in cleaned
    assert "World" in cleaned
    assert "  " not in cleaned  # No double spaces


def test_skill_extractor():
    """Test skill extraction from text."""
    from backend.modules.skill_extractor import extract_skills

    text = "I am proficient in Python, Machine Learning, and SQL. I use TensorFlow and Pandas."
    skills = extract_skills(text)
    assert "Python" in skills
    assert "Machine Learning" in skills
    assert "SQL" in skills
    assert "TensorFlow" in skills
    assert "Pandas" in skills


def test_skill_extractor_empty():
    """Test skill extraction with irrelevant text."""
    from backend.modules.skill_extractor import extract_skills

    text = "I like to eat pizza and watch movies."
    skills = extract_skills(text)
    # Should return empty or very few skills
    assert isinstance(skills, list)
