# Government Schemes Display Module

## Overview

A comprehensive **pure backend module** for displaying government schemes with filtering, caching, and new scheme alerts for the Voice-First Farming Assistant. This module provides scheme browsing by location and category with bilingual support.

## ✨ Features

- **Scheme Display**: Browse all available government schemes
- **Smart Filtering**: Filter by state, district, and category
- **API Integration**: Fetch schemes from external API with mock fallback
- **Caching**: MongoDB-ready caching layer for performance
- **New Scheme Alerts**: Automatic detection and notification of new schemes
- **Bilingual Support**: Hindi and English content
- **Config Management**: .env-based configuration with safe defaults
- **100% Demo Reliable**: Mock fallback ensures zero failures

## 🏗️ Architecture

```
Gov_Schemes/
├── config/                     # Configuration management
│   ├── settings.py            # .env loader with safe defaults
│   └── env.example            # Example configuration
├── repositories/               # Data access layer
│   ├── farmer_repo.py         # Farmer profiles
│   ├── scheme_repo.py         # Scheme caching & filtering
│   ├── scheme_api_client.py   # API integration
│   ├── alert_repo.py          # Alert storage
│   └── audit_repo.py          # Debug logging
├── engines/                    # Business logic
│   ├── scheme_fetch_engine.py # API sync & caching
│   ├── scheme_filter_engine.py # Filtering logic
│   ├── scheme_alert_engine.py # New scheme detection
│   └── response_builder.py    # UI output formatting
├── service.py                  # Main orchestration
└── cli_demo.py                 # Interactive testing
```

## 🚀 Quick Start

### Basic Usage

```python
from Gov_Schemes.service import GovSchemesDisplayService

# Initialize service
service = GovSchemesDisplayService()

# Get schemes for a farmer
output = service.get_schemes_display("FARMER001")

# Access data
print(f"Total schemes: {output.totalSchemes}")
print(f"New schemes: {output.newSchemesCount}")
print(f"Speech: {output.speechText}")

# Iterate through scheme cards
for card in output.schemeCards:
    print(f"{card.schemeName}: {card.scope}")
```

### Filtering

```python
from Gov_Schemes.constants import SchemeCategory

# Filter by category
output = service.get_schemes_display(
    farmer_id="FARMER001",
    category=SchemeCategory.LOAN
)

# Filter by location
output = service.get_schemes_display(
    farmer_id="FARMER001",
    state="Maharashtra",
    district="Nashik"
)
```

### Alerts

```python
# Get new scheme alerts
alerts = service.get_alerts_for_farmer("FARMER001")

for alert in alerts:
    print(f"{alert.title} - {alert.urgency.value}")

# Mark alert as read
service.mark_alert_as_read(alert_id)
```

## 🧪 Testing

### Run CLI Demo

```bash
# Automated demo
cd Backend
python -m Gov_Schemes.cli_demo

# Interactive mode
python -m Gov_Schemes.cli_demo --interactive
```

### Run Quick Test

```bash
cd Backend
python test_gov_schemes.py
```

## 📊 Data Models

### GovSchemesOutput

Main output model for UI integration:

```python
{
    "header": "सरकारी योजनाएं - 9 योजनाएं",
    "language": "hi",
    "speechText": "आपके लिए 9 सरकारी योजनाएं उपलब्ध हैं...",
    "schemeCards": [...],
    "totalSchemes": 9,
    "newSchemesCount": 2,
    "filterApplied": {
        "state": "Maharashtra",
        "district": "Nashik",
        "category": null
    }
}
```

### SchemeCardOutput

Individual scheme card:

```python
{
    "schemeId": "uuid",
    "schemeName": "PM-KISAN",
    "category": "subsidy",
    "categoryDisplay": "Subsidies",
    "description": "Income support of ₹6000 per year...",
    "benefits": "₹2000 every 4 months...",
    "scope": "All India",
    "isNew": false,
    "daysRemaining": null,
    "officialLink": "https://pmkisan.gov.in"
}
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in `Gov_Schemes/` directory:

```bash
# API Configuration
GOV_SCHEME_API_BASE_URL=https://api.example.com/schemes
GOV_SCHEME_API_TOKEN=your_api_token_here

# Environment
ENV_MODE=dev
MOCK_MODE=true

# Cache Settings
API_TIMEOUT=10
CACHE_TTL_HOURS=24
```

### Safe Defaults

The module works without `.env` file:
- `MOCK_MODE=true` (uses mock data)
- `CACHE_TTL_HOURS=24`
- `API_TIMEOUT=10`

## 🎯 Scheme Categories

```python
class SchemeCategory(Enum):
    SOIL = "soil"              # Soil Health
    FERTILIZER = "fertilizer"  # Fertilizer Subsidy
    LOAN = "loan"              # Agricultural Loans
    SUBSIDY = "subsidy"        # Subsidies
    INSURANCE = "insurance"    # Crop Insurance
    TRAINING = "training"      # Training Programs
    OTHER = "other"            # Other Schemes
```

## 📦 Mock Data

The module includes 9 realistic mock schemes:

1. **PM-KISAN** - All India subsidy
2. **PMFBY** - All India crop insurance
3. **Soil Health Card** - All India soil testing
4. **Maharashtra Krishi Samruddhi** - State-level subsidy
5. **Nashik Drip Irrigation** - District-level subsidy (NEW)
6. **Punjab Crop Diversification** - State-level training
7. **Kisan Credit Card** - All India loan
8. **Nutrient Based Subsidy** - All India fertilizer
9. **Digital Agriculture Mission** - All India training (NEW)

## 🔔 Alert System

### Alert Generation

Alerts are automatically generated for:
- Schemes created in last 7 days
- Schemes relevant to farmer's location
- Urgency based on application deadline

### Alert Urgency

- **HIGH**: Deadline ≤ 7 days
- **MEDIUM**: Deadline ≤ 30 days
- **LOW**: No deadline or > 30 days

## 🌐 Bilingual Support

### Hindi Example
```
"आपके लिए 9 सरकारी योजनाएं उपलब्ध हैं। 2 नई योजनाएं हाल ही में जोड़ी गई हैं।"
```

### English Example
```
"You have 9 government schemes available. 2 new schemes were recently added."
```

## 🔌 FastAPI Integration

### Example Endpoints

```python
from fastapi import FastAPI, Query
from Gov_Schemes import GovSchemesDisplayService, SchemeCategory

app = FastAPI()
service = GovSchemesDisplayService()

@app.get("/api/schemes/{farmer_id}")
async def get_schemes(
    farmer_id: str,
    state: str = None,
    district: str = None,
    category: SchemeCategory = None
):
    """Get government schemes"""
    output = service.get_schemes_display(
        farmer_id,
        state=state,
        district=district,
        category=category
    )
    return output.dict()

@app.get("/api/schemes/{farmer_id}/alerts")
async def get_alerts(farmer_id: str):
    """Get new scheme alerts"""
    alerts = service.get_alerts_for_farmer(farmer_id)
    return [alert.dict() for alert in alerts]

@app.post("/api/schemes/alerts/{alert_id}/read")
async def mark_alert_read(alert_id: str):
    """Mark alert as read"""
    success = service.mark_alert_as_read(alert_id)
    return {"success": success}
```

## 🛡️ Error Handling

The module is designed for **100% hackathon reliability**:

- ✅ Works without .env file
- ✅ Mock fallback if API fails
- ✅ Safe defaults for all config
- ✅ No crashes on missing data
- ✅ Graceful degradation

## 📝 Filtering Logic

### Location-Based Filtering

```
1. All-India schemes → Always shown
2. State-specific → Shown if state matches
3. District-specific → Shown if state AND district match
```

### Relevance Sorting

```
1. District-specific schemes (highest relevance)
2. State-wide schemes
3. All-India schemes
```

## 🔧 API Integration

### Mock Mode (Default)

```python
# Uses comprehensive mock data
# No external dependencies
# Perfect for hackathon demo
```

### Real API Mode

```python
# Set in .env:
MOCK_MODE=false
GOV_SCHEME_API_BASE_URL=https://api.example.com
GOV_SCHEME_API_TOKEN=your_token

# API client will attempt real call
# Falls back to mock if API fails
```

### API Integration Placeholder

The `scheme_api_client.py` has a ready-to-use structure:

```python
def _fetch_from_real_api(self):
    # TODO: Implement when API is ready
    # import requests
    # headers = {"Authorization": f"Bearer {self.settings.api_token}"}
    # response = requests.get(...)
    # return [SchemeRecord(**item) for item in response.json()]
    pass
```

## 📈 Caching Strategy

- **TTL**: 24 hours (configurable)
- **Auto-refresh**: When cache is stale
- **Force refresh**: Available via parameter
- **MongoDB-ready**: Repository pattern for easy integration

## 🎬 Demo Scenarios

The module includes realistic scenarios:

1. **All Schemes**: Browse complete catalog
2. **Category Filter**: View only loans/insurance/etc
3. **Location Filter**: State or district-specific
4. **New Schemes**: Recently added schemes with alerts
5. **Bilingual**: Hindi and English farmers

## 🚀 Production Deployment

### MongoDB Integration

Replace mock repositories with real MongoDB clients:

```python
from pymongo import MongoClient

class SchemeRepo:
    def __init__(self, db_client):
        self.collection = db_client.schemes_master
    
    def get_all_schemes(self):
        schemes = self.collection.find({"isActive": True})
        return [SchemeRecord(**s) for s in schemes]
```

### Real API Integration

1. Update `.env` with real API credentials
2. Set `MOCK_MODE=false`
3. Implement `_fetch_from_real_api()` method
4. Add error handling and retry logic

## 📄 Dependencies

```
pydantic>=2.0.0
```

No external API dependencies - fully self-contained!

## 🆘 Troubleshooting

### Module not found
```bash
# Ensure you're in Backend directory
cd Backend
python -m Gov_Schemes.cli_demo
```

### No schemes showing
```bash
# Force refresh from API
output = service.get_schemes_display(farmer_id, force_refresh=True)
```

### Config not loading
```bash
# Check .env file location
# Should be in: Backend/Gov_Schemes/.env
# Or use environment variables directly
```

## 🤝 Integration Points

### With Inventory Module
```python
# Share alert repository for unified notifications
from Inventory.repositories import AlertRepo
from Gov_Schemes.service import GovSchemesDisplayService
```

### With Voice Agent
```python
# Use speechText for voice output
output = service.get_schemes_display(farmer_id)
speak(output.speechText)
```

---

**Built for HackVision 2026** 🏆
*Empowering Indian farmers with government scheme information*
