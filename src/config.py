from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "JRAVIS Backend"
    VERSION: str = "1.0.0"

    OPENAI_API_KEY: str = ""
    N8N_WEBHOOK_SECRET: str = ""  # NEW FIELD

    class Config:
        env_file = ".env"

settings = Settings()
