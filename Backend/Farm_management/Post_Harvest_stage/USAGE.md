# Post-Harvest Decision Engine - Usage Guide

## Running the Module

The Post-Harvest Decision Engine uses relative imports, so it needs to be imported as a package, not run directly.

### Option 1: Import from Parent Directory

```bash
cd Backend/Farm_management
python -c "from Post_Harvest_stage.test_runner import main; main()"
```

### Option 2: Use Python Module Syntax

```bash
cd Backend/Farm_management
python -m Post_Harvest_stage.test_runner
```

### Option 3: Integration with Your Voice Agent

```python
# In your FastAPI/Voice Agent code:
import sys
sys.path.append('path/to/Backend/Farm_management')

from Post_Harvest_stage.core import FarmerContext, PostHarvestDecisionEngine
from datetime import date

# Create farmer context
context = FarmerContext(
    crop_name="onion",
    quantity_kg=1000,
    farmer_location=(18.52, 73.86),
    harvest_date=date.today(),
    today_date=date.today()
)

# Run decision engine
engine = PostHarvestDecisionEngine()
result = engine.run_decision(context)

# Use structured output
decision_data = {
    "storage_decision": result.storage_decision,
    "wait_days": result.recommended_wait_days,
    "best_market": result.best_market_name,
    "net_profit": result.net_profit,
    "reasoning": result.storage_reasoning
}

# Pass to your voice/LLM layer for natural language generation
```

## Module Output Structure

The engine returns a `DecisionResult` dataclass with all decision data:

```python
{
    # Storage Decision
    "storage_decision": "sell_now" or "store_and_sell",
    "recommended_wait_days": int,
    "spoilage_risk": "low" | "medium" | "high",
    "max_safe_storage_days": int,
    
    # Market Recommendation
    "best_market_name": str,
    "market_price": float,
    "transport_cost": float,
    "storage_cost": float,
    "net_profit": float,
    
    # Price Data
    "current_price": float,
    "peak_price": float,
    "peak_day": int,
    "price_trend": "rising" | "falling" | "stable",
    
    # Reasoning
    "storage_reasoning": str,
    "profit_improvement_percent": float
}
```

## Example Integration

```python
# Your Voice Agent endpoint
@app.post("/post-harvest-advice")
async def get_harvest_advice(farmer_input: dict):
    # Parse voice input to context
    context = FarmerContext(
        crop_name=farmer_input["crop"],
        quantity_kg=farmer_input["quantity"],
        farmer_location=farmer_input["location"],
        harvest_date=farmer_input["harvest_date"],
        today_date=date.today()
    )
    
    # Get decision
    engine = PostHarvestDecisionEngine()
    result = engine.run_decision(context)
    
    # Convert to voice output (your layer)
    voice_response = generate_voice_explanation(result)
    
    return {"advice": voice_response, "raw_data": result}
```

## No External Dependencies

The module uses only Python standard library - no pip installs needed beyond what you already have.

---

**Note**: The module is designed as a decision intelligence layer. Voice explanation/TTS is handled by your external voice agent layer.
