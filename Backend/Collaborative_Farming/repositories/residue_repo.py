"""
Residue Repository for Collaborative Farming (Future Scope)
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import uuid

from ..models import ResidueListing


class ResidueRepo:
    def __init__(self):
        self._listings: Dict[str, ResidueListing] = {}
        self.seed_mock_residue_if_empty()

    def create_residue_listing(self, listing: ResidueListing) -> ResidueListing:
        """Create a new residue listing"""
        self._listings[listing.residueId] = listing
        return listing

    def list_open_residue(self, filters: Dict) -> List[ResidueListing]:
        """List open residue listings with filters"""
        results = [r for r in self._listings.values() if r.status == "OPEN"]
        
        if "district" in filters:
            results = [r for r in results if r.district == filters["district"]]
            
        return results

    def seed_mock_residue_if_empty(self):
        """Seed mock residue listings if repository is empty"""
        if self._listings:
            return
            
        now = datetime.now()
        
        r1 = ResidueListing(
            residueId=str(uuid.uuid4()),
            farmerId="FARMER001",
            cropType="Wheat",
            quantityKg=500.0,
            expectedPricePerKg=2.5,
            district="Nashik",
            pincode="422001"
        )
        
        r2 = ResidueListing(
            residueId=str(uuid.uuid4()),
            farmerId="FARMER007",
            cropType="Rice",
            quantityKg=1200.0,
            expectedPricePerKg=3.0,
            district="Nashik",
            pincode="422001"
        )
        
        self._listings[r1.residueId] = r1
        self._listings[r2.residueId] = r2
