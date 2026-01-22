"""
Post-Harvest Decision Engine
Orchestrates all decision logic
"""

from dataclasses import dataclass
from typing import List
from core.context import FarmerContext
from storage import (
    SpoilageRiskCalculator,
    StorageMatcher,
    StorageDecisionMaker,
    PriceForecastData,
    SpoilageAssessment,
    StorageDecision
)
from market import (
    PriceTrendForecaster,
    MarketSelector,
    MarketOption
)
from data_access import StorageType, get_crop_metadata


@dataclass
class DecisionResult:
    """Complete decision output - structured data only"""
    
    # Storage Decision
    storage_decision: str  # "sell_now" or "store_and_sell"
    recommended_wait_days: int
    spoilage_risk: str  # "low", "medium", "high"
    max_safe_storage_days: int
    storage_type_recommended: str
    
    # Market Selection
    best_market_name: str
    best_market_location: tuple
    market_price: float
    transport_cost: float
    storage_cost: float
    net_profit: float
    profit_margin_percent: float
    
    # Alternative markets (top 3)
    alternative_markets: List[dict]
    
    # Price forecast data
    current_price: float
    peak_price: float
    peak_day: int
    price_trend: str  # "rising", "falling", "stable"
    
    # Decision reasoning
    storage_reasoning: str
    profit_improvement_percent: float


class PostHarvestDecisionEngine:
    """
    Main decision engine - orchestrates all modules
    Single entry point: run_decision(context)
    """
    
    def __init__(self):
        self.spoilage_calculator = SpoilageRiskCalculator()
        self.storage_matcher = StorageMatcher()
        self.storage_decision_maker = StorageDecisionMaker()
        self.price_forecaster = PriceTrendForecaster()
        self.market_selector = MarketSelector()
    
    def run_decision(self, context: FarmerContext) -> DecisionResult:
        """
        Run complete decision flow
        
        Args:
            context: FarmerContext with farmer input
            
        Returns:
            DecisionResult with all recommendations
        """
        # 1. Load crop metadata
        crop_meta = get_crop_metadata(context.crop_name)
        if not crop_meta:
            raise ValueError(f"Crop '{context.crop_name}' not supported")
        
        # 2. Forecast prices for best market (initially without storage cost)
        # First, select best market at current prices to know where to sell
        market_recommendation = self.market_selector.select_best_market(
            farmer_location=context.farmer_location,
            crop_name=context.crop_name,
            quantity_kg=context.quantity_kg,
            storage_cost=0  # Initial assessment without storage
        )
        
        best_market = market_recommendation.best_market
        
        # Get price forecast for the best market
        price_forecast = self.price_forecaster.forecast_prices(
            crop_name=context.crop_name,
            mandi_name=best_market.mandi_name,
            days_ahead=14
        )
        
        # 3. Determine optimal storage type based on crop
        # High spoilage crops need cold storage
        if crop_meta.spoilage_sensitivity.value == "high":
            storage_type = StorageType.COLD
        else:
            storage_type = StorageType.OPEN
        
        # 4. Calculate spoilage risk for waiting until peak price
        spoilage_assessment = self.spoilage_calculator.calculate_risk(
            crop_name=context.crop_name,
            days_to_sell=price_forecast.peak_day,
            storage_type=storage_type
        )
        
        # 5. Find available storage
        storage_option = self.storage_matcher.get_best_storage(
            farmer_location=context.farmer_location,
            crop_name=context.crop_name,
            quantity_kg=context.quantity_kg,
            storage_type=storage_type,
            days_needed=price_forecast.peak_day
        )
        
        # 6. Make storage decision
        price_forecast_data = PriceForecastData(
            current_price=price_forecast.current_price,
            peak_price=price_forecast.peak_price,
            peak_day=price_forecast.peak_day,
            trend=price_forecast.trend
        )
        
        storage_decision = self.storage_decision_maker.decide(
            quantity_kg=context.quantity_kg,
            current_price=price_forecast.current_price,
            price_forecast=price_forecast_data,
            spoilage_assessment=spoilage_assessment,
            storage_option=storage_option,
            transport_cost=best_market.transport_cost
        )
        
        # 7. Re-select market with storage cost if storing
        storage_cost = 0.0
        if storage_decision.decision == StorageDecision.STORE_AND_SELL:
            storage_cost = storage_option.total_cost_for_period if storage_option else 0
            
            # Re-evaluate market selection with storage cost
            market_recommendation = self.market_selector.select_best_market(
                farmer_location=context.farmer_location,
                crop_name=context.crop_name,
                quantity_kg=context.quantity_kg,
                storage_cost=storage_cost
            )
            best_market = market_recommendation.best_market
        
        # 8. Build decision result
        alternatives = [
            {
                "market_name": alt.mandi_name,
                "distance_km": alt.distance_km,
                "price": alt.market_price,
                "transport_cost": alt.transport_cost,
                "net_profit": alt.net_profit_details.net_profit
            }
            for alt in market_recommendation.alternative_markets
        ]
        
        return DecisionResult(
            # Storage decision
            storage_decision=storage_decision.decision.value,
            recommended_wait_days=storage_decision.recommended_wait_days,
            spoilage_risk=spoilage_assessment.risk_level.value,
            max_safe_storage_days=spoilage_assessment.max_safe_storage_days,
            storage_type_recommended=storage_type.value,
            
            # Market selection
            best_market_name=best_market.mandi_name,
            best_market_location=best_market.mandi_location,
            market_price=best_market.market_price,
            transport_cost=best_market.transport_cost,
            storage_cost=storage_cost,
            net_profit=best_market.net_profit_details.net_profit,
            profit_margin_percent=best_market.net_profit_details.profit_margin_percent,
            
            # Alternatives
            alternative_markets=alternatives,
            
            # Price forecast
            current_price=price_forecast.current_price,
            peak_price=price_forecast.peak_price,
            peak_day=price_forecast.peak_day,
            price_trend=price_forecast.trend,
            
            # Reasoning
            storage_reasoning=storage_decision.reasoning,
            profit_improvement_percent=storage_decision.profit_improvement_percent
        )
