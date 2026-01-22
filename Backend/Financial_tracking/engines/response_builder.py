"""
Response Builder - Multilingual Output Formatter
Builds voice-agent compatible output with Hindi/English support
Integrates with voice_agent translator for proper translations
"""

from typing import List
from financial_tracking.models import (
    FinanceTotals,
    ExpenseBreakdown,
    LossCause,
    OptimizationSuggestion,
    FinanceModuleOutput,
    FinanceCard,
)
from financial_tracking.constants import UrgencyLevel

# Import voice_agent translator
try:
    from voice_agent.input_processing.translator import get_translator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    print("⚠️  voice_agent translator not available, using fallback")


class ResponseBuilder:
    """
    Builds complete output for voice agent and UI
    Supports Hindi and English with proper translation
    """

    def __init__(self):
        """Initialize response builder with translator"""
        self.translator = None
        if TRANSLATOR_AVAILABLE:
            try:
                self.translator = get_translator()
            except Exception as e:
                print(f"⚠️  Could not initialize translator: {e}")

    def build_output(
        self,
        language: str,
        totals: FinanceTotals,
        top_expense_categories: List[ExpenseBreakdown],
        loss_causes: List[LossCause],
        suggestions: List[OptimizationSuggestion],
    ) -> FinanceModuleOutput:
        """
        Build complete financial module output
        
        Args:
            language: 'hi' for Hindi, 'en' for English
            totals: Financial totals
            top_expense_categories: Top expense breakdowns
            loss_causes: Identified loss causes
            suggestions: Optimization suggestions
            
        Returns:
            Complete module output with speech text
        """
        # Determine urgency level
        urgency = self._determine_urgency(totals, loss_causes)
        
        # Build header
        header = self._build_header(language, totals)
        
        # Build speech text
        speech_text = self._build_speech_text(
            language, totals, top_expense_categories, loss_causes, suggestions
        )
        
        # Build detailed reasoning
        detailed_reasoning = self._build_detailed_reasoning(
            language, totals, loss_causes, suggestions
        )
        
        return FinanceModuleOutput(
            header=header,
            language=language,
            speechText=speech_text,
            totals=totals,
            topExpenseCategories=top_expense_categories,
            lossCauses=loss_causes,
            suggestions=suggestions,
            detailedReasoning=detailed_reasoning,
            urgencyLevel=urgency,
        )

    def build_finance_card(
        self,
        language: str,
        totals: FinanceTotals,
        loss_causes: List[LossCause],
        suggestions: List[OptimizationSuggestion],
    ) -> FinanceCard:
        """
        Build voice_agent compatible finance card
        
        Args:
            language: Language code
            totals: Financial totals
            loss_causes: Loss causes
            suggestions: Suggestions
            
        Returns:
            FinanceCard for voice agent integration
        """
        # Create title
        if language == "hi":
            title = "खेती का लाभ-हानि विवरण"
        else:
            title = "Farm Profit/Loss Report"
        
        # Create summary
        profit_loss_text = self._format_currency(totals.profitOrLoss)
        if language == "hi":
            if totals.profitOrLoss >= 0:
                summary = f"लाभ: ₹{profit_loss_text} ({totals.profitMarginPct}% मार्जिन)"
            else:
                summary = f"हानि: ₹{profit_loss_text}"
        else:
            if totals.profitOrLoss >= 0:
                summary = f"Profit: ₹{profit_loss_text} ({totals.profitMarginPct}% margin)"
            else:
                summary = f"Loss: ₹{profit_loss_text}"
        
        # Build details
        details = {
            "farmerId": totals.farmerId,
            "season": totals.season,
            "totalIncome": totals.totalIncome,
            "totalExpense": totals.totalExpense,
            "profitOrLoss": totals.profitOrLoss,
            "profitMarginPct": totals.profitMarginPct,
            "lossCausesCount": len(loss_causes),
            "suggestionsCount": len(suggestions),
            "topLossCause": loss_causes[0].title if loss_causes else None,
            "topSuggestion": suggestions[0].suggestionTitle if suggestions else None,
        }
        
        return FinanceCard(
            title=title,
            summary=summary,
            details=details,
            metadata={"language": language},
        )

    def _build_header(self, language: str, totals: FinanceTotals) -> str:
        """Build header text"""
        if language == "hi":
            return f"{totals.season} सीजन का वित्तीय रिपोर्ट"
        else:
            return f"{totals.season} Season Financial Report"

    def _build_speech_text(
        self,
        language: str,
        totals: FinanceTotals,
        top_expenses: List[ExpenseBreakdown],
        loss_causes: List[LossCause],
        suggestions: List[OptimizationSuggestion],
    ) -> str:
        """Build natural speech text for voice agent"""
        
        # Format numbers for speech
        income_text = self._format_currency(totals.totalIncome)
        expense_text = self._format_currency(totals.totalExpense)
        profit_loss_text = self._format_currency(abs(totals.profitOrLoss))
        
        if language == "hi":
            speech = self._build_hindi_speech(
                totals, income_text, expense_text, profit_loss_text,
                top_expenses, loss_causes, suggestions
            )
        else:
            speech = self._build_english_speech(
                totals, income_text, expense_text, profit_loss_text,
                top_expenses, loss_causes, suggestions
            )
        
        return speech

    def _build_hindi_speech(
        self,
        totals: FinanceTotals,
        income_text: str,
        expense_text: str,
        profit_loss_text: str,
        top_expenses: List[ExpenseBreakdown],
        loss_causes: List[LossCause],
        suggestions: List[OptimizationSuggestion],
    ) -> str:
        """Build Hindi speech text using translator"""
        
        # Start with summary
        if totals.profitOrLoss >= 0:
            speech = f"आपको {totals.season} सीजन में {profit_loss_text} रुपये का लाभ हुआ है। "
            speech += f"आपकी कुल आय {income_text} रुपये और कुल खर्च {expense_text} रुपये है। "
            speech += f"लाभ मार्जिन {totals.profitMarginPct} प्रतिशत है। "
        else:
            speech = f"आपको {totals.season} सीजन में {profit_loss_text} रुपये की हानि हुई है। "
            speech += f"आपकी कुल आय {income_text} रुपये थी, लेकिन खर्च {expense_text} रुपये आया। "
        
        # Top expenses
        if top_expenses:
            top_cat = top_expenses[0]
            speech += f"सबसे ज़्यादा खर्च {top_cat.categoryNameHi} पर {self._format_currency(top_cat.amount)} रुपये ({top_cat.percent}%) आया। "
        
        # Loss causes (if any)
        if loss_causes:
            speech += f"मुख्य समस्या: "
            # Translate  the title
            main_cause_title = self._translate_to_hindi(loss_causes[0].title)
            speech += main_cause_title + "। "
        
        # Top suggestion
        if suggestions:
            speech += f"सुझाव: "
            suggestion_title = self._translate_to_hindi(suggestions[0].suggestionTitle)
            speech += suggestion_title + "। "
            speech += f"इससे लगभग {self._format_currency(suggestions[0].estimatedSavings)} रुपये बचा सकते हैं। "
        
        return speech.strip()

    def _build_english_speech(
        self,
        totals: FinanceTotals,
        income_text: str,
        expense_text: str,
        profit_loss_text: str,
        top_expenses: List[ExpenseBreakdown],
        loss_causes: List[LossCause],
        suggestions: List[OptimizationSuggestion],
    ) -> str:
        """Build English speech text"""
        
        # Start with summary
        if totals.profitOrLoss >= 0:
            speech = f"You made a profit of ₹{profit_loss_text} in {totals.season} season. "
            speech += f"Your total income was ₹{income_text} and total expenses were ₹{expense_text}. "
            speech += f"Profit margin is {totals.profitMarginPct}%. "
        else:
            speech = f"You incurred a loss of ₹{profit_loss_text} in {totals.season} season. "
            speech += f"Your total income was ₹{income_text}, but expenses were ₹{expense_text}. "
        
        # Top expenses
        if top_expenses:
            top_cat = top_expenses[0]
            speech += f"Highest expense was on {top_cat.categoryNameEn} at ₹{self._format_currency(top_cat.amount)} ({top_cat.percent}%). "
        
        # Loss causes (if any)
        if loss_causes:
            speech += f"Main issue: {loss_causes[0].title}. "
        
        # Top suggestion
        if suggestions:
            speech += f"Recommendation: {suggestions[0].suggestionTitle}. "
            speech += f"This can save approximately ₹{self._format_currency(suggestions[0].estimatedSavings)}. "
        
        return speech.strip()

    def _build_detailed_reasoning(
        self,
        language: str,
        totals: FinanceTotals,
        loss_causes: List[LossCause],
        suggestions: List[OptimizationSuggestion],
    ) -> str:
        """Build detailed reasoning for transparency"""
        
        if language == "hi":
            reasoning = f"वित्तीय विश्लेषण:\n\n"
            reasoning += f"कुल आय: ₹{self._format_currency(totals.totalIncome)}\n"
            reasoning += f"कुल खर्च: ₹{self._format_currency(totals.totalExpense)}\n"
            
            if totals.profitOrLoss >= 0:
                reasoning += f"शुद्ध लाभ: ₹{self._format_currency(totals.profitOrLoss)}\n"
            else:
                reasoning += f"शुद्ध हानि: ₹{self._format_currency(abs(totals.profitOrLoss))}\n"
            
            if loss_causes:
                reasoning += f"\nसमस्याएं पहचानी गईं: {len(loss_causes)}\n"
            
            if suggestions:
                reasoning += f"सुधार के सुझाव: {len(suggestions)}\n"
        else:
            reasoning = f"Financial Analysis:\n\n"
            reasoning += f"Total Income: ₹{self._format_currency(totals.totalIncome)}\n"
            reasoning += f"Total Expenses: ₹{self._format_currency(totals.totalExpense)}\n"
            
            if totals.profitOrLoss >= 0:
                reasoning += f"Net Profit: ₹{self._format_currency(totals.profitOrLoss)}\n"
            else:
                reasoning += f"Net Loss: ₹{self._format_currency(abs(totals.profitOrLoss))}\n"
            
            if loss_causes:
                reasoning += f"\nIssues Identified: {len(loss_causes)}\n"
            
            if suggestions:
                reasoning += f"Improvement Suggestions: {len(suggestions)}\n"
        
        return reasoning

    def _determine_urgency(
        self,
        totals: FinanceTotals,
        loss_causes: List[LossCause],
    ) -> UrgencyLevel:
        """Determine urgency level based on financial health"""
        
        # High urgency if significant loss
        if totals.profitOrLoss < -10000:
            return UrgencyLevel.HIGH
        
        # High urgency if loss and multiple causes
        if totals.profitOrLoss < 0 and len(loss_causes) >= 3:
            return UrgencyLevel.HIGH
        
        # Medium urgency if small loss or low margin
        if totals.profitOrLoss < 0 or (0 < totals.profitMarginPct < 10):
            return UrgencyLevel.MEDIUM
        
        # Low urgency if profitable
        return UrgencyLevel.LOW

    def _format_currency(self, amount: float) -> str:
        """Format currency for display (Indian number system)"""
        return f"{amount:,.0f}"

    def _translate_to_hindi(self, text: str) -> str:
        """Translate English text to Hindi using voice_agent translator"""
        if self.translator:
            try:
                return self.translator.english_to_hindi(text)
            except Exception as e:
                print(f"⚠️  Translation error: {e}")
                return text
        return text

    def _translate_to_english(self, text: str) -> str:
        """Translate Hindi text to English using voice_agent translator"""
        if self.translator:
            try:
                return self.translator.hindi_to_english(text)
            except Exception as e:
                print(f"⚠️  Translation error: {e}")
                return text
        return text
