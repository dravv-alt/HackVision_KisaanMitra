"""
Voice Agent Module - Voice-First Agentic Orchestration Layer
Processes Hindi voice input, detects intent, retrieves information,
reasons about recommendations, and generates UI-ready cards.
"""

from Voice_agent.core.agent import VoiceAgent
from Voice_agent.core.intent import LLMIntentClassifier, Intent
from Voice_agent.cards.base_card import BaseCard

__version__ = "1.0.0"

__all__ = [
    "VoiceAgent",
    "LLMIntentClassifier",
    "Intent",
    "BaseCard",
]
