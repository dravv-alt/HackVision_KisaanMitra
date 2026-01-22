"""
Audit Repository for Debugging and Logging
"""

from datetime import datetime
from typing import Dict, Any, List


class AuditRepo:
    """Repository for audit trail logging"""
    
    def __init__(self):
        # Mock storage for audit logs
        self._audit_logs: List[Dict[str, Any]] = []
    
    def log(self, farmer_id: str, action: str, meta: Dict[str, Any]) -> None:
        """
        Log an audit entry
        
        Args:
            farmer_id: Farmer ID
            action: Action performed
            meta: Additional metadata
        """
        log_entry = {
            "farmerId": farmer_id,
            "action": action,
            "meta": meta,
            "timestamp": datetime.now()
        }
        self._audit_logs.append(log_entry)
        
        # Optional: print for debugging during demo
        # print(f"[AUDIT] {farmer_id} - {action}")
    
    def get_logs(self, farmer_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent audit logs for a farmer"""
        farmer_logs = [log for log in self._audit_logs if log["farmerId"] == farmer_id]
        return sorted(farmer_logs, key=lambda x: x["timestamp"], reverse=True)[:limit]
