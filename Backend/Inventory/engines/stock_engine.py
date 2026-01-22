"""
Stock Engine - Core Stock Tracking Logic
"""

from typing import List, Dict
from datetime import datetime

from ..models import inventoryItem, inventoryLogEntry
from ..constants import inventoryAction, StockStage


class StockEngine:
    """Engine for managing stock state and applying inventory actions"""
    
    def build_current_stock_view(
        self, 
        items: List[inventoryItem], 
        logs: List[inventoryLogEntry]
    ) -> List[inventoryItem]:
        """
        Build current stock view by applying logs to items
        
        Args:
            items: Base inventory items
            logs: Action logs to apply
            
        Returns:
            Updated list of inventory items with current state
        """
        # Create a mapping of items by ID for quick lookup
        item_map: Dict[str, inventoryItem] = {item.itemId: item for item in items}
        
        # Sort logs by timestamp (oldest first)
        sorted_logs = sorted(logs, key=lambda x: x.ts)
        
        # Apply each log to update item state
        for log in sorted_logs:
            if log.itemId not in item_map:
                continue
            
            item = item_map[log.itemId]
            
            # Apply quantity changes
            if log.action == inventoryAction.ADD:
                item.quantityKg += log.quantityKg
                item.stage = StockStage.STORED
                
            elif log.action == inventoryAction.SELL:
                item.quantityKg = max(0, item.quantityKg - log.quantityKg)
                
                # Update stage based on remaining quantity
                if item.quantityKg == 0:
                    item.stage = StockStage.SOLD_COMPLETE
                elif item.quantityKg > 0:
                    item.stage = StockStage.SOLD_PARTIAL
                    
            elif log.action == inventoryAction.SPOILAGE:
                item.quantityKg = max(0, item.quantityKg - log.quantityKg)
                item.spoilageRisk = "high"
                
            elif log.action == inventoryAction.TRANSFER:
                # Transfer doesn't change quantity, just location/stage
                item.stage = StockStage.PACKED
                
            elif log.action == inventoryAction.UPDATE_GRADE:
                # Grade update handled separately
                pass
            
            # Update timestamp
            item.updatedAt = log.ts
        
        # Filter out completely sold items (optional - keep for history)
        active_items = [item for item in item_map.values() if item.quantityKg > 0]
        
        return active_items
    
    def calculate_total_value(self, items: List[inventoryItem], prices: Dict[str, float]) -> float:
        """
        Calculate total inventory value
        
        Args:
            items: inventory items
            prices: Price per kg for each crop
            
        Returns:
            Total value in rupees
        """
        total_value = 0.0
        
        for item in items:
            price = prices.get(item.cropKey, 0.0)
            total_value += item.quantityKg * price
        
        return total_value
