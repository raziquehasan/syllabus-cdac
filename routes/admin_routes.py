from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, send_file, abort
from flask_login import login_required, current_user
from models import (
    get_programs, get_specializations, get_semesters, get_subjects, 
    get_units, get_syllabus_files, get_total_users, get_db_connection
)
from werkzeug.utils import secure_filename
import os
import sqlite3
import magic
import logging
from functools import wraps
from datetime import datetime
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain'
}

def ensure_upload_dir():
    """Ensure upload directory exists and has correct permissions."""
    upload_dir = os.path.join(current_app.root_path, 'uploads')
    try:
        os.makedirs(upload_dir, exist_ok=True, mode=0o755)
        return upload_dir
    except Exception as e:
        logger.error(f"Failed to create upload directory: {e}")
        raise

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
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
    
    # Get total number of users
    total_users = get_total_users()
    
    return render_template('admin_dashboard.html', 
                         programs=programs, 
                         specializations=specializations,
                         subjects=subjects, 
                         units=units, 
                         files=files,
                         total_users=total_users)

# Program Management
@admin_bp.route('/admin/programs', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_programs():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        description = request.form.get('description')
        duration = request.form.get('duration', 4)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO programs (name, code, description, duration_years) VALUES (?, ?, ?, ?)",
                (name, code, description, duration)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Program added successfully', 'success')
        except Exception as e:
            flash(f'Error adding program: {str(e)}', 'error')
    
    programs = get_programs()
    return render_template('admin_programs.html', programs=programs)

@admin_bp.route('/admin/programs/<int:program_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_program(program_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE programs SET is_active = 0 WHERE id = ?", (program_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Program deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting program: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_programs'))

# Subject Management
@admin_bp.route('/admin/subjects', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_subjects():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        credits = request.form.get('credits', 3)
        description = request.form.get('description')
        specialization_id = request.form.get('specialization_id')
        semester_id = request.form.get('semester_id')
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO subjects (name, code, credits, description, specialization_id, semester_id) VALUES (?, ?, ?, ?, ?, ?)",
                (name, code, credits, description, specialization_id, semester_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Subject added successfully', 'success')
        except Exception as e:
            flash(f'Error adding subject: {str(e)}', 'error')
    
    programs = get_programs()
    specializations = get_specializations()
    semesters = get_semesters()
    subjects = get_subjects()
    
    return render_template('admin_subjects.html', 
                         programs=programs, 
                         specializations=specializations, 
                         semesters=semesters, 
                         subjects=subjects)

@admin_bp.route('/admin/subjects/<int:subject_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_subject(subject_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE subjects SET is_active = 0 WHERE id = ?", (subject_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Subject deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting subject: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_subjects'))

# Unit Management
@admin_bp.route('/admin/units', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_units():
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        unit_number = request.form.get('unit_number')
        title = request.form.get('title')
        description = request.form.get('description')
        topics = request.form.get('topics')
        hours = request.form.get('hours', 10)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO units (subject_id, unit_number, title, description, topics, hours_allocated) VALUES (?, ?, ?, ?, ?, ?)",
                (subject_id, unit_number, title, description, topics, hours)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Unit added successfully', 'success')
        except Exception as e:
            flash(f'Error adding unit: {str(e)}', 'error')
    
    subjects = get_subjects()
    units = []
    for subject in subjects:
        subject_units = get_units(subject['id'])
        for unit in subject_units:
            unit['subject_name'] = subject['name']
        units.extend(subject_units)
    
    return render_template('admin_units.html', subjects=subjects, units=units)

@admin_bp.route('/admin/units/<int:unit_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_unit(unit_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE units SET is_active = 0 WHERE id = ?", (unit_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Unit deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting unit: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_units'))

# File Upload Management
@admin_bp.route('/admin/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def upload_syllabus():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        subject_id = request.form.get('subject_id')
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        # Check file size
        file_content = file.read()
        if len(file_content) > MAX_FILE_SIZE:
            flash(f'File too large. Maximum size is {MAX_FILE_SIZE/1024/1024}MB', 'error')
            return redirect(request.url)
        
        # Reset file pointer
        file.seek(0)
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Allowed: pdf, doc, docx, txt', 'error')
            return redirect(request.url)
        
        # Ensure upload directory exists
        try:
            upload_dir = ensure_upload_dir()
        except Exception as e:
            logger.error(f"Upload directory error: {e}")
            flash('Server configuration error. Please contact administrator.', 'error')
            return redirect(request.url)
        
        # Generate safe filename
        unique_filename = sanitize_filename(file.filename)
        file_path = os.path.join(upload_dir, unique_filename)
        
        conn = None
        cursor = None
        try:
            # Save file temporarily to check MIME type
            temp_path = f"{file_path}.tmp"
            file.save(temp_path)
            
            # Verify MIME type
            mime = magic.Magic(mime=True)
            file_mime = mime.from_file(temp_path)
            if file_mime not in ALLOWED_MIME_TYPES:
                os.remove(temp_path)
                flash('Invalid file type detected', 'error')
                return redirect(request.url)
            
            # Rename temp file to final name
            os.rename(temp_path, file_path)
            
            # Save to database in a transaction
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO syllabus_files 
                (subject_id, filename, original_filename, file_path, 
                 file_size, file_type, uploaded_by, uploaded_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """, (
                subject_id, 
                unique_filename, 
                file.filename, 
                file_path,
                os.path.getsize(file_path),
                file_mime,
                current_user.id
            ))
            
            conn.commit()
            logger.info(f"File uploaded successfully: {unique_filename}")
            flash('File uploaded successfully', 'success')
            
        except Exception as e:
            # Clean up in case of error
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass
                    
            logger.error(f"Error uploading file: {e}", exc_info=True)
            flash('Error uploading file. Please try again.', 'error')
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
        # Clean up orphaned files (run occasionally, not on every request)
        if datetime.now().hour % 6 == 0:  # Run every 6 hours
            cleanup_orphaned_files()
    
    subjects = get_subjects()
    # Add files data to each subject
    for subject in subjects:
        subject['files'] = get_syllabus_files(subject['id'])
    
    return render_template('admin_upload.html', subjects=subjects)

@admin_bp.route('/admin/files/<int:file_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_file(file_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get file info before deleting
        cursor.execute("SELECT file_path FROM syllabus_files WHERE id = ?", (file_id,))
        file_info = cursor.fetchone()
        
        if file_info and os.path.exists(file_info[0]):
            os.remove(file_info[0])
        
        cursor.execute("DELETE FROM syllabus_files WHERE id = ?", (file_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('File deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting file: {str(e)}', 'error')
    
    return redirect(url_for('admin.upload_syllabus'))

from flask import send_from_directory
from werkzeug.utils import secure_filename

@admin_bp.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    """
    Download a file using its database ID.
    Uses Flask's send_file for better performance with large files.
    """
    conn = None
    cursor = None
    try:
        # Get file info from database
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row  # This enables dictionary-style access
        cursor = conn.cursor()
        
        # Get file metadata with user permissions check
        cursor.execute("""
            SELECT sf.id, sf.file_path, sf.original_filename, sf.file_type, 
                   sf.file_size, sf.uploaded_by, u.username as uploaded_by_name
            FROM syllabus_files sf
            LEFT JOIN users u ON sf.uploaded_by = u.id
            WHERE sf.id = ?
        """, (file_id,))
        
        file_info = cursor.fetchone()
        if not file_info:
            logger.warning(f"File not found in database: {file_id}")
            flash('File not found', 'error')
            return redirect(url_for('view_syllabus'))
        
        # Convert Row to dict if needed
        if hasattr(file_info, 'keys'):
            file_info = dict(file_info)
        
        # Check if user has permission to download
        if current_user.role != 'admin' and str(file_info.get('uploaded_by')) != str(current_user.id):
            logger.warning(f"Unauthorized download attempt by user {current_user.id} for file {file_id}")
            abort(403, description="You don't have permission to download this file")
        
        file_path = file_info.get('file_path')
        if not file_path:
            logger.error(f"File path is empty for file_id: {file_id}")
            flash('File path is missing', 'error')
            return redirect(url_for('view_syllabus'))
        
        # Verify file exists and is readable
        if not os.path.isfile(file_path):
            # Try to find in uploads directory as fallback
            filename = os.path.basename(file_path)
            alt_path = os.path.join(current_app.root_path, 'uploads', filename)
            if os.path.isfile(alt_path):
                file_path = alt_path
            else:
                logger.error(f"File not found on server: {file_path}")
                flash('File not found on server', 'error')
                return redirect(url_for('view_syllabus'))
        
        # Get safe filename for download
        download_name = secure_filename(file_info.get('original_filename', f'file_{file_id}'))
        
        # Set appropriate MIME type
        mime_type = file_info.get('file_type', 'application/octet-stream')
        
        # Log the download
        logger.info(f"File downloaded - ID: {file_id}, User: {current_user.id}, File: {file_path}")
        
        # Send the file
        return send_file(
            file_path,
            as_attachment=True,
            download_name=download_name,
            mimetype=mime_type,
            etag=True,
            max_age=0,  # Prevent caching
            conditional=True
        )
        
    except Exception as e:
        logger.error(f"Error downloading file {file_id}: {str(e)}", exc_info=True)
        flash('Error downloading file. Please try again.', 'error')
        return redirect(url_for('view_syllabus'))
        
    finally:
        # Clean up database connection
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
            logger.error(f"Error closing database connection: {str(e)}")

def allowed_file(filename):
    """Check if the file has an allowed extension and MIME type."""
    if not ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        return False
    
    # Verify MIME type
    try:
        mime = magic.Magic(mime=True)
        file_mime = mime.from_file(filename)
        return file_mime in ALLOWED_MIME_TYPES
    except Exception as e:
        logger.error(f"Error checking MIME type: {e}")
        return False

def sanitize_filename(filename):
    """Sanitize filename and ensure it's unique."""
    base, ext = os.path.splitext(secure_filename(filename))
    timestamp = int(datetime.utcnow().timestamp() * 1000)
    return f"{base}_{timestamp}{ext}"

def cleanup_orphaned_files():
    """Remove files that exist on disk but not in the database."""
    try:
        upload_dir = ensure_upload_dir()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all files in the database
        cursor.execute("SELECT file_path FROM syllabus_files")
        db_files = {os.path.basename(row[0]) for row in cursor.fetchall()}
        
        # Check files on disk
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path) and filename not in db_files:
                try:
                    os.remove(file_path)
                    logger.info(f"Removed orphaned file: {filename}")
                except Exception as e:
                    logger.error(f"Failed to remove orphaned file {filename}: {e}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error during orphaned files cleanup: {e}")
        if 'conn' in locals():
            conn.close()

# Specialization Management
@admin_bp.route('/admin/specializations', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_specializations():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        description = request.form.get('description')
        program_id = request.form.get('program_id')
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO specializations (name, code, description, program_id) VALUES (?, ?, ?, ?)",
                (name, code, description, program_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Specialization added successfully', 'success')
        except Exception as e:
            flash(f'Error adding specialization: {str(e)}', 'error')
    
    programs = get_programs()
    specializations = get_specializations()
    return render_template('admin_specializations.html', programs=programs, specializations=specializations)

@admin_bp.route('/admin/specializations/<int:specialization_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_specialization(specialization_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE specializations SET is_active = 0 WHERE id = ?", (specialization_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Specialization deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting specialization: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_specializations'))

# Semester Management
@admin_bp.route('/admin/semesters', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_semesters():
    if request.method == 'POST':
        name = request.form.get('name')
        semester_number = request.form.get('semester_number')
        program_id = request.form.get('program_id')
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO semesters (name, semester_number, program_id) VALUES (?, ?, ?)",
                (name, semester_number, program_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Semester added successfully', 'success')
        except Exception as e:
            flash(f'Error adding semester: {str(e)}', 'error')
    
    programs = get_programs()
    semesters = get_semesters()
    return render_template('admin_semesters.html', programs=programs, semesters=semesters)

@admin_bp.route('/admin/semesters/<int:semester_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_semester(semester_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE semesters SET is_active = 0 WHERE id = ?", (semester_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Semester deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting semester: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_semesters')) 