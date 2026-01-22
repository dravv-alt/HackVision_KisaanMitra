import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "KisaanMitra"

class Database:
    client: AsyncIOMotorClient = None
    
    def connect_db(self):
        """Create database connection."""
        self.client = AsyncIOMotorClient(MONGO_DETAILS)
        print("Connected to MongoDB.")

    def close_db(self):
        """Close database connection."""
        self.client.close()
        print("Closed MongoDB connection.")

    def get_database(self):
        """Get database instance."""
        return self.client[DB_NAME]

db = Database()

# Dependency for FastAPI
async def get_database():
    if db.client is None:
        db.connect_db()
    return db.get_database()
