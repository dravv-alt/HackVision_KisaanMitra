"""
Alerts Service - Main Orchestration Layer
"""

from datetime import datetime, timedelta
from typing import Optional, List
import uuid

from .models import AlertsOutput, AlertRecord
from .repositories import (
    FarmerRepo, CropRepo, SchemeRepo, MarketRepo, AlertRepo, AuditRepo
)
from .engines import (
    WeatherEngine, IrrigationAlertEngine, SchemeAlertEngine, 
    PriceAlertEngine, SchedulerEngine, PrioritizationEngine, ResponseBuilder
)
from .constants import AlertType, AlertUrgency


class AlertsService:
    """
    Orchestration layer that scans for triggers and generates prioritised alerts.
    Designed for 100% demo reliability with mock fallbacks.
    """
    
    def __init__(self):
        # Repositories (Assume MongoDB connection handled elsewhere)
        self.farmer_repo = FarmerRepo()
        self.crop_repo = CropRepo()
        self.scheme_repo = SchemeRepo()
        self.market_repo = MarketRepo()
        self.alert_repo = AlertRepo()
        self.audit_repo = AuditRepo()
        
        # Logic Engines
        self.weather_engine = WeatherEngine()
        self.irrigation_engine = IrrigationAlertEngine()
        self.scheme_engine = SchemeAlertEngine()
        self.price_engine = PriceAlertEngine()
        self.scheduler = SchedulerEngine()
        self.prioritizer = PrioritizationEngine()
        self.response_builder = ResponseBuilder()

    def run_alert_scan(
        self, 
        farmer_id: str, 
        last_checked_at: Optional[datetime] = None
    ) -> AlertsOutput:
        """
        Public entry point to generate and fetch formatted alerts for a farmer.
        """
        # 1. Fetch Contexts
        farmer = self.farmer_repo.get_farmer(farmer_id)
        crops = self.crop_repo.get_active_crops(farmer_id)
        weather = self.weather_engine.get_weather(farmer.lat, farmer.lon)
        schemes = self.scheme_repo.list_schemes()
        
        # Last checked fallback: 24h ago
        check_ts = last_checked_at or (datetime.now() - timedelta(days=1))
        
        # 2. Generate Candidate Alerts
        all_candidates: List[AlertRecord] = []
        
        # A. Weather Alerts (Direct from Engine)
        for w_warn in weather.alerts:
            all_candidates.append(AlertRecord(
                alertId=str(uuid.uuid4()),
                farmerId=farmer_id,
                alertType=AlertType.WEATHER,
                title="Weather Warning",
                message=w_warn,
                urgency=AlertUrgency.CRITICAL,
                scheduledAt=datetime.now()
            ))
            
        # B. Irrigation Triggers
        irrigation_alerts = self.irrigation_engine.generate(farmer, crops, weather)
        all_candidates.extend(irrigation_alerts)
        
        # C. New Schemes
        scheme_alerts = self.scheme_engine.generate(farmer, schemes, check_ts)
        all_candidates.extend(scheme_alerts)
        
        # D. Price Fluctuations
        price_alerts = self.price_engine.generate(farmer, crops, self.market_repo)
        all_candidates.extend(price_alerts)
        
        # 3. Schedule, Rank and Sort
        scheduled_alerts = self.scheduler.schedule(all_candidates)
        final_alerts = self.prioritizer.rank(scheduled_alerts)
        
        # 4. Persistence & Audit
        self.alert_repo.save_alerts(final_alerts)
        self.audit_repo.log(farmer_id, "alert_scan", {"hits": len(final_alerts)})
        
        # 5. Build Final Response
        return self.response_builder.build_output(farmer.language, final_alerts)

    def mark_alert_as_read(self, alert_id: str) -> bool:
        """Helper to manage UI read state"""
        self.alert_repo.mark_read(alert_id)
        return True
