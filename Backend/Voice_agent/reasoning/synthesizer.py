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

# Import service connectors
from voice_agent.connectors import (
    get_financial_connector,
    get_collaborative_connector,
    get_inventory_connector,
    get_alerts_connector
)


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
        context = context or {}
        
        # Financial Tracking Intents
        if intent == Intent.FINANCE_REPORT:
            return self._synthesize_finance_report(context)
        elif intent == Intent.ADD_EXPENSE:
            return self._synthesize_add_expense(context)
        elif intent == Intent.ADD_INCOME:
            return self._synthesize_add_income(context)
        elif intent == Intent.COST_ANALYSIS:
            return self._synthesize_finance_report(context)  # Same as finance report
        elif intent == Intent.OPTIMIZATION_ADVICE:
            return self._synthesize_optimization_advice(context)
        
        # Collaborative Farming Intents
        elif intent == Intent.VIEW_MARKETPLACE:
            return self._synthesize_collaborative_marketplace(context)
        elif intent == Intent.EQUIPMENT_RENTAL:
            return self._synthesize_equipment_rental(context)
        elif intent == Intent.LAND_POOLING:
            return self._synthesize_land_pooling(context)
        elif intent == Intent.RESIDUE_MANAGEMENT:
            return self._synthesize_collaborative_marketplace(context)  # Part of marketplace
        
        # Inventory Intents
        elif intent == Intent.CHECK_STOCK:
            return self._synthesize_inventory_check(context)
        elif intent == Intent.SELL_RECOMMENDATION:
            return self._synthesize_sell_recommendation(context)
        elif intent == Intent.SPOILAGE_ALERT:
            return self._synthesize_inventory_check(context)  # Part of inventory check
        
        # Alerts Intents
        elif intent == Intent.CHECK_ALERTS:
            return self._synthesize_alerts_check(context)
        elif intent == Intent.REMINDER_CHECK:
            return self._synthesize_alerts_check(context)  # Part of alerts
        
        # Existing Intents
        elif intent == Intent.CROP_PLANNING:
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
    
    # NEW SYNTHESIS METHODS FOR INTEGRATED MODULES
    
    def _synthesize_finance_report(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize financial report"""
        farmer_id = context.get("farmer_id", "F001")
        language = context.get("language", "hi")
        season = context.get("season", "KHARIF")
        
        connector = get_financial_connector()
        result = connector.get_finance_report(farmer_id, season, language)
        
        return {
            "cards": [],
            "reasoning": result["speech_text"]
        }
    
    def _synthesize_add_expense(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize expense addition"""
        farmer_id = context.get("farmer_id", "F001")
        amount = context.get("amount", 0)
        category = context.get("category", "OTHER")
        notes = context.get("notes", "")
        season = context.get("season", "KHARIF")
        
        connector = get_financial_connector()
        result = connector.add_expense(
            farmer_id, category, amount, season, notes
        )
        
        language = context.get("language", "hi")
        if result["success"]:
            message = f"Expense of ₹{amount} recorded successfully" if language == "en" else f"₹{amount} का खर्च रिकॉर्ड किया गया"
        else:
            message = f"Failed to add expense: {result['message']}"
        
        return {"cards": [], "reasoning": message}
    
    def _synthesize_add_income(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize income addition"""
        farmer_id = context.get("farmer_id", "F001")
        amount = context.get("amount", 0)
        category = context.get("category", "SALE")
        notes = context.get("notes", "")
        season = context.get("season", "KHARIF")
        
        connector = get_financial_connector()
        result = connector.add_income(
            farmer_id, category, amount, season, notes
        )
        
        language = context.get("language", "hi")
        if result["success"]:
            message = f"Income of ₹{amount} recorded successfully" if language == "en" else f"₹{amount} की आय रिकॉर्ड की गई"
        else:
            message = f"Failed to add income: {result['message']}"
        
        return {"cards": [], "reasoning": message}
    
    def _synthesize_optimization_advice(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize optimization advice"""
        farmer_id = context.get("farmer_id", "F001")
        language = context.get("language", "hi")
        season = context.get("season", "KHARIF")
        
        connector = get_financial_connector()
        result = connector.get_finance_report(farmer_id, season, language)
        
        suggestions = result.get("suggestions", [])
        if suggestions:
            top_suggestion = suggestions[0]
            reasoning = f"{top_suggestion.suggestionTitle}: {top_suggestion.whyThisHelps}"
        else:
            reasoning = "No optimization suggestions available at this time"
        
        return {"cards": [], "reasoning": reasoning}
    
    def _synthesize_collaborative_marketplace(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize collaborative farming marketplace"""
        farmer_id = context.get("farmer_id", "F001")
        language = context.get("language", "hi")
        
        connector = get_collaborative_connector()
        result = connector.get_marketplace(farmer_id, language)
        
        return {
            "cards": [],
            "reasoning": result["speech_text"]
        }
    
    def _synthesize_equipment_rental(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize equipment rental request"""
        farmer_id = context.get("farmer_id", "F001")
        equipment_type = context.get("equipment_type", "TRACTOR")
        
        connector = get_collaborative_connector()
        result = connector.request_equipment(farmer_id, equipment_type)
        
        return {"cards": [], "reasoning": result["message"]}
    
    def _synthesize_land_pooling(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize land pooling request"""
        farmer_id = context.get("farmer_id", "F001")
        request_type = context.get("pool_type", "seek_partner")
        land_size = context.get("land_size", 5.0)
        crop = context.get("crop", "Wheat")
        
        connector = get_collaborative_connector()
        result = connector.create_land_pool(farmer_id, request_type, land_size, crop)
        
        return {"cards": [], "reasoning": result["message"]}
    
    def _synthesize_inventory_check(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize inventory check"""
        farmer_id = context.get("farmer_id", "F001")
        language = context.get("language", "hi")
        
        connector = get_inventory_connector()
        result = connector.get_dashboard(farmer_id, language)
        
        return {"cards": [], "reasoning": result.get("speech_text", "Inventory loaded")}
    
    def _synthesize_sell_recommendation(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize sell recommendations"""
        farmer_id = context.get("farmer_id", "F001")
        
        connector = get_inventory_connector()
        to_sell = connector.get_sell_recommendations(farmer_id)
        
        if to_sell:
            items = ", ".join([f"{item['crop']} ({item['quantity']}kg)" for item in to_sell[:3]])
            reasoning = f"Recommended to sell now: {items}"
        else:
            reasoning = "No urgent sell recommendations at this time"
        
        return {"cards": [], "reasoning": reasoning}
    
    def _synthesize_alerts_check(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize alerts check"""
        farmer_id = context.get("farmer_id", "F001")
        language = context.get("language", "hi")
        
        connector = get_alerts_connector()
        result = connector.get_alerts(farmer_id, language=language)
        
        return {"cards": [], "reasoning": result["speech_text"]}



# Singleton instance
_synthesizer = None

def get_synthesizer() -> Synthesizer:
    """Get or create synthesizer"""
    global _synthesizer
    if _synthesizer is None:
        _synthesizer = Synthesizer()
    return _synthesizer
