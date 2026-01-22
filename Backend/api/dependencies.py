from typing import Generator, Optional
try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
except ImportError:
    MongoClient = None

from .config import settings

class DatabaseSession:
    _client: Optional[MongoClient] = None

    @classmethod
    def get_client(cls) -> Optional[MongoClient]:
        if cls._client is None and MongoClient:
            try:
                cls._client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=2000)
                # Check connection
                cls._client.admin.command('ping')
                print("Connected to MongoDB")
            except Exception as e:
                print(f"Could not connect to MongoDB: {e}. Using in-memory mode.")
                cls._client = None
        return cls._client

def get_db_client():
    """Dependency to get MongoDB client"""
    return DatabaseSession.get_client()

def get_current_user():
    """Mock authentication dependency"""
    # In a real app, this would verify JWT tokens
    return {
        "id": "F001",
        "username": "kisaan_demo",
        "role": "farmer",
        "state": "Maharashtra",
        "district": "Nasik"
    }
