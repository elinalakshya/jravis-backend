class Settings(BaseSettings):
    PROJECT_NAME: str = "JRAVIS Backend"
    VERSION: str = "1.0.0"

    OPENAI_API_KEY: str

    # Add this 👇 new line
    N8N_WEBHOOK_SECRET: str = ""

    class Config:
        env_file = ".env"
