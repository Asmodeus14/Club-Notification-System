import sqlite3

def create_table():
    conn = sqlite3.connect('database.db')  # Connect to SQLite database
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_dummy_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    dummy_data = [
        ('John Doe', 'john@example.com'),
        ('Jane Smith', 'jane@example.com'),
        ('Alice Johnson', 'alice@example.com')
    ]
    cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', dummy_data)
    conn.commit()
    conn.close()

def fetch_entries():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows to a list of dictionaries
    # entries = [{'id': row[0], 'name': row[1], 'email': row[2]} for row in rows]
    return rows[0]

create_table()
insert_dummy_data()
print(fetch_entries())  # Output: [(1, 'John Doe', 'john@example.com'),