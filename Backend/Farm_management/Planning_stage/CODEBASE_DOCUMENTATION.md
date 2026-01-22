# Planning Stage - Codebase Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Module Structure](#module-structure)
4. [Core Components](#core-components)
5. [Data Models](#data-models)
6. [Business Logic Engines](#business-logic-engines)
7. [Data Access Layer](#data-access-layer)
8. [Usage Patterns](#usage-patterns)
9. [Integration Guide](#integration-guide)
10. [Extension Points](#extension-points)

---

## Overview

### Purpose
The **Planning Stage** module is a production-ready backend system for the pre-seeding phase of farming. It provides intelligent crop recommendations, government scheme eligibility checking, and automated reminder management for Indian farmers through a voice-first interface.

### Key Capabilities
- **Smart Crop Selection**: Multi-factor scoring algorithm considering soil, season, weather, irrigation, and profit potential
- **Government Scheme Support**: Comprehensive database of 8+ schemes with personalized eligibility checking
- **Reminder Engine**: Automated deadline reminders with multilingual support
- **Weather Integration**: OpenWeather API with graceful fallback to mock data
- **Voice-First Output**: Concise, multilingual speech text optimized for voice assistants

### Technology Stack
- **Language**: Python 3.8+
- **Data Validation**: Pydantic
- **External APIs**: OpenWeather API (optional)
- **Architecture**: Repository Pattern + Service Layer + Engine Pattern

---

## Architecture

### Design Patterns

#### 1. **Repository Pattern**
Clean separation between data access and business logic. All data operations go through repository interfaces.

```python
# Repositories provide data access abstraction
farmer_repo.get_farmer(farmer_id)  # Can be MongoDB, PostgreSQL, or mock
crop_repo.list_crops()
scheme_repo.list_schemes()
```

#### 2. **Service Layer Pattern**
Single entry point (`PreSeedingService`) orchestrates all operations.

```python
service = PreSeedingService()
output = service.run(request)  # Coordinates all engines and repos
```

#### 3. **Engine Pattern**
Modular, testable business logic components with single responsibilities.

```
WeatherEngine → Weather data fetching
CropRecommendationEngine → Crop scoring
SchemeEngine → Eligibility checking
ReminderEngine → Reminder generation
ResponseBuilder → Output formatting
```

### Data Flow

```
┌─────────────────┐
│ PlanningRequest │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ PreSeedingService   │
└────────┬────────────┘
         │
         ├──► FarmerRepository ──► Get farmer profile
         │
         ├──► WeatherEngine ──► Fetch weather context
         │
         ├──► CropRepository + CropRecommendationEngine
         │    └──► Score and rank crops
         │
         ├──► SchemeRepository + SchemeEngine
         │    └──► Check eligibility for schemes
         │
         ├──► ReminderEngine
         │    └──► Generate deadline reminders
         │
         └──► ResponseBuilder
              └──► Format voice-first output
                   │
                   ▼
              ┌────────────────┐
              │ PreSeedingOutput│
              └────────────────┘
```

---

## Module Structure

```
Planning_stage/
├── __init__.py                 # Public API exports
├── constants.py                # Enums, configuration, scoring weights
├── models.py                   # Pydantic data models (DTOs)
├── service.py                  # Main orchestration service
│
├── crop_selection.py           # Simplified crop recommendation wrapper
├── gov_scheme_suggestor.py     # Scheme suggestion wrapper
│
├── cli_demo.py                 # Interactive CLI demonstration
├── test_runner.py              # Automated test suite
│
├── repositories/               # Data Access Layer
│   ├── __init__.py
│   ├── farmer_repo.py          # Farmer profile access (5 mock farmers)
│   ├── crop_repo.py            # Crop encyclopedia (10+ crops)
│   ├── scheme_repo.py          # Government scheme database (8+ schemes)
│   └── reminder_repo.py        # Reminder persistence
│
└── engines/                    # Business Logic Layer
    ├── __init__.py
    ├── weather_engine.py       # Weather API + fallback
    ├── crop_recommendation.py  # Crop scoring algorithm
    ├── scheme_engine.py        # Eligibility checker
    ├── reminder_engine.py      # Reminder generator
    └── response_builder.py     # Voice output formatter
```

---

## Core Components

### 1. PreSeedingService (service.py)

**Purpose**: Main orchestration layer that coordinates all operations.

**Key Methods**:
```python
def run(self, request: PlanningRequest) -> PreSeedingOutput:
    """
    Execute complete pre-seeding planning workflow
    
    Steps:
    1. Get farmer profile
    2. Determine season (auto-detect if not provided)
    3. Fetch weather context
    4. Generate crop recommendations
    5. Check scheme eligibility
    6. Generate reminders
    7. Build voice-first output
    """
```

**Initialization**:
```python
service = PreSeedingService(
    farmer_repo=None,      # Optional: provide custom repository
    crop_repo=None,        # Optional: provide custom repository
    scheme_repo=None,      # Optional: provide custom repository
    reminder_repo=None,    # Optional: provide custom repository
    weather_api_key=None   # Optional: OpenWeather API key
)
```

**Usage Example**:
```python
from Backend.Farm_management.Planning_stage import PreSeedingService, PlanningRequest

service = PreSeedingService()
request = PlanningRequest(
    farmer_id="F001",
    season=None,  # Auto-detect
    risk_preference="balanced"
)
output = service.run(request)
```

---

## Data Models

### Input Models

#### PlanningRequest
```python
@dataclass
class PlanningRequest:
    farmer_id: str                          # Required: Farmer identifier
    season: Optional[Season] = None         # Optional: Auto-detected if None
    risk_preference: str = "balanced"       # "safe" | "balanced" | "high_profit"
```

### Output Models

#### PreSeedingOutput
```python
@dataclass
class PreSeedingOutput:
    header: str                             # Report title
    language: Language                      # Language preference
    speech_text: str                        # Voice assistant output
    weather_summary: str                    # Weather context summary
    crop_cards: List[CropCard]             # Ranked crop recommendations
    scheme_cards: List[SchemeCard]         # Scheme eligibility results
    reminders: List[ReminderRecord]        # Generated reminders
    urgency_level: UrgencyLevel            # Overall urgency
```

#### CropCard
```python
@dataclass
class CropCard:
    crop_name: str                          # Crop name (English)
    crop_name_hindi: str                    # Crop name (Hindi)
    score: float                            # 0-100 suitability score
    profit_level: ProfitLevel              # low | medium | high
    reasons: List[str]                      # Why recommended
    risks: List[str]                        # Potential risks
    crop_requirements: CropRequirements    # Detailed requirements
    next_best_action: str                   # Next step for farmer
```

#### SchemeCard
```python
@dataclass
class SchemeCard:
    scheme_name: str                        # Scheme name
    scheme_name_hindi: str                  # Scheme name (Hindi)
    eligible: bool                          # Eligibility status
    why_eligible: List[str]                # Eligibility reasons
    why_not_eligible: List[str]            # Ineligibility reasons
    deadline_warning: Optional[str]        # Urgency warning
    docs_required: List[str]               # Required documents
    next_step: str                          # Application guidance
```

---

## Business Logic Engines

### 1. CropRecommendationEngine (engines/crop_recommendation.py)

**Purpose**: Scores and ranks crops based on multiple factors.

**Scoring Algorithm**:
```python
Total Score = (
    Soil Match Score (30%) +
    Season Match Score (25%) +
    Weather Score (20%) +
    Irrigation Match Score (15%) +
    Profit Potential Score (10%)
)
```

**Key Method**:
```python
def recommend(
    self,
    request: PlanningRequest,
    farmer: FarmerProfile,
    env: WeatherContext,
    crops: List[Crop],
    season: Season
) -> List[CropCard]:
    """
    Returns top 5 crops ranked by suitability score
    Applies risk preference filtering
    """
```

**Risk Preference Logic**:
- **Safe**: Only crops with score > 70
- **Balanced**: Crops with score > 50
- **High Profit**: All crops, sorted by profit potential

### 2. WeatherEngine (engines/weather_engine.py)

**Purpose**: Fetches weather data from OpenWeather API with fallback.

**Key Method**:
```python
def get_context(self, lat: float, lon: float) -> WeatherContext:
    """
    Returns:
        WeatherContext with temperature, humidity, rain forecast
    
    Fallback Strategy:
        1. Try OpenWeather API
        2. If fails, use seasonal averages
        3. Never throws exception
    """
```

**Weather Context**:
```python
@dataclass
class WeatherContext:
    temperature_c: float
    humidity_pct: float
    rain_mm_next_7_days: float
    weather_condition: str
    source: str  # "api" or "fallback"
```

### 3. SchemeEngine (engines/scheme_engine.py)

**Purpose**: Checks farmer eligibility for government schemes.

**Eligibility Criteria**:
- Geographic availability (state/district)
- Land size requirements
- Crop type compatibility
- Deadline status

**Key Method**:
```python
def recommend_schemes(
    self,
    farmer: FarmerProfile,
    recommended_crops: List[CropCard],
    all_schemes: List[GovernmentScheme]
) -> List[SchemeCard]:
    """
    Returns all schemes with eligibility status and reasoning
    Includes deadline warnings for urgent schemes
    """
```

### 4. ReminderEngine (engines/reminder_engine.py)

**Purpose**: Generates automated reminders for scheme deadlines.

**Reminder Schedule**:
- 15 days before deadline
- 7 days before deadline
- 1 day before deadline

**Key Method**:
```python
def generate(
    self,
    scheme_results: List[SchemeCard],
    farmer: FarmerProfile
) -> List[ReminderRecord]:
    """
    Creates reminders for eligible schemes with deadlines
    Multilingual message generation
    """
```

### 5. ResponseBuilder (engines/response_builder.py)

**Purpose**: Formats all data into voice-first output.

**Key Method**:
```python
def build_output(
    self,
    farmer: FarmerProfile,
    weather: WeatherContext,
    crops: List[CropCard],
    schemes: List[SchemeCard],
    reminders: List[ReminderRecord]
) -> PreSeedingOutput:
    """
    Builds concise speech text for voice assistant
    Prioritizes urgent information
    Supports Hindi and English
    """
```

---

## Data Access Layer

### FarmerRepository (repositories/farmer_repo.py)

**Purpose**: Manages farmer profile data.

**Mock Farmers**:
- **F001**: Punjab - Alluvial soil, Canal irrigation, 4.5 acres
- **F002**: Maharashtra - Black soil, Rainfed, 2.0 acres
- **F003**: Karnataka - Red soil, Drip irrigation, 8.0 acres
- **F004**: Uttar Pradesh - Loamy soil, Tube well, 6.0 acres
- **F005**: Rajasthan - Sandy soil, Sprinkler, 15.0 acres

**Key Method**:
```python
def get_farmer(self, farmer_id: str) -> Optional[FarmerProfile]:
    """
    Returns farmer profile or None
    Replace with MongoDB query in production
    """
```

### CropRepository (repositories/crop_repo.py)

**Purpose**: Manages crop encyclopedia.

**Supported Crops** (10+):
- Wheat, Rice, Cotton, Sugarcane
- Onion, Potato, Tomato
- Maize, Bajra, Jowar
- Groundnut, Soybean

**Crop Data Structure**:
```python
@dataclass
class Crop:
    name: str
    name_hindi: str
    suitable_soils: List[SoilType]
    suitable_seasons: List[Season]
    water_requirement: WaterRequirement
    profit_potential: ProfitLevel
    risks: List[str]
    seed_info: SeedInfo
```

### SchemeRepository (repositories/scheme_repo.py)

**Purpose**: Manages government scheme database.

**Supported Schemes** (8+):
- PM-KISAN (Direct income support)
- PMFBY (Crop insurance)
- KCC (Kisan Credit Card)
- Soil Health Card Scheme
- Pradhan Mantri Krishi Sinchai Yojana
- National Agriculture Market (e-NAM)
- Paramparagat Krishi Vikas Yojana (Organic farming)
- Rashtriya Krishi Vikas Yojana

**Scheme Data Structure**:
```python
@dataclass
class GovernmentScheme:
    name: str
    name_hindi: str
    available_states: List[str]
    min_land_acres: float
    max_land_acres: Optional[float]
    eligible_crops: List[str]  # Empty = all crops
    deadline: Optional[date]
    required_documents: List[str]
    application_process: str
```

---

## Usage Patterns

### Pattern 1: Basic Crop Recommendation

```python
from Backend.Farm_management.Planning_stage import PreSeedingService, PlanningRequest

# Initialize service
service = PreSeedingService()

# Create request
request = PlanningRequest(
    farmer_id="F001",
    season=None,  # Auto-detect
    risk_preference="balanced"
)

# Get recommendations
output = service.run(request)

# Access crop recommendations
for crop in output.crop_cards:
    print(f"{crop.crop_name}: {crop.score}/100")
    print(f"Reasons: {', '.join(crop.reasons)}")
```

### Pattern 2: Scheme Eligibility Check

```python
from Backend.Farm_management.Planning_stage.gov_scheme_suggestor import suggest_schemes_for_farmer

# Get scheme suggestions
schemes = suggest_schemes_for_farmer("F001")

# Filter eligible schemes
eligible = [s for s in schemes if s.eligible]

for scheme in eligible:
    print(f"✅ {scheme.scheme_name}")
    if scheme.deadline_warning:
        print(f"   ⚠️ {scheme.deadline_warning}")
    print(f"   Docs: {', '.join(scheme.docs_required)}")
```

### Pattern 3: Voice Assistant Integration

```python
from Backend.Farm_management.Planning_stage import PreSeedingService, PlanningRequest

service = PreSeedingService()
request = PlanningRequest(farmer_id="F001")
output = service.run(request)

# Get voice output
speech_text = output.speech_text  # Ready for TTS

# Example output:
# "आपके लिए 5 फसलें सुझाई गई हैं। सबसे अच्छी: गेहूं (85 अंक)।
#  आप 3 सरकारी योजनाओं के लिए पात्र हैं। PM-KISAN की अंतिम तिथि 7 दिन में है।"
```

### Pattern 4: Custom Risk Preference

```python
# Safe mode - only high-scoring crops
request = PlanningRequest(
    farmer_id="F001",
    risk_preference="safe"
)
output = service.run(request)  # Only crops with score > 70

# High profit mode - all crops ranked by profit
request = PlanningRequest(
    farmer_id="F001",
    risk_preference="high_profit"
)
output = service.run(request)  # All crops, profit-optimized
```

---

## Integration Guide

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from Backend.Farm_management.Planning_stage import (
    PreSeedingService, PlanningRequest, PreSeedingOutput
)

app = FastAPI()
service = PreSeedingService(weather_api_key="your_api_key")

@app.post("/api/planning/recommend", response_model=PreSeedingOutput)
async def get_recommendations(request: PlanningRequest):
    try:
        output = service.run(request)
        return output
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/planning/schemes/{farmer_id}")
async def get_schemes(farmer_id: str):
    request = PlanningRequest(farmer_id=farmer_id)
    output = service.run(request)
    return {"schemes": output.scheme_cards}
```

### MongoDB Integration

Replace mock repositories with MongoDB:

```python
from pymongo import MongoClient
from Backend.Farm_management.Planning_stage.repositories import FarmerRepository
from Backend.Farm_management.Planning_stage.models import FarmerProfile

class MongoFarmerRepository(FarmerRepository):
    def __init__(self, db_client: MongoClient):
        self.collection = db_client.kisaan_mitra.farmers
    
    def get_farmer(self, farmer_id: str) -> Optional[FarmerProfile]:
        doc = self.collection.find_one({"farmer_id": farmer_id})
        if not doc:
            return None
        return FarmerProfile(**doc)

# Use custom repository
client = MongoClient("mongodb://localhost:27017")
farmer_repo = MongoFarmerRepository(client)
service = PreSeedingService(farmer_repo=farmer_repo)
```

### Celery Task Integration

Schedule reminders with Celery:

```python
from celery import Celery
from Backend.Farm_management.Planning_stage import PreSeedingService, PlanningRequest

app = Celery('tasks', broker='redis://localhost:6379')

@app.task
def generate_planning_report(farmer_id: str):
    service = PreSeedingService()
    request = PlanningRequest(farmer_id=farmer_id)
    output = service.run(request)
    
    # Send reminders via SMS/notification
    for reminder in output.reminders:
        send_sms_notification.delay(farmer_id, reminder.message)
    
    return output.dict()

@app.task
def send_sms_notification(farmer_id: str, message: str):
    # SMS integration logic
    pass
```

---

## Extension Points

### Adding New Crops

Edit `repositories/crop_repo.py`:

```python
def _create_mock_crops(self) -> dict:
    return {
        # ... existing crops ...
        "newcrop": Crop(
            name="NewCrop",
            name_hindi="नई फसल",
            suitable_soils=[SoilType.ALLUVIAL, SoilType.LOAMY],
            suitable_seasons=[Season.KHARIF],
            water_requirement=WaterRequirement.MEDIUM,
            profit_potential=ProfitLevel.HIGH,
            risks=["Risk 1", "Risk 2"],
            seed_info=SeedInfo(
                variety="Variety Name",
                seed_rate_kg_per_acre=10.0,
                procurement_source="Local market"
            )
        )
    }
```

### Adding New Government Schemes

Edit `repositories/scheme_repo.py`:

```python
def _create_mock_schemes(self) -> dict:
    return {
        # ... existing schemes ...
        "new_scheme": GovernmentScheme(
            name="New Scheme",
            name_hindi="नई योजना",
            available_states=["All"],
            min_land_acres=0.0,
            max_land_acres=None,
            eligible_crops=[],  # Empty = all crops
            deadline=date(2026, 12, 31),
            required_documents=["Aadhaar", "Land documents"],
            application_process="Visit CSC or apply online"
        )
    }
```

### Customizing Scoring Weights

Edit `constants.py`:

```python
# Crop scoring weights (must sum to 1.0)
SOIL_WEIGHT = 0.30      # Soil compatibility
SEASON_WEIGHT = 0.25    # Season suitability
WEATHER_WEIGHT = 0.20   # Weather conditions
IRRIGATION_WEIGHT = 0.15  # Irrigation match
PROFIT_WEIGHT = 0.10    # Profit potential
```

### Adding New Languages

1. Add language to `constants.py`:
```python
class Language(str, Enum):
    HINDI = "hi"
    ENGLISH = "en"
    MARATHI = "mr"  # New language
```

2. Update `ResponseBuilder` to support new language:
```python
def _build_speech_text(self, ...) -> str:
    if language == Language.MARATHI:
        return self._build_marathi_speech(...)
    # ... existing logic ...
```

---

## Testing

### Running Tests

```bash
# Automated test
python Backend/Farm_management/Planning_stage/test_runner.py

# Interactive CLI demo
cd Backend/Farm_management/Planning_stage
python -m cli_demo
```

### Test Coverage

The module includes:
- ✅ Unit tests for all engines
- ✅ Integration tests for service layer
- ✅ Mock data for offline testing
- ✅ CLI demo for manual testing

---

## Production Checklist

### Before Deployment

- [ ] Replace mock repositories with MongoDB connections
- [ ] Configure OpenWeather API key
- [ ] Set up structured logging
- [ ] Implement rate limiting for API calls
- [ ] Add caching for weather data
- [ ] Set up monitoring and alerts
- [ ] Configure Celery for reminder scheduling
- [ ] Implement SMS/notification service
- [ ] Add authentication and authorization
- [ ] Set up error tracking (Sentry, etc.)

### Environment Variables

```bash
OPENWEATHER_API_KEY=your_api_key
MONGODB_URI=mongodb://localhost:27017
REDIS_URL=redis://localhost:6379
SMS_API_KEY=your_sms_api_key
```

---

## Performance Considerations

### Complexity
- Crop scoring: O(n) where n = number of crops (typically 10-50)
- Scheme checking: O(m) where m = number of schemes (typically 10-20)
- Overall service call: O(n + m) - linear time

### Optimization Tips
1. Cache weather data (TTL: 1 hour)
2. Cache crop/scheme databases (TTL: 24 hours)
3. Use database indexes on farmer_id
4. Implement pagination for large result sets
5. Use async operations for external API calls

---

## Troubleshooting

### Common Issues

**Issue**: Farmer not found
```python
# Solution: Check farmer_id exists in repository
farmer = farmer_repo.get_farmer("F001")
if not farmer:
    # Add farmer to database
```

**Issue**: Weather API fails
```python
# Solution: Module automatically falls back to mock data
# Check logs for "Using fallback weather data"
```

**Issue**: No crops recommended
```python
# Solution: Lower risk preference or check farmer profile
request = PlanningRequest(
    farmer_id="F001",
    risk_preference="balanced"  # Try "balanced" instead of "safe"
)
```

---

## Support and Maintenance

### Code Quality
- ✅ Type hints throughout
- ✅ Pydantic validation
- ✅ Comprehensive error handling
- ✅ Modular, testable design
- ✅ PEP 8 compliant

### Documentation
- ✅ Inline code documentation
- ✅ README with examples
- ✅ This comprehensive codebase guide
- ✅ CLI demo for exploration

---

**Last Updated**: January 2026  
**Version**: 1.0  
**Status**: Production-Ready Demo Code
