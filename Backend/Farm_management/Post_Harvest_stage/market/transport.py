"""
Transport Cost Estimator
Calculates transport costs based on distance and quantity
"""

from ..utils import haversine_distance, kg_to_quintal


class TransportCostEstimator:
    """Estimates transport costs to markets"""
    
    def __init__(self, base_rate_per_km_per_quintal: float = 4.0):
        """
        Initialize estimator
        
        Args:
            base_rate_per_km_per_quintal: ₹ per km per quintal (default: ₹4)
        """
        self.base_rate = base_rate_per_km_per_quintal
    
    def estimate_cost(
        self,
        from_location: tuple,
        to_location: tuple,
        quantity_kg: float
    ) -> float:
        """
        Estimate transport cost
        
        Args:
            from_location: (lat, lon) of origin
            to_location: (lat, lon) of destination
            quantity_kg: Quantity to transport in kg
            
        Returns:
            Estimated cost in ₹
        """
        # Calculate distance
        distance = haversine_distance(
            from_location[0], from_location[1],
            to_location[0], to_location[1]
        )
        
        # Convert to quintals
        quintals = kg_to_quintal(quantity_kg)
        
        # Base cost
        base_cost = distance * quintals * self.base_rate
        
        # Add fixed loading/unloading charge (₹500)
        loading_charge = 500
        
        # Road quality adjustment (simplified: +20% for long distance)
        road_adjustment = 1.2 if distance > 100 else 1.0
        
        total_cost = (base_cost * road_adjustment) + loading_charge
        
        return round(total_cost, 2)
    
    def estimate_cost_per_kg(
        self,
        from_location: tuple,
        to_location: tuple,
        quantity_kg: float
    ) -> float:
        """
        Calculate cost per kg
        
        Returns:
            Cost per kg in ₹
        """
        total = self.estimate_cost(from_location, to_location, quantity_kg)
        return round(total / quantity_kg, 2) if quantity_kg > 0 else 0.0
