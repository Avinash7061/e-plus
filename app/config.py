from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Pydantic BaseSettings class for environment variables"""
    SUPABASE_URL: str
    SUPABASE_KEY: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
