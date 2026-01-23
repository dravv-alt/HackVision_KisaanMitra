"""
Base Card - UI-ready data structure
All cards inherit from this base class
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime


@dataclass
class BaseCard:
    """
    Base card structure for UI display
    All specific cards inherit from this
    """
    card_type: str  # crop, weather, market, scheme, etc.
    title: str
    summary: str
    details: Dict[str, Any] = field(default_factory=dict)
    source: str = "voice_agent"
    confidence: float = 1.0
    deep_link: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary"""
        return {
            "card_type": self.card_type,
            "title": self.title,
            "summary": self.summary,
            "details": self.details,
            "source": self.source,
            "confidence": self.confidence,
            "deep_link": self.deep_link,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }
    
    def to_hindi_dict(self) -> Dict[str, Any]:
        """
        Convert card to Hindi dictionary
        Override in subclasses for proper Hindi translation
        """
        return self.to_dict()
