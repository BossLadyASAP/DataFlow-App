# Deployment Guide - INF232 EC2 Application

This guide provides instructions for deploying the INF232 EC2 Data Collection and Analysis Application to various platforms.

## Quick Start (Local Development)

```bash
# 1. Extract the ZIP file
unzip inf232_ec2_app.zip
cd inf232_ec2_app

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py

# 5. Open browser and navigate to http://localhost:5000
```

## Deployment to Heroku

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed

### Steps

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows/Linux - Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Add gunicorn to requirements.txt**
   ```bash
   echo "gunicorn==21.2.0" >> requirements.txt
   ```

5. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

6. **Open the app**
   ```bash
   heroku open
   ```

## Deployment to PythonAnywhere

### Steps

1. **Create PythonAnywhere Account**
   - Visit https://www.pythonanywhere.com
   - Sign up for a free account

2. **Upload Files**
   - Use the file upload feature to upload the ZIP file
   - Extract it in your home directory

3. **Create Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose Python and your version
   - Select "Flask" as the framework

4. **Configure WSGI File**
   - Edit the WSGI file to point to your app
   - Replace the content with:
   ```python
   import sys
   path = '/home/yourusername/inf232_ec2_app'
   if path not in sys.path:
       sys.path.append(path)
   from app import app as application
   ```

5. **Reload Web App**
   - Click "Reload" button in the Web tab

## Deployment to AWS (Elastic Beanstalk)

### Steps

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB Application**
   ```bash
   eb init -p python-3.11 inf232-ec2-app
   ```

3. **Create Environment**
   ```bash
   eb create inf232-ec2-env
   ```

4. **Deploy**
   ```bash
   eb deploy
   ```

5. **Open Application**
   ```bash
   eb open
   ```

## Deployment to Railway

### Steps

1. **Create Railway Account**
   - Visit https://railway.app
   - Sign up with GitHub

2. **Connect Repository**
   - Create a new project
   - Connect your GitHub repository
   - Railway will auto-detect Flask

3. **Configure Environment**
   - Set `FLASK_ENV=production`
   - Railway will automatically set up the database

4. **Deploy**
   - Push to main branch
   - Railway will automatically deploy

## Using Docker

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Build and Run

```bash
# Build image
docker build -t inf232-ec2-app .

# Run container
docker run -p 5000:5000 inf232-ec2-app

# Access at http://localhost:5000
```

## Environment Variables

For production deployment, set these environment variables:

```bash
FLASK_ENV=production
SECRET_KEY=your-secure-random-key
DATABASE=feedback.db
```

Generate a secure secret key:
```python
import secrets
print(secrets.token_hex(32))
```

## Database Persistence

For production, consider using:
- **PostgreSQL** for better reliability
- **Cloud Storage** for database backups
- **Automated backups** for data safety

## Monitoring & Logging

1. **Enable Logging**
   - Check application logs on your hosting platform
   - Monitor error rates and performance

2. **Set Up Alerts**
   - Configure alerts for high error rates
   - Monitor uptime

## Performance Optimization

1. **Enable Caching**
   - Cache static files (CSS, JS)
   - Set appropriate cache headers

2. **Database Optimization**
   - Add indexes to frequently queried columns
   - Archive old feedback data

3. **CDN**
   - Use CDN for static assets
   - Reduce load times for users worldwide

## SSL/HTTPS

Most platforms provide free SSL certificates:
- Heroku: Automatic
- PythonAnywhere: Automatic for paid plans
- AWS: Use AWS Certificate Manager
- Railway: Automatic

## Troubleshooting

### Application Won't Start
- Check logs for errors
- Verify all dependencies are installed
- Ensure Python version compatibility

### Database Errors
- Check database file permissions
- Verify database path is correct
- Ensure sufficient disk space

### Port Already in Use
- Change port in app.py
- Kill existing processes

## Support

For issues or questions:
- Check the main README.md
- Review Flask documentation: https://flask.palletsprojects.com/
- Contact course instructor: rollinfrancis28@gmail.com

---

**Last Updated**: April 2026
