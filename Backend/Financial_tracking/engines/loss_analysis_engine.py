"""
Loss Analysis Engine - Identifies Causes of Financial Loss
Analyzes transaction patterns to detect waste and inefficiency
"""

from typing import List, Dict
from collections import defaultdict
from financial_tracking.models import (
    FinanceTransaction,
    FinanceTotals,
    ExpenseBreakdown,
    LossCause,
)
from financial_tracking.constants import (
    TransactionType,
    ExpenseCategory,
)


class LossAnalysisEngine:
    """
    Analyzes financial data to identify causes of loss
    """

    def identify_loss_causes(
        self,
        transactions: List[FinanceTransaction],
        totals: FinanceTotals,
        expense_breakdown: List[ExpenseBreakdown],
    ) -> List[LossCause]:
        """
        Identify and rank causes of financial loss
        
        Args:
            transactions: All transactions
            totals: Financial totals
            expense_breakdown: Expense category breakdown
            
        Returns:
            List of identified loss causes with impact
        """
        causes: List[LossCause] = []
        
        # Only analyze if there's a loss
        if totals.profitOrLoss >= 0:
            # Even if profitable, check for inefficiencies
            causes.extend(self._check_inefficiencies(transactions, totals, expense_breakdown))
        else:
            # Analyze loss causes
            causes.extend(self._analyze_primary_loss_causes(
                transactions, totals, expense_breakdown
            ))
        
        # Sort by impact amount (descending)
        causes.sort(key=lambda x: x.impactAmount, reverse=True)
        
        return causes

    def _analyze_primary_loss_causes(
        self,
        transactions: List[FinanceTransaction],
        totals: FinanceTotals,
        expense_breakdown: List[ExpenseBreakdown],
    ) -> List[LossCause]:
        """Analyze primary causes when there is a loss"""
        causes = []
        
        # Check for low revenue
        if totals.totalIncome < totals.totalExpense * 0.8:
            causes.append(LossCause(
                title="Low Selling Price / Late Selling",
                description="Your selling income is significantly lower than production costs. This could be due to selling at low mandi prices or selling at the wrong time.",
                impactAmount=abs(totals.profitOrLoss) * 0.5,
                confidenceScore=0.85,
            ))
        
        # Check for high transport costs
        transport_breakdown = next(
            (b for b in expense_breakdown if b.category == ExpenseCategory.TRANSPORT.value),
            None
        )
        if transport_breakdown and transport_breakdown.percent > 15:
            causes.append(LossCause(
                title="High Transport Costs",
                description=f"Transport expenses are {transport_breakdown.percent:.1f}% of total costs (₹{transport_breakdown.amount:.0f}). Consider selling at nearer mandi or bulk transport.",
                impactAmount=transport_breakdown.amount * 0.3,
                confidenceScore=0.90,
            ))
        
        # Check for excessive labour costs
        labour_breakdown = next(
            (b for b in expense_breakdown if b.category == ExpenseCategory.LABOUR.value),
            None
        )
        if labour_breakdown and labour_breakdown.percent > 35:
            causes.append(LossCause(
                title="High Labour Costs",
                description=f"Labour expenses are {labour_breakdown.percent:.1f}% of total costs (₹{labour_breakdown.amount:.0f}). Consider mechanization or efficient labour management.",
                impactAmount=labour_breakdown.amount * 0.15,
                confidenceScore=0.75,
            ))
        
        # Check for high fertilizer costs
        fertilizer_breakdown = next(
            (b for b in expense_breakdown if b.category == ExpenseCategory.FERTILIZER.value),
            None
        )
        if fertilizer_breakdown and fertilizer_breakdown.percent > 25:
            causes.append(LossCause(
                title="Excessive Fertilizer Use",
                description=f"Fertilizer costs are {fertilizer_breakdown.percent:.1f}% of expenses (₹{fertilizer_breakdown.amount:.0f}). Over-application wastes money and may harm soil.",
                impactAmount=fertilizer_breakdown.amount * 0.2,
                confidenceScore=0.70,
            ))
        
        # Check for high pesticide costs
        pesticide_breakdown = next(
            (b for b in expense_breakdown if b.category == ExpenseCategory.PESTICIDE.value),
            None
        )
        if pesticide_breakdown and pesticide_breakdown.percent > 12:
            causes.append(LossCause(
                title="High Pesticide Expenses",
                description=f"Pesticide costs are {pesticide_breakdown.percent:.1f}% of total (₹{pesticide_breakdown.amount:.0f}). Consider integrated pest management (IPM).",
                impactAmount=pesticide_breakdown.amount * 0.25,
                confidenceScore=0.68,
            ))
        
        # Check for high electricity/water costs (irrigation inefficiency)
        water_breakdown = next(
            (b for b in expense_breakdown if b.category == ExpenseCategory.WATER.value),
            None
        )
        electricity_breakdown = next(
            (b for b in expense_breakdown if b.category == ExpenseCategory.ELECTRICITY.value),
            None
        )
        
        irrigation_cost = 0.0
        if water_breakdown:
            irrigation_cost += water_breakdown.amount
        if electricity_breakdown:
            irrigation_cost += electricity_breakdown.amount
        
        irrigation_percent = (irrigation_cost / totals.totalExpense * 100) if totals.totalExpense > 0 else 0
        
        if irrigation_percent > 20:
            causes.append(LossCause(
                title="High Irrigation Costs",
                description=f"Water and electricity costs are {irrigation_percent:.1f}% of expenses (₹{irrigation_cost:.0f}). Consider drip irrigation or better water management.",
                impactAmount=irrigation_cost * 0.3,
                confidenceScore=0.72,
            ))
        
        return causes

    def _check_inefficiencies(
        self,
        transactions: List[FinanceTransaction],
        totals: FinanceTotals,
        expense_breakdown: List[ExpenseBreakdown],
    ) -> List[LossCause]:
        """Check for inefficiencies even when profitable"""
        causes = []
        
        # Check for low profit margin (< 15%)
        if 0 < totals.profitMarginPct < 15:
            causes.append(LossCause(
                title="Low Profit Margin",
                description=f"While profitable, your margin is only {totals.profitMarginPct:.1f}%. There's room for improvement through cost optimization.",
                impactAmount=totals.totalIncome * 0.1,  # Potential improvement
                confidenceScore=0.65,
            ))
        
        # Check storage costs
        storage_breakdown = next(
            (b for b in expense_breakdown if b.category == ExpenseCategory.STORAGE.value),
            None
        )
        if storage_breakdown and storage_breakdown.percent > 5:
            causes.append(LossCause(
                title="Storage Costs",
                description=f"Storage costs are {storage_breakdown.percent:.1f}% (₹{storage_breakdown.amount:.0f}). Consider direct selling to reduce storage needs.",
                impactAmount=storage_breakdown.amount * 0.4,
                confidenceScore=0.60,
            ))
        
        return causes

    def calculate_total_waste(self, causes: List[LossCause]) -> float:
        """
        Calculate total estimated waste/loss
        
        Args:
            causes: List of loss causes
            
        Returns:
            Total waste amount
        """
        return round(sum(cause.impactAmount for cause in causes), 2)

    def get_highest_impact_cause(self, causes: List[LossCause]) -> LossCause | None:
        """Get the loss cause with highest impact"""
        if not causes:
            return None
        return max(causes, key=lambda x: x.impactAmount)
