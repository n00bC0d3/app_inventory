import os
from dotenv import load_dotenv
import redis

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session Configuration
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    # ✅ Removed SESSION_USE_SIGNER — not needed in Flask-Session >= 0.8.0
    
    # ✅ Create Redis client object from URL
    redis_client = redis.from_url(os.environ.get('REDIS_URL'))
    SESSION_REDIS = redis_client
    
    # Security settings
    _is_https = os.environ.get('HTTPS_ENABLED', 'false').lower() == 'true'
    SESSION_COOKIE_SECURE = _is_https
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'