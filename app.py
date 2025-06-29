from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.syllabus_routes import syllabus_bp
from routes.admin_routes import admin_bp
from models import User, get_programs, get_specializations, get_semesters, get_subjects, get_units, get_syllabus_files
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(syllabus_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        # Get data for dashboard statistics
        programs = get_programs()
        specializations = get_specializations()
        subjects = get_subjects()
        units = []
        files = []
        
        # Get all units
        for subject in subjects:
            subject_units = get_units(subject['id'])
            units.extend(subject_units)
        
        # Get all files
        for subject in subjects:
            subject_files = get_syllabus_files(subject['id'])
            files.extend(subject_files)
        
        return render_template('admin_dashboard.html', 
                             programs=programs, 
                             specializations=specializations,
                             subjects=subjects, 
                             units=units, 
                             files=files)
    else:
        return render_template('student_dashboard.html')

@app.route('/view_syllabus')
@login_required
def view_syllabus():
    # Get all data from backend
    programs = get_programs()
    specializations = get_specializations()
    semesters = get_semesters()
    subjects = get_subjects()
    
    # Organize data by program for easier access
    program_data = {}
    for program in programs:
        program_data[program['id']] = {
            'program': program,
            'specializations': [spec for spec in specializations if spec['program_id'] == program['id']],
            'semesters': [sem for sem in semesters if sem['program_id'] == program['id']]
        }
    
    return render_template('view_syllabus.html', 
                         programs=programs, 
                         specializations=specializations,
                         semesters=semesters,
                         subjects=subjects,
                         program_data=program_data)

@app.route('/get_specializations/<int:program_id>')
def get_specializations_ajax(program_id):
    specializations = get_specializations(program_id)
    return {'specializations': specializations}

@app.route('/get_semesters/<int:program_id>')
def get_semesters_ajax(program_id):
    semesters = get_semesters(program_id)
    return {'semesters': semesters}

@app.route('/get_subjects/<int:specialization_id>/<int:semester_id>')
def get_subjects_ajax(specialization_id, semester_id):
    subjects = get_subjects(specialization_id, semester_id)
    return {'subjects': subjects}

@app.route('/subject/<int:subject_id>')
@login_required
def view_subject(subject_id):
    from models import get_subjects, get_units, get_syllabus_files
    
    # Get subject details
    subjects = get_subjects()
    subject = None
    for s in subjects:
        if s['id'] == subject_id:
            subject = s
            break
    
    if not subject:
        flash('Subject not found', 'error')
        return redirect(url_for('view_syllabus'))
    
    # Get units and files
    units = get_units(subject_id)
    files = get_syllabus_files(subject_id)
    
    return render_template('subject_detail.html', subject=subject, units=units, files=files)

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'message': 'Syllabus Management System is running'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Get host from environment variable or default to 0.0.0.0 for Docker
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Get debug mode from environment variable
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
