import streamlit as st
<<<<<<< HEAD

from database import init_db, save_result
from parser import extract_text, parse_resume
=======
import pdfplumber
from database import init_db, save_result, fetch_all, role_skills
>>>>>>> f1d7d26 (WIP: docker and app updates)

# ── INIT DB ─────────────────────────────
init_db()

# ── HELPER FUNCTIONS ────────────────────
def extract_text(uploaded_file):
    text = ""
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    else:
        text = str(uploaded_file.read(), 'utf-8')
    return text.lower()


def extract_info(text):
    # Very basic extraction (you can improve later)
    name = "Unknown"
    email = "Not found"
    phone = "Not found"

    words = text.split()
    skills = [skill for role in role_skills.values() for skill in role if skill in text]

    return name, email, phone, list(set(skills))


def calculate_scores(skills):
    scores = {}
    for role, skill_list in role_skills.items():
        match = len(set(skills) & set(skill_list))
        scores[role] = round((match / len(skill_list)) * 100, 2)
    return scores


# ── UI ──────────────────────────────────
st.set_page_config(page_title="Resume Analyzer", layout="centered")

st.sidebar.title("Smart Resume Analyzer")
page = st.sidebar.selectbox("Select Option", ["Upload Resume", "View Database"])

# ── PAGE 1: Upload ─────────────────────
if page == "Upload Resume":
    st.title("Upload Resume")

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])

    if uploaded_file:
        text = extract_text(uploaded_file)

        name, email, phone, skills = extract_info(text)
        scores = calculate_scores(skills)
        best_role = max(scores, key=scores.get)

        st.subheader("Extracted Skills")
        st.write(skills)

        st.subheader("Scores")
        st.write(scores)

        st.success(f"Best Role: {best_role}")

        if st.button("Save to Database"):
            save_result(name, email, phone, skills, scores, best_role)
            st.success("Saved successfully!")

# ── PAGE 2: View DB ─────────────────────
elif page == "View Database":
    st.title("Stored Resumes")

    data = fetch_all()

    if data:
        st.write(data)
    else:
        st.info("No records found.")