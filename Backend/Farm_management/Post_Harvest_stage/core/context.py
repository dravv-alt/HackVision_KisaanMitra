"""
Farmer Context - Normalized input for decision engine
"""

from dataclasses import dataclass
from datetime import date
from Backend.Farm_management.Post_Harvest_stage.utils.time import days_between


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
        
        # Validate location format
        if not isinstance(self.farmer_location, (list, tuple)) or len(self.farmer_location) != 2:
            raise ValueError(
                "farmer_location must be a list/tuple of [latitude, longitude]. "
                f"Example: [19.9975, 73.7898] for Nasik. Got: {self.farmer_location}"
            )
        
        # Validate location values are numeric
        try:
            lat, lon = float(self.farmer_location[0]), float(self.farmer_location[1])
            if not (-90 <= lat <= 90):
                raise ValueError(f"Latitude must be between -90 and 90. Got: {lat}")
            if not (-180 <= lon <= 180):
                raise ValueError(f"Longitude must be between -180 and 180. Got: {lon}")
        except (ValueError, TypeError) as e:
            raise ValueError(
                f"farmer_location coordinates must be numbers (latitude, longitude). "
                f"Got: {self.farmer_location}. Error: {e}"
            )
        
        if self.today_date < self.harvest_date:
            raise ValueError("Today cannot be before harvest date")
