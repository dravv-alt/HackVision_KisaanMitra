"""
Government Scheme Suggestor - Wrapper module
Provides simplified interface for scheme suggestions
"""
from typing import List
from .service import PreSeedingService
from .models import PlanningRequest, SchemeEligibilityResult
from .constants import RiskPreference


def suggest_schemes_for_farmer(farmer_id: str) -> List[SchemeEligibilityResult]:
    """
    Get government scheme suggestions for a farmer
    
    Args:
        farmer_id: Unique farmer identifier
        
    Returns:
        List of scheme eligibility results (eligible schemes first)
        
    Example:
        >>> schemes = suggest_schemes_for_farmer("F001")
        >>> eligible = [s for s in schemes if s.eligible]
        >>> print(f"Eligible for {len(eligible)} schemes")
    """
    service = PreSeedingService()
    request = PlanningRequest(
        farmer_id=farmer_id,
        risk_preference=RiskPreference.BALANCED
    )
    
    output = service.run(request)
    return output.scheme_cards


if __name__ == "__main__":
    # Quick test
    print("Testing scheme suggestions...")
    schemes = suggest_schemes_for_farmer("F001")
    eligible = [s for s in schemes if s.eligible]
    print(f"✓ Eligible for {len(eligible)} schemes")
    for scheme in eligible[:3]:
        print(f"  - {scheme.scheme_name}")
