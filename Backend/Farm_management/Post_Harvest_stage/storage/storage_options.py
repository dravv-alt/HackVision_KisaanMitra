"""
Storage Options Matcher
Finds suitable storage facilities for farmer's needs
"""

from dataclasses import dataclass
from typing import List, Optional
from data_access import StorageFacility, get_storage_by_location, get_storage_by_capacity, StorageType
from utils import haversine_distance


@dataclass
class StorageOption:
    """Matched storage facility with calculated details"""
    facility: StorageFacility
    distance_km: float
    total_cost_for_period: float  # Total storage cost for specified days
    
    def __lt__(self, other):
        """For sorting by total cost"""
        return self.total_cost_for_period < other.total_cost_for_period


class StorageMatcher:
    """Matches farmers with suitable storage facilities"""
    
    def find_available_storage(
        self,
        farmer_location: tuple,
        crop_name: str,
        quantity_kg: float,
        storage_type: StorageType,
        days_needed: int,
        max_distance_km: float = 50
    ) -> List[StorageOption]:
        """
        Find available storage facilities
        
        Args:
            farmer_location: (lat, lon) tuple
            crop_name: Name of crop (for capacity check)
            quantity_kg: Quantity to store
            storage_type: Required storage type
            days_needed: Number of days to store
            max_distance_km: Maximum acceptable distance
            
        Returns:
            List of StorageOption objects, sorted by total cost
        """
        farmer_lat, farmer_lon = farmer_location
        
        # Get nearby facilities
        nearby_facilities = get_storage_by_location(farmer_lat, farmer_lon, max_distance_km)
        
        # Filter by type and capacity
        suitable = []
        for facility in nearby_facilities:
            if facility.type != storage_type:
                continue
            
            if facility.available_capacity_kg < quantity_kg:
                continue
            
            # Calculate distance
            distance = haversine_distance(
                farmer_lat, farmer_lon,
                facility.location[0], facility.location[1]
            )
            
            # Calculate total cost
            total_cost = facility.daily_cost_per_kg * quantity_kg * days_needed
            
            suitable.append(StorageOption(
                facility=facility,
                distance_km=distance,
                total_cost_for_period=total_cost
            ))
        
        # Sort by total cost (cheapest first)
        suitable.sort()
        
        return suitable
    
    def get_best_storage(
        self,
        farmer_location: tuple,
        crop_name: str,
        quantity_kg: float,
        storage_type: StorageType,
        days_needed: int
    ) -> Optional[StorageOption]:
        """
        Get the best storage option (lowest total cost)
        
        Returns:
            Best StorageOption or None if no storage available
        """
        options = self.find_available_storage(
            farmer_location,
            crop_name,
            quantity_kg,
            storage_type,
            days_needed
        )
        
        return options[0] if options else None
