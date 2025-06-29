#!/usr/bin/env python3
"""
Database Setup Script for Syllabus Management System
This script initializes the database with the schema and sample data.
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database with schema and sample data."""
    
    # Create database directory if it doesn't exist
    db_dir = 'database'
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    db_path = os.path.join(db_dir, 'syllabus_app.db')
    
    # Read the schema file
    with open('db_schema.sql', 'r') as f:
        schema = f.read()
    
    # Connect to database and execute schema
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Execute the schema
        cursor.executescript(schema)
        
        # Create admin user with proper password hash
        admin_password_hash = generate_password_hash('admin123')
        cursor.execute("""
            INSERT OR REPLACE INTO users (username, email, password_hash, role, full_name) 
            VALUES (?, ?, ?, ?, ?)
        """, ('admin', 'admin@syllabus.com', admin_password_hash, 'admin', 'System Administrator'))
        
        # Insert sample subjects
        sample_subjects = [
            ('Programming Fundamentals', 'CS101', 3, 'Introduction to programming concepts', 1, 1),
            ('Data Structures', 'CS201', 4, 'Advanced data structures and algorithms', 1, 3),
            ('Database Systems', 'CS301', 3, 'Database design and management', 1, 5),
            ('Web Development', 'CS401', 4, 'Modern web development technologies', 1, 7),
            ('Machine Learning', 'CS501', 4, 'Introduction to machine learning', 1, 8),
        ]
        
        for subject in sample_subjects:
            cursor.execute("""
                INSERT OR IGNORE INTO subjects (name, code, credits, description, specialization_id, semester_id) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, subject)
        
        # Insert sample units
        sample_units = [
            (1, 1, 'Introduction to Programming', 'Basic programming concepts and syntax', 'Variables, Data Types, Control Structures', 10),
            (1, 2, 'Functions and Modules', 'Function definition and modular programming', 'Function Declaration, Parameters, Return Values', 12),
            (2, 1, 'Arrays and Lists', 'Linear data structures', 'Array Operations, List Manipulation, Searching', 15),
            (2, 2, 'Stacks and Queues', 'Stack and queue implementations', 'LIFO, FIFO, Applications', 12),
            (3, 1, 'Database Design', 'Relational database design principles', 'ER Diagrams, Normalization, SQL Basics', 14),
        ]
        
        for unit in sample_units:
            cursor.execute("""
                INSERT OR IGNORE INTO units (subject_id, unit_number, title, description, topics, hours_allocated) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, unit)
        
        conn.commit()
        print("✅ Database initialized successfully!")
        print("📊 Sample data added:")
        print("   - Admin user (username: admin, password: admin123)")
        print("   - 2 Programs (B.Tech, M.Tech)")
        print("   - 4 Specializations (CSE, MECH, EEE, CIVIL)")
        print("   - 8 Semesters")
        print("   - 5 Sample Subjects")
        print("   - 5 Sample Units")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("🚀 Initializing Syllabus Management System Database...")
    init_database()
    print("✨ Setup complete!") 