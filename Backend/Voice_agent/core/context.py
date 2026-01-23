"""
Conversation Context Management
Tracks session state, farmer profile, and conversation history
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from Backend.Voice_agent.core.intent import Intent


@dataclass
class FarmerProfile:
    """Farmer profile information"""
    farmer_id: str
    name: Optional[str] = None
    location: Optional[tuple] = None  # (lat, lon)
    state: Optional[str] = None
    district: Optional[str] = None
    soil_type: Optional[str] = None
    land_size_acres: Optional[float] = None
    irrigation_type: Optional[str] = None
    language: str = "hindi"
    crops_grown: List[str] = field(default_factory=list)


@dataclass
class ConversationTurn:
    """Single conversation turn"""
    turn_id: int
    timestamp: datetime
    user_input_hindi: str
    user_input_english: str
    detected_intent: Intent
    agent_response_english: str
    agent_response_hindi: str
    cards_generated: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConversationContext:
    """
    Manages conversation context and state
    Tracks farmer profile, conversation history, and current state
    """
    
    def __init__(self, farmer_id: str, session_id: Optional[str] = None):
        """
        Initialize conversation context
        
        Args:
            farmer_id: Unique farmer identifier
            session_id: Optional session identifier
        """
        self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.farmer_profile = FarmerProfile(farmer_id=farmer_id)
        self.conversation_history: List[ConversationTurn] = []
        self.current_intent: Optional[Intent] = None
        self.pending_confirmation: Optional[Dict[str, Any]] = None
        self.context_variables: Dict[str, Any] = {}
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
    
    def update_farmer_profile(self, **kwargs):
        """Update farmer profile with new information"""
        for key, value in kwargs.items():
            if hasattr(self.farmer_profile, key):
                setattr(self.farmer_profile, key, value)
        self.last_updated = datetime.now()
    
    def add_turn(
        self,
        user_input_hindi: str,
        user_input_english: str,
        detected_intent: Intent,
        agent_response_english: str,
        agent_response_hindi: str,
        cards: List[Dict[str, Any]] = None,
        metadata: Dict[str, Any] = None
    ) -> ConversationTurn:
        """
        Add a new conversation turn
        
        Args:
            user_input_hindi: User input in Hindi
            user_input_english: Translated user input
            detected_intent: Detected intent
            agent_response_english: Agent response in English
            agent_response_hindi: Agent response in Hindi
            cards: Generated cards
            metadata: Additional metadata
        
        Returns:
            Created conversation turn
        """
        turn = ConversationTurn(
            turn_id=len(self.conversation_history) + 1,
            timestamp=datetime.now(),
            user_input_hindi=user_input_hindi,
            user_input_english=user_input_english,
            detected_intent=detected_intent,
            agent_response_english=agent_response_english,
            agent_response_hindi=agent_response_hindi,
            cards_generated=cards or [],
            metadata=metadata or {}
        )
        
        self.conversation_history.append(turn)
        self.current_intent = detected_intent
        self.last_updated = datetime.now()
        
        return turn
    
    def get_recent_turns(self, n: int = 5) -> List[ConversationTurn]:
        """Get last N conversation turns"""
        return self.conversation_history[-n:]
    
    def get_context_summary(self) -> str:
        """Get a summary of current context"""
        summary_parts = [
            f"Session: {self.session_id}",
            f"Farmer: {self.farmer_profile.farmer_id}",
            f"Turns: {len(self.conversation_history)}",
        ]
        
        if self.farmer_profile.location:
            summary_parts.append(f"Location: {self.farmer_profile.state}, {self.farmer_profile.district}")
        
        if self.current_intent:
            summary_parts.append(f"Current Intent: {self.current_intent.value}")
        
        return " | ".join(summary_parts)
    
    def set_context_variable(self, key: str, value: Any):
        """Set a context variable"""
        self.context_variables[key] = value
        self.last_updated = datetime.now()
    
    def get_context_variable(self, key: str, default: Any = None) -> Any:
        """Get a context variable"""
        return self.context_variables.get(key, default)
    
    def set_pending_confirmation(self, action: str, data: Dict[str, Any]):
        """Set a pending confirmation"""
        self.pending_confirmation = {
            "action": action,
            "data": data,
            "timestamp": datetime.now()
        }
    
    def clear_pending_confirmation(self):
        """Clear pending confirmation"""
        self.pending_confirmation = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary for storage"""
        return {
            "session_id": self.session_id,
            "farmer_id": self.farmer_profile.farmer_id,
            "farmer_profile": {
                "name": self.farmer_profile.name,
                "location": self.farmer_profile.location,
                "state": self.farmer_profile.state,
                "district": self.farmer_profile.district,
                "soil_type": self.farmer_profile.soil_type,
                "land_size_acres": self.farmer_profile.land_size_acres,
                "irrigation_type": self.farmer_profile.irrigation_type,
                "language": self.farmer_profile.language,
                "crops_grown": self.farmer_profile.crops_grown,
            },
            "conversation_history": [
                {
                    "turn_id": turn.turn_id,
                    "timestamp": turn.timestamp.isoformat(),
                    "user_input_hindi": turn.user_input_hindi,
                    "user_input_english": turn.user_input_english,
                    "detected_intent": turn.detected_intent.value,
                    "agent_response_english": turn.agent_response_english,
                    "agent_response_hindi": turn.agent_response_hindi,
                    "cards_generated": turn.cards_generated,
                    "metadata": turn.metadata,
                }
                for turn in self.conversation_history
            ],
            "current_intent": self.current_intent.value if self.current_intent else None,
            "pending_confirmation": self.pending_confirmation,
            "context_variables": self.context_variables,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
        }
