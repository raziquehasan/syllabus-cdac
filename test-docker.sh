#!/bin/bash

echo "🐳 Syllabus Management System - Docker Test Script"
echo "=================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    echo "   Download from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker is installed and running"

# Test Dockerfile syntax
echo "🔍 Testing Dockerfile syntax..."
if docker build --dry-run . &> /dev/null; then
    echo "✅ Dockerfile syntax is valid"
else
    echo "❌ Dockerfile syntax error"
    exit 1
fi

echo ""
echo "🚀 Ready to deploy!"
echo ""
echo "📋 Deployment Steps:"
echo "1. Build the image: docker build -t syllabus-app ."
echo "2. Run with Docker Compose: docker-compose up --build"
echo "3. Or run directly: docker run -p 5000:5000 syllabus-app"
echo ""
echo "🌐 Access the application at: http://localhost:5000"
echo "👤 Admin login: admin@syllabus.com / admin123" 