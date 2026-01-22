"""
Scheme Engine - checks eligibility and recommends schemes
"""
from typing import List, Optional
from datetime import datetime, timedelta
from ..models import (
    SchemeRecord, SchemeEligibilityResult, FarmerProfile, CropRecommendation
)


class SchemeEngine:
    """Engine for scheme eligibility and recommendations"""
    
    def __init__(self):
        """Initialize scheme engine"""
        pass
    
    def recommend_schemes(
        self,
        farmer: FarmerProfile,
        recommended_crops: List[CropRecommendation],
        all_schemes: List[SchemeRecord]
    ) -> List[SchemeEligibilityResult]:
        """
        Recommend schemes for farmer and their crop choices
        
        Args:
            farmer: Farmer profile
            recommended_crops: Crops recommended for farmer
            all_schemes: All available schemes
            
        Returns:
            List of scheme eligibility results (eligible first)
        """
        results = []
        crop_keys = [c.crop_key for c in recommended_crops]
        
        for scheme in all_schemes:
            # Check eligibility
            result = self.check_eligibility(farmer, scheme, crop_keys)
            results.append(result)
        
        # Sort: eligible first, then by deadline urgency
        results.sort(key=lambda x: (
            not x.eligible,  # False (eligible) comes first
            x.deadline_warning is None,  # With deadline comes first
        ))
        
        return results
    
    def check_eligibility(
        self,
        farmer: FarmerProfile,
        scheme: SchemeRecord,
        crop_keys: Optional[List[str]] = None
    ) -> SchemeEligibilityResult:
        """
        Check if farmer is eligible for a scheme
        
        Args:
            farmer: Farmer profile
            scheme: Scheme to check
            crop_keys: Planned crop keys (optional)
            
        Returns:
            SchemeEligibilityResult with eligibility status and reasons
        """
        eligible = True
        why_eligible = []
        why_not_eligible = []
        
        rules = scheme.eligibility_rules
        
        # Check state eligibility
        if scheme.states_eligible is not None:
            if farmer.location.state in scheme.states_eligible:
                why_eligible.append(f"Available in {farmer.location.state}")
            else:
                eligible = False
                why_not_eligible.append(f"Not available in {farmer.location.state}")
        else:
            why_eligible.append("Available across India")
        
        # Check land size requirements
        if "min_land_acres" in rules:
            min_land = rules["min_land_acres"]
            if farmer.land_size_acres >= min_land:
                if min_land > 0:
                    why_eligible.append(f"Land size meets requirement ({farmer.land_size_acres} acres)")
            else:
                eligible = False
                why_not_eligible.append(f"Requires minimum {min_land} acres (you have {farmer.land_size_acres})")
        
        # Check farmer type
        if "farmer_types" in rules:
            allowed_types = rules["farmer_types"]
            farmer_type = farmer.compute_farmer_type()
            if farmer_type.value in allowed_types:
                why_eligible.append(f"Farmer category ({farmer_type.value}) is eligible")
            else:
                eligible = False
                why_not_eligible.append(f"Only for {', '.join(allowed_types)} farmers")
        
        # Check irrigation requirement
        if "irrigation_type" in rules:
            required_irrig = rules["irrigation_type"]
            if farmer.irrigation_type.value == required_irrig:
                why_eligible.append(f"Irrigation type matches")
            else:
                eligible = False
                why_not_eligible.append(f"Requires {required_irrig} irrigation")
        
        # Check crop eligibility
        if scheme.crops_eligible is not None and crop_keys:
            crop_match = any(ck in scheme.crops_eligible for ck in crop_keys)
            if crop_match:
                why_eligible.append("Applicable for your planned crops")
            else:
                eligible = False
                why_not_eligible.append(
                    f"Only for: {', '.join(scheme.crops_eligible)}"
                )
        
        # Check special requirements
        if "kcc_holder" in rules and rules["kcc_holder"]:
            # Assume no KCC data; give conditional eligibility
            why_eligible.append("Requires Kisan Credit Card")
        
        if "crop_enrollment" in rules and rules["crop_enrollment"]:
            why_eligible.append("Must enroll crop details during application")
        
        # Deadline warning
        deadline_warning = None
        if scheme.deadline:
            days_left = (scheme.deadline - datetime.now()).days
            if days_left < 0:
                eligible = False
                why_not_eligible.append("Deadline has passed")
            elif days_left <= 15:
                deadline_warning = f"⚠ URGENT: Only {days_left} days left to apply!"
            elif days_left <= 30:
                deadline_warning = f"Apply soon: {days_left} days remaining"
        
        # Build next step
        next_step = self._build_next_step(scheme, eligible)
        
        return SchemeEligibilityResult(
            scheme_key=scheme.scheme_key,
            scheme_name=scheme.scheme_name,
            scheme_name_hi=scheme.scheme_name_hi,
            eligible=eligible,
            why_eligible=why_eligible,
            why_not_eligible=why_not_eligible,
            deadline_warning=deadline_warning,
            docs_required=scheme.docs_required if eligible else [],
            next_step=next_step,
            apply_url=scheme.apply_url if eligible else None
        )
    
    def _build_next_step(self, scheme: SchemeRecord, eligible: bool) -> str:
        """Build actionable next step text"""
        if not eligible:
            return "Not eligible for this scheme"
        
        if scheme.csc_applicable:
            return f"Visit nearest CSC or apply online at {scheme.apply_url or 'government portal'}"
        else:
            return f"Apply online at {scheme.apply_url or 'scheme portal'}"
