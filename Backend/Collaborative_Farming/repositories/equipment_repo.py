"""
Equipment Repository for Collaborative Farming
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import uuid

from ..models import EquipmentListing
from ..constants import EquipmentType, ListingStatus


class EquipmentRepo:
    def __init__(self):
        self._listings: Dict[str, EquipmentListing] = {}
        self.seed_mock_listings_if_empty()

    def create_listing(self, listing: EquipmentListing) -> EquipmentListing:
        """Create a new equipment listing"""
        self._listings[listing.listingId] = listing
        return listing

    def get_listing(self, listing_id: str) -> Optional[EquipmentListing]:
        """Fetch a specific listing"""
        return self._listings.get(listing_id)

    def search_listings(self, filters: Dict) -> List[EquipmentListing]:
        """Search and filter equipment listings"""
        results = list(self._listings.values())
        
        if "district" in filters:
            results = [r for r in results if r.district == filters["district"]]
        
        if "equipmentType" in filters:
            results = [r for r in results if r.equipmentType == filters["equipmentType"]]
            
        if "status" in filters:
            results = [r for r in results if r.status == filters["status"]]
            
        return results

    def update_listing_status(self, listing_id: str, status: ListingStatus):
        """Update listing status"""
        if listing_id in self._listings:
            self._listings[listing_id].status = status
            self._listings[listing_id].updatedAt = datetime.now()

    def seed_mock_listings_if_empty(self):
        """Seed mock listings if repository is empty"""
        if self._listings:
            return
            
        now = datetime.now()
        
        mock_data = [
            EquipmentListing(
                listingId=str(uuid.uuid4()),
                ownerFarmerId="FARMER002",
                equipmentType=EquipmentType.TRACTOR,
                modelName="Mahindra 575 DI Tractor",
                pricePerDay=800.0,
                condition="Excellent",
                hpRequired="45-50 HP",
                isVerified=True,
                availableFrom=now,
                availableTo=now + timedelta(days=30),
                district="Nashik",
                pincode="422002",
                status=ListingStatus.AVAILABLE
            ),
            EquipmentListing(
                listingId=str(uuid.uuid4()),
                ownerFarmerId="FARMER003",
                equipmentType=EquipmentType.ROTAVATOR,
                modelName="Maschio Gaspardo",
                pricePerDay=800.0,
                condition="Good",
                hpRequired="35-40 HP",
                isVerified=True,
                availableFrom=now - timedelta(days=2),
                availableTo=now + timedelta(days=15),
                district="Nashik",
                pincode="422001",
                status=ListingStatus.AVAILABLE
            ),
            EquipmentListing(
                listingId=str(uuid.uuid4()),
                ownerFarmerId="FARMER004",
                equipmentType=EquipmentType.SPRAYER,
                modelName="John Deere Sprayer",
                pricePerDay=500.0,
                availableFrom=now,
                availableTo=now + timedelta(days=10),
                district="Pune",
                pincode="411001",
                status=ListingStatus.AVAILABLE
            )
        ]
        
        for listing in mock_data:
            self._listings[listing.listingId] = listing
