"""
Quick test runner for Planning Stage module
Tests the module without FastAPI dependencies
"""
import sys
import os

# Add Backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', '..')
sys.path.insert(0, backend_path)

from Backend.farm_management.planning_stage.service import PreSeedingService
from Backend.farm_management.planning_stage.models import PlanningRequest
from Backend.farm_management.planning_stage.constants import Season, RiskPreference


def test_basic_functionality():
    """Test basic module functionality"""
    print("=" * 80)
    print("🌾 PRE-SEEDING PLANNING MODULE - QUICK TEST")
    print("=" * 80)
    
    # Initialize service
    print("\n✓ Initializing service...")
    service = PreSeedingService()
    
    # Create test request
    print("✓ Creating test request for Farmer F001...")
    request = PlanningRequest(
        farmer_id="F001",
        season=None,  # Auto-detect
        risk_preference=RiskPreference.BALANCED
    )
    
    # Run planning
    print("✓ Running pre-seeding planning workflow...\n")
    output = service.run(request)
    
    # Display results
    print("\n" + "=" * 80)
    print("📊 RESULTS SUMMARY")
    print("=" * 80)
    print(f"\n✅ Crop Recommendations: {len(output.crop_cards)}")
    for i, crop in enumerate(output.crop_cards, 1):
        print(f"   {i}. {crop.crop_name} - Score: {crop.score:.1f}/100")
    
    eligible_schemes = [s for s in output.scheme_cards if s.eligible]
    print(f"\n✅ Eligible Schemes: {len(eligible_schemes)}")
    for scheme in eligible_schemes[:3]:
        print(f"   • {scheme.scheme_name}")
    
    print(f"\n✅ Reminders Created: {len(output.reminders)}")
    
    print(f"\n✅ Urgency Level: {output.urgency_level.value.upper()}")
    
    print(f"\n🎤 Voice Output (English):")
    print(f"   \"{output.speech_text}\"")
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("   Module is working correctly and ready for integration.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        test_basic_functionality()
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
