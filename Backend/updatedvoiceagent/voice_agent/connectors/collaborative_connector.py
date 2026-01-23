"""
Collaborative Farming Connector
Bridges voice agent with collaborative farming backend module
"""

import sys
from pathlib import Path

# Add Backend to path for imports
backend_dir = Path(__file__).resolve().parent.parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from typing import Dict, Any, List
from datetime import datetime, timedelta
from collaborative_farming.service import CollaborativeFarmingService
from collaborative_farming.constants import EquipmentType, PoolRequestType


class CollaborativeFarmingConnector:
    """Connector for collaborative farming module"""
    
    def __init__(self):
        self.service = CollaborativeFarmingService()
    
    def get_marketplace(self, farmer_id: str, language: str = "hi") -> Dict[str, Any]:
        """Get marketplace view"""
        output = self.service.run_marketplace_view(farmer_id, language=language)
        
        return {
            "speech_text": output.speechText,
            "equipment_cards": output.equipmentCards,
            "land_pool_cards": output.landPoolCards,
            "rental_cards": output.rentalCards,
            "residue_cards": output.residueCards,
            "reminders": output.remindersSuggested,
            "urgency": output.urgencyLevel,
            "reasoning": output.detailedReasoning
        }
    
    def request_equipment(
        self,
        farmer_id: str,
        equipment_type: str,
        days_from_now: int = 7,
        duration_days: int = 2
    ) -> Dict[str, Any]:
        """Find and request equipment rental"""
        # Get marketplace
        marketplace = self.service.run_marketplace_view(farmer_id)
        
        # Find matching equipment
        matching = [
            eq for eq in marketplace.equipmentCards
            if eq.equipmentType.upper() == equipment_type.upper()
        ]
        
        if not matching:
            return {
                "success": False,
                "message": f"No {equipment_type} available nearby",
                "equipment": None
            }
        
        # Request rental for first match
        listing = matching[0]
        start_date = datetime.now() + timedelta(days=days_from_now)
        end_date = start_date + timedelta(days=duration_days)
        
        rental = self.service.request_equipment_rental(
            farmer_id,
            listing.listingId,
            start_date,
            end_date
        )
        
        return {
            "success": True,
            "rental_id": rental.rentalId,
            "equipment": listing.modelName,
            "price": listing.pricePerDay,
            "status": rental.status,
            "message": f"Rental request created for {listing.modelName}"
        }
    
    def create_land_pool(
        self,
        farmer_id: str,
        request_type: str,
        land_size: float,
        crop: str
    ) -> Dict[str, Any]:
        """Create land pooling request"""
        try:
            pool_type = PoolRequestType(request_type.lower())
        except ValueError:
            pool_type = PoolRequestType.SEEK_PARTNER
        
        pool = self.service.create_land_pool_request(
            farmer_id,
            pool_type,
            land_size,
            crop
        )
        
        return {
            "success": True,
            "request_id": pool.requestId,
            "message": f"Land pool request created for {land_size} acres"
        }


# Singleton
_connector = None

def get_collaborative_connector() -> CollaborativeFarmingConnector:
    """Get or create collaborative farming connector"""
    global _connector
    if _connector is None:
        _connector = CollaborativeFarmingConnector()
    return _connector
