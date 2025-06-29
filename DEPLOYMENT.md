# Deployment Guide

This guide will help you deploy the Syllabus Management System using Docker and Render.

## 🐳 Docker Deployment

### Prerequisites
- Docker installed on your system
- Git repository cloned

### Local Docker Development

1. **Build the Docker image:**
   ```bash
   docker build -t syllabus-app .
   ```

2. **Run with Docker Compose (recommended for development):**
   ```bash
   docker-compose up --build
   ```

3. **Or run with Docker directly:**
   ```bash
   docker run -d \
     --name syllabus-container \
     -p 5000:5000 \
     -e FLASK_ENV=development \
     -e SECRET_KEY=your-secret-key \
     -v $(pwd)/database:/app/database \
     -v $(pwd)/uploads:/app/uploads \
     syllabus-app
   ```

4. **Access the application:**
   - Open your browser and go to `http://localhost:5000`
   - Login with admin credentials:
     - Email: `admin@syllabus.com`
     - Password: `admin123`

### Production Docker Deployment

1. **Build production image:**
   ```bash
   docker build -f Dockerfile.prod -t syllabus-app-prod .
   ```

2. **Run production container:**
   ```bash
   docker run -d \
     --name syllabus-prod \
     -p 5000:5000 \
     -e FLASK_ENV=production \
     -e SECRET_KEY=your-production-secret-key \
     -e PORT=5000 \
     syllabus-app-prod
   ```

## 🚀 Render Deployment

### Automatic Deployment (Recommended)

1. **Connect your GitHub repository to Render:**
   - Go to [render.com](https://render.com)
   - Sign up/Login with your GitHub account
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository

2. **Configure the service:**
   - **Name:** `syllabus-management-system`
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app`
   - **Plan:** Free (or choose your preferred plan)

3. **Environment Variables:**
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: Generate a secure random key
   - `FLASK_DEBUG`: `false`

4. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

### Manual Deployment

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Use the render.yaml file:**
   - The `render.yaml` file in this repository contains the deployment configuration
   - Render will automatically detect and use this file

## 🔧 Environment Variables

### Required Variables
- `SECRET_KEY`: A secure random string for Flask sessions
- `FLASK_ENV`: Set to `production` for production deployment

### Optional Variables
- `PORT`: Port number (default: 5000)
- `HOST`: Host binding (default: 0.0.0.0)
- `FLASK_DEBUG`: Debug mode (default: false)

## 📁 File Structure for Deployment

```
syllabus/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Development Docker configuration
├── Dockerfile.prod       # Production Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── render.yaml           # Render deployment configuration
├── .dockerignore         # Docker ignore file
├── database/             # SQLite database directory
├── uploads/              # File upload directory
├── routes/               # Flask blueprints
├── templates/            # HTML templates
└── static/               # Static files
```

## 🔍 Health Check

The application includes a health check endpoint at `/health` that returns:
```json
{
  "status": "healthy",
  "message": "Syllabus Management System is running"
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Find and kill the process using port 5000
   lsof -ti:5000 | xargs kill -9
   ```

2. **Permission denied:**
   ```bash
   # Make deploy script executable
   chmod +x deploy.sh
   ```

3. **Database not found:**
   - Ensure the `database` directory exists
   - Run the setup script: `python setup.py`

4. **Upload directory not found:**
   - Ensure the `uploads` directory exists
   - The application will create it automatically

### Docker Commands

```bash
# View running containers
docker ps

# View logs
docker logs syllabus-container

# Stop container
docker stop syllabus-container

# Remove container
docker rm syllabus-container

# Remove image
docker rmi syllabus-app
```

## 🔒 Security Considerations

1. **Change default admin password** after first login
2. **Use strong SECRET_KEY** in production
3. **Enable HTTPS** in production
4. **Regular backups** of the database
5. **Monitor logs** for security issues

## 📊 Monitoring

### Render Dashboard
- Monitor application health
- View logs and metrics
- Set up alerts

### Application Logs
- Access logs through Render dashboard
- Monitor for errors and performance issues

## 🔄 Updates and Maintenance

1. **Update code:**
   ```bash
   git pull origin main
   ```

2. **Rebuild and redeploy:**
   ```bash
   docker-compose down
   docker-compose up --build
   ```

3. **Render automatic deployment:**
   - Push changes to GitHub
   - Render will automatically redeploy

## 📞 Support

For deployment issues:
1. Check the application logs
2. Verify environment variables
3. Ensure all dependencies are installed
4. Contact support if needed

---

**Note:** This application uses SQLite for simplicity. For production use with high traffic, consider using PostgreSQL or MySQL with proper database hosting. 