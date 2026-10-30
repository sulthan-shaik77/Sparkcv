"""
Comprehensive Presentation Builder for SparkCV:
Incorporates:
1. Official Slash Mark Internship Completion Certificate (Slide 3)
2. In-Depth Technical Machine Learning Learnings for Summer Internship-1 Review 1 (Slide 4)
3. Correct slide ordering and numbers across all 11 slides.
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Paths
base_dir = r"C:\Users\sulth\.gemini\antigravity\scratch\streamlit_resume_analyzer"
src_pptx = r"C:\Users\sulth\.gemini\antigravity\brain\f74cd3b1-9192-45da-be89-9a6b94d0ca08\.user_uploaded\media_1793354030402_5e64ed81.pptx"
cert_img_path = os.path.join(base_dir, "assets", "slashmark_certificate_full.png")
dst_pptx = os.path.join(base_dir, "SparkCV_Project_Presentation.pptx")

prs = pptx.Presentation(src_pptx)
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Styling Constants
COLOR_BG = RGBColor(15, 23, 42)          # Deep Slate Navy #0F172A
COLOR_CARD = RGBColor(30, 41, 59)        # Card Navy #1E293B
COLOR_GOLD = RGBColor(251, 191, 36)      # Warm Gold #FBBF24
COLOR_CYAN = RGBColor(56, 189, 248)      # Cyan #38BDF8
COLOR_EMERALD = RGBColor(52, 211, 153)   # Green #34D399
COLOR_ROSE = RGBColor(244, 63, 94)       # Rose #F43F5E
COLOR_WHITE = RGBColor(248, 250, 252)    # White #F8FAFC
COLOR_MUTED = RGBColor(148, 163, 184)    # Cool Gray #94A3B8

blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]

def set_slide_bg(slide):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG

def add_standard_header(slide, slide_num, title_text):
    # Top Tag
    t_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(9.0), Inches(0.35))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "MADANAPALLE INSTITUTE OF TECHNOLOGY & SCIENCE"
    p_t.font.name = "Arial"
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_MUTED

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.7), Inches(11.0), Inches(0.75))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Arial"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.6), Inches(1.45), Inches(11.5), Inches(0.35))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "Department of Computer Science and Engineering  •  Summer Internship-1, Review 1"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = COLOR_CYAN

    # Slide Number
    num_box = slide.shapes.add_textbox(Inches(12.2), Inches(0.4), Inches(0.6), Inches(0.4))
    tf_num = num_box.text_frame
    p_num = tf_num.paragraphs[0]
    p_num.text = str(slide_num)
    p_num.font.name = "Arial"
    p_num.font.size = Pt(16)
    p_num.font.bold = True
    p_num.font.color.rgb = COLOR_MUTED
    p_num.alignment = PP_ALIGN.RIGHT

# ========================================================
# 1. CREATE SLIDE A: INTERNSHIP COMPLETION CERTIFICATE
# ========================================================
slide_cert = prs.slides.add_slide(blank_layout)
set_slide_bg(slide_cert)
add_standard_header(slide_cert, 3, "Internship Completion Certificate")

# Left Card: Certificate Image Display
card_cert = slide_cert.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.95), Inches(6.5), Inches(5.1))
card_cert.fill.solid()
card_cert.fill.fore_color.rgb = COLOR_CARD
card_cert.line.color.rgb = COLOR_GOLD
card_cert.line.width = Pt(1.5)

# Insert Certificate Image
if os.path.exists(cert_img_path):
    slide_cert.shapes.add_picture(cert_img_path, Inches(0.8), Inches(2.15), width=Inches(6.1), height=Inches(4.6))

# Right Card: Verified Credentials
card_details = slide_cert.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.3), Inches(1.95), Inches(5.4), Inches(5.1))
card_details.fill.solid()
card_details.fill.fore_color.rgb = COLOR_CARD
card_details.line.color.rgb = COLOR_CYAN
card_details.line.width = Pt(1.5)

tf_d = card_details.text_frame
tf_d.word_wrap = True
tf_d.margin_left = Inches(0.28)
tf_d.margin_right = Inches(0.28)
tf_d.margin_top = Inches(0.25)

p_head = tf_d.paragraphs[0]
p_head.text = "Official Credential Verification"
p_head.font.name = "Arial"
p_head.font.size = Pt(15)
p_head.font.bold = True
p_head.font.color.rgb = COLOR_GOLD
p_head.space_after = Pt(12)

cred_items = [
    ("Company:", "Slash Mark IT Solutions (OPC) Pvt. Ltd."),
    ("Recognition:", "ISO 9001:2015 Certified • DPIIT Recognized"),
    ("Location:", "Karimnagar, Telangana, India"),
    ("Candidate:", "Shaik Sulthan (MITS, Madanapalle)"),
    ("Domain:", "Machine Learning Internship"),
    ("Intern ID:", "SMI85270"),
    ("Duration:", "20 May 2026 to 20 July 2026 (2 Months)"),
    ("Credits:", "4 Academic Credits Awarded"),
    ("Mode:", "Virtual (Online)"),
    ("Authorized HR:", "P. Abhishek, Human Resources (HR)"),
    ("Contact:", "hr@slashmark.in"),
    ("Affiliations:", "AICTE, APSCHE, #startupindia, MSME"),
    ("Status:", "Digitally Verified & Completed")
]

for label, val in cred_items:
    p = tf_d.add_paragraph()
    p.text = f"{label:<16} {val}"
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(4)


# ========================================================
# 2. CREATE SLIDE B: WHAT I LEARNED IN MACHINE LEARNING & NLP
# ========================================================
slide_learn = prs.slides.add_slide(blank_layout)
set_slide_bg(slide_learn)
add_standard_header(slide_learn, 4, "What I Learned: Machine Learning & NLP Concepts")

# 4 Key Competency Cards (2x2 Grid)
learn_cards = [
    (
        "1. Data Ingestion & Preprocessing",
        [
            "Multi-Format Parsing: Extracted raw text from PDF streams (pypdf) and Word documents (python-docx) with XML/ZIP fallback.",
            "Text Cleaning Pipeline: Lowercasing, punctuation stripping, and stopword filtering (NLTK) to eliminate non-informative noise.",
            "Token Boundary Protection: Handled technical skills (C++, Go, .NET) using word-boundary regex patterns."
        ],
        Inches(0.6), Inches(1.95), Inches(5.8), Inches(2.4), COLOR_CYAN
    ),
    (
        "2. Exploratory Data Analysis & Ontology",
        [
            "Ontology Engineering: Built a curated 250+ technical skill taxonomy across Languages, Web, Cloud, and AI.",
            "Domain Classification: Structured skills into Backend, Frontend, DevOps, and Machine Learning categories.",
            "Competency Gap Analysis: Formulated set-theoretic logic (JD \\ Resume) to isolate exact missing candidate skills."
        ],
        Inches(6.8), Inches(1.95), Inches(5.9), Inches(2.4), COLOR_GOLD
    ),
    (
        "3. Feature Engineering (TF-IDF Vectorization)",
        [
            "Statistical n-gram Extraction: Unigram + Bigram extraction to capture multi-word skills ('machine learning', 'fastapi').",
            "TF-IDF Weighting: Down-weighted common prose while amplifying rare, role-critical domain technical skills.",
            "Vector Transformation: Converted textual resumes and JDs into high-dimensional normalized feature vectors."
        ],
        Inches(0.6), Inches(4.55), Inches(5.8), Inches(2.45), COLOR_EMERALD
    ),
    (
        "4. Mathematical Modeling & Evaluation",
        [
            "Cosine Similarity: Evaluated semantic alignment using vector dot products: cos(θ) = (A · B) / (||A|| ||B||).",
            "Balanced Hybrid Scoring: Formulated a 50/50 equation (50% Skill Coverage + 50% TF-IDF Cosine Distance).",
            "Model Testing & Deployment: Validated pipeline with 8 automated unit tests and deployed live on Streamlit Cloud."
        ],
        Inches(6.8), Inches(4.55), Inches(5.9), Inches(2.45), COLOR_ROSE
    )
]

for title, points, x, y, w, h, col in learn_cards:
    card = slide_learn.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD
    card.line.color.rgb = col
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.18)

    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.name = "Arial"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = col
    p0.space_after = Pt(8)

    for pt in points:
        p = tf.add_paragraph()
        p.text = "• " + pt
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(4)


# ========================================================
# 3. REORDER SLIDES TO EXACT FINAL SEQUENCE
# ========================================================
# Target sequence:
# 0: Title Page
# 1: My Internship (Student & Project Details)
# 2: Certificate (slide_cert)
# 3: What I Learned (slide_learn)
# 4: The Problem (was 2)
# 5: Our Solution: How It Works (was 3)
# 6: How the Score Works (was 4)
# 7: What You Get (was 5)
# 8: Why It Is Safe and Practical (was 6)
# 9: Impact (was 7)
# 10: Thank You! Questions? (was 8)

sldIdLst = prs.slides._sldIdLst
elems = list(sldIdLst)
target_order = [0, 1, 9, 10, 2, 3, 4, 5, 6, 7, 8]

for el in elems:
    sldIdLst.remove(el)
for idx in target_order:
    sldIdLst.append(elems[idx])

# ========================================================
# 4. UPDATE SLIDE NUMBERS ACCURATELY
# ========================================================
slide_num_mapping = {
    4: "5",   # The Problem
    5: "6",   # Our Solution
    6: "7",   # How the Score Works
    7: "8",   # What You Get
    8: "9",   # Why Safe & Practical
    9: "10"   # Impact
}

for s_idx, new_digit in slide_num_mapping.items():
    s = prs.slides[s_idx]
    for sp in s.shapes:
        if sp.has_text_frame:
            txt = sp.text.strip()
            if txt in ["3", "4", "5", "6", "7", "8"]:
                sp.text_frame.text = new_digit
                p = sp.text_frame.paragraphs[0]
                p.font.name = "Arial"
                p.font.size = Pt(16)
                p.font.bold = True
                p.font.color.rgb = COLOR_MUTED
                p.alignment = PP_ALIGN.RIGHT
                break

prs.save(dst_pptx)
print(f"SUCCESS: Saved updated presentation with {len(prs.slides)} slides at: {dst_pptx}")
