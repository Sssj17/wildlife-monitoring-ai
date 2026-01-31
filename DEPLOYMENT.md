# 🚀 Deployment Guide - Wildlife Monitoring AI

This guide covers deploying your Wildlife Monitoring System to production using various cloud platforms.

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:
- ✅ Application runs successfully locally
- ✅ All tests pass
- ✅ Dependencies are properly documented
- ✅ Environment variables are identified
- ✅ Security settings are configured

---

## 🎯 Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

**Pros**: Easy setup, free tier, automatic deployments, PostgreSQL included
**Best for**: Quick deployment, learning, portfolio projects

**Steps**:

1. **Create account** at [render.com](https://render.com)

2. **Push code to GitHub**:
   ```bash
   cd C:\Users\SHIVANI\.gemini\antigravity\scratch\wildlife-monitoring-ai
   git init
   git add .
   git commit -m "Initial commit - Wildlife Monitoring AI"
   # Create repo on GitHub, then:
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

3. **Create Web Service on Render**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: wildlife-monitoring-ai
     - **Environment**: Python 3
     - **Build Command**: `pip install -r backend/requirements.txt`
     - **Start Command**: `cd backend && gunicorn app:app`
     - **Instance Type**: Free

4. **Add Environment Variables**:
   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-random-string>
   DATABASE_URL=<render-will-provide>
   ```

5. **Deploy**: Click "Create Web Service"

**Configuration files needed**: See `render.yaml` and `Procfile` below

---

### Option 2: Heroku (Easy, Popular)

**Pros**: Easy CLI, many add-ons, good documentation
**Cons**: No free tier anymore (starts at $5/month)

**Steps**:

1. **Install Heroku CLI**:
   Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login and create app**:
   ```bash
   heroku login
   cd C:\Users\SHIVANI\.gemini\antigravity\scratch\wildlife-monitoring-ai
   heroku create wildlife-monitoring-ai
   ```

3. **Add PostgreSQL**:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set environment variables**:
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=<your-random-key>
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   ```

6. **Open app**:
   ```bash
   heroku open
   ```

**Configuration needed**: `Procfile`, `runtime.txt`

---

### Option 3: PythonAnywhere (Beginner-Friendly)

**Pros**: Designed for Python apps, free tier available, no credit card required
**Best for**: Students, first deployment

**Steps**:

1. **Create account** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload code**:
   - Use "Files" tab to upload ZIP
   - Or use Git: `git clone <your-repo-url>`

3. **Create virtual environment**:
   ```bash
   mkvirtualenv wildlife-env --python=python3.10
   cd wildlife-monitoring-ai/backend
   pip install -r requirements.txt
   ```

4. **Configure Web App**:
   - Go to "Web" tab → "Add a new web app"
   - Choose "Manual configuration" → Python 3.10
   - Set source code directory
   - Edit WSGI configuration file (see template below)

5. **Set static files**:
   - URL: `/static/` → Directory: `/home/yourusername/wildlife-monitoring-ai/static`
   - URL: `/uploads/` → Directory: `/home/yourusername/wildlife-monitoring-ai/uploads`

6. **Reload** and visit your domain

---

### Option 4: Railway (Modern, Developer-Friendly)

**Pros**: Modern UI, automatic HTTPS, generous free tier
**Steps**: Similar to Render, uses `railway.json` config

---

### Option 5: AWS EC2 (Advanced)

**Pros**: Full control, scalable, professional
**Cons**: More complex, requires DevOps knowledge
**Best for**: Production applications, learning cloud infrastructure

---

## 🔧 Production Configuration Files

### 1. requirements.txt (Production)

Create `backend/requirements-prod.txt`:

```
Flask==3.0.0
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.1.1
ultralytics==8.1.0
Pillow==10.2.0
opencv-python-headless==4.9.0.80
numpy==1.26.3
gunicorn==21.2.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

**Changes from dev**:
- Added `gunicorn` for production server
- Added `psycopg2-binary` for PostgreSQL
- Added `python-dotenv` for environment variables
- Changed `opencv-python` to `opencv-python-headless` (smaller, no GUI)

---

### 2. Procfile (for Heroku/Render)

Create `Procfile` in root directory:

```
web: cd backend && gunicorn app:app
```

---

### 3. runtime.txt (for Heroku)

Create `runtime.txt` in root:

```
python-3.11.7
```

---

### 4. render.yaml (for Render)

Create `render.yaml` in root:

```yaml
services:
  - type: web
    name: wildlife-monitoring-ai
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && gunicorn app:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: wildlife-db
          property: connectionString

databases:
  - name: wildlife-db
    databaseName: wildlife
    user: wildlife_user
```

---

### 5. .env.example

Create `.env.example` in root:

```env
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# File Upload
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=/app/uploads
STATIC_FOLDER=/app/static

# ML Model
MODEL_NAME=yolov8n.pt
CONFIDENCE_THRESHOLD=0.25

# Server
HOST=0.0.0.0
PORT=5000
```

---

### 6. .gitignore

Create `.gitignore` in root:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Environment
.env
.env.local

# Database
*.db
database/

# Uploads
uploads/*
!uploads/.gitkeep
static/*
!static/.gitkeep

# ML Models (download at runtime)
*.pt
*.pth

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

---

## 🔒 Production Security Updates

### Update config.py for Production

Add environment variable support:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Detect environment
ENV = os.getenv('FLASK_ENV', 'development')
IS_PRODUCTION = ENV == 'production'

# Base directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Database
if IS_PRODUCTION:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # Fix Heroku postgres:// to postgresql://
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
else:
    DATABASE_FOLDER = os.path.join(BASE_DIR, 'database')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(DATABASE_FOLDER, "wildlife.db")}'

# Secret key for sessions
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Debug mode
DEBUG = not IS_PRODUCTION

# CORS
if IS_PRODUCTION:
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')
else:
    CORS_ORIGINS = '*'
```

---

## 📊 Database Migration (SQLite → PostgreSQL)

When moving to production, migrate to PostgreSQL:

### Step 1: Update app.py

```python
# Change this line
CORS(app)

# To this (for production)
from flask_cors import CORS
CORS(app, origins=config.CORS_ORIGINS)
```

### Step 2: Database initialization

```python
# In app.py, add this before db.create_all():
if config.IS_PRODUCTION:
    # Check if tables exist
    with app.app_context():
        inspector = db.inspect(db.engine)
        if not inspector.has_table('sightings'):
            db.create_all()
            print("Production database initialized!")
```

---

## 🌐 Custom Domain Setup

After deploying, you can add a custom domain:

### For Render:
1. Go to Settings → Custom Domain
2. Add your domain (e.g., `wildlife.yourdomain.com`)
3. Update DNS records as instructed

### For Heroku:
```bash
heroku domains:add www.yourdomain.com
```

### DNS Configuration:
Add CNAME record pointing to your platform's URL.

---

## 📈 Monitoring & Maintenance

### Application Monitoring

**Render**: Built-in metrics dashboard
**Heroku**: Use Heroku CLI `heroku logs --tail`

### Error Tracking

Add Sentry for error monitoring:
```bash
pip install sentry-sdk
```

```python
# In app.py
import sentry_sdk
sentry_sdk.init(dsn=os.getenv('SENTRY_DSN'))
```

### Performance Optimization

1. **Enable caching**: Add Flask-Caching
2. **CDN for images**: Use Cloudflare or AWS CloudFront
3. **Database indexing**: Add indexes on frequently queried fields
4. **Image optimization**: Compress uploads before storage

---

## 🧪 Pre-Deployment Testing

Test production configuration locally:

```bash
# Set environment
set FLASK_ENV=production

# Run with Gunicorn
cd backend
gunicorn app:app
```

Visit `http://localhost:8000` to test.

---

## 🚨 Common Deployment Issues

### Issue: Model file too large
**Solution**: Download model at runtime instead of including in repo
```python
# In ml_detector.py __init__
if not os.path.exists(MODEL_NAME):
    print(f"Downloading {MODEL_NAME}...")
    # YOLO will auto-download
```

### Issue: File uploads not persisting
**Solution**: Use cloud storage (AWS S3, Cloudinary)

### Issue: CORS errors
**Solution**: Configure allowed origins in production config

### Issue: Database connection errors
**Solution**: Check DATABASE_URL format, ensure PostgreSQL addon is active

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Production dependencies listed
- [ ] Environment variables configured  
- [ ] Database migrated to PostgreSQL
- [ ] Static files configured
- [ ] CORS origins restricted
- [ ] SECRET_KEY set (random, secure)
- [ ] Debug mode disabled
- [ ] Error tracking enabled
- [ ] Domain configured (optional)
- [ ] SSL/HTTPS enabled
- [ ] Tested in production environment

---

## 🎓 Recommended First Deployment: Render

For your first deployment, I recommend **Render** because:
1. ✅ Free tier available (no credit card required)
2. ✅ Automatic deployments from GitHub
3. ✅ Built-in PostgreSQL database
4. ✅ Free SSL certificates
5. ✅ Simple configuration
6. ✅ Great for portfolios

---

## 📚 Additional Resources

- [Flask Deployment Documentation](https://flask.palletsprojects.com/en/latest/deploying/)
- [Render Guides](https://render.com/docs)
- [Heroku Python Support](https://devcenter.heroku.com/categories/python-support)
- [PythonAnywhere Help](https://help.pythonanywhere.com/)

---

**Next Steps**: Choose your deployment platform and I'll create the specific configuration files you need!
