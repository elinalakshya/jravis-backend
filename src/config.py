# src/config.py
import os

class Settings:
    PROJECT_NAME = "JRAVIS Backend API"
    VERSION = "1.0.0"
    API_KEY = os.getenv("JRAVIS_API_KEY", "JRV_DEFAULT_KEY")

settings = Settings()
