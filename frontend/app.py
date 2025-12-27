import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>

/* Remove Streamlit padding */
.block-container {
    padding-top: 2rem;
}

/* -------- HERO BOX -------- */
.hero-box {
    background: linear-gradient(
        270deg,
        #6d83f2,
        #8a63d2,
        #4f46e5,
        #9333ea
    );
    background-size: 600% 600%;
    animation: gradientFlow 10s ease infinite;

    padding: 60px;
    border-radius: 28px;
    text-align: center;
    color: white;

    box-shadow:
        0 30px 70px rgba(109,131,242,0.45),
        inset 0 0 45px rgba(255,255,255,0.08);

    margin-bottom: 40px;
    transition: transform 0.3s ease;
}

.hero-box:hover {
    transform: translateY(-6px);
}

.hero-box h1 {
    font-size: 3rem;
    margin-bottom: 12px;
}

.hero-box .subtitle {
    font-size: 1.15rem;
    opacity: 0.9;
}

.hero-box .author {
    margin-top: 14px;
    font-size: 0.95rem;
    opacity: 0.85;
}

/* -------- ANIMATION -------- */
@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* -------- CARDS -------- */
.card {
    background: #111827;
    border-radius: 18px;
    padding: 26px;
    color: white;
    transition: all 0.35s ease;
    border: 1px solid rgba(255,255,255,0.05);
}

.card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    border-color: rgba(139,92,246,0.5);
}

.card h4 {
    margin-bottom: 10px;
}

/* -------- SECTION TITLES -------- */
.section-title {
    font-size: 1.6rem;
    margin-bottom: 20px;
}

/* -------- BUTTON -------- */
.stButton>button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 12px;
    padding: 0.6em 1.6em;
    border: none;
    font-weight: 600;
}

.stButton>button:hover {
    transform: scale(1.03);
    box-shadow: 0 10px 30px rgba(99,102,241,0.4);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero-box">
    <h1>AI Resume Analyzer</h1>
    <p class="subtitle">
        Upload a PDF resume and get ATS-style feedback in seconds
    </p>
    <p class="author">
        Developed by <b>Team DeadLock</b>
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- MAIN LAYOUT ----------------
left, right = st.columns([2.2, 1])

with left:
    st.markdown("<div class='section-title'>Analyze your resume</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    job_role = st.selectbox(
        "Target role",
        [
            "Software Engineer"
        ]
    )

    analyze_btn = st.button("🔍 Analyze Resume")

with right:
    st.markdown("""
    <div class="card">
        <h4>Quick tips</h4>
        <ul>
            <li>Use clear section headings</li>
            <li>Add numbers to achievements</li>
            <li>List tools & tech explicitly</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ---------------- WHY CHOOSE US ----------------
st.markdown("<div class='section-title'>Why choose us</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
        <h4>⚡ Lightning Fast</h4>
        <p>Optimized for speed and clarity</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <h4>🔒 Secure & Private</h4>
        <p>Your resume is never stored</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
        <h4>🎯 Actionable Output</h4>
        <p>Clear strengths, gaps, and fixes</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- ANALYZE ACTION ----------------
if analyze_btn:
    if not uploaded_file:
        st.error("Please upload a PDF resume.")
    else:
        with st.spinner("Analyzing resume..."):
            try:
                BACKEND_URL = "https://ai-powered-resume-analyzer-3oqf.onrender.com"

                response = requests.post(
                f"{BACKEND_URL}/analyze",
                files={"resume": uploaded_file},
                data={"job_role": job_role},
                timeout=60        
                )


                if response.status_code != 200:
                    st.error("Backend error. Check server logs.")
                else:
                    data = response.json()

                    st.markdown("## 📊 ATS Compatibility Score")
                    score = data.get("ats_score", 0)
                    st.progress(score / 100)
                    st.metric("Score", f"{score} / 100")

                    st.markdown("## ✅ Strengths")
                    for s in data.get("strengths", []):
                        st.write(f"• {s}")

                    st.markdown("## ⚠️ Weaknesses")
                    for w in data.get("weaknesses", []):
                        st.write(f"• {w}")

                    st.markdown("## ❌ Missing Skills")
                    for m in data.get("missing_skills", []):
                        st.write(f"• {m}")

                    st.markdown("## 💡 Suggestions")
                    for sug in data.get("suggestions", []):
                        st.write(f"• {sug}")

            except Exception as e:
                st.error(f"Error connecting to backend: {e}")
