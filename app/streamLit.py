"""
Smart Resume Analyzer — Streamlit entry point.
Run: streamlit run app/app.py or streamlit run app/streamlit.py
"""

import streamlit as st
from parser import extract_text, parse_resume
from database import init_db, save_result, calculate_scores, role_skills
import json

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
        # Extract text from uploaded file
        raw_text = extract_text(uploaded_file)
        
        # Parse resume to get basic info
        basic_info = parse_resume(raw_text)
        
        # Get skills list from parsed resume
        skills_list = basic_info.get('skills', [])
        
        # Calculate scores for each role
        scores = calculate_scores(skills_list)
        
        # Find the best role (highest score)
        best_role = max(scores, key=scores.get) if scores else "Not determined"
        
        # Prepare complete result for database
        result = {
            'name': basic_info.get('name', ''),
            'email': basic_info.get('email', ''),
            'phone': basic_info.get('phone', ''),
            'skills': ', '.join(skills_list) if isinstance(skills_list, list) else skills_list,
            'data_engineer_score': scores.get('Data Engineer', 0),
            'software_developer_score': scores.get('Software Developer', 0),
            'data_scientist_score': scores.get('Data Scientist', 0),
            'machine_engineer_score': scores.get('Machine Engineer', 0),
            'best_role': best_role
        }

    st.success("Analysis complete!")

    # Display results in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Extracted Information")
        st.write(f"**Name:** {result['name']}")
        st.write(f"**Email:** {result['email']}")
        st.write(f"**Phone:** {result['phone']}")
        st.write(f"**Skills Found:** {result['skills']}")
    
    with col2:
        st.subheader("🎯 Role Match Scores")
        
        # Display scores with progress bars
        for role, score in scores.items():
            st.write(f"**{role}:** {score:.1f}%")
            st.progress(score / 100)
        
        st.write(f"\n**🏆 Best Match:** {best_role}")
        st.metric(label="Top Match Score", value=f"{scores.get(best_role, 0):.1f}%")

    # Save to database
    save_result(result)
    st.info("✅ Results saved to database successfully!")

    # Optional: Show detailed skills required for best role
    with st.expander("📚 View Required Skills for Top Role"):
        if best_role in role_skills:
            st.write(f"**Skills needed for {best_role}:**")
            for skill in role_skills[best_role]:
                st.write(f"- {skill}")
    
    # Optional: Show all role requirements
    with st.expander("🔍 View All Role Requirements"):
        for role, skills in role_skills.items():
            st.write(f"**{role}:** {', '.join(skills)}")
else:
    # Show instructions when no file is uploaded
    st.info("👈 Please upload a resume (PDF or DOCX) to get started")

# Optional: Add a sidebar with info
with st.sidebar:
    st.header("About")
    st.write("This app analyzes resumes and matches them with different job roles:")
    st.write("- Data Engineer")
    st.write("- Software Developer") 
    st.write("- Data Scientist")
    st.write("- Machine Engineer")
    
    st.header("How it works")
    st.write("1. Upload your resume (PDF or DOCX)")
    st.write("2. App extracts text and identifies skills")
    st.write("3. Skills are matched against role requirements")
    st.write("4. Scores are calculated and saved to database")