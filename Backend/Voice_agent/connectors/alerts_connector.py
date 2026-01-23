"""
Alerts & Notifications Connector
Bridges voice agent with alerts backend module
"""

import sys
from pathlib import Path

# Add Backend to path for imports
backend_dir = Path(__file__).resolve().parent.parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from typing import Dict, Any, List
from datetime import datetime, timedelta
from Backend.Alerts.service import AlertsService


class AlertsConnector:
    """Connector for alerts module"""
    
    def __init__(self):
        self.service = AlertsService()
    
    def get_alerts(
        self,
        farmer_id: str,
        last_check_hours: int = 24,
        language: str = "hi"
    ) -> Dict[str, Any]:
        """Get alerts for farmer"""
        last_check = datetime.now() - timedelta(hours=last_check_hours)
        
        output = self.service.run_alert_scan(farmer_id, last_check, language=language)
        
        return {
            "speech_text": output.speechText,
            "alerts": output.alerts,
            "summary_counts": output.summaryCounts,
            "urgency": output.urgencyLevel,
            "header": output.header,
            "reasoning": output.detailedReasoning
        }
    
    def mark_as_read(self, alert_id: str) -> bool:
        """Mark alert as read"""
        try:
            self.service.mark_alert_as_read(alert_id)
            return True
        except:
            return False


# Singleton
_connector = None

def get_alerts_connector() -> AlertsConnector:
    """Get or create alerts connector"""
    global _connector
    if _connector is None:
        _connector = AlertsConnector()
    return _connector
