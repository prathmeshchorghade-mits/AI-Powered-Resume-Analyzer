<h1><b>AI Resume Analyzer</b></h1>

FastAPI + Streamlit | Powered by Gemini API

<h1><b>📌 Overview</b></h1>

AI Resume Analyzer is a web-based application that provides role-specific, actionable feedback on resumes using large language models. Unlike traditional keyword-based tools, this system evaluates resumes semantically, focusing on clarity, relevance, and skill alignment.

The project is built with a decoupled architecture:

A FastAPI backend handles resume processing and AI analysis

A Streamlit frontend provides an intuitive web interface for users

This design ensures scalability, maintainability, and future extensibility.

<h1><b>🚀 Features</b></h1>

Upload resumes in PDF format

Select a target job role (Software Developer, Data Analyst, ML Engineer)

Receive:

ATS-inspired resume score (heuristic-based)

Strengths and weaknesses

Missing skills for the selected role

Actionable improvement suggestions

Fully web-accessible UI for remote evaluation

<h1><b>🧠 AI & Technology Stack</b></h1>
Backend

FastAPI – REST API for resume analysis

Gemini API – Semantic resume evaluation and feedback generation

pdfplumber – Resume text extraction

Frontend

Streamlit – Interactive web interface

requests – Communication with backend API

Architecture
Streamlit (Frontend)
        ↓
FastAPI (Backend)
        ↓
Gemini API (AI Analysis)

<h1><b>⚠️ Disclaimer</b></h1>

This tool does not claim to replicate proprietary Applicant Tracking Systems (ATS).
The scoring mechanism is ATS-inspired, based on common recruiter heuristics and semantic analysis, and is intended as a decision-support tool, not a hiring authority.

<h1><b>🛠️ How to Run Locally</b></h1>
Backend

```bash cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend

```bash cd frontend
pip install -r requirements.txt
streamlit run app.py
```


Make sure to set your GEMINI_API_KEY as an environment variable.

<h1><b>🎯 Use Cases</b></h1>

Students preparing resumes for internships and placements

Career counselors and mentors

Hackathon and academic demonstrations of applied AI

Prototype for future HR-tech platforms

<h1><b>🔮 Future Enhancements</b></h1>

Support for additional job roles

Resume comparison (before vs after improvement)

Deployment of backend as a cloud microservice

Integration with mobile or enterprise applications

<h1><b>📄 License</b></h1>
  
This project is developed for educational and hackathon purposes.
