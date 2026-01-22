"""
Storage Facility Data - Available storage options
Mock database for demonstration
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class StorageType(str, Enum):
    """Types of storage facilities"""
    OPEN = "open"
    COLD = "cold"
    CONTROLLED = "controlled_atmosphere"


@dataclass
class StorageFacility:
    """Storage facility information"""
    id: str
    name: str
    type: StorageType
    location: tuple  # (lat, lon)
    district: str
    capacity_kg: int
    available_capacity_kg: int
    daily_cost_per_kg: float  # ₹ per kg per day
    is_available: bool = True
    

# Mock storage facilities in Maharashtra
STORAGE_FACILITIES: List[StorageFacility] = [
    # Pune district
    StorageFacility(
        id="PUN_COLD_01",
        name="Pune Cold Storage Co-op",
        type=StorageType.COLD,
        location=(18.5204, 73.8567),
        district="Pune",
        capacity_kg=500000,
        available_capacity_kg=300000,
        daily_cost_per_kg=0.50
    ),
    StorageFacility(
        id="PUN_OPEN_01",
        name="Pune Open Warehouse",
        type=StorageType.OPEN,
        location=(18.5600, 73.9100),
        district="Pune",
        capacity_kg=1000000,
        available_capacity_kg=700000,
        daily_cost_per_kg=0.20
    ),
    # Nashik district
    StorageFacility(
        id="NAS_COLD_01",
        name="Nashik Agro Cold Storage",
        type=StorageType.COLD,
        location=(19.9975, 73.7898),
        district="Nashik",
        capacity_kg=300000,
        available_capacity_kg=150000,
        daily_cost_per_kg=0.45
    ),
    StorageFacility(
        id="NAS_OPEN_01",
        name="Nashik Farmers Warehouse",
        type=StorageType.OPEN,
        location=(20.0100, 73.8000),
        district="Nashik",
        capacity_kg=800000,
        available_capacity_kg=500000,
        daily_cost_per_kg=0.18
    ),
    # Mumbai district
    StorageFacility(
        id="MUM_COLD_01",
        name="Mumbai Central Cold Chain",
        type=StorageType.COLD,
        location=(19.0760, 72.8777),
        district="Mumbai",
        capacity_kg=400000,
        available_capacity_kg=200000,
        daily_cost_per_kg=0.60  # Higher cost in Mumbai
    ),
    # Aurangabad district
    StorageFacility(
        id="AUR_OPEN_01",
        name="Aurangabad Storage Hub",
        type=StorageType.OPEN,
        location=(19.8762, 75.3433),
        district="Aurangabad",
        capacity_kg=600000,
        available_capacity_kg=400000,
        daily_cost_per_kg=0.15
    ),
    # Kolhapur district
    StorageFacility(
        id="KOL_COLD_01",
        name="Kolhapur Cold Storage",
        type=StorageType.COLD,
        location=(16.7050, 74.2433),
        district="Kolhapur",
        capacity_kg=250000,
        available_capacity_kg=100000,
        daily_cost_per_kg=0.48
    ),
]


def get_all_storage_facilities() -> List[StorageFacility]:
    """Get all storage facilities"""
    return STORAGE_FACILITIES


def get_storage_by_type(storage_type: StorageType) -> List[StorageFacility]:
    """
    Get facilities by type
    
    Args:
        storage_type: Type of storage (OPEN or COLD)
        
    Returns:
        List of matching facilities
    """
    return [f for f in STORAGE_FACILITIES if f.type == storage_type and f.is_available]


def get_storage_by_location(lat: float, lon: float, max_distance_km: float = 50) -> List[StorageFacility]:
    """
    Get nearby storage facilities
    
    Args:
        lat: Farmer latitude
        lon: Farmer longitude
        max_distance_km: Maximum acceptable distance
        
    Returns:
        List of nearby facilities
    """
    from ..utils.geo import haversine_distance
    
    nearby = []
    for facility in STORAGE_FACILITIES:
        if not facility.is_available:
            continue
        
        distance = haversine_distance(lat, lon, facility.location[0], facility.location[1])
        if distance <= max_distance_km:
            nearby.append(facility)
    
    return nearby


def get_storage_by_capacity(min_capacity_kg: int) -> List[StorageFacility]:
    """
    Get facilities with sufficient available capacity
    
    Args:
        min_capacity_kg: Minimum required capacity
        
    Returns:
        List of facilities with enough space
    """
    return [
        f for f in STORAGE_FACILITIES 
        if f.available_capacity_kg >= min_capacity_kg and f.is_available
    ]
