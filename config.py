import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Friday Advanced Core"
    VERSION: str = "3.0.0-Render-Ready"
    
    # Render will inject your API keys here
    PRIMARY_AI_API_KEY: str | None = os.environ.get("PRIMARY_AI_API_KEY")
    VISION_API_KEY: str | None = os.environ.get("VISION_API_KEY")
    WEATHER_API_KEY: str | None = os.environ.get("WEATHER_API_KEY")
    
    UPLOAD_DIR: str = "uploads"

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
