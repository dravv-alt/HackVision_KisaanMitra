"""
Database Status Check and API Testing Script
Tests MongoDB connection and verifies API endpoints are working
"""
import requests
import json
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "KisaanMitra"
API_BASE_URL = "http://localhost:8000"

def check_database():
    """Check if MongoDB is active and show stats"""
    print("=" * 70)
    print("🔍 CHECKING DATABASE CONNECTION")
    print("=" * 70)
    
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        print(f"✅ MongoDB is ACTIVE at {MONGO_URI}")
        
        db = client[DB_NAME]
        collections = db.list_collection_names()
        
        print(f"\n📊 Database: {DB_NAME}")
        print(f"   Collections: {len(collections)}")
        
        # Key collections to check
        key_collections = ['farmers', 'crops_master', 'equipment_listings', 'users']
        
        for col in key_collections:
            if col in collections:
                count = db[col].count_documents({})
                print(f"   ✓ {col}: {count} documents")
                
                # Show sample for farmers
                if col == 'farmers' and count > 0:
                    sample = db[col].find_one()
                    print(f"      Sample ID: {sample.get('_id')}")
            else:
                print(f"   ✗ {col}: NOT FOUND")
        
        return True, client
        
    except Exception as e:
        print(f"❌ MongoDB connection FAILED: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check if MongoDB service is running")
        print("   2. Verify MONGO_URI in .env file")
        print("   3. Try: net start MongoDB (Windows)")
        return False, None

def test_api_endpoints(db_active):
    """Test key API endpoints"""
    print("\n" + "=" * 70)
    print("🧪 TESTING API ENDPOINTS")
    print("=" * 70)
    
    # Test 1: Planning Stage - Pre-seeding
    print("\n1️⃣ Testing Farm Management - Pre-seeding Planning")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/farm-management/planning/pre-seeding",
            json={
                "farmer_id": "F001",
                "season": "rabi",
                "risk_preference": "balanced"
            },
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS - Got {len(data.get('crop_cards', []))} crop recommendations")
            print(f"      Urgency: {data.get('urgency_level')}")
        else:
            print(f"   ⚠️  Status {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    
    # Test 2: Collaborative Farming - Marketplace
    print("\n2️⃣ Testing Collaborative Farming - Marketplace")
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/collaborative/marketplace",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS - Found {len(data.get('equipmentCards', []))} equipment listings")
            print(f"      Land pools: {len(data.get('landPoolCards', []))}")
        else:
            print(f"   ⚠️  Status {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    
    # Test 3: Dashboard Stats
    print("\n3️⃣ Testing Dashboard - Stats")
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/dashboard/stats",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS - Active crops: {data.get('active_crops')}")
            print(f"      Weather: {data.get('weather', {}).get('condition')}")
        else:
            print(f"   ⚠️  Status {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")

def seed_sample_data(client):
    """Seed minimal sample data if database is empty"""
    print("\n" + "=" * 70)
    print("🌱 SEEDING SAMPLE DATA")
    print("=" * 70)
    
    if not client:
        print("❌ Cannot seed - no database connection")
        return
    
    db = client[DB_NAME]
    
    # Seed a test farmer
    if db.farmers.count_documents({}) == 0:
        print("\n👨‍🌾 Creating test farmer...")
        farmer_doc = {
            "_id": "F001",
            "userId": "U001",
            "language": "hi",
            "location": {
                "state": "Punjab",
                "district": "Ludhiana",
                "village": "Jagraon",
                "lat": 30.7850,
                "lon": 75.4731
            },
            "soilType": "Alluvial",
            "landSizeAcres": 4.5,
            "setupCompleted": True
        }
        db.farmers.insert_one(farmer_doc)
        print("   ✅ Created farmer F001")
    else:
        print(f"   ℹ️  Farmers already exist ({db.farmers.count_documents({})} found)")

if __name__ == "__main__":
    print("\n🚀 KisanMitra - Database & API Status Check")
    print("=" * 70)
    
    # Step 1: Check database
    db_active, client = check_database()
    
    # Step 2: Seed data if needed
    if db_active:
        seed_sample_data(client)
    
    # Step 3: Test APIs
    print("\n⚠️  Note: Make sure the FastAPI server is running on port 8000")
    print("   Run: uvicorn Backend.api.main:app --reload")
    
    input("\nPress Enter to test API endpoints...")
    test_api_endpoints(db_active)
    
    print("\n" + "=" * 70)
    print("✅ Status check complete!")
    print("=" * 70)
