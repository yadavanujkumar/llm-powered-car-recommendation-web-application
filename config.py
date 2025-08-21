import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the application"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Application settings
    MAX_RECOMMENDATIONS = int(os.getenv('MAX_RECOMMENDATIONS', '5'))
    CHAT_TIMEOUT = int(os.getenv('CHAT_TIMEOUT', '30'))  # seconds
    
    @staticmethod
    def validate_config():
        """Validate that required configuration is present"""
        errors = []
        
        if not Config.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required. Please set it in your .env file.")
        
        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(errors))
        
        return True