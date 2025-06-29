import sqlite3
import os

def get_db_connection():
    # Create database directory if it doesn't exist
    db_dir = 'database'
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    db_path = os.path.join(db_dir, 'syllabus_app.db')
    return sqlite3.connect(db_path)
