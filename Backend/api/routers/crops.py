"""
Active Crops Management API Router
Handles active crop tracking, health monitoring, and updates
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from bson import ObjectId
import uuid

from Backend.api.dependencies import get_db_client

router = APIRouter(prefix="/crops", tags=["Active Crops"])

# Request/Response Models
class AddCropRequest(BaseModel):
    farmer_id: str
    crop_name: str
    crop_id: str  # From crops_master
    area_acres: float
    planting_date: str
    expected_harvest_date: str
    notes: Optional[str] = None

class UpdateCropRequest(BaseModel):
    current_stage: Optional[str] = None
    health_status: Optional[str] = None
    health_score: Optional[int] = None
    notes: Optional[str] = None

# API Endpoints

@router.get("/active/{farmer_id}")
async def get_active_crops(
    farmer_id: str,
    db_client = Depends(get_db_client)
):
    """Get all active crops for a farmer"""
    try:
        db = db_client["kisanmitra"]
        
        crops = list(db.active_crops.find({"farmer_id": farmer_id}))
        
        for crop in crops:
            crop["_id"] = str(crop["_id"])
            crop["active_crop_id"] = crop.get("active_crop_id", str(crop["_id"]))
        
        return {
            "success": True,
            "crops": crops,
            "count": len(crops)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add")
async def add_crop(
    request: AddCropRequest,
    db_client = Depends(get_db_client)
):
    """Add new active crop"""
    try:
        db = db_client["kisanmitra"]
        
        crop = {
            "active_crop_id": f"AC{str(uuid.uuid4())[:8].upper()}",
            "farmer_id": request.farmer_id,
            "crop_id": request.crop_id,
            "crop_name": request.crop_name,
            "area_acres": request.area_acres,
            "planting_date": request.planting_date,
            "expected_harvest_date": request.expected_harvest_date,
            "current_stage": "सीडिंग",
            "health_status": "स्वस्थ",
            "health_score": 100,
            "last_watered": datetime.utcnow(),
            "last_fertilized": None,
            "notes": request.notes or "",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = db.active_crops.insert_one(crop)
        crop["_id"] = str(result.inserted_id)
        
        return {
            "success": True,
            "message": "Crop added successfully",
            "crop": crop
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update/{crop_id}")
async def update_crop(
    crop_id: str,
    request: UpdateCropRequest,
    db_client = Depends(get_db_client)
):
    """Update crop details"""
    try:
        db = db_client["kisanmitra"]
        
        update_data = {"updated_at": datetime.utcnow()}
        
        if request.current_stage:
            update_data["current_stage"] = request.current_stage
        if request.health_status:
            update_data["health_status"] = request.health_status
        if request.health_score is not None:
            update_data["health_score"] = request.health_score
        if request.notes:
            update_data["notes"] = request.notes
        
        result = db.active_crops.update_one(
            {"_id": ObjectId(crop_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Crop not found")
        
        return {
            "success": True,
            "message": "Crop updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{crop_id}")
async def delete_crop(
    crop_id: str,
    db_client = Depends(get_db_client)
):
    """Delete/harvest crop"""
    try:
        db = db_client["kisanmitra"]
        
        result = db.active_crops.delete_one({"_id": ObjectId(crop_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Crop not found")
        
        return {
            "success": True,
            "message": "Crop removed successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/water/{crop_id}")
async def water_crop(
    crop_id: str,
    db_client = Depends(get_db_client)
):
    """Log watering activity"""
    try:
        db = db_client["kisanmitra"]
        
        result = db.active_crops.update_one(
            {"_id": ObjectId(crop_id)},
            {
                "$set": {
                    "last_watered": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Crop not found")
        
        return {
            "success": True,
            "message": "Watering logged successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fertilize/{crop_id}")
async def fertilize_crop(
    crop_id: str,
    db_client = Depends(get_db_client)
):
    """Log fertilizing activity"""
    try:
        db = db_client["kisanmitra"]
        
        result = db.active_crops.update_one(
            {"_id": ObjectId(crop_id)},
            {
                "$set": {
                    "last_fertilized": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Crop not found")
        
        return {
            "success": True,
            "message": "Fertilizing logged successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
