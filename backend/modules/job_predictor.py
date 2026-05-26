import os
import re
import joblib

# ============================================================
# Model paths
# ============================================================
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_MODEL_DIR = os.path.join(_BASE_DIR, "models")
_CLASSIFIER_PATH = os.path.join(_MODEL_DIR, "job_classifier.pkl")
_VECTORIZER_PATH = os.path.join(_MODEL_DIR, "tfidf_vectorizer.pkl")

# Cached models
_classifier = None
_vectorizer = None


def _load_models():
    """Load the trained classifier and vectorizer."""
    global _classifier, _vectorizer

    if _classifier is not None and _vectorizer is not None:
        return

    if not os.path.exists(_CLASSIFIER_PATH):
        raise FileNotFoundError(
            f"Job classifier model not found at: {_CLASSIFIER_PATH}\n"
            f"Please run the training script first: python notebooks/02_train_model.py"
        )
    if not os.path.exists(_VECTORIZER_PATH):
        raise FileNotFoundError(
            f"TF-IDF vectorizer not found at: {_VECTORIZER_PATH}\n"
            f"Please run the training script first: python notebooks/02_train_model.py"
        )

    print("Loading job prediction models...")
    _classifier = joblib.load(_CLASSIFIER_PATH)
    _vectorizer = joblib.load(_VECTORIZER_PATH)
    print("Job prediction models loaded successfully.")


def _clean_resume_text(text: str) -> str:
    """
    Clean resume text EXACTLY the same way as during training.
    This is critical — any mismatch causes wrong predictions.
    """
    if not isinstance(text, str):
        return ""
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove special characters
    text = re.sub(r'[^\w\s]', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()


def predict_job_title(skills: list[str]) -> dict:
    """
    Prediksi dari list skill.
    """
    _load_models()
    skill_text = " ".join(skills)
    clean_text = _clean_resume_text(skill_text)

    X = _vectorizer.transform([clean_text])
    prediction = _classifier.predict(X)[0]

    try:
        probabilities = _classifier.predict_proba(X)[0]
        confidence = float(max(probabilities))
    except AttributeError:
        confidence = 0.75

    return {
        "predicted_job": str(prediction),
        "confidence": round(confidence, 4),
    }


def predict_job_from_text(resume_text: str) -> dict:
    """
    Prediksi dari teks CV penuh — lebih akurat karena lebih banyak konteks.
    Teks di-clean dengan cara yang SAMA persis seperti saat training.
    """
    _load_models()

    # CRITICAL: Clean text the same way as training
    clean_text = _clean_resume_text(resume_text)

    X = _vectorizer.transform([clean_text])
    prediction = _classifier.predict(X)[0]

    try:
        probabilities = _classifier.predict_proba(X)[0]
        confidence = float(max(probabilities))
    except AttributeError:
        confidence = 0.75

    return {
        "predicted_job": str(prediction),
        "confidence": round(confidence, 4),
    }
