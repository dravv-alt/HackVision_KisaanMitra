"""
Financial Tracking Constants and Enums
Defines all transaction types, categories, and classification enums
"""

from enum import Enum


class TransactionType(str, Enum):
    """Type of financial transaction"""
    EXPENSE = "EXPENSE"
    INCOME = "INCOME"


class ExpenseCategory(str, Enum):
    """Categories for farm expenses"""
    SEEDS = "SEEDS"
    FERTILIZER = "FERTILIZER"
    PESTICIDE = "PESTICIDE"
    LABOUR = "LABOUR"
    WATER = "WATER"
    ELECTRICITY = "ELECTRICITY"
    TRANSPORT = "TRANSPORT"
    EQUIPMENT = "EQUIPMENT"
    STORAGE = "STORAGE"
    OTHER = "OTHER"


class IncomeCategory(str, Enum):
    """Categories for farm income"""
    SALE = "SALE"
    SUBSIDY = "SUBSIDY"
    INSURANCE_CLAIM = "INSURANCE_CLAIM"
    OTHER = "OTHER"


class SeasonType(str, Enum):
    """Indian agricultural seasons"""
    KHARIF = "KHARIF"  # Monsoon crops (Jun-Oct)
    RABI = "RABI"      # Winter crops (Nov-Mar)
    ZAID = "ZAID"      # Summer crops (Mar-Jun)


class UrgencyLevel(str, Enum):
    """Priority/urgency level for financial insights"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Currency(str, Enum):
    """Supported currencies"""
    INR = "INR"


# Category display names (Hindi and English)
EXPENSE_CATEGORY_NAMES = {
    ExpenseCategory.SEEDS: {"en": "Seeds", "hi": "बीज"},
    ExpenseCategory.FERTILIZER: {"en": "Fertilizer", "hi": "उर्वरक"},
    ExpenseCategory.PESTICIDE: {"en": "Pesticide", "hi": "कीटनाशक"},
    ExpenseCategory.LABOUR: {"en": "Labour", "hi": "मजदूरी"},
    ExpenseCategory.WATER: {"en": "Water", "hi": "पानी"},
    ExpenseCategory.ELECTRICITY: {"en": "Electricity", "hi": "बिजली"},
    ExpenseCategory.TRANSPORT: {"en": "Transport", "hi": "परिवहन"},
    ExpenseCategory.EQUIPMENT: {"en": "Equipment", "hi": "उपकरण"},
    ExpenseCategory.STORAGE: {"en": "Storage", "hi": "भंडारण"},
    ExpenseCategory.OTHER: {"en": "Other", "hi": "अन्य"},
}

INCOME_CATEGORY_NAMES = {
    IncomeCategory.SALE: {"en": "Sale", "hi": "बिक्री"},
    IncomeCategory.SUBSIDY: {"en": "Subsidy", "hi": "सब्सिडी"},
    IncomeCategory.INSURANCE_CLAIM: {"en": "Insurance Claim", "hi": "बीमा दावा"},
    IncomeCategory.OTHER: {"en": "Other", "hi": "अन्य"},
}

SEASON_NAMES = {
    SeasonType.KHARIF: {"en": "Kharif (Monsoon)", "hi": "खरीफ (मानसून)"},
    SeasonType.RABI: {"en": "Rabi (Winter)", "hi": "रबी (सर्दी)"},
    SeasonType.ZAID: {"en": "Zaid (Summer)", "hi": "जायद (गर्मी)"},
}
