"""
Scheme Alert Engine - Government Policy Monitoring
"""

import uuid
from typing import List
from datetime import datetime
from ..models import FarmerProfile, SchemeContext, AlertRecord
from ..constants import AlertType, AlertUrgency, Language


class SchemeAlertEngine:
    def generate(
        self, 
        farmer: FarmerProfile, 
        schemes: List[SchemeContext], 
        last_checked_at: datetime
    ) -> List[AlertRecord]:
        """
        Detect newly released government schemes relevant to the farmer's state.
        """
        alerts = []
        
        for scheme in schemes:
            # Check if scheme is new and relevant to state
            is_new = scheme.createdAt > last_checked_at
            is_local = farmer.state in scheme.stateEligible or "All" in scheme.stateEligible
            
            if is_new and is_local:
                title = "New Gov Scheme" if farmer.language == Language.ENGLISH else "नई सरकारी योजना"
                msg = (f"New scheme available: {scheme.schemeName}. Tap to check eligibility."
                       if farmer.language == Language.ENGLISH else
                       f"नई योजना उपलब्ध है: {scheme.schemeName}। पात्रता जाँचने के लिए टैप करें।")
                
                alerts.append(AlertRecord(
                    alertId=str(uuid.uuid4()),
                    farmerId=farmer.farmerId,
                    alertType=AlertType.GOV_SCHEME,
                    title=title,
                    message=msg,
                    urgency=AlertUrgency.MEDIUM,
                    related={"schemeKey": scheme.schemeKey},
                    scheduledAt=datetime.now()
                ))
                
        return alerts
