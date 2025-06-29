from flask import Blueprint, render_template, request

syllabus_bp = Blueprint('syllabus', __name__)

@syllabus_bp.route('/course/manage')
def manage_course():
    return render_template('course_management.html')

@syllabus_bp.route('/subject/manage')
def manage_subject():
    return render_template('subject_management.html')

@syllabus_bp.route('/unit/manage')
def manage_unit():
    return render_template('unit_management.html')

@syllabus_bp.route('/unit/view')
def view_units():
    return render_template('view_units.html')
