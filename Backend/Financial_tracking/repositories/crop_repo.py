"""
Crop Repository - Crop Context Reader
Links financial transactions to specific crops
"""

from typing import List, Dict, Optional


class CropRepo:
    """
    Repository for crop context information
    Used to attribute costs/income to specific crops
    """

    def __init__(self):
        """Initialize with mock crop data"""
        self._crops: Dict[str, List[Dict]] = {}

    def get_active_crops(self, farmerId: str, season: Optional[str] = None) -> List[Dict]:
        """
        Get active crops for a farmer
        
        Args:
            farmerId: Farmer ID
            season: Optional season filter
            
        Returns:
            List of crop dictionaries
        """
        # In production: 
        # query = {"farmerId": farmerId, "status": "active"}
        # if season:
        #     query["season"] = season
        # return list(db.farmer_crops.find(query))
        
        crops = self._crops.get(farmerId, [])
        
        if season and crops:
            crops = [c for c in crops if c.get("season") == season]
        
        return crops

    def seed_mock_crops(self, farmerId: str, season: str) -> None:
        """
        Seed mock crop data for demo
        Only called if needed for context
        """
        if farmerId in self._crops:
            return
        
        mock_crops = [
            {
                "cropId": f"{farmerId}_wheat_kharif_2024",
                "farmerId": farmerId,
                "cropName": "Wheat",
                "cropNameHindi": "गेहूं",
                "season": season,
                "status": "harvested",
                "landArea": 2.5,  # acres
                "expectedYield": 40,  # quintals
                "actualYield": 35,  # quintals (slightly lower)
            }
        ]
        
        self._crops[farmerId] = mock_crops

    def get_crop_by_id(self, cropId: str) -> Optional[Dict]:
        """Get a specific crop by ID"""
        for crops_list in self._crops.values():
            for crop in crops_list:
                if crop.get("cropId") == cropId:
                    return crop
        return None
