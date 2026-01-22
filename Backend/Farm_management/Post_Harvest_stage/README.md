# Post-Harvest Decision Engine

Voice-ready decision intelligence module for farmers to optimize storage and market selection decisions.

## Overview

This module provides **pure decision logic** for post-harvest crop management:
1. **Storage Decision**: Should the farmer sell now or store and sell later?
2. **Market Recommendation**: Which mandi gives the best net profit?

The output is **structured data** ready for a voice interface layer.

## Features

✅ **Spoilage Risk Analysis** - Calculates safe storage duration based on crop characteristics  
✅ **Price Forecasting** - Deterministic trend-based price predictions (no heavy ML)  
✅ **Profit Optimization** - Selects best market considering transport and storage costs  
✅ **Connected Decision Logic** - Integrated analysis, not separate rules  
✅ **Hackathon-Ready** - Mock data, no external dependencies, reliable

## Module Structure

```
Post_Harvest_stage/
├── core/
│   ├── context.py          # Farmer input context
│   ├── engine.py            # Main decision orchestrator
├── storage/
│   ├── spoilage_model.py   # Shelf life & risk calculation
│   ├── storage_options.py  # Storage facility matching
│   ├── storage_decision.py # Sell vs Store logic
├── market/
│   ├── price_model.py      # Price trend forecasting
│   ├── transport.py        # Transport cost estimation
│   ├── profit_calculator.py# Net profit calculation
│   ├── market_selector.py  # Best mandi selection
├── data_access/
│   ├── crop_metadata.py    # Crop characteristics (8 crops)
│   ├── mandi_data.py       # Market prices (5 mandis)
│   ├── storage_data.py     # Storage facilities (7 locations)
├── utils/
│   ├── geo.py              # Haversine distance calculation
│   ├── time.py             # Date helpers
│   ├── units.py            # Unit conversions
└── cli_demo.py             # Test & demo script
```

## Quick Start

### Run Predefined Test Scenarios

```bash
cd Post_Harvest_stage
python cli_demo.py
```

### Interactive Mode

```bash
python cli_demo.py --interactive
```

## Supported Crops

- **Onion** (30 days open / 120 days cold)
- **Potato** (45 days open / 150 days cold)
- **Tomato** (7 days open / 21 days cold) - High spoilage risk
- **Wheat** (180 days open / 365 days cold)
- **Rice** (150 days open / 365 days cold)
- **Cotton** (120 days open / 365 days cold)
- **Cabbage** (14 days open / 60 days cold)
- **Carrot** (21 days open / 120 days cold)

## Supported Mandis

- **Pune Mandi** (18.52°N, 73.86°E)
- **Mumbai Mandi** (19.08°N, 72.88°E)
- **Nashik Mandi** (20.00°N, 73.79°E)
- **Aurangabad Mandi** (19.88°N, 75.34°E)
- **Kolhapur Mandi** (16.71°N, 74.24°E)

## Example Usage

```python
from core import FarmerContext, PostHarvestDecisionEngine
from datetime import date

# Create context
context = FarmerContext(
    crop_name="onion",
    quantity_kg=1000,
    farmer_location=(18.52, 73.86),  # Pune
    harvest_date=date.today(),
    today_date=date.today()
)

# Run decision engine
engine = PostHarvestDecisionEngine()
result = engine.run_decision(context)

# Access structured output
print(f"Decision: {result.storage_decision}")
print(f"Best Market: {result.best_market_name}")
print(f"Net Profit: ₹{result.net_profit}")
```

## Decision Output Structure

```python
@dataclass
class DecisionResult:
    # Storage Decision
    storage_decision: str              # "sell_now" or "store_and_sell"
    recommended_wait_days: int
    spoilage_risk: str                 # "low", "medium", "high"
    max_safe_storage_days: int
    
    # Market Selection
    best_market_name: str
    market_price: float
    transport_cost: float
    storage_cost: float
    net_profit: float
    
    # Price Forecast
    current_price: float
    peak_price: float
    peak_day: int
    price_trend: str                   # "rising", "falling", "stable"
    
    # Reasoning
    storage_reasoning: str
    profit_improvement_percent: float
```

## Decision Logic

### Storage Decision

```
IF spoilage_risk == HIGH:
    → SELL NOW

ELIF profit_improvement < 10%:
    → SELL NOW (not worth storage cost)

ELIF no_storage_available:
    → SELL NOW

ELSE:
    → STORE until peak price day
```

### Market Selection

```
For each mandi:
    1. Get current price
    2. Calculate transport cost
    3. Calculate net_profit = (price × quantity) - transport - storage

Select mandi with HIGHEST net_profit (not highest price!)
```

## Dependencies

**None!** Uses only Python standard library:
- `dataclasses` - Structured data
- `datetime` - Date operations
- `math` - Distance calculations
- `typing` - Type hints

## Extending the Module

### Add New Crop

Edit `data_access/crop_metadata.py`:
```python
"newcrop": CropMetadata(
    name="NewCrop",
    open_storage_days=X,
    cold_storage_days=Y,
    spoilage_sensitivity=SpoilageSensitivity.MEDIUM
)
```

### Add New Mandi

Edit `data_access/mandi_data.py`:
```python
"newmandi": MandiInfo(
    name="New Mandi",
    location=(lat, lon),
    district="District"
)
```

### Integrate with LLM/RAG

The `DecisionResult` dataclass can be easily converted to JSON and passed to an LLM for natural language explanation generation.

## Test Scenarios

1. **Onion + Rising Prices** → Should recommend storage
2. **Tomato + High Spoilage** → Should recommend immediate sale
3. **Potato + Distant Market** → Should select nearest mandi
4. **Wheat + Stable Prices** → Should recommend immediate sale

## Architecture Principles

- **Clean Separation**: Data / Storage / Market / Core layers
- **Deterministic**: Same input always produces same output
- **Explainable**: Every decision has clear reasoning
- **Testable**: Pure functions, no side effects
- **Extensible**: Easy to add LLM or real APIs later

## Notes

- All prices in Indian Rupees (₹)
- Distance in kilometers
- Weight in kilograms
- Mock data designed for realistic hackathon demos
- Voice explanation layer handled externally

---

**Built for**: Voice-First Farming Assistant Hackathon  
**Type**: Decision Intelligence Module (No API/Frontend)  
**Status**: Production-Quality Demo Code
