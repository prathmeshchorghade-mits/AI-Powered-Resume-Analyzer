import streamlit as st
import requests
from pypdf import PdfReader
from pdf2image import convert_from_bytes
import pytesseract
from fpdf import FPDF
from PIL import Image
import io
import os
from pathlib import Path
import base64
import streamlit.components.v1 as components


# ---------------- CONFIG ----------------
BACKEND_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.card {
    background: #111827;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 20px;
}
.section-title {
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 10px;
}
.footer {
    text-align: center;
    margin-top: 40px;
    font-size: 0.85rem;
    color: #9ca3af;
}
ul {
    padding-left: 20px;
}
li {
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    if len(text.strip()) > 100:
        return text.strip()

    images = convert_from_bytes(file.getvalue())
    ocr_text = ""
    for img in images:
        ocr_text += pytesseract.image_to_string(img)

    return ocr_text.strip()

def render_list(items):
    st.markdown("<ul>", unsafe_allow_html=True)
    for item in items:
        st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)

def generate_pdf_report(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "AI-Powered Resume Analysis Report", ln=True)
    pdf.ln(5)

    pdf.cell(0, 10, f"ATS Score: {data['ats_score']}%", ln=True)
    pdf.ln(5)

    for section in ["strengths", "weaknesses", "missing_skills", "suggestions"]:
        pdf.cell(0, 10, section.replace("_", " ").title(), ln=True)
        for item in data[section]:
            pdf.multi_cell(0, 8, f"- {item}")
        pdf.ln(3)

    return pdf.output(dest="S").encode("latin-1")

# ---------------- HEADER ----------------
BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "GDG-Logo.png"

def load_logo_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

if LOGO_PATH.exists():
    logo_base64 = load_logo_base64(LOGO_PATH)

    components.html(
        f"""
        <style>
        body {{
            margin: 0;
            padding: 0;
        }}
        .gdg-logo {{
            position: fixed;
            top: 0px;
            left: 16px;
            z-index: 10000;
        }}
        .gdg-logo img {{
            width: 110px;
            background: white;
            padding: 6px;
            border-radius: 10px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.45);
        }}
        </style>

        <div class="gdg-logo">
            <img src="data:image/png;base64,{logo_base64}" />
        </div>
        """,
        height=150,
    )
else:
    st.warning("Logo not found")

st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)

st.markdown("## AI-Powered Resume Analyzer")
st.caption("ATS-style evaluation using Google Gemini AI")
st.caption("Built by Team **DeadLock**")


# ---------------- INPUT CARD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

job_role = st.selectbox(
    "Select Target Job Role",
    [
        "Software Engineer",
        "Data Scientist",
        "Machine Learning Engineer",
        "Web Developer",
        "Frontend Engineer",
        "Backend Engineer",
        "DevOps Engineer"
    ]
)

analyze = st.button("🔍 Analyze Resume")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ANALYSIS ----------------
if analyze:
    if not uploaded_file:
        st.error("Upload a resume first.")
    else:
        with st.spinner("Analyzing with Gemini AI..."):
            resume_text = extract_text_from_pdf(uploaded_file)

            payload = {
                "resume_text": resume_text,
                "job_description": job_role
            }

            response = requests.post(BACKEND_URL, json=payload)

            if response.status_code != 200:
                st.error(response.json().get("detail", "Analysis failed"))
            else:
                data = response.json()

                # ATS SCORE
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">📊 ATS Compatibility Score</div>', unsafe_allow_html=True)
                st.progress(data["ats_score"] / 100)
                st.markdown(f"**Score:** {data['ats_score']}%")
                st.markdown('</div>', unsafe_allow_html=True)

                # RESULTS
                sections = [
                    ("✅ Strengths", "strengths"),
                    ("⚠️ Weaknesses", "weaknesses"),
                    ("❌ Missing Skills", "missing_skills"),
                    ("📌 Suggestions", "suggestions")
                ]

                for title, key in sections:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
                    render_list(data[key])
                    st.markdown('</div>', unsafe_allow_html=True)

                # DOWNLOAD REPORT
                pdf_bytes = generate_pdf_report(data)
                st.download_button(
                    label="📥 Download Analysis Report (PDF)",
                    data=pdf_bytes,
                    file_name="resume_analysis_report.pdf",
                    mime="application/pdf"
                )

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    © 2025 · AI-Powered Resume Analyzer · FastAPI · Streamlit · Google Gemini
</div>
""", unsafe_allow_html=True)
