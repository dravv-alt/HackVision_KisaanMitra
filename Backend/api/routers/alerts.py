"""
Alerts Management API Router
Handles priority alerts and notifications
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId

from Backend.api.dependencies import get_db_client

router = APIRouter(prefix="/alerts", tags=["Alerts"])

# Request/Response Models
class CreateAlertRequest(BaseModel):
    farmer_id: str
    type: str  # मौसम चेतावनी, कीट चेतावनी, बीमारी चेतावनी, etc.
    priority: str  # उच्च, मध्यम, निम्न
    title: str
    message: str
    expires_days: Optional[int] = 7

# API Endpoints

@router.get("/{farmer_id}")
async def get_alerts(
    farmer_id: str,
    unread_only: bool = False,
    db_client = Depends(get_db_client)
):
    """Get all alerts for a farmer"""
    try:
        db = db_client["kisanmitra"]
        
        query = {"farmer_id": farmer_id}
        if unread_only:
            query["is_read"] = False
        
        alerts = list(db.alerts.find(query).sort("created_at", -1))
        
        for alert in alerts:
            alert["_id"] = str(alert["_id"])
            alert["alert_id"] = alert.get("alert_id", str(alert["_id"]))
        
        return {
            "success": True,
            "alerts": alerts,
            "count": len(alerts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/mark-read/{alert_id}")
async def mark_alert_read(
    alert_id: str,
    db_client = Depends(get_db_client)
):
    """Mark alert as read"""
    try:
        db = db_client["kisanmitra"]
        
        result = db.alerts.update_one(
            {"_id": ObjectId(alert_id)},
            {
                "$set": {
                    "is_read": True,
                    "read_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return {
            "success": True,
            "message": "Alert marked as read"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/mark-all-read/{farmer_id}")
async def mark_all_read(
    farmer_id: str,
    db_client = Depends(get_db_client)
):
    """Mark all alerts as read for a farmer"""
    try:
        db = db_client["kisanmitra"]
        
        result = db.alerts.update_many(
            {"farmer_id": farmer_id, "is_read": False},
            {
                "$set": {
                    "is_read": True,
                    "read_at": datetime.utcnow()
                }
            }
        )
        
        return {
            "success": True,
            "message": f"Marked {result.modified_count} alerts as read"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: str,
    db_client = Depends(get_db_client)
):
    """Delete/dismiss alert"""
    try:
        db = db_client["kisanmitra"]
        
        result = db.alerts.delete_one({"_id": ObjectId(alert_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return {
            "success": True,
            "message": "Alert deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create")
async def create_alert(
    request: CreateAlertRequest,
    db_client = Depends(get_db_client)
):
    """Create new alert (for system/admin use)"""
    try:
        db = db_client["kisanmitra"]
        
        from datetime import timedelta
        import uuid
        
        alert = {
            "alert_id": f"ALT{str(uuid.uuid4())[:8].upper()}",
            "farmer_id": request.farmer_id,
            "type": request.type,
            "priority": request.priority,
            "title": request.title,
            "message": request.message,
            "is_read": False,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=request.expires_days)
        }
        
        result = db.alerts.insert_one(alert)
        alert["_id"] = str(result.inserted_id)
        
        return {
            "success": True,
            "message": "Alert created successfully",
            "alert": alert
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
