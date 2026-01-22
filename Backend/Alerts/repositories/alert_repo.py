"""
Alert Storage Repository
"""

from typing import List, Optional
from ..models import AlertRecord
from ..constants import AlertStatus


class AlertRepo:
    def __init__(self):
        self._db: List[AlertRecord] = []

    def save_alerts(self, alerts: List[AlertRecord]) -> None:
        """Persist generated alerts to 'database' (mock memory for demo)"""
        self._db.extend(alerts)

    def list_alerts(self, farmer_id: str, status: Optional[AlertStatus] = None) -> List[AlertRecord]:
        """Fetch historical alerts for a farmer"""
        results = [a for a in self._db if a.farmerId == farmer_id]
        if status:
            results = [a for a in results if a.status == status]
        return results

    def mark_read(self, alert_id: str) -> None:
        """Update alert status to READ"""
        for alert in self._db:
            if alert.alertId == alert_id:
                alert.status = AlertStatus.READ
                break
