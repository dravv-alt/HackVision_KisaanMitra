"""
Financial Tracking Data Models
Pydantic schemas for type-safe data handling
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from Backend.Financial_tracking.constants import (
    TransactionType,
    ExpenseCategory,
    IncomeCategory,
    SeasonType,
    UrgencyLevel,
    Currency,
)


class FinanceTransaction(BaseModel):
    """
    Ledger entry for farm financial transaction
    """
    transactionId: str
    farmerId: str
    relatedCropId: Optional[str] = None
    season: str
    type: TransactionType
    category: str  # ExpenseCategory or IncomeCategory value
    amount: float = Field(gt=0, description="Amount must be positive")
    currency: str = Currency.INR.value
    notes: Optional[str] = None
    ts: datetime  # Transaction timestamp
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than zero")
        return round(v, 2)

    class Config:
        use_enum_values = True


class FinanceTotals(BaseModel):
    """
    Aggregated financial summary
    """
    farmerId: str
    season: str
    totalExpense: float = 0.0
    totalIncome: float = 0.0
    profitOrLoss: float = 0.0
    profitMarginPct: float = 0.0

    @validator('totalExpense', 'totalIncome', 'profitOrLoss', 'profitMarginPct')
    def round_amounts(cls, v):
        return round(v, 2)


class ExpenseBreakdown(BaseModel):
    """
    Expense breakdown by category
    """
    category: str
    amount: float
    percent: float
    categoryNameEn: str
    categoryNameHi: str


class LossCause(BaseModel):
    """
    Identified cause of financial loss
    """
    title: str
    description: str
    impactAmount: float
    confidenceScore: float = Field(ge=0.0, le=1.0, description="Confidence between 0 and 1")

    @validator('confidenceScore')
    def round_confidence(cls, v):
        return round(v, 2)


class OptimizationSuggestion(BaseModel):
    """
    Actionable suggestion for improving profit margin
    """
    suggestionTitle: str
    whyThisHelps: str
    estimatedSavings: float
    priority: int = Field(ge=1, le=5, description="Priority from 1 (highest) to 5 (lowest)")
    actionableSteps: List[str]


class FinanceModuleOutput(BaseModel):
    """
    Complete output from financial tracking module
    Ready for voice agent and UI consumption
    """
    header: str
    language: str
    speechText: str
    totals: FinanceTotals
    topExpenseCategories: List[ExpenseBreakdown]
    lossCauses: List[LossCause]
    suggestions: List[OptimizationSuggestion]
    detailedReasoning: str
    urgencyLevel: UrgencyLevel

    class Config:
        use_enum_values = True


class FinanceCard(BaseModel):
    """
    Card structure compatible with voice_agent BaseCard
    """
    card_type: str = "finance"
    title: str
    summary: str
    details: Dict[str, Any]
    source: str = "financial_tracking"
    confidence: float = 1.0
    deep_link: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary"""
        return {
            "card_type": self.card_type,
            "title": self.title,
            "summary": self.summary,
            "details": self.details,
            "source": self.source,
            "confidence": self.confidence,
            "deep_link": self.deep_link,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }
