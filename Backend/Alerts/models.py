"""
Pydantic Models for Alerts & Notifications Module
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from .constants import (
    AlertType, AlertUrgency, AlertStatus, 
    DeliveryChannel, PriceTrend, Language
)


class FarmerProfile(BaseModel):
    """Contextual data about the farmer"""
    farmerId: str
    language: Language = Language.HINDI
    state: str
    district: str
    pincode: str
    lat: float
    lon: float
    soilType: Optional[str] = None
    irrigationType: Optional[str] = "manual"
    landSizeAcres: float = 0.0


class FarmerCropContext(BaseModel):
    """Contextual data about a specific crop on a farm"""
    farmerCropId: str
    farmerId: str
    cropKey: str
    cropName: str
    stage: str # preseeding, during_farming, harvest, postharvest
    subStage: Optional[str] = None # vegetative, flowering, etc.
    areaAcres: float


class WeatherContext(BaseModel):
    """Standardized weather data"""
    temperatureC: float
    rainForecastBool: bool
    rainChancePct: float
    rainMmNext3Days: float
    humidityPct: float
    windSpeedMps: float
    alerts: List[str] = [] # heatwave, storm, etc.


class MarketContext(BaseModel):
    """Standardized market price data"""
    cropKey: str
    mandi: str
    currentPrice: float
    prevPrice: float
    changePct: float
    trend: PriceTrend


class SchemeContext(BaseModel):
    """Standardized government scheme data"""
    schemeKey: str
    schemeName: str
    category: str
    stateEligible: List[str]
    createdAt: datetime


class DeliveryInfo(BaseModel):
    """Channels used for delivery"""
    push: bool = True
    inApp: bool = True
    voice: bool = True


class AlertRecord(BaseModel):
    """The core record for a triggered alert"""
    alertId: str
    farmerId: str
    alertType: AlertType
    title: str
    message: str
    urgency: AlertUrgency
    delivery: DeliveryInfo = Field(default_factory=DeliveryInfo)
    related: Dict[str, Any] = {} # { cropKey, schemeKey, mandi, price }
    status: AlertStatus = AlertStatus.PENDING
    scheduledAt: datetime
    sentAt: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=datetime.now)


class AlertsOutput(BaseModel):
    """The aggregate response for the UI and Voice Agent"""
    header: str
    language: Language
    speechText: str
    alerts: List[AlertRecord]
    summaryCounts: Dict[str, int] # { critical, high, medium, low }
    detailedReasoning: str
    urgencyLevel: AlertUrgency
