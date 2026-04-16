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

role_skills = {
    'Data Engineer': ['python', 'sql', 'hadoop', 'spark', 'aws', 'etl', 'big data'],
    'Software Developer': ['java', 'python', 'c++', 'git', 'html', 'css', 'javascript'],
    'Data Scientist': ['python', 'machine learning', 'deep learning', 'statistics', 'pandas', 'numpy', 'matplotlib'],
    'Machine Engineer': ['c++', 'python', 'arduino', 'robotics', 'mechanical engineering']
}

# 🔴 ERROR: Variable name typo - 'conn' vs 'connn'
connn = connect_db()  # Misspelled variable name
create_table(connn)   # Using wrong variable name
c = connn.cursor()    # This will work but wrong name

# 🔴 ERROR: Using undefined variable later
print(some_undefined_variable)  # NameError

# 🔴 ERROR: Division by zero in score calculation
test_score = 100 / 0  # ZeroDivisionError
