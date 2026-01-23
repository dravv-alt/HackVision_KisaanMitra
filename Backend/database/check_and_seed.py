import asyncio
import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Backend.Collaborative_Farming.repositories.equipment_repo import EquipmentRepo
from Backend.Collaborative_Farming.repositories.farmer_repo import FarmerRepo as CollabFarmerRepo
from Backend.Farm_management.Planning_stage.repositories.farmer_repo import FarmerRepo as PlanningFarmerRepo
from Backend.Farm_management.Planning_stage.repositories.crop_repo import CropRepository

# Load Env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "KisaanMitra")

def check_and_seed():
    print(f"🔄 Connecting to MongoDB at {MONGO_URI}...")
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        print("✅ Database is ACTIVE")
    except Exception as e:
        print(f"❌ Database is INACTIVE or Unreachable: {e}")
        return

    db = client[DB_NAME]

    # Seed Farmers (Planning Repo)
    print("\n🌱 Seeding Farmers...")
    planning_farmer_repo = PlanningFarmerRepo(client)
    count = 0
    for f_id, profile in planning_farmer_repo._mock_farmers.items():
        # Check if exists
        if not db.farmers.find_one({"_id": ObjectId(f_id) if ObjectId.is_valid(f_id) else f_id}):
             # Convert to dict
            doc = profile.dict()
            doc["_id"] = ObjectId(f_id) if ObjectId.is_valid(f_id) else f_id
            # Handle Enums
            doc["language"] = profile.language.value if hasattr(profile.language, "value") else profile.language
            doc["soilType"] = profile.soil_type.value if hasattr(profile.soil_type, "value") else profile.soil_type
            doc["irrigationType"] = profile.irrigation_type.value if hasattr(profile.irrigation_type, "value") else profile.irrigation_type
            if profile.farmer_type:
                 doc["farmerType"] = profile.farmer_type.value if hasattr(profile.farmer_type, "value") else profile.farmer_type
            
            # Location
            doc["location"] = profile.location.dict()

            db.farmers.insert_one(doc)
            count += 1
    print(f"   Saved {count} farmers.")

    # Seed Equipment
    print("\n🚜 Seeding Equipment Listings...")
    equip_repo = EquipmentRepo(client)
    count = 0
    for l_id, listing in equip_repo._listings.items():
        if not db.equipment_listings.find_one({"_id": l_id}):
            doc = listing.dict()
            doc["_id"] = l_id
            doc["equipmentType"] = listing.equipmentType.value
            doc["status"] = listing.status.value
            db.equipment_listings.insert_one(doc)
            count += 1
    print(f"   Saved {count} equipment listings.")

    # Seed Crops (Reference only, usually static)
    print("\n🌾 Seeding Crops Master...")
    crop_repo = CropRepository()
    count = 0
    for crop in crop_repo.list_crops():
        if not db.crops_master.find_one({"cropKey": crop.crop_key}):
            doc = crop.dict()
            # Enums to strings
            doc["seasons"] = [s.value for s in doc["seasons"]]
            doc["suitable_soils"] = [s.value for s in doc["suitable_soils"]]
            doc["irrigation_supported"] = [i.value for i in doc["irrigation_supported"]]
            doc["profit_level"] = doc["profit_level"].value
            doc["market_demand"] = doc["market_demand"].value
            
            db.crops_master.insert_one(doc)
            count += 1
    print(f"   Saved {count} crops.")

    print("\n✅ Seeding Complete!")

if __name__ == "__main__":
    from bson import ObjectId
    check_and_seed()
