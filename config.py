import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Detect environment
ENV = os.getenv('FLASK_ENV', 'development')
IS_PRODUCTION = ENV == 'production'

# Base directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Upload and storage paths
UPLOAD_FOLDER = os.path.join(BASE_DIR, os.getenv('UPLOAD_FOLDER', 'uploads'))
STATIC_FOLDER = os.path.join(BASE_DIR, os.getenv('STATIC_FOLDER', 'static'))
DATABASE_FOLDER = os.path.join(BASE_DIR, 'database')

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)
if not IS_PRODUCTION:
    os.makedirs(DATABASE_FOLDER, exist_ok=True)

# Database configuration
if IS_PRODUCTION:
    # Use PostgreSQL in production
    DATABASE_URL = os.getenv('DATABASE_URL')
    # Fix Heroku's postgres:// to postgresql://
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
else:
    # Use SQLite in development
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(DATABASE_FOLDER, "wildlife.db")}'

SQLALCHEMY_TRACK_MODIFICATIONS = False

# File upload settings
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB default
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

# ML Model settings
MODEL_NAME = os.getenv('MODEL_NAME', 'yolov8n.pt')  # Nano version for faster inference
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.25))  # Minimum confidence for detections

# Wildlife classes from COCO dataset
WILDLIFE_CLASSES = [
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 
    'elephant', 'bear', 'zebra', 'giraffe'
]

# Flask settings
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't') if IS_PRODUCTION else True
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# CORS settings
if IS_PRODUCTION:
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',') if os.getenv('CORS_ORIGINS') else ['*']
else:
    CORS_ORIGINS = '*'

