#!/bin/bash

# Build the Docker image
echo "Building Docker image..."
docker build -t syllabus-app .

# Run the container
echo "Starting container..."
docker run -d \
  --name syllabus-container \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-production-secret-key \
  -v $(pwd)/database:/app/database \
  -v $(pwd)/uploads:/app/uploads \
  syllabus-app

echo "Container started! Access the application at http://localhost:5000"
echo "To stop the container: docker stop syllabus-container"
echo "To remove the container: docker rm syllabus-container" 