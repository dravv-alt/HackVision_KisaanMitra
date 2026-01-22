"""
Scheme Repository with Mock Fallback
"""

from typing import List
from datetime import datetime, timedelta
from ..models import SchemeContext


class SchemeRepo:
    def __init__(self):
        self._mock_schemes: List[SchemeContext] = []
        self.seed_mock_schemes_if_empty()

    def list_schemes(self) -> List[SchemeContext]:
        return self._mock_schemes

    def list_new_schemes(self, since_datetime: datetime) -> List[SchemeContext]:
        """Fetch schemes created after a specific timestamp"""
        return [s for s in self._mock_schemes if s.createdAt > since_datetime]

    def seed_mock_schemes_if_empty(self):
        now = datetime.now()
        self._mock_schemes.append(SchemeContext(
            schemeKey="SCH001",
            schemeName="Maharashtra Solar Pump Subsidy",
            category="Subsidy",
            stateEligible=["Maharashtra"],
            createdAt=now - timedelta(hours=5) # New
        ))
        self._mock_schemes.append(SchemeContext(
            schemeKey="SCH002",
            schemeName="Pradhan Mantri Fasal Bima Yojana",
            category="Insurance",
            stateEligible=["All"],
            createdAt=now - timedelta(days=200) # Old
        ))
