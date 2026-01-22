import os
import json
import zipfile
import shutil
from datetime import datetime
from pymongo import MongoClient
from bson import json_util

# Config
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "KisaanMitra"
EXPORT_DIR = "mongo_export_temp"
ZIP_FILENAME = "KisaanMitra_DB_Export.zip"

def export_db():
    print(f"Connecting to {MONGO_URI}...")
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return

    # Create temp directory
    if os.path.exists(EXPORT_DIR):
        shutil.rmtree(EXPORT_DIR)
    os.makedirs(EXPORT_DIR)

    collections = db.list_collection_names()
    print(f"Found collections: {collections}")

    if not collections:
        print("No collections found in database.")
        # Create a dummy file so zip works and user knows it was empty
        with open(os.path.join(EXPORT_DIR, "info.txt"), "w") as f:
            f.write("Database was empty.")
    
    for col_name in collections:
        print(f"Exporting {col_name}...")
        collection = db[col_name]
        cursor = collection.find({})
        
        # Convert to list and use json_util for serialization (handles ObjectID, datetime)
        documents = list(cursor)
        
        file_path = os.path.join(EXPORT_DIR, f"{col_name}.json")
        with open(file_path, "w") as file:
            file.write(json_util.dumps(documents, indent=2))

    # Zip the files
    print(f"Creating zip archive: {ZIP_FILENAME}...")
    with zipfile.ZipFile(ZIP_FILENAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(EXPORT_DIR):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)

    # Cleanup temp dir
    shutil.rmtree(EXPORT_DIR)
    print(f"Export complete: {os.path.abspath(ZIP_FILENAME)}")

if __name__ == "__main__":
    export_db()
