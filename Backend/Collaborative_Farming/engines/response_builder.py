"""
Response Builder for Collaborative Farming
"""

from typing import List, Optional
from ..models import (
    CollaborativeOutput, EquipmentListing, RentalRequest, 
    LandPoolRequest, ResidueListing, ReminderRecord
)
from ..constants import Language, UrgencyLevel


class ResponseBuilder:
    """Builder for orchestrating final module output with voice-first speechText"""
    
    def build(
        self,
        language: Language,
        equipment: List[EquipmentListing],
        rentals: List[RentalRequest],
        pools: List[LandPoolRequest],
        residue: List[ResidueListing],
        reminders: List[ReminderRecord]
    ) -> CollaborativeOutput:
        """Construct the final output model for the service"""
        
        # Calculate speech text based on language
        speech_text = self._generate_speech_text(language, equipment, pools, reminders)
        
        # Determine overall urgency
        urgency = UrgencyLevel.LOW
        if any(r.title == "Return Deadline Today" for r in reminders):
            urgency = UrgencyLevel.HIGH
        elif reminders:
            urgency = UrgencyLevel.MEDIUM
            
        header = "Collaborative Farming" if language == Language.ENGLISH else "सहयोगी खेती"
        
        reasoning = f"Showing {len(equipment)} equipment nearby and {len(pools)} open pooling requests."
        
        return CollaborativeOutput(
            header=header,
            language=language,
            speechText=speech_text,
            equipmentCards=equipment,
            rentalCards=rentals,
            landPoolCards=pools,
            residueCards=residue,
            remindersSuggested=reminders,
            detailedReasoning=reasoning,
            urgencyLevel=urgency
        )

    def _generate_speech_text(
        self, 
        language: Language, 
        equipment: List[EquipmentListing], 
        pools: List[LandPoolRequest],
        reminders: List[ReminderRecord]
    ) -> str:
        """Generate localized speech text for voice-first experience"""
        
        if language == Language.HINDI:
            text = f"आपके क्षेत्र में {len(equipment)} उपकरण किराए पर उपलब्ध हैं। "
            if pools:
                text += f"{len(pools)} लैंड पूलिंग अनुरोध भी खुले हैं। "
            if reminders:
                text += "आपके पास उपकरण वापसी के लिए रिमाइंडर हैं।"
            return text
        else:
            text = f"There are {len(equipment)} equipment available near you. "
            if pools:
                text += f"{len(pools)} land pooling requests are open. "
            if reminders:
                text += "You have reminders for equipment return."
            return text
        
