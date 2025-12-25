from fastapi import FastAPI, UploadFile, Form
from analyzer import analyze_resume
from utils import extract_text
import json

app = FastAPI(title="AI Resume Analyzer API")

@app.post("/analyze")
async def analyze(file: UploadFile, role: str = Form(...)):
    resume_text = extract_text(file.file)
    raw_output = analyze_resume(resume_text, role)

    try:
        return json.loads(raw_output)
    except Exception:
        return {
            "error": "Failed to parse AI response",
            "raw_output": raw_output
        }
