"""
Scheme Filter Engine - Location and Category Filtering
"""

from typing import List, Optional

from ..models import SchemeRecord, FarmerProfile
from ..constants import SchemeCategory
from ..repositories import SchemeRepo


class SchemeFilterEngine:
    """Engine for filtering schemes by location and category"""
    
    def __init__(self, scheme_repo: SchemeRepo):
        self.scheme_repo = scheme_repo
    
    def filter_for_farmer(
        self,
        farmer: FarmerProfile,
        category: Optional[SchemeCategory] = None
    ) -> List[SchemeRecord]:
        """
        Filter schemes relevant to a farmer
        
        Args:
            farmer: Farmer profile with location
            category: Optional category filter
            
        Returns:
            Filtered list of schemes
        """
        return self.scheme_repo.filter_schemes(
            state=farmer.state,
            district=farmer.district,
            category=category
        )
    
    def filter_by_location(
        self,
        state: Optional[str] = None,
        district: Optional[str] = None,
        category: Optional[SchemeCategory] = None
    ) -> List[SchemeRecord]:
        """
        Filter schemes by location and category
        
        Args:
            state: State name
            district: District name
            category: Scheme category
            
        Returns:
            Filtered list of schemes
        """
        return self.scheme_repo.filter_schemes(
            state=state,
            district=district,
            category=category
        )
    
    def get_all_active_schemes(self) -> List[SchemeRecord]:
        """Get all active schemes without filters"""
        return self.scheme_repo.filter_schemes()
    
    def group_by_category(
        self,
        schemes: List[SchemeRecord]
    ) -> dict:
        """
        Group schemes by category
        
        Args:
            schemes: List of schemes
            
        Returns:
            Dictionary with category as key and list of schemes as value
        """
        grouped = {}
        for scheme in schemes:
            category = scheme.category
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(scheme)
        
        return grouped
    
    def sort_schemes(
        self,
        schemes: List[SchemeRecord],
        sort_by: str = "relevance"
    ) -> List[SchemeRecord]:
        """
        Sort schemes by various criteria
        
        Args:
            schemes: List of schemes
            sort_by: "relevance", "newest", "ending_soon"
            
        Returns:
            Sorted list of schemes
        """
        if sort_by == "newest":
            return sorted(schemes, key=lambda s: s.createdAt, reverse=True)
        elif sort_by == "ending_soon":
            # Schemes with end dates first, sorted by end date
            with_end = [s for s in schemes if s.endDate is not None]
            without_end = [s for s in schemes if s.endDate is None]
            with_end_sorted = sorted(with_end, key=lambda s: s.endDate)
            return with_end_sorted + without_end
        else:  # relevance
            # District-specific first, then state-wide, then all-India
            district_schemes = [s for s in schemes if s.district is not None]
            state_schemes = [s for s in schemes if s.district is None and s.state is not None]
            all_india = [s for s in schemes if s.state is None]
            
            return district_schemes + state_schemes + all_india
