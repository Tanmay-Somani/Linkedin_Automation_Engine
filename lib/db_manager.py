import sqlite3

def init_db():
    conn = sqlite3.connect('data/engine.db')
    cursor = conn.cursor()
    # Ideas we want to write about
    cursor.execute('''CREATE TABLE IF NOT EXISTS ideas 
        (id INTEGER PRIMARY KEY, topic TEXT, context TEXT, status TEXT DEFAULT 'pending')''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts 
        (id INTEGER PRIMARY KEY, content TEXT, posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def add_idea(topic, context):
    conn = sqlite3.connect('data/engine.db')
    conn.cursor().execute("INSERT INTO ideas (topic, context) VALUES (?, ?)", (topic, context))
    conn.commit()
    conn.close()