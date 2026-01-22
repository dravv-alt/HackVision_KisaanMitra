"""
Scheduler Engine - Time-based Intelligence
"""

from datetime import datetime, timedelta
from typing import List
from ..models import AlertRecord
from ..constants import AlertType


class SchedulerEngine:
    def schedule(self, alerts: List[AlertRecord]) -> List[AlertRecord]:
        """
        Apply time-based scheduling rules for alert visibility.
        """
        now = datetime.now()
        
        for alert in alerts:
            # Weather and Irrigation are critical/immediate
            if alert.alertType in [AlertType.WEATHER, AlertType.IRRIGATION]:
                alert.scheduledAt = now
                
            # Gov Schemes: Schedule for morning (8 AM) next day if late evening
            elif alert.alertType == AlertType.GOV_SCHEME:
                if now.hour > 18:
                    alert.scheduledAt = (now + timedelta(days=1)).replace(hour=8, minute=0)
                else:
                    alert.scheduledAt = now
            
            # Price Alerts: Schedule for midday (1 PM) when markets stabilize
            elif alert.alertType == AlertType.PRICE:
                if now.hour < 13:
                    alert.scheduledAt = now.replace(hour=13, minute=0)
                else:
                    alert.scheduledAt = now
                    
        return alerts
