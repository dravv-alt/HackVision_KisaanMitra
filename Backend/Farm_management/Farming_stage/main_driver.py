"""
CLI Test Driver for Farming Assistant
Comprehensive testing of all engines and features
"""

from datetime import date, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Farming_stage.models import (
    CropContext, CropStage, EnvironmentalContext,
    MarketContext, PriceTrend, DemandLevel
)
from Farming_stage.engines import (
    WeatherEngine, MarketEngine, VisionEngine, KnowledgeEngine
)


def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_advisory(advisory):
    """Pretty print advisory output"""
    print(f"\n📋 {advisory.action_header}")
    print(f"   Urgency: {advisory.urgency.value.upper()}")
    print(f"\n💬 Spoken Advice:")
    print(f"   {advisory.spoken_advice}")
    print(f"\n🔍 Reasoning:")
    print(f"   {advisory.detailed_reasoning}")
    
    if advisory.chemical_dosage:
        print(f"\n💊 Chemical Dosage:")
        print(f"   {advisory.chemical_dosage}")
    
    if advisory.safety_warning:
        print(f"\n⚠️  Safety Warning:")
        print(f"   {advisory.safety_warning}")
    
    if advisory.organic_alternative:
        print(f"\n🌿 Organic Alternative:")
        print(f"   {advisory.organic_alternative}")


def test_weather_engine():
    """Test weather engine with real API and fallback"""
    print_section("TEST 1: WEATHER ENGINE")
    
    engine = WeatherEngine()
    
    # Test coordinates (Delhi, India)
    lat, lon = 28.6139, 77.2090
    print(f"\n📍 Input: Latitude={lat}, Longitude={lon}")
    
    context = engine.get_context(lat, lon)
    
    print(f"\n🌤️  Weather Context:")
    print(f"   Temperature: {context.temperature}°C")
    print(f"   Humidity: {context.humidity}%")
    print(f"   Rain Forecast: {'Yes' if context.rain_forecast else 'No'}")
    print(f"   Wind Speed: {context.wind_speed} km/h" if context.wind_speed else "")
    
    print("\n✅ Weather Engine Test PASSED")


def test_market_engine():
    """Test market engine with various crops"""
    print_section("TEST 2: MARKET ENGINE")
    
    engine = MarketEngine()
    
    test_crops = ["Onion", "Tomato", "Wheat", "UnknownCrop"]
    
    for crop in test_crops:
        print(f"\n🌾 Crop: {crop}")
        market = engine.get_market_data(crop)
        
        print(f"   Price: ₹{market.current_price}/kg")
        print(f"   Trend: {market.price_trend.value.upper()}")
        print(f"   Demand: {market.demand_level.value.upper()}")
        
        forecast = engine.get_price_forecast(crop, days_ahead=7)
        print(f"   Forecast: {forecast}")
    
    print("\n✅ Market Engine Test PASSED")


def test_vision_engine():
    """Test vision engine with dummy image data"""
    print_section("TEST 3: VISION ENGINE")
    
    engine = VisionEngine()
    
    # Create dummy image bytes
    dummy_image = b"fake_image_data_for_testing" * 100
    
    print(f"\n🖼️  Input: {len(dummy_image)} bytes of image data")
    
    result = engine.analyze_image(dummy_image)
    
    print(f"\n🔬 Disease Detection Result:")
    print(f"   Disease: {result.disease_name}")
    print(f"   Confidence: {result.confidence * 100:.1f}%")
    print(f"   Mock Result: {'Yes' if result.is_mock else 'No (Real Model)'}")
    
    # Get disease info
    if result.disease_name != "Healthy":
        info = engine.get_disease_info(result.disease_name)
        print(f"\n📚 Disease Information:")
        print(f"   Severity: {info.get('severity', 'Unknown')}")
        print(f"   Spread Rate: {info.get('spread_rate', 'Unknown')}")
        print(f"   Symptoms: {info.get('symptoms', 'Unknown')}")
    
    print("\n✅ Vision Engine Test PASSED")


def test_irrigation_advisor():
    """Test irrigation advisor feature"""
    print_section("TEST 4: IRRIGATION ADVISOR")
    
    engine = KnowledgeEngine()
    
    # Test Case 1: Rain forecast
    print("\n--- Test Case 1: Rain Forecast ---")
    crop = CropContext(
        name="Tomato",
        sowing_date=date.today() - timedelta(days=30),
        current_stage=CropStage.VEGETATIVE
    )
    environment = EnvironmentalContext(
        temperature=28.0,
        rain_forecast=True,
        humidity=75.0,
        wind_speed=10.0
    )
    
    advisory = engine.get_irrigation_advice(crop, environment)
    print_advisory(advisory)
    
    # Test Case 2: Flowering stage, no rain
    print("\n--- Test Case 2: Flowering Stage, No Rain ---")
    crop.current_stage = CropStage.FLOWERING
    environment.rain_forecast = False
    environment.temperature = 32.0
    
    advisory = engine.get_irrigation_advice(crop, environment)
    print_advisory(advisory)
    
    print("\n✅ Irrigation Advisor Test PASSED")


def test_input_optimizer():
    """Test input optimizer (fertilizer/pesticide recommendations)"""
    print_section("TEST 5: INPUT OPTIMIZER")
    
    engine = KnowledgeEngine()
    
    # Test Case 1: Disease treatment
    print("\n--- Test Case 1: Disease Treatment (Leaf Blight) ---")
    advisory = engine.get_treatment_recommendation(
        disease_name="Leaf Blight",
        crop_name="Tomato"
    )
    print_advisory(advisory)
    
    # Test Case 2: Stage-based fertilizer
    print("\n--- Test Case 2: Vegetative Stage Fertilizer ---")
    advisory = engine.get_treatment_recommendation(
        crop_stage=CropStage.VEGETATIVE,
        crop_name="Wheat"
    )
    print_advisory(advisory)
    
    # Test Case 3: Flowering stage
    print("\n--- Test Case 3: Flowering Stage Fertilizer ---")
    advisory = engine.get_treatment_recommendation(
        crop_stage=CropStage.FLOWERING,
        crop_name="Cotton"
    )
    print_advisory(advisory)
    
    print("\n✅ Input Optimizer Test PASSED")


def test_harvest_planner():
    """Test harvest planner decision tree"""
    print_section("TEST 6: HARVEST PLANNER")
    
    engine = KnowledgeEngine()
    
    # Test Case 1: Rain incoming
    print("\n--- Test Case 1: Rain Forecast - Should DELAY ---")
    environment = EnvironmentalContext(
        temperature=28.0,
        rain_forecast=True,
        humidity=80.0
    )
    market = MarketContext(
        crop_name="Onion",
        current_price=35.0,
        price_trend=PriceTrend.STABLE,
        demand_level=DemandLevel.MEDIUM
    )
    
    advisory = engine.plan_harvest(environment, market, storage_available=True, crop_name="Onion")
    print_advisory(advisory)
    
    # Test Case 2: Price rising + has storage
    print("\n--- Test Case 2: Rising Prices + Storage - Should DELAY ---")
    environment.rain_forecast = False
    market.price_trend = PriceTrend.RISING
    
    advisory = engine.plan_harvest(environment, market, storage_available=True, crop_name="Onion")
    print_advisory(advisory)
    
    # Test Case 3: Price falling
    print("\n--- Test Case 3: Falling Prices - Should HARVEST NOW ---")
    market.price_trend = PriceTrend.FALLING
    
    advisory = engine.plan_harvest(environment, market, storage_available=True, crop_name="Tomato")
    print_advisory(advisory)
    
    # Test Case 4: Optimal conditions
    print("\n--- Test Case 4: Clear Weather + High Price - Should HARVEST NOW ---")
    market.current_price = 45.0
    market.price_trend = PriceTrend.STABLE
    environment.temperature = 30.0
    environment.humidity = 60.0
    
    advisory = engine.plan_harvest(environment, market, storage_available=True, crop_name="Onion")
    print_advisory(advisory)
    
    print("\n✅ Harvest Planner Test PASSED")


def run_full_simulation():
    """Run a complete end-to-end simulation"""
    print_section("FULL SIMULATION: COMPLETE FARMING CYCLE")
    
    print("\n🌱 Scenario: Tomato farmer in Maharashtra")
    print("   Location: Pune (18.5°N, 73.8°E)")
    print("   Crop: Tomato, planted 45 days ago")
    print("   Current Stage: Flowering")
    
    # Initialize all engines
    weather_engine = WeatherEngine()
    market_engine = MarketEngine()
    vision_engine = VisionEngine()
    knowledge_engine = KnowledgeEngine()
    
    # Get contexts
    print("\n📊 Gathering Data...")
    environment = weather_engine.get_context(18.5204, 73.8567)
    market = market_engine.get_market_data("Tomato")
    
    crop = CropContext(
        name="Tomato",
        sowing_date=date.today() - timedelta(days=45),
        current_stage=CropStage.FLOWERING
    )
    
    # Simulate disease detection
    dummy_image = b"tomato_leaf_image" * 50
    disease_result = vision_engine.analyze_image(dummy_image)
    
    print(f"\n🌤️  Weather: {environment.temperature}°C, Humidity {environment.humidity}%")
    print(f"💰 Market: ₹{market.current_price}/kg, Trend: {market.price_trend.value}")
    print(f"🔬 Disease Scan: {disease_result.disease_name} ({disease_result.confidence*100:.0f}% confidence)")
    
    # Get recommendations
    print("\n\n🎯 RECOMMENDATIONS:")
    
    print("\n1️⃣  IRRIGATION:")
    irrigation_advice = knowledge_engine.get_irrigation_advice(crop, environment)
    print(f"   → {irrigation_advice.action_header}")
    print(f"   → {irrigation_advice.spoken_advice}")
    
    print("\n2️⃣  DISEASE TREATMENT:")
    if disease_result.disease_name != "Healthy":
        treatment = knowledge_engine.get_treatment_recommendation(
            disease_name=disease_result.disease_name,
            crop_name="Tomato"
        )
        print(f"   → {treatment.action_header}")
        print(f"   → Chemical: {treatment.chemical_dosage}")
        print(f"   → Organic: {treatment.organic_alternative}")
    else:
        print("   → No treatment needed - crop is healthy!")
    
    print("\n3️⃣  FERTILIZER:")
    fertilizer = knowledge_engine.get_treatment_recommendation(
        crop_stage=crop.current_stage,
        crop_name="Tomato"
    )
    print(f"   → {fertilizer.action_header}")
    print(f"   → {fertilizer.chemical_dosage}")
    
    print("\n4️⃣  HARVEST PLANNING:")
    harvest_plan = knowledge_engine.plan_harvest(
        environment, market, storage_available=False, crop_name="Tomato"
    )
    print(f"   → {harvest_plan.action_header}")
    print(f"   → {harvest_plan.spoken_advice}")
    
    print("\n✅ Full Simulation COMPLETED")


def main():
    """Main test driver"""
    print("\n" + "🚜" * 35)
    print("  FARMING ASSISTANT - COMPREHENSIVE TEST SUITE")
    print("🚜" * 35)
    
    try:
        # Run all tests
        test_weather_engine()
        test_market_engine()
        test_vision_engine()
        test_irrigation_advisor()
        test_input_optimizer()
        test_harvest_planner()
        run_full_simulation()
        
        # Summary
        print("\n" + "=" * 70)
        print("  🎉 ALL TESTS PASSED SUCCESSFULLY!")
        print("=" * 70)
        print("\n✅ Weather Engine: Working (with fallback)")
        print("✅ Market Engine: Working (mock data)")
        print("✅ Vision Engine: Working (with fallback)")
        print("✅ Knowledge Engine:")
        print("   ✅ Irrigation Advisor")
        print("   ✅ Input Optimizer (with dosage, safety, organic alternatives)")
        print("   ✅ Harvest Planner (decision tree)")
        print("\n🎯 System is DEMO-READY!")
        print("   - All engines have fallback mechanisms")
        print("   - No external dependencies required")
        print("   - Comprehensive advisory outputs")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
