"""
Explanation Builder - Generates simple, spoken-style explanations
"""

from typing import List, Dict, Any
from voice_agent.core.intent import Intent
from voice_agent.input_processing.translator import get_translator


class ExplanationBuilder:
    """Builds simple, farmer-friendly explanations"""
    
    def __init__(self):
        self.translator = get_translator()
    
    def build_explanation(
        self,
        intent: Intent,
        cards: List[Any],
        reasoning: str,
        language: str = "hindi"
    ) -> str:
        """
        Build explanation from cards and reasoning
        
        Args:
            intent: Detected intent
            cards: Generated cards
            reasoning: Reasoning text
            language: Output language (hindi/english)
        
        Returns:
            Explanation text
        """
        if intent == Intent.CROP_PLANNING:
            explanation = self._explain_crop_planning(cards, reasoning)
        elif intent == Intent.GOVERNMENT_SCHEME:
            explanation = self._explain_schemes(cards, reasoning)
        elif intent == Intent.WEATHER_QUERY:
            explanation = self._explain_weather(cards)
        elif intent == Intent.MARKET_PRICE:
            explanation = self._explain_market(cards)
        else:
            explanation = reasoning
        
        # Translate to Hindi if needed
        if language == "hindi":
            explanation = self.translator.english_to_hindi(explanation)
        
        return explanation
    
    def _explain_crop_planning(self, cards: List[Any], reasoning: str) -> str:
        """Explain crop planning recommendation"""
        if not cards:
            return "No crop recommendations available."
        
        # Get top crop
        crop_cards = [c for c in cards if c.card_type == "crop"]
        if crop_cards:
            top_crop = crop_cards[0]
            crop_name = top_crop.details["crop_name"]
            crop_name_hindi = top_crop.details["crop_name_hindi"]
            reasons = top_crop.details.get("reasons", [])
            
            explanation = f"I recommend growing {crop_name} ({crop_name_hindi}). "
            
            if reasons:
                explanation += f"Reasons: {', '.join(reasons[:2])}. "
            
            explanation += reasoning
            
            return explanation
        
        return reasoning
    
    def _explain_schemes(self, cards: List[Any], reasoning: str) -> str:
        """Explain government schemes"""
        scheme_cards = [c for c in cards if c.card_type == "scheme"]
        
        if not scheme_cards:
            return "No schemes found."
        
        eligible_schemes = [c for c in scheme_cards if c.details.get("eligible")]
        
        if eligible_schemes:
            scheme_names = [c.details["scheme_name_hindi"] for c in eligible_schemes[:2]]
            explanation = f"You are eligible for {len(eligible_schemes)} schemes: {', '.join(scheme_names)}. "
            explanation += reasoning
            return explanation
        
        return "You are not eligible for any schemes at this time."
    
    def _explain_weather(self, cards: List[Any]) -> str:
        """Explain weather"""
        weather_cards = [c for c in cards if c.card_type == "weather"]
        
        if weather_cards:
            weather = weather_cards[0]
            temp = weather.details["temperature"]
            rain = weather.details["rain_forecast"]
            
            explanation = f"Current temperature is {temp}°C. "
            if rain:
                explanation += "Rain is expected. "
            else:
                explanation += "Clear weather expected. "
            
            return explanation
        
        return "Weather information not available."
    
    def _explain_market(self, cards: List[Any]) -> str:
        """Explain market prices"""
        market_cards = [c for c in cards if c.card_type == "market"]
        
        if market_cards:
            explanations = []
            for card in market_cards[:3]:
                crop = card.details["crop_name"]
                price = card.details["price"]
                trend = card.details["trend_hindi"]
                explanations.append(f"{crop} price is ₹{price}/kg, {trend}")
            
            return ". ".join(explanations) + "."
        
        return "Market information not available."


# Singleton instance
_builder = None

def get_explanation_builder() -> ExplanationBuilder:
    """Get or create explanation builder"""
    global _builder
    if _builder is None:
        _builder = ExplanationBuilder()
    return _builder
