import sqlite3

DB_NAME = "resumes.db"

def connect_db():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = connect_db()
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
    conn.close()


def save_result(name, email, phone, skills, scores, best_role):
    conn = connect_db()
    c = conn.cursor()

    c.execute('''
        INSERT INTO resumes (
            name, email, phone, skills,
            data_engineer_score, software_developer_score,
            data_scientist_score, machine_engineer_score,
            best_role
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        name,
        email,
        phone,
        ', '.join(skills),
        scores['Data Engineer'],
        scores['Software Developer'],
        scores['Data Scientist'],
        scores['Machine Engineer'],
        best_role
    ))

    conn.commit()
    conn.close()


def fetch_all():
    conn = connect_db()
    c = conn.cursor()

    c.execute("SELECT * FROM resumes")
    data = c.fetchall()

    conn.close()
    return data


# Skill mapping
role_skills = {
    'Data Engineer': ['python', 'sql', 'hadoop', 'spark', 'aws', 'etl', 'big data'],
    'Software Developer': ['java', 'python', 'c++', 'git', 'html', 'css', 'javascript'],
    'Data Scientist': ['python', 'machine learning', 'deep learning', 'statistics', 'pandas', 'numpy'],
    'Machine Engineer': ['c++', 'python', 'arduino', 'robotics', 'mechanical']
}