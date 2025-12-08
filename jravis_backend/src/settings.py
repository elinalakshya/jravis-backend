import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
model_config = {"env_file": ".env"}   
 PROJECT_NAME: str = "JRAVIS Backend"

    # Worker API Key
    WORKER_KEY: str = os.getenv("WORKER_API_KEY", "JRAVIS_2040_MASTER_KEY")

    # Internal paths safe for Render
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    FILE_STORAGE: str = os.path.join(BASE_DIR, "files")

    class Config:
        extra = "allow"

settings = Settings()
