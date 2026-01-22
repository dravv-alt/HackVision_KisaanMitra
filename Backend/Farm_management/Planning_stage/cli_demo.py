"""
CLI Demo for Pre-Seeding Planning Stage
Interactive command-line demonstration of all features
Runs without internet connection using fallback data
"""
import sys
import os
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from service import PreSeedingService
from models import PlanningRequest
from constants import Season, RiskPreference
from repositories import FarmerRepository


def print_header():
    """Print demo header"""
    print("\n" + "=" * 80)
    print("🌾 PRE-SEEDING PLANNING STAGE - INTERACTIVE DEMO")
    print("   Voice-First AI Farming Assistant (Backend Module)")
    print("=" * 80)


def print_section(title: str):
    """Print section header"""
    print(f"\n{'─' * 80}")
    print(f"📌 {title}")
    print('─' * 80)


def list_available_farmers():
    """Show available demo farmers"""
    print_section("Available Demo Farmers")
    
    farmer_repo = FarmerRepository()
    farmers = {
        "F001": "Punjab farmer - Alluvial soil, Canal irrigation",
        "F002": "Maharashtra farmer - Black soil, Rainfed",
        "F003": "Karnataka farmer - Red soil, Drip irrigation",
        "F004": "UP farmer - Loamy soil, Tube well",
        "F005": "Rajasthan farmer - Sandy soil, Sprinkler"
    }
    
    for farmer_id, desc in farmers.items():
        farmer = farmer_repo.get_farmer(farmer_id)
        if farmer:
            print(f"\n  {farmer_id}: {desc}")
            print(f"         Location: {farmer.location.district}, {farmer.location.state}")
            print(f"         Land: {farmer.land_size_acres} acres")


def get_user_input() -> tuple:
    """Get user inputs for planning"""
    print_section("Planning Configuration")
    
    # Farmer ID
    print("\nEnter Farmer ID (F001-F005, or press Enter for F001):")
    farmer_id = input("  Farmer ID: ").strip() or "F001"
    
    # Season
    print("\nSelect Season:")
    print("  1. Kharif (June-October)")
    print("  2. Rabi (November-March)")
    print("  3. Zaid (March-June)")
    print("  4. Auto-detect from current date")
    season_choice = input("  Choice (1-4, default 4): ").strip() or "4"
    
    season_map = {
        "1": Season.KHARIF,
        "2": Season.RABI,
        "3": Season.ZAID,
        "4": None
    }
    season = season_map.get(season_choice, None)
    
    # Risk preference
    print("\nSelect Risk Preference:")
    print("  1. Safe (Low-risk crops)")
    print("  2. Balanced (Mix of profit and safety)")
    print("  3. High Profit (Higher risk, higher returns)")
    risk_choice = input("  Choice (1-3, default 2): ").strip() or "2"
    
    risk_map = {
        "1": RiskPreference.SAFE,
        "2": RiskPreference.BALANCED,
        "3": RiskPreference.HIGH_PROFIT
    }
    risk_pref = risk_map.get(risk_choice, RiskPreference.BALANCED)
    
    return farmer_id, season, risk_pref


def display_results(output):
    """Display planning results in readable format"""
    
    # Weather Summary
    print_section("🌤️  Weather Context")
    print(f"\n{output.weather_summary}")
    
    # Crop Recommendations
    print_section("🌱 Crop Recommendations")
    if not output.crop_cards:
        print("\n  ⚠️  No suitable crops found for current conditions.")
    else:
        for i, crop in enumerate(output.crop_cards, 1):
            print(f"\n  {i}. {crop.crop_name}")
            if crop.crop_name_hi:
                print(f"     ({crop.crop_name_hi})")
            print(f"     ├─ Suitability Score: {crop.score:.1f}/100")
            print(f"     ├─ Profit Potential: {crop.profit_level.value.upper()}")
            print(f"     ├─ Why Recommended:")
            for reason in crop.reasons:
                print(f"     │  • {reason}")
            
            if crop.risks:
                print(f"     ├─ Risks:")
                for risk in crop.risks:
                    print(f"     │  ⚠ {risk}")
            
            print(f"     ├─ Requirements:")
            req = crop.crop_requirements
            if req.seed_rate_kg_per_acre:
                print(f"     │  • Seed rate: {req.seed_rate_kg_per_acre} kg/acre")
            if req.fertilizers:
                print(f"     │  • Fertilizers: {', '.join(req.fertilizers)}")
            if req.water_requirement:
                print(f"     │  • Water: {req.water_requirement}")
            
            if crop.seed_material_sources:
                print(f"     ├─ Where to buy seeds:")
                for source in crop.seed_material_sources[:2]:
                    print(f"     │  • {source.name} ({source.source_type})")
            
            if crop.sowing_window_hint:
                print(f"     └─ Timing: {crop.sowing_window_hint}")
    
    # Scheme Recommendations
    print_section("📋 Government Schemes")
    eligible_schemes = [s for s in output.scheme_cards if s.eligible]
    
    if not eligible_schemes:
        print("\n  No schemes available for current criteria.")
    else:
        print(f"\n  ✅ You are ELIGIBLE for {len(eligible_schemes)} schemes:\n")
        
        for i, scheme in enumerate(eligible_schemes, 1):
            print(f"  {i}. {scheme.scheme_name}")
            if scheme.scheme_name_hi:
                print(f"     ({scheme.scheme_name_hi})")
            
            if scheme.deadline_warning:
                print(f"     ⏰ {scheme.deadline_warning}")
            
            print(f"     ├─ Why Eligible:")
            for reason in scheme.why_eligible[:3]:
                print(f"     │  ✓ {reason}")
            
            if scheme.docs_required:
                print(f"     ├─ Required Documents:")
                for doc in scheme.docs_required[:3]:
                    print(f"     │  📄 {doc}")
            
            print(f"     └─ Next Step: {scheme.next_step}")
            print()
    
    # Not eligible schemes (top 2)
    not_eligible = [s for s in output.scheme_cards if not s.eligible][:2]
    if not_eligible:
        print(f"\n  ❌ Not eligible for {len([s for s in output.scheme_cards if not s.eligible])} schemes")
        print("     (showing top 2):\n")
        for scheme in not_eligible:
            print(f"  • {scheme.scheme_name}")
            if scheme.why_not_eligible:
                print(f"    Reason: {scheme.why_not_eligible[0]}")
    
    # Reminders
    print_section("⏰ Reminders Created")
    if not output.reminders:
        print("\n  No deadline reminders needed at this time.")
    else:
        print(f"\n  {len(output.reminders)} reminder(s) scheduled:\n")
        for reminder in output.reminders:
            print(f"  • {reminder.scheme_name}")
            print(f"    ⏰ {reminder.reminder_datetime.strftime('%d %b %Y, %I:%M %p')}")
            print(f"    📱 {reminder.message}")
            print()
    
    # Voice-First Speech Output
    print_section("🎤 Voice Assistant Output")
    print(f"\n  Language: {output.language.value.upper()}")
    print(f"  Urgency: {output.urgency_level.value.upper()}\n")
    
    speech = output.speech_text if output.language.value == "en" else output.speech_text_hi
    print(f"  💬 \"{speech}\"\n")


def run_demo():
    """Main demo runner"""
    print_header()
    
    try:
        # Show available farmers
        list_available_farmers()
        
        # Get user input
        farmer_id, season, risk_pref = get_user_input()
        
        # Create service and request
        print_section("Processing...")
        print("\n⚙️  Initializing Pre-Seeding Service...")
        
        service = PreSeedingService()
        request = PlanningRequest(
            farmer_id=farmer_id,
            season=season,
            risk_preference=risk_pref
        )
        
        # Execute planning
        print("⚙️  Running planning workflow...\n")
        output = service.run(request)
        
        # Display results
        display_results(output)
        
        # Summary
        print_section("✅ Planning Complete!")
        print(f"\n  📊 Summary:")
        print(f"     • {len(output.crop_cards)} crops recommended")
        print(f"     • {len([s for s in output.scheme_cards if s.eligible])} schemes eligible")
        print(f"     • {len(output.reminders)} reminders created")
        print(f"     • Urgency level: {output.urgency_level.value.upper()}")
        
        print("\n" + "=" * 80)
        print("✅ Demo completed successfully!")
        print("   This module is ready for FastAPI integration.")
        print("=" * 80 + "\n")
        
        return output
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return None


def run_quick_test():
    """Quick automated test without user input"""
    print_header()
    print("\n🔥 Running Quick Test (F001, Auto-detect season, Balanced risk)\n")
    
    service = PreSeedingService()
    request = PlanningRequest(
        farmer_id="F001",
        season=None,
        risk_preference=RiskPreference.BALANCED
    )
    
    output = service.run(request)
    display_results(output)
    
    print("\n" + "=" * 80)
    print("✅ Quick test completed!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    # Check if quick test flag is provided
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_quick_test()
    else:
        run_demo()
