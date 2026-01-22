"""
Market Price Repository with Mock Fallback
"""

from datetime import datetime
from typing import Optional, Dict

from ..models import MarketPriceContext


class MarketRepo:
    """Repository for market price data with mock fallback"""
    
    def __init__(self):
        # Mock in-memory storage (simulates price cache)
        self._mock_prices: Dict[str, MarketPriceContext] = {}
        self.seed_mock_prices_if_empty()
    
    def get_latest_price(self, crop_key: str, mandi: Optional[str] = None) -> MarketPriceContext:
        """
        Get latest market price for a crop
        Falls back to mock data if not found
        """
        cache_key = f"{crop_key}_{mandi}" if mandi else crop_key
        
        if cache_key in self._mock_prices:
            return self._mock_prices[cache_key]
        
        # Return default mock price if not found
        return MarketPriceContext(
            cropKey=crop_key,
            mandi=mandi,
            currentPrice=25.0,
            trend="stable",
            lastUpdatedAt=datetime.now()
        )
    
    def seed_mock_prices_if_empty(self):
        """Seed mock market price data"""
        now = datetime.now()
        
        mock_prices = {
            "tomato": MarketPriceContext(
                cropKey="tomato",
                currentPrice=18.0,
                trend="falling",  # Falling price - should sell quickly
                lastUpdatedAt=now
            ),
            "onion": MarketPriceContext(
                cropKey="onion",
                currentPrice=35.0,
                trend="rising",  # Rising price - can wait if storage good
                lastUpdatedAt=now
            ),
            "potato": MarketPriceContext(
                cropKey="potato",
                currentPrice=22.0,
                trend="stable",
                lastUpdatedAt=now
            ),
            "wheat": MarketPriceContext(
                cropKey="wheat",
                currentPrice=2500.0,  # per quintal
                trend="rising",
                lastUpdatedAt=now
            ),
            "rice": MarketPriceContext(
                cropKey="rice",
                currentPrice=3000.0,  # per quintal
                trend="stable",
                lastUpdatedAt=now
            ),
            "groundnut": MarketPriceContext(
                cropKey="groundnut",
                currentPrice=55.0,
                trend="stable",
                lastUpdatedAt=now
            ),
            "cotton": MarketPriceContext(
                cropKey="cotton",
                currentPrice=6500.0,  # per quintal
                trend="rising",
                lastUpdatedAt=now
            ),
        }
        
        self._mock_prices.update(mock_prices)
