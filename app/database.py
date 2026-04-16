import sqlite3

def connect_db():
    return sqlite3.connect('resumes.db')

def create_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            skills TEXT,
            data_engineer_score REAL,
            software_developer_score REAL,
            data_scientist_score REAL,
            machine_engineer_score REAL,
            best_role TEXT
        )
    ''')
    conn.commit()

def init_db():
    """Initialize database and create table"""
    conn = connect_db()  # Fixed: proper variable name
    create_table(conn)
    conn.close()
    print("Database initialized successfully!")

def save_result(result):
    """Save resume analysis result to database"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO resumes (
            name, email, phone, skills, 
            data_engineer_score, software_developer_score, 
            data_scientist_score, machine_engineer_score, 
            best_role
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        result.get('name', ''),
        result.get('email', ''),
        result.get('phone', ''),
        result.get('skills', ''),
        result.get('data_engineer_score', 0),
        result.get('software_developer_score', 0),
        result.get('data_scientist_score', 0),
        result.get('machine_engineer_score', 0),
        result.get('best_role', '')
    ))
    conn.commit()
    conn.close()

# Role skills dictionary (for scoring)
role_skills = {
    'Data Engineer': ['python', 'sql', 'hadoop', 'spark', 'aws', 'etl', 'big data'],
    'Software Developer': ['java', 'python', 'c++', 'git', 'html', 'css', 'javascript'],
    'Data Scientist': ['python', 'machine learning', 'deep learning', 'statistics', 'pandas', 'numpy', 'matplotlib'],
    'Machine Engineer': ['c++', 'python', 'arduino', 'robotics', 'mechanical engineering']
}

def calculate_scores(skills_list):
    """Calculate scores for each role based on matching skills"""
    scores = {}
    for role, required_skills in role_skills.items():
        matches = len(set(skills_list) & set(required_skills))
        total = len(required_skills)
        scores[role] = (matches / total * 100) if total > 0 else 0  # Fixed: avoid division by zero
    return scores

# Test the database (only runs if this file is executed directly)
if __name__ == "__main__":
    init_db()
    
    # Test data
    test_result = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '1234567890',
        'skills': 'python,sql,machine learning',
        'data_engineer_score': 85,
        'software_developer_score': 75,
        'data_scientist_score': 90,
        'machine_engineer_score': 60,
        'best_role': 'Data Scientist'
    }
    
    save_result(test_result)
    print("Test data saved successfully!")