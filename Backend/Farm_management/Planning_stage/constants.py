"""
Constants and enums for Planning Stage
"""
from enum import Enum


class Season(str, Enum):
    """Agricultural seasons in India"""
    KHARIF = "kharif"  # June-October (monsoon)
    RABI = "rabi"  # November-March (winter)
    ZAID = "zaid"  # March-June (summer)
    YEAR_ROUND = "year_round"


class SoilType(str, Enum):
    """Common soil types in India"""
    ALLUVIAL = "alluvial"
    BLACK = "black"
    RED = "red"
    LATERITE = "laterite"
    DESERT = "desert"
    MOUNTAIN = "mountain"
    CLAY = "clay"
    LOAMY = "loamy"
    SANDY = "sandy"


class IrrigationType(str, Enum):
    """Types of irrigation available"""
    RAINFED = "rainfed"
    CANAL = "canal"
    TUBE_WELL = "tube_well"
    DRIP = "drip"
    SPRINKLER = "sprinkler"
    MIXED = "mixed"


class FarmerType(str, Enum):
    """Farmer classification by land size"""
    MARGINAL = "marginal"  # <1 hectare (2.5 acres)
    SMALL = "small"  # 1-2 hectare (2.5-5 acres)
    MEDIUM = "medium"  # 2-10 hectare (5-25 acres)
    LARGE = "large"  # >10 hectare (>25 acres)


class RiskPreference(str, Enum):
    """Risk appetite for crop selection"""
    SAFE = "safe"  # Prioritize low-risk crops
    BALANCED = "balanced"  # Balance profit and risk
    HIGH_PROFIT = "high_profit"  # Prioritize high profit despite risk


class ProfitLevel(str, Enum):
    """Profit potential categories"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class MarketDemand(str, Enum):
    """Market demand levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class Language(str, Enum):
    """Supported languages"""
    HINDI = "hi"
    ENGLISH = "en"


class UrgencyLevel(str, Enum):
    """Urgency levels for actions"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ReminderStatus(str, Enum):
    """Status of reminders"""
    PENDING = "pending"
    SENT = "sent"
    CANCELLED = "cancelled"


# Weather thresholds
WEATHER_THRESHOLDS = {
    "HIGH_TEMP_C": 40,
    "LOW_TEMP_C": 5,
    "HIGH_RAIN_MM_WEEK": 200,
    "LOW_RAIN_MM_WEEK": 10,
    "HIGH_WIND_MPS": 15,
}

# Crop scoring weights
CROP_SCORING_WEIGHTS = {
    "SOIL_MATCH": 30,
    "SEASON_MATCH": 25,
    "RAINFALL_FIT": 15,
    "TEMPERATURE_FIT": 10,
    "IRRIGATION_MATCH": 10,
    "PROFIT_PREFERENCE": 10,
}

# Reminder timing (days before deadline)
REMINDER_DAYS = [15, 7, 1]

# Default weather fallback values (for demo reliability)
DEFAULT_WEATHER = {
    "temperature_c": 28.0,
    "humidity_pct": 65.0,
    "rain_forecast": False,
    "rain_mm_next_7_days": 15.0,
    "wind_speed_mps": 3.5,
    "alerts": ["Using simulated weather data for demo"]
}

# Season date mappings (simplified for India)
SEASON_MONTHS = {
    Season.KHARIF: [6, 7, 8, 9, 10],  # June-October
    Season.RABI: [11, 12, 1, 2, 3],  # November-March
    Season.ZAID: [3, 4, 5, 6],  # March-June
}
