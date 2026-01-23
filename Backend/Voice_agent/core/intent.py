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
    # Existing intents
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
    
    # NEW - Financial Tracking (5 intents)
    FINANCE_REPORT = "finance_report"           # "मेरा मुनाफा बताओ"
    ADD_EXPENSE = "add_expense"                  # "मैंने 5000 रुपये बीज पर खर्च किए"
    ADD_INCOME = "add_income"                    # "मैंने गेहूं 50000 में बेची"
    COST_ANALYSIS = "cost_analysis"              # "कहां ज्यादा खर्च हो रहा?"
    OPTIMIZATION_ADVICE = "optimization_advice"   # "खर्च कैसे कम करूं?"
    
    # NEW - Collaborative Farming (4 intents)
    EQUIPMENT_RENTAL = "equipment_rental"        # "ट्रैक्टर किराए पर चाहिए"
    LAND_POOLING = "land_pooling"               # "साझे में खेती करनी है"
    RESIDUE_MANAGEMENT = "residue_management"    # "पराली कहां बेचूं?"
    VIEW_MARKETPLACE = "view_marketplace"        # "आसपास कौनसे उपकरण मिलेंगे?"
    
    # NEW - Inventory (3 intents)
    CHECK_STOCK = "check_stock"                  # "मेरा स्टॉक कितना है?"
    SELL_RECOMMENDATION = "sell_recommendation"   # "अभी बेचूं या नहीं?"
    SPOILAGE_ALERT = "spoilage_alert"           # "खराब होने वाला माल बताओ"
    
    # NEW - Alerts (2 intents)
    CHECK_ALERTS = "check_alerts"                # "मेरे लिए कोई अलर्ट है?"
    REMINDER_CHECK = "reminder_check"            # "कल क्या करना है?"
    
    # NEW - Advanced Farming (3 intents)
    DISEASE_DIAGNOSIS = "disease_diagnosis"      # "पत्ते पीले हो रहे हैं"
    HARVEST_TIMING = "harvest_timing"            # "कटाई कब करूं?"
    POST_HARVEST_QUERY = "post_harvest_query"    # "भंडारण कैसे करूं?"
    
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
        from Backend.Voice_agent.config import get_config
        
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
                from Backend.Voice_agent.config import get_config
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
                from Backend.Voice_agent.config import get_config
                config = get_config()
                if config.llm_provider != "gemini":
                    raise ValueError("Gemini API key not found in config")
                self.api_key = config.llm_api_key
            
            genai.configure(api_key=self.api_key)
            self.model = self.model or "gemini-1.5-flash"  # Updated to new model
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
            # Existing intents
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
            
            # Financial Tracking
            Intent.FINANCE_REPORT: "Profit/loss report and financial summary",
            Intent.ADD_EXPENSE: "Record farming expense",
            Intent.ADD_INCOME: "Record income from sales",
            Intent.COST_ANALYSIS: "Analyze where money is being spent",
            Intent.OPTIMIZATION_ADVICE: "Get suggestions to reduce costs",
            
            # Collaborative Farming
            Intent.EQUIPMENT_RENTAL: "Find and rent farming equipment",
            Intent.LAND_POOLING: "Find partners for cooperative farming",
            Intent.RESIDUE_MANAGEMENT: "Sell or manage crop residue",
            Intent.VIEW_MARKETPLACE: "Browse available equipment and land pools",
            
            # Inventory
            Intent.CHECK_STOCK: "Check current inventory status",
            Intent.SELL_RECOMMENDATION: "Get recommendation on when to sell",
            Intent.SPOILAGE_ALERT: "Check for items at risk of spoilage",
            
            # Alerts
            Intent.CHECK_ALERTS: "View pending alerts and notifications",
            Intent.REMINDER_CHECK: "Check scheduled reminders",
            
            # Advanced Farming
            Intent.DISEASE_DIAGNOSIS: "Diagnose crop disease from symptoms",
            Intent.HARVEST_TIMING: "Get harvest timing recommendations",
            Intent.POST_HARVEST_QUERY: "Post-harvest storage and processing advice",
            
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
