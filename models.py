from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_db_connection
import os
import sqlite3

class User(UserMixin):
    def __init__(self, id, username, email, role, full_name):
        self.id = id
        self.username = username
        self.email = email
        self.role = role
        self.full_name = full_name

    @staticmethod
    def get_by_id(user_id):
        try:
            conn = get_db_connection()
            conn.row_factory = sqlite3.Row  # Enable dictionary-like access
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    role=user_data['role'],
                    full_name=user_data['full_name']
                )
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None

    @staticmethod
    def get_by_email(email):
        try:
            conn = get_db_connection()
            conn.row_factory = sqlite3.Row  # Enable dictionary-like access
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    role=user_data['role'],
                    full_name=user_data['full_name']
                )
            return None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None

    @staticmethod
    def create_user(username, email, password, full_name, role='student'):
        try:
            password_hash = generate_password_hash(password)
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, full_name, role) VALUES (?, ?, ?, ?, ?)",
                (username, email, password_hash, full_name, role)
            )
            conn.commit()
            user_id = cursor.lastrowid
            cursor.close()
            conn.close()
            
            return User(id=user_id, username=username, email=email, role=role, full_name=full_name)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def check_password(self, password):
        try:
            conn = get_db_connection()
            conn.row_factory = sqlite3.Row  # Enable dictionary-like access
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE id = ?", (self.id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if result:
                return check_password_hash(result['password_hash'], password)
            return False
        except Exception as e:
            print(f"Error checking password: {e}")
            return False

# Database helper functions
def get_programs():
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM programs WHERE is_active = 1 ORDER BY name")
        programs = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(program) for program in programs]
    except Exception as e:
        print(f"Error getting programs: {e}")
        return []

def get_specializations(program_id=None):
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        cursor = conn.cursor()
        if program_id:
            cursor.execute("SELECT * FROM specializations WHERE program_id = ? AND is_active = 1 ORDER BY name", (program_id,))
        else:
            cursor.execute("SELECT * FROM specializations WHERE is_active = 1 ORDER BY name")
        specializations = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(spec) for spec in specializations]
    except Exception as e:
        print(f"Error getting specializations: {e}")
        return []

def get_semesters(program_id=None):
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        cursor = conn.cursor()
        if program_id:
            cursor.execute("SELECT * FROM semesters WHERE program_id = ? AND is_active = 1 ORDER BY semester_number", (program_id,))
        else:
            cursor.execute("SELECT * FROM semesters WHERE is_active = 1 ORDER BY semester_number")
        semesters = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(semester) for semester in semesters]
    except Exception as e:
        print(f"Error getting semesters: {e}")
        return []

def get_subjects(specialization_id=None, semester_id=None):
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        cursor = conn.cursor()
        
        if specialization_id and semester_id:
            cursor.execute("""
                SELECT s.*, sp.name as specialization_name, sem.name as semester_name 
                FROM subjects s 
                LEFT JOIN specializations sp ON s.specialization_id = sp.id 
                LEFT JOIN semesters sem ON s.semester_id = sem.id 
                WHERE s.specialization_id = ? AND s.semester_id = ? AND s.is_active = 1 
                ORDER BY s.name
            """, (specialization_id, semester_id))
        elif specialization_id:
            cursor.execute("""
                SELECT s.*, sp.name as specialization_name, sem.name as semester_name 
                FROM subjects s 
                LEFT JOIN specializations sp ON s.specialization_id = sp.id 
                LEFT JOIN semesters sem ON s.semester_id = sem.id 
                WHERE s.specialization_id = ? AND s.is_active = 1 
                ORDER BY s.name
            """, (specialization_id,))
        else:
            cursor.execute("""
                SELECT s.*, sp.name as specialization_name, sem.name as semester_name 
                FROM subjects s 
                LEFT JOIN specializations sp ON s.specialization_id = sp.id 
                LEFT JOIN semesters sem ON s.semester_id = sem.id 
                WHERE s.is_active = 1 
                ORDER BY s.name
            """)
        
        subjects = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(subject) for subject in subjects]
    except Exception as e:
        print(f"Error getting subjects: {e}")
        return []

def get_units(subject_id):
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM units WHERE subject_id = ? AND is_active = 1 ORDER BY unit_number", (subject_id,))
        units = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(unit) for unit in units]
    except Exception as e:
        print(f"Error getting units: {e}")
        return []

def get_syllabus_files(subject_id):
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sf.*, u.username as uploaded_by_name 
            FROM syllabus_files sf
            LEFT JOIN users u ON sf.uploaded_by = u.id
            WHERE sf.subject_id = ?
            ORDER BY sf.uploaded_at DESC
        """, (subject_id,))
        files = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return files
    except Exception as e:
        print(f"Error getting syllabus files: {e}")
        return []


def get_total_users():
    """
    Get the total number of registered users.
    Returns:
        int: Total number of users
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else 0
    except Exception as e:
        print(f"Error getting total users: {e}")
        return 0