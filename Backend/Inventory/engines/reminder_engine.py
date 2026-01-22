"""
Reminder Engine - Expiry Reminder Generation
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta

from ..models import StockCardOutput
from ..constants import HealthStatus


class ReminderEngine:
    """Engine for generating expiry reminders"""
    
    def generate_expiry_reminders(
        self,
        cards: List[StockCardOutput],
        farmer_id: str,
        language: str = "en"
    ) -> List[Dict[str, Any]]:
        """
        Generate expiry reminders for high-risk items
        
        Args:
            cards: Stock cards with priority information
            farmer_id: Farmer ID for reminders
            language: "en" or "hi"
            
        Returns:
            List of reminder records
        """
        reminders = []
        now = datetime.now()
        
        for card in cards:
            # Only create reminders for critical and warning items
            if card.healthStatus not in [HealthStatus.CRITICAL, HealthStatus.WARNING]:
                continue
            
            # Create reminder schedule based on urgency
            if card.healthStatus == HealthStatus.CRITICAL or card.shelfLifeRemainingDays <= 3:
                # Critical: immediate + tomorrow
                reminders.extend(self._create_critical_reminders(card, farmer_id, now, language))
            elif card.shelfLifeRemainingDays <= 7:
                # Warning: today + in 2 days
                reminders.extend(self._create_warning_reminders(card, farmer_id, now, language))
        
        return reminders
    
    def _create_critical_reminders(
        self,
        card: StockCardOutput,
        farmer_id: str,
        now: datetime,
        language: str
    ) -> List[Dict[str, Any]]:
        """Create reminders for critical items"""
        reminders = []
        
        # Immediate reminder
        if language == "hi":
            message = f"🚨 तुरंत ध्यान दें! {card.cropName} ({card.quantityKg} kg) की शेल्फ लाइफ केवल {card.shelfLifeRemainingDays} दिन बची है। तुरंत बेचें!"
        else:
            message = f"🚨 Urgent! {card.cropName} ({card.quantityKg} kg) has only {card.shelfLifeRemainingDays} days shelf life. Sell immediately!"
        
        reminders.append({
            "farmerId": farmer_id,
            "itemId": card.itemId,
            "type": "expiry_critical",
            "message": message,
            "scheduledFor": now,
            "priority": "high",
            "cropName": card.cropName,
            "quantityKg": card.quantityKg,
            "daysRemaining": card.shelfLifeRemainingDays
        })
        
        # Tomorrow reminder
        if language == "hi":
            message = f"⚠️ अंतिम चेतावनी! {card.cropName} जल्द खराब हो जाएगा। आज ही बेचें।"
        else:
            message = f"⚠️ Final warning! {card.cropName} will spoil soon. Sell today."
        
        reminders.append({
            "farmerId": farmer_id,
            "itemId": card.itemId,
            "type": "expiry_final_warning",
            "message": message,
            "scheduledFor": now + timedelta(days=1),
            "priority": "high",
            "cropName": card.cropName,
            "quantityKg": card.quantityKg,
            "daysRemaining": card.shelfLifeRemainingDays - 1
        })
        
        return reminders
    
    def _create_warning_reminders(
        self,
        card: StockCardOutput,
        farmer_id: str,
        now: datetime,
        language: str
    ) -> List[Dict[str, Any]]:
        """Create reminders for warning items"""
        reminders = []
        
        # Today reminder
        if language == "hi":
            message = f"⏰ {card.cropName} ({card.quantityKg} kg) की शेल्फ लाइफ {card.shelfLifeRemainingDays} दिन बची है। जल्द बेचने की योजना बनाएं।"
        else:
            message = f"⏰ {card.cropName} ({card.quantityKg} kg) has {card.shelfLifeRemainingDays} days shelf life. Plan to sell soon."
        
        reminders.append({
            "farmerId": farmer_id,
            "itemId": card.itemId,
            "type": "expiry_warning",
            "message": message,
            "scheduledFor": now,
            "priority": "medium",
            "cropName": card.cropName,
            "quantityKg": card.quantityKg,
            "daysRemaining": card.shelfLifeRemainingDays
        })
        
        # Follow-up in 2 days
        if language == "hi":
            message = f"📢 याद दिलाना: {card.cropName} जल्द बेचें।"
        else:
            message = f"📢 Reminder: Sell {card.cropName} soon."
        
        reminders.append({
            "farmerId": farmer_id,
            "itemId": card.itemId,
            "type": "expiry_followup",
            "message": message,
            "scheduledFor": now + timedelta(days=2),
            "priority": "medium",
            "cropName": card.cropName,
            "quantityKg": card.quantityKg,
            "daysRemaining": card.shelfLifeRemainingDays - 2
        })
        
        return reminders
