"""
Optimization Engine - Margin Improvement Suggestions
Generates actionable recommendations to improve profit margins
"""

from typing import List
from Backend.Financial_tracking.models import (
    LossCause,
    FinanceTotals,
    ExpenseBreakdown,
    OptimizationSuggestion,
)
from Backend.Financial_tracking.constants import ExpenseCategory


class OptimizationEngine:
    """
    Generates optimization suggestions for improving farm profitability
    """

    def generate_suggestions(
        self,
        loss_causes: List[LossCause],
        totals: FinanceTotals,
        expense_breakdown: List[ExpenseBreakdown],
    ) -> List[OptimizationSuggestion]:
        """
        Generate actionable optimization suggestions
        
        Args:
            loss_causes: Identified loss causes
            totals: Financial totals
            expense_breakdown: Expense category breakdown
            
        Returns:
            List of optimization suggestions prioritized by impact
        """
        suggestions = []
        
        # Generate suggestions based on loss causes
        for cause in loss_causes:
            if "Transport" in cause.title:
                suggestions.append(self._suggest_transport_optimization(cause))
            
            elif "Labour" in cause.title:
                suggestions.append(self._suggest_labour_optimization(cause))
            
            elif "Fertilizer" in cause.title:
                suggestions.append(self._suggest_fertilizer_optimization(cause))
            
            elif "Pesticide" in cause.title:
                suggestions.append(self._suggest_pesticide_optimization(cause))
            
            elif "Irrigation" in cause.title or "Water" in cause.title:
                suggestions.append(self._suggest_irrigation_optimization(cause))
            
            elif "Selling Price" in cause.title or "Low Selling" in cause.title:
                suggestions.append(self._suggest_selling_strategy(cause))
            
            elif "Storage" in cause.title:
                suggestions.append(self._suggest_storage_optimization(cause))
        
        # Add general suggestions for profit improvement
        suggestions.extend(self._general_profit_suggestions(totals, expense_breakdown))
        
        # Remove duplicates and rank by priority
        suggestions = self._deduplicate_suggestions(suggestions)
        suggestions.sort(key=lambda x: x.priority)
        
        return suggestions

    def _suggest_transport_optimization(self, cause: LossCause) -> OptimizationSuggestion:
        """Suggestion for reducing transport costs"""
        return OptimizationSuggestion(
            suggestionTitle="Optimize Transport & Mandi Selection",
            whyThisHelps="Choosing nearer mandi, bulk transport, or farmer cooperatives can significantly reduce transport costs and save 20-40% on logistics.",
            estimatedSavings=cause.impactAmount,
            priority=1,
            actionableSteps=[
                "Research mandis within 30km radius and compare prices",
                "Join farmer producer organization (FPO) for bulk transport",
                "Consider direct buyer contracts to avoid multiple trips",
                "Coordinate with neighbor farmers for shared transport",
            ],
        )

    def _suggest_labour_optimization(self, cause: LossCause) -> OptimizationSuggestion:
        """Suggestion for reducing labour costs"""
        return OptimizationSuggestion(
            suggestionTitle="Mechanization & Efficient Labour Management",
            whyThisHelps="Using machinery for key operations (sowing, harvesting) and better labour planning can reduce costs by 15-30% while improving efficiency.",
            estimatedSavings=cause.impactAmount,
            priority=2,
            actionableSteps=[
                "Rent harvester/thresher instead of manual labour",
                "Use seed drill machine for efficient sowing",
                "Plan labour requirements in advance to avoid urgent hiring at high rates",
                "Consider custom hiring centers (CHC) for machinery rental",
            ],
        )

    def _suggest_fertilizer_optimization(self, cause: LossCause) -> OptimizationSuggestion:
        """Suggestion for optimizing fertilizer use"""
        return OptimizationSuggestion(
            suggestionTitle="Soil Testing & Balanced Fertilizer Use",
            whyThisHelps="Soil testing helps apply only needed nutrients, avoiding wastage. Can save 20-35% on fertilizer costs while maintaining or improving yield.",
            estimatedSavings=cause.impactAmount,
            priority=1,
            actionableSteps=[
                "Get soil health card from nearest agriculture office (free)",
                "Apply fertilizer based on soil test recommendations",
                "Buy fertilizer in bulk during off-season for better prices",
                "Consider organic compost to reduce chemical fertilizer need",
            ],
        )

    def _suggest_pesticide_optimization(self, cause: LossCause) -> OptimizationSuggestion:
        """Suggestion for reducing pesticide costs"""
        return OptimizationSuggestion(
            suggestionTitle="Integrated Pest Management (IPM)",
            whyThisHelps="Using biological controls, crop rotation, and targeted pesticide application can reduce chemical use by 30-50% while maintaining crop health.",
            estimatedSavings=cause.impactAmount,
            priority=2,
            actionableSteps=[
                "Install pheromone traps for early pest detection",
                "Use neem-based organic pesticides as first defense",
                "Consult Krishi Vigyan Kendra (KVK) for IPM training",
                "Apply pesticides only when threshold damage is reached",
            ],
        )

    def _suggest_irrigation_optimization(self, cause: LossCause) -> OptimizationSuggestion:
        """Suggestion for reducing irrigation costs"""
        return OptimizationSuggestion(
            suggestionTitle="Efficient Irrigation & Water Management",
            whyThisHelps="Drip irrigation, mulching, and proper scheduling can reduce water and electricity costs by 30-40% while improving crop health.",
            estimatedSavings=cause.impactAmount,
            priority=1,
            actionableSteps=[
                "Apply for PM Kusum Yojana for solar pump subsidy",
                "Use drip irrigation (subsidized under PMKSY scheme)",
                "Irrigate during early morning/evening to reduce evaporation",
                "Apply mulch to retain soil moisture",
            ],
        )

    def _suggest_selling_strategy(self, cause: LossCause) -> OptimizationSuggestion:
        """Suggestion for improving selling price"""
        return OptimizationSuggestion(
            suggestionTitle="Strategic Selling & Price Optimization",
            whyThisHelps="Selling at the right time, right place, and exploring alternative markets can increase revenue by 15-25% without extra production cost.",
            estimatedSavings=cause.impactAmount,
            priority=1,
            actionableSteps=[
                "Check mandi prices on eNAM portal before selling",
                "Store produce (if possible) to sell during price peaks",
                "Explore direct buyer contracts or FPO collective selling",
                "Consider government procurement at MSP if eligible",
            ],
        )

    def _suggest_storage_optimization(self, cause: LossCause) -> OptimizationSuggestion:
        """Suggestion for reducing storage costs"""
        return OptimizationSuggestion(
            suggestionTitle="Reduce Storage Costs",
            whyThisHelps="Proper storage planning and direct selling can save 30-50% on storage fees and reduce spoilage risk.",
            estimatedSavings=cause.impactAmount,
            priority=3,
            actionableSteps=[
                "Sell immediately after harvest if storage costs are high",
                "Use scientific storage methods to reduce spoilage",
                "Consider warehouse receipt system for better storage rates",
                "Coordinate with buyers for direct pickup from field",
            ],
        )

    def _general_profit_suggestions(
        self,
        totals: FinanceTotals,
        expense_breakdown: List[ExpenseBreakdown],
    ) -> List[OptimizationSuggestion]:
        """General suggestions applicable to most farmers"""
        suggestions = []
        
        # Suggest subsidy awareness
        suggestions.append(OptimizationSuggestion(
            suggestionTitle="Maximize Government Subsidies & Benefits",
            whyThisHelps="Government schemes can reduce input costs by 30-60% through subsidies on seeds, fertilizers, equipment, and insurance.",
            estimatedSavings=totals.totalExpense * 0.15,
            priority=2,
            actionableSteps=[
                "Enroll in PM-KISAN for ₹6000/year direct benefit",
                "Get crop insurance under PMFBY to protect against losses",
                "Check state-specific subsidy schemes for inputs",
                "Visit agriculture office to learn about all applicable schemes",
            ],
        ))
        
        # Suggest record keeping
        if totals.profitMarginPct < 20:
            suggestions.append(OptimizationSuggestion(
                suggestionTitle="Detailed Expense Tracking",
                whyThisHelps="Regular tracking helps identify waste areas and plan better. Farmers who track expenses save 10-15% on average.",
                estimatedSavings=totals.totalExpense * 0.10,
                priority=4,
                actionableSteps=[
                    "Record every expense immediately using this app",
                    "Review expense breakdown before next season",
                    "Compare costs with neighboring farmers",
                    "Set budget limits for each expense category",
                ],
            ))
        
        return suggestions

    def _deduplicate_suggestions(
        self,
        suggestions: List[OptimizationSuggestion],
    ) -> List[OptimizationSuggestion]:
        """Remove duplicate suggestions based on title"""
        seen_titles = set()
        unique_suggestions = []
        
        for suggestion in suggestions:
            if suggestion.suggestionTitle not in seen_titles:
                seen_titles.add(suggestion.suggestionTitle)
                unique_suggestions.append(suggestion)
        
        return unique_suggestions

    def estimate_total_potential_savings(
        self,
        suggestions: List[OptimizationSuggestion],
    ) -> float:
        """
        Calculate total potential savings from all suggestions
        
        Args:
            suggestions: List of suggestions
            
        Returns:
            Total estimated savings
        """
        return round(sum(s.estimatedSavings for s in suggestions), 2)
