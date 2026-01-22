"""
Reminder Repository - handles reminder persistence
In production: saves to MongoDB
For hackathon: mock save operation
"""
from typing import List
from ..models import ReminderRecord


class ReminderRepository:
    """Repository for reminder operations"""
    
    def __init__(self):
        """Initialize reminder repository"""
        self._reminders = []  # In-memory storage for demo
    
    def save_reminders(self, reminders: List[ReminderRecord]) -> None:
        """
        Save reminders to database
        
        Args:
            reminders: List of reminder records to save
        """
        # In production: would save to MongoDB
        # For hackathon: store in memory and log
        self._reminders.extend(reminders)
        
        print(f"\n✓ Saved {len(reminders)} reminder(s) to database (mock)")
        for reminder in reminders:
            print(f"  - {reminder.scheme_name} reminder for {reminder.farmer_id} at {reminder.reminder_datetime}")
    
    def get_reminders_for_farmer(self, farmer_id: str) -> List[ReminderRecord]:
        """Get all reminders for a farmer"""
        return [r for r in self._reminders if r.farmer_id == farmer_id]
    
    def clear_all(self) -> None:
        """Clear all reminders (for testing)"""
        self._reminders.clear()
