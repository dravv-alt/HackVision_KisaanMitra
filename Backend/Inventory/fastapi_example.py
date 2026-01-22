"""
FastAPI Integration Example for Inventory Module

This file demonstrates how to integrate the Inventory module with FastAPI.
Copy these endpoints to your main FastAPI application.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Import the Inventory service
import sys
sys.path.insert(0, 'D:\\KissanMitra\\HackVision_KisaanMitra\\Backend')
from Inventory import InventoryService, InventoryModuleOutput

# Initialize FastAPI app
app = FastAPI(
    title="KissanMitra Inventory API",
    description="Inventory Management API for Voice-First Farming Assistant",
    version="1.0.0"
)

# Initialize service (singleton)
inventory_service = InventoryService()


# Request/Response models for API
class SellRequest(BaseModel):
    """Request model for sell action"""
    item_id: str
    quantity_kg: float
    price_per_kg: Optional[float] = None
    notes: Optional[str] = None


class SpoilageRequest(BaseModel):
    """Request model for spoilage action"""
    item_id: str
    quantity_kg: float
    notes: Optional[str] = None


class ActionResponse(BaseModel):
    """Response model for actions"""
    success: bool
    message: str
    updated_dashboard: InventoryModuleOutput


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "service": "KissanMitra Inventory API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/api/inventory/{farmer_id}",
            "/api/inventory/{farmer_id}/sell",
            "/api/inventory/{farmer_id}/spoilage"
        ]
    }


@app.get("/api/inventory/{farmer_id}", response_model=InventoryModuleOutput)
async def get_inventory_dashboard(
    farmer_id: str,
    include_reminders: bool = Query(True, description="Generate expiry reminders")
):
    """
    Get complete inventory dashboard for a farmer
    
    **Parameters:**
    - farmer_id: Unique farmer identifier
    - include_reminders: Whether to generate and save expiry reminders
    
    **Returns:**
    - Complete inventory dashboard with stock cards, speech text, and analytics
    
    **Example:**
    ```
    GET /api/inventory/FARMER001?include_reminders=true
    ```
    """
    try:
        output = inventory_service.get_inventory_dashboard(
            farmer_id,
            include_reminders=include_reminders
        )
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/inventory/{farmer_id}/sell")
async def sell_stock(
    farmer_id: str,
    request: SellRequest
):
    """
    Record a sell action and get updated dashboard
    
    **Parameters:**
    - farmer_id: Unique farmer identifier
    - request: Sell action details (item_id, quantity, price)
    
    **Returns:**
    - Success status and updated inventory dashboard
    
    **Example:**
    ```json
    POST /api/inventory/FARMER001/sell
    {
        "item_id": "uuid-123",
        "quantity_kg": 50.0,
        "price_per_kg": 30.0,
        "notes": "Sold at local mandi"
    }
    ```
    """
    try:
        updated_dashboard = inventory_service.simulate_sell_action(
            farmer_id=farmer_id,
            item_id=request.item_id,
            quantity_kg=request.quantity_kg,
            price_per_kg=request.price_per_kg
        )
        
        return ActionResponse(
            success=True,
            message=f"Successfully sold {request.quantity_kg} kg",
            updated_dashboard=updated_dashboard
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/inventory/{farmer_id}/spoilage")
async def record_spoilage(
    farmer_id: str,
    request: SpoilageRequest
):
    """
    Record spoilage and get updated dashboard
    
    **Parameters:**
    - farmer_id: Unique farmer identifier
    - request: Spoilage details (item_id, quantity, notes)
    
    **Returns:**
    - Success status and updated inventory dashboard
    
    **Example:**
    ```json
    POST /api/inventory/FARMER001/spoilage
    {
        "item_id": "uuid-123",
        "quantity_kg": 10.0,
        "notes": "Moisture damage during storage"
    }
    ```
    """
    try:
        updated_dashboard = inventory_service.simulate_spoilage_action(
            farmer_id=farmer_id,
            item_id=request.item_id,
            quantity_kg=request.quantity_kg,
            notes=request.notes
        )
        
        return ActionResponse(
            success=True,
            message=f"Recorded {request.quantity_kg} kg spoilage",
            updated_dashboard=updated_dashboard
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/inventory/{farmer_id}/summary")
async def get_inventory_summary(farmer_id: str):
    """
    Get quick inventory summary (lightweight endpoint)
    
    **Parameters:**
    - farmer_id: Unique farmer identifier
    
    **Returns:**
    - Quick summary with counts and urgency level
    """
    try:
        output = inventory_service.get_inventory_dashboard(
            farmer_id,
            include_reminders=False
        )
        
        return {
            "farmer_id": farmer_id,
            "total_items": output.totalStockCount,
            "warning_count": output.warningCount,
            "critical_count": output.criticalCount,
            "urgency_level": output.urgencyLevel.value,
            "speech_text": output.speechText,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/inventory/{farmer_id}/priority-list")
async def get_priority_list(farmer_id: str, limit: int = Query(10, ge=1, le=100)):
    """
    Get sell priority list (top N items to sell)
    
    **Parameters:**
    - farmer_id: Unique farmer identifier
    - limit: Maximum number of items to return (1-100)
    
    **Returns:**
    - List of top priority items with sell recommendations
    """
    try:
        output = inventory_service.get_inventory_dashboard(
            farmer_id,
            include_reminders=False
        )
        
        priority_items = []
        for card in output.stockCards[:limit]:
            priority_items.append({
                "rank": card.sellPriorityRank,
                "crop_name": card.cropName,
                "quantity_kg": card.quantityKg,
                "shelf_life_days": card.shelfLifeRemainingDays,
                "health_status": card.healthStatus.value,
                "sell_now": card.sellNowRecommendation,
                "reasons": card.reasons,
                "suggested_action": card.suggestedNextAction
            })
        
        return {
            "farmer_id": farmer_id,
            "priority_items": priority_items,
            "total_items": output.totalStockCount
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "inventory",
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 80)
    print("  KISSAN MITRA - INVENTORY API")
    print("=" * 80)
    print("\n📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Interactive API: http://localhost:8000/redoc")
    print("\n🚀 Starting server...\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
