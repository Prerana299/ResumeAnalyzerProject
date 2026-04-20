import streamlit as st
import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# ------------------ DATABASE SETUP ------------------
conn = sqlite3.connect("resumes.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    skills TEXT,
    data_engineer_score INTEGER,
    software_developer_score INTEGER,
    data_scientist_score INTEGER,
    machine_engineer_score INTEGER,
    best_role TEXT
)""")
conn.commit()


# ------------------ DUMMY FUNCTIONS ------------------
def extract_info(text):
    return "Name", "email@example.com", "1234567890", ["Python", "SQL"]


def calculate_scores(skills):
    return {
        "Data Engineer": 70,
        "Software Developer": 80,
        "Data Scientist": 60,
        "Machine Engineer": 75,
    }


role_skills = {
    "Data Engineer": [],
    "Software Developer": [],
    "Data Scientist": [],
    "Machine Engineer": [],
}

# ------------------ UI ------------------
st.sidebar.title("Smart Resume Analyzer")
page = st.sidebar.selectbox("Select Option", ["Upload Resume", "View Database"])

if page == "Upload Resume":
    st.title("Upload Candidate Resume")
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])

    if uploaded_file:
        text = ""
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""  # FIX
        else:
            text = str(uploaded_file.read(), "utf-8")

        name, email, phone, skills = extract_info(text)
        scores = calculate_scores(skills)
        best_role = max(scores, key=scores.get)

        st.write(name, email, phone, skills)
        st.write(scores)
        st.success(f"Best Role: {best_role}")

        if st.button("Save"):
            c.execute(
                """INSERT INTO resumes 
                (name, email, phone, skills,
                 data_engineer_score, software_developer_score,
                 data_scientist_score, machine_engineer_score, best_role)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    name,
                    email,
                    phone,
                    ", ".join(skills),
                    scores["Data Engineer"],
                    scores["Software Developer"],
                    scores["Data Scientist"],
                    scores["Machine Engineer"],
                    best_role,
                ),
            )
            conn.commit()
            st.success("Saved!")

elif page == "View Database":
    st.title("Database")

    df = pd.read_sql("SELECT * FROM resumes", conn)

    if not df.empty:
        st.dataframe(df)

        selected_role = st.selectbox("Role", list(role_skills.keys()))
        col = selected_role.lower().replace(" ", "_") + "_score"

        top5 = df[["name", "email", col]].sort_values(by=col, ascending=False).head(5)
        st.dataframe(top5)

        fig, ax = plt.subplots()
        ax.bar(top5["name"], top5[col])
        st.pyplot(fig)
    else:
        st.write("App Finished")
