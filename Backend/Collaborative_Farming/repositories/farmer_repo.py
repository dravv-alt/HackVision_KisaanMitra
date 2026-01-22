"""
Farmer Repository for Collaborative Farming
"""

from typing import Dict, Optional
from ..models import FarmerProfile
from ..constants import Language


class FarmerRepo:
    def __init__(self):
        self._mock_farmers: Dict[str, FarmerProfile] = {}
        self.seed_mock_farmer_if_missing()

    def get_farmer(self, farmer_id: str) -> FarmerProfile:
        """Fetch farmer profile or return mock fallback"""
        if farmer_id in self._mock_farmers:
            return self._mock_farmers[farmer_id]
        
        # Fallback for demo
        return self._mock_farmers.get("FARMER001")

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
