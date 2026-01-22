"""
Audit Logging Repository
"""

from typing import Dict, Any
import datetime


class AuditRepo:
    def log(self, farmer_id: str, action: str, meta: Dict[str, Any]) -> None:
        """Log system events and triggers for debugging"""
        ts = datetime.datetime.now().isoformat()
        log_entry = f"[{ts}] Farmer: {farmer_id} | Action: {action} | Meta: {meta}"
        # For demo purposes, we can print or store in a list
        # print(log_entry)
