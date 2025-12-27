<h1><b>🧠 AI-Powered Resume Analyzer</b></h1>

An ATS-style resume evaluation system that analyzes PDF resumes against a target job role and provides deterministic ATS scores along with AI-generated, detailed feedback using Google Gemini AI.

Built with FastAPI (backend) and Streamlit (frontend).

<h1><b>🚀 Features</b></h1>

📄 Upload resume in PDF format

🎯 Select target job role (e.g. Software Engineer)

📊 Deterministic ATS Compatibility Score (no randomness)

✅ Detailed Strengths

⚠️ Actionable Weaknesses

❌ Role-specific Missing Skills

💡 Practical Improvement Suggestions

🤖 AI feedback powered by Google Gemini

🎨 Modern, interactive Streamlit UI with hover effects

<h1><b>🏗️ Tech Stack</b></h1>
Frontend

Streamlit

Custom HTML + CSS (animations, hover effects)

Backend

FastAPI

Google Gemini API

PyPDF

Python 3.10+

📂 Project Structure
```text
AI-Powered-Resume-Analyzer/
│
├── backend/
│   ├── main.py          # FastAPI entry point
│   ├── analyzer.py      # Resume analysis logic
│
├── frontend/
│   ├── app.py           # Streamlit UI
│   └── assets/
│       └── GDG-Logo.png
│
├── .env                 # Gemini API key
├── requirements.txt
└── README.md
```
<h1><b>⚙️ Setup Instructions</b></h1>

1️⃣ Clone the repository
```bash
git clone https://github.com/prathmeshchorghade-mits/AI-Powered-Resume-Analyzer.git
cd AI-Powered-Resume-Analyzer
```
2️⃣ Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows
```
3️⃣ Install dependencies
``bash
pip install -r requirements.txt
``
4️⃣ Configure Gemini API Key

Create a .env file in the root directory:
```
GEMINI_API_KEY=your_google_gemini_api_key_here
```

<h1><b>▶️ Running the Application</b></h1>

Start Backend (FastAPI)
```bash
uvicorn backend.main:app --reload
```

Backend runs at: http://127.0.0.1:8000

API docs: http://127.0.0.1:8000/docs

Start Frontend (Streamlit)

Open a new terminal:
```bash
cd frontend
streamlit run app.py
```

Frontend runs at: http://localhost:8501

<h1><b>🧪 How ATS Score Works</b></h1>

The ATS score is deterministic, not AI-generated.

It is calculated by:

Matching predefined core skills for the selected role

Computing a percentage based on skill presence

Clamped between 5 and 95 to avoid extremes

Example for Software Engineer:
```
python, java, c++, javascript,
data structures, algorithms,
git, sql, linux, oop
```
<h1><b>🤖 AI Analysis Details</b></h1>

Gemini AI is used only for qualitative feedback:

Strengths

Weaknesses

Missing Skills

Suggestions

Strict rules enforced:

JSON-only output

Minimum length per bullet

Resume-aware feedback

Fallback logic if AI fails

<h1><b>🛡️ Error Handling</b></h1>

Handles empty resumes

Handles scanned PDFs (fallback)

Safe fallback if Gemini API fails

No frontend crashes on backend errors

<h1><b>📸 UI Highlights</b></h1>

Gradient animated hero section

Hover-responsive cards

Clean ATS-style report layout

Dark modern theme

<h1><b>🧩 Future Improvements</b></h1>

Resume vs Job Description comparison

Section-wise scoring (Skills / Projects / Experience)

Keyword highlighting

Downloadable feedback PDF

Multiple role support

Authentication & user history

<h1><b>👥 Team</b></h1>

<b>Developed by Team DeadLock</b>

<h1><b>📜 License</b></h1>

This project is for educational and demonstration purposes.
You are free to fork, modify, and improve it.
