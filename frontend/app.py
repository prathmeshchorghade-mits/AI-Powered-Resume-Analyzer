import streamlit as st
import requests
from pypdf import PdfReader
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import io

# ---------- CONFIG ----------
BACKEND_URL = "http://127.0.0.1:8000/analyze"

JOB_ROLES = {
    "Software Engineer": """
Python, Data Structures, Algorithms, OOP, Git, REST APIs.
""",
    "Data Scientist": """
Python, Pandas, NumPy, Machine Learning, Statistics, SQL.
""",
    "Machine Learning Engineer": """
Python, ML, Deep Learning, TensorFlow/PyTorch, Model Deployment.
""",
    "Frontend Developer": """
HTML, CSS, JavaScript, React, UI/UX principles.
"""
}

# ---------- UTILS ----------
def extract_text_from_pdf(file) -> str:
    # First attempt: normal text extraction
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    # If text is found, return it
    if len(text.strip()) > 100:
        return text.strip()

    # Fallback: OCR (for scanned/image PDFs)
    images = convert_from_bytes(file.getvalue())
    ocr_text = ""

    for img in images:
        ocr_text += pytesseract.image_to_string(img)

    return ocr_text.strip()

def render_points(points):
    for p in points:
        st.markdown(f"- {p}")

# ---------- UI ----------
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.title("📄 AI-Powered Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF only)",
    type=["pdf"]
)

job_role = st.selectbox(
    "Select Job Role",
    options=list(JOB_ROLES.keys())
)

analyze_btn = st.button("Analyze Resume")

# ---------- ACTION ----------
if analyze_btn:
    if not uploaded_file:
        st.error("Please upload a resume PDF.")
        st.stop()

    with st.spinner("Reading resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    if len(resume_text) < 100:
        st.error("Could not extract text from PDF.")
        st.stop()

    payload = {
        "resume_text": resume_text,
        "job_description": JOB_ROLES[job_role]
    }

    with st.spinner("Analyzing with Gemini..."):
        response = requests.post(BACKEND_URL, json=payload, timeout=90)

    if response.status_code != 200:
        st.error(response.text)
        st.stop()

    result = response.json()

    # ---------- RESULTS ----------
    st.success("Analysis Complete")

    score = int(result["match_percentage"])

    st.subheader("📊 ATS Match Score")

    st.progress(score / 100)

    if score >= 75:
        st.success(f"Excellent match: {score}%")
    elif score >= 50:
        st.warning(f"Moderate match: {score}%")
    else:
        st.error(f"Low match: {score}%")

    st.caption(
        "This tool evaluates resume compatibility using Google Gemini AI "
        "based on ATS-style keyword and skill matching."
    )

    st.subheader("✅ Strengths")
    render_points(result["strengths"])

    st.subheader("⚠️ Weaknesses")
    render_points(result["weaknesses"])

    st.subheader("❌ Missing Skills")
    render_points(result["missing_skills"])

    st.subheader("📌 Suggestions")
    render_points(result["suggestions"])

