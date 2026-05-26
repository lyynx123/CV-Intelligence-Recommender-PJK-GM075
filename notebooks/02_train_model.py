"""
Training Script untuk Job Classifier — CV-IR Project
=====================================================
Melatih model TF-IDF + RandomForest untuk memprediksi
kategori pekerjaan berdasarkan teks CV.

Dataset: UpdatedResumeDataSet.csv (Kaggle)
Output:  models/job_classifier.pkl, models/tfidf_vectorizer.pkl

Usage:
    python notebooks/02_train_model.py
"""

import os
import sys
import re
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

# ============================================================
# Paths
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Possible dataset paths
RESUME_PATHS = [
    os.path.join(DATA_DIR, "raw", "UpdatedResumeDataSet.csv"),
    os.path.join(DATA_DIR, "raw", "updated-resume-dataset", "UpdatedResumeDataSet.csv"),
    os.path.join(DATA_DIR, "raw", "Resume.csv"),
]


def find_resume_dataset() -> str:
    """Find the resume dataset from known possible paths."""
    for path in RESUME_PATHS:
        if os.path.exists(path):
            print(f"✅ Found resume dataset: {path}")
            return path
    raise FileNotFoundError(
        f"Resume dataset not found. Searched:\n" +
        "\n".join(f"  - {p}" for p in RESUME_PATHS)
    )


def clean_resume_text(text: str) -> str:
    """Clean resume text for training."""
    if not isinstance(text, str):
        return ""
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    # Remove special characters and HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()


def main():
    print("=" * 60)
    print("🚀 CV-IR — Job Classifier Training Script")
    print("=" * 60)

    # ── 1. Load Dataset ──
    dataset_path = find_resume_dataset()
    print(f"\n📂 Loading dataset from: {dataset_path}")

    # Try different encodings
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            df = pd.read_csv(dataset_path, encoding=encoding)
            print(f"   Encoding: {encoding}")
            break
        except UnicodeDecodeError:
            continue
    else:
        raise RuntimeError("Could not read CSV with any encoding")

    print(f"   Rows: {len(df)}")
    print(f"   Columns: {list(df.columns)}")

    # ── 2. Identify columns ──
    # The dataset might have different column names
    text_col = None
    label_col = None

    for col in df.columns:
        col_lower = col.lower().strip()
        if col_lower in ["resume", "resume_str", "text", "content", "resume_text"]:
            text_col = col
        elif col_lower in ["category", "label", "job_category", "job_title", "class"]:
            label_col = col

    if text_col is None:
        # Use the column with the longest average text
        avg_lens = {col: df[col].astype(str).str.len().mean() for col in df.columns}
        text_col = max(avg_lens, key=avg_lens.get)
        print(f"   ⚠️ Auto-detected text column: '{text_col}' (avg length: {avg_lens[text_col]:.0f})")

    if label_col is None:
        # Use the column with fewest unique values (likely categorical)
        unique_counts = {col: df[col].nunique() for col in df.columns if col != text_col}
        label_col = min(unique_counts, key=unique_counts.get)
        print(f"   ⚠️ Auto-detected label column: '{label_col}' (unique: {unique_counts[label_col]})")

    print(f"\n📊 Using:")
    print(f"   Text column:  '{text_col}'")
    print(f"   Label column: '{label_col}'")

    # ── 3. Clean Data ──
    print("\n🧹 Cleaning data...")
    df = df.dropna(subset=[text_col, label_col])
    df["clean_text"] = df[text_col].apply(clean_resume_text)
    df = df[df["clean_text"].str.len() > 50]  # Remove very short texts

    print(f"   Samples after cleaning: {len(df)}")
    print(f"   Categories: {df[label_col].nunique()}")
    print(f"\n📋 Category distribution:")
    for cat, count in df[label_col].value_counts().items():
        print(f"   {cat}: {count}")

    # ── 4. Feature Engineering ──
    print("\n🔧 Building TF-IDF features...")
    tfidf = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words="english",
        min_df=2,
        max_df=0.95,
    )

    X = tfidf.fit_transform(df["clean_text"])
    y = df[label_col].to_numpy()

    print(f"   Feature matrix: {X.shape}")

    # ── 5. Train/Test Split ──
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\n📊 Split:")
    print(f"   Train: {X_train.shape[0]} samples")
    print(f"   Test:  {X_test.shape[0]} samples")

    # ── 6. Train Model ──
    print("\n🏋️ Training RandomForest classifier...")
    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )
    clf.fit(X_train, y_train)

    # ── 7. Evaluate ──
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n📈 Results:")
    print(f"   Accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)")
    print(f"\n📋 Classification Report:")
    print(classification_report(y_test, y_pred))

    # ── 8. Save Model ──
    os.makedirs(MODEL_DIR, exist_ok=True)

    classifier_path = os.path.join(MODEL_DIR, "job_classifier.pkl")
    vectorizer_path = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")

    joblib.dump(clf, classifier_path)
    joblib.dump(tfidf, vectorizer_path)

    print(f"\n💾 Models saved:")
    print(f"   Classifier:  {classifier_path}")
    print(f"   Vectorizer:  {vectorizer_path}")

    # ── 9. Quick sanity check ──
    print("\n🧪 Sanity check — sample predictions:")
    test_texts = [
        "python machine learning tensorflow deep learning neural network data science",
        "java spring boot microservices rest api backend development",
        "html css javascript react frontend web development ui ux design",
        "sql database administration oracle postgresql etl data warehouse",
        "project management agile scrum leadership team coordination",
    ]
    for text in test_texts:
        X_sample = tfidf.transform([text])
        pred = clf.predict(X_sample)[0]
        prob = max(clf.predict_proba(X_sample)[0])
        print(f"   '{text[:50]}...' → {pred} ({prob*100:.1f}%)")

    print("\n" + "=" * 60)
    print("✅ Training complete! Models saved to models/ directory.")
    print("=" * 60)


if __name__ == "__main__":
    main()
