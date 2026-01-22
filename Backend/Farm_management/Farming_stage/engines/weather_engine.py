"""
Weather Engine - Fetches environmental data with fallback to mock data
Supports OpenWeatherMap API with graceful degradation
"""

import os
import requests
from typing import Optional
from ..models import EnvironmentalContext


class WeatherEngine:
    """
    Fetches weather data from OpenWeatherMap API
    Falls back to realistic mock data if API unavailable
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize weather engine
        
        Args:
            api_key: OpenWeatherMap API key (optional, reads from env if not provided)
        """
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.timeout = 5  # seconds
    
    def get_context(self, lat: float, lon: float) -> EnvironmentalContext:
        """
        Fetch weather data for given coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            EnvironmentalContext with current weather data
        """
        # Try real API first if key available
        if self.api_key:
            try:
                return self._fetch_real_weather(lat, lon)
            except Exception as e:
                print(f"⚠️  Weather API failed: {e}. Using mock data.")
        
        # Fallback to mock data
        return self._get_mock_weather(lat, lon)
    
    def _fetch_real_weather(self, lat: float, lon: float) -> EnvironmentalContext:
        """
        Fetch from OpenWeatherMap API
        
        Raises:
            Exception if API call fails
        """
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"  # Celsius
        }
        
        response = requests.get(self.base_url, params=params, timeout=self.timeout)
        response.raise_for_status()
        
        data = response.json()
        
        # Parse response
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"] * 3.6  # Convert m/s to km/h
        
        # Check for rain in forecast (simplified: check current conditions)
        rain_forecast = "rain" in data.get("weather", [{}])[0].get("main", "").lower()
        
        return EnvironmentalContext(
            temperature=temperature,
            rain_forecast=rain_forecast,
            humidity=humidity,
            wind_speed=wind_speed
        )
    
    def _get_mock_weather(self, lat: float, lon: float) -> EnvironmentalContext:
        """
        Generate realistic mock weather data for demo
        
        Args:
            lat: Latitude (used for slight variation)
            lon: Longitude (used for slight variation)
            
        Returns:
            Mock EnvironmentalContext
        """
        # Use coordinates to add slight variation (deterministic)
        temp_variation = (lat % 10) - 5  # ±5°C variation
        humidity_variation = (lon % 20) - 10  # ±10% variation
        
        return EnvironmentalContext(
            temperature=30.0 + temp_variation,
            rain_forecast=False,  # Default: no rain for stable demo
            humidity=60.0 + humidity_variation,
            wind_speed=12.0
        )
