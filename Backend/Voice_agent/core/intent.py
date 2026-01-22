"""
Intent Classification Module
LLM-based intent detection using Groq or Gemini
"""

from enum import Enum
from typing import List, Optional
from dataclasses import dataclass
import os
import json


class Intent(str, Enum):
    """Supported intents"""
    CROP_PLANNING = "crop_planning"
    STORAGE_DECISION = "storage_decision"
    SELLING_DECISION = "selling_decision"
    GOVERNMENT_SCHEME = "government_scheme"
    IRRIGATION_ADVICE = "irrigation_advice"
    DISEASE_TREATMENT = "disease_treatment"
    FERTILIZER_ADVICE = "fertilizer_advice"
    HARVEST_PLANNING = "harvest_planning"
    WEATHER_QUERY = "weather_query"
    MARKET_PRICE = "market_price"
    FOLLOW_UP = "follow_up"
    UNKNOWN = "unknown"


@dataclass
class IntentResult:
    """Intent detection result"""
    intent: Intent
    confidence: float
    reasoning: str


class LLMIntentClassifier:
    """LLM-based intent classifier using Groq or Gemini"""
    
    def __init__(self, provider: str = None, model: str = None):
        """
        Initialize LLM intent classifier
        
        Args:
            provider: "groq" or "gemini" (optional, auto-detected from config)
            model: Model name (optional, uses default for provider)
        """
        # Import config here to avoid circular imports
        from voice_agent.config import get_config
        
        # Auto-detect provider from config if not specified
        if provider is None:
            config = get_config()
            self.provider = config.llm_provider
            self.api_key = config.llm_api_key
            self.model = model or config.llm_model
        else:
            self.provider = provider.lower()
            self.api_key = None  # Will be loaded from env
            self.model = model
        
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize LLM client based on provider"""
        if self.provider == "groq":
            self._initialize_groq()
        elif self.provider == "gemini":
            self._initialize_gemini()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _initialize_groq(self):
        """Initialize Groq client"""
        try:
            from groq import Groq
            
            # Use provided API key or get from config
            if self.api_key is None:
                from voice_agent.config import get_config
                config = get_config()
                if config.llm_provider != "groq":
                    raise ValueError("Groq API key not found in config")
                self.api_key = config.llm_api_key
            
            self.client = Groq(api_key=self.api_key)
            self.model = self.model or "llama-3.1-8b-instant"  # Fast, lightweight model
            print(f"✅ Groq client initialized with model: {self.model}")
            
        except Exception as e:
            print(f"❌ Error initializing Groq: {e}")
            raise
    
    def _initialize_gemini(self):
        """Initialize Gemini client"""
        try:
            import google.generativeai as genai
            
            # Use provided API key or get from config
            if self.api_key is None:
                from voice_agent.config import get_config
                config = get_config()
                if config.llm_provider != "gemini":
                    raise ValueError("Gemini API key not found in config")
                self.api_key = config.llm_api_key
            
            genai.configure(api_key=self.api_key)
            self.model = self.model or "gemini-1.5-flash"  # Fast, lightweight model
            self.client = genai.GenerativeModel(self.model)
            print(f"✅ Gemini client initialized with model: {self.model}")
            
        except Exception as e:
            print(f"❌ Error initializing Gemini: {e}")
            raise
    
    def classify(self, text: str) -> IntentResult:
        """
        Classify intent from text using LLM
        
        Args:
            text: Input text (Hindi or English)
        
        Returns:
            IntentResult with detected intent and confidence
        """
        # Create prompt for intent classification
        prompt = self._create_classification_prompt(text)
        
        try:
            # Get LLM response
            if self.provider == "groq":
                response = self._classify_with_groq(prompt)
            else:  # gemini
                response = self._classify_with_gemini(prompt)
            
            # Parse response
            intent_result = self._parse_llm_response(response)
            return intent_result
            
        except Exception as e:
            print(f"⚠️  LLM classification error: {e}, using fallback")
            return self._fallback_classify(text)
    
    def _create_classification_prompt(self, text: str) -> str:
        """Create prompt for intent classification"""
        intents_list = "\n".join([
            f"- {intent.value}: {self.get_intent_description(intent)}"
            for intent in Intent if intent != Intent.UNKNOWN
        ])
        
        prompt = f"""You are an intent classifier for a farming assistant application.
Classify the following farmer query into ONE of these intents:

{intents_list}

Farmer Query: "{text}"

Respond ONLY with a JSON object in this exact format:
{{
    "intent": "intent_name",
    "confidence": 0.95,
    "reasoning": "Brief explanation"
}}

Intent must be one of: {', '.join([i.value for i in Intent if i != Intent.UNKNOWN])}
Confidence must be between 0.0 and 1.0.
"""
        return prompt
    
    def _classify_with_groq(self, prompt: str) -> str:
        """Classify using Groq"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,  # Low temperature for consistent classification
            max_tokens=150
        )
        return response.choices[0].message.content
    
    def _classify_with_gemini(self, prompt: str) -> str:
        """Classify using Gemini"""
        response = self.client.generate_content(
            prompt,
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 150
            }
        )
        return response.text
    
    def _parse_llm_response(self, response: str) -> IntentResult:
        """Parse LLM response to extract intent"""
        try:
            # Extract JSON from response
            response = response.strip()
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            data = json.loads(response)
            
            intent_str = data.get("intent", "unknown")
            confidence = float(data.get("confidence", 0.5))
            reasoning = data.get("reasoning", "")
            
            # Convert to Intent enum
            try:
                intent = Intent(intent_str)
            except ValueError:
                intent = Intent.UNKNOWN
            
            return IntentResult(
                intent=intent,
                confidence=confidence,
                reasoning=reasoning
            )
            
        except Exception as e:
            print(f"⚠️  Error parsing LLM response: {e}")
            print(f"   Response was: {response[:200]}")
            return IntentResult(
                intent=Intent.UNKNOWN,
                confidence=0.0,
                reasoning="Failed to parse LLM response"
            )
    
    def _fallback_classify(self, text: str) -> IntentResult:
        """Fallback classification using simple keyword matching"""
        text_lower = text.lower()
        
        # Simple keyword matching as fallback
        if any(kw in text_lower for kw in ["फसल", "crop", "plant", "बोना", "लगाना"]):
            return IntentResult(Intent.CROP_PLANNING, 0.6, "Keyword match (fallback)")
        elif any(kw in text_lower for kw in ["योजना", "scheme", "सरकार"]):
            return IntentResult(Intent.GOVERNMENT_SCHEME, 0.6, "Keyword match (fallback)")
        elif any(kw in text_lower for kw in ["मौसम", "weather", "बारिश"]):
            return IntentResult(Intent.WEATHER_QUERY, 0.6, "Keyword match (fallback)")
        elif any(kw in text_lower for kw in ["कीमत", "price", "बाजार"]):
            return IntentResult(Intent.MARKET_PRICE, 0.6, "Keyword match (fallback)")
        else:
            return IntentResult(Intent.UNKNOWN, 0.3, "No match found (fallback)")
    
    def get_intent_description(self, intent: Intent) -> str:
        """Get human-readable description of intent"""
        descriptions = {
            Intent.CROP_PLANNING: "Crop selection and planning",
            Intent.STORAGE_DECISION: "Storage decision making",
            Intent.SELLING_DECISION: "Selling and market decision",
            Intent.GOVERNMENT_SCHEME: "Government scheme information",
            Intent.IRRIGATION_ADVICE: "Irrigation guidance",
            Intent.DISEASE_TREATMENT: "Disease treatment advice",
            Intent.FERTILIZER_ADVICE: "Fertilizer recommendations",
            Intent.HARVEST_PLANNING: "Harvest timing planning",
            Intent.WEATHER_QUERY: "Weather information",
            Intent.MARKET_PRICE: "Market price information",
            Intent.FOLLOW_UP: "Follow-up question",
            Intent.UNKNOWN: "Unknown intent",
        }
        return descriptions.get(intent, "Unknown")


# Singleton instance
_classifier = None

def get_intent_classifier(provider: str = None, model: str = None) -> LLMIntentClassifier:
    """
    Get or create intent classifier instance
    Auto-detects provider from config if not specified
    
    Args:
        provider: "groq" or "gemini" (optional, auto-detected)
        model: Model name (optional)
    
    Returns:
        LLMIntentClassifier instance
    """
    global _classifier
    if _classifier is None:
        _classifier = LLMIntentClassifier(provider=provider, model=model)
    return _classifier
