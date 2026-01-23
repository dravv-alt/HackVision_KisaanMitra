"""
Weather Service - Live weather data from OpenWeatherMap
"""

import requests
from typing import Dict, Any, Optional
from voice_agent.config import get_config
from voice_agent.retrieval.sources import get_knowledge_registry

class WeatherService:
    """Service to fetch live weather data"""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self):
        self.config = get_config()
        self.api_key = self.config.openweather_api_key
        
    def get_current_weather(self, location: str = "Pune,IN") -> Dict[str, Any]:
        """
        Get current weather for a location
        
        Args:
            location: City name or "lat,lon"
            
        Returns:
            Weather data dictionary
        """
        if not self.api_key:
            print("⚠️  No OpenWeather API key found. Using fallback.")
            return self._get_fallback_weather()
            
        try:
            url = f"{self.BASE_URL}/weather"
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Transform to our internal format
            return {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "rain_forecast": "Rain" in data["weather"][0]["main"],
                "advisory": self._generate_advisory(data),
                "source": "OpenWeatherMap"
            }
            
        except Exception as e:
            print(f"⚠️  Weather API error: {e}. Using fallback.")
            return self._get_fallback_weather()

    def _generate_advisory(self, data: Dict[str, Any]) -> str:
        """Generate simple advisory based on weather"""
        condition = data["weather"][0]["main"].lower()
        temp = data["main"]["temp"]
        
        if "rain" in condition or "drizzle" in condition:
            return "Rain expected. Delay spraying pesticides/fertilizers."
        elif temp > 35:
            return "High temperature. Ensure irrigation for sensitive crops."
        elif temp < 10:
            return "Low temperature. Protect crops from frost."
        else:
            return "Good weather conditions for farming activities."
            
    def _get_fallback_weather(self) -> Dict[str, Any]:
        """Return static mock data as failsafe"""
        registry = get_knowledge_registry()
        source = registry.get_source("weather")
        if source:
            data = source.data["current"]
            # Normalize format to match API return
            return {
                "temperature": data.get("temperature", 28.0),
                "humidity": data.get("humidity", 65.0),
                "condition": "Clear",
                "description": "Clear sky (Mock)",
                "wind_speed": 5.0,
                "rain_forecast": data.get("rain_forecast", False),
                "advisory": data.get("advisory", "Good weather (Mock)"),
                "source": "Mock Data (Fallback)"
            }
        return {}

# Singleton
_weather_service = None

def get_weather_service() -> WeatherService:
    global _weather_service
    if _weather_service is None:
        _weather_service = WeatherService()
    return _weather_service
