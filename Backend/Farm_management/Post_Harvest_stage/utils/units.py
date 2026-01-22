"""
Unit conversion utilities
"""


def kg_to_quintal(kg: float) -> float:
    """Convert kilograms to quintals (1 quintal = 100 kg)"""
    return kg / 100.0


def quintal_to_kg(quintals: float) -> float:
    """Convert quintals to kilograms"""
    return quintals * 100.0


def format_currency(amount: float) -> str:
    """Format currency for Indian Rupees"""
    return f"₹{amount:,.2f}"


def format_weight(kg: float) -> str:
    """Format weight with appropriate unit"""
    if kg >= 1000:
        return f"{kg/1000:.2f} MT"  # Metric tons
    elif kg >= 100:
        return f"{kg/100:.1f} quintals"
    else:
        return f"{kg:.1f} kg"
