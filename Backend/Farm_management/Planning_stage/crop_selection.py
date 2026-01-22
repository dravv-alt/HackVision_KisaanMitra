"""
Crop Selection - Wrapper module for backward compatibility
This provides a simplified interface to the crop recommendation engine
"""
from typing import List, Optional
from .service import PreSeedingService
from .models import PlanningRequest, CropRecommendation, FarmerProfile
from .constants import Season, RiskPreference


def recommend_crops_for_farmer(
    farmer_id: str,
    season: Optional[Season] = None,
    risk_preference: RiskPreference = RiskPreference.BALANCED
) -> List[CropRecommendation]:
    """
    Simplified function to get crop recommendations for a farmer
    
    Args:
        farmer_id: Unique farmer identifier
        season: Target season (auto-detect if None)
        risk_preference: Risk appetite for crop selection
        
    Returns:
        List of recommended crops
        
    Example:
        >>> crops = recommend_crops_for_farmer("F001", season=Season.KHARIF)
        >>> print(f"Top crop: {crops[0].crop_name}")
    """
    service = PreSeedingService()
    request = PlanningRequest(
        farmer_id=farmer_id,
        season=season,
        risk_preference=risk_preference
    )
    
    output = service.run(request)
    return output.crop_cards


def get_full_planning_report(
    farmer_id: str,
    season: Optional[Season] = None,
    risk_preference: RiskPreference = RiskPreference.BALANCED
):
    """
    Get complete pre-seeding planning report
    
    Args:
        farmer_id: Unique farmer identifier
        season: Target season (auto-detect if None)
        risk_preference: Risk appetite
        
    Returns:
        PreSeedingOutput with crops, schemes, reminders
    """
    service = PreSeedingService()
    request = PlanningRequest(
        farmer_id=farmer_id,
        season=season,
        risk_preference=risk_preference
    )
    
    return service.run(request)


if __name__ == "__main__":
    # Quick test
    print("Testing crop selection...")
    crops = recommend_crops_for_farmer("F001")
    print(f"✓ Got {len(crops)} crop recommendations")
    for crop in crops:
        print(f"  - {crop.crop_name}: {crop.score:.1f}/100")
