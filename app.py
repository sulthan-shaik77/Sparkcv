"""
Smart Job Description Analyzer & Resume Optimization System
A production-ready NLP application built with Streamlit, Scikit-Learn, and NLTK.
"""

import base64
import os
from pathlib import Path
import io
import re
import string
from collections import Counter
import datetime
from typing import Any, Dict, List, Set, Tuple

import math

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    st = None
    STREAMLIT_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer, util
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


def get_background_image_base64() -> str:
    """Read the executive luxury background image as base64 string."""
    try:
        bg_path = Path(__file__).parent / "assets" / "luxury_login_bg.webp"
        if bg_path.exists():
            with open(bg_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        pass
    return ""


def get_login_bg_base64() -> str:
    """Read the luxury login background image as base64 string."""
    try:
        bg_path = Path(__file__).parent / "assets" / "luxury_login_bg.webp"
        if bg_path.exists():
            with open(bg_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        pass
    return ""


def get_login_crest_base64() -> str:
    """Read the luxury crest PNG as base64 string."""
    try:
        crest_path = Path(__file__).parent / "assets" / "luxury_crest.png"
        if crest_path.exists():
            with open(crest_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        pass
    return ""


def get_sbert_model(model_name: str = "all-MiniLM-L6-v2"):
    """Loads and caches the Sentence-BERT model if sentence-transformers is installed."""
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        return None
    try:
        if STREAMLIT_AVAILABLE and hasattr(st, "cache_resource"):
            # Streamlit caching wrapper
            return _load_sbert_cached(model_name)
        return SentenceTransformer(model_name)
    except Exception:
        return None


if STREAMLIT_AVAILABLE and hasattr(st, "cache_resource"):
    @st.cache_resource
    def _load_sbert_cached(model_name: str):
        return SentenceTransformer(model_name)
else:
    def _load_sbert_cached(model_name: str):
        return SentenceTransformer(model_name)


def compute_sbert_similarity(resume_text: str, jd_text: str) -> float:
    """Computes dense neural semantic similarity using Sentence-BERT (all-MiniLM-L6-v2)."""
    if not SENTENCE_TRANSFORMERS_AVAILABLE or not resume_text.strip() or not jd_text.strip():
        return 0.0
    try:
        model = get_sbert_model()
        if model is None:
            return 0.0
        # Truncate texts to avoid exceeding token limits
        emb1 = model.encode(resume_text[:4000], convert_to_tensor=True)
        emb2 = model.encode(jd_text[:4000], convert_to_tensor=True)
        sim = util.cos_sim(emb1, emb2).item()
        return max(0.0, min(1.0, float(sim)))
    except Exception:
        return 0.0

# Resilient Pure-Python TF-IDF and Cosine Similarity Fallback
class PurePythonTfidfVectorizer:
    def __init__(self, ngram_range=(1, 2), stop_words='english', max_features=50):
        self.ngram_range = ngram_range
        self.stop_words = stop_words
        self.max_features = max_features
        self.feature_names = []
        self.idf_ = {}

    def _tokenize(self, text: str) -> List[str]:
        words = text.lower().split()
        tokens = []
        min_n, max_n = self.ngram_range
        for n in range(min_n, max_n + 1):
            for i in range(len(words) - n + 1):
                tokens.append(" ".join(words[i:i + n]))
        return tokens

    def fit_transform(self, docs: List[str]):
        doc_tokens = [self._tokenize(doc) for doc in docs]
        n_docs = len(docs)
        df = Counter()
        for dt in doc_tokens:
            for term in set(dt):
                df[term] += 1

        # Smooth IDF
        all_terms = sorted(df.keys())
        if self.max_features and len(all_terms) > self.max_features:
            all_terms = sorted(all_terms, key=lambda t: df[t], reverse=True)[:self.max_features]

        self.feature_names = all_terms
        self.idf_ = {t: math.log((1 + n_docs) / (1 + df[t])) + 1.0 for t in self.feature_names}

        # Vector representations
        vectors = []
        for dt in doc_tokens:
            counts = Counter(dt)
            vec = [counts.get(t, 0) * self.idf_[t] for t in self.feature_names]
            norm = math.sqrt(sum(x * x for x in vec))
            if norm > 0:
                vec = [x / norm for x in vec]
            vectors.append(vec)

        return PurePythonMatrix(vectors, self.feature_names)

    def get_feature_names_out(self):
        return self.feature_names

class PurePythonMatrix:
    def __init__(self, vectors, feature_names):
        self.vectors = vectors
        self.feature_names = feature_names

    def toarray(self):
        return self.vectors

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return self.vectors[idx]
        return self.vectors[idx]

def pure_python_cosine_similarity(vec1, vec2):
    v1 = vec1.vectors[0] if isinstance(vec1, PurePythonMatrix) else (vec1[0] if isinstance(vec1, list) else vec1)
    v2 = vec2.vectors[0] if isinstance(vec2, PurePythonMatrix) else (vec2[0] if isinstance(vec2, list) else vec2)
    min_len = min(len(v1), len(v2))
    dot = sum(v1[i] * v2[i] for i in range(min_len))
    return [[max(0.0, min(1.0, dot))]]

# Choose active TF-IDF and Cosine Sim implementation
ActiveTfidfVectorizer = TfidfVectorizer if SKLEARN_AVAILABLE else PurePythonTfidfVectorizer
active_cosine_similarity = cosine_similarity if SKLEARN_AVAILABLE else pure_python_cosine_similarity

# Optional file parsing libraries
try:
    import pypdf
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# Try importing NLTK, with offline fallback stop words
FALLBACK_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves", "will", "shall", "may", "might", "must", "can",
    "also", "etc", "using", "experience", "work", "role", "years", "candidate",
    "team", "skills", "ability", "responsibilities", "requirements", "including"
}

def get_stopwords() -> Set[str]:
    """Retrieve stopwords from NLTK if available, otherwise use curated set."""
    try:
        import nltk
        try:
            from nltk.corpus import stopwords
            return set(stopwords.words("english")).union(FALLBACK_STOPWORDS)
        except LookupError:
            nltk.download("stopwords", quiet=True)
            from nltk.corpus import stopwords
            return set(stopwords.words("english")).union(FALLBACK_STOPWORDS)
    except Exception:
        return FALLBACK_STOPWORDS

STOPWORDS = get_stopwords()

# Curated Technical Skills and Tools Taxonomy (grouped by domain)
TECHNICAL_SKILLS_TAXONOMY: Dict[str, Dict[str, any]] = {
    # Programming Languages
    "python": {"display": "Python", "category": "Programming Languages", "domain": "backend"},
    "javascript": {"display": "JavaScript", "category": "Programming Languages", "domain": "frontend"},
    "typescript": {"display": "TypeScript", "category": "Programming Languages", "domain": "frontend"},
    "java": {"display": "Java", "category": "Programming Languages", "domain": "backend"},
    "c++": {"display": "C++", "category": "Programming Languages", "domain": "systems"},
    "c#": {"display": "C#", "category": "Programming Languages", "domain": "backend"},
    "golang": {"display": "Go (Golang)", "category": "Programming Languages", "domain": "backend"},
    "go": {"display": "Go", "category": "Programming Languages", "domain": "backend"},
    "rust": {"display": "Rust", "category": "Programming Languages", "domain": "systems"},
    "ruby": {"display": "Ruby", "category": "Programming Languages", "domain": "backend"},
    "php": {"display": "PHP", "category": "Programming Languages", "domain": "backend"},
    "swift": {"display": "Swift", "category": "Programming Languages", "domain": "mobile"},
    "kotlin": {"display": "Kotlin", "category": "Programming Languages", "domain": "mobile"},
    "scala": {"display": "Scala", "category": "Programming Languages", "domain": "data_engineering"},
    "r": {"display": "R", "category": "Programming Languages", "domain": "data_science"},
    "sql": {"display": "SQL", "category": "Databases & Query", "domain": "data_engineering"},
    "bash": {"display": "Bash / Shell", "category": "DevOps & OS", "domain": "devops"},
    "html": {"display": "HTML5", "category": "Frontend", "domain": "frontend"},
    "css": {"display": "CSS3", "category": "Frontend", "domain": "frontend"},

    # Python & Backend Frameworks
    "fastapi": {"display": "FastAPI", "category": "Web Frameworks", "domain": "backend"},
    "flask": {"display": "Flask", "category": "Web Frameworks", "domain": "backend"},
    "django": {"display": "Django", "category": "Web Frameworks", "domain": "backend"},
    "node.js": {"display": "Node.js", "category": "Web Frameworks", "domain": "backend"},
    "nodejs": {"display": "Node.js", "category": "Web Frameworks", "domain": "backend"},
    "express": {"display": "Express.js", "category": "Web Frameworks", "domain": "backend"},
    "spring boot": {"display": "Spring Boot", "category": "Web Frameworks", "domain": "backend"},
    "graphql": {"display": "GraphQL", "category": "API & Networking", "domain": "backend"},
    "rest": {"display": "REST API", "category": "API & Networking", "domain": "backend"},
    "restful": {"display": "RESTful APIs", "category": "API & Networking", "domain": "backend"},
    "microservices": {"display": "Microservices", "category": "Architecture", "domain": "backend"},
    "celery": {"display": "Celery", "category": "Backend Tools", "domain": "backend"},

    # Frontend Frameworks & Libraries
    "react": {"display": "React.js", "category": "Frontend Frameworks", "domain": "frontend"},
    "next.js": {"display": "Next.js", "category": "Frontend Frameworks", "domain": "frontend"},
    "nextjs": {"display": "Next.js", "category": "Frontend Frameworks", "domain": "frontend"},
    "vue": {"display": "Vue.js", "category": "Frontend Frameworks", "domain": "frontend"},
    "angular": {"display": "Angular", "category": "Frontend Frameworks", "domain": "frontend"},
    "tailwind": {"display": "Tailwind CSS", "category": "Frontend Styling", "domain": "frontend"},
    "bootstrap": {"display": "Bootstrap", "category": "Frontend Styling", "domain": "frontend"},
    "redux": {"display": "Redux", "category": "Frontend State", "domain": "frontend"},

    # Data Science, ML & AI
    "pandas": {"display": "Pandas", "category": "Data Science & ML", "domain": "data_science"},
    "numpy": {"display": "NumPy", "category": "Data Science & ML", "domain": "data_science"},
    "scikit-learn": {"display": "Scikit-Learn", "category": "Data Science & ML", "domain": "machine_learning"},
    "sklearn": {"display": "Scikit-Learn", "category": "Data Science & ML", "domain": "machine_learning"},
    "pytorch": {"display": "PyTorch", "category": "Data Science & ML", "domain": "machine_learning"},
    "tensorflow": {"display": "TensorFlow", "category": "Data Science & ML", "domain": "machine_learning"},
    "keras": {"display": "Keras", "category": "Data Science & ML", "domain": "machine_learning"},
    "xgboost": {"display": "XGBoost", "category": "Data Science & ML", "domain": "machine_learning"},
    "lightgbm": {"display": "LightGBM", "category": "Data Science & ML", "domain": "machine_learning"},
    "nlp": {"display": "NLP (Natural Language Processing)", "category": "Data Science & ML", "domain": "machine_learning"},
    "nltk": {"display": "NLTK", "category": "Data Science & ML", "domain": "machine_learning"},
    "spacy": {"display": "spaCy", "category": "Data Science & ML", "domain": "machine_learning"},
    "opencv": {"display": "OpenCV", "category": "Computer Vision", "domain": "machine_learning"},
    "deep learning": {"display": "Deep Learning", "category": "AI / ML Concepts", "domain": "machine_learning"},
    "machine learning": {"display": "Machine Learning", "category": "AI / ML Concepts", "domain": "machine_learning"},
    "data analysis": {"display": "Data Analysis", "category": "Data Science", "domain": "data_science"},
    "matplotlib": {"display": "Matplotlib", "category": "Data Visualization", "domain": "data_science"},
    "seaborn": {"display": "Seaborn", "category": "Data Visualization", "domain": "data_science"},
    "plotly": {"display": "Plotly", "category": "Data Visualization", "domain": "data_science"},
    "huggingface": {"display": "Hugging Face", "category": "GenAI & LLMs", "domain": "gen_ai"},
    "llm": {"display": "Large Language Models (LLMs)", "category": "GenAI & LLMs", "domain": "gen_ai"},
    "llms": {"display": "Large Language Models (LLMs)", "category": "GenAI & LLMs", "domain": "gen_ai"},
    "langchain": {"display": "LangChain", "category": "GenAI & LLMs", "domain": "gen_ai"},
    "rag": {"display": "RAG (Retrieval-Augmented Generation)", "category": "GenAI & LLMs", "domain": "gen_ai"},
    "beautifulsoup": {"display": "BeautifulSoup", "category": "Web Scraping", "domain": "backend"},
    "selenium": {"display": "Selenium", "category": "Web Automation", "domain": "backend"},

    # Databases & Big Data
    "postgresql": {"display": "PostgreSQL", "category": "Databases", "domain": "database"},
    "postgres": {"display": "PostgreSQL", "category": "Databases", "domain": "database"},
    "mysql": {"display": "MySQL", "category": "Databases", "domain": "database"},
    "mongodb": {"display": "MongoDB", "category": "Databases", "domain": "database"},
    "redis": {"display": "Redis", "category": "Databases & Caching", "domain": "database"},
    "sqlite": {"display": "SQLite", "category": "Databases", "domain": "database"},
    "snowflake": {"display": "Snowflake", "category": "Cloud Data Warehouses", "domain": "data_engineering"},
    "bigquery": {"display": "BigQuery", "category": "Cloud Data Warehouses", "domain": "data_engineering"},
    "spark": {"display": "Apache Spark", "category": "Big Data", "domain": "data_engineering"},
    "kafka": {"display": "Apache Kafka", "category": "Data Streaming", "domain": "data_engineering"},
    "airflow": {"display": "Apache Airflow", "category": "Orchestration", "domain": "data_engineering"},

    # Cloud & DevOps
    "aws": {"display": "AWS (Amazon Web Services)", "category": "Cloud Platforms", "domain": "devops"},
    "gcp": {"display": "Google Cloud Platform (GCP)", "category": "Cloud Platforms", "domain": "devops"},
    "azure": {"display": "Microsoft Azure", "category": "Cloud Platforms", "domain": "devops"},
    "docker": {"display": "Docker", "category": "Containerization", "domain": "devops"},
    "kubernetes": {"display": "Kubernetes", "category": "Container Orchestration", "domain": "devops"},
    "k8s": {"display": "Kubernetes", "category": "Container Orchestration", "domain": "devops"},
    "terraform": {"display": "Terraform", "category": "Infrastructure as Code", "domain": "devops"},
    "ci/cd": {"display": "CI/CD Pipelines", "category": "DevOps", "domain": "devops"},
    "jenkins": {"display": "Jenkins", "category": "DevOps", "domain": "devops"},
    "github actions": {"display": "GitHub Actions", "category": "DevOps", "domain": "devops"},
    "linux": {"display": "Linux", "category": "Operating Systems", "domain": "devops"},
    "git": {"display": "Git Version Control", "category": "Developer Tools", "domain": "devops"},

    # Software Engineering Practices
    "agile": {"display": "Agile / Scrum", "category": "Methodologies", "domain": "general"},
    "scrum": {"display": "Scrum", "category": "Methodologies", "domain": "general"},
    "tdd": {"display": "Test-Driven Development (TDD)", "category": "Testing & QA", "domain": "general"},
    "unit testing": {"display": "Unit Testing", "category": "Testing & QA", "domain": "general"},
    "system design": {"display": "System Design", "category": "Architecture", "domain": "general"},
}


# Pre-packaged Project Recommendations by Domain
DOMAIN_PROJECT_TEMPLATES = {
    "backend": [
        {
            "title": "High-Performance Asynchronous REST API with FastAPI & PostgreSQL",
            "desc": "Architect an enterprise-grade backend service utilizing FastAPI, SQLAlchemy, Pydantic validation, and PostgreSQL. Implement JWT authentication, rate limiting, and automated OpenAPI documentation.",
            "tech_stack": ["FastAPI", "Python", "PostgreSQL", "Docker", "REST API"],
            "key_metric": "Handles 1,500+ requests/sec with sub-25ms response latency under load testing."
        },
        {
            "title": "Automated Web Scraper & Data Ingestion Pipeline with BeautifulSoup",
            "desc": "Build a modular, fault-tolerant web crawler using BeautifulSoup and Requests to collect live market or job listing data, clean the text, and store structured results into an SQLite/PostgreSQL database.",
            "tech_stack": ["Python", "BeautifulSoup", "Pandas", "SQLite", "Cron/Celery"],
            "key_metric": "Automates extraction of 10,000+ daily records with retry logic and proxy rotation."
        },
        {
            "title": "Distributed Asynchronous Task Processing Queue with Celery & Redis",
            "desc": "Develop a background task queue worker in Python using Celery and Redis to offload heavy computations, email notifications, and data transformations from the main web server thread.",
            "tech_stack": ["Python", "Celery", "Redis", "Docker", "Linux"],
            "key_metric": "Decreased web request timeout rate by 99% by offloading long-running async tasks."
        }
    ],
    "data_science": [
        {
            "title": "Interactive Exploratory Data Analysis & Analytics Dashboard using Pandas & Streamlit",
            "desc": "Construct an interactive business analytics dashboard using Pandas, NumPy, and Streamlit. Allow users to upload CSVs, run automated anomaly detection, and visualize trends via Plotly.",
            "tech_stack": ["Python", "Pandas", "NumPy", "Streamlit", "Plotly"],
            "key_metric": "Streamlines executive reporting, cutting manual reporting time by 15 hours per week."
        },
        {
            "title": "Automated Financial / Sales Time-Series Forecasting System",
            "desc": "Build an analytical time-series forecasting model using Pandas and statistical modeling to forecast future metrics with confidence intervals, interactive visualizations, and automated reporting.",
            "tech_stack": ["Python", "Pandas", "Scikit-Learn", "Matplotlib", "Seaborn"],
            "key_metric": "Achieved 92% forecast accuracy with 8% Mean Absolute Percentage Error (MAPE)."
        }
    ],
    "machine_learning": [
        {
            "title": "End-to-End Customer Churn Prediction Engine with Scikit-Learn & XGBoost",
            "desc": "Engineer a complete machine learning pipeline: feature engineering, handling class imbalance (SMOTE), cross-validation, hyperparameter tuning, and model evaluation with ROC-AUC.",
            "tech_stack": ["Python", "Scikit-Learn", "XGBoost", "Pandas", "Joblib"],
            "key_metric": "Boosted model F1-score from 0.64 to 0.88, identifying at-risk customers with 85% precision."
        },
        {
            "title": "Intelligent Resume / Document NLP Classification System with spaCy & TF-IDF",
            "desc": "Create a multi-class document classification model using NLP techniques (tokenization, n-gram TF-IDF vectors, and Naive Bayes / SVM) to automatically categorize resumes into job job roles.",
            "tech_stack": ["Python", "NLP", "Scikit-Learn", "spaCy / NLTK", "FastAPI"],
            "key_metric": "Categorizes 500+ documents/minute with 94.2% test accuracy."
        }
    ],
    "gen_ai": [
        {
            "title": "Retrieval-Augmented Generation (RAG) Knowledge Assistant with LangChain",
            "desc": "Develop a conversational document assistant that embeds internal PDFs/documentation into a vector database, performs semantic similarity search, and queries an LLM for grounded answers.",
            "tech_stack": ["Python", "LangChain", "Vector DB (Chroma/FAISS)", "LLMs", "Streamlit"],
            "key_metric": "Reduced customer query lookup time by 75% while achieving 0% hallucination rate."
        }
    ],
    "devops": [
        {
            "title": "Containerized Microservices CI/CD Pipeline with Docker & GitHub Actions",
            "desc": "Dockerize a Python/FastAPI web service with multi-stage builds. Implement a GitHub Actions workflow that executes linting, unit tests, security scans, and auto-deploys to AWS / GCP.",
            "tech_stack": ["Docker", "GitHub Actions", "CI/CD", "AWS / GCP", "Linux"],
            "key_metric": "Reduced deployment turnaround from 45 minutes to 4 minutes with zero downtime."
        },
        {
            "title": "Automated Cloud Infrastructure Provisioning with Terraform on AWS",
            "desc": "Write modular Infrastructure as Code (IaC) templates in Terraform to provision a secure VPC, RDS PostgreSQL database, and ECS container cluster with auto-scaling and IAM security policies.",
            "tech_stack": ["Terraform", "AWS", "Docker", "Bash", "Linux"],
            "key_metric": "Enabled reproducible one-command environment spinning, cutting setup time by 90%."
        }
    ],
    "database": [
        {
            "title": "Relational Data Modeling & Query Optimization Engine in PostgreSQL",
            "desc": "Design a normalized database schema with complex foreign key constraints, composite B-tree indexes, stored procedures, and benchmarked execution plans using EXPLAIN ANALYZE.",
            "tech_stack": ["PostgreSQL", "SQL", "Database Design", "Indexing", "Python"],
            "key_metric": "Optimized slow query bottlenecks, slashing execution runtime from 4.2s to 85ms."
        }
    ],
    "frontend": [
        {
            "title": "Responsive Single-Page Web Application with React & Tailwind CSS",
            "desc": "Develop a modern responsive user interface in React and TypeScript featuring component modularity, global state management, dark mode theming, and smooth API integration.",
            "tech_stack": ["React", "TypeScript", "Tailwind CSS", "REST API", "Vite"],
            "key_metric": "Achieved a 99/100 Google Lighthouse performance score and full WCAG accessibility."
        }
    ]
}

# Strong Action Verbs Guide
ACTION_VERBS = {
    "Architecture & Development": ["Architected", "Engineered", "Developed", "Spearheaded", "Constructed", "Authored"],
    "Optimization & Performance": ["Optimized", "Accelerated", "Streamlined", "Maximized", "Refactored", "Elevated"],
    "Automation & DevOps": ["Automated", "Containerized", "Provisioned", "Orchestrated", "Deployed", "Standardized"],
    "Leadership & Problem Solving": ["Pioneered", "Championed", "Resolved", "Overhauled", "Transformed", "Identified"]
}

# Google XYZ Formula Examples
XYZ_EXAMPLES = [
    {
        "before": "Worked on Python scripts for our data team.",
        "after": "Engineered automated ETL data extraction pipelines using Python & Pandas, reducing daily ingestion latency by 45% and eliminating manual processing errors for 50,000+ records.",
        "breakdown": "Accomplished [automated ETL pipelines] as measured by [45% latency reduction & 50k records] by doing [Python & Pandas engineering]."
    },
    {
        "before": "Created backend API endpoints with FastAPI.",
        "after": "Architected high-throughput asynchronous REST APIs using FastAPI and PostgreSQL, supporting 1,200+ concurrent requests with sub-30ms response times.",
        "breakdown": "Accomplished [high-throughput REST APIs] as measured by [1,200+ concurrent requests & sub-30ms response] by doing [FastAPI & PostgreSQL architecture]."
    },
    {
        "before": "Helped with machine learning models.",
        "after": "Trained and deployed a predictive classification model using Scikit-Learn and XGBoost, elevating customer retention predictions by 22% and securing an 0.89 ROC-AUC score.",
        "breakdown": "Accomplished [predictive classification model] as measured by [22% retention improvement & 0.89 ROC-AUC] by doing [Scikit-Learn & XGBoost deployment]."
    }
]


# NLP & Text Processing Functions
def clean_text(raw_text: str) -> str:
    """Clean text by lowercasing, stripping punctuation, and removing stopwords."""
    if not raw_text:
        return ""
    # Lowercase
    text = raw_text.lower()
    # Normalize .net before punctuation removal
    text = re.sub(r'(?<!\w)\.net\b', 'dotnet', text)
    # Normalize hyphens and slashes to spaces or preserve for compound terms
    text = re.sub(r'[/\\_]', ' ', text)
    # Remove standard punctuation except '+' (for c++) and '#' (for c#)
    custom_punct = string.punctuation.replace('+', '').replace('#', '')
    translator = str.maketrans('', '', custom_punct)
    text = text.translate(translator)
    # Remove multiple spaces/newlines
    words = text.split()
    # Filter stopwords
    filtered_words = [w for w in words if w not in STOPWORDS and len(w) > 1]
    return " ".join(filtered_words)


def extract_skills_from_text(text: str) -> Set[str]:
    """Identify technical skills and tools from text using boundary matching."""
    text_lower = " " + text.lower() + " "
    # Normalize common symbols
    text_lower = text_lower.replace("/", " ").replace(",", " ").replace(";", " ")
    
    found_skills = set()
    for skill_key in TECHNICAL_SKILLS_TAXONOMY:
        # Match using word boundaries or regex for terms with symbols like c++, c#, .net
        escaped_key = re.escape(skill_key)
        # Handle word boundary or bounded by spaces/punctuation
        pattern = rf'(?:\b|(?<=\s)){escaped_key}(?=\b|(?=\s))'
        if re.search(pattern, text_lower):
            found_skills.add(skill_key)
            
    return found_skills


def extract_tfidf_salient_keywords(jd_text: str, top_n: int = 25) -> List[Tuple[str, float]]:
    """Extract top salient unigrams and bigrams from JD using TF-IDF."""
    cleaned = clean_text(jd_text)
    if not cleaned or len(cleaned.split()) < 3:
        return []
    
    try:
        vectorizer = ActiveTfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            max_features=50
        )
        tfidf_matrix = vectorizer.fit_transform([cleaned])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        
        # Sort by TF-IDF weight
        keyword_scores = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)
        # Filter purely numeric or single character tokens
        valid_keywords = [(kw, round(float(sc), 3)) for kw, sc in keyword_scores if not kw.isnumeric() and len(kw) > 2]
        return valid_keywords[:top_n]
    except Exception:
        return []


def calculate_match_metrics(resume_text: str, jd_text: str, engine: str = "tfidf") -> Dict[str, any]:
    """
    Perform core NLP analysis:
    1. Clean texts
    2. Extract technical skills and TF-IDF keywords
    3. Compare keywords to find matching and missing words
    4. Compute final balanced match score using selected semantic engine (TF-IDF or Sentence-BERT)
    """
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(jd_text)
    
    # 1. Skill Extraction
    jd_skills = extract_skills_from_text(jd_text)
    resume_skills = extract_skills_from_text(resume_text)
    
    matched_skills = sorted(list(jd_skills.intersection(resume_skills)))
    missing_skills = sorted(list(jd_skills.difference(resume_skills)))
    
    # 2. Semantic Similarity Calculation (TF-IDF or Sentence-BERT)
    cosine_sim = 0.0
    engine_used = "TF-IDF Statistical n-gram"
    
    if engine == "sbert" and SENTENCE_TRANSFORMERS_AVAILABLE:
        sbert_sim = compute_sbert_similarity(cleaned_resume, cleaned_jd)
        if sbert_sim > 0.0:
            cosine_sim = sbert_sim
            engine_used = "Sentence-BERT Neural Embeddings (all-MiniLM-L6-v2)"
        else:
            engine = "tfidf"  # fallback
            
    if engine != "sbert" or cosine_sim == 0.0:
        if cleaned_resume and cleaned_jd:
            try:
                tfidf_vec = ActiveTfidfVectorizer(ngram_range=(1, 2), stop_words='english')
                vectors = tfidf_vec.fit_transform([cleaned_resume, cleaned_jd])
                sim_matrix = active_cosine_similarity(vectors[0:1], vectors[1:2])
                cosine_sim = float(sim_matrix[0][0])
                if engine == "sbert":
                    engine_used = "TF-IDF Statistical Fallback (sentence-transformers uninstalled)"
                else:
                    engine_used = "TF-IDF Statistical Vectorizer"
            except Exception:
                cosine_sim = 0.0

    # 3. Calibrated Skill Coverage Ratio
    # Benchmark matches 68% of listed tools to represent 100% target coverage
    if len(jd_skills) > 0:
        raw_skill_ratio = len(matched_skills) / len(jd_skills)
        target_benchmark = len(jd_skills) if len(jd_skills) < 4 else max(4, len(jd_skills) * 0.68)
        skill_coverage = min(len(matched_skills) / target_benchmark, 1.0)
    else:
        raw_skill_ratio = cosine_sim
        skill_coverage = cosine_sim

    # 4. Final Balanced Match Score (Weighted blend: 65% Skill Coverage, 35% Semantic Sim)
    scaled_cosine = min(cosine_sim * 1.35, 1.0)
    final_score_raw = (0.65 * skill_coverage + 0.35 * scaled_cosine) * 100
    final_score = min(max(round(final_score_raw, 1), 0.0), 100.0)

    # 5. Extract Salient TF-IDF Keywords from JD
    salient_jd_keywords = extract_tfidf_salient_keywords(jd_text)
    
    # Check which salient keywords are in the resume
    matched_salient_kw = []
    missing_salient_kw = []
    resume_lower = resume_text.lower()
    for kw, score in salient_jd_keywords:
        if kw in resume_lower:
            matched_salient_kw.append(kw)
        else:
            missing_salient_kw.append(kw)

    # 6. Determine Verdict Status
    if final_score < 50.0:
        verdict_key = "weak"
        verdict_label = "❌ Needs Major Improvement (Weak alignment)"
        verdict_color = "#e63946"
        verdict_advice = (
            "Your resume is missing significant technical skills and core terminology explicitly required "
            "by this job description. To pass applicant tracking systems (ATS) and catch recruiter attention, "
            "incorporate the missing keywords and build targeted portfolio projects highlighting them."
        )
    elif 50.0 <= final_score <= 75.0:
        verdict_key = "moderate"
        verdict_label = "⚠️ Good Start, But Needs Tweaking (Moderate alignment)"
        verdict_color = "#f4a261"
        verdict_advice = (
            "You have a solid foundational overlap with the role, but several important tools and qualifications "
            "are currently absent or understated. Add missing keywords to your experience bullet points, "
            "rephrase duties with quantified metrics, and highlight relevant projects."
        )
    else:
        verdict_key = "strong"
        verdict_label = "✅ Strong Match! Perfect Alignment (Ready to apply)"
        verdict_color = "#2a9d8f"
        verdict_advice = (
            "Outstanding alignment! Your resume closely reflects the technical stack, core terminology, "
            "and qualifications listed in the Job Description. Make sure your impact metrics stand out and you're ready to submit!"
        )

    return {
        "final_score": final_score,
        "cosine_sim_pct": round(cosine_sim * 100, 1),
        "skill_coverage_pct": round(skill_coverage * 100, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_jd_skills_count": len(jd_skills),
        "matched_skills_count": len(matched_skills),
        "missing_skills_count": len(missing_skills),
        "salient_keywords": salient_jd_keywords,
        "matched_salient_kw": matched_salient_kw,
        "missing_salient_kw": missing_salient_kw,
        "verdict_label": verdict_label,
        "verdict_color": verdict_color,
        "verdict_advice": verdict_advice,
        "verdict_key": verdict_key,
        "engine_used": engine_used
    }


def generate_project_recommendations(missing_skills: List[str], jd_text: str) -> List[Dict[str, any]]:
    """
    Intelligently select 2-3 specific, domain-targeted project ideas
    based on missing skills and JD context.
    """
    # Identify which domains have missing skills
    domain_deficit_counter: Counter = Counter()
    missing_skill_objects = []

    for skill_key in missing_skills:
        info = TECHNICAL_SKILLS_TAXONOMY.get(skill_key, {})
        domain = info.get("domain", "backend")
        domain_deficit_counter[domain] += 1
        missing_skill_objects.append(info.get("display", skill_key))

    # Also detect domain clues from the raw JD text if specific skills were sparse
    jd_lower = jd_text.lower()
    if "python" in jd_lower and domain_deficit_counter["backend"] == 0:
        domain_deficit_counter["backend"] += 1
    if any(k in jd_lower for k in ["machine learning", "model", "data science", "nlp"]) and domain_deficit_counter["machine_learning"] == 0:
        domain_deficit_counter["machine_learning"] += 1
    if any(k in jd_lower for k in ["cloud", "docker", "aws", "kubernetes", "ci/cd"]) and domain_deficit_counter["devops"] == 0:
        domain_deficit_counter["devops"] += 1

    # Prioritize domains with highest deficits
    top_domains = [d for d, _ in domain_deficit_counter.most_common(3)]
    if not top_domains:
        top_domains = ["backend", "data_science", "devops"]

    recommended_projects = []
    seen_titles = set()

    for dom in top_domains:
        available_templates = DOMAIN_PROJECT_TEMPLATES.get(dom, [])
        for tmpl in available_templates:
            if tmpl["title"] not in seen_titles:
                # Add project
                recommended_projects.append(tmpl)
                seen_titles.add(tmpl["title"])
                break  # Take top from each domain
            if len(recommended_projects) >= 3:
                break
        if len(recommended_projects) >= 3:
            break

    # If we still have fewer than 2 projects, pad with general backend / data science
    fallback_pool = DOMAIN_PROJECT_TEMPLATES["backend"] + DOMAIN_PROJECT_TEMPLATES["data_science"]
    for tmpl in fallback_pool:
        if tmpl["title"] not in seen_titles and len(recommended_projects) < 3:
            recommended_projects.append(tmpl)
            seen_titles.add(tmpl["title"])

    return recommended_projects[:3]


def parse_uploaded_file(uploaded_file) -> str:
    """Extract text from uploaded PDF, DOCX, or TXT file."""
    filename = uploaded_file.name.lower()
    
    if filename.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")
        
    elif filename.endswith(".pdf"):
        if not PYPDF_AVAILABLE:
            st.error("pypdf is required to read PDF files. Please paste raw text instead.")
            return ""
        try:
            pdf_reader = pypdf.PdfReader(io.BytesIO(uploaded_file.read()))
            text_pages = [page.extract_text() or "" for page in pdf_reader.pages]
            return "\n".join(text_pages)
        except Exception as e:
            st.error(f"Error parsing PDF file: {e}")
            return ""
            
    elif filename.endswith(".docx"):
        if not DOCX_AVAILABLE:
            st.error("python-docx is required to read DOCX files. Please paste raw text instead.")
            return ""
        try:
            doc = docx.Document(io.BytesIO(uploaded_file.read()))
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            st.error(f"Error parsing DOCX file: {e}")
            return ""
            
    else:
        st.error("Unsupported file type. Please upload a .pdf, .docx, or .txt file.")
        return ""


def lint_resume_structure(resume_text: str) -> Dict[str, Any]:
    """
    Performs an automated ATS structural health audit on the candidate resume:
    1. Word count analysis (Density & page brevity)
    2. Contact information detection (Email, Phone, LinkedIn/GitHub/Portfolio)
    3. Essential sections scan (Experience, Education, Skills, Projects)
    4. Quantified metrics index (Numbers, percentages, currency, scale)
    5. Structural health score (0-100) and actionable recommendations
    """
    if not resume_text or not resume_text.strip():
        return {
            "score": 0,
            "verdict": "Empty Resume Document",
            "color": "#ef4444",
            "word_count": 0,
            "word_status": "No text detected",
            "word_color": "#ef4444",
            "contact_info": {"email": False, "phone": False, "links": False},
            "sections": {"experience": False, "education": False, "skills": False, "projects": False},
            "quant_metric_count": 0,
            "quant_status": "Zero metrics detected",
            "recommendations": ["Paste or upload a valid resume document to perform structural analysis."]
        }

    words = resume_text.split()
    word_count = len(words)
    score = 0
    recommendations = []

    # 1. Word Count Evaluation (max 25 pts)
    if 400 <= word_count <= 950:
        score += 25
        word_status = f"Optimal ({word_count} words) — Ideal 1 to 2 page density"
        word_color = "#10b981"
    elif 250 <= word_count < 400:
        score += 18
        word_status = f"Slightly Brief ({word_count} words) — Consider expanding on technical achievements"
        word_color = "#f59e0b"
        recommendations.append("Your resume is under 400 words. Expand upon your technical contributions, projects, and architecture decisions.")
    elif 950 < word_count <= 1300:
        score += 18
        word_status = f"Moderately Dense ({word_count} words) — Ensure high scan-ability"
        word_color = "#f59e0b"
        recommendations.append("Your resume exceeds 950 words. Ensure your most recent impact is on page 1 and remove redundant phrasing.")
    elif word_count < 250:
        score += 8
        word_status = f"Underweight ({word_count} words) — Too short for comprehensive ATS scoring"
        word_color = "#ef4444"
        recommendations.append("Word count is under 250 words. Add explicit project breakdowns, technical toolchains, and work responsibilities.")
    else:
        score += 10
        word_status = f"Overweight ({word_count} words) — High risk of recruiter screening fatigue"
        word_color = "#ef4444"
        recommendations.append("Resume exceeds 1300 words. Condense down to 1-2 pages maximum by trimming passive duty lists.")

    # 2. Contact Information Detection (max 25 pts)
    email_match = bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resume_text))
    phone_match = bool(re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', resume_text))
    links_match = bool(re.search(r'(linkedin\.com|github\.com|portfolio|gitlab\.com|[a-zA-Z0-9-]+\.(io|ai|dev|com))', resume_text, re.IGNORECASE))

    if email_match:
        score += 10
    else:
        recommendations.append("Missing email address: Ensure a direct professional email is clearly visible in the header.")

    if phone_match:
        score += 10
    else:
        recommendations.append("Missing phone contact: Include a standard phone number for recruiters.")

    if links_match:
        score += 5
    else:
        recommendations.append("Missing portfolio links: Adding your GitHub or LinkedIn URL increases recruiter callback rates by over 40%.")

    # 3. Essential Sections Scan (max 35 pts)
    has_exp = bool(re.search(r'\b(experience|employment|work history|career|professional experience)\b', resume_text, re.IGNORECASE))
    has_edu = bool(re.search(r'\b(education|university|college|bachelor|master|phd|degree|b\.s|m\.s|b\.tech|m\.tech|academic)\b', resume_text, re.IGNORECASE))
    has_skills = bool(re.search(r'\b(skills|technical skills|technologies|core competencies|tools|tech stack)\b', resume_text, re.IGNORECASE))
    has_projects = bool(re.search(r'\b(projects|personal projects|academic projects|portfolio|built)\b', resume_text, re.IGNORECASE))

    if has_exp:
        score += 10
    else:
        recommendations.append("No explicit 'Experience' or 'Work History' heading detected.")

    if has_edu:
        score += 10
    else:
        recommendations.append("No explicit 'Education' or 'Academic Background' section detected.")

    if has_skills:
        score += 10
    else:
        recommendations.append("No dedicated 'Technical Skills' section detected. ATS software parses this section first.")

    if has_projects:
        score += 5
    else:
        recommendations.append("Include a dedicated 'Projects' section to demonstrate verified production implementation proof.")

    # 4. Quantification Index & Metric Density (max 15 pts)
    metric_matches = re.findall(r'(\d+[\d,.]*|\d+%\s*|\$\d+[\d,.]*|\b\d+[kKmMbB]\b|\b\d+x\b)', resume_text)
    metric_count = len(metric_matches)

    if metric_count >= 6:
        score += 15
        quant_status = f"Strong Metric Rigor ({metric_count} quantified data points detected)"
    elif 3 <= metric_count < 6:
        score += 10
        quant_status = f"Moderate Metric Rigor ({metric_count} metrics detected)"
        recommendations.append("Increase quantified impact metrics (%, $, latency, user volume) using the Google XYZ formula.")
    elif 1 <= metric_count < 3:
        score += 5
        quant_status = f"Low Metric Density ({metric_count} metric detected)"
        recommendations.append("Very few quantified achievements found. Rephrase duties into measurable results.")
    else:
        score += 0
        quant_status = "Zero Quantified Metrics Detected"
        recommendations.append("Zero numerical metrics detected! Replace passive duties with measurable achievements.")

    # Total Score Normalization
    score = min(max(score, 0), 100)
    if score >= 85:
        verdict = "✅ Excellent ATS Structural Readiness"
        color = "#10b981"
    elif 70 <= score < 85:
        verdict = "⚠️ Good Structure, Minor Enhancements Advised"
        color = "#f59e0b"
    else:
        verdict = "❌ Structural Deficits Detected (Needs Action)"
        color = "#ef4444"

    return {
        "score": score,
        "verdict": verdict,
        "color": color,
        "word_count": word_count,
        "word_status": word_status,
        "word_color": word_color,
        "contact_info": {
            "email": email_match,
            "phone": phone_match,
            "links": links_match
        },
        "sections": {
            "experience": has_exp,
            "education": has_edu,
            "skills": has_skills,
            "projects": has_projects
        },
        "quant_metric_count": metric_count,
        "quant_status": quant_status,
        "recommendations": recommendations
    }


def generate_google_xyz_bullets(
    raw_bullet: str,
    action_verb: str,
    target_keyword: str,
    metric: str
) -> List[Dict[str, str]]:
    """
    Synthesizes 3 high-impact Google XYZ impact variations from user inputs:
    'Accomplished [X] as measured by [Y], by doing [Z]'
    """
    verb = action_verb.strip() if action_verb else "Architected"
    kw = target_keyword.strip() if target_keyword else "scalable microservices"
    met = metric.strip() if metric else "by 25%"
    base = raw_bullet.strip() if raw_bullet else "customer-facing system workflows"
    # Clean trailing period
    base = base.rstrip(".")

    # Template 1: Production Engineering & Scale Focus
    var1 = f"{verb} {base} utilizing {kw}, improving operational throughput {met} across production deployments."
    # Template 2: Performance, Latency & Optimization Focus
    var2 = f"{verb} and containerized automated {kw} pipelines for {base}, achieving {met} reduction in system response latency."
    # Template 3: Reliability & System Architecture Focus
    var3 = f"{verb} an end-to-end {kw} architecture to enhance {base}, driving {met} performance gain while ensuring 99.9% uptime."

    return [
        {"title": "Production Engineering & Scale Focus", "bullet": var1},
        {"title": "Performance & Latency Optimization Focus", "bullet": var2},
        {"title": "Enterprise System Architecture Focus", "bullet": var3}
    ]


def generate_executive_audit_report(
    results: Dict[str, Any],
    jd_text: str,
    resume_text: str,
    linter_results: Dict[str, Any],
    projects: List[Dict[str, Any]],
    candidate_name: str = "",
    candidate_email: str = ""
) -> str:
    """
    Builds a comprehensive, publication-ready Markdown & Plain Text Executive Audit Report.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    score = results.get("final_score", 0)
    verdict = results.get("verdict_label", "N/A")
    skill_pct = results.get("skill_coverage_pct", 0)
    sim_pct = results.get("cosine_sim_pct", 0)
    matched_skills = results.get("matched_skills", [])
    missing_skills = results.get("missing_skills", [])
    salient_present = results.get("matched_salient_kw", [])
    salient_missing = results.get("missing_salient_kw", [])
    engine_name = results.get("engine_used", "TF-IDF Statistical")

    lint_score = linter_results.get("score", 0)
    lint_verdict = linter_results.get("verdict", "N/A")
    word_count = linter_results.get("word_count", 0)
    recommendations = linter_results.get("recommendations", [])

    matched_str = ", ".join([TECHNICAL_SKILLS_TAXONOMY.get(s, {}).get("display", s.upper()) for s in matched_skills]) if matched_skills else "None directly detected"
    missing_str = ", ".join([TECHNICAL_SKILLS_TAXONOMY.get(s, {}).get("display", s.upper()) for s in missing_skills]) if missing_skills else "100% Core Competencies Represented"

    report_lines = [
        "=" * 74,
        "SPARKCV — EXECUTIVE TALENT ALIGNMENT & ATS AUDIT REPORT",
        f"Generated At: {timestamp} | Engine: {engine_name}",
    ]
    if candidate_name:
        user_info = f"Candidate   : {candidate_name}"
        if candidate_email:
            user_info += f" ({candidate_email})"
        report_lines.append(user_info)
    report_lines.extend([
        "=" * 74,
        "",
        "1. EXECUTIVE ALIGNMENT METRICS",
        "-" * 74,
        f"• Overall ATS Match Index       : {score}%",
        f"• Recruitment Alignment Verdict : {verdict}",
        f"• Core Technology Coverage      : {skill_pct}% ({len(matched_skills)} of {results.get('total_jd_skills_count', 0)} tools)",
        f"• Semantic Context Overlap      : {sim_pct}% (Semantic Vector Distance)",
        f"• High-Value Keyword Deficit    : {len(missing_skills)} Critical Gaps to Bridge",
        "",
        "2. RESUME STRUCTURAL HEALTH & ATS LINTER",
        "-" * 74,
        f"• Structural Readiness Score    : {lint_score} / 100",
        f"• Structural Health Status      : {lint_verdict}",
        f"• Document Word Count           : {word_count} words ({linter_results.get('word_status', 'N/A')})",
        f"• Quantified Metric Density     : {linter_results.get('quant_status', 'N/A')}",
        f"• Contact Information Present   : Email: {'✓' if linter_results.get('contact_info', {}).get('email') else '✗'}, Phone: {'✓' if linter_results.get('contact_info', {}).get('phone') else '✗'}, Portfolio/Links: {'✓' if linter_results.get('contact_info', {}).get('links') else '✗'}",
        f"• Core Sections Detected        : Experience: {'✓' if linter_results.get('sections', {}).get('experience') else '✗'}, Education: {'✓' if linter_results.get('sections', {}).get('education') else '✗'}, Skills: {'✓' if linter_results.get('sections', {}).get('skills') else '✗'}, Projects: {'✓' if linter_results.get('sections', {}).get('projects') else '✗'}",
        "",
        "3. COMPETENCY GAP MATRIX",
        "-" * 74,
        f"✅ MATCHED COMPETENCIES ({len(matched_skills)}):",
        f"   {matched_str}",
        "",
        f"❌ MISSING TARGET QUALIFICATIONS ({len(missing_skills)}):",
        f"   {missing_str}",
        "",
        f"📈 SALIENT ATS KEYWORDS (Statistical Salient Extraction):",
        f"   • Present in Resume : {', '.join(salient_present) if salient_present else 'None'}",
        f"   • Missing to Ingest : {', '.join(salient_missing) if salient_missing else 'All Present'}",
        "",
        "4. RECOMMENDED STRATEGIC PORTFOLIO ROADMAPS",
        "-" * 74,
    ])

    for idx, p in enumerate(projects, 1):
        report_lines.append(f"PROJECT #{idx}: {p.get('title', 'N/A')}")
        report_lines.append(f"• Description  : {p.get('desc', 'N/A')}")
        report_lines.append(f"• Tech Stack   : {', '.join(p.get('tech_stack', []))}")
        report_lines.append(f"• Sample Metric: \"{p.get('key_metric', 'N/A')}\"")
        report_lines.append("")

    report_lines.extend([
        "5. STRUCTURAL ACTION ITEMS & CORRECTIVE RECOMMENDATIONS",
        "-" * 74,
    ])
    if recommendations:
        for r in recommendations:
            report_lines.append(f"• [Action Required] {r}")
    else:
        report_lines.append("• [Passed] No major structural red flags detected. Clean ATS formatting.")

    report_lines.extend([
        "",
        "=" * 74,
        "END OF AUDIT REPORT — SPARKCV ENTERPRISE TALENT INTELLIGENCE",
        "=" * 74,
    ])

    return "\n".join(report_lines)


# Sample Data Presets for Instant Testing
SAMPLE_JD_PYTHON_DS = """Senior Python & Data Science Engineer
Company: Alpha Analytics Corp

Job Responsibilities:
- Design, architect, and optimize scalable data analysis pipelines and REST APIs using Python, FastAPI, and PostgreSQL.
- Train, evaluate, and deploy machine learning models using Scikit-Learn, Pandas, NumPy, and XGBoost to predict customer retention.
- Implement NLP and text extraction pipelines using spaCy, NLTK, and Large Language Models (LLMs) with LangChain.
- Containerize application services using Docker and orchestrate deployments on AWS using Kubernetes and CI/CD pipelines.
- Automate external web data scraping with BeautifulSoup and Selenium.
- Collaborate in an Agile/Scrum team, enforcing unit testing, TDD, and clean system design principles.

Qualifications & Requirements:
- 4+ years of professional experience in Python, SQL, and database modeling.
- Solid background in Data Analysis, Pandas, Matplotlib, and Scikit-Learn.
- Demonstrated experience deploying FastAPI or Flask microservices in Docker.
- Experience with Git, Linux environments, and AWS cloud services.
"""

SAMPLE_RESUME_MODERATE = """Alex Chen - Software Developer
Email: alex.chen@example.com | GitHub: github.com/alexchen | LinkedIn: linkedin.com/in/alexchen

Professional Summary:
Passionate Software Developer with 3+ years of hands-on experience building backend web services and microservices. Experienced in Python, Flask, Docker containerization, and relational databases.

Technical Skills:
- Languages: Python, SQL, JavaScript, HTML, CSS
- Web & APIs: Flask, REST API, Microservices
- Databases: PostgreSQL, SQLite, MySQL
- Developer Tools: Docker, Git, Linux, Postman
- Practices: Agile, Scrum, Unit Testing

Professional Experience:
Software Engineer | TechVentures Inc. (2021 - Present)
- Developed and maintained REST APIs and backend microservices using Python and Flask.
- Containerized applications using Docker to standardize development and deployment environments.
- Managed and queried relational database tables using PostgreSQL and SQL, writing complex queries and indexes.
- Collaborated in an Agile/Scrum sprint environment, utilizing Git version control and unit testing.

Junior Web Developer | Innovate Soft (2019 - 2021)
- Built interactive web pages using HTML, CSS, and basic JavaScript.
- Wrote unit tests for backend modules and assisted in debugging server errors on Linux machines.

Education:
B.S. in Computer Science | State University (2019)
"""

SAMPLE_RESUME_WEAK = """Jordan Miller
Customer Support Specialist & Junior Tech Enthusiast
Email: jordan.miller@example.com

Summary:
Detail-oriented customer support specialist transitioning into technology. Passionate about problem-solving, customer satisfaction, and basic coding.

Skills:
Customer Service, Communication, Microsoft Excel, Microsoft Office, JIRA, Basic HTML.

Experience:
Customer Support Representative | CloudCare Solutions (2021 - Present)
- Handled 60+ customer inquiries per day regarding software configurations.
- Documented bug tickets in JIRA for developer review.
- Maintained 98% positive customer satisfaction ratings across all channels.

Retail Associate | City Outfitters (2018 - 2021)
- Managed inventory management and processed point-of-sale transactions.

Education:
B.A. in Communications | City College
"""

SAMPLE_RESUME_STRONG = """Dr. Samantha Reed - Senior Machine Learning & Python Engineer
Email: samantha.reed@example.com | Phone: (555) 234-5678 | LinkedIn: linkedin.com/in/samanthareed | Portfolio: samanthareed.ai

Professional Summary:
Accomplished Senior AI/ML Engineer with 6+ years of expertise architecting and deploying production-grade machine learning pipelines, high-throughput FastAPI microservices, and large-scale NLP applications. Specialized in Scikit-Learn, Pandas, PyTorch, AWS cloud infrastructure, and Docker containerization. Proven track record leading Agile engineering squads, optimizing distributed databases, and delivering mission-critical artificial intelligence products that serve millions of daily requests with high reliability.

Technical Skills:
- Programming Languages: Python, SQL, Bash, Go
- ML/AI & Data Science: Scikit-Learn, Pandas, NumPy, XGBoost, NLP, spaCy, NLTK, LangChain, LLMs, Matplotlib, Data Analysis
- Backend & Web Services: FastAPI, Flask, REST API, Microservices, Asynchronous Workflows, BeautifulSoup
- Cloud & Infrastructure: AWS (ECS, S3, RDS), Docker, Kubernetes, CI/CD, Git, Linux, System Design
- Practices & Architecture: Agile, Scrum, Unit Testing, Test-Driven Development (TDD), Code Reviews
- Databases & Storage: PostgreSQL, Redis, DynamoDB

Professional Experience:
Lead Machine Learning Engineer | DataVision Labs (2021 - Present)
- Architected and deployed scalable machine learning microservices using Python and FastAPI, serving 2,000,000+ daily inference requests with sub-25ms latency.
- Engineered automated data extraction and NLP pipelines using spaCy, Pandas, and Scikit-Learn with 94.5% classification precision, reducing manual review by 60%.
- Containerized multi-service architectures using Docker, automated deployment pipelines with AWS and GitHub Actions CI/CD to accelerate releases by 3.5x.
- Implemented automated web scrapers using BeautifulSoup to reliably ingest 50,000+ daily market signals into PostgreSQL.

Senior Machine Learning Developer | Apex Innovations (2018 - 2021)
- Built and tuned customer churn predictive models using XGBoost, Scikit-Learn, and Pandas, elevating retention by 28% and generating $450,000 in saved contract value.
- Designed and documented RESTful APIs in an Agile/Scrum cross-functional team with rigorous unit testing and TDD, reaching 95% test coverage across core codebases.
- Mentored 4 junior engineers on clean code practices, distributed training paradigms, and Git version control.

Education:
Ph.D. in Computer Science & Artificial Intelligence | Stanford University (2018)
B.S. in Applied Mathematics & Statistics | UC Berkeley (2014)

Projects & Key Implementations:
- Open-Source Semantic Search Engine: Engineered vector similarity search indexing 100,000+ documents using LangChain and FastAPI.
"""


# Streamlit Application Main Interface - SparkCV Executive Frontend
def main():
    if not STREAMLIT_AVAILABLE:
        print("Streamlit is not installed. Please install requirements or run with Streamlit.")
        return

    st.set_page_config(
        page_title="SparkCV — Enterprise Job Description Analyzer & Resume Optimizer",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    bg_b64 = get_background_image_base64()
    if bg_b64:
        bg_style = f"""
        background-color: #070a13 !important;
        background-image: 
            linear-gradient(135deg, rgba(7, 12, 24, 0.78) 0%, rgba(5, 8, 18, 0.85) 100%),
            url('data:image/webp;base64,{bg_b64}') !important;
        background-size: cover !important;
        background-position: center center !important;
        background-attachment: fixed !important;
        background-repeat: no-repeat !important;
        """
    else:
        bg_style = """
        background-color: #070a13 !important;
        background-image: 
            radial-gradient(rgba(56, 189, 248, 0.08) 1.2px, transparent 1.2px),
            radial-gradient(ellipse 80% 50% at 20% -10%, rgba(14, 116, 144, 0.32) 0%, transparent 60%),
            radial-gradient(ellipse 60% 60% at 85% 15%, rgba(126, 34, 206, 0.28) 0%, transparent 60%),
            radial-gradient(ellipse 70% 60% at 50% 95%, rgba(2, 132, 199, 0.22) 0%, transparent 65%),
            radial-gradient(ellipse 50% 40% at 10% 85%, rgba(16, 185, 129, 0.15) 0%, transparent 55%) !important;
        background-size: 32px 32px, 150% 150%, 150% 150%, 150% 150%, 150% 150% !important;
        background-position: 0 0, 0% 0%, 100% 0%, 50% 100%, 0% 100% !important;
        animation: auroraMeshShift 18s ease-in-out infinite alternate !important;
        """

    css_content = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800;900&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-deep: #060504;
        --card-surface: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%);
        --card-border: rgba(212, 175, 55, 0.38);
        --card-border-glow: rgba(212, 175, 55, 0.65);
        --gold-light: #fef3c7;
        --gold-mid: #caa14c;
        --gold-dark: #966c1b;
        --accent-emerald: #10b981;
        --accent-rose: #f43f5e;
    }

    /* Executive Luxury Background Canvas */
    .stApp {
        __APP_BG_STYLE__
        font-family: 'Inter', -apple-system, sans-serif !important;
        color: #fdfbf7 !important;
        overflow-x: hidden !important;
    }

    /* Clean Streamlit Default Chrome */
    #MainMenu, footer, header { visibility: hidden !important; }

    /* Custom Webkit Scrollbars with Radiant Gold Accent */
    ::-webkit-scrollbar { width: 7px; height: 7px; }
    ::-webkit-scrollbar-track { background: #060504; }
    ::-webkit-scrollbar-thumb { 
        background: #1a1612; 
        border-radius: 4px; 
        border: 1px solid rgba(212, 175, 55, 0.3); 
        transition: background 0.25s ease;
    }
    ::-webkit-scrollbar-thumb:hover { 
        background: #caa14c; 
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.6);
    }

    /* Keyframe Animation Library */
    @keyframes heroEntrance {
        0% { opacity: 0; transform: translateY(-18px); filter: blur(3px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }

    @keyframes cardFadeInUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes borderSweep {
        0% { transform: translateX(0); }
        100% { transform: translateX(50%); }
    }

    @keyframes radarPing {
        0% { transform: scale(0.8); opacity: 1; }
        80%, 100% { transform: scale(2.4); opacity: 0; }
    }

    /* SparkCV Brand Dashboard Banner */
    .sparkcv-hero-card {
        background: radial-gradient(ellipse at 50% 12%, rgba(28, 24, 20, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%);
        border: 1px solid rgba(212, 175, 55, 0.42);
        border-radius: 20px;
        padding: 34px 32px;
        margin-bottom: 26px;
        text-align: center;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.92), 0 0 35px rgba(212, 175, 55, 0.16);
        animation: heroEntrance 0.85s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .sparkcv-hero-card::before {
        content: '';
        position: absolute;
        top: 0; left: -100%; width: 200%; height: 2px;
        background: linear-gradient(90deg, transparent, #d4af37, #fef3c7, #caa14c, #d4af37, transparent);
        animation: borderSweep 5s linear infinite;
    }

    .hero-badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(18, 15, 12, 0.75);
        color: #d4af37;
        border: 1px solid rgba(212, 175, 55, 0.45);
        padding: 6px 18px;
        border-radius: 30px;
        font-family: 'Cinzel', serif;
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 15px;
        box-shadow: 0 0 14px rgba(212, 175, 55, 0.15);
    }

    .live-beacon-dot {
        width: 8px;
        height: 8px;
        background-color: #d4af37;
        border-radius: 50%;
        display: inline-block;
        position: relative;
    }
    .live-beacon-dot::after {
        content: '';
        position: absolute;
        top: -3px; left: -3px; right: -3px; bottom: -3px;
        border-radius: 50%;
        border: 2px solid #d4af37;
        animation: radarPing 1.8s cubic-bezier(0, 0, 0.2, 1) infinite;
    }

    .brand-title-hero {
        font-family: 'Cinzel', serif;
        font-size: 3.25rem;
        font-weight: 800;
        line-height: 1.15;
        background: linear-gradient(180deg, #fef3c7 0%, #e2be67 45%, #b4852e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        letter-spacing: 0.04em;
        text-shadow: 0 2px 14px rgba(212, 175, 55, 0.25);
    }

    .hero-tagline {
        font-size: 1.02rem;
        color: #c8bcab;
        max-width: 840px;
        margin: 0 auto 18px auto;
        line-height: 1.65;
    }

    .hero-chips-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 10px;
    }
    .hero-meta-chip {
        background: rgba(14, 12, 10, 0.9);
        border: 1px solid rgba(212, 175, 55, 0.25);
        color: #d8cebe;
        font-size: 0.8rem;
        font-weight: 500;
        padding: 6px 14px;
        border-radius: 8px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .hero-meta-chip:hover {
        background: rgba(212, 175, 55, 0.18);
        border-color: rgba(212, 175, 55, 0.6);
        color: #fef08a;
        transform: translateY(-2px);
        box-shadow: 0 4px 14px rgba(212, 175, 55, 0.25);
    }

    /* Executive Sidebar Glass Styling */
    [data-testid="stSidebar"] {
        background: radial-gradient(ellipse at 50% 12%, rgba(20, 16, 13, 0.98) 0%, rgba(8, 7, 6, 0.99) 100%) !important;
        border-right: 1px solid rgba(212, 175, 55, 0.25) !important;
    }
    .sidebar-control-box {
        background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%);
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.5);
        transition: border-color 0.25s ease;
    }
    .sidebar-control-box:hover {
        border-color: rgba(212, 175, 55, 0.55);
        box-shadow: 0 8px 24px rgba(212, 175, 55, 0.15);
    }
    .sidebar-control-title {
        font-family: 'Cinzel', serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: #d4af37;
        text-transform: uppercase;
        letter-spacing: 0.75px;
        margin-bottom: 4px;
    }

    /* Input Panels & Dropzones */
    .panel-header-wrap {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
    }
    .panel-tag {
        background: rgba(212, 175, 55, 0.15);
        color: #fef08a;
        border: 1px solid rgba(212, 175, 55, 0.35);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .panel-chip {
        background: rgba(212, 175, 55, 0.15);
        color: #fef08a;
        border: 1px solid rgba(212, 175, 55, 0.35);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* Fluid Textarea with Radiant Gold Focus Ring */
    .stTextArea textarea {
        background-color: rgba(14, 12, 10, 0.92) !important;
        color: #fdfbf7 !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 14px !important;
        font-size: 0.92rem !important;
        line-height: 1.6 !important;
        padding: 16px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.6) !important;
    }
    .stTextArea textarea:focus {
        border-color: #d4af37 !important;
        box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.28), 0 0 25px rgba(212, 175, 55, 0.25) !important;
        background-color: rgba(18, 15, 12, 0.98) !important;
        transform: translateY(-1px) !important;
    }

    /* Fluid Radio Pill Bar */
    .stRadio > div {
        background: rgba(14, 12, 10, 0.88);
        border: 1px solid rgba(212, 175, 55, 0.28);
        border-radius: 12px;
        padding: 6px 12px;
        display: flex;
        gap: 12px;
        transition: border-color 0.25s ease;
    }
    .stRadio > div:hover {
        border-color: rgba(212, 175, 55, 0.5);
    }
    .stRadio label {
        color: #d8cebe !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }

    /* High-Impact Primary Action Button with Brushed Gold Metallic Gradient */
    .stButton button[kind="primary"] {
        background: linear-gradient(180deg, #f7dd96 0%, #caa14c 45%, #966c1b 100%) !important;
        color: #161005 !important;
        border: 1px solid rgba(254, 240, 138, 0.65) !important;
        border-radius: 12px !important;
        padding: 16px 36px !important;
        font-family: 'Cinzel', serif !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.12em !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.7), 0 0 25px rgba(212, 175, 55, 0.35) !important;
    }
    .stButton button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.01) !important;
        filter: brightness(1.08) !important;
        box-shadow: 0 10px 32px rgba(0, 0, 0, 0.8), 0 0 35px rgba(212, 175, 55, 0.5) !important;
    }
    .stButton button[kind="primary"]:active {
        transform: translateY(1px) scale(0.99) !important;
    }

    /* Secondary Preset Buttons */
    .stButton button:not([kind="primary"]) {
        background: rgba(18, 15, 12, 0.85) !important;
        color: #e2be67 !important;
        border: 1px solid rgba(212, 175, 55, 0.32) !important;
        border-radius: 10px !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        letter-spacing: 0.05em !important;
        transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .stButton button:not([kind="primary"]):hover {
        background: rgba(212, 175, 55, 0.2) !important;
        border-color: #d4af37 !important;
        color: #fef08a !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 18px rgba(212, 175, 55, 0.3) !important;
    }

    /* Floating Metrics Quad Grid */
    .floating-metric-card {
        background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%);
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 16px;
        padding: 22px 18px;
        text-align: center;
        backdrop-filter: blur(16px);
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 12px 30px -6px rgba(0, 0, 0, 0.7);
        position: relative;
        overflow: hidden;
        animation: cardFadeInUp 0.65s cubic-bezier(0.16, 1, 0.3, 1) both;
    }
    .floating-metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(212, 175, 55, 0.65);
        box-shadow: 0 18px 36px -6px rgba(0, 0, 0, 0.8), 0 0 25px rgba(212, 175, 55, 0.22);
    }
    .metric-caption-title {
        font-family: 'Cinzel', serif;
        font-size: 0.78rem;
        font-weight: 700;
        color: #c8bcab;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }
    .metric-hero-val {
        font-size: 2.75rem;
        font-weight: 800;
        line-height: 1.05;
        margin: 8px 0;
        font-family: 'Cinzel', serif;
        letter-spacing: -0.5px;
    }
    .metric-sub-pill {
        font-size: 0.78rem;
        color: #e2be67;
        font-weight: 600;
        background: rgba(18, 15, 12, 0.85);
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
        border: 1px solid rgba(212, 175, 55, 0.25);
    }

    /* Executive Verdict Appraisal Card */
    .verdict-banner-card {
        background: radial-gradient(ellipse at 50% 12%, rgba(28, 24, 20, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%);
        border: 1px solid rgba(212, 175, 55, 0.42);
        border-radius: 18px;
        padding: 26px 30px;
        margin: 26px 0;
        backdrop-filter: blur(16px);
        position: relative;
        box-shadow: 0 18px 40px -8px rgba(0, 0, 0, 0.8), 0 0 30px rgba(212, 175, 55, 0.12);
    }
    .verdict-header-badge {
        font-family: 'Cinzel', serif;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 5px 14px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 12px;
    }

    /* Tabs Engine Overhaul */
    .stTabs [data-baseweb="tab-list"] {
        background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%) !important;
        border: 1px solid rgba(212, 175, 55, 0.35) !important;
        border-radius: 14px !important;
        padding: 6px !important;
        gap: 8px !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        color: #a89c8b !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        padding: 10px 18px !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.25s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #fef08a !important;
        background: rgba(212, 175, 55, 0.15) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #f7dd96 0%, #caa14c 45%, #966c1b 100%) !important;
        color: #161005 !important;
        border: 1px solid rgba(254, 240, 138, 0.6) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5), 0 0 16px rgba(212, 175, 55, 0.3) !important;
    }
    .stTabs [aria-selected="true"] * {
        color: #161005 !important;
        font-weight: 800 !important;
    }

    /* Competency Badges with Interactive Spring Hover */
    .badge-match {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.14);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 6px 14px;
        margin: 4px;
        border-radius: 9px;
        font-size: 0.85rem;
        font-weight: 600;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .badge-match:hover {
        transform: translateY(-2px) scale(1.04);
        background: rgba(16, 185, 129, 0.28);
        border-color: #34d399;
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.3);
    }
    .badge-miss {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(244, 63, 94, 0.14);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.4);
        padding: 6px 14px;
        margin: 4px;
        border-radius: 9px;
        font-size: 0.85rem;
        font-weight: 600;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .badge-miss:hover {
        transform: translateY(-2px) scale(1.04);
        background: rgba(244, 63, 94, 0.28);
        border-color: #fb7185;
        box-shadow: 0 6px 16px rgba(244, 63, 94, 0.3);
    }

    /* Executive Project Recommendation Card with Slide Reveal */
    .project-card-pro {
        background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%);
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-left: 5px solid #d4af37;
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 22px;
        backdrop-filter: blur(14px);
        box-shadow: 0 14px 30px -6px rgba(0, 0, 0, 0.7);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
    }
    .project-card-pro:hover {
        transform: translateX(8px);
        border-color: rgba(212, 175, 55, 0.65);
        border-left-width: 9px;
        box-shadow: 0 18px 38px -6px rgba(0, 0, 0, 0.8), 0 0 25px rgba(212, 175, 55, 0.25);
    }
    .project-title-pro {
        font-family: 'Cinzel', serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #fef08a;
        margin-bottom: 8px;
    }
    .project-desc-pro {
        color: #d8cebe;
        font-size: 0.94rem;
        line-height: 1.6;
        margin-bottom: 12px;
    }
    .project-metric-pro {
        background: rgba(14, 12, 10, 0.95);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 10px;
        padding: 14px 18px;
        font-size: 0.9rem;
        color: #fdfbf7;
        margin-top: 14px;
    }

    /* High-Impact Action Verb Badges */
    .action-badge {
        display: inline-block;
        background: rgba(212, 175, 55, 0.14);
        color: #fef08a;
        border: 1px solid rgba(212, 175, 55, 0.35);
        padding: 5px 12px;
        margin: 3px;
        border-radius: 7px;
        font-size: 0.83rem;
        font-weight: 600;
        transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .action-badge:hover {
        background: rgba(212, 175, 55, 0.28);
        color: #ffffff;
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 4px 14px rgba(212, 175, 55, 0.3);
    }

    /* Google XYZ Callout Box */
    .xyz-formula-card {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(140, 100, 24, 0.28) 100%);
        border: 1px solid rgba(212, 175, 55, 0.5);
        border-radius: 14px;
        padding: 18px 24px;
        margin-bottom: 24px;
        font-family: 'Cinzel', serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #fef08a;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 8px 22px -4px rgba(0, 0, 0, 0.5), 0 0 20px rgba(212, 175, 55, 0.15);
    }

    /* Aesthetic Luxury Executive Login Portal Styles (Exact Match to Reference Image) */
    .luxury-login-card {
        background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%);
        border: 1px solid rgba(212, 175, 55, 0.42);
        border-radius: 18px;
        padding: 38px 36px 24px 36px;
        box-shadow: 
            0 30px 80px -10px rgba(0, 0, 0, 0.98),
            0 0 45px rgba(212, 175, 55, 0.16),
            inset 0 1px 1px rgba(254, 240, 138, 0.28),
            inset 0 0 20px rgba(0, 0, 0, 0.8);
        position: relative;
        text-align: center;
        margin-bottom: 20px;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        animation: heroEntrance 0.85s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .login-crest-wrap {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 10px;
    }
    .login-crest-img {
        width: 68px;
        height: auto;
        filter: drop-shadow(0 2px 10px rgba(212, 175, 55, 0.35));
    }

    .brand-title-login {
        font-family: 'Cinzel', 'Playfair Display', serif;
        font-size: 2.25rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin: 0 0 10px 0;
        background: linear-gradient(180deg, #fef3c7 0%, #e2be67 45%, #b4852e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 14px rgba(212, 175, 55, 0.25);
        line-height: 1.1;
    }

    .badge-private-access {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 14px;
        background: rgba(18, 15, 12, 0.75);
        border: 1px solid rgba(212, 175, 55, 0.45);
        border-radius: 9999px;
        color: #d4af37;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        margin-bottom: 18px;
        box-shadow: 0 0 14px rgba(212, 175, 55, 0.12);
    }
    .badge-bracket {
        color: #caa14c;
        font-weight: 300;
        opacity: 0.8;
    }

    .executive-title {
        font-family: 'Cinzel', 'Playfair Display', serif;
        font-size: 1.45rem;
        font-weight: 600;
        color: #f1ddaa;
        margin: 0 0 6px 0;
        letter-spacing: 0.02em;
    }

    .executive-subtitle {
        font-size: 0.78rem;
        color: #a89c8b;
        margin: 0 0 20px 0;
        font-weight: 400;
        letter-spacing: 0.01em;
        line-height: 1.4;
    }

    /* Style Streamlit Inputs & Buttons inside Login Card */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }

    div[data-testid="stForm"] div[data-testid="stTextInput"] input {
        background: rgba(13, 11, 10, 0.9) !important;
        border: 1px solid rgba(212, 175, 55, 0.28) !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
        font-size: 0.88rem !important;
        padding: 10px 14px !important;
        transition: all 0.25s ease !important;
    }
    div[data-testid="stForm"] div[data-testid="stTextInput"] input:focus {
        border-color: #d4af37 !important;
        background: rgba(18, 15, 13, 0.98) !important;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.35) !important;
        outline: none !important;
    }
    div[data-testid="stForm"] label {
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        color: #c8bcab !important;
        letter-spacing: 0.02em !important;
    }

    div[data-testid="stFormSubmitButton"] > button {
        width: 100% !important;
        height: 46px !important;
        background: linear-gradient(180deg, #f7dd96 0%, #caa14c 45%, #966c1b 100%) !important;
        border: 1px solid rgba(254, 240, 138, 0.65) !important;
        border-radius: 8px !important;
        color: #161005 !important;
        font-family: 'Cinzel', serif !important;
        font-size: 0.94rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.18em !important;
        cursor: pointer !important;
        transition: all 0.25s ease !important;
        box-shadow: 
            0 4px 18px rgba(0, 0, 0, 0.6),
            inset 0 1px 1px rgba(255, 255, 255, 0.65),
            inset 0 -1px 2px rgba(0, 0, 0, 0.4) !important;
        margin-top: 8px !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        filter: brightness(1.08) !important;
        box-shadow: 0 6px 24px rgba(212, 175, 55, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.85) !important;
        transform: translateY(-1px) !important;
    }

    .forgot-link-btn button {
        background: transparent !important;
        border: none !important;
        color: #caa14c !important;
        font-size: 0.76rem !important;
        padding: 0 !important;
        text-decoration: none !important;
    }
    .forgot-link-btn button:hover {
        color: #fef08a !important;
        text-decoration: underline !important;
    }

    .login-footer-text {
        margin-top: 18px;
        padding-top: 14px;
        border-top: 1px solid rgba(212, 175, 55, 0.12);
        font-size: 0.68rem;
        color: #7a7062;
        letter-spacing: 0.02em;
        line-height: 1.4;
        text-align: center;
    }
    /* Luxury Top User Status Bar */
    .luxury-user-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%);
        border: 1px solid rgba(212, 175, 55, 0.42);
        border-radius: 16px;
        padding: 12px 22px;
        margin-bottom: 22px;
        box-shadow: 0 12px 35px -5px rgba(0, 0, 0, 0.85), 0 0 25px rgba(212, 175, 55, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }
    .luxury-user-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .luxury-user-title {
        font-family: 'Cinzel', serif;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        color: #d4af37;
        text-transform: uppercase;
    }
    .luxury-user-meta {
        font-size: 0.88rem;
        color: #fdfbf7;
    }
    .luxury-session-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 14px;
        background: rgba(212, 175, 55, 0.12);
        border: 1px solid rgba(212, 175, 55, 0.45);
        border-radius: 9999px;
        color: #fef08a;
        font-family: 'Cinzel', serif;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        box-shadow: 0 0 14px rgba(212, 175, 55, 0.15);
    }

    /* Executive Audit Report Download Button - High Visibility Brushed Gold */
    div.stDownloadButton,
    div[data-testid="stDownloadButton"] {
        display: flex !important;
        align-items: center !important;
    }
    div.stDownloadButton > button,
    div[data-testid="stDownloadButton"] > button,
    div[data-testid="stDownloadButton"] button {
        background: linear-gradient(180deg, #f7dd96 0%, #caa14c 45%, #966c1b 100%) !important;
        color: #161005 !important;
        border: 1px solid rgba(254, 240, 138, 0.7) !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-family: 'Cinzel', serif !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        cursor: pointer !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6), 0 0 20px rgba(212, 175, 55, 0.35) !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
    }
    div.stDownloadButton > button:hover,
    div[data-testid="stDownloadButton"] > button:hover,
    div[data-testid="stDownloadButton"] button:hover {
        filter: brightness(1.08) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.7), 0 0 28px rgba(212, 175, 55, 0.5) !important;
    }
    div.stDownloadButton > button:active,
    div[data-testid="stDownloadButton"] > button:active,
    div[data-testid="stDownloadButton"] button:active {
        transform: translateY(1px) !important;
    }
    div.stDownloadButton > button *,
    div[data-testid="stDownloadButton"] > button *,
    div[data-testid="stDownloadButton"] button * {
        color: #161005 !important;
        font-weight: 800 !important;
        font-family: 'Cinzel', serif !important;
    }

    /* Form Submit Button */
    div[data-testid="stFormSubmitButton"] > button,
    .stFormSubmitButton > button {
        background: linear-gradient(180deg, #f7dd96 0%, #caa14c 45%, #966c1b 100%) !important;
        color: #161005 !important;
        border: 1px solid rgba(254, 240, 138, 0.65) !important;
        border-radius: 12px !important;
        padding: 13px 26px !important;
        font-family: 'Cinzel', serif !important;
        font-size: 0.98rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.12em !important;
        transition: all 0.28s ease !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6), 0 0 20px rgba(212, 175, 55, 0.35) !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover,
    .stFormSubmitButton > button:hover {
        filter: brightness(1.08) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.7), 0 0 28px rgba(212, 175, 55, 0.5) !important;
    }
    div[data-testid="stFormSubmitButton"] > button *,
    .stFormSubmitButton > button * {
        color: #161005 !important;
        font-weight: 800 !important;
        font-family: 'Cinzel', serif !important;
    }
    </style>
    """
    st.markdown(css_content.replace("__APP_BG_STYLE__", bg_style), unsafe_allow_html=True)

    # Initialize Session State
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""
    if "resume_text" not in st.session_state:
        st.session_state.resume_text = ""
    if "jd_text" not in st.session_state:
        st.session_state.jd_text = ""
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    if "linter_results" not in st.session_state:
        st.session_state.linter_results = None
    if "semantic_engine" not in st.session_state:
        st.session_state.semantic_engine = "tfidf"

    # Gated Executive Authentication Portal
    if not st.session_state.is_authenticated:
        # Hide sidebar and header during login, set luxury velvet sunbeam background
        bg_b64 = get_login_bg_base64()
        crest_b64 = get_login_crest_base64()

        st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: #060504 url('data:image/webp;base64,{bg_b64}') center center / cover no-repeat fixed !important;
        }}
        [data-testid="stSidebar"] {{ display: none !important; }}
        .stApp > header {{ display: none !important; }}
        .stMainBlockContainer {{ max-width: 500px !important; margin: 0 auto !important; padding-top: 60px !important; }}
        </style>
        """, unsafe_allow_html=True)

        crest_img_tag = f'<img src="data:image/png;base64,{crest_b64}" alt="SparkCV Crest" class="login-crest-img" />' if crest_b64 else '<span style="font-size: 2rem;">👑</span>'

        st.markdown(f"""
        <div class="luxury-login-card">
            <div class="login-crest-wrap">
                {crest_img_tag}
            </div>
            <div class="brand-title-login">SparkCV</div>
            <div class="badge-private-access">
                <span class="badge-bracket">⟨</span> PRIVATE ACCESS <span class="badge-bracket">⟩</span>
            </div>
            <div class="executive-title">Executive Login</div>
            <div class="executive-subtitle">Enter your credentials to access the executive dashboard</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("luxury_login_form"):
            user_email_input = st.text_input("Executive ID / Email", placeholder="name@sparkcv.com", key="input_user_email")
            user_pwd_input = st.text_input("Password", type="password", placeholder="••••••••••••", key="input_user_pwd")

            col_rem, col_fgt = st.columns([1.3, 1])
            with col_rem:
                st.checkbox("Remember me for 30 days", value=True, key="login_remember_me")
            with col_fgt:
                st.markdown("<div style='text-align: right; margin-top: 4px;'><a href='javascript:void(0)' onclick='alert(\"🔒 Security Protocol: Password recovery instructions have been dispatched to your corporate security administrator.\")' style='color: #caa14c; font-size: 0.78rem; text-decoration: none;'>Forgot password?</a></div>", unsafe_allow_html=True)

            login_btn = st.form_submit_button("LOGIN", use_container_width=True)

            if login_btn:
                if not user_email_input.strip():
                    st.error("Please enter your Executive ID or Email.")
                elif not user_pwd_input.strip():
                    st.error("Please enter your Password.")
                else:
                    st.session_state.is_authenticated = True
                    email = user_email_input.strip()
                    if "@" in email:
                        prefix = email.split("@")[0]
                        name = " ".join(part.capitalize() for part in re.split(r"[._-]", prefix))
                    else:
                        name = email.capitalize()
                    st.session_state.user_name = name
                    st.session_state.user_email = email
                    st.rerun()

        st.markdown("""
        <div class="login-footer-text">
            Secured with 256-bit encryption • Restricted to authorized executives only
        </div>
        """, unsafe_allow_html=True)

        return

    # Luxury Top User Navigation Bar
    top_col1, top_col2 = st.columns([3.2, 0.8])
    with top_col1:
        crest_b64 = get_login_crest_base64()
        crest_html = f'<img src="data:image/png;base64,{crest_b64}" alt="Crest" style="width: 32px; height: auto; filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.5));">' if crest_b64 else '👑'
        st.markdown(f"""
        <div class="luxury-user-bar">
            <div class="luxury-user-left">
                {crest_html}
                <div>
                    <div class="luxury-user-title">SparkCV Executive Suite</div>
                    <div class="luxury-user-meta">Candidate: <strong style="color: #fdfbf7;">{st.session_state.user_name}</strong> &nbsp;•&nbsp; <span style="color:#c8bcab;">{st.session_state.user_email}</span></div>
                </div>
            </div>
            <div class="luxury-session-badge">
                <span class="live-beacon-dot"></span> ACTIVE SESSION
            </div>
        </div>
        """, unsafe_allow_html=True)
    with top_col2:
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        if st.button("🚪 Sign Out", key="auth_signout_btn", use_container_width=True, help="Sign out and return to the luxury login portal"):
            st.session_state.is_authenticated = False
            st.session_state.user_name = ""
            st.session_state.user_email = ""
            st.rerun()

    # Executive Dashboard Hero Header
    crest_b64 = get_login_crest_base64()
    hero_crest_html = f'<img src="data:image/png;base64,{crest_b64}" alt="SparkCV Crest" style="width: 52px; height: auto; margin-bottom: 8px; filter: drop-shadow(0 2px 10px rgba(212, 175, 55, 0.4));">' if crest_b64 else ''
    st.markdown(f"""
    <div class="sparkcv-hero-card">
        {hero_crest_html}
        <div class="brand-title-hero">SparkCV</div>
        <div class="hero-badge-pill"><span class="live-beacon-dot"></span> Enterprise Talent Intelligence Engine</div>
        <div class="hero-tagline">
            Smart Job Description Analyzer & Resume Optimization System. Advanced NLP semantic alignment,
            predictive ATS keyword gap scoring, and automated candidate portfolio recommendations for executive talent decisions.
        </div>
        <div class="hero-chips-container">
            <span class="hero-meta-chip">🎯 Weighted ATS Scoring</span>
            <span class="hero-meta-chip">🧠 TF-IDF Salient Extraction</span>
            <span class="hero-meta-chip">📊 250+ Tech Skills Taxonomy</span>
            <span class="hero-meta-chip">🚀 Tailored Portfolio Roadmaps</span>
            <span class="hero-meta-chip">✍️ Google XYZ Metric Formulation</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Executive Sidebar
    with st.sidebar:
        # Feature 2: Engine Selector Toggle
        st.markdown("""
        <div class="sidebar-control-box">
            <div class="sidebar-control-title">🧠 Semantic Engine Mode</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 8px;">Select similarity calculation algorithm:</div>
        </div>
        """, unsafe_allow_html=True)

        engine_options = [
            "⚡ Fast TF-IDF (Scikit-Learn)",
            "🤖 Sentence-BERT (MiniLM-L6)"
        ]
        curr_index = 0 if st.session_state.semantic_engine == "tfidf" else 1
        selected_engine_label = st.radio(
            "Semantic Engine:",
            engine_options,
            index=curr_index,
            label_visibility="collapsed"
        )
        engine_key = "tfidf" if "TF-IDF" in selected_engine_label else "sbert"
        if engine_key != st.session_state.semantic_engine:
            st.session_state.semantic_engine = engine_key
            st.session_state.analysis_results = None
            st.rerun()

        if engine_key == "sbert" and not SENTENCE_TRANSFORMERS_AVAILABLE:
            st.info("💡 **Sentence-BERT Mode**: `sentence-transformers` is not currently installed. To activate local neural weights, run `pip install sentence-transformers`. Falling back to TF-IDF automatically.")

        st.markdown("""
        <div class="sidebar-control-box" style="margin-top: 14px;">
            <div class="sidebar-control-title">HR Stakeholder Panel</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">Preset evaluation profiles for executive demonstrations:</div>
        </div>
        """, unsafe_allow_html=True)

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("📊 Moderate (~55%)", help="Loads a developer profile matching ~55% of the target role", use_container_width=True):
                st.session_state.jd_text = SAMPLE_JD_PYTHON_DS
                st.session_state.resume_text = SAMPLE_RESUME_MODERATE
                st.session_state.analysis_results = None
                st.session_state.linter_results = None
                st.rerun()

        with col_b2:
            if st.button("🌟 Strong (>80%)", help="Loads a Senior AI Engineer profile exceeding 80% alignment", use_container_width=True):
                st.session_state.jd_text = SAMPLE_JD_PYTHON_DS
                st.session_state.resume_text = SAMPLE_RESUME_STRONG
                st.session_state.analysis_results = None
                st.session_state.linter_results = None
                st.rerun()

        if st.button("❌ Weak Profile (<15%)", help="Loads an unrelated customer support resume", use_container_width=True):
            st.session_state.jd_text = SAMPLE_JD_PYTHON_DS
            st.session_state.resume_text = SAMPLE_RESUME_WEAK
            st.session_state.analysis_results = None
            st.session_state.linter_results = None
            st.rerun()

        if st.button("🧹 Clear Workspace", use_container_width=True):
            st.session_state.resume_text = ""
            st.session_state.jd_text = ""
            st.session_state.analysis_results = None
            st.session_state.linter_results = None
            st.rerun()

        st.markdown("<hr style='border: none; border-top: 1px solid rgba(212, 175, 55, 0.18); margin: 16px 0;'>", unsafe_allow_html=True)
        st.markdown("""
        <div style="padding: 10px 0;">
            <div style="font-family: 'Cinzel', serif; font-size: 0.82rem; font-weight: 700; color: #d4af37; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                ⚙️ Scoring Calibration
            </div>
            <div style="font-size: 0.8rem; color: #a89c8b; line-height: 1.6;">
                • <strong style="color:#fdfbf7;">60% Skill Coverage</strong>: Direct match across 250+ enterprise technology taxonomies.<br>
                • <strong style="color:#fdfbf7;">40% Semantic Overlap</strong>: Scaled cosine distance (TF-IDF / SBERT embeddings).<br>
            </div>
            <div style="margin-top: 12px; font-size: 0.78rem; color: #d8cebe; background: rgba(18, 15, 12, 0.85); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(212, 175, 55, 0.25);">
                <strong style="color:#fb7185;">&lt; 50%</strong> Weak Alignment<br>
                <strong style="color:#caa14c;">50% - 75%</strong> Moderate Alignment<br>
                <strong style="color:#34d399;">&gt; 75%</strong> Strong Alignment
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Dual Input Panels (Glassmorphic Dropzones)
    col_jd, col_res = st.columns(2)

    with col_jd:
        st.markdown("""
        <div class="panel-header-wrap">
            <span style="font-size: 1.1rem; font-weight: 700; color: #f1f5f9;">📋 Target Job Description (JD)</span>
            <span class="panel-tag">Role Specification</span>
        </div>
        """, unsafe_allow_html=True)
        jd_input = st.text_area(
            "Paste the complete Job Description text here:",
            value=st.session_state.jd_text,
            height=320,
            placeholder="Paste target role requirements (e.g. Senior Python Engineer experienced in FastAPI, Docker, PostgreSQL, AWS, Scikit-Learn)...",
            label_visibility="collapsed"
        )
        st.session_state.jd_text = jd_input

    with col_res:
        st.markdown("""
        <div class="panel-header-wrap">
            <span style="font-size: 1.1rem; font-weight: 700; color: #f1f5f9;">📄 Candidate Profile & Credentials</span>
            <span class="panel-tag">Applicant Data</span>
        </div>
        """, unsafe_allow_html=True)

        resume_mode = st.radio(
            "Choose Resume input method:",
            ["Direct Text Entry", "Upload Document (PDF / DOCX / TXT)"],
            horizontal=True,
            label_visibility="collapsed"
        )

        if resume_mode == "Direct Text Entry":
            resume_input = st.text_area(
                "Paste your Resume text here:",
                value=st.session_state.resume_text,
                height=265,
                placeholder="Paste candidate resume credentials, experience bullet points, technical skills, and educational background...",
                label_visibility="collapsed"
            )
            st.session_state.resume_text = resume_input
        else:
            uploaded_file = st.file_uploader(
                "Upload Candidate Document",
                type=["pdf", "docx", "txt"],
                label_visibility="collapsed"
            )
            if uploaded_file is not None:
                extracted_text = parse_uploaded_file(uploaded_file)
                if extracted_text:
                    st.session_state.resume_text = extracted_text
                    st.success(f"Successfully loaded '{uploaded_file.name}' ({len(extracted_text.split())} words extracted)")

            if st.session_state.resume_text:
                with st.expander("👁️ Inspect Extracted Resume Content"):
                    st.text(st.session_state.resume_text[:1400] + ("..." if len(st.session_state.resume_text) > 1400 else ""))

    # Primary Action Button
    st.markdown("<br>", unsafe_allow_html=True)
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2.5, 1])
    with btn_col2:
        trigger_analysis = st.button("⚡ RUN SPARKCV DEEP ATS MATCH & OPTIMIZATION", type="primary", use_container_width=True)

    if trigger_analysis:
        if not st.session_state.jd_text.strip():
            st.warning("⚠️ Please provide a Job Description before running the analysis.")
        elif not st.session_state.resume_text.strip():
            st.warning("⚠️ Please provide candidate Resume credentials or upload a document.")
        else:
            with st.spinner("Executing NLP semantic vectorization, skill taxonomy matching, and gap analysis..."):
                results = calculate_match_metrics(
                    st.session_state.resume_text,
                    st.session_state.jd_text,
                    engine=st.session_state.semantic_engine
                )
                linter = lint_resume_structure(st.session_state.resume_text)
                st.session_state.analysis_results = results
                st.session_state.linter_results = linter

    # Executive Results Dashboard
    if st.session_state.analysis_results:
        res = st.session_state.analysis_results
        final_score = res["final_score"]

        st.markdown("<br><hr style='border-color: rgba(56, 189, 248, 0.2); margin: 20px 0;'>", unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #f1f5f9; display: flex; align-items: center; gap: 10px;">
                <span>📊 Executive Talent Alignment Report</span>
            </div>
            <span class="panel-tag" style="background: rgba(56, 189, 248, 0.15); font-size: 0.75rem;">SparkCV Deep Analytics</span>
        </div>
        """, unsafe_allow_html=True)

        # Floating Metrics Quad Grid
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)

        with m_col1:
            st.markdown(f"""
            <div class="floating-metric-card" style="border-top: 3px solid {res['verdict_color']}; animation-delay: 0.05s;">
                <div class="metric-caption-title">Overall Match Index</div>
                <div class="metric-hero-val" style="color: {res['verdict_color']}; text-shadow: 0 0 25px {res['verdict_color']}50;">
                    {final_score}%
                </div>
                <div class="metric-sub-pill">Calibrated ATS Fit</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col2:
            st.markdown(f"""
            <div class="floating-metric-card" style="border-top: 3px solid #d4af37; animation-delay: 0.15s;">
                <div class="metric-caption-title">Skill Alignment</div>
                <div class="metric-hero-val" style="color: #34d399; text-shadow: 0 0 25px rgba(52, 211, 153, 0.4);">
                    {res['skill_coverage_pct']}%
                </div>
                <div class="metric-sub-pill">{res['matched_skills_count']} of {res['total_jd_skills_count']} Core Tools</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col3:
            st.markdown(f"""
            <div class="floating-metric-card" style="border-top: 3px solid #caa14c; animation-delay: 0.25s;">
                <div class="metric-caption-title">Semantic Context Overlap</div>
                <div class="metric-hero-val" style="color: #fef08a; text-shadow: 0 0 25px rgba(254, 240, 138, 0.4);">
                    {res['cosine_sim_pct']}%
                </div>
                <div class="metric-sub-pill">{res.get('engine_used', 'Semantic Similarity')}</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col4:
            st.markdown(f"""
            <div class="floating-metric-card" style="border-top: 3px solid #f43f5e; animation-delay: 0.35s;">
                <div class="metric-caption-title">Talent Keyword Deficit</div>
                <div class="metric-hero-val" style="color: #fb7185; text-shadow: 0 0 25px rgba(244, 63, 94, 0.4);">
                    {res['missing_skills_count']}
                </div>
                <div class="metric-sub-pill">Keywords to Bridge</div>
            </div>
            """, unsafe_allow_html=True)

        # Status Verdict Banner with Left Accent Border & Actionable Guidance Indicators
        st.markdown(f"""
        <div class="verdict-banner-card" style="border-left: 6px solid {res['verdict_color']}; animation-delay: 0.45s;">
            <span class="verdict-header-badge" style="background: {res['verdict_color']}25; color: {res['verdict_color']}; border: 1px solid {res['verdict_color']}50;">
                Executive Recruitment Appraisal
            </span>
            <h3 style="margin: 0 0 8px 0; color: #ffffff; font-family: 'Cinzel', serif; font-size: 1.35rem; font-weight: 700;">{res['verdict_label']}</h3>
            <p style="margin: 0 0 14px 0; font-size: 0.98rem; color: #d8cebe; line-height: 1.6;">{res['verdict_advice']}</p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; pt: 6px;">
                <span style="font-size: 0.82rem; background: rgba(212, 175, 55, 0.15); color: #fef08a; border: 1px solid rgba(212, 175, 55, 0.4); padding: 5px 12px; border-radius: 8px; font-weight: 600;">
                    💡 3 Targeted Projects Available in <strong>Tab 2 (Portfolio Roadmaps)</strong>
                </span>
                <span style="font-size: 0.82rem; background: rgba(202, 161, 76, 0.15); color: #caa14c; border: 1px solid rgba(202, 161, 76, 0.4); padding: 5px 12px; border-radius: 8px; font-weight: 600;">
                    ✍️ Live Bullet Re-writer in <strong>Tab 3 (Resume Polish)</strong>
                </span>
                <span style="font-size: 0.82rem; background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 5px 12px; border-radius: 8px; font-weight: 600;">
                    📋 ATS Structural Health Check in <strong>Tab 4 (Linter)</strong>
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Strategic Portfolio Projects
        project_ideas = generate_project_recommendations(res["missing_skills"], st.session_state.jd_text)

        # Feature 1: Executive Audit Report Download Bar
        linter_data = st.session_state.linter_results or lint_resume_structure(st.session_state.resume_text)
        report_content = generate_executive_audit_report(
            res,
            st.session_state.jd_text,
            st.session_state.resume_text,
            linter_data,
            project_ideas,
            candidate_name=st.session_state.get("user_name", ""),
            candidate_email=st.session_state.get("user_email", "")
        )

        rep_col1, rep_col2 = st.columns([2.6, 1.4])
        with rep_col1:
            st.markdown(f"""
            <div style="padding: 10px 0; font-size: 0.88rem; color: #c8bcab;">
                ⚡ <strong>Active Engine:</strong> <span style="color:#fef08a; font-weight:700;">{res.get('engine_used', 'TF-IDF')}</span> &nbsp;|&nbsp; 
                📋 <strong>Structural ATS Score:</strong> <span style="color:{linter_data['color']}; font-weight:700;">{linter_data['score']}/100</span> ({linter_data['verdict']})
            </div>
            """, unsafe_allow_html=True)
        with rep_col2:
            st.download_button(
                label="📥 Export Full Executive Audit Report (.md)",
                data=report_content,
                file_name=f"SparkCV_Talent_Alignment_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True,
                type="primary",
                help="Downloads full candidate appraisal, competency gap breakdown, ATS structural audit, and tailored project roadmap."
            )

        # Interactive Breakdown Tabs with Numbered Steps
        tab_skills, tab_projects, tab_guide, tab_linter = st.tabs([
            "🔍 1. Competency & Keyword Gap Matrix",
            "🚀 2. Strategic Portfolio Roadmaps (Tailored Projects)",
            "✍️ 3. Resume Polish Guide & Live Bullet Builder",
            "📋 4. Resume Structural Health & ATS Linter"
        ])

        # TAB 1: Skills & Keywords Breakdown
        with tab_skills:
            st.markdown("<br>", unsafe_allow_html=True)
            k_col1, k_col2 = st.columns(2)

            with k_col1:
                st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; padding: 18px; margin-bottom: 16px;">
                    <div style="font-size: 1rem; font-weight: 700; color: #34d399; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;">
                        <span>✅ Matched Competencies</span>
                        <span style="font-size: 0.8rem; background: rgba(16, 185, 129, 0.15); padding: 2px 8px; border-radius: 6px;">{len(res['matched_skills'])} Skills</span>
                    </div>
                """, unsafe_allow_html=True)

                if res["matched_skills"]:
                    badges_html = "".join([
                        f'<span class="badge-match">✓ {TECHNICAL_SKILLS_TAXONOMY.get(s, {}).get("display", s.upper())}</span>'
                        for s in res["matched_skills"]
                    ])
                    st.markdown(badges_html + "</div>", unsafe_allow_html=True)
                else:
                    st.markdown('<div style="color:#94a3b8; font-size:0.9rem;">No direct matching technical competencies detected. Review the deficit list to update your profile.</div></div>', unsafe_allow_html=True)

            with k_col2:
                st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(244, 63, 94, 0.25); border-radius: 12px; padding: 18px; margin-bottom: 16px;">
                    <div style="font-size: 1rem; font-weight: 700; color: #fb7185; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;">
                        <span>❌ Missing Target Qualifications</span>
                        <span style="font-size: 0.8rem; background: rgba(244, 63, 94, 0.15); padding: 2px 8px; border-radius: 6px;">{len(res['missing_skills'])} Gaps</span>
                    </div>
                """, unsafe_allow_html=True)

                if res["missing_skills"]:
                    badges_html = "".join([
                        f'<span class="badge-miss">✗ {TECHNICAL_SKILLS_TAXONOMY.get(s, {}).get("display", s.upper())}</span>'
                        for s in res["missing_skills"]
                    ])
                    st.markdown(badges_html + "</div>", unsafe_allow_html=True)
                else:
                    st.markdown('<div style="color:#34d399; font-size:0.9rem;">🎉 Remarkable match! 100% of target role competencies are represented.</div></div>', unsafe_allow_html=True)

            st.markdown("""
            <div style="background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%); border: 1px solid rgba(212, 175, 55, 0.35); border-radius: 12px; padding: 20px; margin-top: 10px;">
                <div style="font-family: 'Cinzel', serif; font-size: 1.05rem; font-weight: 700; color: #fef08a; margin-bottom: 4px;">
                    📈 High-Value ATS Salient Terminology Extraction
                </div>
                <div style="font-size: 0.85rem; color: #a89c8b; margin-bottom: 16px;">
                    Top statistically weighted n-grams extracted by Scikit-Learn TF-IDF vectorization from this specific job description:
                </div>
            """, unsafe_allow_html=True)

            kw_col1, kw_col2 = st.columns(2)
            with kw_col1:
                st.markdown("**Present in Candidate Resume:**")
                if res["matched_salient_kw"]:
                    st.write(", ".join([f"`{kw}`" for kw in res["matched_salient_kw"]]))
                else:
                    st.caption("None of the top weighted TF-IDF terms matched.")

            with kw_col2:
                st.markdown("**Missing from Resume (High-Value ATS Search Terms):**")
                if res["missing_salient_kw"]:
                    st.write(", ".join([f"`{kw}`" for kw in res["missing_salient_kw"]]))
                else:
                    st.caption("All top TF-IDF salient terms are present!")

            st.markdown("</div>", unsafe_allow_html=True)

        # TAB 2: Dynamic Project Suggestions
        with tab_projects:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="margin-bottom: 18px;">
                <div style="font-family: 'Cinzel', serif; font-size: 1.15rem; font-weight: 700; color: #fef08a;">💡 Tailored Portfolio Roadmaps to Bridge Technical Gaps</div>
                <div style="color: #c8bcab; font-size: 0.92rem; line-height: 1.5; margin-top: 4px;">
                    Based on the specific technical gaps identified between the role and candidate profile,
                    here are <strong>hyper-specific project architectures</strong> to demonstrate verified production mastery:
                </div>
            </div>
            """, unsafe_allow_html=True)

            for i, proj in enumerate(project_ideas, 1):
                tech_badges = " ".join([f'<span class="panel-chip" style="margin-right: 4px;">{t}</span>' for t in proj["tech_stack"]])
                st.markdown(f"""
                <div class="project-card-pro">
                    <div class="project-title-pro">{i}. {proj['title']}</div>
                    <div class="project-desc-pro">{proj['desc']}</div>
                    <div style="margin-bottom: 8px;">
                        <strong style="color: #a89c8b; font-size: 0.85rem; text-transform: uppercase;">Core Tech Stack:</strong>
                        <div style="margin-top: 6px;">{tech_badges}</div>
                    </div>
                    <div class="project-metric-pro">
                        <strong style="color: #d4af37;">🎯 Quantified Resume Metric Example:</strong><br>
                        <em style="color: #fdfbf7; font-family: 'Inter', sans-serif; font-size: 0.88rem; display: block; margin-top: 4px;">"{proj['key_metric']}"</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # TAB 3: Action Verbs & Google XYZ Formula Guide + Interactive Live Bullet Builder
        with tab_guide:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div class="xyz-formula-card">
                <span style="font-size: 1.4rem;">📐</span>
                <div>
                    <div style="font-family: 'Cinzel', serif; font-weight: 700;">Proven Google XYZ Impact Formula:</div>
                    <span style="color: #fef08a; font-family: 'Cinzel', serif; font-weight: 700;">"Accomplished [X] as measured by [Y], by doing [Z]"</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Feature 3: Interactive Live Bullet Point Re-writer
            st.markdown("""
            <div style="background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%); border: 1px solid rgba(212, 175, 55, 0.4); border-radius: 14px; padding: 22px; margin-bottom: 24px;">
                <div style="font-family: 'Cinzel', serif; font-size: 1.15rem; font-weight: 700; color: #fef08a; margin-bottom: 6px; display: flex; align-items: center; gap: 8px;">
                    <span>✍️ Interactive Live Bullet Point Re-writer</span>
                    <span class="panel-chip" style="font-size: 0.7rem;">ATS Optimization Engine</span>
                </div>
                <div style="font-size: 0.88rem; color: #a89c8b; margin-bottom: 16px;">
                    Transform weak or passive resume responsibilities into high-impact, quantified Google XYZ achievements infused with your target job description keywords.
                </div>
            """, unsafe_allow_html=True)

            b_col1, b_col2 = st.columns(2)
            with b_col1:
                all_verbs = [v for sublist in ACTION_VERBS.values() for v in sublist]
                selected_verb = st.selectbox(
                    "1. Select Strong Action Verb [Doing Z]:",
                    all_verbs,
                    index=0,
                    help="Choose an authoritative power verb that describes your engineering execution."
                )

                suggested_keywords = [TECHNICAL_SKILLS_TAXONOMY.get(s, {}).get("display", s) for s in res.get("missing_skills", [])]
                if not suggested_keywords:
                    suggested_keywords = ["FastAPI & PostgreSQL", "Docker & Kubernetes", "Scikit-Learn & ML", "AWS Cloud Services", "REST Microservices", "CI/CD Pipelines"]

                selected_keyword = st.selectbox(
                    "2. Target Technical Keyword to Integrate:",
                    suggested_keywords,
                    index=0,
                    help="Integrate one of your target missing competencies directly into this bullet point."
                )

            with b_col2:
                sample_metric = st.selectbox(
                    "3. Select / Enter Measurable Metric [Measured by Y]:",
                    [
                        "reducing response latency by 45%",
                        "improving model precision by 22%",
                        "supporting 1,500+ concurrent requests",
                        "eliminating manual errors for 50,000+ records",
                        "accelerating deployment cycles by 3.5x",
                        "securing 99.9% production system uptime",
                        "saving $35,000 in monthly cloud infrastructure costs"
                    ],
                    index=0
                )
                raw_duty = st.text_input(
                    "4. Base Duty or Task Accomplished [Accomplished X]:",
                    value="backend data ingestion pipelines and microservice endpoints",
                    placeholder="e.g. backend data pipeline or customer recommendation system"
                )

            st.markdown("<br>", unsafe_allow_html=True)
            bullet_variations = generate_google_xyz_bullets(
                raw_bullet=raw_duty,
                action_verb=selected_verb,
                target_keyword=selected_keyword,
                metric=sample_metric
            )

            st.markdown("""
            <div style="font-weight: 700; color: #f1f5f9; font-size: 0.95rem; margin-top: 14px; margin-bottom: 10px;">
                🎯 Synthesized High-Impact Bullet Variations (Ready to copy into your resume):
            </div>
            """, unsafe_allow_html=True)

            for b_idx, var in enumerate(bullet_variations, 1):
                st.markdown(f"""
                <div style="background: rgba(20, 16, 13, 0.95); border: 1px solid rgba(212, 175, 55, 0.35); border-left: 4px solid #d4af37; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px; box-shadow: 0 4px 14px rgba(0,0,0,0.5);">
                    <div style="font-family: 'Cinzel', serif; font-size: 0.78rem; font-weight: 700; color: #fef08a; text-transform: uppercase; margin-bottom: 4px;">
                        Variation {b_idx} • {var['title']}
                    </div>
                    <div style="font-size: 0.92rem; color: #fdfbf7; line-height: 1.5; font-family: 'Inter', sans-serif;">
                        • {var['bullet']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
            <div style="background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 12px; padding: 20px; margin-bottom: 22px;">
                <div style="font-family: 'Cinzel', serif; font-size: 1.05rem; font-weight: 700; color: #fef08a; margin-bottom: 14px;">
                    🔄 Executive Before & After Bullet Transformations
                </div>
            """, unsafe_allow_html=True)

            for ex in XYZ_EXAMPLES:
                st.markdown(f"""
                <div style="border-bottom: 1px solid rgba(212, 175, 55, 0.15); padding-bottom: 14px; margin-bottom: 14px;">
                    <div style="color: #fb7185; font-size: 0.92rem; margin-bottom: 4px;"><strong>❌ Before (Passive Duty):</strong> <em>"{ex['before']}"</em></div>
                    <div style="color: #34d399; font-size: 0.95rem; font-weight: 600; margin-bottom: 4px;"><strong>✅ After (Quantified Impact):</strong> <em>"{ex['after']}"</em></div>
                    <div style="color: #a89c8b; font-size: 0.84rem; font-style: italic;">💡 Formula Breakdown: {ex['breakdown']}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
            <div style="background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 12px; padding: 20px;">
                <div style="font-family: 'Cinzel', serif; font-size: 1.05rem; font-weight: 700; color: #fef08a; margin-bottom: 14px;">
                    ⚡ High-Impact Executive Action Verbs
                </div>
            """, unsafe_allow_html=True)

            v_col1, v_col2 = st.columns(2)
            categories = list(ACTION_VERBS.items())
            with v_col1:
                for cat, verbs in categories[:2]:
                    st.markdown(f"<div style='font-family:\"Cinzel\", serif; font-weight:700; color:#d4af37; font-size:0.88rem; margin: 8px 0 4px 0;'>{cat}</div>", unsafe_allow_html=True)
                    st.markdown(" ".join([f'<span class="action-badge">{v}</span>' for v in verbs]), unsafe_allow_html=True)

            with v_col2:
                for cat, verbs in categories[2:]:
                    st.markdown(f"<div style='font-family:\"Cinzel\", serif; font-weight:700; color:#d4af37; font-size:0.88rem; margin: 8px 0 4px 0;'>{cat}</div>", unsafe_allow_html=True)
                    st.markdown(" ".join([f'<span class="action-badge">{v}</span>' for v in verbs]), unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # Feature 4: TAB 4: Structural Health & ATS Linter
        with tab_linter:
            st.markdown("<br>", unsafe_allow_html=True)
            linter = st.session_state.linter_results or lint_resume_structure(st.session_state.resume_text)

            # Linter Header Metrics Grid
            l_col1, l_col2, l_col3, l_col4 = st.columns(4)

            with l_col1:
                st.markdown(f"""
                <div class="floating-metric-card" style="border-top: 3px solid {linter['color']};">
                    <div class="metric-caption-title">Structural ATS Score</div>
                    <div class="metric-hero-val" style="color: {linter['color']};">
                        {linter['score']} / 100
                    </div>
                    <div class="metric-sub-pill">{linter['verdict']}</div>
                </div>
                """, unsafe_allow_html=True)

            with l_col2:
                st.markdown(f"""
                <div class="floating-metric-card" style="border-top: 3px solid {linter['word_color']};">
                    <div class="metric-caption-title">Document Word Count</div>
                    <div class="metric-hero-val" style="color: {linter['word_color']};">
                        {linter['word_count']}
                    </div>
                    <div class="metric-sub-pill">{linter['word_status']}</div>
                </div>
                """, unsafe_allow_html=True)

            with l_col3:
                ci = linter['contact_info']
                ci_count = sum([1 for v in [ci['email'], ci['phone'], ci['links']] if v])
                ci_color = "#10b981" if ci_count == 3 else ("#caa14c" if ci_count >= 1 else "#ef4444")
                st.markdown(f"""
                <div class="floating-metric-card" style="border-top: 3px solid {ci_color};">
                    <div class="metric-caption-title">Contact Credentials</div>
                    <div class="metric-hero-val" style="color: {ci_color};">
                        {ci_count} / 3
                    </div>
                    <div class="metric-sub-pill">Email • Phone • Links</div>
                </div>
                """, unsafe_allow_html=True)

            with l_col4:
                sec = linter['sections']
                sec_count = sum([1 for v in [sec['experience'], sec['education'], sec['skills'], sec['projects']] if v])
                sec_color = "#10b981" if sec_count >= 3 else ("#caa14c" if sec_count >= 2 else "#ef4444")
                st.markdown(f"""
                <div class="floating-metric-card" style="border-top: 3px solid {sec_color};">
                    <div class="metric-caption-title">Core ATS Sections</div>
                    <div class="metric-hero-val" style="color: {sec_color};">
                        {sec_count} / 4
                    </div>
                    <div class="metric-sub-pill">Exp • Edu • Skills • Proj</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Two columns: Checklist & Action Items
            chk_col1, chk_col2 = st.columns(2)

            with chk_col1:
                st.markdown("""
                <div style="background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 12px; padding: 20px; height: 100%;">
                    <div style="font-family: 'Cinzel', serif; font-size: 1.05rem; font-weight: 700; color: #fef08a; margin-bottom: 12px;">
                        📋 ATS Format Compliance Checklist
                    </div>
                """, unsafe_allow_html=True)

                ci = linter['contact_info']
                email_icon = "✅" if ci['email'] else "❌"
                phone_icon = "✅" if ci['phone'] else "❌"
                links_icon = "✅" if ci['links'] else "❌"
                st.markdown("**Contact Information Detection:**")
                st.markdown(f"- {email_icon} Professional Email Address: {'Found' if ci['email'] else 'Not detected'}")
                st.markdown(f"- {phone_icon} Direct Phone Number: {'Found' if ci['phone'] else 'Not detected'}")
                st.markdown(f"- {links_icon} LinkedIn / GitHub / Portfolio Link: {'Found' if ci['links'] else 'Not detected'}")

                sec = linter['sections']
                exp_icon = "✅" if sec['experience'] else "❌"
                edu_icon = "✅" if sec['education'] else "❌"
                skl_icon = "✅" if sec['skills'] else "❌"
                prj_icon = "✅" if sec['projects'] else "❌"
                st.markdown("<br>**Essential ATS Sections Detected:**", unsafe_allow_html=True)
                st.markdown(f"- {exp_icon} Work Experience / Employment History: {'Verified' if sec['experience'] else 'Missing heading'}")
                st.markdown(f"- {edu_icon} Education / Academic Credentials: {'Verified' if sec['education'] else 'Missing heading'}")
                st.markdown(f"- {skl_icon} Dedicated Technical Skills Section: {'Verified' if sec['skills'] else 'Missing heading'}")
                st.markdown(f"- {prj_icon} Technical Projects / Portfolio Section: {'Verified' if sec['projects'] else 'Missing heading'}")

                st.markdown("<br>**Quantified Impact Rigor:**", unsafe_allow_html=True)
                st.markdown(f"- 📊 Detected Metrics: **{linter['quant_metric_count']}** quantified data points")
                st.markdown(f"- 💡 Status: *{linter['quant_status']}*")

                st.markdown("</div>", unsafe_allow_html=True)

            with chk_col2:
                st.markdown("""
                <div style="background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 12px; padding: 20px; height: 100%;">
                    <div style="font-family: 'Cinzel', serif; font-size: 1.05rem; font-weight: 700; color: #fb7185; margin-bottom: 12px;">
                        🚨 Corrective ATS Recommendations
                    </div>
                """, unsafe_allow_html=True)

                if linter['recommendations']:
                    for r_idx, rec in enumerate(linter['recommendations'], 1):
                        st.markdown(f"""
                        <div style="background: rgba(244, 63, 94, 0.08); border-left: 3px solid #fb7185; border-radius: 6px; padding: 10px 14px; margin-bottom: 10px; font-size: 0.88rem; color: #fdfbf7;">
                            <strong>#{r_idx}:</strong> {rec}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: rgba(16, 185, 129, 0.12); border-left: 3px solid #10b981; border-radius: 6px; padding: 14px; color: #34d399; font-size: 0.92rem;">
                        🎉 Outstanding! Your resume document passed all ATS structural, layout, and contact checks with no formatting red flags detected.
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

    # Executive Footer
    st.markdown("<br><hr style='border: none; border-top: 1px solid rgba(212, 175, 55, 0.18); margin: 30px 0 15px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #a89c8b; font-size: 0.84rem; padding-bottom: 25px;">
        SparkCV Enterprise Talent Intelligence Engine • Built with Python, Streamlit, Scikit-Learn & NLTK • Ready for Presentation
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
