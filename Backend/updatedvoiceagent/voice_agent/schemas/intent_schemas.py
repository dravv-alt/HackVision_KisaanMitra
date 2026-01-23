"""
Pydantic Schemas for Llama 2 8B Structured Outputs
Ensures strict validation of LLM responses
"""

from pydantic import BaseModel, Field, constr, confloat, validator
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime


class Intent(str, Enum):
    """All supported intents for farming assistant"""
    # Planning & Crop Management
    CROP_PLANNING = "crop_planning"
    HARVEST_TIMING = "harvest_timing"
    IRRIGATION_ADVICE = "irrigation_advice"
    
    # Market & Selling
    MARKET_PRICE = "market_price"
    SELLING_DECISION = "selling_decision"
    STORAGE_DECISION = "storage_decision"
    
    # Disease & Treatment
    DISEASE_DIAGNOSIS = "disease_diagnosis"
    DISEASE_TREATMENT = "disease_treatment"
    FERTILIZER_ADVICE = "fertilizer_advice"
    
    # Financial Tracking
    FINANCE_REPORT = "finance_report"
    ADD_EXPENSE = "add_expense"
    ADD_INCOME = "add_income"
    COST_ANALYSIS = "cost_analysis"
    OPTIMIZATION_ADVICE = "optimization_advice"
    
    # Government Schemes
    GOVERNMENT_SCHEME = "government_scheme"
    
    # Collaborative Farming
    EQUIPMENT_RENTAL = "equipment_rental"
    LAND_POOLING = "land_pooling"
    RESIDUE_MANAGEMENT = "residue_management"
    VIEW_MARKETPLACE = "view_marketplace"
    
    # Inventory Management
    CHECK_STOCK = "check_stock"
    SELL_RECOMMENDATION = "sell_recommendation"
    SPOILAGE_ALERT = "spoilage_alert"
    
    # Alerts & Reminders
    CHECK_ALERTS = "check_alerts"
    REMINDER_CHECK = "reminder_check"
    
    # Weather & Post-Harvest
    WEATHER_QUERY = "weather_query"
    POST_HARVEST_QUERY = "post_harvest_query"
    
    # General
    FOLLOW_UP = "follow_up"
    UNKNOWN = "unknown"


class IntentClassificationResult(BaseModel):
    """
    Strict schema for Llama 2 intent classification output
    LLM MUST return data matching this exact structure
    """
    intent: Intent = Field(
        ..., 
        description="Classified user intent from the predefined list"
    )
    
    confidence: confloat(ge=0.0, le=1.0) = Field(
        ..., 
        description="Confidence score between 0.0 and 1.0"
    )
    
    entities: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extracted entities like crop name, amount, location, date"
    )
    
    reasoning: str = Field(
        ..., 
        min_length=5,
        max_length=500,
        description="Brief explanation of why this intent was chosen"
    )
    
    language_detected: str = Field(
        default="hi",
        description="Detected input language: 'hi' for Hindi, 'en' for English"
    )
    
    @validator('language_detected')
    def validate_language(cls, v):
        """Ensure language is either hi or en"""
        if v not in ['hi', 'en']:
            return 'hi'  # Default to Hindi
        return v
    
    @validator('entities')
    def validate_entities(cls, v):
        """Ensure entities is a dictionary"""
        if not isinstance(v, dict):
            return {}
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "intent": "market_price",
                "confidence": 0.95,
                "entities": {
                    "crop": "onion",
                    "location": "pune",
                    "quantity_unit": "quintal"
                },
                "reasoning": "User asked about onion market price in Pune",
                "language_detected": "hi"
            }
        }


class CardData(BaseModel):
    """Base schema for UI card data"""
    card_type: str = Field(
        ...,
        description="Type of card: crop_recommendation, market_price, government_scheme, etc."
    )
    data: Dict[str, Any] = Field(
        ...,
        description="Card-specific data payload"
    )


class VoiceAgentResponse(BaseModel):
    """
    Strict schema for final voice agent response
    This is what gets sent back to the frontend
    """
    session_id: str = Field(
        ...,
        description="Unique session identifier"
    )
    
    intent: Intent = Field(
        ...,
        description="Detected user intent"
    )
    
    intent_confidence: confloat(ge=0.0, le=1.0) = Field(
        ...,
        description="Confidence in intent classification"
    )
    
    cards: List[CardData] = Field(
        default_factory=list,
        description="List of UI cards to display"
    )
    
    explanation_hindi: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Hindi explanation for voice/text output"
    )
    
    explanation_english: Optional[str] = Field(
        None,
        max_length=2000,
        description="English translation (optional)"
    )
    
    reasoning: str = Field(
        default="",
        max_length=1000,
        description="Internal reasoning/debug info"
    )
    
    retrieved_sources: int = Field(
        default=0,
        ge=0,
        description="Number of knowledge sources retrieved"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata (context, timing, etc.)"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response generation timestamp"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_1737598234567",
                "intent": "market_price",
                "intent_confidence": 0.95,
                "cards": [
                    {
                        "card_type": "market_price",
                        "data": {
                            "crop_name": "Onion",
                            "current_price": 2500,
                            "current_price_formatted": "₹2,500",
                            "trend": "rising",
                            "trend_percentage": "+5.2",
                            "last_updated": "2 hours ago"
                        }
                    }
                ],
                "explanation_hindi": "पुणे मंडी में आज प्याज का भाव ₹2,500 प्रति क्विंटल है। पिछले हफ्ते से 5.2% बढ़ा है।",
                "explanation_english": "Today's onion price in Pune mandi is ₹2,500 per quintal. It has increased by 5.2% from last week.",
                "reasoning": "Fetched real-time data from mandi API",
                "retrieved_sources": 1,
                "metadata": {
                    "processing_time_ms": 1250,
                    "data_source": "mandi_api"
                },
                "timestamp": "2026-01-23T06:55:00Z"
            }
        }


class EntityExtractionSchema(BaseModel):
    """Schema for entity extraction from user query"""
    crop_name: Optional[str] = Field(None, description="Crop mentioned (e.g., onion, wheat)")
    amount: Optional[float] = Field(None, description="Numeric amount mentioned")
    currency: Optional[str] = Field(None, description="Currency (₹, rupees)")
    location: Optional[str] = Field(None, description="Location/city mentioned")
    date: Optional[str] = Field(None, description="Date mentioned")
    category: Optional[str] = Field(None, description="Category (seeds, fertilizer, labor, etc.)")
    season: Optional[str] = Field(None, description="Season (kharif, rabi, zaid)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "crop_name": "onion",
                "amount": 5000.0,
                "currency": "₹",
                "location": "pune",
                "category": "seeds",
                "season": "kharif"
            }
        }
