"""
Calendar Events API Router
Handles farming calendar events and reminders
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId
import uuid

from Backend.api.dependencies import get_db_client

router = APIRouter(prefix="/calendar", tags=["Calendar"])

# Request/Response Models
class EventRequest(BaseModel):
    farmer_id: str
    title: str
    description: Optional[str] = None
    event_type: str  # बुवाई, सिंचाई, उर्वरक, कीटनाशक, कटाई, बाजार दिवस
    date: str
    time: Optional[str] = "09:00"
    duration_hours: Optional[int] = 2
    reminder_sent: Optional[bool] = False

# API Endpoints

@router.get("/events/{farmer_id}")
async def get_events(
    farmer_id: str,
    db_client = Depends(get_db_client)
):
    """Get all calendar events for a farmer"""
    try:
        db = db_client["kisanmitra"]
        
        events = list(db.calendar_events.find({"farmer_id": farmer_id}).sort("date", 1))
        
        for event in events:
            event["_id"] = str(event["_id"])
            event["event_id"] = event.get("event_id", str(event["_id"]))
        
        return {
            "success": True,
            "events": events,
            "count": len(events)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/event")
async def create_event(
    request: EventRequest,
    db_client = Depends(get_db_client)
):
    """Create new calendar event"""
    try:
        db = db_client["kisanmitra"]
        
        event = {
            "event_id": f"EVT{str(uuid.uuid4())[:8].upper()}",
            "farmer_id": request.farmer_id,
            "title": request.title,
            "description": request.description or "",
            "event_type": request.event_type,
            "date": request.date,
            "time": request.time,
            "duration_hours": request.duration_hours,
            "status": "नियोजित",
            "reminder_sent": request.reminder_sent,
            "created_at": datetime.utcnow()
        }
        
        result = db.calendar_events.insert_one(event)
        event["_id"] = str(result.inserted_id)
        
        return {
            "success": True,
            "message": "Event created successfully",
            "event": event
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/event/{event_id}")
async def update_event(
    event_id: str,
    request: EventRequest,
    db_client = Depends(get_db_client)
):
    """Update calendar event"""
    try:
        db = db_client["kisanmitra"]
        
        update_data = {
            "title": request.title,
            "description": request.description,
            "event_type": request.event_type,
            "date": request.date,
            "time": request.time,
            "duration_hours": request.duration_hours,
            "updated_at": datetime.utcnow()
        }
        
        result = db.calendar_events.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return {
            "success": True,
            "message": "Event updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/event/{event_id}")
async def delete_event(
    event_id: str,
    db_client = Depends(get_db_client)
):
    """Delete calendar event"""
    try:
        db = db_client["kisanmitra"]
        
        result = db.calendar_events.delete_one({"_id": ObjectId(event_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return {
            "success": True,
            "message": "Event deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/event/{event_id}/complete")
async def mark_event_complete(
    event_id: str,
    db_client = Depends(get_db_client)
):
    """Mark event as completed"""
    try:
        db = db_client["kisanmitra"]
        
        result = db.calendar_events.update_one(
            {"_id": ObjectId(event_id)},
            {
                "$set": {
                    "status": "पूर्ण",
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return {
            "success": True,
            "message": "Event marked as complete"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
