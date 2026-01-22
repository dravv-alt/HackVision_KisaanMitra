"""
Weather Engine - fetches weather data with fallback
Uses OpenWeather API with safe fallback for reliability
"""
import os
from typing import Optional
from ..models import EnvironmentalContext
from ..constants import DEFAULT_WEATHER


class WeatherEngine:
    """Handles weather data fetching with API and fallback"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize weather engine
        
        Args:
            api_key: OpenWeather API key (optional)
        """
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.use_fallback = not self.api_key
    
    def get_context(self, lat: Optional[float], lon: Optional[float]) -> EnvironmentalContext:
        """
        Get weather context for location
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            EnvironmentalContext with weather data
        """
        # Try API if key is available
        if not self.use_fallback and lat and lon:
            try:
                return self._fetch_from_api(lat, lon)
            except Exception as e:
                print(f"⚠ Weather API failed: {e}. Using fallback.")
                return self._get_fallback_weather()
        else:
            return self._get_fallback_weather()
    
    def _fetch_from_api(self, lat: float, lon: float) -> EnvironmentalContext:
        """
        Fetch weather from OpenWeather API
        
        Note: Requires 'requests' package in production
        For hackathon: add basic implementation
        """
        try:
            import requests
            
            # Current weather API
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            # Forecast API for 7-day rain
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast"
            forecast_response = requests.get(forecast_url, params=params, timeout=5)
            forecast_data = forecast_response.json() if forecast_response.ok else None
            
            # Calculate rain forecast
            rain_mm_7d = 0
            rain_forecast = False
            if forecast_data and "list" in forecast_data:
                for item in forecast_data["list"][:21]:  # 7 days * 3-hour intervals
                    if "rain" in item:
                        rain_mm_7d += item["rain"].get("3h", 0)
                        rain_forecast = True
            
            # Build context
            return EnvironmentalContext(
                temperature_c=data["main"]["temp"],
                humidity_pct=data["main"]["humidity"],
                rain_forecast=rain_forecast,
                rain_mm_next_7_days=rain_mm_7d,
                wind_speed_mps=data["wind"]["speed"],
                alerts=self._parse_alerts(data)
            )
            
        except ImportError:
            # requests not installed
            print("⚠ 'requests' package not installed. Using fallback weather.")
            return self._get_fallback_weather()
        except Exception as e:
            raise Exception(f"API call failed: {e}")
    
    def _get_fallback_weather(self) -> EnvironmentalContext:
        """
        Return safe fallback weather data
        Uses realistic average values for demo
        """
        return EnvironmentalContext(**DEFAULT_WEATHER)
    
    def _parse_alerts(self, data: dict) -> list:
        """Parse weather alerts from API response"""
        alerts = []
        
        # Temperature extremes
        temp = data["main"]["temp"]
        if temp > 40:
            alerts.append("High temperature warning")
        elif temp < 5:
            alerts.append("Cold wave warning")
        
        # Wind
        if data["wind"]["speed"] > 15:
            alerts.append("Strong wind warning")
        
        # Rain
        if "rain" in data and data["rain"].get("1h", 0) > 50:
            alerts.append("Heavy rainfall expected")
        
        return alerts
