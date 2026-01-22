"""
Synthesizer - Combines retrieved information into structured reasoning
"""

from typing import List, Dict, Any
from voice_agent.core.intent import Intent
from voice_agent.cards import CropCard, WeatherCard, MarketCard, SchemeCard


class Synthesizer:
    """Synthesizes retrieved information into cards and recommendations"""
    
    def synthesize(
        self,
        intent: Intent,
        retrieved_docs: List[Dict[str, Any]],
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Synthesize retrieved information
        
        Args:
            intent: Detected intent
            retrieved_docs: Retrieved documents
            context: Additional context
        
        Returns:
            Synthesis result with cards and reasoning
        """
        if intent == Intent.CROP_PLANNING:
            return self._synthesize_crop_planning(retrieved_docs, context)
        elif intent == Intent.GOVERNMENT_SCHEME:
            return self._synthesize_schemes(retrieved_docs, context)
        elif intent == Intent.WEATHER_QUERY:
            return self._synthesize_weather(retrieved_docs)
        elif intent == Intent.MARKET_PRICE:
            return self._synthesize_market(retrieved_docs)
        else:
            return {"cards": [], "reasoning": "Information retrieved"}
    
    def _synthesize_crop_planning(
        self,
        docs: List[Dict[str, Any]],
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Synthesize crop planning information"""
        cards = []
        
        # Create crop cards
        for doc in docs:
            if doc.get("type") == "crop_info":
                crop_data = doc["data"]
                card = CropCard(
                    crop_name=crop_data["name"],
                    crop_name_hindi=crop_data["name_hindi"],
                    score=75.0,  # Mock score
                    reasons=["Suitable soil", "Good season"],
                    risks=["Market volatility"],
                    profit_level=crop_data.get("profit_potential", "medium"),
                    source="knowledge_base"
                )
                cards.append(card)
        
        # Add weather card
        weather_docs = [d for d in docs if d.get("type") == "weather_info"]
        if weather_docs:
            weather_data = weather_docs[0]["data"]
            cards.append(WeatherCard(
                temperature=weather_data["temperature"],
                humidity=weather_data["humidity"],
                rain_forecast=weather_data["rain_forecast"],
                advisory=weather_data["advisory"],
                source="weather_service"
            ))
        
        reasoning = "Based on soil type, season, and market conditions, these crops are recommended."
        
        return {"cards": cards, "reasoning": reasoning}
    
    def _synthesize_schemes(
        self,
        docs: List[Dict[str, Any]],
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Synthesize government scheme information"""
        cards = []
        
        for doc in docs:
            if doc.get("type") == "scheme_info":
                scheme_data = doc["data"]
                card = SchemeCard(
                    scheme_name=scheme_data["name"],
                    scheme_name_hindi=scheme_data["name_hindi"],
                    eligible=True,  # Mock eligibility
                    reasons=["Meets criteria"],
                    source="government_database"
                )
                cards.append(card)
        
        reasoning = "You are eligible for these government schemes."
        
        return {"cards": cards, "reasoning": reasoning}
    
    def _synthesize_weather(self, docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize weather information"""
        cards = []
        
        for doc in docs:
            if doc.get("type") == "weather_info":
                weather_data = doc["data"]
                cards.append(WeatherCard(
                    temperature=weather_data["temperature"],
                    humidity=weather_data["humidity"],
                    rain_forecast=weather_data["rain_forecast"],
                    advisory=weather_data["advisory"],
                    source="weather_service"
                ))
        
        return {"cards": cards, "reasoning": "Current weather conditions"}
    
    def _synthesize_market(self, docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize market information"""
        cards = []
        
        for doc in docs:
            if doc.get("type") == "market_price":
                cards.append(MarketCard(
                    crop_name=doc["crop"],
                    price=doc["data"]["price"],
                    trend=doc["data"]["trend"],
                    market_name="Local Mandi",
                    source="market_data"
                ))
        
        return {"cards": cards, "reasoning": "Current market prices"}


# Singleton instance
_synthesizer = None

def get_synthesizer() -> Synthesizer:
    """Get or create synthesizer"""
    global _synthesizer
    if _synthesizer is None:
        _synthesizer = Synthesizer()
    return _synthesizer
