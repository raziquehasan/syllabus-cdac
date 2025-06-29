#!/usr/bin/env python3
"""
Test script for Syllabus Management System
This script tests the basic functionality of the application.
"""

import requests
import json
import time

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_home_page():
    """Test the home page"""
    try:
        response = requests.get('http://localhost:5000/')
        if response.status_code == 200:
            print("✅ Home page accessible")
            return True
        else:
            print(f"❌ Home page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Home page error: {e}")
        return False

def test_admin_login():
    """Test admin login functionality"""
    try:
        # Test login page
        response = requests.get('http://localhost:5000/login')
        if response.status_code == 200:
            print("✅ Login page accessible")
            
            # Test login form submission
            login_data = {
                'email': 'admin@syllabus.com',
                'password': 'admin123'
            }
            
            response = requests.post('http://localhost:5000/login', data=login_data, allow_redirects=False)
            if response.status_code in [200, 302]:
                print("✅ Login form submission works")
                return True
            else:
                print(f"❌ Login form submission failed: {response.status_code}")
                return False
        else:
            print(f"❌ Login page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Login test error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        from db_config import get_db_connection
        from models import get_programs, get_subjects
        
        conn = get_db_connection()
        programs = get_programs()
        subjects = get_subjects()
        
        print(f"✅ Database connection successful")
        print(f"   - Found {len(programs)} programs")
        print(f"   - Found {len(subjects)} subjects")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Syllabus Management System...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Home Page", test_home_page),
        ("Database Connection", test_database_connection),
        ("Admin Login", test_admin_login),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1
        time.sleep(1)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is working correctly.")
        print("\n📝 Next steps:")
        print("1. Open your browser and go to: http://localhost:5000")
        print("2. Login with admin credentials:")
        print("   - Email: admin@syllabus.com")
        print("   - Password: admin123")
        print("3. Start managing your syllabus!")
    else:
        print("⚠️  Some tests failed. Please check the application logs.")
    
    print("=" * 50)

if __name__ == '__main__':
    main() 