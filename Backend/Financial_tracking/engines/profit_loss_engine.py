"""
Profit/Loss Engine - Financial Report Generation
Builds comprehensive profit/loss reports with category breakdown
"""

from typing import List, Dict, Tuple
from collections import defaultdict
from Backend.Financial_tracking.models import (
    FinanceTransaction,
    FinanceTotals,
    ExpenseBreakdown,
)
from Backend.Financial_tracking.constants import (
    TransactionType,
    ExpenseCategory,
    EXPENSE_CATEGORY_NAMES,
)


class ProfitLossEngine:
    """
    Engine for profit/loss analysis and reporting
    """

    def build_profit_loss_report(
        self,
        transactions: List[FinanceTransaction],
        farmerId: str,
        season: str,
    ) -> Tuple[FinanceTotals, List[ExpenseBreakdown]]:
        """
        Build comprehensive P&L report with category breakdown
        
        Args:
            transactions: List of transactions
            farmerId: Farmer ID
            season: Season
            
        Returns:
            Tuple of (financial totals, expense breakdown list)
        """
        # Calculate totals
        total_expense = 0.0
        total_income = 0.0
        expense_by_category: Dict[str, float] = defaultdict(float)
        
        for tx in transactions:
            if tx.type == TransactionType.EXPENSE:
                total_expense += tx.amount
                expense_by_category[tx.category] += tx.amount
            elif tx.type == TransactionType.INCOME:
                total_income += tx.amount
        
        # Compute profit/loss
        profit_or_loss = total_income - total_expense
        profit_margin_pct = self.compute_profit_margin(total_income, total_expense)
        
        totals = FinanceTotals(
            farmerId=farmerId,
            season=season,
            totalExpense=round(total_expense, 2),
            totalIncome=round(total_income, 2),
            profitOrLoss=round(profit_or_loss, 2),
            profitMarginPct=profit_margin_pct,
        )
        
        # Build expense breakdown
        breakdown = self.categorize_expenses(expense_by_category, total_expense)
        
        return totals, breakdown

    def compute_profit_margin(self, total_income: float, total_expense: float) -> float:
        """
        Calculate profit margin percentage
        
        Args:
            total_income: Total income
            total_expense: Total expense
            
        Returns:
            Profit margin as percentage
        """
        if total_income <= 0:
            return 0.0
        
        profit = total_income - total_expense
        margin_pct = (profit / total_income) * 100
        
        return round(margin_pct, 2)

    def categorize_expenses(
        self,
        expense_by_category: Dict[str, float],
        total_expense: float,
    ) -> List[ExpenseBreakdown]:
        """
        Create expense breakdown by category with percentages
        
        Args:
            expense_by_category: Dictionary of category -> amount
            total_expense: Total expense amount
            
        Returns:
            List of expense breakdowns, sorted by amount (descending)
        """
        breakdowns = []
        
        for category, amount in expense_by_category.items():
            # Calculate percentage
            if total_expense > 0:
                percent = (amount / total_expense) * 100
            else:
                percent = 0.0
            
            # Get category names
            category_names = EXPENSE_CATEGORY_NAMES.get(
                ExpenseCategory(category),
                {"en": category, "hi": category}
            )
            
            breakdown = ExpenseBreakdown(
                category=category,
                amount=round(amount, 2),
                percent=round(percent, 2),
                categoryNameEn=category_names["en"],
                categoryNameHi=category_names["hi"],
            )
            
            breakdowns.append(breakdown)
        
        # Sort by amount descending
        breakdowns.sort(key=lambda x: x.amount, reverse=True)
        
        return breakdowns

    def get_top_expense_categories(
        self,
        breakdown: List[ExpenseBreakdown],
        top_n: int = 5,
    ) -> List[ExpenseBreakdown]:
        """
        Get top N expense categories
        
        Args:
            breakdown: Full expense breakdown
            top_n: Number of top categories to return
            
        Returns:
            Top N expense categories
        """
        return breakdown[:top_n]

    def calculate_cost_per_unit(
        self,
        total_expense: float,
        yield_quantity: float,
        unit: str = "quintal",
    ) -> float:
        """
        Calculate cost per unit of production
        
        Args:
            total_expense: Total production expense
            yield_quantity: Yield amount
            unit: Unit of measurement
            
        Returns:
            Cost per unit
        """
        if yield_quantity <= 0:
            return 0.0
        
        cost_per_unit = total_expense / yield_quantity
        return round(cost_per_unit, 2)

    def calculate_revenue_per_unit(
        self,
        total_income: float,
        yield_quantity: float,
        unit: str = "quintal",
    ) -> float:
        """
        Calculate revenue per unit
        
        Args:
            total_income: Total income from sales
            yield_quantity: Yield amount
            unit: Unit of measurement
            
        Returns:
            Revenue per unit
        """
        if yield_quantity <= 0:
            return 0.0
        
        revenue_per_unit = total_income / yield_quantity
        return round(revenue_per_unit, 2)
