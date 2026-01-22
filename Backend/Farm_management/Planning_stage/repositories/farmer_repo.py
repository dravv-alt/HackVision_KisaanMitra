"""
Farmer Repository - handles farmer profile data
In production: connects to MongoDB
For hackathon: provides mock in-memory data
"""
from typing import Optional
from ..models import FarmerProfile, Location
from ..constants import SoilType, IrrigationType, Language, FarmerType


class FarmerRepository:
    """Repository for farmer profile operations"""
    
    def __init__(self):
        """Initialize with mock data for hackathon"""
        self._mock_farmers = self._create_mock_farmers()
    
    def get_farmer(self, farmer_id: str) -> Optional[FarmerProfile]:
        """
        Get farmer profile by ID
        
        Args:
            farmer_id: Unique farmer identifier
            
        Returns:
            FarmerProfile if found, None otherwise
        """
        return self._mock_farmers.get(farmer_id)
    
    def _create_mock_farmers(self) -> dict:
        """Create mock farmer data for testing"""
        return {
            "F001": FarmerProfile(
                farmer_id="F001",
                language=Language.HINDI,
                location=Location(
                    state="Punjab",
                    district="Ludhiana",
                    village="Jagraon",
                    pincode="142026",
                    lat=30.7850,
                    lon=75.4731
                ),
                soil_type=SoilType.ALLUVIAL,
                irrigation_type=IrrigationType.CANAL,
                land_size_acres=4.5,
                farmer_type=FarmerType.SMALL
            ),
            "F002": FarmerProfile(
                farmer_id="F002",
                language=Language.HINDI,
                location=Location(
                    state="Maharashtra",
                    district="Nashik",
                    village="Igatpuri",
                    pincode="422403",
                    lat=19.6952,
                    lon=73.5632
                ),
                soil_type=SoilType.BLACK,
                irrigation_type=IrrigationType.RAINFED,
                land_size_acres=2.0,
                farmer_type=FarmerType.MARGINAL
            ),
            "F003": FarmerProfile(
                farmer_id="F003",
                language=Language.ENGLISH,
                location=Location(
                    state="Karnataka",
                    district="Bangalore Rural",
                    village="Doddaballapur",
                    pincode="561203",
                    lat=13.2257,
                    lon=77.5465
                ),
                soil_type=SoilType.RED,
                irrigation_type=IrrigationType.DRIP,
                land_size_acres=8.0,
                farmer_type=FarmerType.MEDIUM
            ),
            "F004": FarmerProfile(
                farmer_id="F004",
                language=Language.HINDI,
                location=Location(
                    state="Uttar Pradesh",
                    district="Meerut",
                    village="Sardhana",
                    pincode="250342",
                    lat=29.1450,
                    lon=77.6167
                ),
                soil_type=SoilType.LOAMY,
                irrigation_type=IrrigationType.TUBE_WELL,
                land_size_acres=6.0,
                farmer_type=FarmerType.SMALL
            ),
            "F005": FarmerProfile(
                farmer_id="F005",
                language=Language.HINDI,
                location=Location(
                    state="Rajasthan",
                    district="Jaipur",
                    village="Sanganer",
                    pincode="302029",
                    lat=26.8467,
                    lon=75.8048
                ),
                soil_type=SoilType.SANDY,
                irrigation_type=IrrigationType.SPRINKLER,
                land_size_acres=15.0,
                farmer_type=FarmerType.MEDIUM
            ),
        }
