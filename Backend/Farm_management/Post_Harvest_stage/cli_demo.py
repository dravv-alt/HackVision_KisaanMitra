"""
CLI Demo - Interactive testing of Post-Harvest Decision Engine
Run this file to test the system manually
"""

import sys
import os
from datetime import date, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.context import FarmerContext
from core.engine import PostHarvestDecisionEngine, DecisionResult
import json


def print_separator(char="=", length=70):
    """Print a separator line"""
    print(char * length)


def print_section(title: str):
    """Print formatted section header"""
    print("\n")
    print_separator()
    print(f"  {title}")
    print_separator()


def format_decision_result(result: DecisionResult) -> None:
    """Pretty print decision result"""
    
    print_section("📦 STORAGE DECISION")
    print(json.dumps({
        "decision": result.storage_decision,
        "recommended_wait_days": result.recommended_wait_days,
        "spoilage_risk": result.spoilage_risk,
        "max_safe_storage_days": result.max_safe_storage_days,
        "storage_type": result.storage_type_recommended,
        "reasoning": result.storage_reasoning
    }, indent=2))
    
    print_section("🏪 MARKET RECOMMENDATION")
    print(json.dumps({
        "market_name": result.best_market_name,
        "price_per_kg": result.market_price,
        "transport_cost": result.transport_cost,
        "storage_cost": result.storage_cost,
        "net_profit": result.net_profit,
        "profit_margin_percent": result.profit_margin_percent
    }, indent=2))
    
    print_section("📈 PRICE FORECAST")
    print(json.dumps({
        "current_price": result.current_price,
        "peak_price": result.peak_price,
        "peak_day": result.peak_day,
        "trend": result.price_trend
    }, indent=2))
    
    if result.alternative_markets:
        print_section("🔄 ALTERNATIVE MARKETS")
        for i, alt in enumerate(result.alternative_markets[:3], 1):
            print(f"\n{i}. {alt['market_name']}")
            print(f"   Price: ₹{alt['price']}/kg")
            print(f"   Distance: {alt['distance_km']} km")
            print(f"   Net Profit: ₹{alt['net_profit']}")


def run_predefined_scenarios():
    """Run predefined test scenarios"""
    print_section("🌾 POST-HARVEST DECISION ENGINE - TEST SCENARIOS")
    
    engine = PostHarvestDecisionEngine()
    
    scenarios = [
        {
            "name": "Scenario 1: Onion with Rising Prices",
            "context": FarmerContext(
                crop_name="onion",
                quantity_kg=1000,
                farmer_location=(18.5204, 73.8567),  # Pune
                harvest_date=date.today(),
                today_date=date.today()
            )
        },
        {
            "name": "Scenario 2: Tomato Near Spoilage",
            "context": FarmerContext(
                crop_name="tomato",
                quantity_kg=500,
                farmer_location=(19.0760, 72.8777),  # Mumbai
                harvest_date=date.today() - timedelta(days=3),
                today_date=date.today()
            )
        },
        {
            "name": "Scenario 3: Potato - High Transport Cost",
            "context": FarmerContext(
                crop_name="potato",
                quantity_kg=2000,
                farmer_location=(16.7050, 74.2433),  # Kolhapur
                harvest_date=date.today(),
                today_date=date.today()
            )
        },
        {
            "name": "Scenario 4: Wheat - Stable Prices",
            "context": FarmerContext(
                crop_name="wheat",
                quantity_kg=1500,
                farmer_location=(19.8762, 75.3433),  # Aurangabad
                harvest_date=date.today(),
                today_date=date.today()
            )
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print_section(f"TEST {i}: {scenario['name']}")
        print(f"\nCrop: {scenario['context'].crop_name.title()}")
        print(f"Quantity: {scenario['context'].quantity_kg} kg")
        print(f"Days since harvest: {scenario['context'].days_since_harvest()}")
        
        try:
            result = engine.run_decision(scenario['context'])
            format_decision_result(result)
            print("\n✅ Test PASSED")
        except Exception as e:
            print(f"\n❌ Test FAILED: {e}")
            import traceback
            traceback.print_exc()


def run_interactive_mode():
    """Interactive CLI for manual testing"""
    print_section("🌾 POST-HARVEST DECISION ASSISTANT")
    
    print("\nEnter farmer details:")
    
    # Get inputs
    try:
        crop_name = input("1. Crop name (onion/tomato/potato/wheat): ").strip()
        quantity_str = input("2. Quantity (kg): ").strip()
        lat_str = input("3. Latitude: ").strip()
        lon_str = input("4. Longitude: ").strip()
        days_since_str = input("5. Days since harvest: ").strip()
        
        # Parse inputs
        quantity_kg = float(quantity_str)
        lat = float(lat_str)
        lon = float(lon_str)
        days_since = int(days_since_str)
        
        harvest_date = date.today() - timedelta(days=days_since)
        
        # Create context
        context = FarmerContext(
            crop_name=crop_name,
            quantity_kg=quantity_kg,
            farmer_location=(lat, lon),
            harvest_date=harvest_date,
            today_date=date.today()
        )
        
        # Run engine
        print("\n⏳ Running decision engine...")
        engine = PostHarvestDecisionEngine()
        result = engine.run_decision(context)
        
        # Display result
        format_decision_result(result)
        
        print("\n✅ Analysis complete!")
        
    except ValueError as e:
        print(f"\n❌ Invalid input: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point"""
    print("\n" + "🌾" * 35)
    print("  POST-HARVEST DECISION ENGINE - CLI DEMO")
    print("🌾" * 35)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive_mode()
    else:
        print("\nRunning predefined test scenarios...")
        print("(Use --interactive flag for manual input mode)")
        run_predefined_scenarios()
    
    print("\n" + "=" * 70)
    print("  🎉 DEMO COMPLETE")
    print("=" * 70)
    print("\n📝 Note: This module outputs structured data.")
    print("   Voice explanation layer is handled externally.\n")


if __name__ == "__main__":
    main()
