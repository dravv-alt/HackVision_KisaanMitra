"""
Simple Test Runner - Tests Post-Harvest Decision Engine
"""
from datetime import date, timedelta
import json
import sys
import os

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import modules directly
from core.context import FarmerContext
from core.engine import PostHarvestDecisionEngine


def test_scenario_1():
    """Test: Onion with rising prices"""
    print("\n" + "="*70)
    print("TEST 1: ONION WITH RISING PRICES")
    print("="*70)
    
    context = FarmerContext(
        crop_name="onion",
        quantity_kg=1000,
        farmer_location=(18.5204, 73.8567),  # Pune
        harvest_date=date.today(),
        today_date=date.today()
    )
    
    engine = PostHarvestDecisionEngine()
    result = engine.run_decision(context)
    
    print(f"\n✅ Storage Decision: {result.storage_decision}")
    print(f"   Wait Days: {result.recommended_wait_days}")
    print(f"   Spoilage Risk: {result.spoilage_risk}")
    
    print(f"\n✅ Best Market: {result.best_market_name}")
    print(f"   Price: ₹{result.market_price}/kg")
    print(f"   Net Profit: ₹{result.net_profit:,.2f}")
    
    print(f"\n✅ Price Trend: {result.price_trend}")
    print(f"   Current: ₹{result.current_price}/kg")
    print(f"   Peak: ₹{result.peak_price}/kg on day {result.peak_day}")
    
    print(f"\n📝 Reasoning: {result.storage_reasoning}")


def test_scenario_2():
    """Test: Tomato near spoilage"""
    print("\n" + "="*70)
    print("TEST 2: TOMATO NEAR SPOILAGE")
    print("="*70)
    
    context = FarmerContext(
        crop_name="tomato",
        quantity_kg=500,
        farmer_location=(19.0760, 72.8777),  # Mumbai
        harvest_date=date.today() - timedelta(days=3),
        today_date=date.today()
    )
    
    engine = PostHarvestDecisionEngine()
    result = engine.run_decision(context)
    
    print(f"\n✅ Storage Decision: {result.storage_decision}")
    print(f"   Wait Days: {result.recommended_wait_days}")
    print(f"   Spoilage Risk: {result.spoilage_risk}")
    
    print(f"\n✅ Best Market: {result.best_market_name}")
    print(f"   Net Profit: ₹{result.net_profit:,.2f}")
    
    print(f"\n📝 Reasoning: {result.storage_reasoning}")


def test_scenario_3():
    """Test: Potato with high transport cost"""
    print("\n" + "="*70)
    print("TEST 3: POTATO - HIGH TRANSPORT COST")
    print("="*70)
    
    context = FarmerContext(
        crop_name="potato",
        quantity_kg=2000,
        farmer_location=(16.7050, 74.2433),  # Kolhapur
        harvest_date=date.today(),
        today_date=date.today()
    )
    
    engine = PostHarvestDecisionEngine()
    result = engine.run_decision(context)
    
    print(f"\n✅ Storage Decision: {result.storage_decision}")
    print(f"\n✅ Best Market: {result.best_market_name}")
    print(f"   Transport Cost: ₹{result.transport_cost:,.2f}")
    print(f"   Net Profit: ₹{result.net_profit:,.2f}")
    
    if result.alternative_markets:
        print(f"\n📊 Why not {result.alternative_markets[0]['market_name']}?")
        print(f"   Price might be higher, but transport cost makes it less profitable")


def main():
    print("\n" + "🌾"*35)
    print("  POST-HARVEST DECISION ENGINE - TESTS")
    print("🌾"*35)
    
    try:
        test_scenario_1()
        test_scenario_2()
        test_scenario_3()
        
        print("\n" + "="*70)
        print("  🎉 ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\n✅ Engine outputs structured decision data")
        print("✅ Voice explanation handled by external layer")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
