"""
Market Price Repository with Mock Fallback
"""

from typing import Optional
from ..models import MarketContext
from ..constants import PriceTrend


class MarketRepo:
    def __init__(self):
        self._mock_prices = {}
        self.seed_mock_prices_if_empty()

    def get_latest_price(self, crop_key: str, mandi: str) -> Optional[MarketContext]:
        """Fetch latest mandi price for a crop"""
        key = f"{crop_key}:{mandi}"
        if key in self._mock_prices:
            return self._mock_prices[key]
        
        # Consistent fallback
        return MarketContext(
            cropKey=crop_key,
            mandi=mandi,
            currentPrice=2400.0,
            prevPrice=2000.0,
            changePct=20.0,
            trend=PriceTrend.RISING
        )

    def seed_mock_prices_if_empty(self):
        self._mock_prices["tomato:Nashik"] = MarketContext(
            cropKey="tomato",
            mandi="Nashik",
            currentPrice=1200.0,
            prevPrice=1600.0,
            changePct=-25.0,
            trend=PriceTrend.FALLING
        )
