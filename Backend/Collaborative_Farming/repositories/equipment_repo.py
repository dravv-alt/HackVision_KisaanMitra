"""
Equipment Repository for Collaborative Farming
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import uuid
from bson import ObjectId

from ..models import EquipmentListing
from ..constants import EquipmentType, ListingStatus


class EquipmentRepo:
    def __init__(self, db_client=None):
        self.db_client = db_client
        self._listings: Dict[str, EquipmentListing] = {}
        self.seed_mock_listings_if_empty()

    def create_listing(self, listing: EquipmentListing) -> EquipmentListing:
        """Create a new equipment listing"""
        if self.db_client:
            try:
                doc = listing.dict()
                doc["_id"] = listing.listingId  # Use listingId as _id or generic
                # Store Enums as strings
                doc["equipmentType"] = listing.equipmentType.value
                doc["status"] = listing.status.value
                
                self.db_client.kisanmitra.equipment_listings.insert_one(doc)
                return listing
            except Exception as e:
                print(f"DB Error create_listing: {e}")

        # Fallback to in-memory
        self._listings[listing.listingId] = listing
        return listing

    def get_listing(self, listing_id: str) -> Optional[EquipmentListing]:
        """Fetch a specific listing"""
        if self.db_client:
            try:
                doc = self.db_client.kisanmitra.equipment_listings.find_one({"_id": listing_id})
                if doc:
                    return self._map_doc_to_listing(doc)
            except Exception as e:
                pass
                
        return self._listings.get(listing_id)

    def search_listings(self, filters: Dict) -> List[EquipmentListing]:
        """Search and filter equipment listings"""
        if self.db_client:
            try:
                query = {}
                if "district" in filters:
                    query["district"] = filters["district"]
                if "equipmentType" in filters:
                    query["equipmentType"] = filters["equipmentType"]
                if "status" in filters:
                    query["status"] = filters["status"]
                
                cursor = self.db_client.kisanmitra.equipment_listings.find(query)
                return [self._map_doc_to_listing(doc) for doc in cursor]
            except Exception as e:
                print(f"DB Error search_listings: {e}")

        # Fallback to in-memory
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
        if self.db_client:
            try:
                self.db_client.kisanmitra.equipment_listings.update_one(
                    {"_id": listing_id},
                    {"$set": {"status": status.value, "updatedAt": datetime.now()}}
                )
            except Exception as e:
                pass

        if listing_id in self._listings:
            self._listings[listing_id].status = status
            self._listings[listing_id].updatedAt = datetime.now()

    def _map_doc_to_listing(self, doc: Dict) -> EquipmentListing:
        return EquipmentListing(
            listingId=doc.get("listingId", str(doc.get("_id"))),
            ownerFarmerId=doc.get("ownerFarmerId"),
            equipmentType=EquipmentType(doc.get("equipmentType")),
            modelName=doc.get("modelName"),
            pricePerDay=doc.get("pricePerDay"),
            condition=doc.get("condition"),
            hpRequired=doc.get("hpRequired"),
            isVerified=doc.get("isVerified"),
            availableFrom=doc.get("availableFrom"),
            availableTo=doc.get("availableTo"),
            district=doc.get("district"),
            pincode=doc.get("pincode"),
            status=ListingStatus(doc.get("status")),
            createdAt=doc.get("createdAt"),
            updatedAt=doc.get("updatedAt")
        )

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
