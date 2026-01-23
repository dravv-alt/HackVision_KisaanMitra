import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "KisaanMitra")

print(f"🔄 Testing MongoDB connection...")
print(f"   URI: {MONGO_URI}")
print(f"   Database: {DB_NAME}")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    client.admin.command('ping')
    print("✅ Database is ACTIVE and reachable!")
    
    db = client[DB_NAME]
    
    # Check collections
    collections = db.list_collection_names()
    print(f"\n📊 Found {len(collections)} collections:")
    for col in collections[:10]:  # Show first 10
        count = db[col].count_documents({})
        print(f"   - {col}: {count} documents")
    
    # Check farmers specifically
    farmers_count = db.farmers.count_documents({})
    print(f"\n👨‍🌾 Farmers collection: {farmers_count} documents")
    
    if farmers_count > 0:
        sample = db.farmers.find_one()
        print(f"   Sample farmer ID: {sample.get('_id')}")
    
except Exception as e:
    print(f"❌ Database connection FAILED: {e}")
    print("\n💡 Make sure MongoDB is running:")
    print("   - Check if MongoDB service is started")
    print("   - Verify MONGO_URI in .env file")
