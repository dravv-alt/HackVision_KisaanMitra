"""
Price Trend Forecaster
Simple deterministic price forecasting without heavy ML
"""

from dataclasses import dataclass
from typing import Dict, List
from datetime import date, timedelta
from Backend.Farm_management.Post_Harvest_stage.data_access import get_mandi_price, PricePoint


@dataclass
class PriceForecast:
    """Price forecast for a crop at a mandi"""
    crop_name: str
    mandi_name: str
    current_price: float
    forecasted_prices: Dict[int, float]  # day -> price
    peak_day: int  # Day with highest price (0 = today)
    peak_price: float
    trend: str  # "rising", "falling", "stable"
    confidence: str = "medium"


class PriceTrendForecaster:
    """Forecasts future prices using simple heuristics"""
    
    def forecast_prices(
        self,
        crop_name: str,
        mandi_name: str,
        days_ahead: int = 14
    ) -> PriceForecast:
        """
        Forecast future prices using trend analysis
        
        Args:
            crop_name: Name of the crop
            mandi_name: Name of the mandi
            days_ahead: Number of days to forecast
            
        Returns:
            PriceForecast object
        """
        # Get historical prices
        price_data = get_mandi_price(mandi_name, crop_name)
        current_price = price_data.current_price
        history = price_data.price_history
        
        # Calculate simple trend (linear regression-like)
        trend_slope = self._calculate_trend_slope(history)
        
        # Determine trend direction
        if trend_slope > 0.5:  # Rising more than ₹0.50/day
            trend = "rising"
        elif trend_slope < -0.5:  # Falling more than ₹0.50/day
            trend = "falling"
        else:
            trend = "stable"
        
        # Generate forecast
        forecasted_prices = {}
        for day in range(days_ahead + 1):
            # Base forecast from trend
            base_forecast = current_price + (trend_slope * day)
            
            # Add seasonal variation (±5%)
            seasonal_factor = 1.0 + (0.05 * ((day % 7) - 3) / 3)
            
            # Add dampening for long-term (uncertainty increases)
            dampening = 1.0 - (day / days_ahead * 0.1)  # Reduce extreme projections
            
            price = base_forecast * seasonal_factor * dampening
            forecasted_prices[day] = max(round(price, 2), current_price * 0.8)  # Floor at 80% of current
        
        # Find peak price
        peak_day = max(forecasted_prices, key=forecasted_prices.get)
        peak_price = forecasted_prices[peak_day]
        
        return PriceForecast(
            crop_name=crop_name,
            mandi_name=mandi_name,
            current_price=current_price,
            forecasted_prices=forecasted_prices,
            peak_day=peak_day,
            peak_price=peak_price,
            trend=trend
        )
    
    def _calculate_trend_slope(self, history: List[PricePoint]) -> float:
        """
        Calculate trend slope from price history
        Simple linear regression
        
        Returns:
            Slope (change in price per day)
        """
        if len(history) < 2:
            return 0.0
        
        # Use last 7 days for trend
        recent_history = history[-7:] if len(history) > 7 else history
        
        n = len(recent_history)
        sum_x = sum(range(n))
        sum_y = sum(p.price_per_kg for p in recent_history)
        sum_xy = sum(i * p.price_per_kg for i, p in enumerate(recent_history))
        sum_x2 = sum(i ** 2 for i in range(n))
        
        # Linear regression slope formula
        if n * sum_x2 - sum_x ** 2 == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        return round(slope, 2)
