"""
Audit Repository for Collaborative Farming
"""

from typing import Dict, Any
import datetime


class AuditRepo:
    def log(self, farmer_id: str, action: str, meta: Dict[str, Any]) -> None:
        """Log system events for debugging and tracking"""
        # In a real app, this would write to MongoDB 'audit_logs'
        ts = datetime.datetime.now().isoformat()
        # For demo, we just print or would store in a list
        # print(f"[AUDIT] {ts} | Farmer: {farmer_id} | Action: {action} | Meta: {meta}")
