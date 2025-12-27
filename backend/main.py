from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from analyzer import analyze_resume

app = FastAPI(title="AI Resume Analyzer")

@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_role: str = Form(...)
):
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    pdf_bytes = await resume.read()

    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Uploaded PDF is empty")

    return analyze_resume(pdf_bytes=pdf_bytes, role=job_role)

