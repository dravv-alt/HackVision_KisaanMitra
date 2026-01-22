"""
Profit Calculator
Computes net profit considering all costs
"""

from dataclasses import dataclass


@dataclass
class NetProfit:
    """Detailed profit breakdown"""
    gross_revenue: float
    transport_cost: float
    storage_cost: float
    total_costs: float
    net_profit: float
    profit_margin_percent: float


class ProfitCalculator:
    """Calculates net profit from crop sale"""
    
    def calculate_net_profit(
        self,
        selling_price_per_kg: float,
        quantity_kg: float,
        transport_cost: float,
        storage_cost: float = 0.0
    ) -> NetProfit:
        """
        Calculate net profit after all costs
        
        Args:
            selling_price_per_kg: Market price per kg
            quantity_kg: Quantity being sold
            transport_cost: Cost of transport to market
            storage_cost: Cost of storage (if stored)
            
        Returns:
            NetProfit object with breakdown
        """
        gross_revenue = selling_price_per_kg * quantity_kg
        total_costs = transport_cost + storage_cost
        net_profit = gross_revenue - total_costs
        
        profit_margin = (net_profit / gross_revenue * 100) if gross_revenue > 0 else 0
        
        return NetProfit(
            gross_revenue=round(gross_revenue, 2),
            transport_cost=round(transport_cost, 2),
            storage_cost=round(storage_cost, 2),
            total_costs=round(total_costs, 2),
            net_profit=round(net_profit, 2),
            profit_margin_percent=round(profit_margin, 1)
        )
