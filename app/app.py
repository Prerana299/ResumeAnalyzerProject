import streamlit as st
import pdfplumber

from database import init_db, save_result, fetch_all, role_skills

init_db()

def extract_text(uploaded_file):
    text = ""
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    else:
        text = uploaded_file.read().decode("utf-8", errors="ignore")
    return text.lower()


def extract_info(text):
    skills = [skill for role in role_skills.values() for skill in role if skill in text]
    return "Unknown", "Not found", "Not found", list(set(skills))


def calculate_scores(skills):
    scores = {}
    for role, skill_list in role_skills.items():
        match = len(set(skills) & set(skill_list))
        scores[role] = round((match / len(skill_list)) * 100, 2)
    return scores


st.set_page_config(page_title="Resume Analyzer")

st.sidebar.title("Smart Resume Analyzer")
page = st.sidebar.selectbox("Select Option", ["Upload Resume", "View Database"])

if page == "Upload Resume":
    st.title("Upload Resume")
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])

    if uploaded_file:
        text = extract_text(uploaded_file)
        name, email, phone, skills = extract_info(text)
        scores = calculate_scores(skills)
        best_role = max(scores, key=scores.get)

        st.write(skills)
        st.write(scores)
        st.success(best_role)

        if st.button("Save"):
            save_result(name, email, phone, skills, scores, best_role)
            st.success("Saved")

else:
    st.title("Database")
    st.write(fetch_all())
