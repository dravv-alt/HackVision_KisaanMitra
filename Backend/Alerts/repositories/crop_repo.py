"""
Crop Repository with Mock Fallback
"""

from typing import List, Dict
from ..models import FarmerCropContext


class CropRepo:
    def __init__(self):
        self._mock_crops: List[FarmerCropContext] = []
        self.seed_mock_crops_if_empty()

    def get_active_crops(self, farmer_id: str) -> List[FarmerCropContext]:
        """Fetch crop lifecycle context for a farmer"""
        crops = [c for c in self._mock_crops if c.farmerId == farmer_id]
        if not crops:
            # Demo fallback
            return [c for c in self._mock_crops if c.farmerId == "FARMER001"]
        return crops

    def seed_mock_crops_if_empty(self):
        if self._mock_crops:
            return
            
        self._mock_crops.append(FarmerCropContext(
            farmerCropId="FC001",
            farmerId="FARMER001",
            cropKey="tomato",
            cropName="Tomato",
            stage="during_farming",
            subStage="flowering",
            areaAcres=2.0
        ))
        self._mock_crops.append(FarmerCropContext(
            farmerCropId="FC002",
            farmerId="FARMER001",
            cropKey="onion",
            cropName="Onion",
            stage="during_farming",
            subStage="vegetative",
            areaAcres=3.5
        ))
