"""
Health Engine - Stock Health Status Assessment
"""

from ..models import inventoryItem
from ..constants import HealthStatus, StorageType


class HealthEngine:
    """Engine for inferring stock health status"""
    
    def infer_health_status(
        self, 
        item: inventoryItem, 
        remaining_days: int, 
        spoilage_risk: str
    ) -> HealthStatus:
        """
        Infer health status based on multiple factors
        
        Args:
            item: inventory item
            remaining_days: Days until expiry
            spoilage_risk: "low", "medium", or "high"
            
        Returns:
            HealthStatus enum value
        """
        # Critical conditions
        if remaining_days <= 0:
            return HealthStatus.CRITICAL
        
        if spoilage_risk == "high" and remaining_days <= 3:
            return HealthStatus.CRITICAL
        
        # Warning conditions
        if remaining_days <= 7:
            return HealthStatus.WARNING
        
        if spoilage_risk == "high":
            return HealthStatus.WARNING
        
        if spoilage_risk == "medium" and remaining_days <= 14:
            return HealthStatus.WARNING
        
        # Consider storage type
        if item.storageType == StorageType.HOME and remaining_days <= 10:
            # Home storage is less reliable
            return HealthStatus.WARNING
        
        # Default to good
        return HealthStatus.GOOD
    
    def get_health_description(self, health_status: HealthStatus, language: str = "en") -> str:
        """
        Get human-readable health description
        
        Args:
            health_status: Health status enum
            language: "en" or "hi"
            
        Returns:
            Description string
        """
        if language == "hi":
            descriptions = {
                HealthStatus.GOOD: "अच्छी स्थिति",
                HealthStatus.WARNING: "सावधानी - जल्द बेचें",
                HealthStatus.CRITICAL: "खतरनाक - तुरंत बेचें"
            }
        else:
            descriptions = {
                HealthStatus.GOOD: "Good condition",
                HealthStatus.WARNING: "Caution - sell soon",
                HealthStatus.CRITICAL: "Critical - sell immediately"
            }
        
        return descriptions.get(health_status, "Unknown")
