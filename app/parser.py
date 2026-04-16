# parser.py (updated to return skills as list)
import pdfplumber
import re

def extract_text(uploaded_file):
    """Extract text from uploaded PDF file"""
    text = ""
    # Save uploaded file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with pdfplumber.open("temp.pdf") as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    
    return text

def parse_resume(text):
    """Parse resume and extract information"""
    # Extract email
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    email = email_match.group() if email_match else "Not found"
    
    # Extract phone (10 digits)
    phone_match = re.search(r'\b\d{10}\b', text)
    phone = phone_match.group() if phone_match else "Not found"
    
    # Extract name (first line or after common patterns)
    lines = text.strip().split('\n')
    name = lines[0] if lines else "Not found"
    
    # Common skills to look for (expanded list)
    skills_list = [
        'python', 'java', 'sql', 'javascript', 'html', 'css',
    'machine learning', 'deep learning', 'nlp', 'data science',
        'pandas', 'numpy', 'matplotlib', 'scikit-learn', 'tensorflow', 'pytorch',
        'hadoop', 'spark', 'aws', 'etl', 'big data',
        'c++', 'arduino', 'robotics', 'mechanical engineering',
        'git', 'docker', 'kubernetes', 'rest api', 'flask', 'django'
    ]
    
    # Find skills present in resume
    found_skills = []
    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": found_skills  # Return as list
    }