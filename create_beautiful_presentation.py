"""
Professional, High-Aesthetic 11-Slide Presentation Builder for SparkCV
Incorporates:
- Modern executive dark-slate luxury theme (#0B0F19 background, elevated #1E293B cards)
- Vibrant accents: Electric Cyan, Radiant Gold, Emerald Mint, Rose Red
- Slide 4: Simplified, clean, high-impact bullet points (no walls of text)
- Slide 3: Framed certificate + authenticated verification badges
- Balanced typography, proper margins, elegant tag pills
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

base_dir = r"C:\Users\sulth\.gemini\antigravity\scratch\streamlit_resume_analyzer"
cert_img_path = os.path.join(base_dir, "assets", "slashmark_certificate_full.png")
dst_pptx = os.path.join(base_dir, "SparkCV_Project_Presentation.pptx")

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Theme Colors
BG_COLOR = RGBColor(11, 15, 25)         # Deep Obsidian #0B0F19
CARD_BG = RGBColor(24, 34, 53)          # Elevated Slate #182235
CARD_BORDER = RGBColor(51, 65, 85)      # Slate Border #334155
GOLD = RGBColor(245, 158, 11)           # Radiant Amber Gold #F59E0B
CYAN = RGBColor(56, 189, 248)           # Electric Cyan #38BDF8
EMERALD = RGBColor(16, 185, 129)        # Mint Emerald #10B981
ROSE = RGBColor(244, 63, 94)            # Vivid Rose #F43F5E
PURPLE = RGBColor(168, 85, 247)         # Neon Purple #A855F7
TEXT_WHITE = RGBColor(248, 250, 252)    # Crisp White #F8FAFC
TEXT_MUTED = RGBColor(148, 163, 184)    # Cool Gray #94A3B8

def set_slide_background(slide):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, slide_num, title_text, subtitle_text):
    # Top Institution Tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.5), Inches(0.3))
    tf = tag_box.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "MADANAPALLE INSTITUTE OF TECHNOLOGY & SCIENCE  •  DEPT. OF CSE"
    p.font.name = "Arial"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = GOLD

    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(10.0), Inches(0.55))
    tf_t = title_box.text_frame
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = "Arial"
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.32), Inches(10.0), Inches(0.35))
    tf_s = sub_box.text_frame
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitle_text
    p_s.font.name = "Arial"
    p_s.font.size = Pt(11)
    p_s.font.color.rgb = CYAN

    # Slide Number Badge
    num_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.8), Inches(0.55), Inches(0.75), Inches(0.38))
    num_card.fill.solid()
    num_card.fill.fore_color.rgb = CARD_BG
    num_card.line.color.rgb = CARD_BORDER
    num_card.line.width = Pt(1)
    tf_n = num_card.text_frame
    p_n = tf_n.paragraphs[0]
    p_n.text = f"{slide_num:02d}"
    p_n.font.name = "Arial"
    p_n.font.size = Pt(12)
    p_n.font.bold = True
    p_n.font.color.rgb = GOLD
    p_n.alignment = PP_ALIGN.CENTER

    # Subtle Header Accent Line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.68), Inches(11.75), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(30, 41, 59)
    line.line.fill.background()

# ==========================================================
# SLIDE 1: TITLE SLIDE
# ==========================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

# Review Badge Pill
pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(5.8), Inches(0.42))
pill.fill.solid()
pill.fill.fore_color.rgb = CARD_BG
pill.line.color.rgb = GOLD
pill.line.width = Pt(1.5)
tf = pill.text_frame
p = tf.paragraphs[0]
p.text = "★ SUMMER INTERNSHIP-1  •  REVIEW 1  •  4 CREDITS"
p.font.name = "Arial"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = GOLD
p.alignment = PP_ALIGN.CENTER

# Main Title
title_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.5), Inches(1.2))
tf = title_box.text_frame
p = tf.paragraphs[0]
p.text = "SparkCV"
p.font.name = "Arial"
p.font.size = Pt(56)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE

sub_box = s1.shapes.add_textbox(Inches(0.8), Inches(2.75), Inches(11.5), Inches(0.6))
tf = sub_box.text_frame
p = tf.paragraphs[0]
p.text = "AI-Powered Job Description Analyzer & Resume Optimization Engine"
p.font.name = "Arial"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = CYAN

desc_box = s1.shapes.add_textbox(Inches(0.8), Inches(3.4), Inches(11.0), Inches(0.6))
tf = desc_box.text_frame
p = tf.paragraphs[0]
p.text = "An intelligent NLP system that bridges the gap between student resumes and corporate Applicant Tracking Systems (ATS) through automated skill taxonomy matching and mathematical semantic evaluation."
p.font.name = "Arial"
p.font.size = Pt(12)
p.font.color.rgb = TEXT_MUTED

# Two Bottom Cards
# Card 1: Student Presenter
c1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.4))
c1.fill.solid()
c1.fill.fore_color.rgb = CARD_BG
c1.line.color.rgb = CYAN
c1.line.width = Pt(1.5)
tf = c1.text_frame
tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)
p = tf.paragraphs[0]
p.text = "STUDENT PRESENTER"
p.font.name = "Arial"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CYAN
p.space_after = Pt(8)

details1 = [
    ("Name:", "Shaik Sulthan"),
    ("Roll No:", "23691A37B6"),
    ("Department:", "Computer Science & Engineering"),
    ("Institution:", "Madanapalle Institute of Technology & Science (MITS)"),
    ("Academic Year:", "2026-2027 (B.Tech CSE)")
]
for k, v in details1:
    p = tf.add_paragraph()
    p.text = f"{k:<15} {v}"
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(3)

# Card 2: Internship & Guide Details
c2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(4.3), Inches(5.6), Inches(2.4))
c2.fill.solid()
c2.fill.fore_color.rgb = CARD_BG
c2.line.color.rgb = GOLD
c2.line.width = Pt(1.5)
tf = c2.text_frame
tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)
p = tf.paragraphs[0]
p.text = "INTERNSHIP & MENTORSHIP"
p.font.name = "Arial"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = GOLD
p.space_after = Pt(8)

details2 = [
    ("Organization:", "Slash Mark IT Solutions (OPC) Pvt. Ltd."),
    ("Domain:", "Machine Learning & NLP"),
    ("Duration:", "20 May 2026 – 20 July 2026 (2 Months)"),
    ("Internal Guide:", "Mr. Bhabaani Sankar Samantray"),
    ("Recognition:", "DPIIT Recognized • ISO 9001:2015 Certified")
]
for k, v in details2:
    p = tf.add_paragraph()
    p.text = f"{k:<15} {v}"
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(3)

# ==========================================================
# SLIDE 2: MY INTERNSHIP PROFILE
# ==========================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_header(s2, 2, "My Internship Profile", "Academic Credentials, Organization Overview & Project Objectives")

# 3 Balanced Columns
col_width = Inches(3.7)
col_gap = Inches(0.3)
left_base = Inches(0.8)

columns_s2 = [
    (
        "Candidate Information",
        CYAN,
        [
            ("Name", "Shaik Sulthan"),
            ("Roll No", "23691A37B6"),
            ("Department", "Computer Science & Engineering"),
            ("Institution", "MITS, Madanapalle"),
            ("Degree", "B.Tech (CSE)"),
            ("Academic Status", "CGPA: 8.0 (Till III-II)"),
            ("Target Career", "AI / Full-Stack Engineer")
        ]
    ),
    (
        "Internship Organization",
        GOLD,
        [
            ("Company", "Slash Mark IT Solutions"),
            ("Legal Entity", "(OPC) Private Limited"),
            ("Accreditation", "ISO 9001:2015 Certified"),
            ("Government", "DPIIT Recognized Startup"),
            ("Duration", "20 May – 20 July 2026"),
            ("Internship Mode", "Online / Virtual"),
            ("Academic Credits", "4 Credits Awarded")
        ]
    ),
    (
        "Project & Mentorship",
        EMERALD,
        [
            ("Project Title", "SparkCV Resume Engine"),
            ("Internal Guide", "Mr. Bhabaani Sankar Samantray"),
            ("Domain", "Natural Language Processing"),
            ("Core Tech", "Python, Streamlit, Scikit-learn"),
            ("Live URL", "sparkcv.streamlit.app"),
            ("Source Code", "github.com/sulthan-shaik77"),
            ("Deliverables", "Web App, Tests, Presentation")
        ]
    )
]

for i, (title, color, items) in enumerate(columns_s2):
    x = left_base + i * (col_width + col_gap)
    card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.95), col_width, Inches(5.0))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = color
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = color
    p.space_after = Pt(14)

    for k, v in items:
        p = tf.add_paragraph()
        p.text = f"{k}:"
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_MUTED

        p2 = tf.add_paragraph()
        p2.text = v
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_after = Pt(8)

# ==========================================================
# SLIDE 3: INTERNSHIP COMPLETION CERTIFICATE
# ==========================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_header(s3, 3, "Internship Completion Certificate", "Official Verification & Authentication from Slash Mark IT Solutions")

# Left Card: Certificate Graphic
card_cert = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.95), Inches(6.4), Inches(5.0))
card_cert.fill.solid()
card_cert.fill.fore_color.rgb = CARD_BG
card_cert.line.color.rgb = GOLD
card_cert.line.width = Pt(1.5)

if os.path.exists(cert_img_path):
    s3.shapes.add_picture(cert_img_path, Inches(1.0), Inches(2.15), width=Inches(6.0), height=Inches(4.55))

# Right Card: Authenticated Verification Details
card_ver = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), Inches(1.95), Inches(5.05), Inches(5.0))
card_ver.fill.solid()
card_ver.fill.fore_color.rgb = CARD_BG
card_ver.line.color.rgb = CYAN
card_ver.line.width = Pt(1.5)

tf = card_ver.text_frame
tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.28)
p = tf.paragraphs[0]
p.text = "OFFICIAL VERIFICATION"
p.font.name = "Arial"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = GOLD
p.space_after = Pt(12)

cert_records = [
    ("Status", "✔ Officially Verified & Approved"),
    ("Candidate", "Shaik Sulthan (23691A37B6)"),
    ("Intern ID", "SMI85270"),
    ("Company", "Slash Mark IT Solutions (OPC) Pvt. Ltd."),
    ("Registration", "ISO 9001:2015 • DPIIT Recognized"),
    ("Domain", "Machine Learning Internship"),
    ("Internship Period", "20 May 2026 – 20 July 2026 (2 Months)"),
    ("Academic Credits", "4 Credits Awarded"),
    ("Signatory", "P. Abhishek, Human Resources (HR)"),
    ("Verification Email", "hr@slashmark.in"),
    ("Affiliations", "AICTE, APSCHE, MSME, #startupindia")
]

for label, val in cert_records:
    p = tf.add_paragraph()
    p.text = f"{label:<16} : {val}"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    if "✔" in val:
        p.font.color.rgb = EMERALD
        p.font.bold = True
    elif label == "Intern ID":
        p.font.color.rgb = GOLD
        p.font.bold = True
    else:
        p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(5)

# ==========================================================
# SLIDE 4: WHAT I LEARNED: MACHINE LEARNING & NLP (SIMPLIFIED & BEAUTIFUL)
# ==========================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_header(s4, 4, "What I Learned: Machine Learning & NLP", "Key Technical Skills Acquired During the 2-Month Internship")

# 4 Clean, Beautiful Cards (2x2 Grid)
learn_cards_data = [
    (
        "01. Data Preprocessing & NLP",
        CYAN,
        "Text Ingestion & Normalization",
        [
            "Extracted raw text from PDF & Word documents",
            "Cleaned text by removing stopwords, symbols & punctuation",
            "Handled special technical terms (C++, .NET, SQL) using regex"
        ],
        Inches(0.8), Inches(1.95), Inches(5.6), Inches(2.35)
    ),
    (
        "02. Skill Taxonomy & Gap Analysis",
        GOLD,
        "Domain Categorization & Filtering",
        [
            "Curated a library of 250+ technical skills",
            "Grouped into Languages, AI/ML, Cloud & Databases",
            "Identified missing skills automatically using set-difference"
        ],
        Inches(6.9), Inches(1.95), Inches(5.65), Inches(2.35)
    ),
    (
        "03. TF-IDF Feature Engineering",
        EMERALD,
        "Word Importance & Vector Modeling",
        [
            "Converted textual resumes into numerical feature vectors",
            "Down-weighted common words; highlighted rare tech skills",
            "Captured both single keywords & 2-word phrases (bigrams)"
        ],
        Inches(0.8), Inches(4.55), Inches(5.6), Inches(2.35)
    ),
    (
        "04. Cosine Similarity & Deployment",
        PURPLE,
        "Mathematical Scoring & Cloud App",
        [
            "Calculated mathematical similarity score (0% to 100%)",
            "Balanced 50% skill match + 50% overall context match",
            "Built interactive web UI with Python and deployed on Streamlit"
        ],
        Inches(6.9), Inches(4.55), Inches(5.65), Inches(2.35)
    )
]

for title, col, subtitle, points, x, y, w, h in learn_cards_data:
    card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = col
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.18)

    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.name = "Arial"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = col
    p0.space_after = Pt(2)

    p_sub = tf.add_paragraph()
    p_sub.text = subtitle
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(9.5)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.space_after = Pt(8)

    for pt in points:
        p = tf.add_paragraph()
        p.text = "•  " + pt
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(4)

# ==========================================================
# SLIDE 5: THE PROBLEM
# ==========================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_header(s5, 5, "The Problem", "Why Qualified Job Applicants Get Rejected Before an Interview")

prob_cards = [
    (
        "Robots Reject Resumes",
        ROSE,
        "75% Filtered Out",
        "Over 75% of resumes are rejected by Applicant Tracking Systems (ATS) before any human recruiter ever reads them due to missing keywords."
    ),
    (
        "The Black Box Dilemma",
        GOLD,
        "No Clear Feedback",
        "Students and candidates cannot tell which specific skills or qualifications are missing, leading to blind, random keyword stuffing."
    ),
    (
        "Lack of Actionable Help",
        CYAN,
        "Generic Advice",
        "Existing tools only give vague suggestions like 'add more skills' without showing candidates how to rephrase bullet points or fix gaps."
    )
]

for i, (title, color, tag, desc) in enumerate(prob_cards):
    x = Inches(0.8) + i * Inches(4.0)
    card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.2), Inches(3.7), Inches(4.5))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = color
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.28)

    # Tag Badge
    p0 = tf.paragraphs[0]
    p0.text = f"[ {tag.upper()} ]"
    p0.font.name = "Arial"
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = color
    p0.space_after = Pt(8)

    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.name = "Arial"
    p1.font.size = Pt(16)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(14)

    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = "Arial"
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_after = Pt(10)

# ==========================================================
# SLIDE 6: OUR SOLUTION: HOW IT WORKS
# ==========================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_header(s6, 6, "Our Solution: How It Works", "4-Stage Automated Pipeline from Resume Parsing to Instant Optimization")

steps_data = [
    ("01", "Upload", CYAN, "Candidate uploads resume (PDF/Word) and pastes the target job description."),
    ("02", "Find Skills", GOLD, "Engine automatically scans and extracts 250+ technical skills from both texts."),
    ("03", "Get Score", EMERALD, "Mathematical TF-IDF and Cosine Similarity calculate a transparent match score."),
    ("04", "Fix & Optimize", PURPLE, "System provides missing skill checklist and generates Google XYZ bullet rewrites.")
]

for i, (num, title, color, desc) in enumerate(steps_data):
    x = Inches(0.8) + i * Inches(2.98)
    card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.2), Inches(2.75), Inches(4.0))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = color
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.22)

    p0 = tf.paragraphs[0]
    p0.text = num
    p0.font.name = "Arial"
    p0.font.size = Pt(28)
    p0.font.bold = True
    p0.font.color.rgb = color
    p0.space_after = Pt(6)

    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.name = "Arial"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = "Arial"
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_MUTED

# Bottom Tech Stack Banner
banner = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.45), Inches(11.75), Inches(0.6))
banner.fill.solid()
banner.fill.fore_color.rgb = CARD_BG
banner.line.color.rgb = CARD_BORDER
tf_b = banner.text_frame
p_b = tf_b.paragraphs[0]
p_b.text = "Built with Python, Scikit-learn, and Streamlit  •  Fast, responsive & works on phones, laptops and desktops"
p_b.font.name = "Arial"
p_b.font.size = Pt(11)
p_b.font.bold = True
p_b.font.color.rgb = TEXT_WHITE
p_b.alignment = PP_ALIGN.CENTER

# ==========================================================
# SLIDE 7: HOW THE SCORE WORKS (MATHEMATICAL MODEL)
# ==========================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_header(s7, 7, "How the Score Works", "Balanced Mathematical Scoring Engine Combining Skill Coverage & Semantic Similarity")

# 3 Equation Cards
eq_cards = [
    ("Skills Match (50%)", CYAN, "Direct Skill Coverage", "Checks if you have the exact tools, programming languages and frameworks required in the JD."),
    ("Meaning Match (50%)", GOLD, "TF-IDF Cosine Distance", "Measures contextual semantic alignment between project descriptions and role responsibilities."),
    ("Final Score (100%)", EMERALD, "Anti-Gaming Balance", "Prevents artificial keyword stuffing by requiring both explicit skills and real contextual experience.")
]

for i, (title, color, tag, desc) in enumerate(eq_cards):
    x = Inches(0.8) + i * Inches(4.0)
    card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.1), Inches(3.7), Inches(2.8))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = color
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.name = "Arial"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = color
    p0.space_after = Pt(4)

    p1 = tf.add_paragraph()
    p1.text = tag
    p1.font.name = "Arial"
    p1.font.size = Pt(9.5)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_MUTED
    p1.space_after = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = "Arial"
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_WHITE

# Benchmark Tier Cards
benchmarks = [
    ("Below 50%", ROSE, "Weak Match", "Requires significant rework before submitting."),
    ("50% - 75%", GOLD, "Moderate Match", "Getting close; needs missing skills added."),
    ("Above 75%", EMERALD, "Strong Match", "High interview readiness; optimal ATS alignment.")
]

for i, (pct, color, status, advice) in enumerate(benchmarks):
    x = Inches(0.8) + i * Inches(4.0)
    card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(5.15), Inches(3.7), Inches(1.8))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = color
    card.line.width = Pt(1.2)

    tf = card.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
    p0 = tf.paragraphs[0]
    p0.text = pct
    p0.font.name = "Arial"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = color
    p0.space_after = Pt(2)

    p1 = tf.add_paragraph()
    p1.text = f"{status}  •  {advice}"
    p1.font.name = "Arial"
    p1.font.size = Pt(10)
    p1.font.color.rgb = TEXT_WHITE

# ==========================================================
# SLIDE 8: WHAT YOU GET
# ==========================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)
add_header(s8, 8, "What You Get", "Actionable Deliverables and Immediate Guidance Provided by SparkCV")

feat_cards = [
    ("Skill Gap Checklist", CYAN, "Identifies exactly which tools and skills are missing from the resume, categorized by domain."),
    ("Google XYZ Bullet Rewriter", GOLD, "Transforms weak bullet points into high-impact accomplishment statements using Google's formula."),
    ("Targeted Project Suggestions", EMERALD, "Provides high-value project concepts that directly fill candidate skill deficiencies."),
    ("ATS Format Health Check", PURPLE, "Validates resume layout, headings, and font compatibility to ensure seamless robotic parsing.")
]

for i, (title, color, desc) in enumerate(feat_cards):
    row = i // 2
    col = i % 2
    x = Inches(0.8) + col * Inches(6.0)
    y = Inches(2.1) + row * Inches(2.4)
    w = Inches(5.75)
    h = Inches(2.15)

    card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = color
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.margin_left = tf.margin_right = Inches(0.28)
    tf.margin_top = Inches(0.22)

    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.name = "Arial"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = color
    p0.space_after = Pt(8)

    p1 = tf.add_paragraph()
    p1.text = desc
    p1.font.name = "Arial"
    p1.font.size = Pt(11)
    p1.font.color.rgb = TEXT_WHITE

# ==========================================================
# SLIDE 9: WHY IT IS SAFE AND PRACTICAL
# ==========================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9)
add_header(s9, 9, "Why It Is Safe and Practical", "Key Engineering & Architecture Advantages Over Heavy LLM APIs")

safe_cards = [
    (
        "100% Private & In-Memory",
        EMERALD,
        "Zero Data Storage",
        "Resumes are parsed strictly in RAM. Files are never saved to disk, logged, or transmitted to third-party commercial cloud APIs."
    ),
    (
        "Sub-Second Speed (< 0.2s)",
        CYAN,
        "Ultra-Fast Results",
        "Deterministic mathematical algorithms execute in under 200 milliseconds, eliminating slow API wait times and network lag."
    ),
    (
        "Zero Recurring Costs",
        GOLD,
        "$0 Infrastructure Cost",
        "No expensive token billing or API paywalls. Completely free to run for thousands of students and university placement drives."
    )
]

for i, (title, color, tag, desc) in enumerate(safe_cards):
    x = Inches(0.8) + i * Inches(4.0)
    card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.2), Inches(3.7), Inches(4.5))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = color
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.28)

    p0 = tf.paragraphs[0]
    p0.text = f"[ {tag.upper()} ]"
    p0.font.name = "Arial"
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = color
    p0.space_after = Pt(8)

    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.name = "Arial"
    p1.font.size = Pt(16)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(14)

    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = "Arial"
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_MUTED

# ==========================================================
# SLIDE 10: IMPACT & PERFORMANCE METRICS
# ==========================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10)
add_header(s10, 10, "Impact & Metrics", "Real-World Performance Indicators and Production Evaluation")

stat_boxes = [
    ("75%+", ROSE, "Resumes rejected by ATS robots without human review"),
    ("< 0.2s", CYAN, "Turnaround time to scan and score complete resumes"),
    ("$0", EMERALD, "Cost per scan with zero external API dependencies"),
    ("8 / 8", GOLD, "Automated test suites passed with 100% reliability")
]

for i, (big_num, color, label) in enumerate(stat_boxes):
    x = Inches(0.8) + i * Inches(2.98)
    card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.2), Inches(2.75), Inches(3.6))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = color
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.3)

    p0 = tf.paragraphs[0]
    p0.text = big_num
    p0.font.name = "Arial"
    p0.font.size = Pt(40)
    p0.font.bold = True
    p0.font.color.rgb = color
    p0.space_after = Pt(14)

    p1 = tf.add_paragraph()
    p1.text = label
    p1.font.name = "Arial"
    p1.font.size = Pt(11.5)
    p1.font.color.rgb = TEXT_WHITE

# Impact Summary Card
sum_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.05), Inches(11.75), Inches(0.95))
sum_card.fill.solid()
sum_card.fill.fore_color.rgb = CARD_BG
sum_card.line.color.rgb = CARD_BORDER
tf_s = sum_card.text_frame
tf_s.margin_left = tf_s.margin_right = Inches(0.3)
tf_s.margin_top = Inches(0.2)
p = tf_s.paragraphs[0]
p.text = "MISSION: Free, accessible, and privacy-first career empowerment for students and engineering job seekers everywhere."
p.font.name = "Arial"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = GOLD
p.alignment = PP_ALIGN.CENTER

# ==========================================================
# SLIDE 11: THANK YOU & DISCUSSION
# ==========================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11)
add_header(s11, 11, "Thank You!", "Summer Internship-1 Review 1  •  Questions & Discussion")

# Center Card
center_card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(2.0), Inches(9.733), Inches(4.9))
center_card.fill.solid()
center_card.fill.fore_color.rgb = CARD_BG
center_card.line.color.rgb = GOLD
center_card.line.width = Pt(2.0)

tf = center_card.text_frame
tf.margin_left = tf.margin_right = Inches(0.5)
tf.margin_top = Inches(0.4)

p0 = tf.paragraphs[0]
p0.text = "Thank You Respected Faculty & Reviewers!"
p0.font.name = "Arial"
p0.font.size = Pt(24)
p0.font.bold = True
p0.font.color.rgb = TEXT_WHITE
p0.alignment = PP_ALIGN.CENTER
p0.space_after = Pt(8)

p1 = tf.add_paragraph()
p1.text = "I am ready for your valuable questions, feedback, and technical evaluation."
p1.font.name = "Arial"
p1.font.size = Pt(13)
p1.font.color.rgb = CYAN
p1.alignment = PP_ALIGN.CENTER
p1.space_after = Pt(28)

# Links Box
links = [
    ("🌐 Live Deployed Application:", "https://sparkcv.streamlit.app"),
    ("💻 Open-Source GitHub Repository:", "https://github.com/sulthan-shaik77/Sparkcv"),
    ("👤 Presenter:", "Shaik Sulthan  (Roll No: 23691A37B6)"),
    ("🎓 Institution:", "Madanapalle Institute of Technology & Science (MITS)")
]

for label, val in links:
    p = tf.add_paragraph()
    p.text = f"{label:<32} {val}"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(8)
    p.alignment = PP_ALIGN.CENTER

prs.save(dst_pptx)
print(f"SUCCESS: Generated 11-slide beautiful presentation at {dst_pptx}")
