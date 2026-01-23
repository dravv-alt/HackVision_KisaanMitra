"""
Settings Configuration with .env Support
Safely loads configuration from environment variables and .env file
Never crashes if .env is missing
"""

import os
from typing import Optional
from pathlib import Path


class Settings:
    """
    Application settings with safe defaults
    Loads from environment variables and .env file if present
    """
    
    def __init__(self):
        # Try to load .env file if it exists (but don't crash if missing)
        self._load_env_file()
        
        # Load settings with safe defaults
        self.api_base_url: str = os.getenv("GOV_SCHEME_API_BASE_URL", "mock")
        self.api_token: Optional[str] = os.getenv("GOV_SCHEME_API_TOKEN")
        self.env_mode: str = os.getenv("ENV_MODE", "dev")
        self.mock_mode: bool = os.getenv("MOCK_MODE", "true").lower() in ("true", "1", "yes")
        
        # Additional settings
        self.api_timeout: int = int(os.getenv("API_TIMEOUT", "10"))
        self.cache_ttl_hours: int = int(os.getenv("CACHE_TTL_HOURS", "24"))
        
        # Data.gov.in specific
        self.schemes_api_key: Optional[str] = os.getenv("SCHEMES_API_KEY")
        self.schemes_resource_id: Optional[str] = os.getenv("SCHEMES_RESOURCE_ID")
    
    def _load_env_file(self):
        """
        Load .env file if it exists
        Uses simple key=value parsing (no external dependencies)
        """
        # Look for .env in the gov_schemes directory
        env_path = Path(__file__).parent.parent / ".env"
        
        if not env_path.exists():
            # No .env file - that's okay, use environment variables or defaults
            return
        
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse key=value
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        
                        # Only set if not already in environment
                        if key not in os.environ:
                            os.environ[key] = value
        except Exception:
            # If .env file is malformed, just continue with defaults
            pass
    
    def is_mock_mode(self) -> bool:
        """Check if running in mock mode"""
        return self.mock_mode
    
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.env_mode.lower() == "prod"
    
    def __repr__(self) -> str:
        return (
            f"Settings(api_base_url='{self.api_base_url}', "
            f"env_mode='{self.env_mode}', mock_mode={self.mock_mode})"
        )


# Singleton instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get settings singleton instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
