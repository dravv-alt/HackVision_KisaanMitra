"""
Constants and Enums for Collaborative Farming Module
"""

from enum import Enum


class EquipmentType(str, Enum):
    """Types of farming equipment available for rent"""
    TRACTOR = "tractor"
    ROTAVATOR = "rotavator"
    SPRAYER = "sprayer"
    HARVESTER = "harvester"
    PLOW = "plow"
    CULTIVATOR = "cultivator"
    OTHER = "other"


class ListingStatus(str, Enum):
    """Status of an equipment listing"""
    AVAILABLE = "available"
    BOOKED = "booked"
    INACTIVE = "inactive"


class RentalStatus(str, Enum):
    """Workflow status for equipment rental requests"""
    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PoolRequestType(str, Enum):
    """Types of land pooling requests"""
    POOL_LAND = "pool_land"
    SEEK_PARTNER = "seek_partner"


class PoolStatus(str, Enum):
    """Status of a land pooling request"""
    OPEN = "open"
    MATCHED = "matched"
    CLOSED = "closed"


class PoolStage(str, Enum):
    """Specific workflow stages for a pool as seen in UI"""
    FORMATION = "formation"
    AGGREGATION = "aggregation"
    NEGOTIATION = "negotiation"
    LOGISTICS = "logistics"
    PAYMENT = "payment"


class PaymentMethod(str, Enum):
    """Payment methods supported"""
    CASH_ON_DELIVERY = "pay_on_delivery"
    ONLINE = "online"
    CREDIT = "credit"


class UrgencyLevel(str, Enum):
    """Priority levels for reminders and UI"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Language(str, Enum):
    """Supported languages for voice-first output"""
    HINDI = "hi"
    ENGLISH = "en"
