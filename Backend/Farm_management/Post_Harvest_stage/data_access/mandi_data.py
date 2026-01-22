"""
Mandi Data - Market prices and locations
Mock database with realistic price variations
"""

from dataclasses import dataclass
from typing import Dict, List
from datetime import date, timedelta
import random


class DemandLevel(str):
    """Market demand levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class MandiInfo:
    """Market (mandi) information"""
    name: str
    location: tuple  # (lat, lon)
    district: str


@dataclass
class PricePoint:
    """Price at a specific date"""
    date: date
    price_per_kg: float


@dataclass
class MandiPriceData:
    """Price data for a crop at a mandi"""
    mandi_name: str
    crop_name: str
    current_price: float
    price_history: List[PricePoint]  # Last 14 days
    demand_level: str


# Maharashtra mandis database
MANDI_DATABASE: Dict[str, MandiInfo] = {
    "pune": MandiInfo(
        name="Pune Mandi",
        location=(18.5204, 73.8567),
        district="Pune"
    ),
    "mumbai": MandiInfo(
        name="Mumbai Mandi",
        location=(19.0760, 72.8777),
        district="Mumbai"
    ),
    "nashik": MandiInfo(
        name="Nashik Mandi",
        location=(19.9975, 73.7898),
        district="Nashik"
    ),
    "aurangabad": MandiInfo(
        name="Aurangabad Mandi",
        location=(19.8762, 75.3433),
        district="Aurangabad"
    ),
    "kolhapur": MandiInfo(
        name="Kolhapur Mandi",
        location=(16.7050, 74.2433),
        district="Kolhapur"
    ),
}


# Base prices for crops (₹ per kg)
BASE_PRICES = {
    "onion": 40.0,
    "potato": 25.0,
    "tomato": 30.0,
    "wheat": 22.0,
    "rice": 35.0,
    "cotton": 55.0,
    "cabbage": 20.0,
    "carrot": 28.0,
}


def _generate_price_history(base_price: float, trend: str, days: int = 14) -> List[PricePoint]:
    """
    Generate deterministic price history
    
    Args:
        base_price: Starting price
        trend: "rising", "falling", or "stable"
        days: Number of days of history
        
    Returns:
        List of PricePoint objects
    """
    history = []
    today = date.today()
    
    for i in range(days, 0, -1):
        day_date = today - timedelta(days=i)
        
        # Trend component
        if trend == "rising":
            trend_factor = 1.0 + (0.015 * (days - i))  # 1.5% increase per day
        elif trend == "falling":
            trend_factor = 1.0 - (0.012 * (days - i))  # 1.2% decrease per day
        else:  # stable
            trend_factor = 1.0
        
        # Seasonal variation (±3%)
        seasonal = 1.0 + (0.03 * ((i % 7) - 3) / 3)
        
        price = base_price * trend_factor * seasonal
        history.append(PricePoint(date=day_date, price_per_kg=round(price, 2)))
    
    return history


def get_mandi_price(mandi_name: str, crop_name: str) -> MandiPriceData:
    """
    Get current price and history for a crop at a mandi
    
    Args:
        mandi_name: Name of the mandi
        crop_name: Name of the crop
        
    Returns:
        MandiPriceData object
    """
    mandi_key = mandi_name.lower().replace(" mandi", "").strip()
    crop_key = crop_name.lower()
    
    # Get base price
    base_price = BASE_PRICES.get(crop_key, 30.0)
    
    # Mandi-specific variation (±10%)
    mandi_factor = {
        "pune": 1.00,
        "mumbai": 1.08,  # Higher prices in Mumbai
        "nashik": 0.95,
        "aurangabad": 0.92,
        "kolhapur": 0.97,
    }.get(mandi_key, 1.0)
    
    current_price = round(base_price * mandi_factor, 2)
    
    # Determine trend based on crop (simplified)
    if crop_key in ["onion", "wheat"]:
        trend = "rising"
        demand = DemandLevel.HIGH
    elif crop_key in ["tomato", "cotton"]:
        trend = "falling"
        demand = DemandLevel.LOW
    else:
        trend = "stable"
        demand = DemandLevel.MEDIUM
    
    history = _generate_price_history(current_price, trend)
    
    return MandiPriceData(
        mandi_name=MANDI_DATABASE[mandi_key].name,
        crop_name=crop_name,
        current_price=current_price,
        price_history=history,
        demand_level=demand
    )


def get_all_mandis() -> List[MandiInfo]:
    """Get list of all mandis"""
    return list(MANDI_DATABASE.values())


def get_mandi_info(mandi_name: str) -> MandiInfo:
    """Get mandi information by name"""
    return MANDI_DATABASE.get(mandi_name.lower())
