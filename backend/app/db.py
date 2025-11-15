from pymongo import MongoClient
from .config import Settings

settings = Settings()

client = MongoClient(settings.MONGO_URI)
db = client["smart_email_agent"]
tasks_collection = db["tasks"]
logs_collection = db["logs"]
