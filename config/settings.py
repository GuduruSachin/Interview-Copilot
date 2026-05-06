from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str = Field("YOUR_API_KEY", env="GEMINI_API_KEY")
    WHISPER_MODEL: str = "base"
    LOG_LEVEL: str = "INFO"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
