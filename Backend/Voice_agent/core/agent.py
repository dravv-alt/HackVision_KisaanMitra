"""
Voice Agent - Main Orchestrator
Coordinates all components for voice-first farming assistant
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

from Backend.Voice_agent.input_processing import get_translator, get_speech_to_text
from Backend.Voice_agent.core.intent import get_intent_classifier, Intent
from Backend.Voice_agent.core.context import ConversationContext
from Backend.Voice_agent.memory import get_session_memory
from Backend.Voice_agent.retrieval import get_retriever
from Backend.Voice_agent.reasoning import get_reasoning_planner, get_synthesizer
from Backend.Voice_agent.explain import get_explanation_builder
from Backend.Voice_agent.cards import BaseCard


@dataclass
class AgentResponse:
    """Voice agent response"""
    session_id: str
    intent: Intent
    intent_confidence: float
    cards: List[BaseCard]
    explanation_hindi: str
    explanation_english: str
    reasoning: str
    retrieved_sources: int
    timestamp: datetime
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "session_id": self.session_id,
            "intent": self.intent.value,
            "intent_confidence": self.intent_confidence,
            "cards": [card.to_dict() for card in self.cards],
            "explanation_hindi": self.explanation_hindi,
            "explanation_english": self.explanation_english,
            "reasoning": self.reasoning,
            "retrieved_sources": self.retrieved_sources,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


class VoiceAgent:
    """
    Main Voice Agent Orchestrator
    Coordinates all components for voice-first interaction
    """
    
    def __init__(self, db_client=None):
        """
        Initialize Voice Agent with Llama 2 Classifier
        
        Args:
            db_client: MongoDB client (optional, auto-configured from .env)
        """
        # Load config
        from Backend.Voice_agent.config import get_config
        config = get_config()
        
        # Initialize components
        self.translator = get_translator()
        self.stt = get_speech_to_text()  # Uses config for Whisper model
        
        # NEW: Use Llama 2 Intent Classifier with Pydantic schemas
        from voice_agent.core.llama_classifier import get_llama2_classifier
        try:
            self.intent_classifier = get_llama2_classifier()
            print("✅ Voice Agent using Llama 3.1 8B classifier (lightweight & fast)")
        except Exception as e:
            print(f"⚠️  Llama 2 classifier init failed: {e}")
            print("   Falling back to legacy classifier")
            from voice_agent.core.intent import get_intent_classifier
            self.intent_classifier = get_intent_classifier()
        
        # MongoDB - use provided client or try to connect from config
        if db_client is None and config.mongodb_uri:
            try:
                from pymongo import MongoClient
                # Set a short timeout for the initial connection check
                temp_client = MongoClient(config.mongodb_uri, serverSelectionTimeoutMS=2000)
                # Verify connection
                temp_client.admin.command('ping')
                
                db_client = temp_client[config.mongodb_db_name]
                print(f"✅ Connected to MongoDB: {config.mongodb_db_name}")
            except Exception as e:
                print(f"⚠️  MongoDB connection failed (Server unreachable): {e}")
                print("   Using in-memory storage")
                db_client = None
        
        self.session_memory = get_session_memory(db_client)
        self.retriever = get_retriever()
        self.reasoning_planner = get_reasoning_planner()
        self.synthesizer = get_synthesizer()
        self.explanation_builder = get_explanation_builder()
        
        # Active contexts
        self._active_contexts: Dict[str, ConversationContext] = {}
    
    def process_input(
        self,
        hindi_text: str,
        farmer_id: str = "F001",
        session_id: Optional[str] = None
    ) -> AgentResponse:
        """
        Process Hindi voice input (main entry point)
        
        Args:
            hindi_text: Hindi text input (from voice or text)
            farmer_id: Farmer identifier
            session_id: Optional session ID
        
        Returns:
            Agent response with cards and explanation
        """
        # Step 1: Get or create conversation context
        context = self._get_or_create_context(farmer_id, session_id)
        
        # Step 2: Translate Hindi to English
        english_text = self.translator.hindi_to_english(hindi_text)
        
        # Step 3: Detect intent
        intent_result = self.intent_classifier.classify(english_text)
        intent = intent_result.intent
        confidence = intent_result.confidence
        
        if intent_result.entities:
            context.update_from_dict(intent_result.entities)
        
        # Step 4: Create reasoning plan
        reasoning_plan = self.reasoning_planner.create_plan(intent)
        
        # Step 5: Retrieve relevant information
        retrieved_docs = self.retriever.retrieve(
            intent=intent,
            query_text=english_text,
            context=context.to_dict()
        )
        
        # Step 6: Synthesize information into cards
        synth_context = context.to_dict()
        # Flatten context variables for easier access in synthesizer
        synth_context.update(context.context_variables)
        
        synthesis_result = self.synthesizer.synthesize(
            intent=intent,
            retrieved_docs=retrieved_docs,
            context=synth_context
        )
        
        cards = synthesis_result["cards"]
        reasoning = synthesis_result["reasoning"]
        
        # Step 7: Build explanation
        explanation_english = self.explanation_builder.build_explanation(
            intent=intent,
            cards=cards,
            reasoning=reasoning,
            language="english"
        )
        
        explanation_hindi = self.explanation_builder.build_explanation(
            intent=intent,
            cards=cards,
            reasoning=reasoning,
            language="hindi"
        )
        
        # Step 8: Update conversation context
        context.add_turn(
            user_input_hindi=hindi_text,
            user_input_english=english_text,
            detected_intent=intent,
            agent_response_english=explanation_english,
            agent_response_hindi=explanation_hindi,
            cards=[card.to_dict() for card in cards],
            metadata={
                "intent_confidence": confidence,
                "retrieved_sources": len(retrieved_docs),
                "reasoning_plan": reasoning_plan.output_format,
            }
        )
        
        # Step 9: Save context to memory
        self.session_memory.save_context(context)
        
        # Step 9b: Ingest turn into Vector RAG (Dynamic Memory)
        try:
            from voice_agent.retrieval.vector_store import get_vector_store
            vector_store = get_vector_store()
            
            # Get the latest turn we just added
            latest_turn = context.conversation_history[-1]
            
            turn_data = {
                "turn_id": latest_turn.turn_id,
                "timestamp": latest_turn.timestamp.isoformat(),
                "user_input_english": latest_turn.user_input_english,
                "agent_response_english": latest_turn.agent_response_english,
                "intent": latest_turn.detected_intent.value
            }
            vector_store.ingest_conversation_turn(turn_data)
        except Exception as e:
            print(f"⚠️  Failed to ingest turn into VectorDB: {e}")
        
        # Step 10: Build response
        response = AgentResponse(
            session_id=context.session_id,
            intent=intent,
            intent_confidence=confidence,
            cards=cards,
            explanation_hindi=explanation_hindi,
            explanation_english=explanation_english,
            reasoning=reasoning,
            retrieved_sources=len(retrieved_docs),
            timestamp=datetime.now(),
            metadata={
                "reasoning": intent_result.reasoning,
                "factors_considered": reasoning_plan.factors_to_consider,
                "user_input_english": english_text,
            }
        )
        
        return response
    
    def _get_or_create_context(
        self,
        farmer_id: str,
        session_id: Optional[str] = None
    ) -> ConversationContext:
        """Get existing or create new conversation context"""
        
        # Try to load from session ID
        if session_id:
            context = self.session_memory.load_context(session_id)
            if context:
                self._active_contexts[session_id] = context
                return context
        
        # Try to get from active contexts
        if session_id and session_id in self._active_contexts:
            return self._active_contexts[session_id]
        
        # Create new context
        context = ConversationContext(farmer_id=farmer_id, session_id=session_id)
        self._active_contexts[context.session_id] = context
        
        return context
    
    def get_session_history(self, session_id: str) -> Optional[ConversationContext]:
        """Get session history"""
        return self.session_memory.load_context(session_id)
    
    def clear_session(self, session_id: str):
        """Clear a session"""
        self.session_memory.delete_session(session_id)
        self._active_contexts.pop(session_id, None)


# Singleton instance
_agent = None

def get_voice_agent(db_client=None) -> VoiceAgent:
    """Get or create voice agent instance"""
    global _agent
    if _agent is None:
        _agent = VoiceAgent(db_client=db_client)
    return _agent
