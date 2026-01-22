"""
Pre-Seeding Service - Main orchestration layer
Single entry point for all pre-seeding planning operations
"""
from datetime import datetime
from typing import Optional

from .models import PlanningRequest, PreSeedingOutput
from .constants import Season, SEASON_MONTHS
from .repositories import (
    FarmerRepository, CropRepository, SchemeRepository, ReminderRepository
)
from .engines import (
    WeatherEngine, CropRecommendationEngine, SchemeEngine,
    ReminderEngine, ResponseBuilder
)


class PreSeedingService:
    """
    Main service for pre-seeding planning
    Orchestrates all engines and repositories
    """
    
    def __init__(
        self,
        farmer_repo: Optional[FarmerRepository] = None,
        crop_repo: Optional[CropRepository] = None,
        scheme_repo: Optional[SchemeRepository] = None,
        reminder_repo: Optional[ReminderRepository] = None,
        weather_api_key: Optional[str] = None
    ):
        """
        Initialize service with repositories and engines
        
        Args:
            farmer_repo: Farmer repository (creates default if None)
            crop_repo: Crop repository (creates default if None)
            scheme_repo: Scheme repository (creates default if None)
            reminder_repo: Reminder repository (creates default if None)
            weather_api_key: OpenWeather API key (optional)
        """
        # Repositories
        self.farmer_repo = farmer_repo or FarmerRepository()
        self.crop_repo = crop_repo or CropRepository()
        self.scheme_repo = scheme_repo or SchemeRepository()
        self.reminder_repo = reminder_repo or ReminderRepository()
        
        # Engines
        self.weather_engine = WeatherEngine(api_key=weather_api_key)
        self.crop_engine = CropRecommendationEngine()
        self.scheme_engine = SchemeEngine()
        self.reminder_engine = ReminderEngine()
        self.response_builder = ResponseBuilder()
    
    def run(self, request: PlanningRequest) -> PreSeedingOutput:
        """
        Execute complete pre-seeding planning workflow
        
        Args:
            request: Planning request with farmer ID and preferences
            
        Returns:
            PreSeedingOutput with crop recommendations, schemes, and reminders
            
        Raises:
            ValueError: If farmer not found or invalid input
        """
        print(f"\n🌾 Starting Pre-Seeding Planning for Farmer: {request.farmer_id}")
        print("=" * 70)
        
        # Step 1: Get farmer profile
        farmer = self.farmer_repo.get_farmer(request.farmer_id)
        if not farmer:
            raise ValueError(f"Farmer not found: {request.farmer_id}")
        
        print(f"✓ Farmer Profile: {farmer.location.state}, {farmer.location.district}")
        print(f"  - Soil: {farmer.soil_type.value}, Irrigation: {farmer.irrigation_type.value}")
        print(f"  - Land: {farmer.land_size_acres} acres")
        
        # Step 2: Determine season
        season = request.season
        if not season:
            season = self._detect_current_season()
            print(f"✓ Auto-detected Season: {season.value}")
        else:
            print(f"✓ Requested Season: {season.value}")
        
        # Step 3: Get weather context
        print(f"\n⛅ Fetching weather data...")
        weather_context = self.weather_engine.get_context(
            farmer.location.lat,
            farmer.location.lon
        )
        print(f"✓ Weather: {weather_context.temperature_c}°C, Humidity: {weather_context.humidity_pct}%")
        print(f"  - Rain forecast: {weather_context.rain_mm_next_7_days}mm in 7 days")
        
        # Step 4: Get crop recommendations
        print(f"\n🌱 Analyzing crop suitability...")
        all_crops = self.crop_repo.list_crops()
        crop_recommendations = self.crop_engine.recommend(
            request=request,
            farmer=farmer,
            env=weather_context,
            crops=all_crops,
            season=season
        )
        print(f"✓ Top {len(crop_recommendations)} crops recommended:")
        for i, crop in enumerate(crop_recommendations, 1):
            print(f"  {i}. {crop.crop_name} (Score: {crop.score:.1f})")
        
        # Step 5: Check scheme eligibility
        print(f"\n📋 Checking government scheme eligibility...")
        all_schemes = self.scheme_repo.list_schemes()
        scheme_results = self.scheme_engine.recommend_schemes(
            farmer=farmer,
            recommended_crops=crop_recommendations,
            all_schemes=all_schemes
        )
        
        eligible_count = len([s for s in scheme_results if s.eligible])
        print(f"✓ Eligible for {eligible_count} schemes:")
        for scheme in scheme_results[:3]:
            if scheme.eligible:
                status = "✅ ELIGIBLE"
                if scheme.deadline_warning:
                    status += f" - {scheme.deadline_warning}"
                print(f"  - {scheme.scheme_name}: {status}")
        
        # Step 6: Generate reminders
        print(f"\n⏰ Generating scheme deadline reminders...")
        reminders = self.reminder_engine.generate(
            scheme_results=scheme_results,
            farmer=farmer
        )
        print(f"✓ Created {len(reminders)} reminder(s)")
        
        # Step 7: Save reminders
        if reminders:
            self.reminder_repo.save_reminders(reminders)
        
        # Step 8: Build final output
        print(f"\n📄 Building final output...")
        output = self.response_builder.build_output(
            farmer=farmer,
            weather=weather_context,
            crops=crop_recommendations,
            schemes=scheme_results,
            reminders=reminders
        )
        
        print(f"✓ Output ready - Urgency: {output.urgency_level.value.upper()}")
        print("=" * 70)
        
        return output
    
    def _detect_current_season(self) -> Season:
        """
        Auto-detect current agricultural season based on month
        
        Returns:
            Current season
        """
        current_month = datetime.now().month
        
        for season, months in SEASON_MONTHS.items():
            if current_month in months:
                return season
        
        # Default to Kharif
        return Season.KHARIF
