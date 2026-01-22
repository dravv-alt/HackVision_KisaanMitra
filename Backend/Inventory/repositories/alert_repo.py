"""
Alert Repository for Expiry Reminders
"""

from typing import List, Dict, Any
from datetime import datetime


class AlertRepo:
    """Repository for storing expiry reminders (mock implementation)"""
    
    def __init__(self):
        # Mock storage for reminders
        self._mock_reminders: List[Dict[str, Any]] = []
    
    def save_expiry_reminders(self, reminders: List[Dict[str, Any]]) -> None:
        """
        Save expiry reminders
        In production, this would write to MongoDB alerts_notifications collection
        For hackathon, we log to console and store in memory
        """
        for reminder in reminders:
            reminder["savedAt"] = datetime.now()
            self._mock_reminders.append(reminder)
            
            # Log for demo purposes
            print(f"[ALERT] Reminder saved: {reminder.get('message', 'N/A')} "
                  f"for item {reminder.get('itemId', 'N/A')}")
    
    def get_reminders(self, farmer_id: str) -> List[Dict[str, Any]]:
        """Get all reminders for a farmer"""
        return [r for r in self._mock_reminders if r.get("farmerId") == farmer_id]
