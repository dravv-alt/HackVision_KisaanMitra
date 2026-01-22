# Pre-Seeding / Planning Stage Module

**Complete Backend Module for Voice-First AI Farming Assistant**

## 🎯 Overview

This is a production-ready, pure backend module for the **Pre-Seeding Planning Stage** of a farming assistant application. It provides comprehensive crop recommendation, government scheme eligibility checking, and reminder management for Indian farmers.

### Key Features

✅ **Smart Crop Selection**
- Multi-factor scoring algorithm (soil, season, weather, irrigation, profit)
- Risk-aware recommendations (safe/balanced/high-profit modes)
- Detailed reasoning and risk analysis
- Seed procurement guidance

✅ **Government Scheme Support**
- Comprehensive scheme database (PM-KISAN, PMFBY, KCC, etc.)
- Personalized eligibility checking with detailed reasons
- Deadline tracking and urgency warnings
- Document checklist and application guidance

✅ **Reminder Engine**
- Automated deadline reminders (15, 7, 1 days before)
- Multilingual support (Hindi + English)
- MongoDB-ready persistence layer

✅ **Reliability-First Design**
- Works without internet (fallback mock data)
- Never crashes on missing data
- OpenWeather API with graceful fallback
- Repository pattern for easy DB integration

✅ **Voice-First Output**
- Concise speech text for voice assistants
- Multilingual support (Hindi + English)
- Urgency-based prioritization

---

## 📁 Module Structure

```
Planning_stage/
├── __init__.py                 # Module exports
├── constants.py                # Enums and configuration
├── models.py                   # Pydantic models (DTOs)
├── service.py                  # Main orchestration service
├── crop_selection.py           # Simplified wrapper (backward compat)
├── gov_scheme_suggestor.py     # Scheme suggestion wrapper
├── cli_demo.py                 # Interactive CLI demo
├── test_runner.py              # Quick automated test
│
├── repositories/               # Data access layer
│   ├── __init__.py
│   ├── farmer_repo.py          # Farmer profile access
│   ├── crop_repo.py            # Crop encyclopedia (10+ crops)
│   ├── scheme_repo.py          # Scheme database (8+ schemes)
│   └── reminder_repo.py        # Reminder persistence
│
└── engines/                    # Business logic engines
    ├── __init__.py
    ├── weather_engine.py       # Weather API + fallback
    ├── crop_recommendation.py  # Crop scoring engine
    ├── scheme_engine.py        # Eligibility checker
    ├── reminder_engine.py      # Reminder generator
    └── response_builder.py     # Voice output formatter
```

---

## 🚀 Quick Start

### 1. Installation

```bash
# No external dependencies required for basic functionality
# Optional: Install requests for live weather API
pip install pydantic requests
```

### 2. Basic Usage

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

# Access results
print(f"Top crop: {output.crop_cards[0].crop_name}")
print(f"Eligible schemes: {len([s for s in output.scheme_cards if s.eligible])}")
print(f"Voice output: {output.speech_text}")
```

### 3. Test the Module

```bash
# Quick automated test
python Backend/Farm_management/Planning_stage/test_runner.py

# Interactive CLI demo (from Planning_stage directory)
cd Backend/Farm_management/Planning_stage
python -m cli_demo
```

---

## 💡 Usage Examples

### Example 1: Crop Recommendations

```python
from Backend.Farm_management.Planning_stage.crop_selection import recommend_crops_for_farmer
from Backend.Farm_management.Planning_stage.constants import Season, RiskPreference

# Get crop recommendations
crops = recommend_crops_for_farmer(
    farmer_id="F001",
    season=Season.KHARIF,
    risk_preference=RiskPreference.HIGH_PROFIT
)

for crop in crops:
    print(f"{crop.crop_name}: {crop.score:.1f}/100")
    print(f"  Profit: {crop.profit_level.value}")
    print(f"  Reasons: {', '.join(crop.reasons)}")
```

### Example 2: Scheme Eligibility

```python
from Backend.Farm_management.Planning_stage.gov_scheme_suggestor import suggest_schemes_for_farmer

# Get scheme suggestions
schemes = suggest_schemes_for_farmer("F001")

for scheme in schemes:
    if scheme.eligible:
        print(f"✅ {scheme.scheme_name}")
        if scheme.deadline_warning:
            print(f"   ⚠️ {scheme.deadline_warning}")
```

### Example 3: Full Planning Report

```python
from Backend.Farm_management.Planning_stage import PreSeedingService, PlanningRequest

service = PreSeedingService()
request = PlanningRequest(farmer_id="F001")

output = service.run(request)

# Weather context
print(output.weather_summary)

# Crop recommendations with scoring
for crop in output.crop_cards:
    print(f"{crop.crop_name}: {crop.score}/100")

# Eligible schemes
eligible = [s for s in output.scheme_cards if s.eligible]
print(f"Eligible for {len(eligible)} schemes")

# Reminders
print(f"Created {len(output.reminders)} reminders")

# Voice output
print(f"🎤 {output.speech_text}")
```

---

## 🔧 Configuration

### Weather API (Optional)

Set environment variable for live weather data:

```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

Without API key, the module uses reliable fallback data.

### Adding Custom Farmers

Edit `repositories/farmer_repo.py`:

```python
def _create_mock_farmers(self) -> dict:
    return {
        "F001": FarmerProfile(
            farmer_id="F001",
            language=Language.HINDI,
            location=Location(state="Punjab", district="Ludhiana", ...),
            soil_type=SoilType.ALLUVIAL,
            irrigation_type=IrrigationType.CANAL,
            land_size_acres=4.5
        ),
        # Add more farmers...
    }
```

### Adding Custom Crops

Edit `repositories/crop_repo.py` to add more crops to the database.

### Adding Custom Schemes

Edit `repositories/scheme_repo.py` to add government schemes.

---

## 🏗️ Architecture

### Design Patterns

- **Repository Pattern**: Clean separation between data access and business logic
- **Service Layer**: Single entry point orchestrating all operations
- **Engine Pattern**: Modular, testable business logic components
- **DTO Pattern**: Pydantic models for type safety and validation

### Data Flow

```
Request → Service → [Repos + Engines] → Response Builder → Output
                     ↓
              Farmer Profile
              Weather Context
              Crop Database
              Scheme Database
                     ↓
              Crop Scoring
              Scheme Eligibility
              Reminder Generation
```

---

## 🧪 Testing

### Available Test Farmers

- **F001**: Punjab - Alluvial soil, Canal irrigation, 4.5 acres
- **F002**: Maharashtra - Black soil, Rainfed, 2.0 acres
- **F003**: Karnataka - Red soil, Drip irrigation, 8.0 acres
- **F004**: Uttar Pradesh - Loamy soil, Tube well, 6.0 acres
- **F005**: Rajasthan - Sandy soil, Sprinkler, 15.0 acres

### Running Tests

```bash
# Automated test
python Backend/Farm_management/Planning_stage/test_runner.py

# Manual testing with different farmers
python -m Backend.Farm_management.Planning_stage.cli_demo
```

---

## 🔌 FastAPI Integration

```python
from fastapi import FastAPI
from Backend.Farm_management.Planning_stage import PreSeedingService, PlanningRequest

app = FastAPI()
service = PreSeedingService()

@app.post("/api/planning/recommend")
async def get_recommendations(request: PlanningRequest):
    output = service.run(request)
    return output

@app.get("/api/planning/schemes/{farmer_id}")
async def get_schemes(farmer_id: str):
    request = PlanningRequest(farmer_id=farmer_id)
    output = service.run(request)
    return {"schemes": output.scheme_cards}
```

---

## 📊 Output Model

### PreSeedingOutput

```python
{
    "header": "Your Pre-Seeding Planning Report",
    "language": "hi" | "en",
    "speech_text": "Brief voice output...",
    "weather_summary": "Temperature: 28°C...",
    "crop_cards": [
        {
            "crop_name": "Wheat",
            "score": 85.5,
            "profit_level": "medium",
            "reasons": ["Excellent soil match", ...],
            "risks": ["Yellow rust", ...],
            "crop_requirements": {...},
            "next_best_action": "..."
        }
    ],
    "scheme_cards": [
        {
            "scheme_name": "PM-KISAN",
            "eligible": true,
            "why_eligible": ["Available in Punjab", ...],
            "deadline_warning": "Apply soon...",
            "docs_required": ["Aadhaar", "Land docs"],
            "next_step": "Visit CSC or apply online"
        }
    ],
    "reminders": [
        {
            "scheme_name": "PMFBY",
            "reminder_datetime": "2026-01-30T10:00:00",
            "message": "Deadline in 7 days"
        }
    ],
    "urgency_level": "high" | "medium" | "low"
}
```

---

## 🌐 Multilingual Support

The module supports **Hindi** and **English** throughout:

- Crop names (English + Hindi)
- Scheme names and descriptions
- Reminder messages
- Voice output text
- All user-facing text

Set farmer language in `FarmerProfile`:
```python
language=Language.HINDI  # or Language.ENGLISH
```

---

## 🛡️ Error Handling

The module is designed for **zero downtime**:

- ✅ Works without internet
- ✅ Graceful API fallback
- ✅ Handles missing farmer data
- ✅ Safe defaults for all operations
- ✅ Never throws unhandled exceptions

---

## 📈 Production Readiness

### What's Included

✅ Type hints throughout  
✅ Pydantic validation  
✅ Repository pattern for DB  
✅ Comprehensive error handling  
✅ Logging-ready design  
✅ Modular, testable code  
✅ Mock data for demos  

### What to Add for Production

- Replace mock repositories with MongoDB connections
- Add proper logging (structured logging recommended)
- Configure OpenWeather API key
- Set up monitoring and alerts
- Add rate limiting for API calls
- Implement caching for weather data

---

## 🤝 Integration Points

### MongoDB Integration

Replace mock repos with actual DB queries:

```python
class FarmerRepository:
    def __init__(self, db_client):
        self.collection = db_client.farmers
    
    def get_farmer(self, farmer_id: str) -> FarmerProfile:
        doc = self.collection.find_one({"farmer_id": farmer_id})
        return FarmerProfile(**doc) if doc else None
```

### FastAPI Routes

See FastAPI integration section above.

### Celery Tasks

Schedule reminders with Celery:

```python
from celery import Celery

@app.task
def send_scheme_reminder(reminder: ReminderRecord):
    # Send SMS/notification
    pass
```

---

## 📝 License

Part of HackVision_KisaanMitra project for 24-hour hackathon.

---

## 👨‍💻 Developer Notes

### Code Quality

- All code is typed with Python type hints
- Follows PEP 8 style guidelines
- Modular design for easy testing
- Repository pattern for clean architecture

### Performance

- Scoring algorithm: O(n) where n = number of crops
- Scheme checking: O(m) where m = number of schemes
- Optimized for typical use (10-50 crops, 10-20 schemes)

### Extensibility

- Easy to add new crops (just add to repository)
- Easy to add new schemes (just add to repository)
- Easy to customize scoring weights (modify constants.py)
- Easy to add new languages (extend models and response builder)

---

## ✅ Hackathon Ready

This module is:
- ✅ **100% Backend** (no UI code)
- ✅ **Framework-independent** (can integrate with FastAPI/Flask)
- ✅ **Fully functional** without internet
- ✅ **Production-clean** code structure
- ✅ **Voice-first** optimized output
- ✅ **Multilingual** (Hindi + English)
- ✅ **Tested** and working
- ✅ **Well-documented**

Perfect for a 24-hour hackathon demo that works reliably!

---

**For questions or issues, check the inline code documentation or run the CLI demo for interactive testing.**
