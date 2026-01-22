"""
Constants and Enums for Alerts & Notifications Management
"""

from enum import Enum


class AlertType(str, Enum):
    """Categories of alerts"""
    WEATHER = "weather"
    IRRIGATION = "irrigation"
    GOV_SCHEME = "gov_scheme"
    PRICE = "price"


class AlertUrgency(str, Enum):
    """Priority levels for ranking"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, Enum):
    """Life cycle of an alert record"""
    PENDING = "pending"
    SENT = "sent"
    READ = "read"
    CANCELLED = "cancelled"


class DeliveryChannel(str, Enum):
    """How the alert is delivered"""
    PUSH = "push"
    IN_APP = "in_app"
    VOICE = "voice"


class PriceTrend(str, Enum):
    """Market price movement trends"""
    RISING = "rising"
    FALLING = "falling"
    STABLE = "stable"
    VOLATILE = "volatile"


class Language(str, Enum):
    """Supported languages"""
    HINDI = "hi"
    ENGLISH = "en"
