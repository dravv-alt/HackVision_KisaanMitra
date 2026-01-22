"""
Prioritization Engine - Importance Ranking
"""

from typing import List
from ..models import AlertRecord
from ..constants import AlertUrgency


class PrioritizationEngine:
    def rank(self, alerts: List[AlertRecord]) -> List[AlertRecord]:
        """
        Rank alerts based on urgency score and scheduled time.
        Critical warnings (Heatwave, Price crash) float to top.
        """
        # Map urgency to score for sorting
        scores = {
            AlertUrgency.CRITICAL: 100,
            AlertUrgency.HIGH: 80,
            AlertUrgency.MEDIUM: 40,
            AlertUrgency.LOW: 10
        }
        
        # Sort by urgency score (desc) then by scheduledAt (asc)
        ranked = sorted(
            alerts, 
            key=lambda x: (-scores.get(x.urgency, 0), x.scheduledAt)
        )
        return ranked
