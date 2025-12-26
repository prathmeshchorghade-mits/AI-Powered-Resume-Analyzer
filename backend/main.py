import json
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.analyzer import analyze_resume

app = FastAPI()

class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str

def extract_json(text: str) -> dict:
    """
    Extract the first valid JSON object from model output.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to extract JSON substring
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())

    raise ValueError("No valid JSON found")

@app.post("/analyze")
def analyze(data: AnalyzeRequest):
    raw = analyze_resume(data.resume_text, data.job_description)

    try:
        return extract_json(raw)
    except Exception:
        # ONE retry with correction instruction
        retry_prompt = (
            raw
            + "\n\nFIX THE ABOVE AND RETURN ONLY VALID JSON."
        )

        corrected = analyze_resume(
            data.resume_text,
            data.job_description
        )

        try:
            return extract_json(corrected)
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Model failed to return valid JSON after retry"
            )
