"""
Response Builder - Human-Centric Output Generation
"""

from typing import List, Dict
from ..models import AlertRecord, AlertsOutput
from ..constants import AlertUrgency, Language


class ResponseBuilder:
    def build_output(self, language: Language, alerts: List[AlertRecord]) -> AlertsOutput:
        """
        Create the final localized output with voice and UI elements.
        """
        # Calculate summary counts
        summary = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        max_urgency = AlertUrgency.LOW
        
        urgency_map = {
            AlertUrgency.CRITICAL: 4,
            AlertUrgency.HIGH: 3,
            AlertUrgency.MEDIUM: 2,
            AlertUrgency.LOW: 1
        }
        
        for a in alerts:
            summary[a.urgency.value] += 1
            if urgency_map[a.urgency] > urgency_map[max_urgency]:
                max_urgency = a.urgency
        
        # Build speech text (Voice-First)
        speech = self._generate_speech(language, alerts)
        header = "Alerts Center" if language == Language.ENGLISH else "अलर्ट केंद्र"
        
        # Detailed reasoning
        reasoning = (f"Currently tracking {len(alerts)} updates across weather, irrigation, and market price categories."
                     if language == Language.ENGLISH else
                     f"मौसम, सिंचाई और बाज़ार मूल्य श्रेणियों में {len(alerts)} अपडेट्स ट्रैक किए जा रहे हैं।")
        
        return AlertsOutput(
            header=header,
            language=language,
            speechText=speech,
            alerts=alerts,
            summaryCounts=summary,
            detailedReasoning=reasoning,
            urgencyLevel=max_urgency
        )

    def _generate_speech(self, language: Language, alerts: List[AlertRecord]) -> str:
        if not alerts:
            return ("You have no new alerts." if language == Language.ENGLISH else 
                    "आपके पास कोई नया अलर्ट नहीं है।")
        
        top_alert = alerts[0]
        count = len(alerts)
        
        if language == Language.ENGLISH:
            msg = f"You have {count} alerts today. "
            if count > 0:
                msg += f"Most important: {top_alert.message}"
            return msg
        else:
            msg = f"आपके लिए आज {count} अलर्ट हैं। "
            if count > 0:
                msg += f"सबसे महत्वपूर्ण: {top_alert.message}"
            return msg
