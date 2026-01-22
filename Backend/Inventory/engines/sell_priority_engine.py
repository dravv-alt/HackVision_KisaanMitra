"""
Sell Priority Engine - Intelligent Sell Priority Ranking
"""

from typing import List, Dict, Optional
from datetime import datetime

from ..models import inventoryItem, StockCardOutput, MarketPriceContext
from ..constants import (
    HealthStatus,
    StorageType,
    PRIORITY_WEIGHT_HEALTH,
    PRIORITY_WEIGHT_SHELF_LIFE,
    PRIORITY_WEIGHT_SPOILAGE_RISK,
    PRIORITY_WEIGHT_MARKET_TREND
)


class SellPriorityEngine:
    """Engine for ranking stock items by sell priority"""
    
    def rank_stock(
        self,
        items: List[inventoryItem],
        shelf_life_info: Dict[str, Dict],
        health_info: Dict[str, HealthStatus],
        market_context: Optional[Dict[str, MarketPriceContext]] = None
    ) -> List[StockCardOutput]:
        """
        Rank stock items by sell priority
        
        Args:
            items: List of inventory items
            shelf_life_info: Shelf life data for each item (keyed by itemId)
            health_info: Health status for each item (keyed by itemId)
            market_context: Optional market price data (keyed by cropKey)
            
        Returns:
            Sorted list of StockCardOutput with priority ranking
        """
        scored_items = []
        
        for item in items:
            shelf_info = shelf_life_info.get(item.itemId, {})
            health_status = health_info.get(item.itemId, HealthStatus.GOOD)
            market_data = market_context.get(item.cropKey) if market_context else None
            
            # Calculate priority score (higher = more urgent to sell)
            score = self._calculate_priority_score(
                item, shelf_info, health_status, market_data
            )
            
            # Generate reasons for this priority
            reasons = self._generate_reasons(
                item, shelf_info, health_status, market_data
            )
            
            # Determine sell now recommendation
            sell_now = self._should_sell_now(
                health_status, shelf_info.get("remainingDays", 999), market_data
            )
            
            # Suggest next action
            next_action = self._suggest_next_action(
                health_status, shelf_info.get("remainingDays", 999), market_data
            )
            
            scored_items.append({
                "item": item,
                "score": score,
                "reasons": reasons,
                "sellNow": sell_now,
                "nextAction": next_action,
                "shelfInfo": shelf_info,
                "healthStatus": health_status
            })
        
        # Sort by score (descending - highest priority first)
        scored_items.sort(key=lambda x: x["score"], reverse=True)
        
        # Build stock cards with ranking
        stock_cards = []
        for rank, scored_item in enumerate(scored_items, start=1):
            item = scored_item["item"]
            shelf_info = scored_item["shelfInfo"]
            
            card = StockCardOutput(
                itemId=item.itemId,
                cropName=item.cropName,
                quantityKg=item.quantityKg,
                grade=item.qualityGrade,
                storedAt=item.storedAt,
                shelfLifeRemainingDays=shelf_info.get("remainingDays", 0),
                expectedSellBy=item.expectedSellBy,
                stage=item.stage,
                healthStatus=scored_item["healthStatus"],
                sellPriorityRank=rank,
                sellNowRecommendation=scored_item["sellNow"],
                reasons=scored_item["reasons"],
                suggestedNextAction=scored_item["nextAction"],
                spoilageRisk=item.spoilageRisk,
                storageType=item.storageType
            )
            stock_cards.append(card)
        
        return stock_cards
    
    def _calculate_priority_score(
        self,
        item: inventoryItem,
        shelf_info: Dict,
        health_status: HealthStatus,
        market_data: Optional[MarketPriceContext]
    ) -> float:
        """Calculate numerical priority score"""
        score = 0.0
        
        # Health status weight
        health_scores = {
            HealthStatus.CRITICAL: PRIORITY_WEIGHT_HEALTH,
            HealthStatus.WARNING: PRIORITY_WEIGHT_HEALTH * 0.6,
            HealthStatus.GOOD: 0
        }
        score += health_scores.get(health_status, 0)
        
        # Shelf life weight (inverse - less days = higher priority)
        remaining_days = shelf_info.get("remainingDays", 999)
        if remaining_days <= 3:
            score += PRIORITY_WEIGHT_SHELF_LIFE
        elif remaining_days <= 7:
            score += PRIORITY_WEIGHT_SHELF_LIFE * 0.7
        elif remaining_days <= 14:
            score += PRIORITY_WEIGHT_SHELF_LIFE * 0.4
        
        # Spoilage risk weight
        spoilage_scores = {
            "high": PRIORITY_WEIGHT_SPOILAGE_RISK,
            "medium": PRIORITY_WEIGHT_SPOILAGE_RISK * 0.5,
            "low": 0
        }
        score += spoilage_scores.get(item.spoilageRisk, 0)
        
        # Market trend weight
        if market_data:
            if market_data.trend == "falling":
                # Falling prices - sell urgently
                score += PRIORITY_WEIGHT_MARKET_TREND
            elif market_data.trend == "rising" and item.storageType == StorageType.COLD_STORAGE:
                # Rising prices + good storage - can wait
                score -= PRIORITY_WEIGHT_MARKET_TREND * 0.5
        
        return score
    
    def _generate_reasons(
        self,
        item: inventoryItem,
        shelf_info: Dict,
        health_status: HealthStatus,
        market_data: Optional[MarketPriceContext]
    ) -> List[str]:
        """Generate human-readable reasons for priority"""
        reasons = []
        
        remaining_days = shelf_info.get("remainingDays", 999)
        
        # Health-based reasons
        if health_status == HealthStatus.CRITICAL:
            reasons.append("Critical health status - immediate action required")
        elif health_status == HealthStatus.WARNING:
            reasons.append("Warning status - sell soon to avoid loss")
        
        # Shelf life reasons
        if remaining_days <= 0:
            reasons.append("Already expired - sell immediately or use")
        elif remaining_days <= 3:
            reasons.append(f"Only {remaining_days} days until expiry")
        elif remaining_days <= 7:
            reasons.append(f"Shelf life ending in {remaining_days} days")
        
        # Spoilage risk reasons
        if item.spoilageRisk == "high":
            reasons.append("High spoilage risk detected")
        elif item.spoilageRisk == "medium":
            reasons.append("Medium spoilage risk")
        
        # Market trend reasons
        if market_data:
            if market_data.trend == "falling":
                reasons.append(f"Market price falling (₹{market_data.currentPrice}/kg)")
            elif market_data.trend == "rising":
                reasons.append(f"Market price rising (₹{market_data.currentPrice}/kg) - can wait if storage good")
        
        # Storage type considerations
        if item.storageType == StorageType.HOME and remaining_days <= 10:
            reasons.append("Home storage - limited shelf life extension")
        elif item.storageType == StorageType.COLD_STORAGE:
            reasons.append("Cold storage - can wait for better prices")
        
        return reasons if reasons else ["Stock in good condition"]
    
    def _should_sell_now(
        self,
        health_status: HealthStatus,
        remaining_days: int,
        market_data: Optional[MarketPriceContext]
    ) -> bool:
        """Determine if item should be sold immediately"""
        # Critical health always sell now
        if health_status == HealthStatus.CRITICAL:
            return True
        
        # Very short shelf life
        if remaining_days <= 3:
            return True
        
        # Falling market prices + warning status
        if market_data and market_data.trend == "falling" and health_status == HealthStatus.WARNING:
            return True
        
        return False
    
    def _suggest_next_action(
        self,
        health_status: HealthStatus,
        remaining_days: int,
        market_data: Optional[MarketPriceContext]
    ) -> str:
        """Suggest next action for the item"""
        if health_status == HealthStatus.CRITICAL or remaining_days <= 3:
            return "Sell immediately at current market price"
        
        if health_status == HealthStatus.WARNING or remaining_days <= 7:
            return "List for sale within 2-3 days"
        
        if market_data and market_data.trend == "rising":
            return "Monitor market prices, can wait for better rates"
        
        if market_data and market_data.trend == "falling":
            return "Sell within a week before prices drop further"
        
        return "Monitor regularly, sell when prices are favorable"
