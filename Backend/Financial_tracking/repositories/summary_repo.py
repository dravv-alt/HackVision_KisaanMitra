"""
Summary Repository - Dashboard Summary Storage
Caches computed financial summaries for performance
"""

from typing import Optional, Dict
from financial_tracking.models import FinanceTotals


class SummaryRepo:
    """
    Repository for caching financial summaries
    In production, this would store in MongoDB for dashboard optimization
    """

    def __init__(self):
        """Initialize with in-memory storage"""
        self._summaries: Dict[str, FinanceTotals] = {}

    def save_summary(self, totals: FinanceTotals) -> None:
        """
        Save/update a financial summary
        
        Args:
            totals: Financial totals to cache
        """
        # In production: db.financial_summaries.update_one(
        #     {"farmerId": totals.farmerId, "season": totals.season},
        #     {"$set": totals.dict()},
        #     upsert=True
        # )
        
        key = f"{totals.farmerId}_{totals.season}"
        self._summaries[key] = totals

    def get_summary(self, farmerId: str, season: str) -> Optional[FinanceTotals]:
        """
        Retrieve cached summary
        
        Args:
            farmerId: Farmer ID
            season: Season
            
        Returns:
            Cached summary if exists, None otherwise
        """
        # In production: db.financial_summaries.find_one({
        #     "farmerId": farmerId,
        #     "season": season
        # })
        
        key = f"{farmerId}_{season}"
        return self._summaries.get(key)

    def delete_summary(self, farmerId: str, season: str) -> bool:
        """Delete a cached summary"""
        key = f"{farmerId}_{season}"
        if key in self._summaries:
            del self._summaries[key]
            return True
        return False

    def list_summaries_for_farmer(self, farmerId: str) -> list[FinanceTotals]:
        """Get all summaries for a farmer across all seasons"""
        return [
            summary for key, summary in self._summaries.items()
            if summary.farmerId == farmerId
        ]
