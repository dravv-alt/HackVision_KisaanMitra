"""
Farmer Repository - handles farmer profile data
In production: connects to MongoDB
For hackathon: provides mock in-memory data
"""
from typing import Optional
from bson import ObjectId
from ..models import FarmerProfile, Location
from ..constants import SoilType, IrrigationType, Language, FarmerType


class FarmerRepository:
    """Repository for farmer profile operations"""
    
    def __init__(self, db_client=None):
        """Initialize with DB client or mock data"""
        self.db_client = db_client
        self._mock_farmers = self._create_mock_farmers()
    
    def get_farmer(self, farmer_id: str) -> Optional[FarmerProfile]:
        """
        Get farmer profile by ID
        Prioritizes Database if available, falls back to mock data
        
        Args:
            farmer_id: Unique farmer identifier
            
        Returns:
            FarmerProfile if found, None otherwise
        """
        # Try Database first
        if self.db_client:
            try:
                # Handle ObjectId validation
                if ObjectId.is_valid(farmer_id):
                    doc = self.db_client.kisanmitra.farmers.find_one({"_id": ObjectId(farmer_id)})
                    if doc:
                        return self._map_doc_to_profile(doc)
            except Exception as e:
                print(f"DB Fetch Error: {e}")
        
        # Fallback to mock data
        return self._mock_farmers.get(farmer_id)
    
    def _map_doc_to_profile(self, doc: dict) -> FarmerProfile:
        """Map MongoDB document to Domain Model"""
        loc_data = doc.get("location", {})
        
        # Determine Enum values safely
        try:
            soil_enum = SoilType(doc.get("soilType", "Alluvial").title())
        except ValueError:
            soil_enum = SoilType.ALLUVIAL
            
        try:
            # Map DB language code to Enum
            lang_code = doc.get("language", "en")
            lang_map = {"hi": Language.HINDI, "mr": Language.MARATHI, "en": Language.ENGLISH}
            lang_enum = lang_map.get(lang_code, Language.ENGLISH)
        except ValueError:
            lang_enum = Language.ENGLISH

        profile = FarmerProfile(
            farmer_id=str(doc["_id"]),
            language=lang_enum,
            location=Location(
                state=loc_data.get("state", "Unknown"),
                district=loc_data.get("district", "Unknown"),
                village=loc_data.get("village"),
                lat=loc_data.get("lat"),
                lon=loc_data.get("lon")
            ),
            soil_type=soil_enum,
            # Defaulting to TUBE_WELL as DB doesn't have this field yet
            irrigation_type=IrrigationType.TUBE_WELL, 
            land_size_acres=doc.get("landSizeAcres", 0.0)
        )
        
        # Auto-compute farmer type
        profile.farmer_type = profile.compute_farmer_type()
        return profile

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
