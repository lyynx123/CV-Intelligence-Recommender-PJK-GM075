import spacy
from typing import Optional

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("⚠️ spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

# ============================================================
# Comprehensive skill list — expandable
# ============================================================
SKILL_KEYWORDS = [
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust",
    "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB", "Perl", "Dart",
    "Objective-C", "Lua", "Haskell", "Shell", "Bash", "PowerShell",

    # Web Development
    "HTML", "CSS", "React", "Angular", "Vue.js", "Vue", "Next.js", "Nuxt.js",
    "Node.js", "Express.js", "Express", "Django", "Flask", "FastAPI",
    "Spring Boot", "Spring", "Laravel", "Ruby on Rails", "ASP.NET",
    "Svelte", "jQuery", "Bootstrap", "Tailwind CSS", "Tailwind",
    "GraphQL", "REST API", "REST", "WebSocket",

    # Data Science & ML
    "Machine Learning", "Deep Learning", "Data Science", "Data Analysis",
    "Data Engineering", "Data Mining", "Natural Language Processing", "NLP",
    "Computer Vision", "Reinforcement Learning", "Neural Networks",
    "Feature Engineering", "Model Deployment", "MLOps",
    "Statistical Analysis", "Statistics", "A/B Testing",

    # ML Frameworks & Libraries
    "TensorFlow", "PyTorch", "Keras", "Scikit-Learn", "XGBoost", "LightGBM",
    "CatBoost", "NLTK", "spaCy", "Hugging Face", "Transformers",
    "OpenCV", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn",
    "Plotly", "Jupyter", "SBERT", "Sentence-Transformers",

    # Databases
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch",
    "SQLite", "Oracle", "DynamoDB", "Cassandra", "Firebase",
    "Neo4j", "MariaDB", "Supabase",

    # Cloud & DevOps
    "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes",
    "CI/CD", "Jenkins", "GitHub Actions", "Terraform", "Ansible",
    "Nginx", "Apache", "Linux", "Unix", "Git", "GitHub", "GitLab",

    # Big Data
    "Spark", "Hadoop", "Kafka", "Airflow", "Hive", "Flink",
    "Snowflake", "BigQuery", "Databricks", "ETL", "Data Pipeline",
    "Data Warehouse", "Data Lake",

    # Business & Soft Skills
    "Project Management", "Agile", "Scrum", "Jira", "Confluence",
    "Leadership", "Communication", "Problem Solving", "Teamwork",
    "Critical Thinking", "Presentation", "Public Speaking",

    # Design & Tools
    "Figma", "Adobe Photoshop", "Photoshop", "Adobe Illustrator",
    "Illustrator", "Sketch", "InVision", "UI/UX", "UX Design",
    "UI Design", "Wireframing", "Prototyping",

    # Other Tech
    "Blockchain", "IoT", "Cybersecurity", "Networking",
    "Microservices", "API Development", "Web Scraping",
    "Automation", "RPA", "Power BI", "Tableau",
    "Excel", "Microsoft Office", "SAP", "Salesforce",
]

# Normalize skill lookup — lowercase for case-insensitive matching
_SKILL_LOOKUP = {skill.lower(): skill for skill in SKILL_KEYWORDS}


def extract_skills(text: str) -> list[str]:
    """
    Metode hybrid: keyword matching + spaCy NER.
    Returns a deduplicated list of skills found in the text.
    """
    found_skills = set()

    # ── 1. Keyword Matching (case-insensitive) ──
    text_lower = text.lower()
    for skill_lower, skill_proper in _SKILL_LOOKUP.items():
        if skill_lower in text_lower:
            found_skills.add(skill_proper)

    # ── 2. spaCy NER — capture ORG/PRODUCT entities as potential skills ──
    if nlp is not None:
        doc = nlp(text[:100000])  # Limit text length for performance
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT"] and len(ent.text) > 2:
                # Check if entity matches a known skill
                ent_lower = ent.text.lower().strip()
                if ent_lower in _SKILL_LOOKUP:
                    found_skills.add(_SKILL_LOOKUP[ent_lower])

    return sorted(list(found_skills))
