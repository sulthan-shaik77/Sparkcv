"""
Script to generate the complete SIH-style 7-Slide Presentation for SparkCV:
AI-Powered Job Description Analyzer & Resume Optimization Engine.
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

# Initialize presentation with 16:9 widescreen layout
prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette Constants
COLOR_BG = RGBColor(15, 23, 42)          # Deep Navy #0F172A
COLOR_CARD = RGBColor(30, 41, 59)        # Slate Card #1E293B
COLOR_CARD_BORDER = RGBColor(51, 65, 85) # Slate Border #334155
COLOR_GOLD = RGBColor(212, 175, 55)      # Metallic Gold #D4AF37
COLOR_GOLD_LIGHT = RGBColor(254, 240, 138)
COLOR_CYAN = RGBColor(56, 189, 248)      # Sky Blue #38BDF8
COLOR_EMERALD = RGBColor(16, 185, 129)   # Green #10B981
COLOR_ROSE = RGBColor(244, 63, 94)       # Coral Red #F43F5E
COLOR_WHITE = RGBColor(248, 250, 252)    # Pure White #F8FAFC
COLOR_MUTED = RGBColor(148, 163, 184)    # Cool Gray #94A3B8
COLOR_DARK_TEXT = RGBColor(15, 23, 42)   # Dark Navy for light badges

def set_slide_background(slide):
    """Sets a rich dark navy gradient background on the slide."""
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = COLOR_BG
    bg_shape.line.color.rgb = COLOR_BG
    return bg_shape

def add_header(slide, slide_number, title_text, category_tag="SMART INDIA HACKATHON 2026"):
    """Adds a standardized SIH-style header with slide category tag and slide number."""
    # Top Tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.4))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = category_tag.upper()
    p_tag.font.name = "Arial"
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_GOLD

    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(10), Inches(0.65))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Arial"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE

    # Slide Number Badge (Top Right)
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(12.0), Inches(0.45), Inches(0.6), Inches(0.5))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_CARD
    badge.line.color.rgb = COLOR_GOLD
    tf_badge = badge.text_frame
    p_badge = tf_badge.paragraphs[0]
    p_badge.text = str(slide_number)
    p_badge.font.name = "Arial"
    p_badge.font.size = Pt(16)
    p_badge.font.bold = True
    p_badge.font.color.rgb = COLOR_GOLD
    p_badge.alignment = PP_ALIGN.CENTER

    # Footer Template Note
    foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.4))
    tf_foot = foot_box.text_frame
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = "@SIH Idea Submission - Template  |  Project: SparkCV  |  Team: SparkCV (Sulthan Shaik)"
    p_foot.font.name = "Arial"
    p_foot.font.size = Pt(10)
    p_foot.font.color.rgb = COLOR_MUTED


# ==========================================
# SLIDE 1: TITLE PAGE
# ==========================================
slide1 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide1)

# Hackathon Header
h_box = slide1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(0.6))
p_h = h_box.text_frame.paragraphs[0]
p_h.text = "SMART INDIA HACKATHON 2026  •  INNOVATION & AI CATEGORY"
p_h.font.name = "Arial"
p_h.font.size = Pt(14)
p_h.font.bold = True
p_h.font.color.rgb = COLOR_GOLD
p_h.alignment = PP_ALIGN.CENTER

# Big Project Title
t_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.3), Inches(1.4))
tf_t = t_box.text_frame
p_t = tf_t.paragraphs[0]
p_t.text = "SparkCV: AI-Powered Job Description Analyzer\n& Resume Optimization Engine"
p_t.font.name = "Arial"
p_t.font.size = Pt(30)
p_t.font.bold = True
p_t.font.color.rgb = COLOR_WHITE
p_t.alignment = PP_ALIGN.CENTER

# Subtitle
sub_box = slide1.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(11.3), Inches(0.6))
p_sub = sub_box.text_frame.paragraphs[0]
p_sub.text = "Autonomous ATS Alignment, 250+ Skill Gap Analysis, and Google XYZ Bullet Synthesis"
p_sub.font.name = "Arial"
p_sub.font.size = Pt(16)
p_sub.font.italic = True
p_sub.font.color.rgb = COLOR_CYAN
p_sub.alignment = PP_ALIGN.CENTER

# Metadata Card (Centered Grid)
card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(3.5), Inches(10.3), Inches(2.9))
card1.fill.solid()
card1.fill.fore_color.rgb = COLOR_CARD
card1.line.color.rgb = COLOR_GOLD
card1.line.width = Pt(1.5)

tf_c1 = card1.text_frame
tf_c1.word_wrap = True
tf_c1.margin_left = Inches(0.5)
tf_c1.margin_top = Inches(0.3)

meta_items = [
    ("Problem Statement ID:", "SIH26_HR01 / PS-AI-2026 (Smart Automated Hiring & ATS Optimization)"),
    ("Problem Statement Title:", "AI-Driven NLP Alignment & Gap Detection for Candidate Resumes vs Industry JDs"),
    ("Theme:", "Artificial Intelligence / EdTech / HR-Tech / Smart Career Automation"),
    ("PS Category:", "Software & Natural Language Processing (NLP)"),
    ("Team / Submitter:", "SparkCV  •  Lead: Sulthan Shaik (GitHub: sulthan-shaik77)"),
    ("Live Cloud Demo:", "https://sparkcv.streamlit.app  |  Repository: github.com/sulthan-shaik77/Sparkcv")
]

for label, val in meta_items:
    p = tf_c1.add_paragraph() if tf_c1.paragraphs[0].text else tf_c1.paragraphs[0]
    p.text = f"{label:<25} {val}"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(6)


# ==========================================
# SLIDE 2: IDEA TITLE & PROPOSED SOLUTION
# ==========================================
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide2)
add_header(slide2, 2, "PROPOSED SOLUTION (IDEA / PROTOTYPE OVERVIEW)")

# Left Card: The Core Problem
card2_left = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.1))
card2_left.fill.solid()
card2_left.fill.fore_color.rgb = COLOR_CARD
card2_left.line.color.rgb = COLOR_CARD_BORDER

tf_l = card2_left.text_frame
tf_l.word_wrap = True
tf_l.margin_left = Inches(0.3)
tf_l.margin_right = Inches(0.3)
tf_l.margin_top = Inches(0.3)

p_l_head = tf_l.paragraphs[0]
p_l_head.text = "⚠️ THE INDUSTRY CHALLENGE"
p_l_head.font.name = "Arial"
p_l_head.font.size = Pt(16)
p_l_head.font.bold = True
p_l_head.font.color.rgb = COLOR_ROSE
p_l_head.space_after = Pt(12)

problems = [
    "75%+ Automated Rejection: Resumes are filtered out by ATS algorithms before human recruiters ever review them.",
    "Blind Keyword Stuffing: Applicants do not know exact technical ontology gaps and resort to ineffective keyword cramming.",
    "No Actionable Bridge: Conventional scanners show a low score but never provide concrete projects or bullet rewrites to fix gaps.",
    "Expensive & Slow LLMs: Commercial tools rely on costly, slow, privacy-risky external APIs (OpenAI/Anthropic)."
]

for pr in problems:
    p = tf_l.add_paragraph()
    p.text = "• " + pr
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_MUTED
    p.space_after = Pt(10)

# Right Card: The SparkCV Solution
card2_right = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.1))
card2_right.fill.solid()
card2_right.fill.fore_color.rgb = COLOR_CARD
card2_right.line.color.rgb = COLOR_GOLD

tf_r = card2_right.text_frame
tf_r.word_wrap = True
tf_r.margin_left = Inches(0.3)
tf_r.margin_right = Inches(0.3)
tf_r.margin_top = Inches(0.3)

p_r_head = tf_r.paragraphs[0]
p_r_head.text = "✨ SPARKCV PROPOSED SOLUTION"
p_r_head.font.name = "Arial"
p_r_head.font.size = Pt(16)
p_r_head.font.bold = True
p_r_head.font.color.rgb = COLOR_GOLD
p_r_head.space_after = Pt(12)

solutions = [
    "Multi-Format Ingestion: Parses PDF, DOCX, and TXT resumes with zero-dependency native XML/ZIP fallback.",
    "250+ Hard-Skill Ontology: Deep technical taxonomy with regex word-boundary protection (e.g. C++, Go, .NET).",
    "Balanced Hybrid Scoring: Combines 50% Skill Coverage Ratio with 50% TF-IDF Cosine Similarity for fair evaluation.",
    "Dynamic Portfolio Recommendations: Generates 2-3 production-grade project specs (tech stack + metrics) to fill missing skills.",
    "Google XYZ Bullet Synthesizer: Automatically converts weak bullets into high-impact quantified achievements.",
    "ATS Structural Linter: Audits metrics density, action verb power, and format traps with instant executive report export."
]

for sol in solutions:
    p = tf_r.add_paragraph()
    p.text = "✔ " + sol
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(8)


# ==========================================
# SLIDE 3: TECHNICAL APPROACH & PIPELINE
# ==========================================
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide3)
add_header(slide3, 3, "TECHNICAL APPROACH (PIPELINE & WORKFLOW)")

# 4 Horizontal Pipeline Stages
stages = [
    ("1. INGESTION", "PDF / DOCX / TXT\nPyPDF + Docx Parsers\nNative In-Memory ZIP/XML\nOne-Click Demo Presets", COLOR_CYAN),
    ("2. PREPROCESSING", "Text Normalization\nPunctuation & Stopwords\n250+ Ontology Matching\nBoundary Regex (\bGo\b)", COLOR_GOLD),
    ("3. SCORING ENGINE", "Scikit-Learn TF-IDF\nCosine Similarity (n-gram)\n50% Coverage + 50% Vector\n3-Tier Verdict System", COLOR_EMERALD),
    ("4. OPTIMIZATION", "Dynamic Portfolio Projects\nGoogle XYZ Bullet Rewriter\nATS Structural Linter\nExecutive Markdown Audit", COLOR_ROSE)
]

col_width = Inches(2.7)
col_gap = Inches(0.25)
start_x = Inches(0.8)

for idx, (st_title, st_desc, st_color) in enumerate(stages):
    x = start_x + idx * (col_width + col_gap)
    # Stage box
    box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), col_width, Inches(3.0))
    box.fill.solid()
    box.fill.fore_color.rgb = COLOR_CARD
    box.line.color.rgb = st_color
    box.line.width = Pt(1.5)
    
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_top = Inches(0.2)
    tf.margin_left = Inches(0.15)
    tf.margin_right = Inches(0.15)
    
    p0 = tf.paragraphs[0]
    p0.text = st_title
    p0.font.name = "Arial"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = st_color
    p0.space_after = Pt(10)
    
    p1 = tf.add_paragraph()
    p1.text = st_desc
    p1.font.name = "Arial"
    p1.font.size = Pt(11)
    p1.font.color.rgb = COLOR_WHITE
    p1.space_after = Pt(4)

    # Arrow connector between stages
    if idx < 3:
        arrow_box = slide3.shapes.add_textbox(x + col_width - Inches(0.05), Inches(2.7), Inches(0.35), Inches(0.5))
        p_arr = arrow_box.text_frame.paragraphs[0]
        p_arr.text = "➔"
        p_arr.font.size = Pt(18)
        p_arr.font.bold = True
        p_arr.font.color.rgb = COLOR_MUTED

# Bottom Detail Card: Technical Highlights
bot_card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.7), Inches(1.9))
bot_card.fill.solid()
bot_card.fill.fore_color.rgb = COLOR_CARD
bot_card.line.color.rgb = COLOR_CARD_BORDER

tf_b = bot_card.text_frame
tf_b.word_wrap = True
tf_b.margin_left = Inches(0.3)
tf_b.margin_top = Inches(0.2)

p_b_head = tf_b.paragraphs[0]
p_b_head.text = "🔬 MATHEMATICAL FORMULA & CONTEXTUAL METHODOLOGY"
p_b_head.font.name = "Arial"
p_b_head.font.size = Pt(14)
p_b_head.font.bold = True
p_b_head.font.color.rgb = COLOR_GOLD
p_b_head.space_after = Pt(6)

points = [
    "Final Match Score = [0.50 × Skill Coverage Ratio] + [0.50 × TF-IDF Cosine Similarity]",
    "Why Dual Metric? Prevents pure keyword-stuffing while rewarding deep semantic alignment across experience bullet points.",
    "Verdict Tiers: <50% (Weak / Major Rework), 50-75% (Moderate Alignment), >75% (Strong Match / Application Ready).",
    "100% Deterministic & Private: Runs locally in <200ms without sending candidate PII to third-party cloud APIs."
]
for pt in points:
    p = tf_b.add_paragraph()
    p.text = "• " + pt
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(3)


# ==========================================
# SLIDE 4: TECHNICAL ARCHITECTURE & FEASIBILITY
# ==========================================
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide4)
add_header(slide4, 4, "TECHNICAL ARCHITECTURE & SYSTEM DESIGN")

# Top Stack Architecture Cards (3 Horizontal Blocks)
arch_blocks = [
    ("INPUT / INGESTION LAYER", "• PDF Extraction (pypdf)\n• Word Docx (python-docx)\n• Native in-memory ZIP/XML\n• Job Description Text Stream\n• Instant Weak/Mod/Strong Presets", Inches(0.8), COLOR_CYAN),
    ("CORE NLP & ANALYTICAL ENGINE", "• Scikit-Learn TfidfVectorizer\n• Cosine Similarity Matrix\n• 250+ Skill Taxonomy Matcher\n• Sentence-Transformers SBERT Fallback\n• Regex Boundary Tokenizer", Inches(4.8), COLOR_GOLD),
    ("ACTIONABLE OUTPUT ENGINES", "• Dynamic Portfolio Generator\n• Google XYZ Bullet Synthesizer\n• ATS Structural Checklist Linter\n• Executive Markdown Audit Export\n• Responsive Streamlit + Web UI", Inches(8.8), COLOR_EMERALD)
]

for title, content, x_pos, col in arch_blocks:
    box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(1.5), Inches(3.7), Inches(2.7))
    box.fill.solid()
    box.fill.fore_color.rgb = COLOR_CARD
    box.line.color.rgb = col
    box.line.width = Pt(1.5)
    
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_top = Inches(0.2)
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = col
    p.space_after = Pt(8)
    
    for line in content.split("\n"):
        p_c = tf.add_paragraph()
        p_c.text = line
        p_c.font.name = "Arial"
        p_c.font.size = Pt(11)
        p_c.font.color.rgb = COLOR_WHITE
        p_c.space_after = Pt(3)

# Bottom Specifications Table
bot_specs = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.4), Inches(11.7), Inches(2.2))
bot_specs.fill.solid()
bot_specs.fill.fore_color.rgb = COLOR_CARD
bot_specs.line.color.rgb = COLOR_CARD_BORDER

tf_bs = bot_specs.text_frame
tf_bs.word_wrap = True
tf_bs.margin_left = Inches(0.3)
tf_bs.margin_top = Inches(0.2)

p_bs = tf_bs.paragraphs[0]
p_bs.text = "⚙️ IMPLEMENTATION SPECIFICATIONS & DUAL DELIVERY"
p_bs.font.name = "Arial"
p_bs.font.size = Pt(14)
p_bs.font.bold = True
p_bs.font.color.rgb = COLOR_GOLD
p_bs.space_after = Pt(6)

spec_details = [
    "Primary Stack: Python 3.10+, Streamlit, Scikit-Learn, PyPDF, Python-docx, NumPy.",
    "Dual Delivery Model: 1) Cloud-Hosted Streamlit app (sparkcv.streamlit.app), 2) Zero-dependency pure Python standalone server (standalone_app.py) requiring no pip installations.",
    "Computational Efficiency: Sub-200ms execution on standard CPUs without GPU dependencies or recurring API subscriptions.",
    "Test Coverage: 100% automated test pass rate across 8 core unit tests (cleaning, taxonomy, scoring, linter, XYZ bullets, audit export)."
]

for s in spec_details:
    p = tf_bs.add_paragraph()
    p.text = "• " + s
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(3)


# ==========================================
# SLIDE 5: FEASIBILITY, VIABILITY & RISK MITIGATION
# ==========================================
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide5)
add_header(slide5, 5, "FEASIBILITY, VIABILITY & RISK MITIGATION")

# 4 Risk vs Mitigation Rows
risks_mitigations = [
    ("Non-Standard File Formats", "Complex PDF layouts, legacy Word tables, non-UTF-8 character encodings.", "Multi-parser fallback (PyPDF -> native in-memory XML/ZIP -> multi-encoding text decoding utf-8/cp1252)."),
    ("Keyword Stuffing Vulnerability", "Candidates pasting random skill keywords to artificially game naive ATS scanners.", "Hybrid Scoring: 50% vector cosine similarity ensures contextual relevance across full bullet statements."),
    ("Short Skill False Positives", "Terms like 'Go', 'R', or 'C' matching everyday English words ('go', 'c').", "Strict regex word boundaries (\bGo\b, \bC\+\+\b, \b\.NET\b) with technical contextual verification."),
    ("Cloud API Costs & PII Privacy", "Sending candidate resumes to 3rd-party LLM APIs risks data leaks and high per-scan bills.", "100% local mathematical NLP execution. Zero external API calls, zero cost per scan, 100% PII privacy.")
]

y_pos = Inches(1.5)
row_h = Inches(1.1)
gap_y = Inches(0.18)

for r_title, r_desc, m_desc in risks_mitigations:
    # Risk Card
    r_card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y_pos, Inches(5.6), row_h)
    r_card.fill.solid()
    r_card.fill.fore_color.rgb = COLOR_CARD
    r_card.line.color.rgb = COLOR_ROSE
    
    tf_r = r_card.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = Inches(0.2)
    tf_r.margin_top = Inches(0.1)
    
    p_rt = tf_r.paragraphs[0]
    p_rt.text = "⚡ RISK: " + r_title
    p_rt.font.name = "Arial"
    p_rt.font.size = Pt(11)
    p_rt.font.bold = True
    p_rt.font.color.rgb = COLOR_ROSE
    
    p_rd = tf_r.add_paragraph()
    p_rd.text = r_desc
    p_rd.font.name = "Arial"
    p_rd.font.size = Pt(10)
    p_rd.font.color.rgb = COLOR_MUTED

    # Mitigation Card
    m_card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), y_pos, Inches(5.7), row_h)
    m_card.fill.solid()
    m_card.fill.fore_color.rgb = COLOR_CARD
    m_card.line.color.rgb = COLOR_EMERALD
    
    tf_m = m_card.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = Inches(0.2)
    tf_m.margin_top = Inches(0.1)
    
    p_mt = tf_m.paragraphs[0]
    p_mt.text = "🛡️ MITIGATION: " + r_title
    p_mt.font.name = "Arial"
    p_mt.font.size = Pt(11)
    p_mt.font.bold = True
    p_mt.font.color.rgb = COLOR_EMERALD
    
    p_md = tf_m.add_paragraph()
    p_md.text = m_desc
    p_md.font.name = "Arial"
    p_md.font.size = Pt(10)
    p_md.font.color.rgb = COLOR_WHITE

    y_pos += row_h + gap_y

# Bottom Viability Summary
sum_box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.9), Inches(11.7), Inches(0.85))
sum_box.fill.solid()
sum_box.fill.fore_color.rgb = COLOR_CARD
sum_box.line.color.rgb = COLOR_GOLD

tf_sb = sum_box.text_frame
p_sb = tf_sb.paragraphs[0]
p_sb.text = "💡 COMMERCIAL & SCALABLE VIABILITY"
p_sb.font.name = "Arial"
p_sb.font.size = Pt(12)
p_sb.font.bold = True
p_sb.font.color.rgb = COLOR_GOLD

p_sb2 = tf_sb.add_paragraph()
p_sb2.text = "Highly scalable across Universities, Bootcamps, and Enterprise ATS portals with zero infrastructure overhead and zero recurring model fees."
p_sb2.font.name = "Arial"
p_sb2.font.size = Pt(11)
p_sb2.font.color.rgb = COLOR_WHITE


# ==========================================
# SLIDE 6: IMPACT AND BENEFITS
# ==========================================
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide6)
add_header(slide6, 6, "IMPACT AND VALUE PROPOSITION")

# 8 Value Drivers arranged in a 4x2 grid
benefits = [
    ("🚀 Higher ATS Pass Rate", "Pierces automated filters by aligning hard skills and semantic context directly with job requisitions.", COLOR_CYAN),
    ("💰 Zero API Overhead", "100% free open-source NLP stack. Zero recurring OpenAI/Anthropic API bills, eliminating financial scaling bottlenecks.", COLOR_GOLD),
    ("⚡ Blazing Fast (<200ms)", "Immediate analysis feedback loop compared to 15-30 second latency on heavy generative LLMs.", COLOR_EMERALD),
    ("🛠️ Dynamic Skill Bridging", "Recommends actionable, concrete portfolio projects with quantifiable metrics to bridge candidate skill gaps.", COLOR_CYAN),
    ("🎯 Google XYZ Bullet Polish", "Parameterizes experience bullets using Google's proven 'Accomplished [X] measured by [Y] by doing [Z]' formula.", COLOR_GOLD),
    ("🔒 Complete PII Privacy", "Candidate resume data is processed locally in-memory and is never stored, sold, or shared with third parties.", COLOR_EMERALD),
    ("📋 ATS Structural Linter", "Audits metric density, active verb ratio, and document formatting traps to ensure clean robotic readability.", COLOR_CYAN),
    ("📱 Multi-Device Accessible", "Seamlessly accessible across desktop, laptop, iPad, and smartphones via responsive cloud deployment.", COLOR_GOLD)
]

bw = Inches(2.7)
bh = Inches(2.3)
bx_start = Inches(0.8)
by_start = Inches(1.5)
bgap_x = Inches(0.28)
bgap_y = Inches(0.25)

for i, (b_title, b_desc, b_col) in enumerate(benefits):
    row = i // 4
    col = i % 4
    x = bx_start + col * (bw + bgap_x)
    y = by_start + row * (bh + bgap_y)
    
    b_card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, bw, bh)
    b_card.fill.solid()
    b_card.fill.fore_color.rgb = COLOR_CARD
    b_card.line.color.rgb = b_col
    b_card.line.width = Pt(1.5)
    
    tf = b_card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.18)
    tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.18)
    
    p = tf.paragraphs[0]
    p.text = b_title
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = b_col
    p.space_after = Pt(8)
    
    p2 = tf.add_paragraph()
    p2.text = b_desc
    p2.font.name = "Arial"
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_WHITE
    p2.space_after = Pt(3)

# Bottom Value Summary Banner
b_banner = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.1), Inches(11.7), Inches(0.65))
b_banner.fill.solid()
b_banner.fill.fore_color.rgb = COLOR_CARD
b_banner.line.color.rgb = COLOR_CARD_BORDER

tf_bb = b_banner.text_frame
p_bb = tf_bb.paragraphs[0]
p_bb.text = "🌟 SOCIAL & ECONOMIC IMPACT: Democratizes executive-grade career coaching for millions of students and job seekers worldwide."
p_bb.font.name = "Arial"
p_bb.font.size = Pt(12)
p_bb.font.bold = True
p_bb.font.color.rgb = COLOR_GOLD_LIGHT
p_bb.alignment = PP_ALIGN.CENTER


# ==========================================
# SLIDE 7: RESEARCH, METRICS & REFERENCES
# ==========================================
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide7)
add_header(slide7, 7, "RESEARCH, BENCHMARKS & REFERENCES")

# 4 Key Stat Metrics at the top
metrics = [
    ("75%+", "Resumes filtered out by ATS before human review", COLOR_ROSE),
    ("< 200ms", "End-to-end NLP analysis latency per resume", COLOR_CYAN),
    ("$0.00", "Cost per analysis (Zero external API dependencies)", COLOR_EMERALD),
    ("100%", "Test pass rate across all 8 core unit modules", COLOR_GOLD)
]

mw = Inches(2.7)
mh = Inches(1.3)
mx_start = Inches(0.8)
mgap = Inches(0.28)

for idx, (m_val, m_lbl, m_col) in enumerate(metrics):
    mx = mx_start + idx * (mw + mgap)
    m_box = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, mx, Inches(1.4), mw, mh)
    m_box.fill.solid()
    m_box.fill.fore_color.rgb = COLOR_CARD
    m_box.line.color.rgb = m_col
    m_box.line.width = Pt(1.5)
    
    tf = m_box.text_frame
    tf.word_wrap = True
    tf.margin_top = Inches(0.12)
    
    p = tf.paragraphs[0]
    p.text = m_val
    p.font.name = "Arial"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = m_col
    p.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = m_lbl
    p2.font.name = "Arial"
    p2.font.size = Pt(10)
    p2.font.color.rgb = COLOR_MUTED
    p2.alignment = PP_ALIGN.CENTER

# Left Column: Market Opportunity & Growth
card7_left = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.9), Inches(5.6), Inches(2.8))
card7_left.fill.solid()
card7_left.fill.fore_color.rgb = COLOR_CARD
card7_left.line.color.rgb = COLOR_CARD_BORDER

tf_c7l = card7_left.text_frame
tf_c7l.word_wrap = True
tf_c7l.margin_left = Inches(0.25)
tf_c7l.margin_top = Inches(0.2)

p_7l = tf_c7l.paragraphs[0]
p_7l.text = "📈 MARKET RESEARCH & OPPORTUNITY"
p_7l.font.name = "Arial"
p_7l.font.size = Pt(14)
p_7l.font.bold = True
p_7l.font.color.rgb = COLOR_CYAN
p_7l.space_after = Pt(8)

mkt_points = [
    "Global HR-Tech & Talent Acquisition market projected to reach $42.5 Billion by 2030 (CAGR 12.8%).",
    "Over 98% of Fortune 500 enterprises use ATS (Workday, Taleo, Greenhouse, Lever).",
    "High Student Need: 80% of university graduates submit unformatted resumes lacking quantifiable metrics.",
    "B2B & B2C Revenue Potential: SaaS subscription for university placement cells and career coaching bootcamps."
]
for mp in mkt_points:
    p = tf_c7l.add_paragraph()
    p.text = "• " + mp
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(4)

# Right Column: Technical References & Stack
card7_right = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.9), Inches(5.7), Inches(2.8))
card7_right.fill.solid()
card7_right.fill.fore_color.rgb = COLOR_CARD
card7_right.line.color.rgb = COLOR_GOLD

tf_c7r = card7_right.text_frame
tf_c7r.word_wrap = True
tf_c7r.margin_left = Inches(0.25)
tf_c7r.margin_top = Inches(0.2)

p_7r = tf_c7r.paragraphs[0]
p_7r.text = "📚 TECHNICAL REFERENCES & FRAMEWORKS"
p_7r.font.name = "Arial"
p_7r.font.size = Pt(14)
p_7r.font.bold = True
p_7r.font.color.rgb = COLOR_GOLD
p_7r.space_after = Pt(8)

tech_refs = [
    "Scikit-Learn: Salient n-gram extraction via TF-IDF Vectorizer & Cosine Similarity distance metrics.",
    "Streamlit Community Cloud: Scalable Python web application delivery with instant reactive state.",
    "Google XYZ Formula: 'Accomplished [X] as measured by [Y], by doing [Z]' career framework.",
    "PyPDF & Python-Docx: Binary document text stream decoders with native XML unzipping fallbacks.",
    "Sentence-Transformers: MiniLM dense embeddings for deep semantic vector verification."
]
for tr in tech_refs:
    p = tf_c7r.add_paragraph()
    p.text = "• " + tr
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(4)

# Bottom Thank You & Links Banner
ty_banner = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.9), Inches(11.7), Inches(0.85))
ty_banner.fill.solid()
ty_banner.fill.fore_color.rgb = COLOR_CARD
ty_banner.line.color.rgb = COLOR_GOLD

tf_ty = ty_banner.text_frame
tf_ty.margin_top = Inches(0.12)
p_ty1 = tf_ty.paragraphs[0]
p_ty1.text = "THANK YOU! QUESTIONS & DISCUSSION"
p_ty1.font.name = "Arial"
p_ty1.font.size = Pt(14)
p_ty1.font.bold = True
p_ty1.font.color.rgb = COLOR_GOLD_LIGHT
p_ty1.alignment = PP_ALIGN.CENTER

p_ty2 = tf_ty.add_paragraph()
p_ty2.text = "Live Web App: https://sparkcv.streamlit.app   •   GitHub: https://github.com/sulthan-shaik77/Sparkcv"
p_ty2.font.name = "Arial"
p_ty2.font.size = Pt(11)
p_ty2.font.color.rgb = COLOR_WHITE
p_ty2.alignment = PP_ALIGN.CENTER

# Save Presentation
output_path = os.path.join(os.getcwd(), "SparkCV_Project_Presentation.pptx")
prs.save(output_path)
print(f"SUCCESS: Presentation created at: {output_path}")
