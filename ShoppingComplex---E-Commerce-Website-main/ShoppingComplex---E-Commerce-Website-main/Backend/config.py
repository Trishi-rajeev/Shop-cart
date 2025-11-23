"""
Configuration settings for the recommendation system
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # API Settings
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Database Settings
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ecommerce.db')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'ecommerce_db')
    
    # Recommendation Settings
    MIN_RATINGS_FOR_RECOMMENDATION = int(os.getenv('MIN_RATINGS', 5))
    MAX_RECOMMENDATIONS = int(os.getenv('MAX_RECOMMENDATIONS', 10))
    SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', 0.3))
    
    # Model Settings
    COLLABORATIVE_WEIGHT = float(os.getenv('COLLABORATIVE_WEIGHT', 0.6))
    CONTENT_WEIGHT = float(os.getenv('CONTENT_WEIGHT', 0.4))
    
    # Cache Settings
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True').lower() == 'true'
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 hour
    
    # CORS Settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Secret Key
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
