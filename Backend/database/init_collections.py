import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "KisaanMitra")

def init_db():
    print(f"Connecting to MongoDB at {MONGO_DETAILS}...")
    client = pymongo.MongoClient(MONGO_DETAILS)
    db = client[DB_NAME]
    
    print(f"Initializing database: {DB_NAME}")

    # ==============================
    # 1. Standard Collection Indexes
    # ==============================

    # Users
    try:
        db.users.create_index("phone", unique=True)
        print("✅ Index created: users.phone (Unique)")
    except Exception as e:
        print(f"⚠️ Error creating index for users: {e}")

    # Farmers
    try:
        db.farmers.create_index("userId", unique=True)
        print("✅ Index created: farmers.userId (Unique)")
    except Exception as e:
         print(f"⚠️ Error creating index for farmers: {e}")

    # Crops Master
    try:
        db.crops_master.create_index("cropKey", unique=True)
        print("✅ Index created: crops_master.cropKey (Unique)")
    except Exception as e:
        print(f"⚠️ Error creating index for crops_master: {e}")

    # Schemes Master
    try:
        db.schemes_master.create_index("schemeKey", unique=True)
        db.schemes_master.create_index([("isActive", 1), ("category", 1)])
        print("✅ Index created: schemes_master")
    except Exception as e:
        print(f"⚠️ Error creating index for schemes_master: {e}")

    # Disease Master
    try:
        db.disease_master.create_index("diseaseKey", unique=True)
        print("✅ Index created: disease_master")
    except Exception as e:
        print(f"⚠️ Error creating index for disease_master: {e}")

    # Mandi Masters
    try:
        db.mandi_masters.create_index([("state", 1), ("district", 1)])
        print("✅ Index created: mandi_masters")
    except Exception as e:
        print(f"⚠️ Error creating index for mandi_masters: {e}")

    # Farmer Crops
    try:
        db.farmer_crops.create_index([("farmerId", 1), ("status", 1)])
        print("✅ Index created: farmer_crops")
    except Exception as e:
        print(f"⚠️ Error creating index for farmer_crops: {e}")

    # ==============================
    # 2. Time-Series Collections
    # ==============================
    
    existing_collections = db.list_collection_names()

    ts_collections = [
        {
            "name": "sessions",
            "timeField": "sessionStartTime",
            "metaField": "conversationMeta",
            "granularity": "minutes"
        },
        {
            "name": "cards",
            "timeField": "createdAt",
            "metaField": "cardMeta",
            "granularity": "minutes"
        },
        {
            "name": "crop_stage_logs",
            "timeField": "performedAt",
            "metaField": "eventMeta",
            "granularity": "hours"
        },
        {
            "name": "tasks_calendar",
            "timeField": "dueAt",
            "metaField": "taskMeta",
            "granularity": "hours"
        },
        {
            "name": "inventory_logs",
            "timeField": "ts",
            "metaField": "inventoryMeta",
            "granularity": "hours"
        },
        {
            "name": "finance_transactions",
            "timeField": "ts",
            "metaField": "transactionMeta",
            "granularity": "hours"
        },
        {
            "name": "mandi_prices_cache",
            "timeField": "date",
            "metaField": "marketMeta",
            "granularity": "hours"
        },
        {
            "name": "weather_data",
            "timeField": "ts",
            "metaField": "locationMeta",
            "granularity": "hours",
            "expireAfterSeconds": 7776000 # 90 days
        },
        {
            "name": "alerts_notifications",
            "timeField": "sentAt",
            "metaField": "alertMeta",
            "granularity": "minutes"
        },
        {
            "name": "crop_doctor_reports",
            "timeField": "createdAt",
            "metaField": "scanMeta",
            "granularity": "hours"
        },
        {
            "name": "equipment_rentals",
            "timeField": "startDate",
            "metaField": "rentalMeta",
            "granularity": "hours"
        },
        {
            "name": "scheme_applications",
            "timeField": "applicationDate",
            "metaField": "schemeMeta",
            "granularity": "hours"
        },
        {
            "name": "audit_logs",
            "timeField": "ts",
            "metaField": "auditMeta",
            "granularity": "seconds"
        }
    ]

    for col in ts_collections:
        name = col["name"]
        if name not in existing_collections:
            try:
                ts_options = {
                    "timeField": col["timeField"],
                    "metaField": col["metaField"],
                    "granularity": col["granularity"]
                }
                
                db.create_collection(name, timeseries=ts_options)
                
                if "expireAfterSeconds" in col:
                     db[name].create_index(col["timeField"], expireAfterSeconds=col["expireAfterSeconds"])
                
                print(f"✅ Time-Series Collection created: {name}")
            except Exception as e:
                print(f"⚠️ Error creating {name}: {e}")
        else:
            print(f"ℹ️  Collection {name} already exists. Skipping.")

    print("\nDatabase initialization complete.")

if __name__ == "__main__":
    init_db()
