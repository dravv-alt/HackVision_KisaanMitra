"""
Spoilage Risk Calculator
Determines spoilage risk based on crop characteristics and storage duration
"""

from dataclasses import dataclass
from enum import Enum
from Backend.Farm_management.Post_Harvest_stage.data_access import get_crop_metadata, StorageType


class SpoilageRisk(str, Enum):
    """Spoilage risk levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class SpoilageAssessment:
    """Result of spoilage risk calculation"""
    risk_level: SpoilageRisk
    max_safe_storage_days: int
    shelf_life_days: int
    utilization_percent: float
    storage_type_used: str


class SpoilageRiskCalculator:
    """Calculates spoilage risk for crops"""
    
    def calculate_risk(
        self,
        crop_name: str,
        days_to_sell: int,
        storage_type: StorageType = StorageType.OPEN
    ) -> SpoilageAssessment:
        """
        Calculate spoilage risk for given storage duration
        
        Args:
            crop_name: Name of the crop
            days_to_sell: Number of days until planned sale
            storage_type: Type of storage (OPEN or COLD)
            
        Returns:
            SpoilageAssessment object with risk analysis
        """
        # Get crop metadata
        crop_meta = get_crop_metadata(crop_name)
        if not crop_meta:
            # Unknown crop - assume moderate risk
            shelf_life = 30
            risk = SpoilageRisk.MEDIUM
        else:
            # Determine shelf life based on storage type
            if storage_type == StorageType.COLD:
                shelf_life = crop_meta.cold_storage_days
            else:
                shelf_life = crop_meta.open_storage_days
            
            # Calculate utilization
            utilization = days_to_sell / shelf_life if shelf_life > 0 else 1.0
            
            # Determine risk level
            if utilization < 0.5:
                risk = SpoilageRisk.LOW
            elif utilization < 0.8:
                risk = SpoilageRisk.MEDIUM
            else:
                risk = SpoilageRisk.HIGH
        
        # Calculate max safe storage
        max_safe_days = int(shelf_life * 0.8)  # 80% of shelf life is safe
        utilization_pct = (days_to_sell / shelf_life * 100) if shelf_life > 0 else 100
        
        return SpoilageAssessment(
            risk_level=risk,
            max_safe_storage_days=max_safe_days,
            shelf_life_days=shelf_life,
            utilization_percent=round(utilization_pct, 1),
            storage_type_used=storage_type.value
        )
