"""
Constants and Enums for inventory Management
"""

from enum import Enum


class StorageType(str, Enum):
    """Type of storage facility"""
    HOME = "home"
    WAREHOUSE = "warehouse"
    COLD_STORAGE = "cold_storage"


class StockStage(str, Enum):
    """Current stage of stock item"""
    STORED = "stored"
    DRYING = "drying"
    PACKED = "packed"
    READY_TO_SELL = "ready_to_sell"
    SOLD_PARTIAL = "sold_partial"
    SOLD_COMPLETE = "sold_complete"


class HealthStatus(str, Enum):
    """Health status of stock"""
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"


class inventoryAction(str, Enum):
    """Types of inventory actions"""
    ADD = "add"
    SELL = "sell"
    SPOILAGE = "spoilage"
    TRANSFER = "transfer"
    UPDATE_GRADE = "update_grade"


class QualityGrade(str, Enum):
    """Quality grade of produce"""
    A = "A"
    B = "B"
    C = "C"
    UNKNOWN = "unknown"


class UrgencyLevel(str, Enum):
    """Urgency level for actions"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Language(str, Enum):
    """Supported languages"""
    HINDI = "hi"
    ENGLISH = "en"


# Shelf life in days for different crops (hackathon approximations)
SHELF_LIFE_DAYS = {
    "onion": 30,
    "potato": 60,
    "wheat": 180,
    "rice": 240,
    "tomato": 7,
    "cotton": 365,
    "groundnut": 90,
    "garlic": 45,
    "cabbage": 14,
    "carrot": 21,
    "cauliflower": 10,
    "chilli": 15,
    "coriander": 7,
    "cucumber": 10,
    "eggplant": 12,
    "ginger": 30,
    "maize": 120,
    "mango": 7,
    "mustard": 180,
    "peas": 5,
    "soybean": 150,
    "sugarcane": 14,
    "turmeric": 60,
    "default": 30
}

# Risk threshold constants
SHELF_LIFE_HIGH_RISK_DAYS = 3
SHELF_LIFE_MEDIUM_RISK_DAYS = 7

# Priority scoring weights
PRIORITY_WEIGHT_HEALTH = 100
PRIORITY_WEIGHT_SHELF_LIFE = 50
PRIORITY_WEIGHT_SPOILAGE_RISK = 30
PRIORITY_WEIGHT_MARKET_TREND = 20
