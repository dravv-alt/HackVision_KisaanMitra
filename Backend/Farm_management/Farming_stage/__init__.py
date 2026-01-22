"""
Farming Stage Module - Voice-First Farming Assistant Core Logic
Provides crop management decision engines with robust fallback mechanisms
"""

from .models import (
    CropContext,
    CropStage,
    EnvironmentalContext,
    MarketContext,
    PriceTrend,
    DemandLevel,
    AdvisoryOutput,
    UrgencyLevel,
    DiseaseDetectionResult
)

from .engines import (
    WeatherEngine,
    MarketEngine,
    VisionEngine,
    KnowledgeEngine
)

__all__ = [
    # Models
    "CropContext",
    "CropStage",
    "EnvironmentalContext",
    "MarketContext",
    "PriceTrend",
    "DemandLevel",
    "AdvisoryOutput",
    "UrgencyLevel",
    "DiseaseDetectionResult",
    # Engines
    "WeatherEngine",
    "MarketEngine",
    "VisionEngine",
    "KnowledgeEngine",
]
