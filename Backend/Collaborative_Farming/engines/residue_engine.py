"""
Residue Engine for Collaborative Farming (Future Scope)
"""

from typing import List, Dict
from ..models import ResidueListing
from ..repositories import ResidueRepo


class ResidueEngine:
    """Engine for listing and grouping crop residue (Future Scope)"""
    
    def __init__(self, residue_repo: ResidueRepo):
        self.repo = residue_repo

    def list_residue_offers(self, district: str) -> List[ResidueListing]:
        """List open residue offers in a district"""
        return self.repo.list_open_residue({"district": district})

    def group_residue_for_bulk_offer(self, residue_listings: List[ResidueListing]) -> List[Dict]:
        """
        Future Scope Logic: Group residue by crop type for bulk sale offers.
        Provides power in numbers for better pricing.
        """
        groups = {}
        for r in residue_listings:
            if r.cropType not in groups:
                groups[r.cropType] = {
                    "cropType": r.cropType,
                    "totalQty": 0.0,
                    "avgExpectedPrice": 0.0,
                    "memberCount": 0,
                    "district": r.district
                }
            
            g = groups[r.cropType]
            g["totalQty"] += r.quantityKg
            # Simple weighted average simulation
            g["avgExpectedPrice"] = (g["avgExpectedPrice"] * g["memberCount"] + r.expectedPricePerKg) / (g["memberCount"] + 1)
            g["memberCount"] += 1
            
        return list(groups.values())
