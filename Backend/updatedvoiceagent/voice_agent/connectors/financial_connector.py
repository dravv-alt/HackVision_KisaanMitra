"""
Financial Tracking Connector
Bridges voice agent with financial tracking backend module
"""

import sys
from pathlib import Path

# Add Backend to path for imports
backend_dir = Path(__file__).resolve().parent.parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from typing import Dict, Any, List, Optional
from financial_tracking import get_finance_tracking_service
from financial_tracking.constants import SeasonType, ExpenseCategory, IncomeCategory


class FinancialTrackingConnector:
    """Connector for financial tracking module"""
    
    def __init__(self):
        self.service = get_finance_tracking_service()
    
    def get_finance_report(
        self,
        farmer_id: str,
        season: str = SeasonType.KHARIF.value,
        language: str = "hi"
    ) -> Dict[str, Any]:
        """Get complete financial report"""
        output = self.service.run_finance_report(
            farmerId=farmer_id,
            season=season,
            language=language
        )
        
        return {
            "speech_text": output.speechText,
            "totals": output.totals,
            "loss_causes": output.lossCauses,
            "suggestions": output.suggestions,
            "urgency": output.urgencyLevel,
            "expense_breakdown": output.topExpenseCategories,
            "reasoning": output.detailedReasoning
        }
    
    def add_expense(
        self,
        farmer_id: str,
        category: str,
        amount: float,
        season: str = SeasonType.KHARIF.value,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Record an expense"""
        result = self.service.add_expense(
            farmerId=farmer_id,
            season=season,
            category=category,
            amount=amount,
            notes=notes
        )
        
        return {
            "success": result.get("success", False),
            "message": result.get("message", ""),
            "transaction_id": result.get("transactionId")
        }
    
    def add_income(
        self,
        farmer_id: str,
        category: str,
        amount: float,
        season: str = SeasonType.KHARIF.value,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Record income"""
        result = self.service.add_income(
            farmerId=farmer_id,
            season=season,
            category=category,
            amount=amount,
            notes=notes
        )
        
        return {
            "success": result.get("success", False),
            "message": result.get("message", ""),
            "transaction_id": result.get("transactionId")
        }


# Singleton
_connector = None

def get_financial_connector() -> FinancialTrackingConnector:
    """Get or create financial tracking connector"""
    global _connector
    if _connector is None:
        _connector = FinancialTrackingConnector()
    return _connector
