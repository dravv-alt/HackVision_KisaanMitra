"""
Pydantic Data Models for Farming Assistant
Provides type-safe schemas for inter-engine communication
"""

from pydantic import BaseModel, Field
from datetime import date
from enum import Enum
from typing import Optional


class CropStage(str, Enum):
    """Enumeration of crop growth stages"""
    SOWING = "sowing"
    GERMINATION = "germination"
    VEGETATIVE = "vegetative"
    FLOWERING = "flowering"
    FRUITING = "fruiting"
    MATURATION = "maturation"
    HARVEST_READY = "harvest_ready"


class PriceTrend(str, Enum):
    """Market price trend indicators"""
    RISING = "rising"
    STABLE = "stable"
    FALLING = "falling"


class DemandLevel(str, Enum):
    """Market demand levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class UrgencyLevel(str, Enum):
    """Advisory urgency levels"""
    INFO = "info"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class CropContext(BaseModel):
    """
    Represents the current state of a crop
    """
    name: str = Field(..., description="Crop name (e.g., 'Tomato', 'Wheat')")
    sowing_date: date = Field(..., description="Date when crop was sown")
    current_stage: CropStage = Field(..., description="Current growth stage")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Tomato",
                "sowing_date": "2024-01-15",
                "current_stage": "flowering"
            }
        }


class EnvironmentalContext(BaseModel):
    """
    Weather and environmental conditions
    """
    temperature: float = Field(..., description="Temperature in Celsius", ge=-10, le=60)
    rain_forecast: bool = Field(..., description="Rain expected in next 24-48 hours")
    humidity: float = Field(..., description="Relative humidity percentage", ge=0, le=100)
    wind_speed: Optional[float] = Field(None, description="Wind speed in km/h", ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "temperature": 28.5,
                "rain_forecast": False,
                "humidity": 65.0,
                "wind_speed": 12.0
            }
        }


class MarketContext(BaseModel):
    """
    Market price and demand information
    """
    crop_name: str = Field(..., description="Name of the crop")
    current_price: float = Field(..., description="Current market price per kg in ₹", ge=0)
    price_trend: PriceTrend = Field(..., description="Price movement trend")
    demand_level: DemandLevel = Field(..., description="Current market demand")
    
    class Config:
        json_schema_extra = {
            "example": {
                "crop_name": "Onion",
                "current_price": 40.0,
                "price_trend": "rising",
                "demand_level": "high"
            }
        }


class AdvisoryOutput(BaseModel):
    """
    Standardized advisory/recommendation output
    """
    action_header: str = Field(..., description="Short action title (e.g., 'STOP IRRIGATION')")
    spoken_advice: str = Field(..., description="Natural language advice for voice output")
    detailed_reasoning: str = Field(..., description="Technical explanation of the recommendation")
    urgency: UrgencyLevel = Field(default=UrgencyLevel.INFO, description="How urgent this action is")
    
    # Optional fields for specific advisory types
    chemical_dosage: Optional[str] = Field(None, description="Exact chemical application instructions")
    safety_warning: Optional[str] = Field(None, description="Safety precautions")
    organic_alternative: Optional[str] = Field(None, description="Low-cost organic option")
    
    class Config:
        json_schema_extra = {
            "example": {
                "action_header": "APPLY FUNGICIDE",
                "spoken_advice": "Your tomato plants show signs of leaf blight. Apply Mancozeb fungicide immediately.",
                "detailed_reasoning": "Leaf blight spreads rapidly in humid conditions. Early treatment prevents crop loss.",
                "urgency": "high",
                "chemical_dosage": "Mancozeb 2g/L water, spray 200mL per square meter",
                "safety_warning": "Do not spray in windy conditions (>15km/h). Wear protective gloves.",
                "organic_alternative": "Neem oil solution: 30mL neem oil per liter of water, spray in early morning"
            }
        }


class DiseaseDetectionResult(BaseModel):
    """
    Result from vision engine disease detection
    """
    disease_name: str = Field(..., description="Identified disease or 'Healthy'")
    confidence: float = Field(..., description="Confidence score 0-1", ge=0, le=1)
    is_mock: bool = Field(default=False, description="Whether this is a fallback mock result")
    
    class Config:
        json_schema_extra = {
            "example": {
                "disease_name": "Leaf Blight",
                "confidence": 0.98,
                "is_mock": False
            }
        }
