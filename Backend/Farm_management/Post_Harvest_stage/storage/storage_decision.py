"""
Storage Decision Maker
Core logic for sell-now vs store-and-sell decision
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from farm_management.post_harvest_stage.storage.spoilage_model import SpoilageRisk, SpoilageAssessment
from farm_management.post_harvest_stage.storage.storage_options import StorageOption


class StorageDecision(str, Enum):
    """Storage decision types"""
    SELL_NOW = "sell_now"
    STORE_AND_SELL = "store_and_sell"


@dataclass
class StorageDecisionResult:
    """Result of storage decision analysis"""
    decision: StorageDecision
    recommended_wait_days: int
    spoilage_assessment: SpoilageAssessment
    storage_facility: Optional[StorageOption]
    profit_improvement_percent: float
    reasoning: str


@dataclass
class PriceForecastData:
    """Price forecast information"""
    current_price: float
    peak_price: float
    peak_day: int  # Days from now
    trend: str  # "rising", "falling", "stable"


class StorageDecisionMaker:
    """Makes sell vs store decisions"""
    
    def decide(
        self,
        quantity_kg: float,
        current_price: float,
        price_forecast: PriceForecastData,
        spoilage_assessment: SpoilageAssessment,
        storage_option: Optional[StorageOption],
        transport_cost: float = 0
    ) -> StorageDecisionResult:
        """
        Make storage decision based on all factors
        
        Args:
            quantity_kg: Quantity of crop
            current_price: Today's market price per kg
            price_forecast: Future price predictions
            spoilage_assessment: Spoilage risk analysis
            storage_option: Available storage facility (if any)
            transport_cost: Transport cost to market
            
        Returns:
            StorageDecisionResult with recommendation
        """
        # Calculate profit if selling today
        profit_today = (current_price * quantity_kg) - transport_cost
        
        # If peak day is beyond safe storage period, cap it
        safe_wait_days = min(
            price_forecast.peak_day,
            spoilage_assessment.max_safe_storage_days
        )
        
        # If no storage available, must sell now
        if storage_option is None:
            return StorageDecisionResult(
                decision=StorageDecision.SELL_NOW,
                recommended_wait_days=0,
                spoilage_assessment=spoilage_assessment,
                storage_facility=None,
                profit_improvement_percent=0.0,
                reasoning="No storage facility available within acceptable distance"
            )
        
        # If spoilage risk is HIGH, sell now
        if spoilage_assessment.risk_level == SpoilageRisk.HIGH:
            return StorageDecisionResult(
                decision=StorageDecision.SELL_NOW,
                recommended_wait_days=0,
                spoilage_assessment=spoilage_assessment,
                storage_facility=None,
                profit_improvement_percent=0.0,
                reasoning=f"Spoilage risk is too high - crop will deteriorate before price improvement"
            )
        
        # Calculate profit if storing until peak
        price_at_peak = price_forecast.peak_price
        storage_cost = storage_option.total_cost_for_period if storage_option else 0
        profit_at_peak = (price_at_peak * quantity_kg) - transport_cost - storage_cost
        
        # Calculate profit improvement
        profit_improvement = profit_at_peak - profit_today
        profit_improvement_pct = (profit_improvement / profit_today * 100) if profit_today > 0 else 0
        
        # Decision logic: Store only if profit improvement > 10%
        if profit_improvement_pct >= 10.0 and safe_wait_days > 0:
            return StorageDecisionResult(
                decision=StorageDecision.STORE_AND_SELL,
                recommended_wait_days=safe_wait_days,
                spoilage_assessment=spoilage_assessment,
                storage_facility=storage_option,
                profit_improvement_percent=round(profit_improvement_pct, 1),
                reasoning=f"Storing for {safe_wait_days} days will increase profit by {profit_improvement_pct:.1f}%"
            )
        else:
            # Not worth storing
            reason = "stable" if price_forecast.trend == "stable" else "minimal"
            return StorageDecisionResult(
                decision=StorageDecision.SELL_NOW,
                recommended_wait_days=0,
                spoilage_assessment=spoilage_assessment,
                storage_facility=None,
                profit_improvement_percent=round(profit_improvement_pct, 1),
                reasoning=f"Price improvement is {reason} - storage cost not justified (only {profit_improvement_pct:.1f}% gain)"
            )
