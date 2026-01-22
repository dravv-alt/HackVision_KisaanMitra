"""
Farmer Repository with Mock Fallback
"""

from typing import Optional
from ..models import FarmerProfile
from ..constants import Language


class FarmerRepo:
    """Repository for farmer data with mock fallback"""
    
    def __init__(self):
        # Mock in-memory storage (simulates DB)
        self._mock_farmers = {}
        self.seed_mock_farmer_if_missing()
    
    def get_farmer(self, farmer_id: str) -> FarmerProfile:
        """
        Get farmer profile by ID
        Falls back to mock data if not found
        """
        if farmer_id in self._mock_farmers:
            return self._mock_farmers[farmer_id]
        
        # Create mock farmer on-the-fly
        mock_farmer = FarmerProfile(
            farmerId=farmer_id,
            language=Language.HINDI,
            state="Maharashtra",
            district="Pune",
            pincode="411001"
        )
        self._mock_farmers[farmer_id] = mock_farmer
        return mock_farmer
    
    def seed_mock_farmer_if_missing(self):
        """Seed mock farmer data for testing"""
        if "FARMER001" not in self._mock_farmers:
            self._mock_farmers["FARMER001"] = FarmerProfile(
                farmerId="FARMER001",
                language=Language.HINDI,
                state="Maharashtra",
                district="Nashik",
                pincode="422001"
            )
        
        if "FARMER002" not in self._mock_farmers:
            self._mock_farmers["FARMER002"] = FarmerProfile(
                farmerId="FARMER002",
                language=Language.ENGLISH,
                state="Punjab",
                district="Ludhiana",
                pincode="141001"
            )
