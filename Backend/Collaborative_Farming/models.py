"""
Pydantic Models for Collaborative Farming Module
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from .constants import (
    EquipmentType, ListingStatus, RentalStatus,
    PoolRequestType, PoolStatus, UrgencyLevel, Language,
    PaymentMethod, PoolStage
)


class FarmerProfile(BaseModel):
    """Farmer profile information"""
    farmerId: str
    name: str
    language: Language = Language.HINDI
    state: str
    district: str
    pincode: str
    lat: float
    lon: float


class EquipmentListing(BaseModel):
    """Equipment listing for rental"""
    listingId: str
    ownerFarmerId: str
    equipmentType: EquipmentType
    modelName: str
    pricePerDay: float
    condition: str = "Good" # Excellent, Good, Fair
    hpRequired: Optional[str] = None # e.g. "45-50 HP"
    isVerified: bool = True
    availableFrom: datetime
    availableTo: datetime
    district: str
    pincode: str
    status: ListingStatus = ListingStatus.AVAILABLE
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)


class RentalRequest(BaseModel):
    """Rental request for equipment"""
    rentalId: str
    listingId: str
    renterFarmerId: str
    ownerFarmerId: str
    startDate: datetime
    endDate: datetime
    totalAmount: float
    serviceFee: float = 0.0
    paymentMethod: PaymentMethod = PaymentMethod.CASH_ON_DELIVERY
    status: RentalStatus = RentalStatus.REQUESTED
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)


class LandPoolRequest(BaseModel):
    """Land pooling request"""
    requestId: str
    farmerId: str # creator
    requestType: PoolRequestType
    landSizeAcres: float
    cropPreference: Optional[str] = None
    season: Optional[str] = None
    expectedMembers: Optional[int] = None
    joinedFarmers: List[str] = []
    district: str
    pincode: str
    currentStage: PoolStage = PoolStage.FORMATION
    progressPct: int = 0
    targetPrice: Optional[float] = None
    highestBid: Optional[float] = None
    sellingWindow: Optional[str] = None
    totalQuantity: float = 0.0
    keyBenefit: Optional[str] = None
    status: PoolStatus = PoolStatus.OPEN
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)


class ResidueListing(BaseModel):
    """Crop residue listing for bulk sale"""
    residueId: str
    farmerId: str
    cropType: str
    quantityKg: float
    expectedPricePerKg: float
    district: str
    pincode: str
    status: str = "OPEN" # OPEN/CLOSED
    createdAt: datetime = Field(default_factory=datetime.now)


class ReminderRecord(BaseModel):
    """Reminder for deadlines"""
    farmerId: str
    title: str
    message: str
    reminderDateTime: datetime
    relatedRentalId: Optional[str] = None
    status: str = "pending"


class CollaborativeOutput(BaseModel):
    """Complete output for collaborative farming service"""
    header: str
    language: Language
    speechText: str
    equipmentCards: List[EquipmentListing]
    rentalCards: List[RentalRequest]
    landPoolCards: List[LandPoolRequest]
    residueCards: List[ResidueListing]
    remindersSuggested: List[ReminderRecord]
    detailedReasoning: str
    urgencyLevel: UrgencyLevel
