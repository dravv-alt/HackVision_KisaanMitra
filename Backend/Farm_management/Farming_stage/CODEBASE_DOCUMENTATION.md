# Farming Stage - Codebase Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Module Structure](#module-structure)
4. [Core Components](#core-components)
5. [Data Models](#data-models)
6. [Engine Components](#engine-components)
7. [Usage Patterns](#usage-patterns)
8. [Integration Guide](#integration-guide)
9. [Extension Points](#extension-points)

---

## Overview

### Purpose
The **Farming Stage** module provides real-time decision support for farmers during the active growing season. It delivers intelligent recommendations for irrigation, disease treatment, fertilizer application, and harvest timing through a voice-first interface.

### Key Capabilities
- **Weather Monitoring**: Real-time weather data with OpenWeather API integration and fallback
- **Market Intelligence**: Price tracking and demand forecasting for optimal selling decisions
- **Disease Detection**: Vision-based crop disease identification with treatment recommendations
- **Irrigation Advisory**: Smart irrigation scheduling based on weather and crop stage
- **Input Optimization**: Fertilizer and pesticide recommendations with dosage calculations
- **Harvest Planning**: Decision tree for optimal harvest timing based on weather and market conditions

### Technology Stack
- **Language**: Python 3.8+
- **Data Validation**: Pydantic
- **External APIs**: OpenWeather API (optional), Vision AI (optional)
- **Architecture**: Engine Pattern with Fallback Mechanisms

---

## Architecture

### Design Philosophy

The module follows a **modular engine architecture** where each engine is:
- **Independent**: Can function standalone with mock data
- **Resilient**: Never crashes - always provides fallback responses
- **Testable**: Pure functions with clear inputs/outputs
- **Voice-First**: Outputs optimized for text-to-speech

### Engine Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Farming Assistant                       │
│                  (Main Orchestrator)                     │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┼───────────┬───────────┐
        │           │           │           │
        ▼           ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Weather  │ │ Market   │ │ Vision   │ │Knowledge │
│ Engine   │ │ Engine   │ │ Engine   │ │ Engine   │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
     │            │            │            │
     ▼            ▼            ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│OpenWeather│ │Mock Price│ │Vision AI │ │Knowledge │
│   API     │ │  Data    │ │  Model   │ │   Base   │
│(+Fallback)│ │          │ │(+Fallback)│ │          │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
```

### Data Flow

```
User Input (Voice/Text)
         │
         ▼
┌─────────────────────┐
│ Gather Contexts     │
│ - Crop Context      │
│ - Environmental     │
│ - Market Context    │
└──────────┬──────────┘
           │
           ├──► WeatherEngine.get_context()
           ├──► MarketEngine.get_market_data()
           └──► VisionEngine.analyze_image()
           │
           ▼
┌─────────────────────┐
│ KnowledgeEngine     │
│ Decision Making     │
└──────────┬──────────┘
           │
           ├──► get_irrigation_advice()
           ├──► get_treatment_recommendation()
           └──► plan_harvest()
           │
           ▼
┌─────────────────────┐
│ AdvisoryOutput      │
│ (Voice-Ready)       │
└─────────────────────┘
```

---

## Module Structure

```
Farming_stage/
├── __init__.py                 # Public API exports
├── models.py                   # Pydantic data models
├── main_driver.py              # Comprehensive test suite
├── test_output.txt             # Test results
│
├── engines/                    # Core decision engines
│   ├── __init__.py
│   ├── weather_engine.py       # Weather data fetching
│   ├── market_engine.py        # Market price tracking
│   ├── vision_engine.py        # Disease detection
│   └── knowledge_engine.py     # Advisory logic
│
└── models/                     # Additional model definitions
    └── (if any)
```

---

## Core Components

### 1. Main Driver (main_driver.py)

**Purpose**: Comprehensive testing framework demonstrating all engine capabilities.

**Test Scenarios**:
1. Weather Engine Test
2. Market Engine Test
3. Vision Engine Test
4. Irrigation Advisor Test
5. Input Optimizer Test
6. Harvest Planner Test
7. Full End-to-End Simulation

**Running Tests**:
```bash
cd Backend/Farm_management/Farming_stage
python main_driver.py
```

**Expected Output**:
```
🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜
  FARMING ASSISTANT - COMPREHENSIVE TEST SUITE
🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜🚜

✅ Weather Engine: Working (with fallback)
✅ Market Engine: Working (mock data)
✅ Vision Engine: Working (with fallback)
✅ Knowledge Engine:
   ✅ Irrigation Advisor
   ✅ Input Optimizer
   ✅ Harvest Planner

🎯 System is DEMO-READY!
```

---

## Data Models

### Core Enums

#### CropStage
```python
class CropStage(str, Enum):
    SOWING = "sowing"
    GERMINATION = "germination"
    VEGETATIVE = "vegetative"
    FLOWERING = "flowering"
    FRUITING = "fruiting"
    MATURATION = "maturation"
    HARVEST_READY = "harvest_ready"
```

#### PriceTrend
```python
class PriceTrend(str, Enum):
    RISING = "rising"
    STABLE = "stable"
    FALLING = "falling"
```

#### UrgencyLevel
```python
class UrgencyLevel(str, Enum):
    INFO = "info"          # General information
    MODERATE = "moderate"  # Action recommended soon
    HIGH = "high"          # Action needed within 24-48 hours
    CRITICAL = "critical"  # Immediate action required
```

### Input Models

#### CropContext
```python
class CropContext(BaseModel):
    name: str                    # Crop name (e.g., "Tomato", "Wheat")
    sowing_date: date            # When crop was planted
    current_stage: CropStage     # Current growth stage
```

**Example**:
```python
crop = CropContext(
    name="Tomato",
    sowing_date=date(2026, 1, 15),
    current_stage=CropStage.FLOWERING
)
```

#### EnvironmentalContext
```python
class EnvironmentalContext(BaseModel):
    temperature: float           # Temperature in Celsius (-10 to 60)
    rain_forecast: bool          # Rain expected in 24-48 hours
    humidity: float              # Relative humidity (0-100%)
    wind_speed: Optional[float]  # Wind speed in km/h
```

**Example**:
```python
environment = EnvironmentalContext(
    temperature=28.5,
    rain_forecast=False,
    humidity=65.0,
    wind_speed=12.0
)
```

#### MarketContext
```python
class MarketContext(BaseModel):
    crop_name: str               # Name of the crop
    current_price: float         # Current price per kg in ₹
    price_trend: PriceTrend      # Price movement trend
    demand_level: DemandLevel    # Current market demand
```

**Example**:
```python
market = MarketContext(
    crop_name="Onion",
    current_price=40.0,
    price_trend=PriceTrend.RISING,
    demand_level=DemandLevel.HIGH
)
```

### Output Models

#### AdvisoryOutput
```python
class AdvisoryOutput(BaseModel):
    action_header: str           # Short action title (e.g., "STOP IRRIGATION")
    spoken_advice: str           # Natural language for voice output
    detailed_reasoning: str      # Technical explanation
    urgency: UrgencyLevel        # How urgent this action is
    
    # Optional fields
    chemical_dosage: Optional[str]      # Exact application instructions
    safety_warning: Optional[str]       # Safety precautions
    organic_alternative: Optional[str]  # Low-cost organic option
```

**Example**:
```python
advisory = AdvisoryOutput(
    action_header="APPLY FUNGICIDE",
    spoken_advice="Your tomato plants show signs of leaf blight. Apply Mancozeb fungicide immediately.",
    detailed_reasoning="Leaf blight spreads rapidly in humid conditions. Early treatment prevents crop loss.",
    urgency=UrgencyLevel.HIGH,
    chemical_dosage="Mancozeb 2g/L water, spray 200mL per square meter",
    safety_warning="Do not spray in windy conditions (>15km/h). Wear protective gloves.",
    organic_alternative="Neem oil solution: 30mL neem oil per liter of water"
)
```

#### DiseaseDetectionResult
```python
class DiseaseDetectionResult(BaseModel):
    disease_name: str            # Identified disease or "Healthy"
    confidence: float            # Confidence score 0-1
    is_mock: bool                # Whether this is fallback mock result
```

---

## Engine Components

### 1. WeatherEngine (engines/weather_engine.py)

**Purpose**: Fetches real-time weather data with automatic fallback.

**Key Method**:
```python
def get_context(self, lat: float, lon: float) -> EnvironmentalContext:
    """
    Fetch weather data for given coordinates
    
    Args:
        lat: Latitude
        lon: Longitude
    
    Returns:
        EnvironmentalContext with weather data
    
    Fallback Strategy:
        1. Try OpenWeather API
        2. If fails, use seasonal averages
        3. Never throws exception
    """
```

**Usage Example**:
```python
from Farming_stage.engines import WeatherEngine

engine = WeatherEngine(api_key="your_api_key")  # Optional
context = engine.get_context(28.6139, 77.2090)  # Delhi coordinates

print(f"Temperature: {context.temperature}°C")
print(f"Humidity: {context.humidity}%")
print(f"Rain forecast: {context.rain_forecast}")
```

**Fallback Behavior**:
- If API key not provided → Uses mock data
- If API call fails → Uses seasonal averages
- Always returns valid `EnvironmentalContext`

---

### 2. MarketEngine (engines/market_engine.py)

**Purpose**: Provides market price data and demand forecasting.

**Key Methods**:

```python
def get_market_data(self, crop_name: str) -> MarketContext:
    """
    Get current market data for a crop
    
    Args:
        crop_name: Name of the crop
    
    Returns:
        MarketContext with price and demand info
    """

def get_price_forecast(self, crop_name: str, days_ahead: int = 7) -> str:
    """
    Get price forecast for next N days
    
    Args:
        crop_name: Name of the crop
        days_ahead: Number of days to forecast
    
    Returns:
        Human-readable forecast string
    """
```

**Usage Example**:
```python
from Farming_stage.engines import MarketEngine

engine = MarketEngine()
market = engine.get_market_data("Onion")

print(f"Current price: ₹{market.current_price}/kg")
print(f"Trend: {market.price_trend.value}")
print(f"Demand: {market.demand_level.value}")

forecast = engine.get_price_forecast("Onion", days_ahead=7)
print(f"Forecast: {forecast}")
```

**Supported Crops**:
- Onion, Tomato, Potato, Wheat, Rice, Cotton, Cabbage, Carrot

**Mock Data Structure**:
```python
{
    "Onion": {
        "price": 35.0,
        "trend": PriceTrend.RISING,
        "demand": DemandLevel.HIGH
    },
    # ... more crops
}
```

---

### 3. VisionEngine (engines/vision_engine.py)

**Purpose**: Analyzes crop images for disease detection.

**Key Methods**:

```python
def analyze_image(self, image_bytes: bytes) -> DiseaseDetectionResult:
    """
    Analyze crop image for disease detection
    
    Args:
        image_bytes: Raw image data
    
    Returns:
        DiseaseDetectionResult with disease name and confidence
    
    Fallback:
        Returns mock disease if vision model unavailable
    """

def get_disease_info(self, disease_name: str) -> dict:
    """
    Get detailed information about a disease
    
    Args:
        disease_name: Name of the disease
    
    Returns:
        Dictionary with severity, spread rate, symptoms
    """
```

**Usage Example**:
```python
from Farming_stage.engines import VisionEngine

engine = VisionEngine()

# Analyze image
with open("crop_image.jpg", "rb") as f:
    image_bytes = f.read()

result = engine.analyze_image(image_bytes)

print(f"Disease: {result.disease_name}")
print(f"Confidence: {result.confidence * 100:.1f}%")
print(f"Mock result: {result.is_mock}")

# Get disease details
if result.disease_name != "Healthy":
    info = engine.get_disease_info(result.disease_name)
    print(f"Severity: {info['severity']}")
    print(f"Symptoms: {info['symptoms']}")
```

**Supported Diseases**:
- Leaf Blight
- Powdery Mildew
- Bacterial Wilt
- Mosaic Virus
- Root Rot
- Healthy (no disease)

**Fallback Behavior**:
- If vision model unavailable → Returns mock disease with `is_mock=True`
- Always returns valid `DiseaseDetectionResult`

---

### 4. KnowledgeEngine (engines/knowledge_engine.py)

**Purpose**: Core decision-making engine for all farming advisories.

**Key Methods**:

#### 4.1 Irrigation Advisory

```python
def get_irrigation_advice(
    self,
    crop: CropContext,
    environment: EnvironmentalContext
) -> AdvisoryOutput:
    """
    Provide irrigation recommendations
    
    Decision Logic:
    - If rain forecast → STOP irrigation
    - If flowering stage + no rain → INCREASE irrigation
    - If high temperature + low humidity → IRRIGATE
    - Else → NORMAL irrigation
    
    Returns:
        AdvisoryOutput with irrigation instructions
    """
```

**Usage Example**:
```python
from Farming_stage.engines import KnowledgeEngine
from Farming_stage.models import CropContext, EnvironmentalContext, CropStage
from datetime import date, timedelta

engine = KnowledgeEngine()

crop = CropContext(
    name="Tomato",
    sowing_date=date.today() - timedelta(days=30),
    current_stage=CropStage.FLOWERING
)

environment = EnvironmentalContext(
    temperature=32.0,
    rain_forecast=False,
    humidity=60.0,
    wind_speed=10.0
)

advisory = engine.get_irrigation_advice(crop, environment)

print(f"Action: {advisory.action_header}")
print(f"Advice: {advisory.spoken_advice}")
print(f"Urgency: {advisory.urgency.value}")
```

#### 4.2 Treatment Recommendations

```python
def get_treatment_recommendation(
    self,
    disease_name: Optional[str] = None,
    crop_stage: Optional[CropStage] = None,
    crop_name: str = "Generic"
) -> AdvisoryOutput:
    """
    Provide disease treatment or fertilizer recommendations
    
    Args:
        disease_name: If provided, gives disease treatment
        crop_stage: If provided, gives stage-based fertilizer advice
        crop_name: Name of the crop
    
    Returns:
        AdvisoryOutput with treatment/fertilizer instructions
        Includes chemical dosage, safety warnings, organic alternatives
    """
```

**Usage Example - Disease Treatment**:
```python
# Disease treatment
advisory = engine.get_treatment_recommendation(
    disease_name="Leaf Blight",
    crop_name="Tomato"
)

print(f"Treatment: {advisory.action_header}")
print(f"Chemical: {advisory.chemical_dosage}")
print(f"Organic: {advisory.organic_alternative}")
print(f"Safety: {advisory.safety_warning}")
```

**Usage Example - Fertilizer Recommendation**:
```python
# Stage-based fertilizer
advisory = engine.get_treatment_recommendation(
    crop_stage=CropStage.FLOWERING,
    crop_name="Wheat"
)

print(f"Fertilizer: {advisory.action_header}")
print(f"Dosage: {advisory.chemical_dosage}")
```

**Treatment Database**:
```python
DISEASE_TREATMENTS = {
    "Leaf Blight": {
        "chemical": "Mancozeb 2g/L water",
        "organic": "Neem oil 30mL/L water",
        "safety": "Wear gloves, avoid windy conditions"
    },
    # ... more diseases
}

FERTILIZER_SCHEDULE = {
    CropStage.VEGETATIVE: {
        "fertilizer": "Urea (Nitrogen-rich)",
        "dosage": "50kg/acre",
        "timing": "Split into 2 doses"
    },
    # ... more stages
}
```

#### 4.3 Harvest Planning

```python
def plan_harvest(
    self,
    environment: EnvironmentalContext,
    market: MarketContext,
    storage_available: bool,
    crop_name: str
) -> AdvisoryOutput:
    """
    Decide optimal harvest timing
    
    Decision Tree:
    1. If rain forecast → DELAY harvest
    2. If price falling → HARVEST NOW
    3. If price rising + storage available → DELAY harvest
    4. If high price + good weather → HARVEST NOW
    5. Else → WAIT for better conditions
    
    Returns:
        AdvisoryOutput with harvest timing recommendation
    """
```

**Usage Example**:
```python
environment = EnvironmentalContext(
    temperature=28.0,
    rain_forecast=False,
    humidity=60.0
)

market = MarketContext(
    crop_name="Onion",
    current_price=45.0,
    price_trend=PriceTrend.RISING,
    demand_level=DemandLevel.HIGH
)

advisory = engine.plan_harvest(
    environment=environment,
    market=market,
    storage_available=True,
    crop_name="Onion"
)

print(f"Decision: {advisory.action_header}")
print(f"Reasoning: {advisory.detailed_reasoning}")
```

---

## Usage Patterns

### Pattern 1: Complete Farming Cycle Simulation

```python
from Farming_stage.engines import (
    WeatherEngine, MarketEngine, VisionEngine, KnowledgeEngine
)
from Farming_stage.models import CropContext, CropStage
from datetime import date, timedelta

# Initialize engines
weather_engine = WeatherEngine()
market_engine = MarketEngine()
vision_engine = VisionEngine()
knowledge_engine = KnowledgeEngine()

# Define crop
crop = CropContext(
    name="Tomato",
    sowing_date=date.today() - timedelta(days=45),
    current_stage=CropStage.FLOWERING
)

# Gather contexts
environment = weather_engine.get_context(18.5204, 73.8567)  # Pune
market = market_engine.get_market_data("Tomato")

# Get recommendations
irrigation_advice = knowledge_engine.get_irrigation_advice(crop, environment)
fertilizer_advice = knowledge_engine.get_treatment_recommendation(
    crop_stage=crop.current_stage,
    crop_name="Tomato"
)
harvest_plan = knowledge_engine.plan_harvest(
    environment, market, storage_available=False, crop_name="Tomato"
)

# Display results
print(f"Irrigation: {irrigation_advice.spoken_advice}")
print(f"Fertilizer: {fertilizer_advice.spoken_advice}")
print(f"Harvest: {harvest_plan.spoken_advice}")
```

### Pattern 2: Disease Detection and Treatment

```python
from Farming_stage.engines import VisionEngine, KnowledgeEngine

vision_engine = VisionEngine()
knowledge_engine = KnowledgeEngine()

# Analyze crop image
with open("crop_leaf.jpg", "rb") as f:
    image_bytes = f.read()

disease_result = vision_engine.analyze_image(image_bytes)

if disease_result.disease_name != "Healthy":
    # Get treatment recommendation
    treatment = knowledge_engine.get_treatment_recommendation(
        disease_name=disease_result.disease_name,
        crop_name="Tomato"
    )
    
    print(f"🔬 Disease Detected: {disease_result.disease_name}")
    print(f"📊 Confidence: {disease_result.confidence * 100:.0f}%")
    print(f"💊 Treatment: {treatment.chemical_dosage}")
    print(f"🌿 Organic Option: {treatment.organic_alternative}")
    print(f"⚠️  Safety: {treatment.safety_warning}")
else:
    print("✅ Crop is healthy!")
```

### Pattern 3: Voice Assistant Integration

```python
def get_farming_advice(farmer_location: tuple, crop_name: str, crop_stage: str):
    """
    Voice assistant endpoint
    Returns spoken advice ready for TTS
    """
    # Initialize engines
    weather_engine = WeatherEngine()
    market_engine = MarketEngine()
    knowledge_engine = KnowledgeEngine()
    
    # Gather data
    environment = weather_engine.get_context(*farmer_location)
    market = market_engine.get_market_data(crop_name)
    
    crop = CropContext(
        name=crop_name,
        sowing_date=date.today() - timedelta(days=30),
        current_stage=CropStage(crop_stage)
    )
    
    # Get advice
    irrigation = knowledge_engine.get_irrigation_advice(crop, environment)
    
    # Return voice-ready text
    return {
        "speech_text": irrigation.spoken_advice,
        "urgency": irrigation.urgency.value,
        "action": irrigation.action_header
    }

# Usage
advice = get_farming_advice(
    farmer_location=(28.6139, 77.2090),
    crop_name="Wheat",
    crop_stage="flowering"
)

print(f"🎤 {advice['speech_text']}")
```

---

## Integration Guide

### FastAPI Integration

```python
from fastapi import FastAPI, UploadFile, File
from Farming_stage.engines import (
    WeatherEngine, MarketEngine, VisionEngine, KnowledgeEngine
)
from Farming_stage.models import (
    CropContext, EnvironmentalContext, MarketContext, AdvisoryOutput
)

app = FastAPI()

# Initialize engines
weather_engine = WeatherEngine(api_key="your_api_key")
market_engine = MarketEngine()
vision_engine = VisionEngine()
knowledge_engine = KnowledgeEngine()

@app.get("/api/weather/{lat}/{lon}")
async def get_weather(lat: float, lon: float):
    context = weather_engine.get_context(lat, lon)
    return context

@app.get("/api/market/{crop_name}")
async def get_market_data(crop_name: str):
    market = market_engine.get_market_data(crop_name)
    return market

@app.post("/api/disease/detect")
async def detect_disease(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = vision_engine.analyze_image(image_bytes)
    
    if result.disease_name != "Healthy":
        treatment = knowledge_engine.get_treatment_recommendation(
            disease_name=result.disease_name
        )
        return {
            "disease": result.disease_name,
            "confidence": result.confidence,
            "treatment": treatment
        }
    return {"disease": "Healthy", "confidence": result.confidence}

@app.post("/api/advice/irrigation", response_model=AdvisoryOutput)
async def get_irrigation_advice(
    crop: CropContext,
    environment: EnvironmentalContext
):
    advice = knowledge_engine.get_irrigation_advice(crop, environment)
    return advice

@app.post("/api/advice/harvest", response_model=AdvisoryOutput)
async def get_harvest_advice(
    environment: EnvironmentalContext,
    market: MarketContext,
    storage_available: bool,
    crop_name: str
):
    advice = knowledge_engine.plan_harvest(
        environment, market, storage_available, crop_name
    )
    return advice
```

### WebSocket Integration for Real-Time Updates

```python
from fastapi import WebSocket
import asyncio

@app.websocket("/ws/farming/{farmer_id}")
async def farming_websocket(websocket: WebSocket, farmer_id: str):
    await websocket.accept()
    
    while True:
        # Send periodic updates
        weather = weather_engine.get_context(28.6139, 77.2090)
        market = market_engine.get_market_data("Tomato")
        
        await websocket.send_json({
            "weather": weather.dict(),
            "market": market.dict(),
            "timestamp": datetime.now().isoformat()
        })
        
        await asyncio.sleep(3600)  # Update every hour
```

---

## Extension Points

### Adding New Crops

Edit `engines/market_engine.py`:

```python
MOCK_MARKET_DATA = {
    # ... existing crops ...
    "NewCrop": {
        "price": 50.0,
        "trend": PriceTrend.STABLE,
        "demand": DemandLevel.MEDIUM
    }
}
```

### Adding New Diseases

Edit `engines/vision_engine.py`:

```python
DISEASE_DATABASE = {
    # ... existing diseases ...
    "New Disease": {
        "severity": "high",
        "spread_rate": "fast",
        "symptoms": "Description of symptoms",
        "affected_crops": ["Tomato", "Potato"]
    }
}
```

Edit `engines/knowledge_engine.py`:

```python
DISEASE_TREATMENTS = {
    # ... existing treatments ...
    "New Disease": {
        "chemical": "Chemical name and dosage",
        "organic": "Organic alternative",
        "safety": "Safety precautions",
        "urgency": UrgencyLevel.HIGH
    }
}
```

### Customizing Decision Logic

Edit `engines/knowledge_engine.py`:

```python
def plan_harvest(self, environment, market, storage_available, crop_name):
    # Add custom decision logic
    if crop_name == "SpecialCrop":
        # Custom logic for special crop
        return AdvisoryOutput(...)
    
    # Default logic
    # ...
```

---

## Testing

### Running Comprehensive Tests

```bash
cd Backend/Farm_management/Farming_stage
python main_driver.py
```

### Test Coverage

The `main_driver.py` includes:
- ✅ Weather Engine Test (API + Fallback)
- ✅ Market Engine Test (All crops)
- ✅ Vision Engine Test (Mock disease detection)
- ✅ Irrigation Advisor Test (Multiple scenarios)
- ✅ Input Optimizer Test (Disease + Fertilizer)
- ✅ Harvest Planner Test (Decision tree)
- ✅ Full End-to-End Simulation

### Manual Testing

```python
# Test individual engines
from Farming_stage.engines import WeatherEngine

engine = WeatherEngine()
context = engine.get_context(28.6139, 77.2090)
print(context)
```

---

## Production Checklist

### Before Deployment

- [ ] Configure OpenWeather API key
- [ ] Integrate real vision AI model
- [ ] Connect to live market price APIs
- [ ] Set up structured logging
- [ ] Implement rate limiting
- [ ] Add caching for weather/market data
- [ ] Set up monitoring and alerts
- [ ] Configure error tracking
- [ ] Add authentication for API endpoints
- [ ] Implement usage analytics

### Environment Variables

```bash
OPENWEATHER_API_KEY=your_api_key
VISION_AI_ENDPOINT=https://your-vision-api.com
MARKET_API_KEY=your_market_api_key
```

---

## Performance Considerations

### Optimization Tips

1. **Cache Weather Data**: TTL 30-60 minutes
2. **Cache Market Data**: TTL 15-30 minutes
3. **Batch Vision Processing**: Process multiple images together
4. **Async API Calls**: Use asyncio for parallel requests
5. **Database Indexing**: Index on farmer_id, crop_name

### Scalability

- Each engine is stateless → Easy horizontal scaling
- No database dependencies → Fast response times
- Fallback mechanisms → High availability

---

## Troubleshooting

### Common Issues

**Issue**: Weather API returns None
```python
# Solution: Check API key and fallback is working
engine = WeatherEngine(api_key="valid_key")
context = engine.get_context(lat, lon)
# Should always return valid context, even with fallback
```

**Issue**: Disease detection always returns mock
```python
# Solution: Integrate real vision model
# Current implementation uses fallback by default
```

**Issue**: Market data not available for crop
```python
# Solution: Add crop to MOCK_MARKET_DATA
# Or integrate with real market API
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
- ✅ Comprehensive test suite
- ✅ This codebase guide
- ✅ Example usage patterns

---

**Last Updated**: January 2026  
**Version**: 1.0  
**Status**: Production-Ready Demo Code with Fallback Mechanisms
