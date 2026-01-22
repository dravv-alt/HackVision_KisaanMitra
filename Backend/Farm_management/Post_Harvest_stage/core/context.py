"""
Farmer Context - Normalized input for decision engine
"""

from dataclasses import dataclass
from datetime import date
from farm_management.post_harvest_stage.utils.time import days_between


@dataclass
class FarmerContext:
    """Input context from farmer"""
    crop_name: str
    quantity_kg: float
    farmer_location: tuple  # (lat, lon)
    harvest_date: date
    today_date: date
    
    def days_since_harvest(self) -> int:
        """Calculate days since harvest"""
        return days_between(self.harvest_date, self.today_date)
    
    def has_immediate_spoilage_risk(self) -> bool:
        """Quick check for immediate spoilage concern"""
        days_elapsed = self.days_since_harvest()
        # If more than 5 days since harvest for perishables, flag it
        return days_elapsed > 5
    
    def __post_init__(self):
        """Validate inputs"""
        if self.quantity_kg <= 0:
            raise ValueError("Quantity must be positive")
        
        if len(self.farmer_location) != 2:
            raise ValueError("Location must be (lat, lon) tuple")
        
        if self.today_date < self.harvest_date:
            raise ValueError("Today cannot be before harvest date")
