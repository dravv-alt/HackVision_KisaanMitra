"""
Weather Card - Weather information card
"""

from dataclasses import dataclass
from Backend.Voice_agent.cards.base_card import BaseCard


@dataclass
class WeatherCard(BaseCard):
    """Weather information card"""
    
    def __init__(
        self,
        temperature: float,
        humidity: float,
        rain_forecast: bool,
        advisory: str,
        **kwargs
    ):
        super().__init__(
            card_type="weather",
            title="मौसम की जानकारी (Weather Information)",
            summary=f"{temperature}°C, {'बारिश संभावित' if rain_forecast else 'साफ मौसम'}",
            details={
                "temperature": temperature,
                "humidity": humidity,
                "rain_forecast": rain_forecast,
                "advisory": advisory,
            },
            **kwargs
        )
