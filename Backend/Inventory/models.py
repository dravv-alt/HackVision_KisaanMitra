"""
Pydantic Models for Inventory Management
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from .constants import (
    StorageType,
    StockStage,
    HealthStatus,
    InventoryAction,
    QualityGrade,
    UrgencyLevel,
    Language
)


class FarmerProfile(BaseModel):
    """Farmer profile information"""
    farmerId: str
    language: Language = Language.HINDI
    state: Optional[str] = None
    district: Optional[str] = None
    pincode: Optional[str] = None


class InventoryItem(BaseModel):
    """Core inventory item model"""
    itemId: str
    farmerId: str
    cropKey: str  # normalized key (lowercase)
    cropName: str  # display name
    quantityKg: float
    qualityGrade: QualityGrade = QualityGrade.UNKNOWN
    storageType: StorageType = StorageType.HOME
    storedAt: datetime
    shelfLifeDays: int
    expectedSellBy: datetime
    stage: StockStage = StockStage.STORED
    healthStatus: HealthStatus = HealthStatus.GOOD
    spoilageRisk: str = "low"  # low/medium/high
    notes: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)


class InventoryLogEntry(BaseModel):
    """Inventory action log entry"""
    logId: str
    farmerId: str
    itemId: str
    action: InventoryAction
    quantityKg: float
    pricePerKg: Optional[float] = None
    notes: Optional[str] = None
    ts: datetime = Field(default_factory=datetime.now)
    createdAt: datetime = Field(default_factory=datetime.now)


class MarketPriceContext(BaseModel):
    """Market price context (optional)"""
    cropKey: str
    mandi: Optional[str] = None
    currentPrice: float
    trend: str = "stable"  # rising/falling/stable
    lastUpdatedAt: datetime = Field(default_factory=datetime.now)


class StockCardOutput(BaseModel):
    """UI-ready stock card output"""
    itemId: str
    cropName: str
    quantityKg: float
    grade: QualityGrade
    storedAt: datetime
    shelfLifeRemainingDays: int
    expectedSellBy: datetime
    stage: StockStage
    healthStatus: HealthStatus
    sellPriorityRank: int
    sellNowRecommendation: bool
    reasons: List[str]
    suggestedNextAction: str
    spoilageRisk: str
    storageType: StorageType


class InventoryModuleOutput(BaseModel):
    """Complete inventory dashboard output"""
    header: str
    language: Language
    speechText: str
    stockCards: List[StockCardOutput]
    totalStockCount: int
    warningCount: int
    criticalCount: int
    detailedReasoning: str
    urgencyLevel: UrgencyLevel
