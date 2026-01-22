"""
Configuration Module - Centralized environment variable management
Loads from Backend/.env and provides config singleton
"""

import os
from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class VoiceAgentConfig:
    """Voice Agent configuration"""
    # LLM Provider
    llm_provider: str  # "gemini" or "groq"
    llm_api_key: str
    llm_model: Optional[str] = None
    
    # Whisper
    whisper_model: str = "base"
    
    # MongoDB
    mongodb_uri: Optional[str] = None
    mongodb_db_name: str = "farming_assistant"
    
    # Other APIs
    openweather_api_key: Optional[str] = None
    vision_ai_endpoint: Optional[str] = None
    market_api_key: Optional[str] = None
    mandi_api_key: Optional[str] = None


class ConfigManager:
    """Centralized configuration manager"""
    
    def __init__(self):
        self._config: Optional[VoiceAgentConfig] = None
        self._load_env()
    
    def _load_env(self):
        """Load environment variables from .env file"""
        # Find .env file in Backend directory
        current_dir = Path(__file__).resolve().parent
        backend_dir = current_dir.parent  # Go up to Backend/
        env_path = backend_dir / ".env"
        
        if env_path.exists():
            load_dotenv(env_path)
            print(f"✅ Loaded environment from: {env_path}")
        else:
            print(f"⚠️  Warning: .env file not found at {env_path}")
            print("   Using environment variables from system")
    
    def _detect_llm_provider(self) -> Tuple[str, str]:
        """
        Auto-detect LLM provider based on available API keys
        Priority: Gemini > Groq
        
        Returns:
            Tuple of (provider_name, api_key)
        """
        gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        groq_key = os.getenv("GROQ_API_KEY", "").strip()
        
        # Gemini takes precedence
        if gemini_key:
            print("✅ Using Gemini as LLM provider")
            return "gemini", gemini_key
        elif groq_key:
            print("✅ Using Groq as LLM provider")
            return "groq", groq_key
        else:
            raise ValueError(
                "No LLM API key found. Please set GEMINI_API_KEY or GROQ_API_KEY in Backend/.env"
            )
    
    def get_config(self) -> VoiceAgentConfig:
        """
        Get configuration singleton
        
        Returns:
            VoiceAgentConfig instance
        """
        if self._config is None:
            # Detect LLM provider
            llm_provider, llm_api_key = self._detect_llm_provider()
            
            # Create config
            self._config = VoiceAgentConfig(
                llm_provider=llm_provider,
                llm_api_key=llm_api_key,
                llm_model=None,  # Will use default for provider
                whisper_model=os.getenv("WHISPER_MODEL", "base"),
                mongodb_uri=os.getenv("MONGODB_URI"),
                mongodb_db_name=os.getenv("MONGODB_DB_NAME", "farming_assistant"),
                openweather_api_key=os.getenv("OPENWEATHER_API_KEY"),
                vision_ai_endpoint=os.getenv("VISION_AI_ENDPOINT"),
                market_api_key=os.getenv("MARKET_API_KEY"),
                mandi_api_key=os.getenv("MANDI_API_KEY"),
            )
            
            print(f"✅ Configuration loaded:")
            print(f"   LLM Provider: {self._config.llm_provider}")
            print(f"   Whisper Model: {self._config.whisper_model}")
            print(f"   MongoDB: {'Configured' if self._config.mongodb_uri else 'Not configured (using in-memory)'}")
        
        return self._config
    
    def reload(self):
        """Reload configuration (useful for testing)"""
        self._config = None
        self._load_env()


# Singleton instance
_config_manager = None

def get_config() -> VoiceAgentConfig:
    """
    Get configuration singleton
    
    Returns:
        VoiceAgentConfig instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager.get_config()


def reload_config():
    """Reload configuration from .env file"""
    global _config_manager
    if _config_manager is not None:
        _config_manager.reload()
