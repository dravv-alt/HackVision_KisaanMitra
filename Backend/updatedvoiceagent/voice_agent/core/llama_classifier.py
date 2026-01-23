"""
Llama 2 Intent Classifier via Groq API
Uses Pydantic schemas for strict structured outputs
"""

from groq import Groq
from pydantic import ValidationError
from voice_agent.schemas.intent_schemas import (
    IntentClassificationResult,
    Intent,
    EntityExtractionSchema
)
import json
import os
from typing import Dict, Any


class Llama2IntentClassifier:
    """
    Intent classifier using Llama 3.1 8B via Groq API
    with Pydantic structured output validation
    
    Uses the lightweight 8B model for fast, efficient intent classification
    """
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize Llama classifier
        
        Args:
            api_key: Groq API key (optional, will use env var)
            model: Groq model name (default: llama-3.1-8b-instant)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment or parameters")
        
        self.client = Groq(api_key=self.api_key)
        # Use Llama 3.1 8B Instant - smaller, faster model for basic intent classification
        self.model = model or "llama-3.1-8b-instant"
        
        print(f"✅ Llama 3.1 8B Intent Classifier initialized")
        print(f"   Model: {self.model} (lightweight & fast)")
        print(f"   Provider: Groq API")
    
    def classify(self, transcribed_text: str) -> IntentClassificationResult:
        """
        Classify intent from transcribed voice text using Llama 3.1 8B
        
        Args:
            transcribed_text: Text from Whisper STT or user input
            
        Returns:
            IntentClassificationResult (Pydantic validated)
        """
        print(f"\n🎯 Classifying intent with Llama 3.1 8B: '{transcribed_text}'")
        
        # Create strict prompt with Pydantic schema
        system_prompt = self._create_system_prompt()
        user_prompt = self._create_user_prompt(transcribed_text)
        
        try:
            # Call Groq Llama 3.1 8B API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temp for consistent classification
                max_tokens=400,
                top_p=0.9
            )
            
            # Extract and validate response
            llm_output = response.choices[0].message.content
            intent_result = self._parse_and_validate(llm_output)
            
            print(f"✅ Intent classified: {intent_result.intent}")
            print(f"   Confidence: {intent_result.confidence:.2f}")
            print(f"   Entities: {intent_result.entities}")
            
            return intent_result
            
        except Exception as e:
            print(f"❌ Llama 3.1 8B classification error: {e}")
            return self._fallback_classify(transcribed_text)
    
    def _create_system_prompt(self) -> str:
        """Create system prompt with Pydantic schema and all intent descriptions"""
        
        intent_descriptions = {
            Intent.CROP_PLANNING: "User wants crop recommendations for planting",
            Intent.MARKET_PRICE: "User asks about current market prices for crops",
            Intent.GOVERNMENT_SCHEME: "User asks about government schemes or subsidies",
            Intent.FINANCE_REPORT: "User wants profit/loss report or financial summary",
            Intent.ADD_EXPENSE: "User wants to record a farming expense",
            Intent.ADD_INCOME: "User wants to record income from crop sales",
            Intent.COST_ANALYSIS: "User asks where money is being spent",
            Intent.OPTIMIZATION_ADVICE: "User wants advice to reduce costs",
            Intent.DISEASE_DIAGNOSIS: "User describes crop disease symptoms",
            Intent.DISEASE_TREATMENT: "User asks how to treat a crop disease",
            Intent.WEATHER_QUERY: "User asks about weather conditions",
            Intent.HARVEST_TIMING: "User asks when to harvest crops",
            Intent.SELLING_DECISION: "User asks whether to sell crops now",
            Intent.STORAGE_DECISION: "User asks about crop storage",
            Intent.FERTILIZER_ADVICE: "User asks about fertilizer recommendations",
            Intent.IRRIGATION_ADVICE: "User asks about irrigation/watering",
            Intent.EQUIPMENT_RENTAL: "User wants to rent farming equipment",
            Intent.LAND_POOLING: "User wants to do cooperative farming",
            Intent.CHECK_STOCK: "User asks about current inventory/stock",
            Intent.SELL_RECOMMENDATION: "User asks when to sell stored crops",
            Intent.CHECK_ALERTS: "User asks for pending alerts or notifications",
            Intent.POST_HARVEST_QUERY: "User asks about post-harvest handling",
            Intent.FOLLOW_UP: "Follow-up question related to previous conversation",
            Intent.UNKNOWN: "Cannot classify - query not related to farming"
        }
        
        intents_list = "\n".join([
            f"  - {intent.value}: {desc}"
            for intent, desc in intent_descriptions.items()
            if intent != Intent.UNKNOWN  # Don't encourage UNKNOWN
        ])
        
        return f"""You are an intent classifier for KisaanMitra, a farming assistant application in India.

Your task: Classify the farmer's query (in Hindi or English) into ONE of these intents:

{intents_list}

You must also extract key entities like:
- crop_name: Name of crop mentioned (e.g., "onion", "wheat", "प्याज")
- amount: Any numeric value (price, quantity, etc.)
- location: City/district mentioned
- category: Type of expense/income (seeds, fertilizer, labor, etc.)
- season: kharif, rabi, or zaid if mentioned

CRITICAL INSTRUCTIONS:
1. Respond ONLY with valid JSON
2. Match this EXACT Pydantic schema:

{{
  "intent": "<one of the intent values above>",
  "confidence": <float between 0.0 and 1.0>,
  "entities": {{
    "crop_name": "<crop if mentioned>",
    "amount": <number if mentioned>,
    "location": "<location if mentioned>",
    "category": "<category if expense/income>",
    "season": "<season if mentioned>"
  }},
  "reasoning": "<brief 1-2 sentence explanation>",
  "language_detected": "hi" or "en"
}}

3. DO NOT add any explanation before or after the JSON
4. ONLY return the JSON object
5. All keys must be lowercase
6. Confidence must be realistic (0.7-0.95 for good matches, lower if uncertain)

Examples:
- "प्याज की कीमत क्या है" → intent: market_price, entities: {{"crop_name": "onion"}}
- "कौनसी फसल बोऊं" → intent: crop_planning
- "5000 रुपये बीज पर खर्च किया" → intent: add_expense, entities: {{"amount": 5000, "category": "seeds"}}
"""
    
    def _create_user_prompt(self, text: str) -> str:
        """Create user prompt with farmer query"""
        return f"""Farmer Query: "{text}"

Classify the intent and extract entities. Return ONLY the JSON object."""
    
    def _parse_and_validate(self, llm_output: str) -> IntentClassificationResult:
        """
        Parse LLM output and validate with Pydantic
        
        Raises:
            ValidationError if output doesn't match schema
        """
        try:
            # Clean JSON from LLM output
            llm_output = llm_output.strip()
            
            # Remove markdown code blocks if present
            if "```json" in llm_output:
                llm_output = llm_output.split("```json")[1].split("```")[0].strip()
            elif "```" in llm_output:
                llm_output = llm_output.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            data = json.loads(llm_output)
            
            # Validate with Pydantic (strict enforcement!)
            result = IntentClassificationResult(**data)
            
            print(f"✅ Pydantic validation passed")
            return result
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON Parse Error: {e}")
            print(f"   LLM Output: {llm_output[:300]}")
            
            # Fallback to UNKNOWN intent
            return IntentClassificationResult(
                intent=Intent.UNKNOWN,
                confidence=0.0,
                entities={},
                reasoning=f"Failed to parse LLM JSON output: {str(e)}",
                language_detected="hi"
            )
            
        except ValidationError as e:
            print(f"❌ Pydantic Validation Error: {e}")
            print(f"   Parsed data: {data}")
            
            # Try to salvage what we can
            try:
                intent_str = data.get("intent", "unknown")
                intent = Intent(intent_str) if intent_str in [i.value for i in Intent] else Intent.UNKNOWN
                
                return IntentClassificationResult(
                    intent=intent,
                    confidence=float(data.get("confidence", 0.5)),
                    entities=data.get("entities", {}),
                    reasoning=data.get("reasoning", "Partial validation failure"),
                    language_detected=data.get("language_detected", "hi")
                )
            except:
                # Complete fallback
                return IntentClassificationResult(
                    intent=Intent.UNKNOWN,
                    confidence=0.0,
                    entities={},
                    reasoning=f"LLM output failed Pydantic validation: {str(e)}",
                    language_detected="hi"
                )
        
        except Exception as e:
            print(f"❌ Unexpected error in parsing: {e}")
            return IntentClassificationResult(
                intent=Intent.UNKNOWN,
                confidence=0.0,
                entities={},
                reasoning=f"Unexpected error: {str(e)}",
                language_detected="hi"
            )
    
    def _fallback_classify(self, text: str) -> IntentClassificationResult:
        """Fallback classification using simple keyword matching"""
        text_lower = text.lower()
        
        print("⚠️  Using fallback keyword-based classification")
        
        # Simple keyword matching as fallback
        if any(kw in text_lower for kw in ["फसल", "crop", "plant", "बोना", "लगाना", "कौन", "which"]):
            return IntentClassificationResult(
                intent=Intent.CROP_PLANNING,
                confidence=0.6,
                entities={},
                reasoning="Fallback: Keyword match for crop planning",
                language_detected="hi" if any(c in text for c in "ाीुूेैोौंः") else "en"
            )
        
        elif any(kw in text_lower for kw in ["योजना", "scheme", "सरकार", "government", "subsidy"]):
            return IntentClassificationResult(
                intent=Intent.GOVERNMENT_SCHEME,
                confidence=0.6,
                entities={},
                reasoning="Fallback: Keyword match for schemes",
                language_detected="hi" if any(c in text for c in "ाीुूेैोौंः") else "en"
            )
        
        elif any(kw in text_lower for kw in ["मौसम", "weather", "बारिश", "rain"]):
            return IntentClassificationResult(
                intent=Intent.WEATHER_QUERY,
                confidence=0.6,
                entities={},
                reasoning="Fallback: Keyword match for weather",
                language_detected="hi" if any(c in text for c in "ाीुूेैोौंः") else "en"
            )
        
        elif any(kw in text_lower for kw in ["कीमत", "price", "भाव", "rate", "मंडी", "mandi", "market"]):
            # Try to extract crop name
            crops = ["onion", "प्याज", "wheat", "गेहूं", "rice", "धान", "potato", "आलू"]
            crop_found = None
            for crop in crops:
                if crop in text_lower:
                    crop_found = crop
                    break
            
            return IntentClassificationResult(
                intent=Intent.MARKET_PRICE,
                confidence=0.65,
                entities={"crop_name": crop_found} if crop_found else {},
                reasoning="Fallback: Keyword match for market price",
                language_detected="hi" if any(c in text for c in "ाीुूेैोौंः") else "en"
            )
        
        elif any(kw in text_lower for kw in ["खर्च", "expense", "खर्चा", "खरीद", "bought"]):
            return IntentClassificationResult(
                intent=Intent.ADD_EXPENSE,
                confidence=0.6,
                entities={},
                reasoning="Fallback: Keyword match for expense",
                language_detected="hi" if any(c in text for c in "ाीुूेैोौंः") else "en"
            )
        
        elif any(kw in text_lower for kw in ["मुनाफा", "profit", "फायदा", "लाभ", "income", "आय"]):
            return IntentClassificationResult(
                intent=Intent.FINANCE_REPORT,
                confidence=0.6,
                entities={},
                reasoning="Fallback: Keyword match for finance",
                language_detected="hi" if any(c in text for c in "ाीुूेैोौंः") else "en"
            )
        
        else:
            return IntentClassificationResult(
                intent=Intent.UNKNOWN,
                confidence=0.3,
                entities={},
                reasoning="Fallback: No keyword match found",
                language_detected="hi" if any(c in text for c in "ाीुूेैोौंः") else "en"
            )


# Singleton instance
_llama2_classifier = None

def get_llama2_classifier(api_key: str = None, model: str = None) -> Llama2IntentClassifier:
    """
    Get or create Llama 2 classifier instance
    
    Args:
        api_key: Groq API key (optional)
        model: Model name (optional)
    
    Returns:
        Llama2IntentClassifier instance
    """
    global _llama2_classifier
    if _llama2_classifier is None:
        _llama2_classifier = Llama2IntentClassifier(api_key=api_key, model=model)
    return _llama2_classifier
