"""
Shelf Life Engine - Shelf Life Countdown and Expiry Risk
"""

from datetime import datetime
from typing import Dict

from ..models import InventoryItem
from ..constants import SHELF_LIFE_HIGH_RISK_DAYS, SHELF_LIFE_MEDIUM_RISK_DAYS


class ShelfLifeEngine:
    """Engine for computing shelf life and expiry risk"""
    
    def compute_shelf_life(self, item: InventoryItem, now: datetime) -> Dict[str, any]:
        """
        Compute shelf life information for an item
        
        Args:
            item: Inventory item
            now: Current datetime
            
        Returns:
            Dictionary with shelf life metadata:
            - remainingDays: Days until expiry
            - expiryRiskLevel: "low", "medium", or "high"
            - isExpired: Boolean
            - daysStored: Days since storage
        """
        # Calculate days stored
        days_stored = (now - item.storedAt).days
        
        # Calculate remaining days until expected sell by date
        remaining_days = (item.expectedSellBy - now).days
        
        # Determine expiry risk level
        if remaining_days <= 0:
            expiry_risk_level = "high"
            is_expired = True
        elif remaining_days <= SHELF_LIFE_HIGH_RISK_DAYS:
            expiry_risk_level = "high"
            is_expired = False
        elif remaining_days <= SHELF_LIFE_MEDIUM_RISK_DAYS:
            expiry_risk_level = "medium"
            is_expired = False
        else:
            expiry_risk_level = "low"
            is_expired = False
        
        # Calculate percentage of shelf life used
        shelf_life_used_percent = (days_stored / item.shelfLifeDays) * 100 if item.shelfLifeDays > 0 else 0
        
        return {
            "remainingDays": remaining_days,
            "expiryRiskLevel": expiry_risk_level,
            "isExpired": is_expired,
            "daysStored": days_stored,
            "shelfLifeUsedPercent": min(100, shelf_life_used_percent)
        }
    
    def get_urgency_message(self, remaining_days: int, language: str = "en") -> str:
        """
        Get urgency message based on remaining days
        
        Args:
            remaining_days: Days until expiry
            language: "en" or "hi"
            
        Returns:
            Urgency message string
        """
        if language == "hi":
            if remaining_days <= 0:
                return "समाप्त हो गया! तुरंत बेचें या उपयोग करें"
            elif remaining_days <= 3:
                return f"केवल {remaining_days} दिन बचे! जल्दी बेचें"
            elif remaining_days <= 7:
                return f"{remaining_days} दिन बचे, जल्द बेचें"
            else:
                return f"{remaining_days} दिन बचे"
        else:
            if remaining_days <= 0:
                return "Expired! Sell or use immediately"
            elif remaining_days <= 3:
                return f"Only {remaining_days} days left! Sell urgently"
            elif remaining_days <= 7:
                return f"{remaining_days} days left, sell soon"
            else:
                return f"{remaining_days} days remaining"
