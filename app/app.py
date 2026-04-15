"""
Smart Resume Analyzer — Streamlit entry point.
Run: streamlit run app/app.py
"""

import streamlit as st
from parser import extract_text, parse_resume
from database import init_db, save_result

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📄",
    layout="centered",
)

# ── Init DB on startup ────────────────────────────────────────────────────────
init_db()

# ── UI ────────────────────────────────────────────────────────────────────────
st.title("Smart Resume Analyzer")
st.caption("Upload a resume to extract skills, score it, and store the results.")

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("Parsing resume…"):
        raw_text = extract_text(uploaded_file)
        result = parse_resume(raw_text)

    st.success("Analysis complete!")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Extracted Info")
        st.json(result)
    with col2:
        st.subheader("Match Score")
        st.metric(label="Skill Match", value=f"{result.get('score', 0)}%")

    save_result(result)
    st.info("Results saved to database.")
