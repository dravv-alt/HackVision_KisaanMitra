"""
Seed KisaanMitra Database with Initial Data
Populates farmers, crops_master, equipment_listing, and schemes_master
"""
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import uuid

# Connect to MongoDB
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "KisaanMitra"

print("🔄 Connecting to MongoDB...")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# ============================================================================
# 1. SEED FARMERS
# ============================================================================
print("\n👨‍🌾 Seeding Farmers...")

farmers_data = [
    {
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
        "setupCompleted": True,
        "createdAt": datetime.utcnow()
    },
    {
        "_id": "F002",
        "userId": "U002",
        "language": "hi",
        "location": {
            "state": "Maharashtra",
            "district": "Nashik",
            "village": "Igatpuri",
            "lat": 19.6952,
            "lon": 73.5632
        },
        "soilType": "Black",
        "landSizeAcres": 2.0,
        "setupCompleted": True,
        "createdAt": datetime.utcnow()
    },
    {
        "_id": "F003",
        "userId": "U003",
        "language": "en",
        "location": {
            "state": "Karnataka",
            "district": "Bangalore Rural",
            "village": "Doddaballapur",
            "lat": 13.2257,
            "lon": 77.5465
        },
        "soilType": "Red",
        "landSizeAcres": 8.0,
        "setupCompleted": True,
        "createdAt": datetime.utcnow()
    }
]

for farmer in farmers_data:
    db.farmers.update_one(
        {"_id": farmer["_id"]},
        {"$set": farmer},
        upsert=True
    )
print(f"   ✅ Inserted {len(farmers_data)} farmers")

# ============================================================================
# 2. SEED CROPS MASTER
# ============================================================================
print("\n🌾 Seeding Crops Master...")

crops_data = [
    {
        "cropKey": "wheat",
        "localNames": {"hi": "गेहूं", "en": "Wheat"},
        "suitableSoils": ["Alluvial", "Black", "Loamy"],
        "season": "rabi",
        "maturityDays": 120,
        "waterRequirement": "Moderate",
        "requirements": {
            "avgRainfallMm": 75.0,
            "temperatureRange": {"min": 10, "max": 25}
        },
        "avgYieldPerAcre": 1200.0,
        "marketDemandTrend": "High",
        "commonDiseases": ["Yellow rust", "Aphid attack"]
    },
    {
        "cropKey": "rice",
        "localNames": {"hi": "चावल", "en": "Rice"},
        "suitableSoils": ["Alluvial", "Black", "Clay"],
        "season": "kharif",
        "maturityDays": 120,
        "waterRequirement": "High",
        "requirements": {
            "avgRainfallMm": 175.0,
            "temperatureRange": {"min": 20, "max": 35}
        },
        "avgYieldPerAcre": 1500.0,
        "marketDemandTrend": "Very High",
        "commonDiseases": ["Blast disease", "Brown spot"]
    },
    {
        "cropKey": "cotton",
        "localNames": {"hi": "कपास", "en": "Cotton"},
        "suitableSoils": ["Black", "Alluvial", "Red"],
        "season": "kharif",
        "maturityDays": 165,
        "waterRequirement": "Moderate",
        "requirements": {
            "avgRainfallMm": 100.0,
            "temperatureRange": {"min": 21, "max": 35}
        },
        "avgYieldPerAcre": 800.0,
        "marketDemandTrend": "High",
        "commonDiseases": ["Pink bollworm", "Whitefly"]
    },
    {
        "cropKey": "tomato",
        "localNames": {"hi": "टमाटर", "en": "Tomato"},
        "suitableSoils": ["Loamy", "Sandy", "Red"],
        "season": "rabi",
        "maturityDays": 75,
        "waterRequirement": "Moderate",
        "requirements": {
            "avgRainfallMm": 50.0,
            "temperatureRange": {"min": 15, "max": 30}
        },
        "avgYieldPerAcre": 2500.0,
        "marketDemandTrend": "Very High",
        "commonDiseases": ["Leaf curl virus", "Fruit borer"]
    }
]

for crop in crops_data:
    db.crops_master.update_one(
        {"cropKey": crop["cropKey"]},
        {"$set": crop},
        upsert=True
    )
print(f"   ✅ Inserted {len(crops_data)} crops")

# ============================================================================
# 3. SEED EQUIPMENT LISTINGS
# ============================================================================
print("\n🚜 Seeding Equipment Listings...")

now = datetime.utcnow()
equipment_data = [
    {
        "_id": str(uuid.uuid4()),
        "listingId": str(uuid.uuid4()),
        "ownerFarmerId": "F002",
        "equipmentType": "tractor",
        "modelName": "Mahindra 575 DI",
        "pricePerDay": 800.0,
        "condition": "Excellent",
        "hpRequired": "45-50 HP",
        "isVerified": True,
        "availableFrom": now,
        "availableTo": now + timedelta(days=30),
        "district": "Nashik",
        "pincode": "422002",
        "status": "available",
        "createdAt": now,
        "updatedAt": now
    },
    {
        "_id": str(uuid.uuid4()),
        "listingId": str(uuid.uuid4()),
        "ownerFarmerId": "F003",
        "equipmentType": "rotavator",
        "modelName": "Maschio Gaspardo",
        "pricePerDay": 600.0,
        "condition": "Good",
        "hpRequired": "35-40 HP",
        "isVerified": True,
        "availableFrom": now,
        "availableTo": now + timedelta(days=15),
        "district": "Bangalore Rural",
        "pincode": "561203",
        "status": "available",
        "createdAt": now,
        "updatedAt": now
    }
]

for equipment in equipment_data:
    db.equipment_listing.insert_one(equipment)
print(f"   ✅ Inserted {len(equipment_data)} equipment listings")

# ============================================================================
# 4. SEED SCHEMES MASTER
# ============================================================================
print("\n📋 Seeding Government Schemes...")

schemes_data = [
    {
        "schemeKey": "pmksy",
        "schemeName": "Pradhan Mantri Krishi Sinchayee Yojana",
        "localizedNames": {"hi": "प्रधानमंत्री कृषि सिंचाई योजना"},
        "description": "Irrigation support scheme",
        "benefits": "Subsidy on drip/sprinkler irrigation",
        "eligibilityRules": {
            "minLandSizeAcres": 1.0,
            "soilTypes": [],
            "crops": [],
            "states": []
        },
        "requiredDocuments": ["Land records", "Aadhaar", "Bank details"],
        "deadline": datetime(2025, 12, 31),
        "category": "irrigation",
        "isActive": True
    },
    {
        "schemeKey": "pmfby",
        "schemeName": "Pradhan Mantri Fasal Bima Yojana",
        "localizedNames": {"hi": "प्रधानमंत्री फसल बीमा योजना"},
        "description": "Crop insurance scheme",
        "benefits": "Insurance against crop loss",
        "eligibilityRules": {
            "minLandSizeAcres": 0.0,
            "soilTypes": [],
            "crops": ["wheat", "rice", "cotton"],
            "states": []
        },
        "requiredDocuments": ["Land records", "Crop details"],
        "deadline": None,
        "category": "insurance",
        "isActive": True
    }
]

for scheme in schemes_data:
    db.schemes_master.update_one(
        {"schemeKey": scheme["schemeKey"]},
        {"$set": scheme},
        upsert=True
    )
print(f"   ✅ Inserted {len(schemes_data)} schemes")

# ============================================================================
# VERIFICATION
# ============================================================================
print("\n" + "="*70)
print("📊 DATABASE VERIFICATION")
print("="*70)

collections_to_check = {
    "farmers": "👨‍🌾",
    "crops_master": "🌾",
    "equipment_listing": "🚜",
    "schemes_master": "📋"
}

for collection, emoji in collections_to_check.items():
    count = db[collection].count_documents({})
    print(f"{emoji} {collection}: {count} documents")

print("\n✅ Database seeding complete!")
print("="*70)
