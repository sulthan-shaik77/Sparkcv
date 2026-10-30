"""
Generates the self-contained 11-slide presentation.html with:
- Fullscreen and keyboard navigation
- Embedded high-res certificate image
- In-depth technical machine learning learnings
- Slide navigation counter (1 to 11)
"""

import os

base_dir = r"C:\Users\sulth\.gemini\antigravity\scratch\streamlit_resume_analyzer"
cert_b64_path = os.path.join(base_dir, "assets", "cert_b64.txt")

with open(cert_b64_path, "r", encoding="utf-8") as f:
    cert_b64 = f.read().strip()

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SparkCV - Summer Internship-1 Review 1 Presentation (Shaik Sulthan)</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Cinzel:wght@700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0b1120;
            --card-bg: rgba(30, 41, 59, 0.75);
            --card-border: rgba(51, 65, 85, 0.8);
            --gold: #fbbf24;
            --gold-light: #fef08a;
            --cyan: #38bdf8;
            --emerald: #34d399;
            --rose: #f43f5e;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, sans-serif;
        }}

        body {{
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow-x: hidden;
            background-image: radial-gradient(ellipse at 50% 0%, rgba(30, 58, 138, 0.25) 0%, rgba(11, 17, 32, 0.95) 100%);
        }}

        .controls-bar {{
            position: fixed;
            top: 15px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            gap: 12px;
            background: rgba(15, 23, 42, 0.88);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(251, 191, 36, 0.35);
            padding: 8px 20px;
            border-radius: 999px;
            z-index: 100;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.6);
        }}

        .controls-bar button {{
            background: rgba(255, 255, 255, 0.08);
            color: var(--text-main);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .controls-bar button:hover {{
            background: var(--gold);
            color: #0b1120;
            border-color: var(--gold);
        }}

        .slide-counter {{
            font-size: 0.9rem;
            font-weight: 700;
            color: var(--gold);
            min-width: 90px;
            text-align: center;
        }}

        .presentation-container {{
            width: 95vw;
            max-width: 1280px;
            aspect-ratio: 16 / 9;
            position: relative;
            background: radial-gradient(ellipse at 50% 12%, rgba(26, 32, 53, 0.96) 0%, rgba(15, 23, 42, 0.98) 100%);
            border: 1px solid rgba(251, 191, 36, 0.35);
            border-radius: 20px;
            box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.9), 0 0 40px rgba(251, 191, 36, 0.12);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            padding: 34px 44px 26px 44px;
        }}

        .slide {{
            display: none;
            flex-direction: column;
            width: 100%;
            height: 100%;
            animation: fadeIn 0.35s ease forwards;
        }}

        .slide.active {{
            display: flex;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .slide-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 12px;
        }}

        .slide-tag {{
            font-size: 0.75rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            margin-bottom: 4px;
        }}

        .slide-title {{
            font-size: 1.6rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.01em;
        }}

        .slide-subtitle {{
            font-size: 0.85rem;
            color: var(--cyan);
            margin-top: 2px;
        }}

        .slide-badge {{
            background: rgba(30, 41, 59, 0.85);
            border: 1px solid var(--gold);
            color: var(--gold);
            width: 36px;
            height: 36px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 1.1rem;
        }}

        .slide-content {{
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .slide-footer {{
            margin-top: auto;
            padding-top: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: var(--text-muted);
        }}

        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 22px;
            height: 100%;
        }}

        .grid-4 {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 20px;
            backdrop-filter: blur(10px);
            display: flex;
            flex-direction: column;
        }}

        .card.gold-border {{ border-color: rgba(251, 191, 36, 0.5); }}
        .card.cyan-border {{ border-color: rgba(56, 189, 248, 0.5); }}
        .card.emerald-border {{ border-color: rgba(52, 211, 153, 0.5); }}
        .card.rose-border {{ border-color: rgba(244, 63, 94, 0.5); }}

        .card-header {{
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .bullet-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .bullet-list li {{
            font-size: 0.88rem;
            line-height: 1.45;
            color: #e2e8f0;
            position: relative;
            padding-left: 18px;
        }}

        .bullet-list li::before {{
            content: "•";
            position: absolute;
            left: 0;
            color: var(--gold);
            font-weight: bold;
            font-size: 1.2rem;
            line-height: 1;
        }}

        .bullet-list.emerald-bullets li::before {{ color: var(--emerald); content: "✔"; font-size: 0.9rem; }}

        .title-hero {{
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 14px;
        }}

        .title-hero h1 {{
            font-family: 'Cinzel', serif;
            font-size: 2.7rem;
            font-weight: 800;
            background: linear-gradient(180deg, #fef3c7 0%, #fbbf24 45%, #b45309 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.2;
        }}

        .title-hero h2 {{
            font-size: 1.25rem;
            font-weight: 500;
            color: var(--cyan);
        }}

        .meta-table {{
            width: 100%;
            max-width: 880px;
            margin: 18px auto 0 auto;
            border-collapse: separate;
            border-spacing: 0 8px;
        }}

        .meta-table td {{
            padding: 8px 16px;
            font-size: 0.88rem;
            background: rgba(30, 41, 59, 0.6);
        }}

        .meta-table tr td:first-child {{
            border-radius: 8px 0 0 8px;
            font-weight: 700;
            color: var(--gold);
            width: 28%;
            border-left: 2px solid var(--gold);
        }}

        .meta-table tr td:last-child {{
            border-radius: 0 8px 8px 0;
            color: #ffffff;
        }}

        @media print {{
            .controls-bar {{ display: none !important; }}
            body {{ background: #0f172a !important; -webkit-print-color-adjust: exact; }}
            .presentation-container {{
                width: 100vw !important;
                height: 100vh !important;
                aspect-ratio: auto !important;
                box-shadow: none !important;
                border: none !important;
                border-radius: 0 !important;
                page-break-after: always;
            }}
            .slide {{ display: flex !important; }}
        }}
    </style>
</head>
<body>

    <div class="controls-bar">
        <button onclick="prevSlide()">◀ Previous</button>
        <span class="slide-counter" id="slideIndicator">Slide 1 / 11</span>
        <button onclick="nextSlide()">Next ▶</button>
        <button onclick="toggleFullScreen()">⛶ Fullscreen</button>
        <button onclick="window.print()">🖨️ Export PDF</button>
    </div>

    <div class="presentation-container" id="presentation">

        <!-- SLIDE 1: TITLE PAGE -->
        <div class="slide active" id="slide-1">
            <div class="slide-header" style="justify-content: center; border-bottom: none; margin-bottom: 10px;">
                <div style="text-align: center;">
                    <div class="slide-tag">MADANAPALLE INSTITUTE OF TECHNOLOGY & SCIENCE (UGC-AUTONOMOUS)</div>
                </div>
            </div>
            <div class="slide-content">
                <div class="title-hero">
                    <h1>SparkCV: AI-Powered Resume Matcher & ATS Optimizer</h1>
                    <h2>Summer Internship-1, Review 1 • Department of Computer Science and Engineering</h2>
                    <table class="meta-table">
                        <tr><td>Student Name</td><td>Shaik Sulthan</td></tr>
                        <tr><td>Roll Number</td><td>23691A37B6</td></tr>
                        <tr><td>Internship Domain</td><td>Machine Learning</td></tr>
                        <tr><td>Internship Company</td><td>Slash Mark IT Solutions (OPC) Pvt. Ltd. (ISO 9001:2015 & DPIIT-Recognized)</td></tr>
                        <tr><td>Internal / External Mentor</td><td>Mr. Bhabaani Sankar Samantray</td></tr>
                        <tr><td>Live Cloud Application</td><td><strong>https://sparkcv.streamlit.app</strong> | Repo: <strong>github.com/sulthan-shaik77/Sparkcv</strong></td></tr>
                    </table>
                </div>
            </div>
            <div class="slide-footer">
                <span>Madanapalle Institute of Technology & Science</span>
                <span>Summer Internship-1 Review 1</span>
            </div>
        </div>

        <!-- SLIDE 2: MY INTERNSHIP PROFILE -->
        <div class="slide" id="slide-2">
            <div class="slide-header">
                <div>
                    <div class="slide-tag">MADANAPALLE INSTITUTE OF TECHNOLOGY & SCIENCE</div>
                    <div class="slide-title">My Internship Profile & Objectives</div>
                    <div class="slide-subtitle">Department of Computer Science and Engineering • Summer Internship-1, Review 1</div>
                </div>
                <div class="slide-badge">2</div>
            </div>
            <div class="slide-content">
                <div class="grid-2">
                    <div class="card gold-border">
                        <div class="card-header" style="color: var(--gold);">👤 About Me & Organization</div>
                        <ul class="bullet-list">
                            <li><strong>Student Name:</strong> Shaik Sulthan</li>
                            <li><strong>Roll Number:</strong> 23691A37B6 (B.Tech CSE)</li>
                            <li><strong>Domain:</strong> Machine Learning</li>
                            <li><strong>Company:</strong> Slash Mark IT Solutions (OPC) Pvt. Ltd.</li>
                            <li><strong>Period:</strong> 20 May to 20 July 2026 (2 Months)</li>
                            <li><strong>Mode:</strong> Virtual (Online)</li>
                            <li><strong>Project:</strong> SparkCV (AI Job Description Analyzer & Resume Optimizer)</li>
                            <li><strong>Mentor:</strong> Mr. Bhabaani Sankar Samantray</li>
                        </ul>
                    </div>
                    <div class="card emerald-border">
                        <div class="card-header" style="color: var(--emerald);">🎯 Internship Focus & Competencies</div>
                        <ul class="bullet-list emerald-bullets">
                            <li><strong>Basics of Machine Learning:</strong> Supervised learning, classification, and text analytics.</li>
                            <li><strong>Data Collection & Ingestion:</strong> Multi-format text processing from real-world resumes and JDs.</li>
                            <li><strong>Data Preprocessing & Cleaning:</strong> Tokenization, stopwords filtering, and regex normalization.</li>
                            <li><strong>Exploratory Data Analysis (EDA):</strong> Extracting patterns and building a 250+ skill ontology.</li>
                            <li><strong>Feature Engineering:</strong> Statistical TF-IDF vectorization and n-gram modeling.</li>
                            <li><strong>Mathematical Modeling:</strong> Cosine similarity calculation in vector space.</li>
                            <li><strong>Model Evaluation:</strong> Structural ATS linting and automated unit testing.</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>MITS • Summer Internship-1</span>
                <span>Slide 2 of 11</span>
            </div>
        </div>

        <!-- SLIDE 3: INTERNSHIP COMPLETION CERTIFICATE -->
        <div class="slide" id="slide-3">
            <div class="slide-header">
                <div>
                    <div class="slide-tag">MADANAPALLE INSTITUTE OF TECHNOLOGY & SCIENCE</div>
                    <div class="slide-title">Official Internship Completion Certificate</div>
                    <div class="slide-subtitle">Department of Computer Science and Engineering • Summer Internship-1, Review 1</div>
                </div>
                <div class="slide-badge">3</div>
            </div>
            <div class="slide-content">
                <div class="grid-2">
                    <div class="card gold-border" style="padding: 10px; align-items: center; justify-content: center;">
                        <img src="data:image/png;base64,{cert_b64}" style="max-width: 100%; max-height: 100%; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);">
                    </div>
                    <div class="card cyan-border">
                        <div class="card-header" style="color: var(--cyan);">📜 Verified Credential Breakdown</div>
                        <ul class="bullet-list">
                            <li><strong>Issuing Organization:</strong> Slash Mark IT Solutions (OPC) Pvt. Ltd.</li>
                            <li><strong>Accreditations:</strong> ISO 9001:2015 Certified • DPIIT Recognized (Govt. of India)</li>
                            <li><strong>Candidate:</strong> Shaik Sulthan (MITS Madanapalle)</li>
                            <li><strong>Domain:</strong> Machine Learning Internship</li>
                            <li><strong>Intern ID:</strong> SMI85270</li>
                            <li><strong>Period:</strong> 20 May 2026 to 20 July 2026 (2 Months)</li>
                            <li><strong>Academic Credits Awarded:</strong> 4 Credits</li>
                            <li><strong>Mode of Internship:</strong> Virtual (Online)</li>
                            <li><strong>Authorized HR Signatory:</strong> P. Abhishek, Human Resources (HR)</li>
                            <li><strong>Affiliations:</strong> AICTE, APSCHE, #startupindia, MSME</li>
                            <li><strong>Verification Status:</strong> Digitally Sealed & QR Verified</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>MITS • Summer Internship-1</span>
                <span>Slide 3 of 11</span>
            </div>
        </div>

        <!-- SLIDE 4: WHAT I LEARNED IN ML & NLP -->
        <div class="slide" id="slide-4">
            <div class="slide-header">
                <div>
                    <div class="slide-tag">MADANAPALLE INSTITUTE OF TECHNOLOGY & SCIENCE</div>
                    <div class="slide-title">What I Learned: Machine Learning & NLP</div>
                    <div class="slide-subtitle">Key Technical Skills Acquired During the 2-Month Internship at Slash Mark</div>
                </div>
                <div class="slide-badge">4</div>
            </div>
            <div class="slide-content">
                <div class="grid-2" style="grid-template-rows: 1fr 1fr; gap: 16px;">
                    <div class="card cyan-border" style="padding: 16px;">
                        <div class="card-header" style="color: var(--cyan); font-size: 1rem; margin-bottom: 2px;">01. Data Preprocessing & NLP</div>
                        <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; font-weight: 600;">Text Ingestion & Normalization</div>
                        <ul class="bullet-list" style="font-size: 0.84rem;">
                            <li>Extracted raw text from PDF & Word documents</li>
                            <li>Cleaned text by removing stopwords, symbols & punctuation</li>
                            <li>Handled special technical terms (C++, .NET, SQL) using regex</li>
                        </ul>
                    </div>
                    <div class="card gold-border" style="padding: 16px;">
                        <div class="card-header" style="color: var(--gold); font-size: 1rem; margin-bottom: 2px;">02. Skill Taxonomy & Gap Analysis</div>
                        <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; font-weight: 600;">Domain Categorization & Filtering</div>
                        <ul class="bullet-list" style="font-size: 0.84rem;">
                            <li>Curated a library of 250+ technical skills</li>
                            <li>Grouped into Languages, AI/ML, Cloud & Databases</li>
                            <li>Identified missing skills automatically using set-difference</li>
                        </ul>
                    </div>
                    <div class="card emerald-border" style="padding: 16px;">
                        <div class="card-header" style="color: var(--emerald); font-size: 1rem; margin-bottom: 2px;">03. TF-IDF Feature Engineering</div>
                        <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; font-weight: 600;">Word Importance & Vector Modeling</div>
                        <ul class="bullet-list" style="font-size: 0.84rem;">
                            <li>Converted textual resumes into numerical feature vectors</li>
                            <li>Down-weighted common words; highlighted rare tech skills</li>
                            <li>Captured both single keywords & 2-word phrases (bigrams)</li>
                        </ul>
                    </div>
                    <div class="card rose-border" style="padding: 16px;">
                        <div class="card-header" style="color: var(--rose); font-size: 1rem; margin-bottom: 2px;">04. Cosine Similarity & Deployment</div>
                        <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; font-weight: 600;">Mathematical Scoring & Cloud App</div>
                        <ul class="bullet-list" style="font-size: 0.84rem;">
                            <li>Calculated mathematical similarity score (0% to 100%)</li>
                            <li>Balanced 50% skill match + 50% overall context match</li>
                            <li>Built interactive web UI with Python and deployed on Streamlit</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>MITS • Summer Internship-1</span>
                <span>Slide 4 of 11</span>
            </div>
        </div>

        <!-- SLIDE 5: THE PROBLEM -->
        <div class="slide" id="slide-5">
            <div class="slide-header">
                <div>
                    <div class="slide-tag">INDUSTRY CHALLENGE</div>
                    <div class="slide-title">The Problem: Why Students Get Rejected</div>
                    <div class="slide-subtitle">Department of Computer Science and Engineering • Summer Internship-1, Review 1</div>
                </div>
                <div class="slide-badge">5</div>
            </div>
            <div class="slide-content">
                <div class="grid-2">
                    <div class="card rose-border">
                        <div class="card-header" style="color: var(--rose);">🤖 Robots Reject Resumes First</div>
                        <p style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.5;">
                            Most companies use automated software (called ATS — Applicant Tracking Systems) to filter resumes before human HR ever reads them.<br><br>
                            <strong style="color: var(--rose); font-size: 1.1rem;">Over 75% of resumes are rejected automatically</strong> due to formatting traps and keyword mismatches.
                        </p>
                    </div>
                    <div class="card gold-border">
                        <div class="card-header" style="color: var(--gold);">❓ Students Don't Know Why</div>
                        <p style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.5;">
                            Candidates have no visibility into what exact skills are missing from their resumes, so they resort to ineffective keyword stuffing.<br><br>
                            Existing tools give a superficial percentage score, but <strong style="color: var(--gold);">never provide concrete projects or bullet rewrites to bridge gaps</strong>.
                        </p>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>MITS • Summer Internship-1</span>
                <span>Slide 5 of 11</span>
            </div>
        </div>

        <!-- SLIDE 6: OUR SOLUTION: HOW IT WORKS -->
        <div class="slide" id="slide-6">
            <div class="slide-header">
                <div>
                    <div class="slide-tag">END-TO-END PIPELINE</div>
                    <div class="slide-title">Our Solution: How SparkCV Works</div>
                    <div class="slide-subtitle">Department of Computer Science and Engineering • Summer Internship-1, Review 1</div>
                </div>
                <div class="slide-badge">6</div>
            </div>
            <div class="slide-content">
                <div class="grid-4" style="height: 100%;">
                    <div class="card cyan-border" style="text-align: center;">
                        <div style="font-size: 2rem; color: var(--cyan); font-weight: 800; margin-bottom: 8px;">1</div>
                        <div style="font-weight: 700; color: #ffffff; margin-bottom: 6px;">Upload</div>
                        <p style="font-size: 0.82rem; color: var(--text-muted);">Paste or upload resume (.pdf/.docx/.txt) and target Job Description.</p>
                    </div>
                    <div class="card gold-border" style="text-align: center;">
                        <div style="font-size: 2rem; color: var(--gold); font-weight: 800; margin-bottom: 8px;">2</div>
                        <div style="font-weight: 700; color: #ffffff; margin-bottom: 6px;">Find Skills</div>
                        <p style="font-size: 0.82rem; color: var(--text-muted);">Extracts and compares 250+ hard skills across both documents.</p>
                    </div>
                    <div class="card emerald-border" style="text-align: center;">
                        <div style="font-size: 2rem; color: var(--emerald); font-weight: 800; margin-bottom: 8px;">3</div>
                        <div style="font-weight: 700; color: #ffffff; margin-bottom: 6px;">Get a Score</div>
                        <p style="font-size: 0.82rem; color: var(--text-muted);">Computes balanced score using TF-IDF cosine similarity and skill coverage.</p>
                    </div>
                    <div class="card rose-border" style="text-align: center;">
                        <div style="font-size: 2rem; color: var(--rose); font-weight: 800; margin-bottom: 8px;">4</div>
                        <div style="font-weight: 700; color: #ffffff; margin-bottom: 6px;">Fix It</div>
                        <p style="font-size: 0.82rem; color: var(--text-muted);">Generates portfolio projects, Google XYZ bullets, and audit report.</p>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>Built with Python & Streamlit • Works on phone, laptop & desktop</span>
                <span>Slide 6 of 11</span>
            </div>
        </div>

        <!-- SLIDE 7: HOW THE SCORE WORKS -->
        <div class="slide" id="slide-7">
            <div class="slide-header">
                <div>
                    <div class="slide-tag">SCORING METHODOLOGY</div>
                    <div class="slide-title">How the Balanced Match Score Works</div>
                    <div class="slide-subtitle">Department of Computer Science and Engineering • Summer Internship-1, Review 1</div>
                </div>
                <div class="slide-badge">7</div>
            </div>
            <div class="slide-content">
                <div class="grid-2">
                    <div class="card gold-border">
                        <div class="card-header" style="color: var(--gold);">⚖️ Dual Mathematical Balance</div>
                        <p style="font-size: 0.95rem; color: #ffffff; margin-bottom: 12px; font-weight: 600;">
                            Final Score = (50% Skill Match) + (50% Semantic Meaning Match)
                        </p>
                        <p style="font-size: 0.84rem; color: var(--text-muted); line-height: 1.5;">
                            • <strong>Skill Match (50%):</strong> Do you have the specific technical tools the job asks for?<br>
                            • <strong>Meaning Match (50%):</strong> Does your experience and wording actually fit the job description?<br><br>
                            <em>Using both parts stops people from just stuffing keywords to cheat the system!</em>
                        </p>
                    </div>
                    <div class="card cyan-border">
                        <div class="card-header" style="color: var(--cyan);">🎯 3-Tier Calibrated Verdicts</div>
                        <ul class="bullet-list" style="gap: 12px;">
                            <li><strong style="color: var(--rose);">Below 50%:</strong> ❌ Weak — Missing critical core skills; needs major rework.</li>
                            <li><strong style="color: var(--gold);">50% – 75%:</strong> ⚠️ Moderate — Solid foundation, but needs tweaking.</li>
                            <li><strong style="color: var(--emerald);">Above 75%:</strong> ✅ Strong Match — Perfect alignment; ready to apply!</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>MITS • Summer Internship-1</span>
                <span>Slide 7 of 11</span>
            </div>
        </div>

        <!-- SLIDE 8: WHAT YOU GET -->
        <div class="slide" id="slide-8">
            <div class="slide-header">
                <div>
                    <div class="slide-tag">FEATURES & DELIVERABLES</div>
                    <div class="slide-title">What the Candidate Gets: 4 Actionable Tools</div>
                    <div class="slide-subtitle">Department of Computer Science and Engineering • Summer Internship-1, Review 1</div>
                </div>
                <div class="slide-badge">8</div>
            </div>
            <div class="slide-content">
                <div class="grid-2" style="grid-template-rows: 1fr 1fr; gap: 14px;">
                    <div class="card cyan-border" style="padding: 14px;">
                        <div style="font-weight: 700; color: var(--cyan); margin-bottom: 4px;">1. Skill Gap Analysis</div>
                        <p style="font-size: 0.82rem; color: #cbd5e1;">Green badges for matched skills, red badges for missing skills.</p>
                    </div>
                    <div class="card gold-border" style="padding: 14px;">
                        <div style="font-weight: 700; color: var(--gold); margin-bottom: 4px;">2. Google XYZ Bullet Rewriter</div>
                        <p style="font-size: 0.82rem; color: #cbd5e1;">Parameterizes weak bullets into: <em>Accomplished [X] measured by [Y] by doing [Z]</em>.</p>
                    </div>
                    <div class="card emerald-border" style="padding: 14px;">
                        <div style="font-weight: 700; color: var(--emerald); margin-bottom: 4px;">3. Dynamic Portfolio Projects</div>
                        <p style="font-size: 0.82rem; color: #cbd5e1;">Recommends 2-3 production-grade project blueprints to fill missing skills.</p>
                    </div>
                    <div class="card rose-border" style="padding: 14px;">
                        <div style="font-weight: 700; color: var(--rose); margin-bottom: 4px;">4. Structural ATS Linter</div>
                        <p style="font-size: 0.82rem; color: #cbd5e1;">Checks word count, contact details, sections, and quantified metrics density.</p>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>MITS • Summer Internship-1</span>
                <span>Slide 8 of 11</span>
            </div>
        </div>

        <!-- SLIDE 9: WHY IT IS SAFE & PRACTICAL -->
        <div class="slide" id="slide-9">
            <div class="slide-header">
                <div>
                    <div class="slide-tag">ENGINEERING HIGHLIGHTS</div>
                    <div class="slide-title">Why It Is Safe, Fast & Practical</div>
                    <div class="slide-subtitle">Department of Computer Science and Engineering • Summer Internship-1, Review 1</div>
                </div>
                <div class="slide-badge">9</div>
            </div>
            <div class="slide-content">
                <div class="grid-2">
                    <div class="card emerald-border">
                        <div class="card-header" style="color: var(--emerald);">🔒 100% Private & In-Memory</div>
                        <p style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.5;">
                            • Candidate resumes are processed locally in-memory.<br>
                            • <strong>Zero PII leaks:</strong> Resume data is never stored, sold, or shared with third parties.<br>
                            • No reliance on expensive, slow, external LLM APIs (OpenAI/Anthropic).
                        </p>
                    </div>
                    <div class="card gold-border">
                        <div class="card-header" style="color: var(--gold);">⚡ Zero Cost & Sub-0.2s Speed</div>
                        <p style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.5;">
                            • <strong>Free forever:</strong> Zero API subscription fees, completely scalable.<br>
                            • <strong>Sub-200ms latency:</strong> Immediate results vs 15-30s on heavy generative AI.<br>
                            • <strong>Universal file support:</strong> Handles PDF, Word (.docx), and Plain Text.
                        </p>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>MITS • Summer Internship-1</span>
                <span>Slide 9 of 11</span>
            </div>
        </div>

        <!-- SLIDE 10: IMPACT -->
        <div class="slide" id="slide-10">
            <div class="slide-header">
                <div>
                    <div class="slide-tag">METRICS & RESULTS</div>
                    <div class="slide-title">Measurable Impact & Validation</div>
                    <div class="slide-subtitle">Department of Computer Science and Engineering • Summer Internship-1, Review 1</div>
                </div>
                <div class="slide-badge">10</div>
            </div>
            <div class="slide-content">
                <div class="grid-4" style="height: 100%;">
                    <div class="card rose-border" style="text-align: center;">
                        <div style="font-size: 2.2rem; font-weight: 800; color: var(--rose);">75%+</div>
                        <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">Resumes rejected by robots before human review</div>
                    </div>
                    <div class="card cyan-border" style="text-align: center;">
                        <div style="font-size: 2.2rem; font-weight: 800; color: var(--cyan);">&lt; 0.2s</div>
                        <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">End-to-end NLP analysis execution speed</div>
                    </div>
                    <div class="card emerald-border" style="text-align: center;">
                        <div style="font-size: 2.2rem; font-weight: 800; color: var(--emerald);">$0.00</div>
                        <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">Cost per scan with zero recurring cloud API bills</div>
                    </div>
                    <div class="card gold-border" style="text-align: center;">
                        <div style="font-size: 2.2rem; font-weight: 800; color: var(--gold);">8 / 8</div>
                        <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">Automated unit tests passing with 100% success</div>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>Free career coaching for students & job seekers everywhere</span>
                <span>Slide 10 of 11</span>
            </div>
        </div>

        <!-- SLIDE 11: THANK YOU -->
        <div class="slide" id="slide-11">
            <div class="slide-content" style="align-items: center; justify-content: center; text-align: center;">
                <h1 style="font-family: 'Cinzel', serif; font-size: 3rem; color: var(--gold); margin-bottom: 12px;">Thank You!</h1>
                <h2 style="font-size: 1.4rem; color: #ffffff; margin-bottom: 24px;">Questions & Discussion</h2>
                <div class="card gold-border" style="max-width: 650px; padding: 20px; text-align: center;">
                    <p style="font-size: 1rem; color: #ffffff; margin-bottom: 8px;">
                        🌐 <strong>Live Cloud App:</strong> <a href="https://sparkcv.streamlit.app" target="_blank" style="color: var(--cyan); text-decoration: none;">sparkcv.streamlit.app</a>
                    </p>
                    <p style="font-size: 1rem; color: #ffffff;">
                        💻 <strong>GitHub Code:</strong> <a href="https://github.com/sulthan-shaik77/Sparkcv" target="_blank" style="color: var(--gold); text-decoration: none;">github.com/sulthan-shaik77/Sparkcv</a>
                    </p>
                </div>
            </div>
            <div class="slide-footer">
                <span>Shaik Sulthan (23691A37B6) • Madanapalle Institute of Technology & Science</span>
                <span>Slide 11 of 11</span>
            </div>
        </div>

    </div>

    <script>
        let currentSlide = 1;
        const totalSlides = 11;

        function showSlide(n) {{
            if (n < 1) n = 1;
            if (n > totalSlides) n = totalSlides;
            currentSlide = n;

            for (let i = 1; i <= totalSlides; i++) {{
                const el = document.getElementById(`slide-${{i}}`);
                if (el) el.classList.remove('active');
            }}

            const activeEl = document.getElementById(`slide-${{currentSlide}}`);
            if (activeEl) activeEl.classList.add('active');

            document.getElementById('slideIndicator').innerText = `Slide ${{currentSlide}} / ${{totalSlides}}`;
        }}

        function nextSlide() {{
            if (currentSlide < totalSlides) {{
                showSlide(currentSlide + 1);
            }}
        }}

        function prevSlide() {{
            if (currentSlide > 1) {{
                showSlide(currentSlide - 1);
            }}
        }}

        function toggleFullScreen() {{
            const elem = document.getElementById("presentation");
            if (!document.fullscreenElement) {{
                if (elem.requestFullscreen) {{
                    elem.requestFullscreen();
                }} else if (elem.webkitRequestFullscreen) {{
                    elem.webkitRequestFullscreen();
                }}
            }} else {{
                if (document.exitFullscreen) {{
                    document.exitFullscreen();
                }}
            }}
        }}

        document.addEventListener('keydown', function(e) {{
            if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
                nextSlide();
            }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
                prevSlide();
            }} else if (e.key.toLowerCase() === 'f') {{
                toggleFullScreen();
            }}
        }});
    </script>
</body>
</html>
"""

html_path = os.path.join(base_dir, "presentation.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"SUCCESS: Generated 11-slide presentation.html at {html_path}")
