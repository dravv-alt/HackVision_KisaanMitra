"""
Farm Management System - CLI Testing Module
Simple menu-driven interface to test all three stages manually
"""

import sys
import os
from datetime import date, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_separator():
    """Print separator line"""
    print("-" * 70)


def wait_for_enter():
    """Wait for user to press Enter"""
    input("\nPress Enter to continue...")


# ============================================================================
# PLANNING STAGE TESTS
# ============================================================================

def test_planning_stage():
    """Test Planning Stage functions"""
    from Planning_stage import PreSeedingService, PlanningRequest
    from Planning_stage.crop_selection import recommend_crops_for_farmer
    from Planning_stage.gov_scheme_suggestor import suggest_schemes_for_farmer
    
    while True:
        print_header("PLANNING STAGE - Test Menu")
        print("\n1. Get Crop Recommendations (Farmer F001)")
        print("2. Check Scheme Eligibility (Farmer F001)")
        print("3. Full Planning Report (Farmer F001)")
        print("4. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            print_header("Crop Recommendations Test")
            try:
                crops = recommend_crops_for_farmer("F001")
                print(f"\n✅ Found {len(crops)} crop recommendations:\n")
                for i, crop in enumerate(crops, 1):
                    print(f"{i}. {crop.crop_name} ({crop.crop_name_hindi})")
                    print(f"   Score: {crop.score:.1f}/100")
                    print(f"   Profit Level: {crop.profit_level.value}")
                    print(f"   Reasons: {', '.join(crop.reasons[:2])}")
                    print()
            except Exception as e:
                print(f"❌ Error: {e}")
            wait_for_enter()
        
        elif choice == "2":
            print_header("Scheme Eligibility Test")
            try:
                schemes = suggest_schemes_for_farmer("F001")
                eligible = [s for s in schemes if s.eligible]
                print(f"\n✅ Eligible for {len(eligible)} schemes:\n")
                for scheme in eligible:
                    print(f"✅ {scheme.scheme_name}")
                    print(f"   {scheme.scheme_name_hindi}")
                    if scheme.deadline_warning:
                        print(f"   ⚠️  {scheme.deadline_warning}")
                    print(f"   Docs: {', '.join(scheme.docs_required[:3])}")
                    print()
            except Exception as e:
                print(f"❌ Error: {e}")
            wait_for_enter()
        
        elif choice == "3":
            print_header("Full Planning Report Test")
            try:
                service = PreSeedingService()
                request = PlanningRequest(farmer_id="F001")
                output = service.run(request)
                
                print(f"\n📋 {output.header}")
                print(f"🌤️  {output.weather_summary}")
                print(f"\n🌱 Top 3 Crops:")
                for i, crop in enumerate(output.crop_cards[:3], 1):
                    print(f"  {i}. {crop.crop_name}: {crop.score:.1f}/100")
                
                eligible = [s for s in output.scheme_cards if s.eligible]
                print(f"\n📋 Eligible Schemes: {len(eligible)}")
                for scheme in eligible[:3]:
                    print(f"  ✅ {scheme.scheme_name}")
                
                print(f"\n⏰ Reminders: {len(output.reminders)}")
                print(f"\n🎤 Voice Output:")
                print(f"   {output.speech_text[:200]}...")
            except Exception as e:
                print(f"❌ Error: {e}")
            wait_for_enter()
        
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")


# ============================================================================
# FARMING STAGE TESTS
# ============================================================================

def test_farming_stage():
    """Test Farming Stage functions"""
    from Farming_stage.engines import WeatherEngine, MarketEngine, VisionEngine, KnowledgeEngine
    from Farming_stage.models import CropContext, EnvironmentalContext, MarketContext, CropStage, PriceTrend, DemandLevel
    
    while True:
        print_header("FARMING STAGE - Test Menu")
        print("\n1. Get Weather Data (Pune)")
        print("2. Get Market Prices (Onion)")
        print("3. Detect Disease (Mock Image)")
        print("4. Get Irrigation Advice (Tomato - Flowering)")
        print("5. Get Treatment Recommendation (Leaf Blight)")
        print("6. Plan Harvest (Onion)")
        print("7. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            print_header("Weather Data Test")
            try:
                engine = WeatherEngine()
                context = engine.get_context(18.5204, 73.8567)  # Pune
                print(f"\n🌤️  Weather in Pune:")
                print(f"   Temperature: {context.temperature}°C")
                print(f"   Humidity: {context.humidity}%")
                print(f"   Rain Forecast: {'Yes' if context.rain_forecast else 'No'}")
                if context.wind_speed:
                    print(f"   Wind Speed: {context.wind_speed} km/h")
            except Exception as e:
                print(f"❌ Error: {e}")
            wait_for_enter()
        
        elif choice == "2":
            print_header("Market Prices Test")
            try:
                engine = MarketEngine()
                market = engine.get_market_data("Onion")
                print(f"\n💰 Onion Market Data:")
                print(f"   Current Price: ₹{market.current_price}/kg")
                print(f"   Price Trend: {market.price_trend.value.upper()}")
                print(f"   Demand Level: {market.demand_level.value.upper()}")
                
                forecast = engine.get_price_forecast("Onion", days_ahead=7)
                print(f"\n📈 7-Day Forecast:")
                print(f"   {forecast}")
            except Exception as e:
                print(f"❌ Error: {e}")
            wait_for_enter()
        
        elif choice == "3":
            print_header("Disease Detection Test")
            try:
                engine = VisionEngine()
                dummy_image = b"fake_image_data" * 100
                result = engine.analyze_image(dummy_image)
                
                print(f"\n🔬 Disease Detection Result:")
                print(f"   Disease: {result.disease_name}")
                print(f"   Confidence: {result.confidence * 100:.1f}%")
                print(f"   Mock Result: {'Yes' if result.is_mock else 'No'}")
                
                if result.disease_name != "Healthy":
                    info = engine.get_disease_info(result.disease_name)
                    print(f"\n📚 Disease Info:")
                    print(f"   Severity: {info.get('severity', 'Unknown')}")
                    print(f"   Spread Rate: {info.get('spread_rate', 'Unknown')}")
            except Exception as e:
                print(f"❌ Error: {e}")
            wait_for_enter()
        
        elif choice == "4":
            print_header("Irrigation Advice Test")
            try:
                weather_engine = WeatherEngine()
                knowledge_engine = KnowledgeEngine()
                
                crop = CropContext(
                    name="Tomato",
                    sowing_date=date.today() - timedelta(days=30),
                    current_stage=CropStage.FLOWERING
                )
                environment = weather_engine.get_context(18.5204, 73.8567)
                
                advice = knowledge_engine.get_irrigation_advice(crop, environment)
                
                print(f"\n💧 Irrigation Advice:")
                print(f"   Action: {advice.action_header}")
                print(f"   Urgency: {advice.urgency.value.upper()}")
                print(f"\n   🎤 Spoken Advice:")
                print(f"   {advice.spoken_advice}")
                print(f"\n   📝 Reasoning:")
                print(f"   {advice.detailed_reasoning}")
            except Exception as e:
                print(f"❌ Error: {e}")
            wait_for_enter()
        
        elif choice == "5":
            print_header("Treatment Recommendation Test")
            try:
                engine = KnowledgeEngine()
                advice = engine.get_treatment_recommendation(
                    disease_name="Leaf Blight",
                    crop_name="Tomato"
                )
                
                print(f"\n💊 Treatment Recommendation:")
                print(f"   Action: {advice.action_header}")
                print(f"   Urgency: {advice.urgency.value.upper()}")
                print(f"\n   Chemical Dosage:")
                print(f"   {advice.chemical_dosage}")
                print(f"\n   🌿 Organic Alternative:")
                print(f"   {advice.organic_alternative}")
                if advice.safety_warning:
                    print(f"\n   ⚠️  Safety Warning:")
                    print(f"   {advice.safety_warning}")
            except Exception as e:
                print(f"❌ Error: {e}")
            wait_for_enter()
        
        elif choice == "6":
            print_header("Harvest Planning Test")
            try:
                weather_engine = WeatherEngine()
                market_engine = MarketEngine()
                knowledge_engine = KnowledgeEngine()
                
                environment = weather_engine.get_context(18.5204, 73.8567)
                market = market_engine.get_market_data("Onion")
                
                advice = knowledge_engine.plan_harvest(
                    environment, market, storage_available=True, crop_name="Onion"
                )
                
                print(f"\n🌾 Harvest Planning:")
                print(f"   Decision: {advice.action_header}")
                print(f"   Urgency: {advice.urgency.value.upper()}")
                print(f"\n   🎤 Spoken Advice:")
                print(f"   {advice.spoken_advice}")
                print(f"\n   📝 Reasoning:")
                print(f"   {advice.detailed_reasoning}")
            except Exception as e:
                print(f"❌ Error: {e}")
            wait_for_enter()
        
        elif choice == "7":
            break
        else:
            print("❌ Invalid choice. Please enter 1-7.")


# ============================================================================
# POST-HARVEST STAGE TESTS
# ============================================================================

def test_post_harvest_stage():
    """Test Post-Harvest Stage functions"""
    from Post_Harvest_stage.core import FarmerContext, PostHarvestDecisionEngine
    
    while True:
        print_header("POST-HARVEST STAGE - Test Menu")
        print("\n1. Storage Decision - Onion (1000 kg)")
        print("2. Storage Decision - Tomato (500 kg)")
        print("3. Storage Decision - Wheat (2000 kg)")
        print("4. Custom Input")
        print("5. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice in ["1", "2", "3"]:
            crop_data = {
                "1": ("onion", 1000),
                "2": ("tomato", 500),
                "3": ("wheat", 2000)
            }
            crop_name, quantity = crop_data[choice]
            
            print_header(f"Storage Decision - {crop_name.title()}")
            try:
                context = FarmerContext(
                    crop_name=crop_name,
                    quantity_kg=quantity,
                    farmer_location=(18.52, 73.86),  # Pune
                    harvest_date=date.today(),
                    today_date=date.today()
                )
                
                engine = PostHarvestDecisionEngine()
                result = engine.run_decision(context)
                
                print(f"\n📦 Storage Decision: {result.storage_decision.upper()}")
                print(f"   Wait Days: {result.recommended_wait_days}")
                print(f"   Spoilage Risk: {result.spoilage_risk.upper()}")
                print(f"   Max Safe Days: {result.max_safe_storage_days}")
                
                print(f"\n🏪 Market Recommendation:")
                print(f"   Best Market: {result.best_market_name}")
                print(f"   Market Price: ₹{result.market_price}/kg")
                print(f"   Transport Cost: ₹{result.transport_cost:,.2f}")
                print(f"   Storage Cost: ₹{result.storage_cost:,.2f}")
                print(f"   Net Profit: ₹{result.net_profit:,.2f}")
                
                print(f"\n📈 Price Forecast:")
                print(f"   Current Price: ₹{result.current_price}/kg")
                print(f"   Peak Price: ₹{result.peak_price}/kg")
                print(f"   Peak Day: {result.peak_day}")
                print(f"   Trend: {result.price_trend.upper()}")
                
                print(f"\n💡 Reasoning:")
                print(f"   {result.storage_reasoning}")
                
                if result.alternative_markets:
                    print(f"\n🔄 Alternative Markets:")
                    for i, alt in enumerate(result.alternative_markets[:2], 1):
                        print(f"   {i}. {alt['market_name']}: ₹{alt['net_profit']:,.2f} net profit")
            except Exception as e:
                print(f"❌ Error: {e}")
            wait_for_enter()
        
        elif choice == "4":
            print_header("Custom Storage Decision")
            try:
                print("\nAvailable crops: onion, potato, tomato, wheat, rice, cotton, cabbage, carrot")
                crop = input("Enter crop name: ").strip().lower()
                quantity = float(input("Enter quantity (kg): ").strip())
                
                context = FarmerContext(
                    crop_name=crop,
                    quantity_kg=quantity,
                    farmer_location=(18.52, 73.86),
                    harvest_date=date.today(),
                    today_date=date.today()
                )
                
                engine = PostHarvestDecisionEngine()
                result = engine.run_decision(context)
                
                print(f"\n📦 Decision: {result.storage_decision.upper()}")
                print(f"🏪 Best Market: {result.best_market_name}")
                print(f"💰 Net Profit: ₹{result.net_profit:,.2f}")
                print(f"💡 Reasoning: {result.storage_reasoning}")
            except Exception as e:
                print(f"❌ Error: {e}")
            wait_for_enter()
        
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    """Main menu"""
    print_header("🌾 FARM MANAGEMENT SYSTEM - CLI TESTING MODULE 🌾")
    print("\nWelcome! This tool helps you test all three farming stages manually.")
    
    while True:
        print_header("MAIN MENU")
        print("\n1. Test Planning Stage (Pre-Seeding)")
        print("2. Test Farming Stage (Growing Season)")
        print("3. Test Post-Harvest Stage (Selling Decision)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            test_planning_stage()
        elif choice == "2":
            test_farming_stage()
        elif choice == "3":
            test_post_harvest_stage()
        elif choice == "4":
            print_header("Thank you for using the Farm Management Testing Module!")
            print("\n👋 Goodbye!\n")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
