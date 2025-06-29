from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import User
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please fill in all fields', 'error')
            return render_template('login.html')
        
        user = User.get_by_email(email)
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        
        # Validation
        if not all([username, email, password, confirm_password, full_name]):
            flash('Please fill in all fields', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('register.html')
        
        # Check if email is valid
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            flash('Please enter a valid email address', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if User.get_by_email(email):
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create user
        user = User.create_user(username, email, password, full_name, 'student')
        if user:
            login_user(user)
            flash(f'Welcome, {user.full_name}! Your account has been created successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Error creating account. Please try again.', 'error')
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('home'))

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('dashboard'))
        else:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please fill in all fields', 'error')
            return render_template('admin_login.html')
        
        user = User.get_by_email(email)
        if user and user.role == 'admin' and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, Admin {user.full_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid admin credentials', 'error')
    
    return render_template('admin_login.html')
