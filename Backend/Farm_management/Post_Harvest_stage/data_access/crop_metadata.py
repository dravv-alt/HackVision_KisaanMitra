"""
Crop Metadata - Shelf life and storage characteristics
Mock database for hackathon demo
"""

from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum


class SpoilageSensitivity(str, Enum):
    """Crop sensitivity to spoilage"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class CropMetadata:
    """Storage and spoilage characteristics for a crop"""
    name: str
    open_storage_days: int  # Shelf life without cold storage
    cold_storage_days: int  # Shelf life with cold storage
    spoilage_sensitivity: SpoilageSensitivity
    optimal_temp_celsius: Optional[float] = None
    humidity_tolerance: str = "medium"


# Mock crop database
CROP_DATABASE: Dict[str, CropMetadata] = {
    "onion": CropMetadata(
        name="Onion",
        open_storage_days=30,
        cold_storage_days=120,
        spoilage_sensitivity=SpoilageSensitivity.LOW,
        optimal_temp_celsius=0.0,
        humidity_tolerance="low"
    ),
    "potato": CropMetadata(
        name="Potato",
        open_storage_days=45,
        cold_storage_days=150,
        spoilage_sensitivity=SpoilageSensitivity.LOW,
        optimal_temp_celsius=4.0,
        humidity_tolerance="medium"
    ),
    "tomato": CropMetadata(
        name="Tomato",
        open_storage_days=7,
        cold_storage_days=21,
        spoilage_sensitivity=SpoilageSensitivity.HIGH,
        optimal_temp_celsius=13.0,
        humidity_tolerance="medium"
    ),
    "wheat": CropMetadata(
        name="Wheat",
        open_storage_days=180,
        cold_storage_days=365,
        spoilage_sensitivity=SpoilageSensitivity.LOW,
        optimal_temp_celsius=20.0,
        humidity_tolerance="low"
    ),
    "rice": CropMetadata(
        name="Rice",
        open_storage_days=150,
        cold_storage_days=365,
        spoilage_sensitivity=SpoilageSensitivity.LOW,
        optimal_temp_celsius=20.0,
        humidity_tolerance="low"
    ),
    "cotton": CropMetadata(
        name="Cotton",
        open_storage_days=120,
        cold_storage_days=365,
        spoilage_sensitivity=SpoilageSensitivity.LOW,
        optimal_temp_celsius=25.0,
        humidity_tolerance="low"
    ),
    "cabbage": CropMetadata(
        name="Cabbage",
        open_storage_days=14,
        cold_storage_days=60,
        spoilage_sensitivity=SpoilageSensitivity.MEDIUM,
        optimal_temp_celsius=0.0,
        humidity_tolerance="high"
    ),
    "carrot": CropMetadata(
        name="Carrot",
        open_storage_days=21,
        cold_storage_days=120,
        spoilage_sensitivity=SpoilageSensitivity.MEDIUM,
        optimal_temp_celsius=0.0,
        humidity_tolerance="high"
    ),
}


def get_crop_metadata(crop_name: str) -> Optional[CropMetadata]:
    """
    Get crop metadata by name (case-insensitive)
    
    Args:
        crop_name: Name of the crop
        
    Returns:
        CropMetadata object or None if crop not found
    """
    return CROP_DATABASE.get(crop_name.lower())


def get_all_crops() -> list[str]:
    """Get list of all supported crop names"""
    return [meta.name for meta in CROP_DATABASE.values()]
