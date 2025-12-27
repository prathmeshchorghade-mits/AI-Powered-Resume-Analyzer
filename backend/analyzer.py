import os
import json
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader
from io import BytesIO

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

CORE_SKILLS = {
    "Software Engineer": [
        "python", "java", "c++", "javascript",
        "data structures", "algorithms",
        "git", "sql", "linux", "oop"
    ]
}


# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    text = []
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text.append(t)
    return "\n".join(text).strip()


# ---------------- DETERMINISTIC ATS SCORE ----------------
def deterministic_ats_score(resume_text: str, role: str) -> int:
    skills = CORE_SKILLS.get(role, [])
    resume_lower = resume_text.lower()

    matched = sum(1 for s in skills if s in resume_lower)
    score = int((matched / len(skills)) * 100)

    return min(max(score, 5), 95)


# ---------------- GEMINI ANALYSIS ----------------
def analyze_with_gemini(resume_text: str, role: str):
    if not client:
        return detailed_fallback(role)

    prompt = f"""
You are an ATS resume reviewer.

STRICT RULES:
- Return ONLY valid JSON
- NO markdown
- NO explanations
- Each bullet must be at least 15 words
- Be specific and resume-aware
- Do NOT repeat generic phrases

JSON SCHEMA:
{{
  "strengths": [string, string, string],
  "weaknesses": [string, string, string],
  "missing_skills": [string, string, string],
  "suggestions": [string, string, string]
}}

Target Role: {role}

Resume Content:
{resume_text}
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt
        )

        data = json.loads(response.text)

        # Safety check to avoid shallow bullets
        for key in data:
            if not isinstance(data[key], list) or len(data[key]) < 2:
                raise ValueError("Shallow AI response")

        return data

    except Exception:
        return detailed_fallback(role)


# ---------------- FALLBACK (DETAILED, NOT GENERIC) ----------------
def detailed_fallback(role: str):
    return {
        "strengths": [
            "The resume follows a recognizable academic structure with clear separation between education, skills, and extracurricular activities.",
            "The candidate demonstrates early exposure to computer science concepts such as programming and problem solving.",
            "Inclusion of certifications and coursework indicates willingness to learn beyond formal curriculum."
        ],
        "weaknesses": [
            "The resume lacks quantified achievements, making it difficult to assess the real impact of listed activities.",
            "Technical skills are listed without supporting project descriptions or real-world application context.",
            "The document structure could be improved by prioritizing projects and skills over general information."
        ],
        "missing_skills": CORE_SKILLS.get(role, []),
        "suggestions": [
            "Add 2–3 technical projects with clear problem statements, technologies used, and measurable outcomes.",
            "Quantify achievements wherever possible, such as performance improvements or completed milestones.",
            "Reorganize the resume to highlight technical skills and projects at the top for ATS optimization."
        ]
    }


# ---------------- MAIN ENTRY ----------------
def analyze_resume(pdf_bytes: bytes, role: str):
    resume_text = extract_text_from_pdf(pdf_bytes)

    ats_score = deterministic_ats_score(resume_text, role)
    ai_feedback = analyze_with_gemini(resume_text, role)

    return {
        "ats_score": ats_score,
        "strengths": ai_feedback["strengths"],
        "weaknesses": ai_feedback["weaknesses"],
        "missing_skills": ai_feedback["missing_skills"],
        "suggestions": ai_feedback["suggestions"]
    }
