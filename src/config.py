from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "JRAVIS Backend"
    VERSION: str = "1.0.0"

    # External APIs
    OPENAI_API_KEY: str = ""
    N8N_WEBHOOK_SECRET: str = ""

    # 🔥 Worker Authentication Key (Required!)
    REPORT_API_CODE: str = ""   # ⭐ ADD THIS

    class Config:
        env_file = ".env"


settings = Settings()
