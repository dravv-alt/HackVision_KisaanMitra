# Inventory Management Module

## Overview

A comprehensive **pure backend module** for inventory management in the Voice-First Farming Assistant. This module provides stock tracking, shelf-life management, health monitoring, and intelligent sell priority recommendations for Indian farmers.

## ✨ Features

- **Stock Tracking**: Monitor all inventory items with quantity, grade, and storage details
- **Shelf-Life Countdown**: Automatic expiry calculation and risk assessment
- **Health Status**: Real-time health monitoring (Good/Warning/Critical)
- **Sell Priority Intelligence**: AI-driven ranking to minimize waste
- **Market-Aware**: Considers market price trends for sell recommendations
- **Bilingual Support**: Hindi and English voice outputs
- **Mock Fallback**: 100% demo reliability with automatic mock data
- **Repository Pattern**: Clean architecture ready for MongoDB integration

## 🏗️ Architecture

```
Inventory/
├── __init__.py                 # Module exports
├── constants.py                # Enums and configuration
├── models.py                   # Pydantic data models
├── service.py                  # Main orchestration layer
├── cli_demo.py                 # Interactive testing tool
├── repositories/               # Data access layer
│   ├── farmer_repo.py         # Farmer profiles
│   ├── inventory_repo.py      # Stock items
│   ├── inventory_log_repo.py  # Action logs
│   ├── market_repo.py         # Price data
│   ├── alert_repo.py          # Reminders
│   └── audit_repo.py          # Debug logs
└── engines/                    # Business logic
    ├── stock_engine.py        # Stock state management
    ├── shelf_life_engine.py   # Expiry calculations
    ├── health_engine.py       # Health assessment
    ├── sell_priority_engine.py # Priority ranking
    ├── reminder_engine.py     # Alert generation
    └── response_builder.py    # UI output formatting
```

## 🚀 Quick Start

### Basic Usage

```python
from Inventory.service import InventoryService

# Initialize service
service = InventoryService()

# Get inventory dashboard
output = service.get_inventory_dashboard("FARMER001")

# Access data
print(f"Total items: {output.totalStockCount}")
print(f"Speech: {output.speechText}")

# Iterate through stock cards
for card in output.stockCards:
    print(f"{card.cropName}: {card.quantityKg} kg")
    print(f"Priority: #{card.sellPriorityRank}")
    print(f"Sell now: {card.sellNowRecommendation}")
```

### Simulate Actions

```python
# Simulate selling stock
updated = service.simulate_sell_action(
    farmer_id="FARMER001",
    item_id="item-123",
    quantity_kg=50.0,
    price_per_kg=30.0
)

# Simulate spoilage
updated = service.simulate_spoilage_action(
    farmer_id="FARMER001",
    item_id="item-123",
    quantity_kg=10.0,
    notes="Moisture damage"
)
```

## 🧪 Testing

### Run CLI Demo

```bash
# Automated demo
cd Backend
python -m Inventory.cli_demo

# Interactive mode
python -m Inventory.cli_demo --interactive
```

### Run Quick Test

```bash
cd Backend
python test_inventory.py
```

## 📊 Data Models

### InventoryModuleOutput

Main output model for UI integration:

```python
{
    "header": "Inventory Dashboard - 5 Items",
    "language": "hi",
    "speechText": "आपके पास 5 स्टॉक आइटम हैं...",
    "stockCards": [...],
    "totalStockCount": 5,
    "warningCount": 2,
    "criticalCount": 1,
    "urgencyLevel": "high"
}
```

### StockCardOutput

Individual stock item card:

```python
{
    "itemId": "uuid",
    "cropName": "Tomato",
    "quantityKg": 150.0,
    "grade": "A",
    "shelfLifeRemainingDays": 2,
    "healthStatus": "critical",
    "sellPriorityRank": 1,
    "sellNowRecommendation": true,
    "reasons": ["Only 2 days until expiry", "High spoilage risk"],
    "suggestedNextAction": "Sell immediately at current market price"
}
```

## 🔌 FastAPI Integration

### Example Endpoint

```python
from fastapi import FastAPI
from Inventory import InventoryService

app = FastAPI()
service = InventoryService()

@app.get("/api/inventory/{farmer_id}")
async def get_inventory(farmer_id: str):
    """Get inventory dashboard"""
    output = service.get_inventory_dashboard(farmer_id)
    return output.dict()

@app.post("/api/inventory/{farmer_id}/sell")
async def sell_stock(farmer_id: str, item_id: str, quantity: float):
    """Record sell action"""
    output = service.simulate_sell_action(
        farmer_id, item_id, quantity
    )
    return output.dict()
```

## 🎯 Sell Priority Algorithm

Items are ranked based on:

1. **Health Status** (100 points)
   - Critical: Full weight
   - Warning: 60% weight
   - Good: 0 points

2. **Shelf Life** (50 points)
   - ≤3 days: Full weight
   - ≤7 days: 70% weight
   - ≤14 days: 40% weight

3. **Spoilage Risk** (30 points)
   - High: Full weight
   - Medium: 50% weight
   - Low: 0 points

4. **Market Trend** (20 points)
   - Falling: +20 (sell urgently)
   - Rising + Cold Storage: -10 (can wait)

## 📝 Shelf Life Data

Default shelf life (in days):

| Crop | Days | Crop | Days |
|------|------|------|------|
| Tomato | 7 | Potato | 60 |
| Onion | 30 | Wheat | 180 |
| Rice | 240 | Cotton | 365 |
| Groundnut | 90 | Garlic | 45 |

## 🌐 Bilingual Support

### Hindi Example
```
"आपके पास 4 स्टॉक आइटम हैं। 2 आइटम खतरनाक स्थिति में हैं, 
उन्हें तुरंत बेचना चाहिए। Tomato की शेल्फ लाइफ केवल 2 दिन बची है।"
```

### English Example
```
"You have 4 stock items. 2 items are in critical condition and should 
be sold immediately. Tomato has only 2 days shelf life remaining."
```

## 🛡️ Error Handling

The module is designed for **100% hackathon reliability**:

- ✅ Automatic mock data if DB is empty
- ✅ Graceful fallbacks for missing market data
- ✅ No crashes on invalid inputs
- ✅ Deterministic behavior for demos

## 🔧 Configuration

### Constants (constants.py)

```python
# Adjust risk thresholds
SHELF_LIFE_HIGH_RISK_DAYS = 3
SHELF_LIFE_MEDIUM_RISK_DAYS = 7

# Adjust priority weights
PRIORITY_WEIGHT_HEALTH = 100
PRIORITY_WEIGHT_SHELF_LIFE = 50
PRIORITY_WEIGHT_SPOILAGE_RISK = 30
PRIORITY_WEIGHT_MARKET_TREND = 20
```

## 📦 Dependencies

```
pydantic>=2.0.0
```

No external API dependencies - fully self-contained!

## 🎬 Demo Scenarios

The module includes realistic mock data:

1. **Critical Item**: Tomato with 2 days shelf life
2. **Warning Item**: Onion with 6 days shelf life
3. **Good Items**: Potato, Wheat with long shelf life
4. **Partial Sold**: Groundnut with sales history

## 🚀 Production Deployment

### MongoDB Integration

Replace mock repositories with real MongoDB clients:

```python
# In inventory_repo.py
from pymongo import MongoClient

class InventoryRepo:
    def __init__(self, db_client):
        self.collection = db_client.inventory_items
    
    def list_items(self, farmer_id):
        items = self.collection.find({"farmerId": farmer_id})
        return [InventoryItem(**item) for item in items]
```

### Environment Variables

```bash
MONGODB_URI=mongodb://localhost:27017
DB_NAME=kissan_mitra
ENABLE_MOCK_FALLBACK=false
```

## 📈 Future Enhancements

- [ ] Real-time price API integration
- [ ] Weather-based shelf life adjustment
- [ ] Batch operations for multiple items
- [ ] Export to CSV/PDF reports
- [ ] SMS/WhatsApp reminder integration
- [ ] Analytics dashboard

## 🤝 Contributing

This module follows clean architecture principles:

1. **Repositories**: Data access only
2. **Engines**: Pure business logic
3. **Service**: Orchestration layer
4. **Models**: Type-safe data structures

## 📄 License

Part of the KissanMitra HackVision project.

## 🆘 Support

For issues or questions:
1. Check the CLI demo: `python -m Inventory.cli_demo --interactive`
2. Run tests: `python test_inventory.py`
3. Review audit logs in `AuditRepo`

---

**Built for HackVision 2026** 🏆
*Empowering Indian farmers with intelligent inventory management*
