"""
Equipment Engine for Collaborative Farming
"""

from typing import List, Optional, Dict
from datetime import datetime
import uuid

from ..models import EquipmentListing
from ..constants import EquipmentType, ListingStatus
from ..repositories import EquipmentRepo


class EquipmentEngine:
    """Engine for managing equipment listings and discovery"""
    
    def __init__(self, equipment_repo: EquipmentRepo):
        self.repo = equipment_repo

    def list_available_equipment(
        self, 
        district: Optional[str] = None, 
        equipment_type: Optional[EquipmentType] = None
    ) -> List[EquipmentListing]:
        """Discovery logic for available equipment"""
        filters = {"status": ListingStatus.AVAILABLE}
        
        if district:
            filters["district"] = district
        if equipment_type:
            filters["equipmentType"] = equipment_type
            
        return self.repo.search_listings(filters)

    def create_listing(
        self,
        owner_id: str,
        equipment_type: EquipmentType,
        model_name: str,
        price_per_day: float,
        available_from: datetime,
        available_to: datetime,
        district: str,
        pincode: str,
        condition: str = "Good",
        hp_required: Optional[str] = None
    ) -> EquipmentListing:
        """Logic for creating a new equipment listing"""
        listing = EquipmentListing(
            listingId=str(uuid.uuid4()),
            ownerFarmerId=owner_id,
            equipmentType=equipment_type,
            modelName=model_name,
            pricePerDay=price_per_day,
            availableFrom=available_from,
            availableTo=available_to,
            district=district,
            pincode=pincode,
            condition=condition,
            hpRequired=hp_required,
            status=ListingStatus.AVAILABLE
        )
        return self.repo.create_listing(listing)
