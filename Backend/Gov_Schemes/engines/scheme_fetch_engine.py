"""
Scheme Fetch Engine - API Sync and Caching
"""

from typing import List
from datetime import datetime

from ..models import SchemeRecord
from ..repositories import SchemeAPIClient, SchemeRepo


class SchemeFetchEngine:
    """Engine for fetching and caching schemes from API"""
    
    def __init__(self, api_client: SchemeAPIClient, scheme_repo: SchemeRepo):
        self.api_client = api_client
        self.scheme_repo = scheme_repo
    
    def sync_schemes(self, force_refresh: bool = False) -> List[SchemeRecord]:
        """
        Sync schemes from API to cache
        
        Args:
            force_refresh: Force refresh even if cache is recent
            
        Returns:
            List of all schemes after sync
        """
        # Check if we need to refresh
        should_refresh = force_refresh or self._should_refresh_cache()
        
        if should_refresh:
            # Fetch from API
            schemes = self.api_client.fetch_schemes()
            
            # Save to cache
            self.scheme_repo.save_schemes(schemes)
            
            return schemes
        else:
            # Return cached schemes
            return self.scheme_repo.get_all_schemes()
    
    def _should_refresh_cache(self) -> bool:
        """
        Determine if cache should be refreshed
        
        Returns:
            True if cache is stale or empty
        """
        last_sync = self.scheme_repo.get_last_sync_time()
        
        # No sync yet - need to refresh
        if last_sync is None:
            return True
        
        # Check if cache is stale (older than 24 hours)
        from ..config import get_settings
        settings = get_settings()
        
        hours_since_sync = (datetime.now() - last_sync).total_seconds() / 3600
        
        return hours_since_sync >= settings.cache_ttl_hours
    
    def get_cached_schemes(self) -> List[SchemeRecord]:
        """Get schemes from cache without API call"""
        return self.scheme_repo.get_all_schemes()
