import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "KisaanMitra")

class Database:
    client: AsyncIOMotorClient = None
    
    async def connect_db(self):
        """Create database connection."""
        try:
            self.client = AsyncIOMotorClient(MONGO_DETAILS)
            # Verify connection
            await self.client.admin.command('ping')
            logger.info("Connected to MongoDB.")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise e

    def close_db(self):
        """Close database connection."""
        if self.client:
            self.client.close()
            logger.info("Closed MongoDB connection.")

    def get_database(self):
        """Get database instance."""
        if self.client is None:
             # In case it's called before explicit connect (though not recommended for async)
             logger.warning("Database client is not initialized. Attempting lazy connection...")
             self.client = AsyncIOMotorClient(MONGO_DETAILS)
        return self.client[DB_NAME]

db = Database()

# Dependency for FastAPI
async def get_database():
    if db.client is None:
        await db.connect_db()
    return db.get_database()
