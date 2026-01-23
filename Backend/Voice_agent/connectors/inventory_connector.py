"""
Inventory Management Connector
Bridges voice agent with inventory backend module
"""

import sys
from pathlib import Path

# Add Backend to path for imports
backend_dir = Path(__file__).resolve().parent.parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from typing import Dict, Any, List


class InventoryConnector:
    """Connector for inventory module"""
    
    def __init__(self):
        # Import here to handle structure variations
        try:
            from Backend.Inventory.service import InventoryService
            self.service = InventoryService()
        except ImportError:
            print("⚠️  Inventory service not available")
            self.service = None
    
    def get_dashboard(self, farmer_id: str, language: str = "hi") -> Dict[str, Any]:
        """Get inventory dashboard"""
        if not self.service:
            return {
                "error": "Service not available",
                "speech_text": "Inventory service is not available"
            }
        
        output = self.service.get_inventory_dashboard(farmer_id, language=language)
        
        return {
            "speech_text": output.speechText,
            "stock_cards": output.stockCards,
            "total_items": output.totalStockCount,
            "warning_count": output.warningCount,
            "critical_count": output.criticalCount,
            "urgency": output.urgencyLevel,
            "reasoning": output.detailedReasoning
        }
    
    def get_sell_recommendations(self, farmer_id: str) -> List[Dict]:
        """Get items to sell now"""
        if not self.service:
            return []
        
        dashboard = self.service.get_inventory_dashboard(farmer_id)
        
        # Filter cards with sell recommendation
        to_sell = [
            {
                "crop": card.cropName,
                "quantity": card.quantityKg,
                "priority": card.sellPriorityRank,
                "reasons": card.reasons
            }
            for card in dashboard.stockCards
            if card.sellNowRecommendation
        ]
        
        return to_sell


# Singleton
_connector = None

def get_inventory_connector() -> InventoryConnector:
    """Get or create inventory connector"""
    global _connector
    if _connector is None:
        _connector = InventoryConnector()
    return _connector
