"""
Financial Tracking CLI Demo
Manual testing interface for the financial tracking module
Run this to test the complete financial tracking flow
"""

import sys
from pathlib import Path

# Add Backend directory to Python path for imports
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from datetime import datetime
from financial_tracking.service import get_finance_tracking_service
from financial_tracking.constants import SeasonType, ExpenseCategory, IncomeCategory


def print_section(title: str):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_transactions_summary(service, farmerId: str, season: str):
    """Print transaction summary"""
    print_section("TRANSACTION LEDGER")
    
    transactions = service.transaction_repo.list_transactions(farmerId, season)
    
    if not transactions:
        print("No transactions found.")
        return
    
    # Group by type
    expenses = [tx for tx in transactions if tx.type.value == "EXPENSE"]
    incomes = [tx for tx in transactions if tx.type.value == "INCOME"]
    
    print(f"Total Transactions: {len(transactions)}")
    print(f"  Expenses: {len(expenses)}")
    print(f"  Income: {len(incomes)}\n")
    
    # Show recent transactions
    print("Recent Transactions:")
    print(f"{'Date':<12} {'Type':<10} {'Category':<15} {'Amount':>12} {'Notes'}")
    print("-" * 70)
    
    for tx in transactions[-10:]:  # Last 10 transactions
        date_str = tx.ts.strftime("%d-%b-%Y")
        amount_str = f"₹{tx.amount:,.0f}"
        notes_str = (tx.notes or "")[:30]
        print(f"{date_str:<12} {tx.type.value:<10} {tx.category:<15} {amount_str:>12} {notes_str}")


def print_financial_totals(totals):
    """Print financial totals"""
    print_section("FINANCIAL SUMMARY")
    
    print(f"Farmer ID:      {totals.farmerId}")
    print(f"Season:         {totals.season}")
    print(f"\nTotal Income:   ₹{totals.totalIncome:>12,.0f}")
    print(f"Total Expense:  ₹{totals.totalExpense:>12,.0f}")
    print("-" * 40)
    
    if totals.profitOrLoss >= 0:
        print(f"Net Profit:     ₹{totals.profitOrLoss:>12,.0f} ✓")
        print(f"Profit Margin:  {totals.profitMarginPct:>11.2f}%")
    else:
        print(f"Net Loss:       ₹{abs(totals.profitOrLoss):>12,.0f} ✗")
        print(f"Margin:         {totals.profitMarginPct:>11.2f}%")


def print_expense_breakdown(breakdown):
    """Print expense breakdown"""
    print_section("TOP EXPENSE CATEGORIES")
    
    if not breakdown:
        print("No expenses recorded.")
        return
    
    print(f"{'Category':<20} {'Amount':>15} {'Percentage':>12}")
    print("-" * 50)
    
    for item in breakdown:
        category_display = f"{item.categoryNameEn} ({item.categoryNameHi})"
        amount_str = f"₹{item.amount:,.0f}"
        percent_str = f"{item.percent:.1f}%"
        print(f"{category_display:<20} {amount_str:>15} {percent_str:>12}")


def print_loss_causes(causes):
    """Print loss causes"""
    print_section("LOSS CAUSES IDENTIFIED")
    
    if not causes:
        print("No loss causes identified (good news!)")
        return
    
    for i, cause in enumerate(causes, 1):
        print(f"\n{i}. {cause.title}")
        print(f"   Description: {cause.description}")
        print(f"   Impact: ₹{cause.impactAmount:,.0f}")
        print(f"   Confidence: {cause.confidenceScore * 100:.0f}%")


def print_optimization_suggestions(suggestions):
    """Print optimization suggestions"""
    print_section("OPTIMIZATION SUGGESTIONS")
    
    if not suggestions:
        print("No suggestions available.")
        return
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n{i}. {suggestion.suggestionTitle} (Priority: {suggestion.priority})")
        print(f"   Why this helps: {suggestion.whyThisHelps}")
        print(f"   Estimated Savings: ₹{suggestion.estimatedSavings:,.0f}")
        print(f"   Action Steps:")
        for step in suggestion.actionableSteps:
            print(f"     • {step}")


def print_speech_text(output):
    """Print voice-ready speech text"""
    print_section("VOICE AGENT OUTPUT (Speech Text)")
    
    print(f"Language: {output.language.upper()}")
    print(f"Urgency: {output.urgencyLevel.value}\n")
    print(output.speechText)


def run_demo():
    """Run the complete demo"""
    print("\n" + "="*70)
    print(" " * 15 + "FINANCIAL TRACKING MODULE - CLI DEMO")
    print("="*70)
    
    # Get input from user
    print("\nEnter farmer details:")
    farmerId = input("Farmer ID (press Enter for demo 'FARMER_001'): ").strip()
    if not farmerId:
        farmerId = "FARMER_001"
    
    print("\nSelect Season:")
    print("1. KHARIF (Monsoon - Jun to Oct)")
    print("2. RABI (Winter - Nov to Mar)")
    print("3. ZAID (Summer - Mar to Jun)")
    
    season_choice = input("Choice (press Enter for KHARIF): ").strip()
    season_map = {
        "1": SeasonType.KHARIF.value,
        "2": SeasonType.RABI.value,
        "3": SeasonType.ZAID.value,
        "": SeasonType.KHARIF.value,
    }
    season = season_map.get(season_choice, SeasonType.KHARIF.value)
    
    print("\nSelect Language:")
    print("1. Hindi")
    print("2. English")
    
    lang_choice = input("Choice (press Enter for Hindi): ").strip()
    language = "en" if lang_choice == "2" else "hi"
    
    # Initialize service
    print("\n→ Initializing Financial Tracking Service...")
    service = get_finance_tracking_service()
    
    # Generate report
    print("\n→ Generating financial report...")
    output = service.run_finance_report(
        farmerId=farmerId,
        season=season,
        language=language,
        force_refresh=True,
    )
    
    # Display results
    print_transactions_summary(service, farmerId, season)
    print_financial_totals(output.totals)
    print_expense_breakdown(output.topExpenseCategories)
    print_loss_causes(output.lossCauses)
    print_optimization_suggestions(output.suggestions)
    print_speech_text(output)
    
    # Print detailed reasoning
    print_section("DETAILED REASONING")
    print(output.detailedReasoning)
    
    # Voice agent card
    print_section("VOICE AGENT CARD")
    card = service.get_finance_card(farmerId, season, language)
    print(f"Card Type: {card.card_type}")
    print(f"Title: {card.title}")
    print(f"Summary: {card.summary}")
    print(f"\nCard Details:")
    for key, value in card.details.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*70)
    print(" " * 20 + "DEMO COMPLETED SUCCESSFULLY!")
    print("="*70 + "\n")


def run_quick_test():
    """Quick test without user input"""
    print("\n" + "="*70)
    print(" " * 18 + "QUICK TEST MODE")
    print("="*70)
    
    service = get_finance_tracking_service()
    
    # Test both languages
    for language in ["en", "hi"]:
        print(f"\n→ Testing language: {language.upper()}")
        
        output = service.run_finance_report(
            farmerId="TEST_FARMER",
            season=SeasonType.KHARIF.value,
            language=language,
            force_refresh=True,
        )
        
        print(f"\n  Speech Output ({language}):")
        print(f"  {output.speechText}")
        
        print(f"\n  Financial Summary:")
        print(f"    Income: ₹{output.totals.totalIncome:,.0f}")
        print(f"    Expense: ₹{output.totals.totalExpense:,.0f}")
        print(f"    Profit/Loss: ₹{output.totals.profitOrLoss:,.0f}")
        print(f"    Margin: {output.totals.profitMarginPct}%")
        
        print(f"\n  Issues: {len(output.lossCauses)}")
        print(f"  Suggestions: {len(output.suggestions)}")
    
    print("\n" + "="*70)
    print(" " * 20 + "QUICK TEST PASSED!")
    print("="*70 + "\n")


if __name__ == "__main__":
    print("\nFinancial Tracking Module - CLI Demo")
    print("=====================================\n")
    
    print("Select mode:")
    print("1. Interactive Demo (default)")
    print("2. Quick Test (automated)")
    
    mode = input("\nChoice: ").strip()
    
    if mode == "2":
        run_quick_test()
    else:
        run_demo()
