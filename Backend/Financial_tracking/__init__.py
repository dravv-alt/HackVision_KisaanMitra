"""
Financial Tracking Module
Backend module for farm financial tracking and profit/loss analysis
"""

from Backend.Financial_tracking.service import (
    FinanceTrackingService,
    get_finance_tracking_service,
)
from Backend.Financial_tracking.models import (
    FinanceTransaction,
    FinanceTotals,
    LossCause,
    OptimizationSuggestion,
    FinanceModuleOutput,
    FinanceCard,
)
from Backend.Financial_tracking.constants import (
    TransactionType,
    ExpenseCategory,
    IncomeCategory,
    SeasonType,
    UrgencyLevel,
    Currency,
)

__version__ = "1.0.0"

__all__ = [
    # Service
    "FinanceTrackingService",
    "get_finance_tracking_service",
    
    # Models
    "FinanceTransaction",
    "FinanceTotals",
    "LossCause",
    "OptimizationSuggestion",
    "FinanceModuleOutput",
    "FinanceCard",
    
    # Constants
    "TransactionType",
    "ExpenseCategory",
    "IncomeCategory",
    "SeasonType",
    "UrgencyLevel",
    "Currency",
]
