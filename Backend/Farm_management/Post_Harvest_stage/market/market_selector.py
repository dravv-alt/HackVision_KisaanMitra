"""
Market Selector
Selects best market based on net profit
"""

from dataclasses import dataclass
from typing import List
from .transport import TransportCostEstimator
from .profit_calculator import ProfitCalculator, NetProfit
from .price_model import PriceTrendForecaster
from Backend.Farm_management.Post_Harvest_stage.data_access import get_all_mandis, get_mandi_price


@dataclass
class MarketOption:
    """A market option with profit analysis"""
    mandi_name: str
    mandi_location: tuple
    distance_km: float
    market_price: float
    transport_cost: float
    net_profit_details: NetProfit
    
    def __lt__(self, other):
        """For sorting by net profit"""
        return self.net_profit_details.net_profit < other.net_profit_details.net_profit


@dataclass
class MarketRecommendation:
    """Best market recommendation with alternatives"""
    best_market: MarketOption
    alternative_markets: List[MarketOption]  # Top 3 alternatives


class MarketSelector:
    """Selects best market for selling crop"""
    
    def __init__(self):
        self.transport_estimator = TransportCostEstimator()
        self.profit_calculator = ProfitCalculator()
    
    def select_best_market(
        self,
        farmer_location: tuple,
        crop_name: str,
        quantity_kg: float,
        storage_cost: float = 0.0
    ) -> MarketRecommendation:
        """
        Select market with highest net profit
        
        Args:
            farmer_location: (lat, lon) of farmer
            crop_name: Name of crop
            quantity_kg: Quantity to sell
            storage_cost: Storage cost if crop was stored
            
        Returns:
            MarketRecommendation with best market and alternatives
        """
        from Backend.Farm_management.Post_Harvest_stage.utils import haversine_distance
        
        # Get all mandis
        all_mandis = get_all_mandis()
        
        market_options = []
        
        for mandi in all_mandis:
            # Get current price at this mandi
            price_data = get_mandi_price(mandi.name, crop_name)
            market_price = price_data.current_price
            
            # Calculate distance
            distance = haversine_distance(
                farmer_location[0], farmer_location[1],
                mandi.location[0], mandi.location[1]
            )
            
            # Calculate transport cost
            transport_cost = self.transport_estimator.estimate_cost(
                farmer_location,
                mandi.location,
                quantity_kg
            )
            
            # Calculate net profit
            profit = self.profit_calculator.calculate_net_profit(
                selling_price_per_kg=market_price,
                quantity_kg=quantity_kg,
                transport_cost=transport_cost,
                storage_cost=storage_cost
            )
            
            market_options.append(MarketOption(
                mandi_name=mandi.name,
                mandi_location=mandi.location,
                distance_km=distance,
                market_price=market_price,
                transport_cost=transport_cost,
                net_profit_details=profit
            ))
        
        # Sort by net profit (highest first)
        market_options.sort(reverse=True)
        
        # Select best and alternatives
        best = market_options[0]
        alternatives = market_options[1:4] if len(market_options) > 1 else []
        
        return MarketRecommendation(
            best_market=best,
            alternative_markets=alternatives
        )
