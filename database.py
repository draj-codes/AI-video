import sqlite3

def init_db():
    conn = sqlite3.connect('summarizer.db')
    c = conn.cursor()
    # Create table to store video details
    c.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            original_duration REAL,
            summary_duration REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_video_record(filename, original_dur, summary_dur):
    conn = sqlite3.connect('summarizer.db')
    c = conn.cursor()
    c.execute('INSERT INTO videos (filename, original_duration, summary_duration) VALUES (?, ?, ?)',
              (filename, original_dur, summary_dur))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('summarizer.db')
    c = conn.cursor()
    c.execute('SELECT * FROM videos ORDER BY created_at DESC')
    data = c.fetchall()
    conn.close()
    return data