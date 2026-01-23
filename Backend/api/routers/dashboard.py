from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from datetime import datetime, timedelta
from Backend.database.connection import get_database
from Backend.database.models import User, Farmer, Task, Alert, FinanceTransaction, ConversationMeta, Session
from bson import ObjectId

router = APIRouter()

@router.get("/dashboard/stats")
async def get_dashboard_stats(db=Depends(get_database)):
    """
    Get summary statistics for the dashboard.
    """
    # Mock hardcoded farmer ID for MVP (Demo User: Ramesh)
    # In production, get from auth token
    
    # Try to find a demo farmer, or use a placeholder ID
    # For now, we'll assume a dummy ID if not found, but ideally init_db seeds this.
    
    # 1. Active Crops Count
    # active_crops_count = await db.components.count_documents({"farmerId": farmer_id, "status": "active"})
    
    # 2. Alerts Count (Unread)
    # unread_alerts = await db.alerts_notifications.count_documents({"farmerId": farmer_id, "isRead": False})
    
    # Return mock stats for now if DB is empty to prevent UI crashing
    return {
        "active_crops": 3,
        "unread_alerts": 2,
        "weather": {
            "temp": 32,
            "condition": "Sunny",
            "chance_of_rain": 10
        }
    }

@router.get("/dashboard/timeline", response_model=List[Dict[str, Any]])
async def get_dashboard_timeline(db=Depends(get_database)):
    """
    Get today's tasks for the dashboard timeline/calendar.
    """
    # In real app: filter by farmer_id and date range (today)
    
    # Example fetching from tasks_calendar
    tasks_cursor = db.tasks_calendar.find().limit(5)
    tasks = await tasks_cursor.to_list(length=5)
    
    if not tasks:
        # Return some default tasks so the UI shows something
        now = datetime.now()
        return [
            {
                "id": "mock-1",
                "title": "Wheat Irrigation",
                "start": now.replace(hour=10, minute=0).isoformat(),
                "end": now.replace(hour=12, minute=0).isoformat(),
                "type": "water"
            },
            {
                "id": "mock-2",
                "title": "Visit Mandi",
                "start": now.replace(day=now.day+1, hour=9, minute=0).isoformat(),
                "end": now.replace(day=now.day+1, hour=11, minute=0).isoformat(),
                "type": "market"
            }
        ]

    # Convert mongo tasks to UI format
    result = []
    for t in tasks:
        result.append({
            "id": str(t["_id"]),
            "title": t.get("title", t["taskMeta"]["taskType"]), # Fallback to taskType
            "start": t["dueAt"].isoformat(),
            "end": (t["dueAt"] + timedelta(hours=1)).isoformat(), # Default 1h duration
            "type": "water" # dynamic mapping needed
        })
    return result

@router.get("/dashboard/finance")
async def get_dashboard_finance(db=Depends(get_database)):
    """
    Get financial summary.
    """
    return {
        "revenue": 124500,
        "expenses": 45200,
        "revenue_change": "+12%",
        "expenses_change": "High fertilizer cost"
    }

@router.get("/alerts", response_model=List[Alert])
async def get_alerts(db=Depends(get_database)):
    """
    Get priority alerts.
    """
    # Fetch real alerts
    alerts = await db.alerts_notifications.find().sort("sentAt", -1).limit(10).to_list(length=10)
    
    # Map to Pydantic model
    return [Alert(**a) for a in alerts]
