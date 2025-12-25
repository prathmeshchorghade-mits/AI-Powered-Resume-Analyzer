import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="AI Resume Analyzer")
st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
role = st.selectbox(
    "Select Target Role",
    ["Software Developer", "Data Analyst", "ML Engineer"]
)

if uploaded_file and st.button("Analyze Resume"):
    with st.spinner("Analyzing with AI..."):
        response = requests.post(
            BACKEND_URL,
            files={"file": uploaded_file},
            data={"role": role}
        )

        data = response.json()

        if "error" in data:
            st.error(data["error"])
            st.code(data.get("raw_output", ""))
        else:
            st.metric("ATS-Inspired Score", data["ats_score"])

            st.subheader("Strengths")
            st.write(data["strengths"])

            st.subheader("Weaknesses")
            st.write(data["weaknesses"])

            st.subheader("Missing Skills")
            st.write(data["missing_skills"])

            st.subheader("Improvement Suggestions")
            st.write(data["improvement_suggestions"])
