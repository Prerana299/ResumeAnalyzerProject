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

role_skills = {
    'Data Engineer': ['python', 'sql', 'hadoop', 'spark', 'aws', 'etl', 'big data'],
    'Software Developer': ['java', 'python', 'c++', 'git', 'html', 'css', 'javascript'],
    'Data Scientist': ['python', 'machine learning', 'deep learning', 'statistics', 'pandas', 'numpy', 'matplotlib'],
    'Machine Engineer': ['c++', 'python', 'arduino', 'robotics', 'mechanical engineering']
}

conn = connect_db()
create_table(conn)
c = conn.cursor()


