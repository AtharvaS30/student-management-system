import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    prn TEXT NOT NULL,
    course TEXT NOT NULL
)
''')

conn.close()

print("Database created successfully!")
