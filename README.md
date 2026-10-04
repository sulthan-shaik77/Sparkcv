# 🎯 Smart Job Description Analyzer & Resume Optimization System

A complete, production-ready AI/NLP application built with **Python**, **Streamlit**, and **Scikit-Learn** that evaluates how well a resume aligns with a given Job Description, surfaces missing critical keywords, calculates a balanced match score, and generates hyper-specific portfolio projects to bridge candidate skill gaps.

---

## 🚀 Features

1. **Dual Ingestion Options**:
   - Paste raw text for Resume and Job Description.
   - Upload Resume files directly (`.pdf`, `.docx`, `.txt`).
   - One-click **Demo Presets** in the sidebar (Weak, Moderate, and Strong match scenarios) for instantaneous testing.

2. **Core NLP Analysis**:
   - **Text Cleaning**: Normalization, punctuation stripping, and stopwords removal with graceful offline fallback.
   - **Technical Skill Ontology**: Identifies 250+ technical tools, frameworks, programming languages, databases, and DevOps tools.
   - **TF-IDF Keyword Extraction**: Extracts salient unigrams and bigrams from the Job Description using Scikit-Learn's `TfidfVectorizer`.
   - **Gap Analysis**: Segregates skills into **Matched Skills** (green badges) and **Missing Skills** (red badges).

3. **Balanced Match Score & Verdict Status**:
   - **Scoring Formula**:
     $$\text{Match Score} = 0.50 \times \text{Skill Coverage Ratio} + 0.50 \times \text{TF-IDF Cosine Similarity}$$
   - **Status Badges**:
     - `< 50%`: ❌ **Needs Major Improvement (Weak alignment)**
     - `50% - 75%`: ⚠️ **Good Start, But Needs Tweaking (Moderate alignment)**
     - `> 75%`: ✅ **Strong Match! Perfect Alignment (Ready to apply)**

4. **Dynamic AI Project & Learning Suggestions**:
   - Inspects the missing tools and categories.
   - Generates **2–3 hyper-specific project ideas** with tech stacks, project descriptions, and concrete quantifiable metrics.
   - Tailored examples (e.g. FastAPI REST APIs, BeautifulSoup web scrapers, Scikit-Learn predictive modeling, Docker CI/CD pipelines).

5. **Resume Polish & Action Verbs Guide**:
   - Explains the **Google XYZ Formula** (`Accomplished [X] as measured by [Y], by doing [Z]`).
   - Categorized strong action verbs (*Architected*, *Optimized*, *Automated*, *Spearheaded*).
   - Before & After bullet transformation examples.

---

## 🛠️ Quick Start

### 1. Launch with One Click (Windows)
Double-click `run_app.bat` inside this folder.

### 2. Manual CLI Launch
```bash
# Navigate to this directory
cd C:\Users\sulth\Documents\sulthan\sulthan\Sparkcv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run the Streamlit application
streamlit run app.py
```

### 3. Running Automated Tests
```bash
.venv\Scripts\python test_analyzer.py
```
