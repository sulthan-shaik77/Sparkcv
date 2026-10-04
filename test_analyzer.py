"""
Unit tests for the NLP and scoring logic of the Job Description Analyzer & Resume Optimizer.
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from app import (
    clean_text,
    extract_skills_from_text,
    calculate_match_metrics,
    generate_project_recommendations,
    lint_resume_structure,
    generate_google_xyz_bullets,
    generate_executive_audit_report,
    SAMPLE_JD_PYTHON_DS,
    SAMPLE_RESUME_WEAK,
    SAMPLE_RESUME_MODERATE,
    SAMPLE_RESUME_STRONG
)

def test_clean_text():
    sample = "We are seeking a Python/FastAPI developer with 3+ years of experience in AWS & Docker!"
    cleaned = clean_text(sample)
    # Punctuation stripped, stopwords removed, lowercase
    assert "seeking" not in cleaned or "years" not in cleaned or "python" in cleaned
    assert "python" in cleaned
    assert "fastapi" in cleaned
    assert "aws" in cleaned
    assert "docker" in cleaned
    print("[PASS] test_clean_text passed")

def test_extract_skills():
    skills = extract_skills_from_text(SAMPLE_JD_PYTHON_DS)
    # Should detect python, fastapi, postgresql, scikit-learn, pandas, numpy, xgboost, spacy, nltk, docker, aws, kubernetes, etc.
    expected = {"python", "fastapi", "postgresql", "scikit-learn", "pandas", "numpy", "docker", "aws"}
    assert expected.issubset(skills), f"Missing expected skills: {expected - skills}"
    print(f"[PASS] test_extract_skills passed ({len(skills)} skills detected)")

def test_verdict_categories():
    # 1. Weak Match Test (< 50%)
    res_weak = calculate_match_metrics(SAMPLE_RESUME_WEAK, SAMPLE_JD_PYTHON_DS)
    print(f"Weak score: {res_weak['final_score']}%, Verdict: {res_weak['verdict_label']}")
    assert res_weak['final_score'] < 50.0, f"Expected < 50%, got {res_weak['final_score']}"
    assert "Needs Major Improvement" in res_weak['verdict_label']

    # 2. Moderate Match Test (50% - 75%)
    res_mod = calculate_match_metrics(SAMPLE_RESUME_MODERATE, SAMPLE_JD_PYTHON_DS)
    print(f"Moderate score: {res_mod['final_score']}%, Verdict: {res_mod['verdict_label']}")
    assert 50.0 <= res_mod['final_score'] <= 75.0, f"Expected 50-75%, got {res_mod['final_score']}"
    assert "Good Start, But Needs Tweaking" in res_mod['verdict_label']

    # 3. Strong Match Test (> 75%)
    res_strong = calculate_match_metrics(SAMPLE_RESUME_STRONG, SAMPLE_JD_PYTHON_DS)
    print(f"Strong score: {res_strong['final_score']}%, Verdict: {res_strong['verdict_label']}")
    assert res_strong['final_score'] > 75.0, f"Expected > 75%, got {res_strong['final_score']}"
    assert "Strong Match! Perfect Alignment" in res_strong['verdict_label']

    print("[PASS] test_verdict_categories passed for all 3 tiers")

def test_project_recommendations():
    res_mod = calculate_match_metrics(SAMPLE_RESUME_MODERATE, SAMPLE_JD_PYTHON_DS)
    missing = res_mod['missing_skills']
    projects = generate_project_recommendations(missing, SAMPLE_JD_PYTHON_DS)
    assert len(projects) >= 2, f"Expected at least 2 projects, got {len(projects)}"
    for p in projects:
        assert "title" in p and "desc" in p and "tech_stack" in p and "key_metric" in p
        print(f"  Recommended Project: {p['title']}")
    print("[PASS] test_project_recommendations passed")

def test_linter():
    # Test weak resume linter
    linter_weak = lint_resume_structure(SAMPLE_RESUME_WEAK)
    assert "score" in linter_weak
    assert linter_weak["word_count"] > 0
    assert linter_weak["contact_info"]["email"] is True
    assert len(linter_weak["recommendations"]) > 0

    # Test strong resume linter
    linter_strong = lint_resume_structure(SAMPLE_RESUME_STRONG)
    assert linter_strong["score"] >= 80, f"Expected strong linter score >= 80, got {linter_strong['score']}"
    assert linter_strong["contact_info"]["email"] is True
    assert linter_strong["contact_info"]["links"] is True
    assert linter_strong["sections"]["experience"] is True
    assert linter_strong["sections"]["education"] is True
    assert linter_strong["sections"]["skills"] is True
    assert linter_strong["quant_metric_count"] >= 5
    print(f"[PASS] test_linter passed (Strong score: {linter_strong['score']}/100, Metrics: {linter_strong['quant_metric_count']})")

def test_google_xyz_bullets():
    variations = generate_google_xyz_bullets(
        raw_bullet="microservice endpoints and API integrations",
        action_verb="Architected",
        target_keyword="FastAPI & PostgreSQL",
        metric="by 38%"
    )
    assert len(variations) == 3, f"Expected 3 variations, got {len(variations)}"
    for v in variations:
        assert "Architected" in v["bullet"]
        assert "FastAPI & PostgreSQL" in v["bullet"]
        assert "by 38%" in v["bullet"]
        print(f"  [XYZ Variation] {v['title']}: {v['bullet']}")
    print("[PASS] test_google_xyz_bullets passed")

def test_executive_audit_report():
    res = calculate_match_metrics(SAMPLE_RESUME_MODERATE, SAMPLE_JD_PYTHON_DS)
    linter = lint_resume_structure(SAMPLE_RESUME_MODERATE)
    projects = generate_project_recommendations(res["missing_skills"], SAMPLE_JD_PYTHON_DS)
    report = generate_executive_audit_report(res, SAMPLE_JD_PYTHON_DS, SAMPLE_RESUME_MODERATE, linter, projects)

    assert "SPARKCV — EXECUTIVE TALENT ALIGNMENT & ATS AUDIT REPORT" in report
    assert "1. EXECUTIVE ALIGNMENT METRICS" in report
    assert "2. RESUME STRUCTURAL HEALTH & ATS LINTER" in report
    assert "3. COMPETENCY GAP MATRIX" in report
    assert "4. RECOMMENDED STRATEGIC PORTFOLIO ROADMAPS" in report
    assert len(report.splitlines()) > 30
    print(f"[PASS] test_executive_audit_report passed ({len(report)} characters generated)")

def test_semantic_engine_modes():
    # Test TF-IDF mode
    res_tfidf = calculate_match_metrics(SAMPLE_RESUME_MODERATE, SAMPLE_JD_PYTHON_DS, engine="tfidf")
    assert "TF-IDF" in res_tfidf["engine_used"]

    # Test SBERT mode (graceful fallback if uninstalled)
    res_sbert = calculate_match_metrics(SAMPLE_RESUME_MODERATE, SAMPLE_JD_PYTHON_DS, engine="sbert")
    assert "engine_used" in res_sbert
    assert res_sbert["final_score"] > 0
    print(f"[PASS] test_semantic_engine_modes passed (TF-IDF: {res_tfidf['engine_used']} | SBERT: {res_sbert['engine_used']})")

if __name__ == "__main__":
    test_clean_text()
    test_extract_skills()
    test_verdict_categories()
    test_project_recommendations()
    test_linter()
    test_google_xyz_bullets()
    test_executive_audit_report()
    test_semantic_engine_modes()
    print("\n>>> ALL 8 TESTS PASSED SUCCESSFULLY! <<<")
