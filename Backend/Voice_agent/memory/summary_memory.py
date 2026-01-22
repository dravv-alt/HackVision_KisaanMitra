"""
Summary Memory - Rolling session summary
Maintains a condensed summary of the conversation
"""

from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SessionSummary:
    """Summary of a conversation session"""
    session_id: str
    farmer_id: str
    summary_text: str
    key_decisions: List[str]
    mentioned_crops: List[str]
    mentioned_locations: List[str]
    intents_covered: List[str]
    created_at: datetime
    updated_at: datetime


class SummaryMemory:
    """
    Rolling summary memory
    Maintains condensed summaries of conversations
    """
    
    def __init__(self):
        self._summaries: dict[str, SessionSummary] = {}
    
    def create_summary(
        self,
        session_id: str,
        farmer_id: str,
        conversation_turns: List[Any]
    ) -> SessionSummary:
        """
        Create or update session summary
        
        Args:
            session_id: Session identifier
            farmer_id: Farmer identifier
            conversation_turns: List of conversation turns
        
        Returns:
            Session summary
        """
        # Extract key information
        key_decisions = []
        mentioned_crops = set()
        mentioned_locations = set()
        intents_covered = set()
        
        for turn in conversation_turns:
            # Track intents
            intents_covered.add(turn.detected_intent.value)
            
            # Extract entities from metadata
            if "crops" in turn.metadata:
                mentioned_crops.update(turn.metadata["crops"])
            if "location" in turn.metadata:
                mentioned_locations.add(turn.metadata["location"])
            if "decision" in turn.metadata:
                key_decisions.append(turn.metadata["decision"])
        
        # Generate summary text
        summary_text = self._generate_summary_text(
            conversation_turns,
            list(intents_covered),
            list(mentioned_crops)
        )
        
        # Create summary
        now = datetime.now()
        summary = SessionSummary(
            session_id=session_id,
            farmer_id=farmer_id,
            summary_text=summary_text,
            key_decisions=key_decisions,
            mentioned_crops=list(mentioned_crops),
            mentioned_locations=list(mentioned_locations),
            intents_covered=list(intents_covered),
            created_at=now,
            updated_at=now
        )
        
        self._summaries[session_id] = summary
        return summary
    
    def get_summary(self, session_id: str) -> Optional[SessionSummary]:
        """Get session summary"""
        return self._summaries.get(session_id)
    
    def _generate_summary_text(
        self,
        turns: List[Any],
        intents: List[str],
        crops: List[str]
    ) -> str:
        """Generate human-readable summary text"""
        parts = []
        
        if len(turns) > 0:
            parts.append(f"Conversation with {len(turns)} turns")
        
        if intents:
            intent_str = ", ".join(intents[:3])
            parts.append(f"Topics: {intent_str}")
        
        if crops:
            crop_str = ", ".join(crops[:3])
            parts.append(f"Crops discussed: {crop_str}")
        
        return ". ".join(parts) if parts else "Empty conversation"


# Singleton instance
_summary_memory = None

def get_summary_memory() -> SummaryMemory:
    """Get or create summary memory instance"""
    global _summary_memory
    if _summary_memory is None:
        _summary_memory = SummaryMemory()
    return _summary_memory
