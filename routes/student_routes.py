from flask import Blueprint, request, jsonify
from db_config import get_db_connection

student_bp = Blueprint('student_bp', __name__)

# Route to add a student
@student_bp.route('/add_student', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    program = data.get('program')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO students (name, email, program) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, program))
        conn.commit()
        return jsonify({'message': 'Student added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Route to get all students
@student_bp.route('/students', methods=['GET'])
def get_students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        return jsonify(students), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
