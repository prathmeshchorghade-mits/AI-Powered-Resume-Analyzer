import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def analyze_resume(resume_text: str, role: str):
    prompt = f"""
You are an experienced technical recruiter.

Evaluate the resume below for the role of: {role}

Return STRICT JSON ONLY in this format:
{{
  "ats_score": 0-100,
  "strengths": [],
  "weaknesses": [],
  "missing_skills": [],
  "improvement_suggestions": []
}}

Resume:
{resume_text}
"""
    response = model.generate_content(prompt)
    return response.text
