-- Syllabus Management System Database Schema (SQLite)

-- Users table (for both students and admins)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'student')) DEFAULT 'student',
    full_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Programs/Courses table (B.Tech, M.Tech, etc.)
CREATE TABLE IF NOT EXISTS programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    description TEXT,
    duration_years INTEGER DEFAULT 4,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Specializations table (CS, Mech, etc.)
CREATE TABLE IF NOT EXISTS specializations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id INTEGER,
    name TEXT NOT NULL,
    code TEXT NOT NULL,
    description TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE
);

-- Semesters table
CREATE TABLE IF NOT EXISTS semesters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id INTEGER,
    semester_number INTEGER NOT NULL,
    name TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE
);

-- Subjects table
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    credits INTEGER DEFAULT 3,
    description TEXT,
    specialization_id INTEGER,
    semester_id INTEGER,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (specialization_id) REFERENCES specializations(id) ON DELETE SET NULL,
    FOREIGN KEY (semester_id) REFERENCES semesters(id) ON DELETE SET NULL
);

-- Units table
CREATE TABLE IF NOT EXISTS units (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    unit_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    topics TEXT,
    hours_allocated INTEGER DEFAULT 10,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

-- Syllabus files table
CREATE TABLE IF NOT EXISTS syllabus_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    filename TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER,
    file_type TEXT,
    uploaded_by INTEGER,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Student enrollments table
CREATE TABLE IF NOT EXISTS student_enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    program_id INTEGER,
    specialization_id INTEGER,
    enrollment_date DATE,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE,
    FOREIGN KEY (specialization_id) REFERENCES specializations(id) ON DELETE CASCADE
);

-- Insert default admin user (password: admin123)
INSERT OR IGNORE INTO users (username, email, password_hash, role, full_name) 
VALUES ('admin', 'admin@syllabus.com', 'pbkdf2:sha256:600000$admin123$hash_here', 'admin', 'System Administrator');

-- Insert sample programs
INSERT OR IGNORE INTO programs (name, code, description) VALUES 
('Bachelor of Technology', 'BTECH', '4-year undergraduate engineering program'),
('Master of Technology', 'MTECH', '2-year postgraduate engineering program');

-- Insert sample specializations
INSERT OR IGNORE INTO specializations (program_id, name, code, description) VALUES 
(1, 'Computer Science Engineering', 'CSE', 'Computer Science and Engineering specialization'),
(1, 'Mechanical Engineering', 'MECH', 'Mechanical Engineering specialization'),
(1, 'Electrical Engineering', 'EEE', 'Electrical and Electronics Engineering specialization'),
(1, 'Civil Engineering', 'CIVIL', 'Civil Engineering specialization');

-- Insert sample semesters for B.Tech
INSERT OR IGNORE INTO semesters (program_id, semester_number, name) VALUES 
(1, 1, 'First Semester'),
(1, 2, 'Second Semester'),
(1, 3, 'Third Semester'),
(1, 4, 'Fourth Semester'),
(1, 5, 'Fifth Semester'),
(1, 6, 'Sixth Semester'),
(1, 7, 'Seventh Semester'),
(1, 8, 'Eighth Semester'); 