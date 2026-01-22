"""
Alert Repository for Notification Storage
"""

from typing import List, Dict, Any
from datetime import datetime
import uuid

from ..models import AlertRecord
from ..constants import AlertType, AlertStatus


class AlertRepo:
    """Repository for storing alert notifications"""
    
    def __init__(self):
        # Mock storage for alerts
        self._mock_alerts: List[AlertRecord] = []
    
    def save_alert(self, alert: AlertRecord) -> AlertRecord:
        """
        Save a single alert
        
        Args:
            alert: Alert record to save
            
        Returns:
            Saved alert record
        """
        self._mock_alerts.append(alert)
        print(f"[ALERT] Saved: {alert.title} for farmer {alert.farmerId}")
        return alert
    
    def save_alerts(self, alerts: List[AlertRecord]) -> int:
        """
        Save multiple alerts
        
        Args:
            alerts: List of alert records
            
        Returns:
            Number of alerts saved
        """
        for alert in alerts:
            self.save_alert(alert)
        return len(alerts)
    
    def get_alerts_for_farmer(
        self,
        farmer_id: str,
        status: AlertStatus = None,
        alert_type: AlertType = None
    ) -> List[AlertRecord]:
        """
        Get alerts for a specific farmer
        
        Args:
            farmer_id: Farmer ID
            status: Optional filter by status
            alert_type: Optional filter by type
            
        Returns:
            List of matching alerts
        """
        alerts = [a for a in self._mock_alerts if a.farmerId == farmer_id]
        
        if status:
            alerts = [a for a in alerts if a.status == status]
        
        if alert_type:
            alerts = [a for a in alerts if a.alertType == alert_type]
        
        return sorted(alerts, key=lambda x: x.createdAt, reverse=True)
    
    def mark_as_read(self, alert_id: str) -> bool:
        """
        Mark alert as read
        
        Args:
            alert_id: Alert ID
            
        Returns:
            True if updated, False if not found
        """
        for alert in self._mock_alerts:
            if alert.alertId == alert_id:
                alert.status = AlertStatus.READ
                alert.readAt = datetime.now()
                return True
        return False
    
    def get_unread_count(self, farmer_id: str) -> int:
        """Get count of unread alerts for a farmer"""
        return len([
            a for a in self._mock_alerts
            if a.farmerId == farmer_id and a.status != AlertStatus.READ
        ])
