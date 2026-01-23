"""
Market Service - Live Mandi prices from OGD India API
"""

import requests
from typing import Dict, Any, List
from voice_agent.config import get_config
from voice_agent.retrieval.sources import get_knowledge_registry

class MarketService:
    """Service to fetch live market prices"""
    
    BASE_URL = "https://api.data.gov.in/resource"
    
    def __init__(self):
        self.config = get_config()
        self.api_key = self.config.mandi_api_key
        self.resource_id = self.config.mandi_resource_id
        
    def get_market_prices(self, commodity: str = None, state: str = "Maharashtra") -> List[Dict[str, Any]]:
        """
        Get market prices for commodities
        
        Args:
            commodity: Filter by commodity name (optional)
            state: Filter by state (optional, default Maharashtra)
            
        Returns:
            List of price records
        """
        if not self.api_key:
            print("⚠️  No Mandi API key found. Using fallback.")
            return self._get_fallback_prices(commodity)
            
        try:
            # Construct OGD API URL
            # limit=100 to get enough records to filter
            url = f"{self.BASE_URL}/{self.resource_id}"
            params = {
                "api-key": self.api_key,
                "format": "json",
                "limit": 100,
            }
            
            # Add filters if OGD supports them directly (usually filters[field]=value)
            if state:
                params["filters[state]"] = state
            if commodity:
                # OGD naming can be tricky (e.g. "Wheat" vs "Wheat(Husked)"), so exact match might fail
                # Better to fetch all and fuzzy filter in python, but let's try direct filter first
                params["filters[commodity]"] = commodity
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            records = data.get("records", [])
            
            if not records:
                # If direct filter failed, try fetching without commodity filter
                if commodity and "filters[commodity]" in params:
                    print(f"⚠️  No records for {commodity}, trying broader search...")
                    del params["filters[commodity]"]
                    response = requests.get(url, params=params, timeout=10)
                    data = response.json()
                    records = data.get("records", [])
            
            # Process records
            results = []
            for rec in records:
                # Basic fuzzy matching if we fetched broad data
                rec_comm = rec.get("commodity", "").lower()
                if commodity and commodity.lower() not in rec_comm:
                    continue
                    
                results.append({
                    "crop": rec.get("commodity"),
                    "market": rec.get("market"),
                    "district": rec.get("district"),
                    "price": rec.get("modal_price"),  # Usually the standard price
                    "date": rec.get("arrival_date"),
                    "source": "Govt Mandi API"
                })
            
            if not results:
                print("⚠️  No relevant market records found in API. Using fallback.")
                return self._get_fallback_prices(commodity)
                
            return results[:5]  # Return top 5
            
        except Exception as e:
            print(f"⚠️  Market API error: {e}. Using fallback.")
            return self._get_fallback_prices(commodity)

    def _get_fallback_prices(self, commodity_filter: str = None) -> List[Dict[str, Any]]:
        """Return static mock data as failsafe"""
        registry = get_knowledge_registry()
        source = registry.get_source("market")
        if not source:
            return []
            
        results = []
        for crop, data in source.data.items():
            if commodity_filter and commodity_filter.lower() not in crop.lower():
                continue
                
            results.append({
                "crop": crop.capitalize(),
                "market": "Local Mandi (Mock)",
                "district": "Pune",
                "price": data["price"],
                "trend": data["trend"],
                "source": "Mock Data (Fallback)"
            })
            
        return results

# Singleton
_market_service = None

def get_market_service() -> MarketService:
    global _market_service
    if _market_service is None:
        _market_service = MarketService()
    return _market_service
