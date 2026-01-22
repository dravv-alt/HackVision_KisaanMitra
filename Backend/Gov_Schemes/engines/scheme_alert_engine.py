"""
Scheme Alert Engine - New Scheme Detection and Alert Generation
"""

from typing import List
from datetime import datetime, timedelta
import uuid

from ..models import SchemeRecord, AlertRecord, FarmerProfile
from ..constants import AlertType, AlertUrgency, AlertStatus, Language
from ..repositories import SchemeRepo


class SchemeAlertEngine:
    """Engine for detecting new schemes and generating alerts"""
    
    def __init__(self, scheme_repo: SchemeRepo):
        self.scheme_repo = scheme_repo
        self._last_check: datetime = datetime.now() - timedelta(days=7)
    
    def detect_new_schemes(
        self,
        since: datetime = None
    ) -> List[SchemeRecord]:
        """
        Detect schemes added since a specific time
        
        Args:
            since: Check for schemes added after this datetime
                   If None, uses last check time
            
        Returns:
            List of new schemes
        """
        check_time = since if since else self._last_check
        new_schemes = self.scheme_repo.get_new_schemes_since(check_time)
        
        # Update last check time
        self._last_check = datetime.now()
        
        return new_schemes
    
    def generate_alerts_for_farmer(
        self,
        farmer: FarmerProfile,
        new_schemes: List[SchemeRecord]
    ) -> List[AlertRecord]:
        """
        Generate alert records for new schemes relevant to farmer
        
        Args:
            farmer: Farmer profile
            new_schemes: List of new schemes
            
        Returns:
            List of alert records
        """
        alerts = []
        
        for scheme in new_schemes:
            # Check if scheme is relevant to farmer's location
            if not self._is_scheme_relevant(scheme, farmer):
                continue
            
            # Determine urgency based on end date
            urgency = self._determine_urgency(scheme)
            
            # Create alert
            alert = self._create_alert(farmer, scheme, urgency)
            alerts.append(alert)
        
        return alerts
    
    def _is_scheme_relevant(
        self,
        scheme: SchemeRecord,
        farmer: FarmerProfile
    ) -> bool:
        """
        Check if scheme is relevant to farmer's location
        
        Args:
            scheme: Scheme record
            farmer: Farmer profile
            
        Returns:
            True if relevant
        """
        # All-India schemes are always relevant
        if scheme.state is None:
            return True
        
        # State-specific schemes
        if scheme.state and farmer.state:
            if scheme.state.lower() != farmer.state.lower():
                return False
            
            # District-specific schemes
            if scheme.district and farmer.district:
                if scheme.district.lower() != farmer.district.lower():
                    return False
        
        return True
    
    def _determine_urgency(self, scheme: SchemeRecord) -> AlertUrgency:
        """
        Determine alert urgency based on scheme end date
        
        Args:
            scheme: Scheme record
            
        Returns:
            Alert urgency level
        """
        if scheme.endDate is None:
            # No end date - low urgency
            return AlertUrgency.LOW
        
        days_remaining = (scheme.endDate - datetime.now()).days
        
        if days_remaining <= 7:
            return AlertUrgency.HIGH
        elif days_remaining <= 30:
            return AlertUrgency.MEDIUM
        else:
            return AlertUrgency.LOW
    
    def _create_alert(
        self,
        farmer: FarmerProfile,
        scheme: SchemeRecord,
        urgency: AlertUrgency
    ) -> AlertRecord:
        """
        Create alert record for a new scheme
        
        Args:
            farmer: Farmer profile
            scheme: Scheme record
            urgency: Alert urgency
            
        Returns:
            Alert record
        """
        # Determine scope
        if scheme.district:
            scope = f"{scheme.district} District"
        elif scheme.state:
            scope = f"{scheme.state} State"
        else:
            scope = "All India"
        
        # Create title and message
        if farmer.language == Language.HINDI:
            title = f"नई योजना: {scheme.schemeNameHindi or scheme.schemeName}"
            message = (
                f"{scheme.descriptionHindi or scheme.description}\n"
                f"क्षेत्र: {scope}\n"
                f"लाभ: {scheme.benefitsHindi or scheme.benefits}"
            )
        else:
            title = f"New Scheme: {scheme.schemeName}"
            message = (
                f"{scheme.description}\n"
                f"Scope: {scope}\n"
                f"Benefits: {scheme.benefits}"
            )
        
        return AlertRecord(
            alertId=str(uuid.uuid4()),
            farmerId=farmer.farmerId,
            alertType=AlertType.GOV_SCHEME,
            urgency=urgency,
            status=AlertStatus.PENDING,
            title=title,
            titleHindi=f"नई योजना: {scheme.schemeNameHindi or scheme.schemeName}",
            message=message,
            messageHindi=(
                f"{scheme.descriptionHindi or scheme.description}\n"
                f"क्षेत्र: {scope}\n"
                f"लाभ: {scheme.benefitsHindi or scheme.benefits}"
            ),
            relatedId=scheme.schemeId,
            actionUrl=scheme.officialLink,
            createdAt=datetime.now()
        )
