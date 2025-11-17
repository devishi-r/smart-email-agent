from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    MONGO_URI: str
    CALENDAR_ID: str
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"
