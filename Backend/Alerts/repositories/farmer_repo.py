"""
Farmer Repository with Mock Fallback
"""

from typing import Dict, Optional
from ..models import FarmerProfile
from ..constants import Language


class FarmerRepo:
    def __init__(self):
        self._mock_farmers: Dict[str, FarmerProfile] = {}
        self._seed_mock_farmer_if_missing()

    def get_farmer(self, farmer_id: str) -> FarmerProfile:
        """Fetch farmer context or return mock fallback if missing"""
        if farmer_id in self._mock_farmers:
            return self._mock_farmers[farmer_id]
        
        # Consistent hackathon fallback: return default if ID not found
        return list(self._mock_farmers.values())[0]

    def _seed_mock_farmer_if_missing(self):
        """Seed mock data for demo persistence"""
        self._mock_farmers["FARMER001"] = FarmerProfile(
            farmerId="FARMER001",
            language=Language.HINDI,
            state="Maharashtra",
            district="Nashik",
            pincode="422001",
            lat=20.0,
            lon=73.7,
            soilType="Black Soil",
            irrigationType="Drip",
            landSizeAcres=5.5
        )
