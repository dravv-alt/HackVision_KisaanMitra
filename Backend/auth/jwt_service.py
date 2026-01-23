"""
JWT Token Service
Handles JWT token generation and validation
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt
from dotenv import load_dotenv

load_dotenv()

class JWTService:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "default_secret_key_change_in_production")
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.expiration_hours = int(os.getenv("JWT_EXPIRATION_HOURS", "720"))  # 30 days default
    
    def create_access_token(self, user_data: Dict) -> str:
        """
        Create JWT access token
        
        Args:
            user_data: Dictionary containing user information
                      (user_id, phone_number, farmer_id, etc.)
        
        Returns:
            JWT token string
        """
        # Create payload
        payload = {
            **user_data,
            "exp": datetime.utcnow() + timedelta(hours=self.expiration_hours),
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        # Generate token
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify and decode JWT token
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded payload if valid, None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def refresh_token(self, token: str) -> Optional[str]:
        """
        Refresh an existing token
        
        Args:
            token: Current JWT token
        
        Returns:
            New JWT token if valid, None if invalid
        """
        payload = self.verify_token(token)
        if payload:
            # Remove exp and iat from old payload
            payload.pop('exp', None)
            payload.pop('iat', None)
            payload.pop('type', None)
            
            # Create new token
            return self.create_access_token(payload)
        return None

# Singleton instance
_jwt_service = None

def get_jwt_service() -> JWTService:
    """Get singleton instance of JWTService"""
    global _jwt_service
    if _jwt_service is None:
        _jwt_service = JWTService()
    return _jwt_service
