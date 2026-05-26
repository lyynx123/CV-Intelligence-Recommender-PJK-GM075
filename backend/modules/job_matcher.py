import os
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
# Cached state — computed once, reused on every request
# ============================================================
_jobs_df = None
_tfidf_vectorizer = None
_job_tfidf_matrix = None


def _clean_text(text: str) -> str:
    """Clean text for matching."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()


def _find_job_dataset() -> str:
    """Find the job listings dataset."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    possible_paths = [
        os.path.join(base_dir, "data", "processed", "job_listings.csv"),
        os.path.join(base_dir, "data", "job_listings.csv"),
        os.path.join(base_dir, "data", "raw", "job_postings.csv"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        f"Job listings dataset not found. Checked: {possible_paths}"
    )


def _load_and_cache_jobs():
    """Load dataset and pre-compute TF-IDF matrix ONCE (very fast)."""
    global _jobs_df, _tfidf_vectorizer, _job_tfidf_matrix

    if _jobs_df is not None and _job_tfidf_matrix is not None:
        return

    path = _find_job_dataset()
    print(f"Loading job dataset from: {path}")

    df = pd.read_csv(path)
    df.columns = df.columns.str.lower().str.strip()

    # Ensure required columns
    df["title"] = df.get("title", pd.Series(["Unknown"] * len(df))).fillna("Unknown Position")
    df["description"] = df.get("description", pd.Series([""] * len(df))).fillna("")
    df["company"] = df.get("company", pd.Series(["N/A"] * len(df))).fillna("N/A")
    df["location"] = df.get("location", pd.Series(["N/A"] * len(df))).fillna("N/A")
    df["link"] = df.get("link", pd.Series(["#"] * len(df))).fillna("#")

    # Drop empty descriptions
    df = df[df["description"].str.len() > 20].reset_index(drop=True)

    # Use ALL data — TF-IDF is fast enough to handle 10k+ rows
    _jobs_df = df

    # Clean descriptions for matching
    clean_descriptions = df["description"].apply(_clean_text).tolist()

    # Build TF-IDF matrix (very fast — seconds, not minutes)
    print(f"Building TF-IDF matrix for {len(df)} jobs...")
    _tfidf_vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words="english",
        min_df=2,
        max_df=0.95,
    )
    _job_tfidf_matrix = _tfidf_vectorizer.fit_transform(clean_descriptions)
    print(f"Job matching ready! ({len(df)} jobs indexed)")


def match_jobs(cv_text: str, top_k: int = 5, dataset_path: str = None) -> list[dict]:
    """
    Mencocokkan CV dengan daftar lowongan menggunakan TF-IDF cosine similarity.
    Sangat cepat — hanya butuh <1 detik per request.
    """
    _load_and_cache_jobs()

    # Clean and vectorize CV text
    clean_cv = _clean_text(cv_text)
    cv_vector = _tfidf_vectorizer.transform([clean_cv])

    # Compute cosine similarity against all jobs
    scores = cosine_similarity(cv_vector, _job_tfidf_matrix)[0]

    # Get top-K indices
    actual_k = min(top_k, len(_jobs_df))
    top_indices = scores.argsort()[-actual_k:][::-1]

    results = []
    for idx in top_indices:
        row = _jobs_df.iloc[idx]
        results.append({
            "title": str(row.get("title", "Unknown")),
            "company": str(row.get("company", "N/A")),
            "location": str(row.get("location", "N/A")),
            "link": str(row.get("link", "#")),
            "match_score": round(float(scores[idx]), 4),
        })

    return results
