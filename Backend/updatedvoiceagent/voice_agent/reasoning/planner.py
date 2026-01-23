"""
Reasoning Planner - Creates reasoning plans per intent
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from voice_agent.core.intent import Intent


@dataclass
class ReasoningPlan:
    """Reasoning plan for an intent"""
    intent: Intent
    factors_to_consider: List[str]
    decision_criteria: List[str]
    output_format: str


class ReasoningPlanner:
    """Creates reasoning plans based on intent"""
    
    def create_plan(self, intent: Intent) -> ReasoningPlan:
        """
        Create reasoning plan for intent
        
        Args:
            intent: Detected intent
        
        Returns:
            Reasoning plan
        """
        plans = {
            Intent.CROP_PLANNING: ReasoningPlan(
                intent=Intent.CROP_PLANNING,
                factors_to_consider=[
                    "Soil type",
                    "Current season",
                    "Weather conditions",
                    "Market demand",
                    "Water availability",
                    "Profit potential"
                ],
                decision_criteria=[
                    "Soil compatibility",
                    "Season suitability",
                    "Market price trends",
                    "Risk level"
                ],
                output_format="Recommend top 3 crops with reasoning"
            ),
            
            Intent.STORAGE_DECISION: ReasoningPlan(
                intent=Intent.STORAGE_DECISION,
                factors_to_consider=[
                    "Crop spoilage risk",
                    "Current market price",
                    "Price forecast",
                    "Storage cost",
                    "Storage availability"
                ],
                decision_criteria=[
                    "Profit improvement potential",
                    "Spoilage risk level",
                    "Storage cost vs benefit"
                ],
                output_format="Recommend sell now or store with reasoning"
            ),
            
            Intent.GOVERNMENT_SCHEME: ReasoningPlan(
                intent=Intent.GOVERNMENT_SCHEME,
                factors_to_consider=[
                    "Farmer location",
                    "Land size",
                    "Crop type",
                    "Scheme deadlines"
                ],
                decision_criteria=[
                    "Eligibility criteria",
                    "Deadline urgency",
                    "Benefit amount"
                ],
                output_format="List eligible schemes with reasons"
            ),
        }
        
        return plans.get(intent, ReasoningPlan(
            intent=intent,
            factors_to_consider=["Context", "User query"],
            decision_criteria=["Relevance"],
            output_format="Provide relevant information"
        ))


# Singleton instance
_planner = None

def get_reasoning_planner() -> ReasoningPlanner:
    """Get or create reasoning planner"""
    global _planner
    if _planner is None:
        _planner = ReasoningPlanner()
    return _planner
