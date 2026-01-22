"""
Scheme Repository - MongoDB Cache Abstraction
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
import uuid

from ..models import SchemeRecord
from ..constants import SchemeCategory


class SchemeRepo:
    """
    Repository for scheme data with MongoDB abstraction
    Provides caching and filtering capabilities
    """
    
    def __init__(self):
        # Mock in-memory storage (simulates MongoDB collection)
        self._mock_schemes: Dict[str, SchemeRecord] = {}
        self._last_sync: Optional[datetime] = None
    
    def get_all_schemes(self) -> List[SchemeRecord]:
        """Get all cached schemes"""
        return list(self._mock_schemes.values())
    
    def get_scheme_by_id(self, scheme_id: str) -> Optional[SchemeRecord]:
        """Get specific scheme by ID"""
        return self._mock_schemes.get(scheme_id)
    
    def filter_schemes(
        self,
        state: Optional[str] = None,
        district: Optional[str] = None,
        category: Optional[SchemeCategory] = None
    ) -> List[SchemeRecord]:
        """
        Filter schemes by location and category
        
        Args:
            state: Filter by state (None = all states)
            district: Filter by district (None = all districts)
            category: Filter by category (None = all categories)
            
        Returns:
            Filtered list of schemes
        """
        schemes = list(self._mock_schemes.values())
        
        # Filter by state
        if state:
            schemes = [
                s for s in schemes
                if s.state is None or s.state.lower() == state.lower()
            ]
        
        # Filter by district
        if district and state:
            schemes = [
                s for s in schemes
                if s.district is None or s.district.lower() == district.lower()
            ]
        
        # Filter by category
        if category:
            schemes = [s for s in schemes if s.category == category]
        
        # Only return active schemes
        schemes = [s for s in schemes if s.isActive]
        
        return schemes
    
    def save_schemes(self, schemes: List[SchemeRecord]) -> int:
        """
        Save/update schemes in cache
        
        Args:
            schemes: List of schemes to save
            
        Returns:
            Number of schemes saved
        """
        count = 0
        for scheme in schemes:
            scheme.updatedAt = datetime.now()
            self._mock_schemes[scheme.schemeId] = scheme
            count += 1
        
        self._last_sync = datetime.now()
        return count
    
    def get_new_schemes_since(self, since: datetime) -> List[SchemeRecord]:
        """
        Get schemes created after a specific datetime
        
        Args:
            since: Datetime to check against
            
        Returns:
            List of new schemes
        """
        return [
            s for s in self._mock_schemes.values()
            if s.createdAt > since
        ]
    
    def get_last_sync_time(self) -> Optional[datetime]:
        """Get last sync timestamp"""
        return self._last_sync
    
    def clear_cache(self):
        """Clear all cached schemes"""
        self._mock_schemes.clear()
        self._last_sync = None
