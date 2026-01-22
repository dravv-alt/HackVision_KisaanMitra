"""
Alert Repository for Collaborative Farming Reminders
"""

from typing import List
from ..models import ReminderRecord


class AlertRepo:
    def __init__(self):
        self._reminders: List[ReminderRecord] = []

    def save_reminders(self, reminders: List[ReminderRecord]) -> None:
        """Persist generated reminders"""
        self._reminders.extend(reminders)
        
    def list_reminders(self, farmer_id: str) -> List[ReminderRecord]:
        """List reminders for a farmer"""
        return [r for r in self._reminders if r.farmerId == farmer_id]
