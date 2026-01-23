"""
Crop Card - Crop recommendation card
"""

from dataclasses import dataclass
from typing import List
from voice_agent.cards.base_card import BaseCard


@dataclass
class CropCard(BaseCard):
    """Crop recommendation card"""
    
    def __init__(
        self,
        crop_name: str,
        crop_name_hindi: str,
        score: float,
        reasons: List[str],
        risks: List[str],
        profit_level: str,
        **kwargs
    ):
        super().__init__(
            card_type="crop",
            title=f"{crop_name} ({crop_name_hindi})",
            summary=f"Score: {score:.1f}/100 - {profit_level} profit potential",
            details={
                "crop_name": crop_name,
                "crop_name_hindi": crop_name_hindi,
                "score": score,
                "reasons": reasons,
                "risks": risks,
                "profit_level": profit_level,
            },
            **kwargs
        )
