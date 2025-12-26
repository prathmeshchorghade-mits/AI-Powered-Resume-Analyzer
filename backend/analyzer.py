import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_resume(resume_text: str, job_desc: str) -> str:
    prompt = f"""
You are an ATS engine.

RULES:
- Return ONLY valid JSON
- Do NOT use markdown
- Do NOT add explanations
- Do NOT add text outside JSON
- Use double quotes only

JSON SCHEMA:
{{
  "match_percentage": number,
  "strengths": [string],
  "weaknesses": [string],
  "missing_skills": [string],
  "suggestions": [string]
}}

Job Description:
{job_desc}

Resume:
{resume_text}
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )

    return response.text.strip()
