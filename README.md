# Syllabus Management System

A comprehensive web-based portal for managing academic syllabi, designed for educational institutions. This system allows both administrators and students to efficiently manage and access course materials, syllabi, and academic content.

## 🌟 Features

### For Administrators
- **Program Management**: Add, edit, and manage academic programs (B.Tech, M.Tech, etc.)
- **Subject Management**: Create and organize subjects by specialization and semester
- **Unit Management**: Define course units with topics and allocated hours
- **File Upload System**: Upload syllabus files (PDF, DOC, DOCX, TXT)
- **User Management**: Manage student and admin accounts
- **Dashboard Analytics**: View statistics and recent activities

### For Students
- **Syllabus Viewer**: Browse subjects by program, specialization, and semester
- **File Downloads**: Access uploaded syllabus files and course materials
- **Progress Tracking**: Monitor academic progress and attendance
- **Responsive Interface**: Access content on any device

### General Features
- **Role-based Access Control**: Separate interfaces for admins and students
- **Modern UI/UX**: Clean, responsive design with Bootstrap 5
- **Secure Authentication**: Flask-Login with password hashing
- **Database Management**: SQLite backend with proper relationships
- **File Management**: Secure file upload and download system

## 🚀 Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (built-in Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login
- **File Handling**: Werkzeug
- **Icons**: Font Awesome

## 📋 Prerequisites

Before running this application, make sure you have:

1. **Python 3.8+** installed
2. **pip** (Python package manager)

**Note**: No external database server required - SQLite is built into Python!

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd syllabus
```

### 2. Run Setup Script (Recommended)
```bash
python setup.py
```

This will automatically:
- Install all required dependencies
- Create the SQLite database
- Set up the database schema
- Create a default admin user
- Create necessary directories

### 3. Manual Installation (Alternative)
If you prefer manual setup:

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Create Database and Setup Schema
```bash
python setup.py
```

## 🏃‍♂️ Running the Application

### Development Mode
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Production Mode
For production deployment, consider using:
- Gunicorn or uWSGI as WSGI server
- Nginx as reverse proxy
- Environment variables for configuration

## 📁 Project Structure

```
syllabus/
├── app.py                 # Main Flask application
├── models.py              # User model and database helpers
├── db_config.py           # Database configuration (SQLite)
├── db_schema.sql          # Database schema and sample data
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── setup.py              # Setup script for SQLite
├── routes/               # Flask blueprints
│   ├── auth_routes.py    # Authentication routes
│   ├── admin_routes.py   # Admin management routes
│   ├── student_routes.py # Student routes
│   └── syllabus_routes.py # Syllabus viewing routes
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── admin_dashboard.html # Admin dashboard
│   ├── student_dashboard.html # Student dashboard
│   ├── view_syllabus.html # Syllabus viewer
│   ├── admin_programs.html # Program management
│   └── ...               # Other templates
├── static/               # Static files
│   ├── syllabus.jpg      # Logo image
│   └── style.css         # Custom styles
├── database/             # SQLite database directory
│   └── syllabus_app.db   # SQLite database file
└── uploads/              # File upload directory
```

## 🔐 Default Credentials

### Admin Account
- **Email**: admin@syllabus.com
- **Password**: admin123
- **Role**: Administrator

### Sample Data
The database schema includes:
- Sample programs (B.Tech, M.Tech)
- Sample specializations (CSE, MECH, EEE, CIVIL)
- Sample semesters (1st to 8th semester)

## 🎯 Usage Guide

### For Administrators

1. **Login** with admin credentials
2. **Dashboard**: View system statistics and quick actions
3. **Manage Programs**: Add/edit academic programs
4. **Manage Subjects**: Create subjects for different specializations
5. **Manage Units**: Define course units and topics
6. **Upload Files**: Upload syllabus documents and materials

### For Students

1. **Register** for a new account or **Login** with existing credentials
2. **Dashboard**: View academic progress and recent activities
3. **View Syllabus**: Select program, specialization, and semester to browse subjects
4. **Download Materials**: Access uploaded syllabus files

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production:
```env
FLASK_SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

### File Upload Settings
- **Allowed Extensions**: PDF, DOC, DOCX, TXT
- **Upload Directory**: `uploads/`
- **Max File Size**: Configure in Flask settings

## 🛡️ Security Features

- **Password Hashing**: Using Werkzeug's security functions
- **Session Management**: Flask-Login for user sessions
- **Role-based Access**: Admin and student role separation
- **SQL Injection Prevention**: Parameterized queries
- **File Upload Security**: File type validation and secure filenames

## 📊 Database Schema

### Core Tables
- **users**: User accounts and authentication
- **programs**: Academic programs (B.Tech, M.Tech, etc.)
- **specializations**: Program specializations (CSE, MECH, etc.)
- **semesters**: Academic semesters
- **subjects**: Course subjects
- **units**: Subject units and topics
- **syllabus_files**: Uploaded syllabus files
- **student_enrollments**: Student program enrollments

## 🚀 Deployment

### Local Development
```bash
export FLASK_ENV=development
python app.py
```

### Production Deployment
1. Set up a production WSGI server (Gunicorn)
2. Configure Nginx as reverse proxy
3. Set up SSL certificates
4. Configure environment variables
5. Set up database backups (SQLite file)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0**: Initial release with basic functionality
- **v1.1.0**: Added file upload system
- **v1.2.0**: Enhanced UI/UX and dashboard features
- **v1.3.0**: Added role-based access control
- **v2.0.0**: Migrated from MySQL to SQLite for easier deployment

## 📞 Contact

- **Email**: support@syllabus.com
- **Website**: https://syllabus-manager.com
- **Documentation**: https://docs.syllabus-manager.com

---

**Note**: This is a comprehensive syllabus management system designed for educational institutions. The system now uses SQLite for easier setup and deployment without requiring external database servers.

## 🎉 Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd syllabus
   python setup.py
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Access the application**:
   - Open: http://localhost:5000
   - Login as admin: admin@syllabus.com / admin123

That's it! No database server setup required. 🚀
