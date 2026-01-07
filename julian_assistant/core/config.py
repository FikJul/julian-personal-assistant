"""
Configuration management for Julian Assistant
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for Julian Assistant"""
    
    # API Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///julian_assistant.db")
    
    # Agent Configuration
    AGENT_NAME: str = os.getenv("AGENT_NAME", "Julian")
    LANGUAGE: str = os.getenv("LANGUAGE", "id")  # Indonesian by default
    
    # Model Configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Schedule Configuration
    TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Jakarta")
    
    # Finance Configuration
    DEFAULT_CURRENCY: str = os.getenv("DEFAULT_CURRENCY", "IDR")
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith("_") and key.isupper()
        }
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required in .env file")
        return True


# Create global config instance
config = Config()
