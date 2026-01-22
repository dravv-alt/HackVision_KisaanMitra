"""
Government Schemes Display Service - Main Orchestration Layer
"""

from datetime import datetime, timedelta
from typing import Optional

from .models import GovSchemesOutput
from .constants import SchemeCategory
from .repositories import (
    FarmerRepo,
    SchemeRepo,
    SchemeAPIClient,
    AlertRepo,
    AuditRepo
)
from .engines import (
    SchemeFetchEngine,
    SchemeFilterEngine,
    SchemeAlertEngine,
    ResponseBuilder
)


class GovSchemesDisplayService:
    """
    Main service for government schemes display
    Orchestrates all engines and repositories
    """
    
    def __init__(self):
        # Initialize repositories
        self.farmer_repo = FarmerRepo()
        self.scheme_repo = SchemeRepo()
        self.api_client = SchemeAPIClient()
        self.alert_repo = AlertRepo()
        self.audit_repo = AuditRepo()
        
        # Initialize engines
        self.fetch_engine = SchemeFetchEngine(self.api_client, self.scheme_repo)
        self.filter_engine = SchemeFilterEngine(self.scheme_repo)
        self.alert_engine = SchemeAlertEngine(self.scheme_repo)
        self.response_builder = ResponseBuilder()
    
    def get_schemes_display(
        self,
        farmer_id: str,
        state: Optional[str] = None,
        district: Optional[str] = None,
        category: Optional[SchemeCategory] = None,
        force_refresh: bool = False,
        generate_alerts: bool = True
    ) -> GovSchemesOutput:
        """
        Get government schemes display for a farmer
        
        This is the main entry point that will be called from FastAPI endpoints
        
        Args:
            farmer_id: Farmer ID
            state: Optional state filter (overrides farmer's state)
            district: Optional district filter (overrides farmer's district)
            category: Optional category filter
            force_refresh: Force refresh from API
            generate_alerts: Whether to generate alerts for new schemes
            
        Returns:
            GovSchemesOutput with complete display data
        """
        try:
            # Audit log
            self.audit_repo.log(
                farmer_id,
                "get_schemes_display",
                {"timestamp": datetime.now(), "force_refresh": force_refresh}
            )
            
            # 1. Get farmer profile
            farmer = self.farmer_repo.get_farmer(farmer_id)
            
            # 2. Sync schemes from API (with cache)
            all_schemes = self.fetch_engine.sync_schemes(force_refresh=force_refresh)
            
            # 3. Detect new schemes (for alerts)
            new_schemes = []
            if generate_alerts:
                # Check for schemes added in last 7 days
                since = datetime.now() - timedelta(days=7)
                new_schemes = self.alert_engine.detect_new_schemes(since=since)
                
                # Generate and save alerts
                if new_schemes:
                    alerts = self.alert_engine.generate_alerts_for_farmer(
                        farmer,
                        new_schemes
                    )
                    if alerts:
                        self.alert_repo.save_alerts(alerts)
            
            # 4. Apply filters
            # Use provided filters or fall back to farmer's location
            filter_state = state if state is not None else farmer.state
            filter_district = district if district is not None else farmer.district
            
            filtered_schemes = self.filter_engine.filter_by_location(
                state=filter_state,
                district=filter_district,
                category=category
            )
            
            # 5. Sort by relevance
            sorted_schemes = self.filter_engine.sort_schemes(
                filtered_schemes,
                sort_by="relevance"
            )
            
            # 6. Build response
            filter_applied = {
                "state": filter_state,
                "district": filter_district,
                "category": category
            }
            
            output = self.response_builder.build(
                farmer,
                sorted_schemes,
                len(new_schemes),
                filter_applied
            )
            
            # Audit log success
            self.audit_repo.log(
                farmer_id,
                "display_success",
                {
                    "totalSchemes": len(sorted_schemes),
                    "newSchemes": len(new_schemes)
                }
            )
            
            return output
            
        except Exception as e:
            # Audit log error
            self.audit_repo.log(
                farmer_id,
                "display_error",
                {"error": str(e)}
            )
            raise
    
    def get_scheme_by_id(self, scheme_id: str):
        """
        Get detailed information for a specific scheme
        
        Args:
            scheme_id: Scheme ID
            
        Returns:
            SchemeRecord or None
        """
        return self.scheme_repo.get_scheme_by_id(scheme_id)
    
    def get_alerts_for_farmer(self, farmer_id: str):
        """
        Get all alerts for a farmer
        
        Args:
            farmer_id: Farmer ID
            
        Returns:
            List of alert records
        """
        from .constants import AlertType
        return self.alert_repo.get_alerts_for_farmer(
            farmer_id,
            alert_type=AlertType.GOV_SCHEME
        )
    
    def mark_alert_as_read(self, alert_id: str) -> bool:
        """
        Mark an alert as read
        
        Args:
            alert_id: Alert ID
            
        Returns:
            True if successful
        """
        return self.alert_repo.mark_as_read(alert_id)
