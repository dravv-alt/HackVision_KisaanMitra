"""
Constants and Enums for Government Schemes Module
"""

from enum import Enum


class SchemeCategory(str, Enum):
    """Government scheme categories"""
    SOIL = "soil"
    FERTILIZER = "fertilizer"
    LOAN = "loan"
    SUBSIDY = "subsidy"
    INSURANCE = "insurance"
    TRAINING = "training"
    OTHER = "other"


class Language(str, Enum):
    """Supported languages"""
    HINDI = "hi"
    ENGLISH = "en"


class AlertType(str, Enum):
    """Types of alerts"""
    GOV_SCHEME = "gov_scheme"
    INVENTORY_EXPIRY = "inventory_expiry"
    MARKET_PRICE = "market_price"
    WEATHER = "weather"


class AlertUrgency(str, Enum):
    """Alert urgency levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AlertStatus(str, Enum):
    """Alert status"""
    PENDING = "pending"
    SENT = "sent"
    READ = "read"


# Indian states
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
]

# Scheme category display names
CATEGORY_DISPLAY_NAMES = {
    SchemeCategory.SOIL: {
        "en": "Soil Health",
        "hi": "मृदा स्वास्थ्य"
    },
    SchemeCategory.FERTILIZER: {
        "en": "Fertilizer Subsidy",
        "hi": "उर्वरक सब्सिडी"
    },
    SchemeCategory.LOAN: {
        "en": "Agricultural Loans",
        "hi": "कृषि ऋण"
    },
    SchemeCategory.SUBSIDY: {
        "en": "Subsidies",
        "hi": "सब्सिडी"
    },
    SchemeCategory.INSURANCE: {
        "en": "Crop Insurance",
        "hi": "फसल बीमा"
    },
    SchemeCategory.TRAINING: {
        "en": "Training Programs",
        "hi": "प्रशिक्षण कार्यक्रम"
    },
    SchemeCategory.OTHER: {
        "en": "Other Schemes",
        "hi": "अन्य योजनाएं"
    }
}
