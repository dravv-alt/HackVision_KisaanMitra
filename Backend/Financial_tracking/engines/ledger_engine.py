"""
Ledger Engine - Transaction Recording and Computation
Handles recording and validating financial transactions
"""

from typing import List
from datetime import datetime
import uuid
from Backend.Financial_tracking.models import FinanceTransaction, FinanceTotals
from Backend.Financial_tracking.constants import TransactionType, ExpenseCategory, IncomeCategory


class LedgerEngine:
    """
    Core engine for ledger operations
    Validates, records, and computes financial totals
    """

    def record_expense(
        self,
        farmerId: str,
        season: str,
        category: str,
        amount: float,
        notes: str = None,
        relatedCropId: str = None,
    ) -> FinanceTransaction:
        """
        Record an expense transaction
        
        Args:
            farmerId: Farmer ID
            season: Season
            category: Expense category
            amount: Expense amount
            notes: Optional notes
            relatedCropId: Optional crop ID
            
        Returns:
            Created transaction
            
        Raises:
            ValueError: If validation fails
        """
        # Validate category
        try:
            ExpenseCategory(category)
        except ValueError:
            raise ValueError(f"Invalid expense category: {category}")
        
        # Validate amount
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        
        # Create transaction
        transaction = FinanceTransaction(
            transactionId=str(uuid.uuid4()),
            farmerId=farmerId,
            relatedCropId=relatedCropId,
            season=season,
            type=TransactionType.EXPENSE,
            category=category,
            amount=amount,
            notes=notes,
            ts=datetime.now(),
        )
        
        return transaction

    def record_income(
        self,
        farmerId: str,
        season: str,
        category: str,
        amount: float,
        notes: str = None,
        relatedCropId: str = None,
    ) -> FinanceTransaction:
        """
        Record an income transaction
        
        Args:
            farmerId: Farmer ID
            season: Season
            category: Income category
            amount: Income amount
            notes: Optional notes
            relatedCropId: Optional crop ID
            
        Returns:
            Created transaction
            
        Raises:
            ValueError: If validation fails
        """
        # Validate category
        try:
            IncomeCategory(category)
        except ValueError:
            raise ValueError(f"Invalid income category: {category}")
        
        # Validate amount
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        
        # Create transaction
        transaction = FinanceTransaction(
            transactionId=str(uuid.uuid4()),
            farmerId=farmerId,
            relatedCropId=relatedCropId,
            season=season,
            type=TransactionType.INCOME,
            category=category,
            amount=amount,
            notes=notes,
            ts=datetime.now(),
        )
        
        return transaction

    def compute_totals(
        self, 
        transactions: List[FinanceTransaction],
        farmerId: str,
        season: str,
    ) -> FinanceTotals:
        """
        Compute financial totals from transactions
        
        Args:
            transactions: List of transactions
            farmerId: Farmer ID
            season: Season
            
        Returns:
            Financial totals with profit/loss and margin
        """
        total_expense = 0.0
        total_income = 0.0
        
        for tx in transactions:
            if tx.type == TransactionType.EXPENSE:
                total_expense += tx.amount
            elif tx.type == TransactionType.INCOME:
                total_income += tx.amount
        
        # Round to 2 decimal places
        total_expense = round(total_expense, 2)
        total_income = round(total_income, 2)
        
        # Calculate profit/loss
        profit_or_loss = round(total_income - total_expense, 2)
        
        # Calculate profit margin percentage
        if total_income > 0:
            profit_margin_pct = round((profit_or_loss / total_income) * 100, 2)
        else:
            profit_margin_pct = 0.0
        
        return FinanceTotals(
            farmerId=farmerId,
            season=season,
            totalExpense=total_expense,
            totalIncome=total_income,
            profitOrLoss=profit_or_loss,
            profitMarginPct=profit_margin_pct,
        )

    def validate_transaction(self, tx: FinanceTransaction) -> bool:
        """
        Validate a transaction
        
        Args:
            tx: Transaction to validate
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If validation fails
        """
        if tx.amount <= 0:
            raise ValueError("Transaction amount must be positive")
        
        if not tx.farmerId:
            raise ValueError("Farmer ID is required")
        
        if not tx.season:
            raise ValueError("Season is required")
        
        if not tx.ts:
            raise ValueError("Transaction timestamp is required")
        
        return True
