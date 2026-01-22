"""
Synthesizer - Combines retrieved information into structured reasoning
"""

from typing import List, Dict, Any, Optional
from voice_agent.core.intent import Intent
from voice_agent.cards import CropCard, WeatherCard, MarketCard, SchemeCard
from voice_agent.config import get_config

# Import logic from Farm Management
from farm_management.planning_stage.service import PreSeedingService
from farm_management.planning_stage.models import PlanningRequest, PreSeedingOutput
from farm_management.planning_stage.repositories import FarmerRepository, CropRepository, SchemeRepository, ReminderRepository


class Synthesizer:
    """Synthesizes retrieved information into cards and recommendations using Real Logic"""
    
    def __init__(self):
        self.config = get_config()
        self.weather_api_key = self.config.openweather_api_key
        
        # Initialize Farm Management Service
        # We allow repositories to mock themselves (default behavior)
        self.planning_service = PreSeedingService(
            weather_api_key=self.weather_api_key
        )
    
    def synthesize(
        self,
        intent: Intent,
        retrieved_docs: List[Dict[str, Any]],
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Synthesize retrieved information
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
        """Synthesize crop planning using PreSeedingService logic"""
        cards = []
        context = context or {}
        farmer_id = context.get("farmer_id", "F001")
        
        try:
            # 1. Call Logic Layer
            request = PlanningRequest(farmer_id=farmer_id)
            output: PreSeedingOutput = self.planning_service.run(request)
            
            # 2. Map Results to UI Cards
            # Crops
            for rec in output.crop_cards:
                card = CropCard(
                    crop_name=rec.crop_name,
                    crop_name_hindi=rec.crop_name_hi or rec.crop_name,
                    score=rec.score,
                    reasons=rec.reasons,
                    risks=rec.risks,
                    profit_level=rec.profit_level.value,
                    source="FarmLogicEngine"
                )
                cards.append(card)
                
            # Schemes (from planning output)
            for scheme in output.scheme_cards:
                if scheme.eligible:
                    card = SchemeCard(
                        scheme_name=scheme.scheme_name,
                        scheme_name_hindi=scheme.scheme_name_hi or scheme.scheme_name,
                        eligible=scheme.eligible,
                        reasons=scheme.why_eligible,
                        source="FarmLogicEngine"
                    )
                    cards.append(card)
            
            # Weather (from planning output summary)
            # Accessing context from service is hard as it returns output struct
            # We'll trust the summary string or check retrieved_docs fallback
            cards.append(WeatherCard(
                temperature=0.0, # Placeholder, logic engine used it but didn't expose raw values easily in summary
                humidity=0.0,
                rain_forecast=False,
                advisory=output.weather_summary,
                source="FarmLogicEngine"
            ))
            
            reasoning = output.detailed_reasoning or output.speech_text
            return {"cards": cards, "reasoning": reasoning}
            
        except Exception as e:
            print(f"⚠️  Logic Engine Error: {e}. Falling back to RAG synthesis.")
            return self._fallback_crop_synthesis(docs)

    def _fallback_crop_synthesis(self, docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Legacy fallback if logic engine fails"""
        cards = []
        for doc in docs:
            if doc.get("type") == "crop_info":
                data = doc["data"]
                # Handle varying data structures from RAG vs Mock
                name = data.get("name") or data.get("crop_name")
                name_hi = data.get("name_hindi") or data.get("crop_name_hi")
                cards.append(CropCard(
                    crop_name=name,
                    crop_name_hindi=name_hi,
                    score=60.0,
                    reasons=["Retrieved from Database"],
                    source="VectorDB"
                ))
        return {"cards": cards, "reasoning": "Retrieved from knowledge base (Logic Engine Unavailable)"}

    def _synthesize_schemes(
        self,
        docs: List[Dict[str, Any]],
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Synthesize government scheme information"""
        cards = []
        
        for doc in docs:
            if doc.get("type") == "scheme_info":
                data = doc["data"]
                card = SchemeCard(
                    scheme_name=data.get("name"),
                    scheme_name_hindi=data.get("name_hindi"),
                    eligible=True,  # Default for general queries
                    reasons=[data.get("description", "Relevant scheme")],
                    source="VectorDB"
                )
                cards.append(card)
        
        return {"cards": cards, "reasoning": "Relevant government schemes found."}
    
    def _synthesize_weather(self, docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize weather information"""
        cards = []
        
        for doc in docs:
            if doc.get("type") == "weather_info":
                data = doc["data"]
                cards.append(WeatherCard(
                    temperature=data.get("temperature", 0.0),
                    humidity=data.get("humidity", 0.0),
                    rain_forecast=data.get("rain_forecast", False),
                    advisory=data.get("advisory", ""),
                    source=doc.get("source", "WeatherAPI")
                ))
        
        return {"cards": cards, "reasoning": "Current weather conditions."}
    
    def _synthesize_market(self, docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize market information"""
        cards = []
        
        for doc in docs:
            if doc.get("type") == "market_price":
                data = doc["data"]
                cards.append(MarketCard(
                    crop_name=doc.get("crop") or data.get("crop"),
                    price=data.get("price"),
                    trend=data.get("trend", "Stable"),
                    market_name=data.get("market") or data.get("market_name", "Mandi"),
                    source=doc.get("source", "MarketAPI")
                ))
        
        return {"cards": cards, "reasoning": "Latest market prices."}


# Singleton instance
_synthesizer = None

def get_synthesizer() -> Synthesizer:
    """Get or create synthesizer"""
    global _synthesizer
    if _synthesizer is None:
        _synthesizer = Synthesizer()
    return _synthesizer
