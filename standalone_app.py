"""
Zero-Dependency Standalone Web Server for Smart Job Description Analyzer & Resume Optimizer.
Supports direct text input, PDF (.pdf), Word (.docx, .doc), and Text (.txt) file parsing.
"""

import base64
import http.server
import io
import json
import os
import re
import socketserver
import sys
import webbrowser
import xml.etree.ElementTree as ET
import zipfile
from typing import Dict, Any

from app import (
    calculate_match_metrics,
    generate_project_recommendations,
    lint_resume_structure,
    generate_google_xyz_bullets,
    generate_executive_audit_report,
    SAMPLE_JD_PYTHON_DS,
    SAMPLE_RESUME_MODERATE,
    SAMPLE_RESUME_STRONG,
    SAMPLE_RESUME_WEAK,
    ACTION_VERBS,
    XYZ_EXAMPLES,
    TECHNICAL_SKILLS_TAXONOMY
)

PORT = int(os.environ.get("PORT", 8501))
HOST = os.environ.get("HOST", "0.0.0.0")

def extract_text_from_file_bytes(filename: str, file_bytes: bytes) -> str:
    """Extract clean text from PDF, DOCX, DOC, or TXT file bytes."""
    lower_name = filename.lower()
    
    # 1. Plain Text
    if lower_name.endswith('.txt'):
        for enc in ['utf-8', 'latin-1', 'cp1252']:
            try:
                return file_bytes.decode(enc)
            except Exception:
                continue
        return file_bytes.decode('utf-8', errors='ignore')

    # 2. Microsoft Word Document (.docx)
    elif lower_name.endswith('.docx'):
        # Try python-docx first if available
        try:
            import docx
            doc = docx.Document(io.BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs if p.text]
            if paragraphs:
                return "\n".join(paragraphs)
        except Exception:
            pass

        # Native zero-dependency extractor using zipfile & xml
        try:
            with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
                xml_content = z.read('word/document.xml')
                tree = ET.fromstring(xml_content)
                namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                paragraphs = []
                for p in tree.iterfind('.//w:p', namespaces):
                    texts = [node.text for node in p.iterfind('.//w:t', namespaces) if node.text]
                    if texts:
                        paragraphs.append("".join(texts))
                return "\n".join(paragraphs)
        except Exception as e:
            return f"Error reading Word (.docx) document: {e}"

    # 3. PDF Document (.pdf)
    elif lower_name.endswith('.pdf'):
        # Try pypdf if available
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            pages = [page.extract_text() or "" for page in reader.pages]
            full_text = "\n".join(pages).strip()
            if full_text:
                return full_text
        except Exception:
            pass

        # Try pdfplumber if available
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
                full_text = "\n".join(pages).strip()
                if full_text:
                    return full_text
        except Exception:
            pass

        # Fallback text stream regex extraction
        try:
            raw = file_bytes.decode('latin-1', errors='ignore')
            matches = re.findall(r'\(([\w\s.,;:/\-@#+&!]+)\)\s*Tj', raw)
            if matches:
                return " ".join(matches)
        except Exception:
            pass

        return ""

    # 4. Legacy Word Document (.doc)
    elif lower_name.endswith('.doc'):
        ascii_text = re.findall(rb'[\x20-\x7E\r\n\t]{4,}', file_bytes)
        return "\n".join([t.decode('ascii', errors='ignore') for t in ascii_text])

    return ""


HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800;900&family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <!-- PDF.js for ultra-fast browser-side PDF text extraction -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
    <script>
        if (typeof pdfjsLib !== 'undefined') {
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
        }
    </script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, sans-serif; }
        
        body {
            background-color: #060504;
            background-image: 
                radial-gradient(ellipse at 50% 0%, rgba(20, 16, 12, 0.7) 0%, rgba(6, 5, 4, 0.92) 100%),
                url('/assets/luxury_login_bg.webp');
            background-size: cover;
            background-position: center top;
            background-attachment: fixed;
            background-repeat: no-repeat;
            color: #fdfbf7;
            min-height: 100vh;
            padding: 30px 20px;
        }

        .container { max-width: 1200px; margin: 0 auto; }
        
        @keyframes heroEntrance {
            0% { opacity: 0; transform: translateY(-18px); filter: blur(3px); }
            100% { opacity: 1; transform: translateY(0); filter: blur(0); }
        }
        @keyframes textLiquidShimmer {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes goldGlowPulse {
            0%, 100% { box-shadow: 0 10px 28px -4px rgba(212, 175, 55, 0.4), 0 0 20px rgba(180, 133, 46, 0.3); }
            50% { box-shadow: 0 14px 38px -2px rgba(254, 240, 138, 0.6), 0 0 35px rgba(212, 175, 55, 0.5); }
        }

        .header {
            background: radial-gradient(ellipse at 50% 12%, rgba(28, 24, 20, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%);
            border: 1px solid rgba(212, 175, 55, 0.42);
            border-radius: 20px;
            padding: 32px 36px;
            margin-bottom: 24px;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.92), 0 0 35px rgba(212, 175, 55, 0.16);
            animation: heroEntrance 0.75s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            position: relative;
            overflow: hidden;
        }
        .header::before {
            content: '';
            position: absolute;
            top: 0; left: -100%; width: 200%; height: 2px;
            background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.9), rgba(254, 240, 138, 0.9), transparent);
            animation: borderSweep 6s linear infinite;
        }
        @keyframes borderSweep {
            0% { transform: translateX(0); }
            100% { transform: translateX(50%); }
        }
        .header h1 {
            font-family: 'Cinzel', 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: 0.03em;
            background: linear-gradient(180deg, #fef3c7 0%, #e2be67 45%, #b4852e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 14px;
            text-shadow: 0 2px 14px rgba(212, 175, 55, 0.25);
        }
        .header p { 
            color: #c8bcab; 
            font-size: 0.98rem; 
            margin-top: 8px; 
            font-weight: 400;
            letter-spacing: 0.02em;
        }
        
        .toolbar {
            background: rgba(18, 15, 12, 0.88);
            border: 1px solid rgba(212, 175, 55, 0.35);
            border-radius: 14px;
            padding: 14px 20px;
            margin-bottom: 22px;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
            backdrop-filter: blur(16px);
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.7), 0 0 20px rgba(212, 175, 55, 0.1);
        }
        .toolbar-label { 
            font-family: 'Cinzel', serif;
            font-size: 0.82rem; 
            font-weight: 700; 
            color: #d4af37; 
            text-transform: uppercase; 
            letter-spacing: 0.08em; 
        }
        .btn-preset {
            background: rgba(26, 22, 18, 0.85);
            color: #fdfbf7;
            border: 1px solid rgba(212, 175, 55, 0.3);
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.84rem;
            font-weight: 600;
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .btn-preset:hover {
            background: rgba(212, 175, 55, 0.22);
            color: #fef08a;
            border-color: #fef08a;
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(212, 175, 55, 0.35);
        }
        
        .btn-upload {
            background: linear-gradient(180deg, #f7dd96 0%, #caa14c 45%, #966c1b 100%);
            color: #161005;
            border: 1px solid rgba(254, 240, 138, 0.65);
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-family: 'Cinzel', serif;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.25s ease;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.6);
        }
        .btn-upload:hover {
            filter: brightness(1.08);
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(212, 175, 55, 0.5);
        }
        
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 22px; margin-bottom: 22px; }
        @media (max-width: 768px) { .grid-2 { grid-template-columns: 1fr; } }
        
        .card {
            background: radial-gradient(ellipse at 50% 12%, rgba(24, 20, 16, 0.95) 0%, rgba(12, 10, 9, 0.98) 100%);
            border: 1px solid rgba(212, 175, 55, 0.35);
            border-radius: 18px;
            padding: 24px;
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            box-shadow: 0 16px 40px -8px rgba(0, 0, 0, 0.85), 0 0 25px rgba(212, 175, 55, 0.1);
            transition: border-color 0.25s ease;
        }
        .card:hover { border-color: rgba(212, 175, 55, 0.55); }
        .card h2 { 
            font-family: 'Cinzel', serif;
            font-size: 1.15rem; 
            font-weight: 700; 
            color: #f1ddaa; 
            margin-bottom: 14px; 
            display: flex; 
            align-items: center; 
            justify-content: space-between; 
            flex-wrap: wrap; 
            gap: 8px; 
            letter-spacing: 0.02em;
        }
        
        .dropzone { 
            border: 2px dashed rgba(212, 175, 55, 0.32); 
            border-radius: 12px; 
            transition: all 0.25s ease; 
            position: relative; 
        }
        .dropzone.dragover { 
            border-color: #fef08a; 
            background: rgba(212, 175, 55, 0.1); 
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.35); 
        }
        
        textarea {
            width: 100%;
            height: 280px;
            background: rgba(13, 11, 10, 0.92);
            border: 1px solid rgba(212, 175, 55, 0.28);
            border-radius: 12px;
            color: #f8fafc;
            padding: 14px;
            font-size: 0.92rem;
            resize: vertical;
            outline: none;
            line-height: 1.6;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }
        textarea:focus {
            border-color: #d4af37;
            box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.25), 0 0 20px rgba(212, 175, 55, 0.3);
            background: rgba(18, 15, 13, 0.98);
        }
        
        .btn-analyze {
            width: 100%;
            background: linear-gradient(180deg, #f7dd96 0%, #caa14c 45%, #966c1b 100%);
            color: #161005;
            border: 1px solid rgba(254, 240, 138, 0.7);
            padding: 18px;
            font-size: 1.15rem;
            font-family: 'Cinzel', serif;
            font-weight: 800;
            letter-spacing: 0.14em;
            border-radius: 14px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 12px;
            margin-top: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7), 0 0 25px rgba(212, 175, 55, 0.4), inset 0 1px 2px rgba(255, 255, 255, 0.7);
        }
        .btn-analyze:hover {
            transform: translateY(-2px) scale(1.01);
            filter: brightness(1.08);
            box-shadow: 0 14px 40px rgba(0, 0, 0, 0.8), 0 0 35px rgba(212, 175, 55, 0.65), inset 0 1px 2px rgba(255, 255, 255, 0.9);
        }
        .btn-analyze:active { transform: translateY(1px) scale(0.99); }
        
        .upload-status { font-size: 0.85rem; font-weight: 600; padding: 8px 14px; border-radius: 8px; margin-top: 10px; display: none; }
        .status-success { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); }
        .status-loading { background: rgba(212, 175, 55, 0.15); color: #fef08a; border: 1px solid rgba(212, 175, 55, 0.35); }
        .status-error { background: rgba(244, 63, 94, 0.15); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.35); }
        
        /* Metrics */
        .metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 28px 0 22px 0; }
        @media (max-width: 900px) { .metrics-grid { grid-template-columns: repeat(2, 1fr); } }
        .metric-card {
            background: radial-gradient(ellipse at 50% 12%, rgba(24, 20, 16, 0.94) 0%, rgba(12, 10, 9, 0.98) 100%);
            border: 1px solid rgba(212, 175, 55, 0.35);
            border-radius: 16px;
            padding: 22px 18px;
            text-align: center;
            backdrop-filter: blur(16px);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 14px 32px -6px rgba(0,0,0,0.7), 0 0 20px rgba(212, 175, 55, 0.1);
        }
        .metric-card:hover {
            transform: translateY(-6px) scale(1.02);
            border-color: rgba(212, 175, 55, 0.65);
            box-shadow: 0 20px 42px -8px rgba(0,0,0,0.8), 0 0 30px rgba(212, 175, 55, 0.28);
        }
        .metric-title { font-family: 'Cinzel', serif; font-size: 0.78rem; text-transform: uppercase; color: #c8bcab; font-weight: 700; letter-spacing: 0.08em; }
        .metric-val { font-family: 'Cinzel', serif; font-size: 2.6rem; font-weight: 800; margin: 6px 0; letter-spacing: -0.5px; }
        .metric-sub { font-size: 0.8rem; color: #e2d7c5; background: rgba(18, 15, 12, 0.85); padding: 4px 12px; border-radius: 20px; display: inline-block; border: 1px solid rgba(212, 175, 55, 0.25); }
        
        .verdict-box {
            border-radius: 16px;
            padding: 24px 28px;
            margin-bottom: 26px;
            color: #ffffff;
            backdrop-filter: blur(16px);
            box-shadow: 0 16px 40px -8px rgba(0,0,0,0.75), 0 0 25px rgba(212, 175, 55, 0.12);
            border-left: 6px solid #d4af37;
            border: 1px solid rgba(212, 175, 55, 0.45);
            background: radial-gradient(ellipse at 50% 12%, rgba(28, 24, 20, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%);
        }
        .verdict-box h3 { font-family: 'Cinzel', serif; font-size: 1.35rem; font-weight: 700; margin-bottom: 8px; letter-spacing: 0.02em; }
        .verdict-box p { font-size: 0.98rem; line-height: 1.6; color: #d8cebe; }
        
        .tab-nav {
            display: flex;
            gap: 8px;
            background: rgba(18, 15, 12, 0.9);
            border: 1px solid rgba(212, 175, 55, 0.35);
            border-radius: 14px;
            padding: 6px;
            margin-bottom: 22px;
            flex-wrap: wrap;
            box-shadow: 0 10px 30px -5px rgba(0,0,0,0.6);
        }
        .tab-btn {
            background: transparent;
            border: none;
            color: #a89c8b;
            font-family: 'Cinzel', serif;
            font-weight: 600;
            font-size: 0.88rem;
            letter-spacing: 0.04em;
            padding: 11px 22px;
            cursor: pointer;
            border-radius: 10px;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .tab-btn:hover { color: #fdfbf7; background: rgba(212, 175, 55, 0.15); transform: translateY(-1px); }
        .tab-btn.active {
            color: #fef08a;
            background: linear-gradient(180deg, rgba(212, 175, 55, 0.25) 0%, rgba(180, 133, 46, 0.32) 100%);
            border: 1px solid rgba(212, 175, 55, 0.6);
            box-shadow: 0 0 18px rgba(212, 175, 55, 0.25);
        }
        
        .tab-content { display: none; }
        .tab-content.active { display: block; animation: heroEntrance 0.4s ease forwards; }
        
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            margin: 4px;
            border-radius: 9px;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .badge-match {
            background: rgba(16, 185, 129, 0.16);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }
        .badge-match:hover {
            transform: translateY(-2px) scale(1.06);
            background: rgba(16, 185, 129, 0.28);
            box-shadow: 0 6px 16px rgba(16, 185, 129, 0.3);
        }
        .badge-miss {
            background: rgba(244, 63, 94, 0.16);
            color: #fb7185;
            border: 1px solid rgba(244, 63, 94, 0.4);
        }
        .badge-miss:hover {
            transform: translateY(-2px) scale(1.06);
            background: rgba(244, 63, 94, 0.28);
            box-shadow: 0 6px 16px rgba(244, 63, 94, 0.3);
        }
        .badge-tech {
            background: rgba(212, 175, 55, 0.15);
            color: #fef08a;
            border: 1px solid rgba(212, 175, 55, 0.4);
            font-size: 0.8rem;
        }
        .badge-verb {
            background: rgba(212, 175, 55, 0.12);
            color: #e8cf8d;
            border: 1px solid rgba(212, 175, 55, 0.35);
            transition: all 0.18s ease;
        }
        .badge-verb:hover {
            background: rgba(212, 175, 55, 0.28);
            color: #ffffff;
            transform: translateY(-2px) scale(1.05);
            box-shadow: 0 4px 14px rgba(212, 175, 55, 0.35);
        }
        
        .project-card {
            background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.95) 0%, rgba(12, 10, 9, 0.98) 100%);
            border: 1px solid rgba(212, 175, 55, 0.35);
            border-left: 5px solid #d4af37;
            border-radius: 16px;
            padding: 22px 26px;
            margin-bottom: 20px;
            backdrop-filter: blur(16px);
            box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.65), 0 0 20px rgba(212, 175, 55, 0.1);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .project-card:hover {
            transform: translateX(8px);
            border-color: rgba(212, 175, 55, 0.6);
            border-left-width: 9px;
            box-shadow: 0 18px 38px -6px rgba(0, 0, 0, 0.8), 0 0 25px rgba(212, 175, 55, 0.25);
        }
        .project-title { font-family: 'Cinzel', serif; font-size: 1.25rem; font-weight: 700; color: #fef08a; margin-bottom: 8px; }
        .project-desc { color: #d8cebe; font-size: 0.94rem; line-height: 1.6; margin-bottom: 12px; }
        .project-metric {
            background: rgba(14, 12, 10, 0.95);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 10px;
            padding: 14px 18px;
            font-size: 0.9rem;
            color: #fdfbf7;
            margin-top: 14px;
        }
        
        .formula-callout {
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(140, 100, 24, 0.28) 100%);
            border: 1px solid rgba(212, 175, 55, 0.5);
            color: #fef08a;
            padding: 16px 22px;
            border-radius: 14px;
            font-family: 'Cinzel', serif;
            font-weight: 700;
            margin-bottom: 22px;
            font-size: 1.05rem;
            box-shadow: 0 8px 22px -4px rgba(0, 0, 0, 0.5), 0 0 20px rgba(212, 175, 55, 0.15);
        }
        .bullet-item { margin-bottom: 16px; border-bottom: 1px solid rgba(212, 175, 55, 0.15); padding-bottom: 14px; }
        .bullet-before { color: #fb7185; font-size: 0.92rem; margin-bottom: 4px; }
        .bullet-after { color: #34d399; font-weight: 600; font-size: 0.95rem; margin-bottom: 4px; }
        .bullet-why { color: #a89c8b; font-size: 0.85rem; font-style: italic; }

        .input-field {
            background: rgba(14, 12, 10, 0.92);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 8px;
            color: #fdfbf7;
            padding: 10px 14px;
            font-size: 0.9rem;
            width: 100%;
            outline: none;
            transition: all 0.2s ease;
        }
        .input-field:focus {
            border-color: #d4af37;
            box-shadow: 0 0 12px rgba(212, 175, 55, 0.35);
        }
        .chk-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 9px 12px;
            border-radius: 8px;
            background: rgba(18, 15, 12, 0.7);
            margin-bottom: 7px;
            font-size: 0.88rem;
            border: 1px solid rgba(212, 175, 55, 0.18);
        }

        /* Aesthetic Luxury Executive Login Styles (Exact Match to Reference) */
        .luxury-login-page {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            overflow-y: auto;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #060504 url('/assets/luxury_login_bg.webp') center center / cover no-repeat fixed;
            z-index: 99999;
            padding: 30px 16px;
            box-sizing: border-box;
        }

        .luxury-login-card {
            width: 100%;
            max-width: 440px;
            background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%);
            border: 1px solid rgba(212, 175, 55, 0.42);
            border-radius: 18px;
            padding: 38px 36px 28px 36px;
            box-shadow: 
                0 30px 80px -10px rgba(0, 0, 0, 0.98),
                0 0 45px rgba(212, 175, 55, 0.16),
                inset 0 1px 1px rgba(254, 240, 138, 0.28),
                inset 0 0 20px rgba(0, 0, 0, 0.8);
            position: relative;
            text-align: center;
            box-sizing: border-box;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            animation: cardFadeIn 0.75s cubic-bezier(0.16, 1, 0.3, 1) forwards;
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

        .brand-title {
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
            margin: 0 0 24px 0;
            font-weight: 400;
            letter-spacing: 0.01em;
            line-height: 1.4;
        }

        .login-form {
            display: flex;
            flex-direction: column;
            gap: 15px;
            text-align: left;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .form-label {
            font-size: 0.78rem;
            font-weight: 500;
            color: #c8bcab;
            letter-spacing: 0.02em;
        }

        .input-container {
            position: relative;
            display: flex;
            align-items: center;
            width: 100%;
        }

        .input-icon {
            position: absolute;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #8c7e6c;
            pointer-events: none;
            transition: color 0.2s ease;
        }
        .left-icon {
            left: 14px;
        }
        .right-icon {
            right: 12px;
            cursor: pointer;
            pointer-events: auto;
            background: none;
            border: none;
            padding: 4px;
        }
        .right-icon:hover {
            color: #e2be67;
        }

        .luxury-input {
            width: 100%;
            background: rgba(13, 11, 10, 0.9);
            border: 1px solid rgba(212, 175, 55, 0.28);
            border-radius: 8px;
            padding: 12px 14px 12px 42px;
            color: #f8fafc;
            font-size: 0.88rem;
            font-family: inherit;
            box-sizing: border-box;
            transition: all 0.25s ease;
        }
        .luxury-input::placeholder {
            color: #6e6252;
            letter-spacing: normal;
        }
        .luxury-input:focus {
            outline: none;
            border-color: #d4af37;
            background: rgba(18, 15, 13, 0.98);
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.35);
        }
        .input-container:focus-within .left-icon {
            color: #d4af37;
        }

        #loginPassword {
            padding-right: 42px;
            letter-spacing: 0.15em;
        }
        #loginPassword::placeholder {
            letter-spacing: 0.2em;
        }

        .utility-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 2px;
            margin-bottom: 6px;
            font-size: 0.76rem;
        }

        .checkbox-container {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            user-select: none;
            color: #a89b87;
        }
        .checkbox-container input[type="checkbox"] {
            accent-color: #d4af37;
            width: 14px;
            height: 14px;
            cursor: pointer;
        }

        .forgot-password-link {
            color: #caa14c;
            text-decoration: none;
            font-size: 0.76rem;
            font-weight: 500;
            transition: color 0.2s ease, text-decoration 0.2s ease;
        }
        .forgot-password-link:hover {
            color: #fef08a;
            text-decoration: underline;
        }

        .btn-luxury-login {
            width: 100%;
            height: 46px;
            background: linear-gradient(180deg, #f7dd96 0%, #caa14c 45%, #966c1b 100%);
            border: 1px solid rgba(254, 240, 138, 0.65);
            border-radius: 8px;
            color: #161005;
            font-family: 'Cinzel', serif;
            font-size: 0.94rem;
            font-weight: 700;
            letter-spacing: 0.18em;
            cursor: pointer;
            transition: all 0.25s ease;
            box-shadow: 
                0 4px 18px rgba(0, 0, 0, 0.6),
                inset 0 1px 1px rgba(255, 255, 255, 0.65),
                inset 0 -1px 2px rgba(0, 0, 0, 0.4);
            margin-top: 4px;
        }
        .btn-luxury-login:hover {
            filter: brightness(1.08);
            transform: translateY(-1px);
            box-shadow: 
                0 6px 24px rgba(212, 175, 55, 0.5),
                inset 0 1px 1px rgba(255, 255, 255, 0.85);
        }
        .btn-luxury-login:active {
            transform: translateY(1px);
            filter: brightness(0.96);
        }

        .login-error-msg {
            background: rgba(225, 29, 72, 0.12);
            border: 1px solid rgba(244, 63, 94, 0.4);
            border-radius: 6px;
            padding: 8px 12px;
            color: #fb7185;
            font-size: 0.78rem;
            text-align: left;
        }

        .forgot-alert-msg {
            background: rgba(212, 175, 55, 0.12);
            border: 1px solid rgba(212, 175, 55, 0.45);
            border-radius: 6px;
            padding: 10px 12px;
            color: #fef08a;
            font-size: 0.78rem;
            text-align: left;
            line-height: 1.4;
        }

        .login-footer {
            margin-top: 22px;
            padding-top: 14px;
            border-top: 1px solid rgba(212, 175, 55, 0.12);
            font-size: 0.68rem;
            color: #7a7062;
            letter-spacing: 0.02em;
            line-height: 1.4;
        }
        /* Top Navigation Bar in App View */
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
        .luxury-user-emblem {
            font-size: 1.6rem;
            filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.6));
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

        /* High Visibility Luxury Gold Audit Report Export Button */
        .btn-export-audit {
            background: linear-gradient(180deg, #f7dd96 0%, #caa14c 45%, #966c1b 100%) !important;
            color: #161005 !important;
            border: 1px solid rgba(254, 240, 138, 0.7) !important;
            border-radius: 10px !important;
            padding: 11px 24px !important;
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
        .btn-export-audit:hover {
            filter: brightness(1.08) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.7), 0 0 28px rgba(212, 175, 55, 0.5) !important;
        }
        .btn-luxury-signout {
            padding: 7px 16px;
            background: rgba(30, 20, 16, 0.85);
            border: 1px solid rgba(212, 175, 55, 0.35);
            border-radius: 8px;
            color: #fca5a5;
            font-family: 'Cinzel', serif;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .btn-luxury-signout:hover {
            background: rgba(225, 29, 72, 0.25);
            border-color: #f43f5e;
            color: #ffffff;
            box-shadow: 0 0 15px rgba(244, 63, 94, 0.4);
            transform: translateY(-1px);
        }
    </style>
</head>
<body>
    <div id="loginView" class="luxury-login-page">
        <div class="luxury-login-card">
            <!-- Laurel Wreath Crest -->
            <div class="login-crest-wrap">
                <img src="/assets/luxury_crest.png" alt="SparkCV Crest" class="login-crest-img" />
            </div>

            <!-- Brand Name -->
            <h1 class="brand-title">SparkCV</h1>

            <!-- Private Access Badge -->
            <div class="badge-private-access">
                <span class="badge-bracket">⟨</span> PRIVATE ACCESS <span class="badge-bracket">⟩</span>
            </div>

            <!-- Heading & Subtitle -->
            <h2 class="executive-title">Executive Login</h2>
            <p class="executive-subtitle">Enter your credentials to access the executive dashboard</p>

            <!-- Login Form -->
            <form id="luxuryLoginForm" onsubmit="event.preventDefault(); executeLogin();" class="login-form">
                <!-- Executive ID / Email Field -->
                <div class="form-group">
                    <label class="form-label" for="loginEmail">Executive ID / Email</label>
                    <div class="input-container">
                        <span class="input-icon left-icon">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                <circle cx="12" cy="7" r="4"></circle>
                            </svg>
                        </span>
                        <input type="text" id="loginEmail" class="luxury-input" placeholder="name@sparkcv.com" autocomplete="username" required />
                    </div>
                </div>

                <!-- Password Field -->
                <div class="form-group">
                    <label class="form-label" for="loginPassword">Password</label>
                    <div class="input-container">
                        <span class="input-icon left-icon">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                            </svg>
                        </span>
                        <input type="password" id="loginPassword" class="luxury-input" placeholder="••••••••••••" autocomplete="current-password" required />
                        <button type="button" class="input-icon right-icon" onclick="togglePasswordVisibility()" title="Toggle password visibility">
                            <svg id="eyeIcon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                <circle cx="12" cy="12" r="3"></circle>
                            </svg>
                        </button>
                    </div>
                </div>

                <!-- Utility Row: Remember me + Forgot password -->
                <div class="utility-row">
                    <label class="checkbox-container">
                        <input type="checkbox" id="rememberMe" checked />
                        <span class="checkbox-label">Remember me for 30 days</span>
                    </label>
                    <a href="javascript:void(0)" onclick="triggerForgotPassword(event)" class="forgot-password-link">Forgot password?</a>
                </div>

                <!-- Error Box -->
                <div id="loginError" class="login-error-msg" style="display: none;"></div>

                <!-- Forgot Password Alert Box -->
                <div id="forgotAlert" class="forgot-alert-msg" style="display: none;"></div>

                <!-- Action Button -->
                <button type="submit" class="btn-luxury-login">LOGIN</button>
            </form>

            <!-- Card Footer -->
            <div class="login-footer">
                Secured with 256-bit encryption • Restricted to authorized executives only
            </div>
        </div>
    </div>

    <div id="appView" style="display: none;">
        <div class="container">
            <div class="luxury-user-bar">
                <div class="luxury-user-left">
                    <img src="/assets/luxury_crest.png" alt="Crest" style="width: 34px; height: auto; filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.5));">
                    <div>
                        <div class="luxury-user-title">SparkCV Executive Suite</div>
                        <div class="luxury-user-meta">Candidate: <strong id="navCandidateName" style="color: #fdfbf7;"></strong> &nbsp;•&nbsp; <span id="navCandidateEmail" style="color: #c8bcab;"></span></div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div class="luxury-session-badge">
                        <span class="live-beacon-dot"></span> ACTIVE SESSION
                    </div>
                    <button class="btn-luxury-signout" onclick="signOut()" title="Sign out and return to login portal">
                        🚪 Sign Out
                    </button>
                </div>
            </div>

            <div class="header">
                <h1>
                    <img src="/assets/luxury_crest.png" alt="SparkCV Crest" style="width: 44px; height: auto; filter: drop-shadow(0 2px 8px rgba(212, 175, 55, 0.4));">
                    <span>SparkCV</span>
                </h1>
                <p>Smart Job Description Analyzer & Resume Optimization System • Enterprise Talent Intelligence</p>
            </div>

        <div class="toolbar">
            <span class="toolbar-label">⚡ Demo Presets:</span>
            <button class="btn-preset" onclick="loadPreset('moderate')">📊 Moderate Match (~55%)</button>
            <button class="btn-preset" onclick="loadPreset('strong')">🌟 Strong Match (>80%)</button>
            <button class="btn-preset" onclick="loadPreset('weak')">❌ Weak Match (<15%)</button>
            <button class="btn-preset" onclick="clearInputs()">🧹 Clear Inputs</button>

            <!-- Feature 2: Engine Selector -->
            <div style="margin-left: auto; display: flex; align-items: center; gap: 8px;">
                <span class="toolbar-label">🧠 Engine:</span>
                <select id="engineSelect" class="btn-preset" style="outline: none; cursor: pointer;">
                    <option value="tfidf">⚡ Fast TF-IDF (Scikit-Learn)</option>
                    <option value="sbert">🤖 Sentence-BERT (MiniLM-L6)</option>
                </select>
            </div>
        </div>

        <div class="grid-2">
            <div class="card">
                <h2>📋 1. Job Description (JD)</h2>
                <textarea id="jdInput" placeholder="Paste the Job Description text here..."></textarea>
            </div>
            <div class="card">
                <h2>
                    <span>📄 2. Candidate Resume</span>
                    <div>
                        <input type="file" id="fileInput" accept=".pdf,.docx,.doc,.txt" style="display:none;" onchange="handleFileUpload(event)">
                        <button class="btn-upload" onclick="document.getElementById('fileInput').click()">
                            📁 Upload Resume (PDF / Word / TXT)
                        </button>
                    </div>
                </h2>
                <div class="dropzone" id="resumeDropzone">
                    <textarea id="resumeInput" placeholder="Paste your Resume text here, or click 'Upload Resume' above to load your PDF or Word document..."></textarea>
                </div>
                <div id="uploadStatus" class="upload-status"></div>
            </div>
        </div>

        <button class="btn-analyze" onclick="runAnalysis()">🚀 Analyze Resume & Match Score</button>

        <div id="resultsContainer" style="display: none;">
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-title">Overall Match Score</div>
                    <div class="metric-val" id="metricScore" style="color: #fef08a;">--%</div>
                    <div class="metric-sub">Weighted Alignment</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">Skill Coverage</div>
                    <div class="metric-val" id="metricCoverage" style="color: #34d399;">--%</div>
                    <div class="metric-sub" id="metricCoverageSub">0 of 0 Skills</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">Semantic Overlap</div>
                    <div class="metric-val" id="metricSemantic" style="color: #e2be67;">--%</div>
                    <div class="metric-sub" id="metricEngineSub">TF-IDF Cosine Sim</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">Missing Skills Gap</div>
                    <div class="metric-val" id="metricGap" style="color: #fb7185;">--</div>
                    <div class="metric-sub">Keywords to Bridge</div>
                </div>
            </div>

            <div class="verdict-box" id="verdictBox">
                <h3 id="verdictTitle">Status</h3>
                <p id="verdictAdvice" style="margin-bottom: 12px;">Advice</p>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <span style="font-size: 0.82rem; background: rgba(212, 175, 55, 0.15); color: #fef08a; border: 1px solid rgba(212, 175, 55, 0.4); padding: 5px 12px; border-radius: 8px; font-weight: 600;">
                        💡 3 Targeted Projects in <strong>Tab 2 (Recommended Projects)</strong>
                    </span>
                    <span style="font-size: 0.82rem; background: rgba(202, 161, 76, 0.15); color: #caa14c; border: 1px solid rgba(202, 161, 76, 0.4); padding: 5px 12px; border-radius: 8px; font-weight: 600;">
                        ✍️ Live Bullet Re-writer in <strong>Tab 3 (Resume Polish)</strong>
                    </span>
                    <span style="font-size: 0.82rem; background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 5px 12px; border-radius: 8px; font-weight: 600;">
                        📋 ATS Structural Health Check in <strong>Tab 4 (Linter)</strong>
                    </span>
                </div>
            </div>

            <!-- Feature 1: Export Audit Report Bar -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin: 18px 0; background: radial-gradient(ellipse at 50% 12%, rgba(26, 22, 18, 0.96) 0%, rgba(12, 10, 9, 0.98) 100%); padding: 14px 20px; border-radius: 14px; border: 1px solid rgba(212, 175, 55, 0.35); box-shadow: 0 8px 24px rgba(0,0,0,0.6); flex-wrap: wrap; gap: 10px;">
                <div style="font-size: 0.88rem; color: #c8bcab;">
                    ⚡ <strong>Active Engine:</strong> <span id="engineUsedLabel" style="color: #fef08a; font-weight: 700;">TF-IDF Statistical</span> &nbsp;|&nbsp; 
                    📋 <strong>Structural ATS Score:</strong> <span id="linterSummaryScore" style="color: #34d399; font-weight: 700;">--/100</span>
                </div>
                <button id="btnExportReport" class="btn-export-audit" onclick="downloadExecutiveReport()">
                    📥 Export Full Executive Audit Report (.md)
                </button>
            </div>

            <!-- Tab Navigation with 4 Tabs -->
            <div class="tab-nav">
                <button class="tab-btn active" onclick="switchTab(0)">🔍 1. Skills & Keywords Breakdown</button>
                <button class="tab-btn" onclick="switchTab(1)">💡 2. Recommended Projects (Tailored Blueprints)</button>
                <button class="tab-btn" onclick="switchTab(2)">✍️ 3. Resume Polish Guide & Live Bullet Builder</button>
                <button class="tab-btn" onclick="switchTab(3)">📋 4. Resume Structural Health & ATS Linter</button>
            </div>

            <!-- Tab 1: Skills Breakdown -->
            <div class="tab-content active" id="tab0">
                <div class="grid-2">
                    <div class="card">
                        <h2>✅ Matched Skills (<span id="matchedCount">0</span>)</h2>
                        <div id="matchedBadges"></div>
                    </div>
                    <div class="card">
                        <h2>❌ Missing Skills from JD (<span id="missingCount">0</span>)</h2>
                        <div id="missingBadges"></div>
                    </div>
                </div>
                <div class="card" style="margin-top: 15px;">
                    <h2>High-Value ATS Keywords from Job Description</h2>
                    <p style="color:#a89c8b; font-size:0.85rem; margin-bottom:10px;">Salient unigrams and bigrams extracted via TF-IDF analysis:</p>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
                        <div>
                            <strong style="color:#34d399; font-size:0.9rem;">Present in Resume:</strong>
                            <div id="matchedTfidf" style="margin-top:5px; color:#fdfbf7; font-size:0.85rem;"></div>
                        </div>
                        <div>
                            <strong style="color:#fb7185; font-size:0.9rem;">Missing from Resume (Add these to bullets):</strong>
                            <div id="missingTfidf" style="margin-top:5px; color:#fdfbf7; font-size:0.85rem;"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tab 2: Recommended Projects -->
            <div class="tab-content" id="tab1">
                <div id="projectCards"></div>
            </div>

            <!-- Feature 3: Tab 3: Action Verbs & XYZ Formula + Live Bullet Builder -->
            <div class="tab-content" id="tab2">
                <div class="formula-callout">
                    Google XYZ Formula: "Accomplished [X] as measured by [Y], by doing [Z]"
                </div>

                <div class="card" style="margin-bottom: 22px; border: 1px solid rgba(212, 175, 55, 0.4);">
                    <h2>
                        <span>✍️ Interactive Live Bullet Point Re-writer</span>
                        <span style="font-size: 0.75rem; background: rgba(212, 175, 55, 0.15); color: #fef08a; padding: 3px 8px; border-radius: 6px; border: 1px solid rgba(212, 175, 55, 0.3);">Google XYZ Synthesizer</span>
                    </h2>
                    <p style="color: #a89c8b; font-size: 0.88rem; margin-bottom: 16px;">
                        Transform weak or passive resume responsibilities into high-impact, quantified Google XYZ achievements infused with your target job description keywords:
                    </p>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px;">
                        <div>
                            <label style="font-size: 0.82rem; font-weight: 700; color: #c8bcab; display: block; margin-bottom: 5px;">1. Strong Action Verb [Doing Z]:</label>
                            <select id="builderVerb" class="input-field"></select>
                        </div>
                        <div>
                            <label style="font-size: 0.82rem; font-weight: 700; color: #c8bcab; display: block; margin-bottom: 5px;">2. Target Technical Keyword to Integrate:</label>
                            <select id="builderKeyword" class="input-field"></select>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px;">
                        <div>
                            <label style="font-size: 0.82rem; font-weight: 700; color: #c8bcab; display: block; margin-bottom: 5px;">3. Measurable Metric [Measured by Y]:</label>
                            <input id="builderMetric" class="input-field" value="by 35%" placeholder="e.g. by 35% or sub-25ms response time">
                        </div>
                        <div>
                            <label style="font-size: 0.82rem; font-weight: 700; color: #c8bcab; display: block; margin-bottom: 5px;">4. Base Duty Accomplished [Accomplished X]:</label>
                            <input id="builderDuty" class="input-field" value="backend data ingestion pipelines and microservice endpoints" placeholder="e.g. backend data pipeline">
                        </div>
                    </div>
                    <button class="btn-preset" onclick="synthesizeBullets()" style="background: linear-gradient(180deg, #f7dd96 0%, #caa14c 45%, #966c1b 100%); border: 1px solid rgba(254, 240, 138, 0.65); color: #161005; width: 100%; padding: 13px; font-weight: 700; font-family: 'Cinzel', serif; letter-spacing: 0.08em; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 18px rgba(0,0,0,0.6);">
                        ⚡ Synthesize High-Impact XYZ Variations
                    </button>
                    <div id="synthesizedOutput" style="margin-top: 16px;"></div>
                </div>

                <div class="card" style="margin-bottom: 20px;">
                    <h2>🔄 Before & After Bullet Transformations</h2>
                    <div id="xyzExamples"></div>
                </div>
                <div class="card">
                    <h2>⚡ High-Impact Action Verbs by Category</h2>
                    <div id="actionVerbsGrid" style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;"></div>
                </div>
            </div>

            <!-- Feature 4: Tab 4: Structural Health & ATS Linter -->
            <div class="tab-content" id="tab3">
                <div class="metrics-grid">
                    <div class="metric-card" id="linterScoreCard">
                        <div class="metric-title">Structural ATS Score</div>
                        <div class="metric-val" id="linterScore" style="color: #34d399;">--/100</div>
                        <div class="metric-sub" id="linterVerdict">Status</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Document Word Count</div>
                        <div class="metric-val" id="linterWords" style="color: #fef08a;">0</div>
                        <div class="metric-sub" id="linterWordStatus">Words</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Contact Credentials</div>
                        <div class="metric-val" id="linterContact" style="color: #caa14c;">0 / 3</div>
                        <div class="metric-sub">Email • Phone • Links</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Core ATS Sections</div>
                        <div class="metric-val" id="linterSections" style="color: #34d399;">0 / 4</div>
                        <div class="metric-sub">Exp • Edu • Skills • Proj</div>
                    </div>
                </div>

                <div class="grid-2">
                    <div class="card">
                        <h2>📋 ATS Format Compliance Checklist</h2>
                        <div id="linterChecklist"></div>
                    </div>
                    <div class="card">
                        <h2>🚨 Corrective ATS Recommendations</h2>
                        <div id="linterRecs"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

    <script>
        let currentReportText = "";
        let currentAnalysisData = null;

        const presets = {
            moderate: { jd: `""" + SAMPLE_JD_PYTHON_DS.replace("`", "\\`") + """`, resume: `""" + SAMPLE_RESUME_MODERATE.replace("`", "\\`") + """` },
            strong: { jd: `""" + SAMPLE_JD_PYTHON_DS.replace("`", "\\`") + """`, resume: `""" + SAMPLE_RESUME_STRONG.replace("`", "\\`") + """` },
            weak: { jd: `""" + SAMPLE_JD_PYTHON_DS.replace("`", "\\`") + """`, resume: `""" + SAMPLE_RESUME_WEAK.replace("`", "\\`") + """` }
        };

        function showStatus(msg, type) {
            const st = document.getElementById('uploadStatus');
            st.className = 'upload-status ' + (type === 'success' ? 'status-success' : (type === 'loading' ? 'status-loading' : 'status-error'));
            st.textContent = msg;
            st.style.display = 'block';
        }

        // Drag and Drop
        const dropzone = document.getElementById('resumeDropzone');
        ['dragenter', 'dragover'].forEach(eventName => {
            dropzone.addEventListener(eventName, (e) => { e.preventDefault(); dropzone.classList.add('dragover'); }, false);
        });
        ['dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, (e) => { e.preventDefault(); dropzone.classList.remove('dragover'); }, false);
        });
        dropzone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files && files[0]) {
                processFile(files[0]);
            }
        });

        function handleFileUpload(e) {
            const file = e.target.files[0];
            if (!file) return;
            processFile(file);
        }

        async function processFile(file) {
            const filename = file.name;
            const ext = filename.split('.').pop().toLowerCase();
            showStatus(`⏳ Reading "${filename}"...`, 'loading');

            if (ext === 'pdf' && typeof pdfjsLib !== 'undefined') {
                try {
                    const arrayBuffer = await file.arrayBuffer();
                    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
                    let extracted = [];
                    for (let i = 1; i <= pdf.numPages; i++) {
                        const page = await pdf.getPage(i);
                        const textContent = await page.getTextContent();
                        const pageText = textContent.items.map(item => item.str).join(' ');
                        extracted.push(pageText);
                    }
                    const fullText = extracted.join('\\n').trim();
                    if (fullText.length > 20) {
                        document.getElementById('resumeInput').value = fullText;
                        const wordCount = fullText.split(/\\s+/).length;
                        showStatus(`✅ Successfully extracted "${filename}" (${wordCount} words)`, 'success');
                        return;
                    }
                } catch (pdfErr) {
                    console.warn("Client-side PDF.js fallback to backend parser:", pdfErr);
                }
            }

            try {
                const reader = new FileReader();
                reader.onload = async function(evt) {
                    const base64Data = evt.target.result.split(',')[1];
                    try {
                        const res = await fetch('/api/upload', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ filename, filedata: base64Data })
                        });
                        const data = await res.json();
                        if (data.text && data.text.trim().length > 0) {
                            document.getElementById('resumeInput').value = data.text;
                            showStatus(`✅ Successfully loaded "${filename}" (${data.word_count} words)`, 'success');
                        } else {
                            showStatus(`⚠️ Could not extract text from "${filename}". File might be empty or a scanned image.`, 'error');
                        }
                    } catch (netErr) {
                        showStatus(`❌ Error processing file: ${netErr.message}`, 'error');
                    }
                };
                reader.readAsDataURL(file);
            } catch (err) {
                showStatus(`❌ File read failed: ${err.message}`, 'error');
            }
        }

        function loadPreset(type) {
            document.getElementById('jdInput').value = presets[type].jd;
            document.getElementById('resumeInput').value = presets[type].resume;
            document.getElementById('uploadStatus').style.display = 'none';
            runAnalysis();
        }

        function clearInputs() {
            document.getElementById('jdInput').value = "";
            document.getElementById('resumeInput').value = "";
            document.getElementById('resultsContainer').style.display = 'none';
            document.getElementById('uploadStatus').style.display = 'none';
        }

        function switchTab(index) {
            const tabs = document.querySelectorAll('.tab-content');
            const btns = document.querySelectorAll('.tab-btn');
            tabs.forEach((t, i) => t.classList.toggle('active', i === index));
            btns.forEach((b, i) => b.classList.toggle('active', i === index));
        }

        function downloadExecutiveReport() {
            if (!currentReportText) {
                alert("Please run an analysis first to generate your report.");
                return;
            }
            const blob = new Blob([currentReportText], { type: 'text/markdown;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            const now = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
            a.href = url;
            a.download = `SparkCV_Talent_Alignment_Report_${now}.md`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }

        async function synthesizeBullets() {
            const raw = document.getElementById('builderDuty').value.trim();
            const verb = document.getElementById('builderVerb').value;
            const kw = document.getElementById('builderKeyword').value;
            const metric = document.getElementById('builderMetric').value.trim();

            const res = await fetch('/api/synthesize_bullet', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ raw, verb, kw, metric })
            });
            const data = await res.json();
            const out = document.getElementById('synthesizedOutput');
            out.innerHTML = data.bullets.map((b, i) => `
                <div style="background: rgba(20, 16, 13, 0.95); border: 1px solid rgba(212, 175, 55, 0.35); border-left: 4px solid #d4af37; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px; box-shadow: 0 4px 14px rgba(0,0,0,0.5);">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #fef08a; font-family: 'Cinzel', serif; text-transform: uppercase; margin-bottom: 4px;">
                        Variation ${i + 1} • ${b.title}
                    </div>
                    <div style="font-size: 0.92rem; color: #fdfbf7; line-height: 1.5;">
                        • ${b.bullet}
                    </div>
                </div>
            `).join('');
        }

        async function runAnalysis() {
            const jd = document.getElementById('jdInput').value.trim();
            const resume = document.getElementById('resumeInput').value.trim();
            const engine = document.getElementById('engineSelect').value;

            if (!jd || !resume) {
                alert("Please provide both a Job Description and a Resume (or upload a resume file).");
                return;
            }

            const res = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    jd, 
                    resume, 
                    engine,
                    candidate_name: currentUser ? currentUser.name : '',
                    candidate_email: currentUser ? currentUser.email : ''
                })
            });
            const data = await res.json();
            currentAnalysisData = data;
            currentReportText = data.report_text || "";

            document.getElementById('resultsContainer').style.display = 'block';
            document.getElementById('metricScore').textContent = data.final_score + '%';
            document.getElementById('metricScore').style.color = data.verdict_color;
            document.getElementById('metricCoverage').textContent = data.skill_coverage_pct + '%';
            document.getElementById('metricCoverageSub').textContent = `${data.matched_skills_count} of ${data.total_jd_skills_count} Core Skills`;
            document.getElementById('metricSemantic').textContent = data.cosine_sim_pct + '%';
            document.getElementById('metricEngineSub').textContent = data.engine_used || 'Cosine Similarity';
            document.getElementById('metricGap').textContent = data.missing_skills_count;

            document.getElementById('engineUsedLabel').textContent = data.engine_used || 'TF-IDF Statistical';
            const lint = data.linter || {};
            document.getElementById('linterSummaryScore').textContent = (lint.score || 0) + '/100';
            document.getElementById('linterSummaryScore').style.color = lint.color || '#10b981';

            const vb = document.getElementById('verdictBox');
            vb.style.backgroundColor = data.verdict_color;
            document.getElementById('verdictTitle').textContent = data.verdict_label;
            document.getElementById('verdictAdvice').textContent = data.verdict_advice;

            document.getElementById('matchedCount').textContent = data.matched_skills.length;
            document.getElementById('matchedBadges').innerHTML = data.matched_skills.map(s => `<span class="badge badge-match">✓ ${data.taxonomy[s]?.display || s.toUpperCase()}</span>`).join('') || '<em style="color:#94a3b8">None detected</em>';

            document.getElementById('missingCount').textContent = data.missing_skills.length;
            document.getElementById('missingBadges').innerHTML = data.missing_skills.map(s => `<span class="badge badge-miss">✗ ${data.taxonomy[s]?.display || s.toUpperCase()}</span>`).join('') || '<span style="color:#6ee7b7">All identified skills matched!</span>';

            document.getElementById('matchedTfidf').textContent = data.matched_salient_kw.map(k => `\`${k}\``).join(', ') || 'None';
            document.getElementById('missingTfidf').textContent = data.missing_salient_kw.map(k => `\`${k}\``).join(', ') || 'None';

            document.getElementById('projectCards').innerHTML = data.projects.map((p, idx) => `
                <div class="project-card">
                    <div class="project-title">${idx + 1}. ${p.title}</div>
                    <div class="project-desc">${p.desc}</div>
                    <div style="margin-bottom:8px;"><strong>Technologies:</strong> ${p.tech_stack.map(t => `<span class="badge badge-tech">${t}</span>`).join(' ')}</div>
                    <div class="project-metric"><strong>🎯 Quantified Resume Metric Example:</strong> <em>"${p.key_metric}"</em></div>
                </div>
            `).join('');

            // Populate Live Bullet Builder options
            const verbSelect = document.getElementById('builderVerb');
            const allVerbs = Object.values(data.action_verbs || {}).flat();
            verbSelect.innerHTML = allVerbs.map(v => `<option value="${v}">${v}</option>`).join('');

            const kwSelect = document.getElementById('builderKeyword');
            const missingKw = (data.missing_skills || []).map(s => data.taxonomy[s]?.display || s);
            const kwList = missingKw.length > 0 ? missingKw : ["FastAPI & PostgreSQL", "Docker & Kubernetes", "Scikit-Learn & ML", "AWS Cloud Services"];
            kwSelect.innerHTML = kwList.map(k => `<option value="${k}">${k}</option>`).join('');

            // Auto-trigger default synthesize
            synthesizeBullets();

            document.getElementById('xyzExamples').innerHTML = data.xyz_examples.map(ex => `
                <div class="bullet-item">
                    <div class="bullet-before">❌ Before: "${ex.before}"</div>
                    <div class="bullet-after">✅ After: "${ex.after}"</div>
                    <div class="bullet-why">💡 Formula: ${ex.breakdown}</div>
                </div>
            `).join('');

            document.getElementById('actionVerbsGrid').innerHTML = Object.entries(data.action_verbs).map(([cat, verbs]) => `
                <div style="margin-bottom:12px;">
                    <div style="font-weight:700; color:#d4af37; font-size:0.9rem; font-family:'Cinzel', serif; margin-bottom:6px;">${cat}</div>
                    <div>${verbs.map(v => `<span class="badge badge-verb">${v}</span>`).join(' ')}</div>
                </div>
            `).join('');

            // Populate Tab 4: Linter
            document.getElementById('linterScore').textContent = lint.score + '/100';
            document.getElementById('linterScore').style.color = lint.color;
            document.getElementById('linterVerdict').textContent = lint.verdict;

            document.getElementById('linterWords').textContent = lint.word_count;
            document.getElementById('linterWords').style.color = lint.word_color;
            document.getElementById('linterWordStatus').textContent = lint.word_status;

            const ci = lint.contact_info || {};
            const ciCount = [ci.email, ci.phone, ci.links].filter(Boolean).length;
            document.getElementById('linterContact').textContent = `${ciCount} / 3`;

            const sec = lint.sections || {};
            const secCount = [sec.experience, sec.education, sec.skills, sec.projects].filter(Boolean).length;
            document.getElementById('linterSections').textContent = `${secCount} / 4`;

            document.getElementById('linterChecklist').innerHTML = `
                <div class="chk-row"><span>Professional Email Address</span><strong style="color:${ci.email ? '#34d399' : '#fb7185'}">${ci.email ? '✓ Detected' : '✗ Missing'}</strong></div>
                <div class="chk-row"><span>Direct Phone Contact</span><strong style="color:${ci.phone ? '#34d399' : '#fb7185'}">${ci.phone ? '✓ Detected' : '✗ Missing'}</strong></div>
                <div class="chk-row"><span>Portfolio / LinkedIn Link</span><strong style="color:${ci.links ? '#34d399' : '#fb7185'}">${ci.links ? '✓ Detected' : '✗ Missing'}</strong></div>
                <div class="chk-row"><span>Experience / Work History</span><strong style="color:${sec.experience ? '#34d399' : '#fb7185'}">${sec.experience ? '✓ Detected' : '✗ Missing'}</strong></div>
                <div class="chk-row"><span>Education / Academic Background</span><strong style="color:${sec.education ? '#34d399' : '#fb7185'}">${sec.education ? '✓ Detected' : '✗ Missing'}</strong></div>
                <div class="chk-row"><span>Dedicated Technical Skills</span><strong style="color:${sec.skills ? '#34d399' : '#fb7185'}">${sec.skills ? '✓ Detected' : '✗ Missing'}</strong></div>
                <div class="chk-row"><span>Projects / Portfolio Section</span><strong style="color:${sec.projects ? '#34d399' : '#fb7185'}">${sec.projects ? '✓ Detected' : '✗ Missing'}</strong></div>
                <div class="chk-row"><span>Quantified Impact Metrics</span><strong style="color:#fef08a">${lint.quant_metric_count || 0} metrics detected</strong></div>
            `;

            const recs = lint.recommendations || [];
            if (recs.length > 0) {
                document.getElementById('linterRecs').innerHTML = recs.map((r, i) => `
                    <div style="background: rgba(244, 63, 94, 0.08); border-left: 3px solid #fb7185; border-radius: 6px; padding: 10px 14px; margin-bottom: 10px; font-size: 0.88rem; color: #f1f5f9;">
                        <strong>#${i + 1}:</strong> ${r}
                    </div>
                `).join('');
            } else {
                document.getElementById('linterRecs').innerHTML = `
                    <div style="background: rgba(16, 185, 129, 0.12); border-left: 3px solid #10b981; border-radius: 6px; padding: 14px; color: #34d399; font-size: 0.92rem;">
                        🎉 Outstanding! Your resume document passed all ATS structural, layout, and contact checks with no formatting red flags detected.
                    </div>
                `;
            }

            document.getElementById('resultsContainer').scrollIntoView({ behavior: 'smooth' });
        }

        // Authentication & Session Management
        let currentUser = null;

        function checkAuth() {
            try {
                const stored = localStorage.getItem('sparkcv_auth') || sessionStorage.getItem('sparkcv_auth');
                if (stored) {
                    currentUser = JSON.parse(stored);
                    showAppView();
                } else {
                    showLoginView();
                }
            } catch (e) {
                showLoginView();
            }
        }

        function showLoginView() {
            currentUser = null;
            document.getElementById('loginView').style.display = 'flex';
            document.getElementById('appView').style.display = 'none';
            const emailInp = document.getElementById('loginEmail');
            const pwdInp = document.getElementById('loginPassword');
            if (emailInp) emailInp.value = '';
            if (pwdInp) pwdInp.value = '';
            const errBox = document.getElementById('loginError');
            if (errBox) errBox.style.display = 'none';
            const forgotAlert = document.getElementById('forgotAlert');
            if (forgotAlert) forgotAlert.style.display = 'none';
        }

        function showAppView() {
            if (!currentUser) return;
            document.getElementById('loginView').style.display = 'none';
            document.getElementById('appView').style.display = 'block';
            document.getElementById('navCandidateName').textContent = currentUser.name || "Executive";
            document.getElementById('navCandidateEmail').textContent = currentUser.email || "";
        }

        function togglePasswordVisibility() {
            const pwd = document.getElementById('loginPassword');
            const eye = document.getElementById('eyeIcon');
            if (pwd.type === 'password') {
                pwd.type = 'text';
                eye.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line>';
            } else {
                pwd.type = 'password';
                eye.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>';
            }
        }

        function triggerForgotPassword(e) {
            if (e) e.preventDefault();
            const alertBox = document.getElementById('forgotAlert');
            const errBox = document.getElementById('loginError');
            if (errBox) errBox.style.display = 'none';
            alertBox.innerHTML = '🔒 <strong>Security Protocol:</strong> Password recovery instructions have been dispatched to your corporate security administrator.';
            alertBox.style.display = 'block';
        }

        function executeLogin() {
            const emailInput = document.getElementById('loginEmail').value.trim();
            const passwordInput = document.getElementById('loginPassword').value.trim();
            const rememberMe = document.getElementById('rememberMe').checked;
            const errBox = document.getElementById('loginError');
            const forgotAlert = document.getElementById('forgotAlert');
            if (forgotAlert) forgotAlert.style.display = 'none';

            if (!emailInput) {
                errBox.textContent = "Please enter your Executive ID or Email.";
                errBox.style.display = 'block';
                return;
            }
            if (!passwordInput) {
                errBox.textContent = "Please enter your Password.";
                errBox.style.display = 'block';
                return;
            }

            // Derive polished name from email/ID
            let displayName = "Executive";
            if (emailInput.includes('@')) {
                const prefix = emailInput.split('@')[0];
                displayName = prefix.split(/[._-]/).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
            } else {
                displayName = emailInput.charAt(0).toUpperCase() + emailInput.slice(1);
            }

            errBox.style.display = 'none';
            currentUser = { name: displayName, email: emailInput };
            if (rememberMe) {
                localStorage.setItem('sparkcv_auth', JSON.stringify(currentUser));
            } else {
                sessionStorage.setItem('sparkcv_auth', JSON.stringify(currentUser));
            }
            showAppView();
        }

        function signOut() {
            localStorage.removeItem('sparkcv_auth');
            sessionStorage.removeItem('sparkcv_auth');
            currentUser = null;
            showLoginView();
        }

        window.addEventListener('DOMContentLoaded', checkAuth);
    </script>
</body>
</html>
"""

class StandaloneHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path.startswith("/assets/"):
            import os
            clean_name = os.path.basename(self.path.split("?")[0])
            asset_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", clean_name)
            if os.path.exists(asset_file):
                mime = "image/webp" if clean_name.endswith(".webp") else ("image/png" if clean_name.endswith(".png") else ("image/jpeg" if (clean_name.endswith(".jpg") or clean_name.endswith(".jpeg")) else "application/octet-stream"))
                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.send_header("Cache-Control", "public, max-age=86400")
                self.end_headers()
                with open(asset_file, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/upload":
            # File upload handler for PDF, DOCX, DOC, TXT
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            filename = data.get("filename", "")
            filedata = data.get("filedata", "")

            try:
                raw_bytes = base64.b64decode(filedata)
                text = extract_text_from_file_bytes(filename, raw_bytes)
                word_count = len(text.split()) if text else 0
                resp = {"success": True, "filename": filename, "text": text, "word_count": word_count}
            except Exception as e:
                resp = {"success": False, "filename": filename, "text": "", "error": str(e)}

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))

        elif self.path == "/api/analyze":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            jd_text = data.get("jd", "")
            resume_text = data.get("resume", "")
            engine = data.get("engine", "tfidf")
            candidate_name = data.get("candidate_name", "")
            candidate_email = data.get("candidate_email", "")

            results = calculate_match_metrics(resume_text, jd_text, engine=engine)
            projects = generate_project_recommendations(results["missing_skills"], jd_text)
            linter = lint_resume_structure(resume_text)
            report_text = generate_executive_audit_report(
                results, jd_text, resume_text, linter, projects,
                candidate_name=candidate_name, candidate_email=candidate_email
            )

            payload = {
                **results,
                "projects": projects,
                "linter": linter,
                "report_text": report_text,
                "action_verbs": ACTION_VERBS,
                "xyz_examples": XYZ_EXAMPLES,
                "taxonomy": TECHNICAL_SKILLS_TAXONOMY
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))

        elif self.path == "/api/synthesize_bullet":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            raw = data.get("raw", "")
            verb = data.get("verb", "")
            kw = data.get("kw", "")
            metric = data.get("metric", "")

            bullets = generate_google_xyz_bullets(raw, verb, kw, metric)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"bullets": bullets}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

def run_server():
    server_address = (HOST, PORT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(server_address, StandaloneHandler) as httpd:
        print("========================================================")
        print("SparkCV: Executive Resume Analyzer & ATS Optimizer")
        print("========================================================")
        print(f"Web application is LIVE at: http://localhost:{PORT}")
        print(f"Network access enabled on: http://0.0.0.0:{PORT}")
        print(f"Opening browser automatically...")
        if os.environ.get("NO_BROWSER") != "1":
            try:
                webbrowser.open(f"http://localhost:{PORT}")
            except Exception:
                pass
        print("Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run_server()
