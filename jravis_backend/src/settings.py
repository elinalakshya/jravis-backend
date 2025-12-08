from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

    PROJECT_NAME: str = "JRAVIS BACKEND"
    API_KEY: str = "JRV2040_LOCKED_KEY_001"
    DEBUG: bool = False


settings = Settings()

