# Post-Harvest Stage - Codebase Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Module Structure](#module-structure)
4. [Core Components](#core-components)
5. [Data Models](#data-models)
6. [Storage Decision System](#storage-decision-system)
7. [Market Selection System](#market-selection-system)
8. [Usage Patterns](#usage-patterns)
9. [Integration Guide](#integration-guide)
10. [Extension Points](#extension-points)

---

## Overview

### Purpose
The **Post-Harvest Stage** module provides intelligent decision support for farmers after crop harvest. It optimizes two critical decisions:
1. **Storage Decision**: Should the farmer sell immediately or store and sell later?
2. **Market Selection**: Which mandi (market) provides the best net profit?

### Key Capabilities
- **Spoilage Risk Analysis**: Calculates safe storage duration based on crop characteristics
- **Price Forecasting**: Deterministic trend-based price predictions
- **Profit Optimization**: Selects best market considering transport and storage costs
- **Connected Decision Logic**: Integrated analysis, not separate rules
- **Zero Dependencies**: Uses only Python standard library

### Technology Stack
- **Language**: Python 3.8+
- **Architecture**: Modular Decision Intelligence System
- **Data Structures**: Dataclasses for type safety
- **External Dependencies**: None (pure Python)

---

## Architecture

### Design Philosophy

The module follows a **layered decision architecture**:

```
┌─────────────────────────────────────────────────────────┐
│              PostHarvestDecisionEngine                   │
│              (Main Orchestrator)                         │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┼───────────┬───────────┐
        │           │           │           │
        ▼           ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Storage  │ │ Market   │ │ Data     │ │ Utils    │
│ System   │ │ System   │ │ Access   │ │          │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
     │            │            │            │
     ├─ Spoilage  ├─ Price     ├─ Crop      ├─ Geo
     ├─ Storage   ├─ Transport ├─ Mandi     ├─ Time
     └─ Decision  └─ Profit    └─ Storage   └─ Units
```

### Decision Flow

```
┌─────────────────┐
│ FarmerContext   │ (Input: crop, quantity, location, dates)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│ PostHarvestDecisionEngine.run_decision()                │
└────────┬────────────────────────────────────────────────┘
         │
         ├──► 1. Load Crop Metadata
         │       └─ Get spoilage characteristics
         │
         ├──► 2. Select Initial Best Market
         │       └─ Find market with best current price
         │
         ├──► 3. Forecast Prices
         │       └─ Predict price trend for 14 days
         │
         ├──► 4. Calculate Spoilage Risk
         │       └─ Assess risk for waiting until peak price
         │
         ├──► 5. Find Storage Facility
         │       └─ Match storage type and capacity
         │
         ├──► 6. Make Storage Decision
         │       └─ Sell now vs Store and sell
         │
         ├──► 7. Re-select Market (if storing)
         │       └─ Re-evaluate with storage cost
         │
         └──► 8. Build Decision Result
                 └─ Return structured output
                     │
                     ▼
              ┌────────────────┐
              │ DecisionResult │
              └────────────────┘
```

---

## Module Structure

```
Post_Harvest_stage/
├── core/                       # Core orchestration
│   ├── __init__.py
│   ├── context.py              # Input context model
│   └── engine.py               # Main decision engine
│
├── storage/                    # Storage decision system
│   ├── __init__.py
│   ├── spoilage_model.py       # Shelf life & risk calculation
│   ├── storage_options.py      # Storage facility matching
│   └── storage_decision.py     # Sell vs Store logic
│
├── market/                     # Market selection system
│   ├── __init__.py
│   ├── price_model.py          # Price trend forecasting
│   ├── transport.py            # Transport cost estimation
│   ├── profit_calculator.py    # Net profit calculation
│   └── market_selector.py      # Best mandi selection
│
├── data_access/                # Data layer
│   ├── __init__.py
│   ├── crop_metadata.py        # Crop characteristics (8 crops)
│   ├── mandi_data.py           # Market prices (5 mandis)
│   └── storage_data.py         # Storage facilities (7 locations)
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── geo.py                  # Haversine distance calculation
│   ├── time.py                 # Date helpers
│   └── units.py                # Unit conversions
│
├── cli_demo.py                 # Interactive demo
├── test_runner.py              # Automated tests
├── harvest_planner.py          # Legacy wrapper
├── README.md                   # Quick start guide
└── USAGE.md                    # Integration guide
```

---

## Core Components

### 1. PostHarvestDecisionEngine (core/engine.py)

**Purpose**: Main orchestrator that coordinates all decision modules.

**Key Method**:
```python
def run_decision(self, context: FarmerContext) -> DecisionResult:
    """
    Execute complete post-harvest decision workflow
    
    Args:
        context: FarmerContext with farmer input
    
    Returns:
        DecisionResult with storage and market recommendations
    
    Raises:
        ValueError: If crop not supported
    """
```

**Initialization**:
```python
engine = PostHarvestDecisionEngine()
# No configuration needed - uses mock data
```

**Usage Example**:
```python
from Post_Harvest_stage.core import FarmerContext, PostHarvestDecisionEngine
from datetime import date

context = FarmerContext(
    crop_name="onion",
    quantity_kg=1000,
    farmer_location=(18.52, 73.86),  # Pune coordinates
    harvest_date=date.today(),
    today_date=date.today()
)

engine = PostHarvestDecisionEngine()
result = engine.run_decision(context)

print(f"Decision: {result.storage_decision}")
print(f"Best Market: {result.best_market_name}")
print(f"Net Profit: ₹{result.net_profit:,.2f}")
print(f"Reasoning: {result.storage_reasoning}")
```

---

## Data Models

### Input Model

#### FarmerContext
```python
@dataclass
class FarmerContext:
    crop_name: str                  # Crop name (lowercase, e.g., "onion")
    quantity_kg: float              # Quantity in kilograms
    farmer_location: tuple          # (latitude, longitude)
    harvest_date: date              # When crop was harvested
    today_date: date                # Current date
```

**Example**:
```python
context = FarmerContext(
    crop_name="potato",
    quantity_kg=2000,
    farmer_location=(19.08, 72.88),  # Mumbai
    harvest_date=date(2026, 1, 15),
    today_date=date(2026, 1, 22)
)
```

### Output Model

#### DecisionResult
```python
@dataclass
class DecisionResult:
    # Storage Decision
    storage_decision: str                   # "sell_now" or "store_and_sell"
    recommended_wait_days: int              # Days to wait before selling
    spoilage_risk: str                      # "low" | "medium" | "high"
    max_safe_storage_days: int              # Maximum safe storage duration
    storage_type_recommended: str           # "open" or "cold"
    
    # Market Selection
    best_market_name: str                   # Name of best mandi
    best_market_location: tuple             # (lat, lon) of market
    market_price: float                     # Price at best market (₹/kg)
    transport_cost: float                   # Total transport cost (₹)
    storage_cost: float                     # Total storage cost (₹)
    net_profit: float                       # Net profit after all costs (₹)
    profit_margin_percent: float            # Profit margin percentage
    
    # Alternative Markets
    alternative_markets: List[dict]         # Top 3 alternative markets
    
    # Price Forecast
    current_price: float                    # Current market price (₹/kg)
    peak_price: float                       # Predicted peak price (₹/kg)
    peak_day: int                           # Day when peak price expected
    price_trend: str                        # "rising" | "falling" | "stable"
    
    # Reasoning
    storage_reasoning: str                  # Explanation of decision
    profit_improvement_percent: float       # % improvement from storing
```

---

## Storage Decision System

### 1. SpoilageRiskCalculator (storage/spoilage_model.py)

**Purpose**: Calculates spoilage risk and safe storage duration.

**Key Method**:
```python
def calculate_risk(
    self,
    crop_name: str,
    days_to_sell: int,
    storage_type: StorageType
) -> SpoilageAssessment:
    """
    Calculate spoilage risk for storing crop
    
    Args:
        crop_name: Name of the crop
        days_to_sell: Number of days until selling
        storage_type: OPEN or COLD storage
    
    Returns:
        SpoilageAssessment with risk level and safe days
    """
```

**Spoilage Risk Levels**:
```python
class SpoilageRisk(str, Enum):
    LOW = "low"         # < 50% of shelf life
    MEDIUM = "medium"   # 50-80% of shelf life
    HIGH = "high"       # > 80% of shelf life
```

**Crop Storage Durations**:
```python
| Crop    | Open Storage | Cold Storage |
| ------- | ------------ | ------------ |
| Onion   | 30 days      | 120 days     |
| Potato  | 45 days      | 150 days     |
| Tomato  | 7 days       | 21 days      |
| Wheat   | 180 days     | 365 days     |
| Rice    | 150 days     | 365 days     |
| Cotton  | 120 days     | 365 days     |
| Cabbage | 14 days      | 60 days      |
| Carrot  | 21 days      | 120 days     |
```

**Usage Example**:
```python
from Post_Harvest_stage.storage import SpoilageRiskCalculator
from Post_Harvest_stage.data_access import StorageType

calculator = SpoilageRiskCalculator()
assessment = calculator.calculate_risk(
    crop_name="tomato",
    days_to_sell=5,
    storage_type=StorageType.COLD
)

print(f"Risk Level: {assessment.risk_level.value}")
print(f"Max Safe Days: {assessment.max_safe_storage_days}")
print(f"Spoilage %: {assessment.spoilage_percentage:.1f}%")
```

### 2. StorageMatcher (storage/storage_options.py)

**Purpose**: Finds suitable storage facilities near farmer.

**Key Method**:
```python
def get_best_storage(
    self,
    farmer_location: tuple,
    crop_name: str,
    quantity_kg: float,
    storage_type: StorageType,
    days_needed: int
) -> Optional[StorageOption]:
    """
    Find best storage facility
    
    Args:
        farmer_location: (lat, lon)
        crop_name: Name of crop
        quantity_kg: Quantity to store
        storage_type: OPEN or COLD
        days_needed: Storage duration
    
    Returns:
        StorageOption with facility details and cost
        None if no suitable storage found
    """
```

**Storage Facilities Database** (7 locations):
- Pune Cold Storage (500 tons capacity)
- Mumbai Warehouse (1000 tons capacity)
- Nashik Storage (300 tons capacity)
- Aurangabad Facility (400 tons capacity)
- Kolhapur Storage (250 tons capacity)
- Pune Open Storage (2000 tons capacity)
- Mumbai Open Warehouse (3000 tons capacity)

**Cost Calculation**:
```python
# Cold Storage: ₹2/kg/day
# Open Storage: ₹0.5/kg/day

total_cost = quantity_kg * days_needed * rate_per_kg_per_day
```

### 3. StorageDecisionMaker (storage/storage_decision.py)

**Purpose**: Decides whether to sell now or store and sell later.

**Key Method**:
```python
def decide(
    self,
    quantity_kg: float,
    current_price: float,
    price_forecast: PriceForecastData,
    spoilage_assessment: SpoilageAssessment,
    storage_option: Optional[StorageOption],
    transport_cost: float
) -> StorageDecisionResult:
    """
    Make storage decision
    
    Decision Logic:
    1. If spoilage risk HIGH → SELL NOW
    2. If profit improvement < 10% → SELL NOW
    3. If no storage available → SELL NOW
    4. Else → STORE AND SELL
    
    Returns:
        StorageDecisionResult with decision and reasoning
    """
```

**Decision Tree**:
```
┌─────────────────────┐
│ Spoilage Risk HIGH? │
└──────┬──────────────┘
       │ Yes → SELL NOW
       │ No
       ▼
┌─────────────────────┐
│ Profit Improvement  │
│     < 10%?          │
└──────┬──────────────┘
       │ Yes → SELL NOW
       │ No
       ▼
┌─────────────────────┐
│ Storage Available?  │
└──────┬──────────────┘
       │ No → SELL NOW
       │ Yes
       ▼
┌─────────────────────┐
│ STORE AND SELL      │
└─────────────────────┘
```

---

## Market Selection System

### 1. PriceTrendForecaster (market/price_model.py)

**Purpose**: Forecasts price trends for crops.

**Key Method**:
```python
def forecast_prices(
    self,
    crop_name: str,
    mandi_name: str,
    days_ahead: int = 14
) -> PriceForecast:
    """
    Forecast price trend
    
    Args:
        crop_name: Name of crop
        mandi_name: Name of mandi
        days_ahead: Forecast horizon
    
    Returns:
        PriceForecast with current, peak price, and trend
    """
```

**Forecasting Logic**:
```python
# Deterministic trend-based model
# Not ML-based - uses seasonal patterns

if crop in ["onion", "potato"]:
    trend = "rising"  # Typically rise after harvest
    peak_price = current_price * 1.15
    peak_day = 7
elif crop in ["tomato", "cabbage"]:
    trend = "falling"  # Perishable, price drops
    peak_price = current_price * 0.95
    peak_day = 2
else:
    trend = "stable"
    peak_price = current_price
    peak_day = 0
```

**Supported Mandis** (5 markets):
- **Pune Mandi** (18.52°N, 73.86°E)
- **Mumbai Mandi** (19.08°N, 72.88°E)
- **Nashik Mandi** (20.00°N, 73.79°E)
- **Aurangabad Mandi** (19.88°N, 75.34°E)
- **Kolhapur Mandi** (16.71°N, 74.24°E)

### 2. TransportCostCalculator (market/transport.py)

**Purpose**: Estimates transport cost based on distance.

**Key Method**:
```python
def calculate_cost(
    self,
    farmer_location: tuple,
    mandi_location: tuple,
    quantity_kg: float
) -> float:
    """
    Calculate transport cost
    
    Formula:
    distance_km = haversine(farmer_location, mandi_location)
    cost = distance_km * quantity_kg * RATE_PER_KM_PER_KG
    
    RATE_PER_KM_PER_KG = ₹0.02
    
    Returns:
        Total transport cost in ₹
    """
```

**Example**:
```python
from Post_Harvest_stage.market import TransportCostCalculator

calculator = TransportCostCalculator()
cost = calculator.calculate_cost(
    farmer_location=(18.52, 73.86),  # Pune
    mandi_location=(19.08, 72.88),   # Mumbai
    quantity_kg=1000
)
# Distance: ~150 km
# Cost: 150 * 1000 * 0.02 = ₹3,000
```

### 3. ProfitCalculator (market/profit_calculator.py)

**Purpose**: Calculates net profit after all costs.

**Key Method**:
```python
def calculate_profit(
    self,
    quantity_kg: float,
    price_per_kg: float,
    transport_cost: float,
    storage_cost: float = 0.0
) -> ProfitDetails:
    """
    Calculate net profit
    
    Formula:
    gross_revenue = quantity_kg * price_per_kg
    total_cost = transport_cost + storage_cost
    net_profit = gross_revenue - total_cost
    profit_margin = (net_profit / gross_revenue) * 100
    
    Returns:
        ProfitDetails with breakdown
    """
```

### 4. MarketSelector (market/market_selector.py)

**Purpose**: Selects best market considering all costs.

**Key Method**:
```python
def select_best_market(
    self,
    farmer_location: tuple,
    crop_name: str,
    quantity_kg: float,
    storage_cost: float = 0.0
) -> MarketRecommendation:
    """
    Select market with highest net profit
    
    Process:
    1. Get all mandi prices for crop
    2. Calculate transport cost to each
    3. Calculate net profit for each
    4. Rank by net profit (not by price!)
    5. Return top market + alternatives
    
    Returns:
        MarketRecommendation with best and alternative markets
    """
```

**Important**: Selects by **net profit**, not highest price!

**Example**:
```python
Mandi A: Price ₹50/kg, Distance 200km
  → Net Profit: ₹46,000

Mandi B: Price ₹45/kg, Distance 50km
  → Net Profit: ₹44,000

Best Choice: Mandi A (higher net profit despite distance)
```

---

## Usage Patterns

### Pattern 1: Basic Decision Making

```python
from Post_Harvest_stage.core import FarmerContext, PostHarvestDecisionEngine
from datetime import date

# Create context
context = FarmerContext(
    crop_name="onion",
    quantity_kg=1000,
    farmer_location=(18.52, 73.86),  # Pune
    harvest_date=date.today(),
    today_date=date.today()
)

# Run engine
engine = PostHarvestDecisionEngine()
result = engine.run_decision(context)

# Display results
print(f"📦 Storage Decision: {result.storage_decision.upper()}")
print(f"⏳ Wait Days: {result.recommended_wait_days}")
print(f"⚠️  Spoilage Risk: {result.spoilage_risk.upper()}")
print(f"🏪 Best Market: {result.best_market_name}")
print(f"💰 Net Profit: ₹{result.net_profit:,.2f}")
print(f"📈 Price Trend: {result.price_trend.upper()}")
print(f"💡 Reasoning: {result.storage_reasoning}")
```

### Pattern 2: Comparing Multiple Crops

```python
from Post_Harvest_stage.core import FarmerContext, PostHarvestDecisionEngine
from datetime import date

engine = PostHarvestDecisionEngine()
crops = ["onion", "potato", "tomato", "wheat"]

for crop in crops:
    context = FarmerContext(
        crop_name=crop,
        quantity_kg=1000,
        farmer_location=(18.52, 73.86),
        harvest_date=date.today(),
        today_date=date.today()
    )
    
    result = engine.run_decision(context)
    
    print(f"\n{crop.upper()}:")
    print(f"  Decision: {result.storage_decision}")
    print(f"  Net Profit: ₹{result.net_profit:,.2f}")
    print(f"  Best Market: {result.best_market_name}")
```

### Pattern 3: Voice Assistant Integration

```python
def get_post_harvest_advice(
    crop: str,
    quantity: float,
    location: tuple
) -> dict:
    """
    Voice assistant endpoint
    Returns voice-ready advice
    """
    from Post_Harvest_stage.core import FarmerContext, PostHarvestDecisionEngine
    from datetime import date
    
    context = FarmerContext(
        crop_name=crop.lower(),
        quantity_kg=quantity,
        farmer_location=location,
        harvest_date=date.today(),
        today_date=date.today()
    )
    
    engine = PostHarvestDecisionEngine()
    result = engine.run_decision(context)
    
    # Format for voice output
    if result.storage_decision == "sell_now":
        advice = f"आपको अपनी {crop} अभी बेचनी चाहिए। "
        advice += f"सबसे अच्छा बाजार {result.best_market_name} है। "
        advice += f"आपको ₹{result.net_profit:,.0f} का शुद्ध लाभ होगा। "
        advice += f"कारण: {result.storage_reasoning}"
    else:
        advice = f"आपको {result.recommended_wait_days} दिन इंतजार करना चाहिए। "
        advice += f"कीमत बढ़ने की संभावना है। "
        advice += f"₹{result.storage_cost:,.0f} का भंडारण खर्च होगा। "
        advice += f"लेकिन {result.profit_improvement_percent:.1f}% अधिक लाभ होगा।"
    
    return {
        "speech_text": advice,
        "decision": result.storage_decision,
        "net_profit": result.net_profit,
        "best_market": result.best_market_name,
        "raw_data": result
    }

# Usage
advice = get_post_harvest_advice(
    crop="Onion",
    quantity=1000,
    location=(18.52, 73.86)
)
print(advice["speech_text"])
```

### Pattern 4: Alternative Market Analysis

```python
from Post_Harvest_stage.core import FarmerContext, PostHarvestDecisionEngine
from datetime import date

context = FarmerContext(
    crop_name="potato",
    quantity_kg=2000,
    farmer_location=(18.52, 73.86),
    harvest_date=date.today(),
    today_date=date.today()
)

engine = PostHarvestDecisionEngine()
result = engine.run_decision(context)

# Display all market options
print(f"Best Market: {result.best_market_name}")
print(f"  Price: ₹{result.market_price}/kg")
print(f"  Transport: ₹{result.transport_cost:,.2f}")
print(f"  Net Profit: ₹{result.net_profit:,.2f}")

print("\nAlternative Markets:")
for i, alt in enumerate(result.alternative_markets, 1):
    print(f"{i}. {alt['market_name']}")
    print(f"   Distance: {alt['distance_km']:.1f} km")
    print(f"   Price: ₹{alt['price']}/kg")
    print(f"   Net Profit: ₹{alt['net_profit']:,.2f}")
```

---

## Integration Guide

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from Post_Harvest_stage.core import FarmerContext, PostHarvestDecisionEngine

app = FastAPI()
engine = PostHarvestDecisionEngine()

class HarvestInput(BaseModel):
    crop_name: str
    quantity_kg: float
    latitude: float
    longitude: float
    harvest_date: str  # ISO format

@app.post("/api/post-harvest/decision")
async def get_decision(input: HarvestInput):
    try:
        context = FarmerContext(
            crop_name=input.crop_name.lower(),
            quantity_kg=input.quantity_kg,
            farmer_location=(input.latitude, input.longitude),
            harvest_date=date.fromisoformat(input.harvest_date),
            today_date=date.today()
        )
        
        result = engine.run_decision(context)
        
        return {
            "storage_decision": result.storage_decision,
            "recommended_wait_days": result.recommended_wait_days,
            "best_market": result.best_market_name,
            "net_profit": result.net_profit,
            "reasoning": result.storage_reasoning,
            "alternatives": result.alternative_markets
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/post-harvest/supported-crops")
async def get_supported_crops():
    return {
        "crops": ["onion", "potato", "tomato", "wheat", "rice", "cotton", "cabbage", "carrot"]
    }
```

### LLM/RAG Integration

```python
def generate_natural_language_advice(result: DecisionResult) -> str:
    """
    Convert structured decision to natural language
    Can be enhanced with LLM for better explanations
    """
    prompt = f"""
    Generate farmer-friendly advice based on this data:
    
    Crop: {result.crop_name}
    Decision: {result.storage_decision}
    Wait Days: {result.recommended_wait_days}
    Spoilage Risk: {result.spoilage_risk}
    Best Market: {result.best_market_name}
    Net Profit: ₹{result.net_profit:,.2f}
    Price Trend: {result.price_trend}
    Reasoning: {result.storage_reasoning}
    
    Generate concise Hindi advice for voice output.
    """
    
    # Send to LLM (Gemini, GPT, etc.)
    # llm_response = llm.generate(prompt)
    
    # For now, return structured text
    return result.storage_reasoning
```

---

## Extension Points

### Adding New Crops

Edit `data_access/crop_metadata.py`:

```python
CROP_DATABASE = {
    # ... existing crops ...
    "newcrop": CropMetadata(
        name="NewCrop",
        open_storage_days=60,
        cold_storage_days=180,
        spoilage_sensitivity=SpoilageSensitivity.MEDIUM
    )
}
```

Edit `data_access/mandi_data.py`:

```python
MANDI_PRICES = {
    "Pune Mandi": {
        # ... existing crops ...
        "newcrop": 45.0  # Price per kg
    },
    # ... other mandis ...
}
```

### Adding New Mandis

Edit `data_access/mandi_data.py`:

```python
MANDI_DATABASE = {
    # ... existing mandis ...
    "New Mandi": MandiInfo(
        name="New Mandi",
        location=(lat, lon),
        district="District Name"
    )
}

MANDI_PRICES = {
    # ... existing mandis ...
    "New Mandi": {
        "onion": 35.0,
        "potato": 25.0,
        # ... all crops
    }
}
```

### Adding New Storage Facilities

Edit `data_access/storage_data.py`:

```python
STORAGE_FACILITIES = [
    # ... existing facilities ...
    StorageFacility(
        name="New Storage",
        location=(lat, lon),
        storage_type=StorageType.COLD,
        capacity_kg=500000,  # 500 tons
        rate_per_kg_per_day=2.0
    )
]
```

### Customizing Decision Logic

Edit `storage/storage_decision.py`:

```python
def decide(self, ...) -> StorageDecisionResult:
    # Add custom logic
    if crop_name == "special_crop":
        # Custom decision for special crop
        return StorageDecisionResult(...)
    
    # Default logic
    # ...
```

---

## Testing

### Running Tests

```bash
# From Farm_management directory
cd Backend/Farm_management
python -m Post_Harvest_stage.test_runner

# Or use CLI demo
python -m Post_Harvest_stage.cli_demo
```

### Test Scenarios

The module includes 4 predefined test scenarios:

1. **Onion + Rising Prices** → Should recommend storage
2. **Tomato + High Spoilage** → Should recommend immediate sale
3. **Potato + Distant Market** → Should select nearest mandi
4. **Wheat + Stable Prices** → Should recommend immediate sale

### Manual Testing

```python
from Post_Harvest_stage.core import FarmerContext, PostHarvestDecisionEngine
from datetime import date

# Test different scenarios
scenarios = [
    ("onion", 1000, "Should store - prices rising"),
    ("tomato", 500, "Should sell - high spoilage"),
    ("wheat", 2000, "Should sell - stable prices"),
]

engine = PostHarvestDecisionEngine()

for crop, qty, expected in scenarios:
    context = FarmerContext(
        crop_name=crop,
        quantity_kg=qty,
        farmer_location=(18.52, 73.86),
        harvest_date=date.today(),
        today_date=date.today()
    )
    
    result = engine.run_decision(context)
    print(f"{crop}: {result.storage_decision} - {expected}")
```

---

## Production Checklist

### Before Deployment

- [ ] Integrate with real mandi price APIs
- [ ] Connect to live storage facility database
- [ ] Implement real-time price forecasting (ML model)
- [ ] Add authentication for API endpoints
- [ ] Set up monitoring and logging
- [ ] Implement caching for price data
- [ ] Add rate limiting
- [ ] Configure error tracking
- [ ] Set up database for storing decisions
- [ ] Implement notification system for price alerts

### Environment Variables

```bash
MANDI_API_KEY=your_api_key
STORAGE_DB_URI=mongodb://localhost:27017
PRICE_FORECAST_MODEL_PATH=/path/to/model
```

---

## Performance Considerations

### Complexity
- Spoilage calculation: O(1)
- Market selection: O(m) where m = number of mandis (typically 5-10)
- Overall decision: O(m) - linear time

### Optimization Tips
1. Cache mandi prices (TTL: 1 hour)
2. Cache storage facility data (TTL: 24 hours)
3. Use database indexes on crop_name, mandi_name
4. Implement async API calls for price fetching
5. Pre-calculate distances for common farmer-mandi pairs

---

## Troubleshooting

### Common Issues

**Issue**: Crop not supported
```python
# Solution: Check supported crops
from Post_Harvest_stage.data_access import get_crop_metadata
metadata = get_crop_metadata("your_crop")
if not metadata:
    print("Crop not supported. Add to crop_metadata.py")
```

**Issue**: No storage available
```python
# Solution: Decision will default to "sell_now"
# Check storage facilities in storage_data.py
```

**Issue**: All markets show same price
```python
# Solution: Using mock data
# Integrate with real mandi price API
```

---

## Support and Maintenance

### Code Quality
- ✅ Type hints throughout
- ✅ Dataclass validation
- ✅ Comprehensive error handling
- ✅ Modular, testable design
- ✅ PEP 8 compliant
- ✅ Zero external dependencies

### Documentation
- ✅ Inline code documentation
- ✅ README with quick start
- ✅ USAGE guide for integration
- ✅ This comprehensive codebase guide
- ✅ CLI demo for exploration

---

**Last Updated**: January 2026  
**Version**: 1.0  
**Status**: Production-Quality Demo Code  
**Dependencies**: None (Pure Python Standard Library)
