"""
Inventory Management API Router
Handles inventory items (seeds, fertilizers, tools, equipment)
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from Backend.api.dependencies import get_db_client

router = APIRouter(prefix="/inventory", tags=["Inventory"])

# Request/Response Models
class InventoryItem(BaseModel):
    item_id: Optional[str] = None
    farmer_id: str
    category: str  # seeds, fertilizers, pesticides, tools, equipment
    name: str
    quantity: float
    unit: str  # kg, liters, pieces, etc.
    cost_per_unit: float
    total_cost: float
    purchase_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    supplier: Optional[str] = None
    notes: Optional[str] = None
    status: str = "in_stock"  # in_stock, low_stock, out_of_stock
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class AddItemRequest(BaseModel):
    farmer_id: str
    category: str
    name: str
    quantity: float
    unit: str
    cost_per_unit: float
    purchase_date: Optional[str] = None
    expiry_date: Optional[str] = None
    supplier: Optional[str] = None
    notes: Optional[str] = None

class UseItemRequest(BaseModel):
    quantity: float

class RestockItemRequest(BaseModel):
    quantity: float
    cost_per_unit: Optional[float] = None

# API Endpoints

@router.get("/items/{farmer_id}")
async def get_inventory_items(
    farmer_id: str,
    category: Optional[str] = None,
    db_client = Depends(get_db_client)
):
    """
    Get all inventory items for a farmer
    
    - **farmer_id**: Farmer ID
    - **category**: Optional filter by category
    """
    try:
        db = db_client["kisanmitra"]
        
        # Build query
        query = {"farmer_id": farmer_id}
        if category:
            query["category"] = category
        
        # Fetch items
        items = list(db.inventory.find(query))
        
        # Convert ObjectId to string
        for item in items:
            item["_id"] = str(item["_id"])
            if "item_id" not in item:
                item["item_id"] = item["_id"]
        
        return {
            "success": True,
            "items": items,
            "count": len(items)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add")
async def add_inventory_item(
    request: AddItemRequest,
    db_client = Depends(get_db_client)
):
    """
    Add new inventory item
    
    - **farmer_id**: Farmer ID
    - **category**: Item category (seeds, fertilizers, etc.)
    - **name**: Item name
    - **quantity**: Quantity
    - **unit**: Unit of measurement
    - **cost_per_unit**: Cost per unit
    """
    try:
        db = db_client["kisanmitra"]
        
        # Calculate total cost
        total_cost = request.quantity * request.cost_per_unit
        
        # Determine status based on quantity
        if request.quantity == 0:
            status = "out_of_stock"
        elif request.quantity < 10:  # Threshold for low stock
            status = "low_stock"
        else:
            status = "in_stock"
        
        # Create item
        item = {
            "farmer_id": request.farmer_id,
            "category": request.category,
            "name": request.name,
            "quantity": request.quantity,
            "unit": request.unit,
            "cost_per_unit": request.cost_per_unit,
            "total_cost": total_cost,
            "purchase_date": request.purchase_date or datetime.utcnow().isoformat(),
            "expiry_date": request.expiry_date,
            "supplier": request.supplier,
            "notes": request.notes,
            "status": status,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Insert into database
        result = db.inventory.insert_one(item)
        item["item_id"] = str(result.inserted_id)
        item["_id"] = str(result.inserted_id)
        
        return {
            "success": True,
            "message": "Item added successfully",
            "item": item
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/use/{item_id}")
async def use_inventory_item(
    item_id: str,
    request: UseItemRequest,
    db_client = Depends(get_db_client)
):
    """
    Use/consume inventory item (reduces quantity)
    
    - **item_id**: Item ID
    - **quantity**: Quantity to use
    """
    try:
        db = db_client["kisanmitra"]
        
        # Find item
        item = db.inventory.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Check if enough quantity
        if item["quantity"] < request.quantity:
            raise HTTPException(status_code=400, detail="Insufficient quantity")
        
        # Update quantity
        new_quantity = item["quantity"] - request.quantity
        
        # Update status
        if new_quantity == 0:
            status = "out_of_stock"
        elif new_quantity < 10:
            status = "low_stock"
        else:
            status = "in_stock"
        
        # Update in database
        db.inventory.update_one(
            {"_id": ObjectId(item_id)},
            {
                "$set": {
                    "quantity": new_quantity,
                    "status": status,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return {
            "success": True,
            "message": f"Used {request.quantity} {item['unit']}",
            "remaining_quantity": new_quantity,
            "status": status
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/restock/{item_id}")
async def restock_inventory_item(
    item_id: str,
    request: RestockItemRequest,
    db_client = Depends(get_db_client)
):
    """
    Restock inventory item (increases quantity)
    
    - **item_id**: Item ID
    - **quantity**: Quantity to add
    - **cost_per_unit**: Optional new cost per unit
    """
    try:
        db = db_client["kisanmitra"]
        
        # Find item
        item = db.inventory.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Update quantity
        new_quantity = item["quantity"] + request.quantity
        
        # Update cost if provided
        cost_per_unit = request.cost_per_unit if request.cost_per_unit else item["cost_per_unit"]
        total_cost = new_quantity * cost_per_unit
        
        # Update status
        if new_quantity == 0:
            status = "out_of_stock"
        elif new_quantity < 10:
            status = "low_stock"
        else:
            status = "in_stock"
        
        # Update in database
        update_data = {
            "quantity": new_quantity,
            "cost_per_unit": cost_per_unit,
            "total_cost": total_cost,
            "status": status,
            "updated_at": datetime.utcnow()
        }
        
        db.inventory.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": update_data}
        )
        
        return {
            "success": True,
            "message": f"Restocked {request.quantity} {item['unit']}",
            "new_quantity": new_quantity,
            "status": status
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{item_id}")
async def delete_inventory_item(
    item_id: str,
    db_client = Depends(get_db_client)
):
    """
    Delete inventory item
    
    - **item_id**: Item ID
    """
    try:
        db = db_client["kisanmitra"]
        
        result = db.inventory.delete_one({"_id": ObjectId(item_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return {
            "success": True,
            "message": "Item deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary/{farmer_id}")
async def get_inventory_summary(
    farmer_id: str,
    db_client = Depends(get_db_client)
):
    """
    Get inventory summary statistics
    
    - **farmer_id**: Farmer ID
    """
    try:
        db = db_client["kisanmitra"]
        
        # Get all items
        items = list(db.inventory.find({"farmer_id": farmer_id}))
        
        # Calculate statistics
        total_items = len(items)
        total_value = sum(item.get("total_cost", 0) for item in items)
        low_stock_items = len([item for item in items if item.get("status") == "low_stock"])
        out_of_stock_items = len([item for item in items if item.get("status") == "out_of_stock"])
        
        # Category breakdown
        categories = {}
        for item in items:
            category = item.get("category", "other")
            if category not in categories:
                categories[category] = {"count": 0, "value": 0}
            categories[category]["count"] += 1
            categories[category]["value"] += item.get("total_cost", 0)
        
        return {
            "success": True,
            "summary": {
                "total_items": total_items,
                "total_value": total_value,
                "low_stock_items": low_stock_items,
                "out_of_stock_items": out_of_stock_items,
                "categories": categories
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
