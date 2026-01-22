"""
Pydantic Models for Government Schemes Module
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from .constants import SchemeCategory, Language, AlertType, AlertUrgency, AlertStatus


class FarmerProfile(BaseModel):
    """Farmer profile information"""
    farmerId: str
    language: Language = Language.HINDI
    state: Optional[str] = None
    district: Optional[str] = None
    pincode: Optional[str] = None


class SchemeRecord(BaseModel):
    """Government scheme record"""
    schemeId: str
    schemeName: str
    schemeNameHindi: Optional[str] = None
    category: SchemeCategory
    description: str
    descriptionHindi: Optional[str] = None
    state: Optional[str] = None  # None means all-India
    district: Optional[str] = None  # None means state-wide
    benefits: str
    benefitsHindi: Optional[str] = None
    eligibility: Optional[str] = None
    eligibilityHindi: Optional[str] = None
    howToApply: Optional[str] = None
    howToApplyHindi: Optional[str] = None
    officialLink: Optional[str] = None
    contactNumber: Optional[str] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    isActive: bool = True
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)


class SchemeCardOutput(BaseModel):
    """UI-ready scheme card"""
    schemeId: str
    schemeName: str
    category: SchemeCategory
    categoryDisplay: str
    description: str
    benefits: str
    eligibility: Optional[str] = None
    howToApply: Optional[str] = None
    officialLink: Optional[str] = None
    contactNumber: Optional[str] = None
    scope: str  # "All India", "State-wide", "District-specific"
    isNew: bool = False  # Newly added scheme
    daysRemaining: Optional[int] = None  # Days until end date


class AlertRecord(BaseModel):
    """Alert notification record"""
    alertId: str
    farmerId: str
    alertType: AlertType
    urgency: AlertUrgency
    status: AlertStatus = AlertStatus.PENDING
    title: str
    titleHindi: Optional[str] = None
    message: str
    messageHindi: Optional[str] = None
    relatedId: Optional[str] = None  # e.g., schemeId
    actionUrl: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.now)
    sentAt: Optional[datetime] = None
    readAt: Optional[datetime] = None


class GovSchemesOutput(BaseModel):
    """Complete government schemes display output"""
    header: str
    language: Language
    speechText: str
    schemeCards: List[SchemeCardOutput]
    totalSchemes: int
    newSchemesCount: int
    filterApplied: dict  # state, district, category
    detailedReasoning: str
