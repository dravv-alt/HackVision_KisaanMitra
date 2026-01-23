"""
Farmer Repository for Collaborative Farming
"""

from typing import Dict, Optional
from bson import ObjectId
from ..models import FarmerProfile
from ..constants import Language


class FarmerRepo:
    def __init__(self, db_client=None):
        self.db_client = db_client
        self._mock_farmers: Dict[str, FarmerProfile] = {}
        self.seed_mock_farmer_if_missing()

    def get_farmer(self, farmer_id: str) -> FarmerProfile:
        """Fetch farmer profile or return mock fallback"""
        
        # Try Database
        if self.db_client:
            try:
                if ObjectId.is_valid(farmer_id):
                    doc = self.db_client.kisanmitra.farmers.find_one({"_id": ObjectId(farmer_id)})
                    if doc:
                        return self._map_doc_to_profile(doc)
            except Exception as e:
                # Log error if needed
                pass

        # Fallback to mock
        if farmer_id in self._mock_farmers:
            return self._mock_farmers[farmer_id]
        
        # Fallback for demo
        return self._mock_farmers.get("FARMER001")
    
    def _map_doc_to_profile(self, doc: dict) -> FarmerProfile:
        loc = doc.get("location", {})
        
        # Parse Language
        lang_str = doc.get("language", "en")
        try:
            if lang_str == "hi": language = Language.HINDI
            elif lang_str == "mr": language = Language.MARATHI
            else: language = Language.ENGLISH
        except:
             language = Language.ENGLISH

        return FarmerProfile(
            farmerId=str(doc.get("_id")),
            name="Farmer", # DB doesn't have name yet
            language=language,
            state=loc.get("state", "Unknown"),
            district=loc.get("district", "Unknown"),
            pincode="000000", # DB doesn't have pincode yet
            lat=loc.get("lat", 0.0),
            lon=loc.get("lon", 0.0)
        )

    def seed_mock_farmer_if_missing(self):
        """Seed mock farmers for demo stability"""
        if "FARMER001" not in self._mock_farmers:
            self._mock_farmers["FARMER001"] = FarmerProfile(
                farmerId="FARMER001",
                name="Rajesh Kumar",
                language=Language.HINDI,
                state="Maharashtra",
                district="Nashik",
                pincode="422001",
                lat=20.0,
                lon=73.7
            )
        if "FARMER002" not in self._mock_farmers:
            self._mock_farmers["FARMER002"] = FarmerProfile(
                farmerId="FARMER002",
                name="Amit Singh",
                language=Language.ENGLISH,
                state="Maharashtra",
                district="Nashik",
                pincode="422002",
                lat=20.1,
                lon=73.8
            )
