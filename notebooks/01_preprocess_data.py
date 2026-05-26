"""
Dataset Preprocessing Script — CV-IR Project
=============================================
Memproses raw dataset dari Kaggle menjadi format yang siap digunakan.

Input:  data/raw/ (dari Kaggle download)
Output: data/processed/job_listings.csv

Usage:
    python notebooks/01_preprocess_data.py
"""

import os
import sys
import pandas as pd
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")


def find_job_postings_file() -> str:
    """Search for the job postings CSV in raw data directory."""
    possible_names = [
        "job_postings.csv",
        "postings.csv",
        "linkedin_job_postings.csv",
        "jobs.csv",
    ]

    # Direct files
    for name in possible_names:
        path = os.path.join(RAW_DIR, name)
        if os.path.exists(path):
            return path

    # Search subdirectories
    for root, dirs, files in os.walk(RAW_DIR):
        for name in possible_names:
            if name in files:
                return os.path.join(root, name)

    # Last resort — find any CSV with 'job' or 'posting' in the name
    for root, dirs, files in os.walk(RAW_DIR):
        for f in files:
            if f.endswith(".csv") and ("job" in f.lower() or "posting" in f.lower()):
                return os.path.join(root, f)

    return None


def find_companies_file() -> str:
    """Search for the companies CSV in raw data directory."""
    possible_names = [
        "companies.csv",
        "company_details.csv",
    ]

    for root, dirs, files in os.walk(RAW_DIR):
        for name in possible_names:
            if name in files:
                return os.path.join(root, name)
    return None


def process_linkedin_dataset(job_path: str, company_path: str = None) -> pd.DataFrame:
    """Process the LinkedIn Job Postings dataset."""
    print(f"📂 Loading job postings from: {job_path}")

    # Read with error handling
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            df = pd.read_csv(job_path, encoding=encoding, low_memory=False)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise RuntimeError(f"Could not read {job_path}")

    print(f"   Raw rows: {len(df)}")
    print(f"   Columns: {list(df.columns)}")

    # Normalize column names
    df.columns = df.columns.str.lower().str.strip()

    # ── Map columns ──
    col_mapping = {}

    # Title
    for c in ["title", "job_title", "position", "job_name"]:
        if c in df.columns:
            col_mapping["title"] = c
            break

    # Description
    for c in ["description", "job_description", "desc", "job_desc"]:
        if c in df.columns:
            col_mapping["description"] = c
            break

    # Location
    for c in ["location", "job_location", "city", "place"]:
        if c in df.columns:
            col_mapping["location"] = c
            break

    # Company
    for c in ["company_name", "company", "employer", "organization"]:
        if c in df.columns:
            col_mapping["company"] = c
            break

    # Salary
    for c in ["salary", "pay_period", "med_salary", "max_salary", "min_salary",
              "normalized_salary"]:
        if c in df.columns:
            col_mapping["salary"] = c
            break

    print(f"\n📋 Column mapping: {col_mapping}")

    # ── Build processed dataframe ──
    processed = pd.DataFrame()
    processed["title"] = df[col_mapping.get("title", df.columns[0])].fillna("Unknown")
    processed["description"] = df[col_mapping.get("description", df.columns[1])].fillna("")

    if "location" in col_mapping:
        processed["location"] = df[col_mapping["location"]].fillna("N/A")
    else:
        processed["location"] = "N/A"

    if "company" in col_mapping:
        processed["company"] = df[col_mapping["company"]].fillna("N/A")
    elif company_path:
        # Try to join with companies file
        try:
            companies = pd.read_csv(company_path, encoding="utf-8", low_memory=False)
            companies.columns = companies.columns.str.lower().str.strip()
            if "company_id" in df.columns and "company_id" in companies.columns:
                name_col = next(
                    (c for c in ["name", "company_name"] if c in companies.columns),
                    None
                )
                if name_col:
                    company_map = dict(zip(companies["company_id"], companies[name_col]))
                    processed["company"] = df["company_id"].map(company_map).fillna("N/A")
                else:
                    processed["company"] = "N/A"
            else:
                processed["company"] = "N/A"
        except Exception as e:
            print(f"   ⚠️ Could not load companies: {e}")
            processed["company"] = "N/A"
    else:
        processed["company"] = "N/A"

    # Generate LinkedIn-style link
    if "job_id" in df.columns:
        processed["link"] = df["job_id"].apply(
            lambda x: f"https://www.linkedin.com/jobs/view/{x}" if pd.notna(x) else "#"
        )
    else:
        processed["link"] = "#"

    # ── Clean up ──
    # Remove rows with no description or very short descriptions
    processed = processed[processed["description"].str.len() > 50]

    # Remove duplicates
    processed = processed.drop_duplicates(subset=["title", "description"]).reset_index(drop=True)

    # Limit to manageable size
    if len(processed) > 10000:
        print(f"   📌 Sampling 10,000 from {len(processed)} rows for performance...")
        processed = processed.sample(n=10000, random_state=42).reset_index(drop=True)

    print(f"\n✅ Processed: {len(processed)} job listings")
    return processed


def create_fallback_dataset() -> pd.DataFrame:
    """Create a synthetic job listings dataset as fallback."""
    print("⚠️ No job postings dataset found. Creating synthetic dataset...")

    jobs = [
        # Data Science & AI
        {"title": "Data Scientist", "company": "Tokopedia", "location": "Jakarta, Indonesia",
         "description": "Looking for Data Scientist with Python, Machine Learning, SQL, TensorFlow, Deep Learning experience. Build predictive models and data pipelines.",
         "link": "https://linkedin.com/jobs/data-scientist"},
        {"title": "Machine Learning Engineer", "company": "Gojek", "location": "Jakarta, Indonesia",
         "description": "ML Engineer needed. Skills: Python, PyTorch, TensorFlow, NLP, Computer Vision, MLOps, Docker, Kubernetes.",
         "link": "https://linkedin.com/jobs/ml-engineer"},
        {"title": "AI Research Scientist", "company": "Bukalapak", "location": "Bandung, Indonesia",
         "description": "Research position in AI. Required: Deep Learning, Neural Networks, NLP, Python, TensorFlow, Research papers.",
         "link": "https://linkedin.com/jobs/ai-researcher"},
        {"title": "Data Analyst", "company": "Shopee", "location": "Jakarta, Indonesia",
         "description": "Data Analyst role. Skills: SQL, Python, Excel, Tableau, Data Visualization, Statistical Analysis, A/B Testing.",
         "link": "https://linkedin.com/jobs/data-analyst"},
        {"title": "Data Engineer", "company": "Traveloka", "location": "Jakarta, Indonesia",
         "description": "Data Engineer position. Required: Python, SQL, Spark, Airflow, ETL, Data Pipeline, AWS, BigQuery.",
         "link": "https://linkedin.com/jobs/data-engineer"},

        # Software Development
        {"title": "Backend Developer", "company": "Telkom Indonesia", "location": "Bandung, Indonesia",
         "description": "Backend Developer needed. Skills: Java, Spring Boot, REST API, PostgreSQL, Docker, Microservices, Git.",
         "link": "https://linkedin.com/jobs/backend-dev"},
        {"title": "Frontend Developer", "company": "Blibli", "location": "Jakarta, Indonesia",
         "description": "Frontend Developer role. Required: JavaScript, React, TypeScript, HTML, CSS, Node.js, Figma.",
         "link": "https://linkedin.com/jobs/frontend-dev"},
        {"title": "Full Stack Developer", "company": "Ruangguru", "location": "Jakarta, Indonesia",
         "description": "Full Stack Developer. Skills: JavaScript, React, Node.js, Python, PostgreSQL, MongoDB, Docker, AWS.",
         "link": "https://linkedin.com/jobs/fullstack-dev"},
        {"title": "Mobile Developer", "company": "Dana", "location": "Jakarta, Indonesia",
         "description": "Mobile Developer position. Required: Kotlin, Swift, Flutter, Dart, REST API, Firebase, Git.",
         "link": "https://linkedin.com/jobs/mobile-dev"},
        {"title": "DevOps Engineer", "company": "OVO", "location": "Jakarta, Indonesia",
         "description": "DevOps Engineer needed. Skills: Docker, Kubernetes, AWS, CI/CD, Jenkins, Terraform, Linux, Monitoring.",
         "link": "https://linkedin.com/jobs/devops"},

        # Web Development
        {"title": "Web Developer", "company": "Tiket.com", "location": "Jakarta, Indonesia",
         "description": "Web Developer role. Required: HTML, CSS, JavaScript, React, Vue.js, Node.js, REST API, Git.",
         "link": "https://linkedin.com/jobs/web-dev"},
        {"title": "UI/UX Designer", "company": "Tokopedia", "location": "Jakarta, Indonesia",
         "description": "UI/UX Designer. Skills: Figma, Adobe Photoshop, Illustrator, Wireframing, Prototyping, User Research.",
         "link": "https://linkedin.com/jobs/uiux-designer"},

        # Management & Business
        {"title": "Project Manager", "company": "Accenture", "location": "Jakarta, Indonesia",
         "description": "Project Manager role. Skills: Agile, Scrum, Jira, Leadership, Communication, Project Planning, Risk Management.",
         "link": "https://linkedin.com/jobs/project-manager"},
        {"title": "Business Analyst", "company": "Deloitte", "location": "Jakarta, Indonesia",
         "description": "Business Analyst position. Required: Data Analysis, SQL, Excel, Power BI, Presentation, Problem Solving.",
         "link": "https://linkedin.com/jobs/business-analyst"},
        {"title": "Product Manager", "company": "Grab", "location": "Jakarta, Indonesia",
         "description": "Product Manager needed. Skills: Product Strategy, Agile, Data Analysis, Leadership, Communication, A/B Testing.",
         "link": "https://linkedin.com/jobs/product-manager"},

        # Cybersecurity & Networking
        {"title": "Network Security Engineer", "company": "Telkomsel", "location": "Jakarta, Indonesia",
         "description": "Security Engineer role. Skills: Cybersecurity, Networking, Firewall, Linux, Python, Penetration Testing.",
         "link": "https://linkedin.com/jobs/security-engineer"},

        # Database
        {"title": "Database Administrator", "company": "BCA", "location": "Jakarta, Indonesia",
         "description": "DBA position. Required: SQL, Oracle, PostgreSQL, Database Administration, Performance Tuning, Backup.",
         "link": "https://linkedin.com/jobs/dba"},

        # HR & Sales
        {"title": "HR Manager", "company": "Unilever", "location": "Jakarta, Indonesia",
         "description": "HR Manager role. Skills: Recruitment, Employee Relations, HR Policy, Leadership, Communication, Training.",
         "link": "https://linkedin.com/jobs/hr-manager"},
        {"title": "Sales Executive", "company": "Samsung", "location": "Jakarta, Indonesia",
         "description": "Sales role. Required: Sales Strategy, Communication, Negotiation, CRM, Customer Relations, Presentation.",
         "link": "https://linkedin.com/jobs/sales"},

        # Engineering
        {"title": "Mechanical Engineer", "company": "Astra International", "location": "Jakarta, Indonesia",
         "description": "Mechanical Engineer position. Skills: CAD, AutoCAD, SolidWorks, Manufacturing, Quality Control.",
         "link": "https://linkedin.com/jobs/mechanical-eng"},
        {"title": "Civil Engineer", "company": "Wijaya Karya", "location": "Jakarta, Indonesia",
         "description": "Civil Engineer role. Required: AutoCAD, Structural Analysis, Project Management, Construction.",
         "link": "https://linkedin.com/jobs/civil-eng"},
        {"title": "Electrical Engineer", "company": "PLN", "location": "Jakarta, Indonesia",
         "description": "Electrical Engineer. Skills: Circuit Design, PLC, SCADA, AutoCAD, Electrical Systems, Power Systems.",
         "link": "https://linkedin.com/jobs/electrical-eng"},

        # QA & Testing
        {"title": "QA Engineer", "company": "Traveloka", "location": "Jakarta, Indonesia",
         "description": "QA Engineer role. Skills: Testing, Automation Testing, Selenium, Python, API Testing, Bug Tracking, Jira.",
         "link": "https://linkedin.com/jobs/qa-engineer"},
        {"title": "Automation Test Engineer", "company": "Bukalapak", "location": "Jakarta, Indonesia",
         "description": "Automation Testing position. Required: Selenium, Python, Java, CI/CD, Test Frameworks, Performance Testing.",
         "link": "https://linkedin.com/jobs/automation-test"},

        # Blockchain & Emerging Tech
        {"title": "Blockchain Developer", "company": "Indodax", "location": "Jakarta, Indonesia",
         "description": "Blockchain Developer. Skills: Solidity, Web3, Ethereum, Smart Contracts, JavaScript, Python, Cryptography.",
         "link": "https://linkedin.com/jobs/blockchain-dev"},

        # SAP
        {"title": "SAP Consultant", "company": "IBM Indonesia", "location": "Jakarta, Indonesia",
         "description": "SAP Consultant needed. Skills: SAP, ERP, Business Process, ABAP, Project Management, Consulting.",
         "link": "https://linkedin.com/jobs/sap-consultant"},
    ]

    # Duplicate each with variations to create a larger dataset
    expanded = []
    locations = ["Jakarta, Indonesia", "Bandung, Indonesia", "Surabaya, Indonesia",
                 "Yogyakarta, Indonesia", "Semarang, Indonesia", "Medan, Indonesia",
                 "Remote", "Singapore", "Kuala Lumpur, Malaysia"]
    companies_extra = ["Google Indonesia", "Microsoft Indonesia", "Amazon", "Meta",
                       "Apple", "Netflix", "Spotify", "Stripe", "Airbnb"]

    for job in jobs:
        expanded.append(job)
        # Create 3 variations
        for i in range(3):
            variant = job.copy()
            variant["location"] = locations[(hash(job["title"]) + i) % len(locations)]
            variant["company"] = companies_extra[(hash(job["title"]) + i) % len(companies_extra)]
            variant["description"] = job["description"] + f" {i+2}+ years of experience preferred."
            expanded.append(variant)

    df = pd.DataFrame(expanded)
    print(f"✅ Created synthetic dataset with {len(df)} job listings")
    return df


def main():
    print("=" * 60)
    print("🔧 CV-IR — Dataset Preprocessing")
    print("=" * 60)

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # ── Process Job Postings ──
    job_path = find_job_postings_file()
    company_path = find_companies_file()

    if job_path:
        print(f"\n📂 Found job postings: {job_path}")
        if company_path:
            print(f"📂 Found companies: {company_path}")
        df = process_linkedin_dataset(job_path, company_path)
    else:
        df = create_fallback_dataset()

    # ── Save processed data ──
    output_path = os.path.join(PROCESSED_DIR, "job_listings.csv")
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"\n💾 Saved to: {output_path}")
    print(f"   Rows: {len(df)}")
    print(f"   Columns: {list(df.columns)}")

    # ── Preview ──
    print(f"\n📋 Preview (first 5 rows):")
    print(df[["title", "company", "location"]].head().to_string(index=False))

    print("\n" + "=" * 60)
    print("✅ Preprocessing complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
