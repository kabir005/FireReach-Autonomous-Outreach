"""Configuration management for FireReach."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    
    # Gmail SMTP Configuration
    GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
    GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
    
    # Email Configuration
    FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@firereach.ai")
    FROM_NAME = os.getenv("FROM_NAME", "FireReach by Rabbitt AI")
    
    # Model Configuration
    LLM_MODEL = "llama-3.3-70b-versatile"
    
    @classmethod
    def validate(cls) -> list[str]:
        """Validate required configuration."""
        errors = []
        
        if not cls.GROQ_API_KEY:
            errors.append("GROQ_API_KEY is required")
        
        if not cls.SERPAPI_KEY and not cls.TAVILY_API_KEY:
            errors.append("Either SERPAPI_KEY or TAVILY_API_KEY is required")
        
        if not cls.GMAIL_EMAIL or not cls.GMAIL_APP_PASSWORD:
            errors.append("GMAIL_EMAIL and GMAIL_APP_PASSWORD are required")
        
        return errors

config = Config()
