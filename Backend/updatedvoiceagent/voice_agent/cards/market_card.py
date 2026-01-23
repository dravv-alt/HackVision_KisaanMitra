"""
Market Card - Market price card
"""

from dataclasses import dataclass
from voice_agent.cards.base_card import BaseCard


@dataclass
class MarketCard(BaseCard):
    """Market price card"""
    
    def __init__(
        self,
        crop_name: str,
        price: float,
        trend: str,
        market_name: str,
        **kwargs
    ):
        trend_hindi = {
            "rising": "बढ़ रही है",
            "falling": "गिर रही है",
            "stable": "स्थिर है"
        }.get(trend, trend)
        
        super().__init__(
            card_type="market",
            title=f"{crop_name} - {market_name}",
            summary=f"₹{price}/kg - {trend_hindi}",
            details={
                "crop_name": crop_name,
                "price": price,
                "trend": trend,
                "trend_hindi": trend_hindi,
                "market_name": market_name,
            },
            **kwargs
        )
