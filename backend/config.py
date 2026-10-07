import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
os.makedirs(DB_DIR, exist_ok=True)
DEFAULT_DB_FILE = os.path.join(DB_DIR, "farmer_advisory.db").replace("\\", "/")

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-farmer-advisory-key-2026")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-advisory-token-key-2026")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_EXPIRES_HOURS", 24)))
    
    # Database Configuration: SQLite fallback if DATABASE_URL is not set or unavailable
    env_db_url = os.getenv("DATABASE_URL", "")
    if not env_db_url or env_db_url.startswith("sqlite"):
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{DEFAULT_DB_FILE}"
    else:
        SQLALCHEMY_DATABASE_URI = env_db_url

    # Fix for Heroku/Render postgres:// URI schema
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Uploads Configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    
    # External APIs and Demo Mode
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    WEATHER_API_BASE_URL = "https://api.openweathermap.org/data/2.5"
    DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")
    
    # ML Models Paths
    CROP_MODEL_PATH = os.path.join(BASE_DIR, "ml", "crop_recommendation", "crop_model.pkl")
    CROP_PREPROCESSOR_PATH = os.path.join(BASE_DIR, "ml", "crop_recommendation", "preprocessor.pkl")
    DISEASE_MODEL_PATH = os.path.join(BASE_DIR, "ml", "disease_detection", "disease_model.keras")
    YIELD_MODEL_PATH = os.path.join(BASE_DIR, "ml", "yield_prediction", "yield_model.pkl")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
