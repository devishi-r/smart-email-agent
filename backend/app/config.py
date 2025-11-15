from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    MONGO_URI: str
    CALENDAR_ID: str

    class Config:
        env_file = ".env"
