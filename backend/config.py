"""
🛡️ AegisMed - AI Hospital Administration Assistant
Backend Configuration & Settings
"""
from pydantic_settings import BaseSettings
from pathlib import Path
import os


class Settings(BaseSettings):
    # OpenAI Configuration
    openai_api_key: str = "your_openai_api_key_here"
    openai_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"

    # Storage Paths
    chroma_persist_dir: str = "./data/chroma_db"
    upload_dir: str = "./data/uploads"
    policies_dir: str = "./data/policies"

    # MongoDB Configuration
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "aegismed_db"

    # Server Config
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

# Ensure directories exist
for dir_path in [
    settings.chroma_persist_dir,
    settings.upload_dir,
    settings.policies_dir,
]:
    Path(dir_path).mkdir(parents=True, exist_ok=True)
