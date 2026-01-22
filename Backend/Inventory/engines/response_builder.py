"""
Response Builder - UI Output Generation
"""

from typing import List, Dict
from ..models import StockCardOutput, InventoryModuleOutput
from ..constants import Language, UrgencyLevel, HealthStatus


class ResponseBuilder:
    """Engine for building UI-ready responses"""
    
    def build(
        self,
        language: Language,
        cards: List[StockCardOutput],
        farmer_id: str
    ) -> InventoryModuleOutput:
        """
        Build complete inventory dashboard output
        
        Args:
            language: Language preference
            cards: Stock cards (already sorted by priority)
            farmer_id: Farmer ID
            
        Returns:
            Complete InventoryModuleOutput for UI
        """
        # Calculate counts
        total_count = len(cards)
        warning_count = sum(1 for card in cards if card.healthStatus == HealthStatus.WARNING)
        critical_count = sum(1 for card in cards if card.healthStatus == HealthStatus.CRITICAL)
        
        # Determine urgency level
        urgency = self._determine_urgency(critical_count, warning_count)
        
        # Generate speech text
        speech_text = self._generate_speech_text(
            language, total_count, warning_count, critical_count, cards
        )
        
        # Generate header
        header = self._generate_header(language, total_count)
        
        # Generate detailed reasoning
        detailed_reasoning = self._generate_detailed_reasoning(
            language, cards, critical_count, warning_count
        )
        
        return InventoryModuleOutput(
            header=header,
            language=language,
            speechText=speech_text,
            stockCards=cards,
            totalStockCount=total_count,
            warningCount=warning_count,
            criticalCount=critical_count,
            detailedReasoning=detailed_reasoning,
            urgencyLevel=urgency
        )
    
    def _determine_urgency(self, critical_count: int, warning_count: int) -> UrgencyLevel:
        """Determine overall urgency level"""
        if critical_count > 0:
            return UrgencyLevel.HIGH
        elif warning_count > 0:
            return UrgencyLevel.MEDIUM
        else:
            return UrgencyLevel.LOW
    
    def _generate_speech_text(
        self,
        language: Language,
        total_count: int,
        warning_count: int,
        critical_count: int,
        cards: List[StockCardOutput]
    ) -> str:
        """Generate voice-friendly speech text"""
        if language == Language.HINDI:
            if total_count == 0:
                return "आपके पास कोई स्टॉक नहीं है।"
            
            speech = f"आपके पास {total_count} स्टॉक आइटम हैं। "
            
            if critical_count > 0:
                speech += f"{critical_count} आइटम खतरनाक स्थिति में हैं, उन्हें तुरंत बेचना चाहिए। "
                # Mention top critical item
                critical_items = [c for c in cards if c.healthStatus == HealthStatus.CRITICAL]
                if critical_items:
                    top = critical_items[0]
                    speech += f"{top.cropName} की शेल्फ लाइफ केवल {top.shelfLifeRemainingDays} दिन बची है। "
            
            if warning_count > 0:
                speech += f"{warning_count} आइटम सावधानी की स्थिति में हैं, उन्हें जल्द बेचें। "
            
            if critical_count == 0 and warning_count == 0:
                speech += "सभी स्टॉक अच्छी स्थिति में हैं। "
            
            # Add sell priority guidance
            if cards and cards[0].sellNowRecommendation:
                speech += f"पहले {cards[0].cropName} बेचें।"
            
        else:  # English
            if total_count == 0:
                return "You have no stock items."
            
            speech = f"You have {total_count} stock items. "
            
            if critical_count > 0:
                speech += f"{critical_count} items are in critical condition and should be sold immediately. "
                # Mention top critical item
                critical_items = [c for c in cards if c.healthStatus == HealthStatus.CRITICAL]
                if critical_items:
                    top = critical_items[0]
                    speech += f"{top.cropName} has only {top.shelfLifeRemainingDays} days shelf life remaining. "
            
            if warning_count > 0:
                speech += f"{warning_count} items need caution, sell them soon. "
            
            if critical_count == 0 and warning_count == 0:
                speech += "All stock is in good condition. "
            
            # Add sell priority guidance
            if cards and cards[0].sellNowRecommendation:
                speech += f"Sell {cards[0].cropName} first."
        
        return speech.strip()
    
    def _generate_header(self, language: Language, total_count: int) -> str:
        """Generate dashboard header"""
        if language == Language.HINDI:
            return f"इन्वेंटरी डैशबोर्ड - {total_count} आइटम"
        else:
            return f"Inventory Dashboard - {total_count} Items"
    
    def _generate_detailed_reasoning(
        self,
        language: Language,
        cards: List[StockCardOutput],
        critical_count: int,
        warning_count: int
    ) -> str:
        """Generate detailed reasoning for dashboard"""
        if language == Language.HINDI:
            reasoning = "स्टॉक विश्लेषण:\n\n"
            
            if critical_count > 0:
                reasoning += f"🚨 {critical_count} आइटम तुरंत ध्यान देने की जरूरत है।\n"
            
            if warning_count > 0:
                reasoning += f"⚠️ {warning_count} आइटम जल्द बेचने की जरूरत है।\n"
            
            if cards:
                reasoning += f"\nसबसे पहले बेचें: {cards[0].cropName} ({cards[0].quantityKg} kg)\n"
                reasoning += f"कारण: {', '.join(cards[0].reasons[:2])}\n"
            
            reasoning += "\nसुझाव: शेल्फ लाइफ के आधार पर प्राथमिकता दी गई है।"
            
        else:  # English
            reasoning = "Stock Analysis:\n\n"
            
            if critical_count > 0:
                reasoning += f"🚨 {critical_count} items need immediate attention.\n"
            
            if warning_count > 0:
                reasoning += f"⚠️ {warning_count} items should be sold soon.\n"
            
            if cards:
                reasoning += f"\nSell first: {cards[0].cropName} ({cards[0].quantityKg} kg)\n"
                reasoning += f"Reason: {', '.join(cards[0].reasons[:2])}\n"
            
            reasoning += "\nNote: Priority is based on shelf life and market conditions."
        
        return reasoning
