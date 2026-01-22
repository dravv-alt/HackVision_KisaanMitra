"""
Pydantic models for Planning Stage backend
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from .constants import (
    Season, SoilType, IrrigationType, FarmerType, 
    RiskPreference, ProfitLevel, MarketDemand, 
    Language, UrgencyLevel, ReminderStatus
)


# ============================================================================
# FARMER & INPUT MODELS
# ============================================================================

class Location(BaseModel):
    """Farmer location details"""
    state: str
    district: str
    village: Optional[str] = None
    pincode: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None


class FarmerProfile(BaseModel):
    """Complete farmer profile"""
    farmer_id: str
    language: Language = Language.HINDI
    location: Location
    soil_type: SoilType
    irrigation_type: IrrigationType
    land_size_acres: float
    farmer_type: Optional[FarmerType] = None

    def compute_farmer_type(self) -> FarmerType:
        """Auto-compute farmer type from land size if not set"""
        if self.farmer_type:
            return self.farmer_type
        
        acres = self.land_size_acres
        if acres < 2.5:
            return FarmerType.MARGINAL
        elif acres < 5:
            return FarmerType.SMALL
        elif acres < 25:
            return FarmerType.MEDIUM
        else:
            return FarmerType.LARGE


class PlanningRequest(BaseModel):
    """Request for pre-seeding planning"""
    farmer_id: str
    season: Optional[Season] = None  # Auto-detect if missing
    risk_preference: RiskPreference = RiskPreference.BALANCED
    budget_level: Optional[str] = None


# ============================================================================
# ENVIRONMENTAL/WEATHER MODELS
# ============================================================================

class EnvironmentalContext(BaseModel):
    """Weather and environmental conditions"""
    temperature_c: float
    humidity_pct: float
    rain_forecast: bool
    rain_mm_next_7_days: float
    wind_speed_mps: float
    alerts: List[str] = Field(default_factory=list)


# ============================================================================
# CROP MODELS
# ============================================================================

class ClimateRange(BaseModel):
    """Temperature and rainfall requirements"""
    temp_min_c: Optional[float] = None
    temp_max_c: Optional[float] = None
    rain_min_mm: Optional[float] = None
    rain_max_mm: Optional[float] = None


class CropRequirements(BaseModel):
    """Crop cultivation requirements"""
    seed_rate_kg_per_acre: Optional[float] = None
    fertilizers: List[str] = Field(default_factory=list)
    water_requirement: Optional[str] = None


class ProcurementSource(BaseModel):
    """Where to get seeds/materials"""
    source_type: str  # e.g., "govt_store", "private_dealer", "online"
    name: str
    contact: Optional[str] = None


class CropRecord(BaseModel):
    """Crop encyclopedia entry"""
    crop_key: str
    crop_name: str
    crop_name_hi: Optional[str] = None
    seasons: List[Season]
    suitable_soils: List[SoilType]
    irrigation_supported: List[IrrigationType]
    climate: ClimateRange
    maturity_days_min: int
    maturity_days_max: int
    profit_level: ProfitLevel
    market_demand: MarketDemand
    risks: List[str] = Field(default_factory=list)
    requirements: CropRequirements
    procurement_sources: List[ProcurementSource] = Field(default_factory=list)


class CropRecommendation(BaseModel):
    """Recommended crop with scoring and reasoning"""
    crop_key: str
    crop_name: str
    crop_name_hi: Optional[str] = None
    score: float = Field(..., ge=0, le=100)
    profit_level: ProfitLevel
    reasons: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    crop_requirements: CropRequirements
    seed_material_sources: List[ProcurementSource] = Field(default_factory=list)
    sowing_window_hint: Optional[str] = None
    next_best_action: Optional[str] = None


# ============================================================================
# SCHEME MODELS
# ============================================================================

class SchemeRecord(BaseModel):
    """Government scheme encyclopedia entry"""
    scheme_key: str
    scheme_name: str
    scheme_name_hi: Optional[str] = None
    description: str
    description_hi: Optional[str] = None
    benefits: List[str]
    benefits_hi: Optional[List[str]] = None
    deadline: Optional[datetime] = None
    docs_required: List[str] = Field(default_factory=list)
    eligibility_rules: Dict[str, Any] = Field(default_factory=dict)
    states_eligible: Optional[List[str]] = None  # None = all India
    crops_eligible: Optional[List[str]] = None  # None = all crops
    apply_url: Optional[str] = None
    csc_applicable: bool = True


class SchemeEligibilityResult(BaseModel):
    """Scheme eligibility check result"""
    scheme_key: str
    scheme_name: str
    scheme_name_hi: Optional[str] = None
    eligible: bool
    why_eligible: List[str] = Field(default_factory=list)
    why_not_eligible: List[str] = Field(default_factory=list)
    deadline_warning: Optional[str] = None
    docs_required: List[str] = Field(default_factory=list)
    next_step: str
    apply_url: Optional[str] = None


# ============================================================================
# REMINDER MODELS
# ============================================================================

class ReminderRecord(BaseModel):
    """Reminder for scheme deadline"""
    farmer_id: str
    scheme_key: str
    scheme_name: str
    reminder_datetime: datetime
    message: str
    message_hi: Optional[str] = None
    status: ReminderStatus = ReminderStatus.PENDING


# ============================================================================
# OUTPUT MODEL (FINAL RESPONSE)
# ============================================================================

class PreSeedingOutput(BaseModel):
    """Complete pre-seeding planning output"""
    header: str
    header_hi: Optional[str] = None
    language: Language
    speech_text: str  # Voice-first output (short, actionable)
    speech_text_hi: Optional[str] = None
    weather_summary: str
    weather_summary_hi: Optional[str] = None
    crop_cards: List[CropRecommendation]
    scheme_cards: List[SchemeEligibilityResult]
    reminders: List[ReminderRecord]
    detailed_reasoning: Optional[str] = None
    urgency_level: UrgencyLevel = UrgencyLevel.MEDIUM
