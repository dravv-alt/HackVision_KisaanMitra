"""
Insert comprehensive mock data into MongoDB
Run this script to populate the database with realistic data
"""

import sys
import os
from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

# Import mock data
exec(open('Backend/database/generate_mock_data.py').read())

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "kisanmitra"

def insert_mock_data():
    """Insert all mock data into MongoDB"""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        print("🚀 Starting mock data insertion...")
        print("=" * 60)
        
        # 1. Insert Farmers
        print("\n📊 Inserting Farmers...")
        db.farmers.delete_many({})  # Clear existing
        result = db.farmers.insert_many(farmers_data)
        print(f"✅ Inserted {len(result.inserted_ids)} farmers")
        
        # 2. Insert Crops Master
        print("\n🌾 Inserting Crops Master...")
        db.crops_master.delete_many({})
        result = db.crops_master.insert_many(crops_master_data)
        print(f"✅ Inserted {len(result.inserted_ids)} crops")
        
        # 3. Insert Active Crops
        print("\n🌱 Inserting Active Crops...")
        db.active_crops.delete_many({})
        result = db.active_crops.insert_many(active_crops_data)
        print(f"✅ Inserted {len(result.inserted_ids)} active crops")
        
        # 4. Insert Equipment
        print("\n🚜 Inserting Equipment Listings...")
        db.equipment_listings.delete_many({})
        result = db.equipment_listings.insert_many(equipment_data)
        print(f"✅ Inserted {len(result.inserted_ids)} equipment listings")
        
        # 5. Insert Government Schemes
        print("\n🏛️ Inserting Government Schemes...")
        db.schemes_master.delete_many({})
        result = db.schemes_master.insert_many(schemes_data)
        print(f"✅ Inserted {len(result.inserted_ids)} schemes")
        
        # 6. Insert Financial Transactions
        print("\n💰 Inserting Financial Transactions...")
        db.financial_transactions.delete_many({})
        result = db.financial_transactions.insert_many(financial_data)
        print(f"✅ Inserted {len(result.inserted_ids)} transactions")
        
        # 7. Insert Market Prices
        print("\n📈 Inserting Market Prices...")
        db.market_prices.delete_many({})
        result = db.market_prices.insert_many(market_prices_data)
        print(f"✅ Inserted {len(result.inserted_ids)} market prices")
        
        # 8. Insert Weather Data
        print("\n🌤️ Inserting Weather Data...")
        db.weather_data.delete_many({})
        result = db.weather_data.insert_many(weather_data)
        print(f"✅ Inserted {len(result.inserted_ids)} weather records")
        
        # 9. Insert Alerts
        print("\n🔔 Inserting Alerts...")
        db.alerts.delete_many({})
        result = db.alerts.insert_many(alerts_data)
        print(f"✅ Inserted {len(result.inserted_ids)} alerts")
        
        # 10. Insert Calendar Events
        print("\n📅 Inserting Calendar Events...")
        db.calendar_events.delete_many({})
        result = db.calendar_events.insert_many(calendar_events_data)
        print(f"✅ Inserted {len(result.inserted_ids)} calendar events")
        
        print("\n" + "=" * 60)
        print("🎉 Mock data insertion completed successfully!")
        print("=" * 60)
        
        # Print summary
        print("\n📊 Database Summary:")
        print(f"   Farmers: {db.farmers.count_documents({})}")
        print(f"   Crops Master: {db.crops_master.count_documents({})}")
        print(f"   Active Crops: {db.active_crops.count_documents({})}")
        print(f"   Equipment: {db.equipment_listings.count_documents({})}")
        print(f"   Schemes: {db.schemes_master.count_documents({})}")
        print(f"   Transactions: {db.financial_transactions.count_documents({})}")
        print(f"   Market Prices: {db.market_prices.count_documents({})}")
        print(f"   Weather: {db.weather_data.count_documents({})}")
        print(f"   Alerts: {db.alerts.count_documents({})}")
        print(f"   Calendar Events: {db.calendar_events.count_documents({})}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error inserting mock data: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    insert_mock_data()
