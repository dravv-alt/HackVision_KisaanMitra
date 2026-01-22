"""
Market Engine - Simulates market price trends and demand
Provides realistic mock data for hackathon demo
"""

import random
from ..models import MarketContext, PriceTrend, DemandLevel


class MarketEngine:
    """
    Simulates market trends for various crops
    Uses predefined scenarios for common crops, randomizes others
    """
    
    # Predefined market scenarios for demo consistency
    CROP_SCENARIOS = {
        "onion": {
            "price": 40.0,
            "trend": PriceTrend.RISING,
            "demand": DemandLevel.HIGH
        },
        "tomato": {
            "price": 15.0,
            "trend": PriceTrend.FALLING,
            "demand": DemandLevel.LOW
        },
        "potato": {
            "price": 25.0,
            "trend": PriceTrend.STABLE,
            "demand": DemandLevel.MEDIUM
        },
        "wheat": {
            "price": 22.0,
            "trend": PriceTrend.RISING,
            "demand": DemandLevel.HIGH
        },
        "rice": {
            "price": 35.0,
            "trend": PriceTrend.STABLE,
            "demand": DemandLevel.HIGH
        },
        "cotton": {
            "price": 55.0,
            "trend": PriceTrend.FALLING,
            "demand": DemandLevel.MEDIUM
        },
        "sugarcane": {
            "price": 28.0,
            "trend": PriceTrend.STABLE,
            "demand": DemandLevel.MEDIUM
        }
    }
    
    def __init__(self, seed: int = 42):
        """
        Initialize market engine
        
        Args:
            seed: Random seed for reproducible randomization
        """
        random.seed(seed)
    
    def get_market_data(self, crop_name: str) -> MarketContext:
        """
        Get market data for specified crop
        
        Args:
            crop_name: Name of the crop (case-insensitive)
            
        Returns:
            MarketContext with price, trend, and demand info
        """
        crop_key = crop_name.lower().strip()
        
        # Check if we have predefined scenario
        if crop_key in self.CROP_SCENARIOS:
            scenario = self.CROP_SCENARIOS[crop_key]
            return MarketContext(
                crop_name=crop_name,
                current_price=scenario["price"],
                price_trend=scenario["trend"],
                demand_level=scenario["demand"]
            )
        
        # Generate random but realistic data for unknown crops
        return self._generate_random_market(crop_name)
    
    def _generate_random_market(self, crop_name: str) -> MarketContext:
        """
        Generate randomized market data for crops without predefined scenarios
        
        Args:
            crop_name: Name of the crop
            
        Returns:
            MarketContext with randomized values
        """
        # Use crop name hash for deterministic randomization
        seed_value = sum(ord(c) for c in crop_name)
        random.seed(seed_value)
        
        price = round(random.uniform(10.0, 60.0), 2)
        trend = random.choice(list(PriceTrend))
        demand = random.choice(list(DemandLevel))
        
        # Reset seed
        random.seed(42)
        
        return MarketContext(
            crop_name=crop_name,
            current_price=price,
            price_trend=trend,
            demand_level=demand
        )
    
    def get_price_forecast(self, crop_name: str, days_ahead: int = 7) -> str:
        """
        Generate simple price forecast narrative
        
        Args:
            crop_name: Name of the crop
            days_ahead: Number of days to forecast
            
        Returns:
            Human-readable forecast string
        """
        market = self.get_market_data(crop_name)
        
        if market.price_trend == PriceTrend.RISING:
            return f"Prices expected to increase by 5-10% in next {days_ahead} days"
        elif market.price_trend == PriceTrend.FALLING:
            return f"Prices may drop by 8-12% in next {days_ahead} days"
        else:
            return f"Prices expected to remain stable around ₹{market.current_price}/kg"
