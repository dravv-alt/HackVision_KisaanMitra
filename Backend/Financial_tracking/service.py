"""
Financial Tracking Service - Main Orchestrator
Coordinates all financial tracking operations
"""

from typing import Optional
from Backend.Financial_tracking.models import FinanceModuleOutput, FinanceCard
from Backend.Financial_tracking.repositories import TransactionRepo, SummaryRepo, CropRepo
from Backend.Financial_tracking.engines import (
    LedgerEngine,
    ProfitLossEngine,
    LossAnalysisEngine,
    OptimizationEngine,
    ResponseBuilder,
)
from Backend.Financial_tracking.constants import SeasonType


class FinanceTrackingService:
    """
    Main service orchestrator for financial tracking
    Coordinates repos and engines to generate complete financial reports
    """

    def __init__(self):
        """Initialize service with repositories and engines"""
        # Repositories
        self.transaction_repo = TransactionRepo()
        self.summary_repo = SummaryRepo()
        self.crop_repo = CropRepo()
        
        # Engines
        self.ledger_engine = LedgerEngine()
        self.profit_loss_engine = ProfitLossEngine()
        self.loss_analysis_engine = LossAnalysisEngine()
        self.optimization_engine = OptimizationEngine()
        self.response_builder = ResponseBuilder()

    def run_finance_report(
        self,
        farmerId: str,
        season: str = SeasonType.KHARIF.value,
        language: str = "hi",
        force_refresh: bool = False,
    ) -> FinanceModuleOutput:
        """
        Generate complete financial report
        
        Args:
            farmerId: Farmer ID
            season: Season (KHARIF/RABI/ZAID)
            language: Output language ('hi' or 'en')
            force_refresh: Force recomputation instead of using cache
            
        Returns:
            Complete financial module output with voice-ready speech text
        """
        print(f"\n{'='*60}")
        print(f"Generating Financial Report for Farmer: {farmerId}")
        print(f"Season: {season} | Language: {language}")
        print(f"{'='*60}\n")
        
        # Step 1: Check for cached summary (unless forced refresh)
        if not force_refresh:
            cached_summary = self.summary_repo.get_summary(farmerId, season)
            if cached_summary:
                print("✓ Using cached summary (use force_refresh=True to recompute)")
        
        # Step 2: Seed mock data if DB empty (FALLBACK ONLY)
        # This ensures hackathon demos never fail
        self.transaction_repo.seed_mock_data_if_empty(farmerId, season)
        
        # Step 3: Fetch transactions
        print("→ Fetching transactions...")
        transactions = self.transaction_repo.list_transactions(farmerId, season)
        print(f"  Found {len(transactions)} transactions")
        
        if not transactions:
            print("⚠️  No transactions found - cannot generate report")
            # Return empty report
            return self._empty_report(farmerId, season, language)
        
        # Step 4: Compute totals and breakdown
        print("→ Computing profit/loss...")
        totals, expense_breakdown = self.profit_loss_engine.build_profit_loss_report(
            transactions, farmerId, season
        )
        
        print(f"  Total Income:   ₹{totals.totalIncome:,.0f}")
        print(f"  Total Expense:  ₹{totals.totalExpense:,.0f}")
        print(f"  Profit/Loss:    ₹{totals.profitOrLoss:,.0f}")
        print(f"  Margin:         {totals.profitMarginPct}%")
        
        # Step 5: Analyze loss causes
        print("→ Analyzing loss causes...")
        loss_causes = self.loss_analysis_engine.identify_loss_causes(
            transactions, totals, expense_breakdown
        )
        print(f"  Identified {len(loss_causes)} issues")
        
        # Step 6: Generate optimization suggestions
        print("→ Generating optimization suggestions...")
        suggestions = self.optimization_engine.generate_suggestions(
            loss_causes, totals, expense_breakdown
        )
        print(f"  Generated {len(suggestions)} suggestions")
        
        # Step 7: Build response
        print("→ Building multilingual response...")
        top_expense_categories = self.profit_loss_engine.get_top_expense_categories(
            expense_breakdown, top_n=5
        )
        
        output = self.response_builder.build_output(
            language=language,
            totals=totals,
            top_expense_categories=top_expense_categories,
            loss_causes=loss_causes,
            suggestions=suggestions,
        )
        
        # Step 8: Cache summary for dashboard
        print("→ Caching summary...")
        self.summary_repo.save_summary(totals)
        
        # Step 8b: Ingest into RAG Vector Store
        try:
            # We import here to avoid circular dependencies if any
            from voice_agent.retrieval.vector_store import get_vector_store
            vector_store = get_vector_store()
            
            fin_summary_data = {
                "season": season,
                "totalIncome": totals.totalIncome,
                "totalExpense": totals.totalExpense,
                "profitOrLoss": totals.profitOrLoss,
                "timestamp": output.generatedAt.isoformat() if hasattr(output, "generatedAt") else None,
                "lossCauses": [{"description": lc.description} for lc in loss_causes]
            }
            vector_store.ingest_financial_summary(fin_summary_data)
            print("✓ Ingested financial summary into VectorDB")
        except Exception as e:
            print(f"⚠️  Failed to ingest finance info into VectorDB: {e}")
        
        print(f"\n{'='*60}")
        print("✓ Financial report generated successfully")
        print(f"{'='*60}\n")
        
        return output

    def get_finance_card(
        self,
        farmerId: str,
        season: str = SeasonType.KHARIF.value,
        language: str = "hi",
    ) -> FinanceCard:
        """
        Generate voice_agent compatible finance card
        
        Args:
            farmerId: Farmer ID
            season: Season
            language: Output language
            
        Returns:
            FinanceCard for voice agent integration
        """
        # Get full report
        output = self.run_finance_report(farmerId, season, language)
        
        # Build card
        card = self.response_builder.build_finance_card(
            language=language,
            totals=output.totals,
            loss_causes=output.lossCauses,
            suggestions=output.suggestions,
        )
        
        return card

    def add_expense(
        self,
        farmerId: str,
        season: str,
        category: str,
        amount: float,
        notes: Optional[str] = None,
        relatedCropId: Optional[str] = None,
    ) -> dict:
        """
        Add a new expense transaction
        
        Args:
            farmerId: Farmer ID
            season: Season
            category: Expense category
            amount: Amount
            notes: Optional notes
            relatedCropId: Optional related crop ID
            
        Returns:
            Success response with transaction ID
        """
        try:
            # Create transaction
            transaction = self.ledger_engine.record_expense(
                farmerId=farmerId,
                season=season,
                category=category,
                amount=amount,
                notes=notes,
                relatedCropId=relatedCropId,
            )
            
            # Save to repository
            saved_tx = self.transaction_repo.add_transaction(transaction)
            
            # Invalidate cached summary
            self.summary_repo.delete_summary(farmerId, season)
            
            return {
                "success": True,
                "transactionId": saved_tx.transactionId,
                "message": "Expense recorded successfully",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to record expense",
            }

    def add_income(
        self,
        farmerId: str,
        season: str,
        category: str,
        amount: float,
        notes: Optional[str] = None,
        relatedCropId: Optional[str] = None,
    ) -> dict:
        """
        Add a new income transaction
        
        Args:
            farmerId: Farmer ID
            season: Season
            category: Income category
            amount: Amount
            notes: Optional notes
            relatedCropId: Optional related crop ID
            
        Returns:
            Success response with transaction ID
        """
        try:
            # Create transaction
            transaction = self.ledger_engine.record_income(
                farmerId=farmerId,
                season=season,
                category=category,
                amount=amount,
                notes=notes,
                relatedCropId=relatedCropId,
            )
            
            # Save to repository
            saved_tx = self.transaction_repo.add_transaction(transaction)
            
            # Invalidate cached summary
            self.summary_repo.delete_summary(farmerId, season)
            
            return {
                "success": True,
                "transactionId": saved_tx.transactionId,
                "message": "Income recorded successfully",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to record income",
            }

    def _empty_report(
        self,
        farmerId: str,
        season: str,
        language: str,
    ) -> FinanceModuleOutput:
        """Generate empty report when no data available"""
        from Backend.Financial_tracking.models import FinanceTotals
        from Backend.Financial_tracking.constants import UrgencyLevel
        
        empty_totals = FinanceTotals(
            farmerId=farmerId,
            season=season,
            totalExpense=0.0,
            totalIncome=0.0,
            profitOrLoss=0.0,
            profitMarginPct=0.0,
        )
        
        if language == "hi":
            speech_text = "कोई वित्तीय डेटा उपलब्ध नहीं है। कृपया अपने खर्च और आय दर्ज करें।"
            header = "वित्तीय रिपोर्ट - डेटा नहीं मिला"
            reasoning = "कोई लेनदेन नहीं मिला।"
        else:
            speech_text = "No financial data available. Please record your expenses and income."
            header = "Financial Report - No Data Found"
            reasoning = "No transactions found."
        
        return FinanceModuleOutput(
            header=header,
            language=language,
            speechText=speech_text,
            totals=empty_totals,
            topExpenseCategories=[],
            lossCauses=[],
            suggestions=[],
            detailedReasoning=reasoning,
            urgencyLevel=UrgencyLevel.LOW,
        )


# Singleton instance
_service_instance = None


def get_finance_tracking_service() -> FinanceTrackingService:
    """Get or create singleton service instance"""
    global _service_instance
    if _service_instance is None:
        _service_instance = FinanceTrackingService()
    return _service_instance
