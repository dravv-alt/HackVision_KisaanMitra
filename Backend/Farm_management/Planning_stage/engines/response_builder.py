"""
Response Builder - formats voice-first multilingual output
"""
from typing import List
from ..models import (
    PreSeedingOutput, EnvironmentalContext, CropRecommendation,
    SchemeEligibilityResult, ReminderRecord, FarmerProfile
)
from ..constants import Language, UrgencyLevel


class ResponseBuilder:
    """Builds final voice-first output for UI/voice assistant"""
    
    def __init__(self):
        """Initialize response builder"""
        pass
    
    def build_output(
        self,
        farmer: FarmerProfile,
        weather: EnvironmentalContext,
        crops: List[CropRecommendation],
        schemes: List[SchemeEligibilityResult],
        reminders: List[ReminderRecord]
    ) -> PreSeedingOutput:
        """
        Build complete pre-seeding output
        
        Args:
            farmer: Farmer profile
            weather: Weather context
            crops: Recommended crops
            schemes: Scheme eligibility results
            reminders: Generated reminders
            
        Returns:
            PreSeedingOutput ready for UI/voice
        """
        language = farmer.language
        
        # Determine urgency
        urgency = self._calculate_urgency(schemes)
        
        # Build components
        header = self._build_header(language)
        weather_summary = self._build_weather_summary(weather, language)
        speech_text = self._build_speech_text(crops, schemes, urgency, language)
        detailed_reasoning = self._build_detailed_reasoning(crops, schemes, language)
        
        return PreSeedingOutput(
            header=header["en"],
            header_hi=header["hi"],
            language=language,
            speech_text=speech_text["en"],
            speech_text_hi=speech_text["hi"],
            weather_summary=weather_summary["en"],
            weather_summary_hi=weather_summary["hi"],
            crop_cards=crops,
            scheme_cards=schemes[:5],  # Top 5 schemes
            reminders=reminders,
            detailed_reasoning=detailed_reasoning,
            urgency_level=urgency
        )
    
    def _calculate_urgency(self, schemes: List[SchemeEligibilityResult]) -> UrgencyLevel:
        """Calculate urgency level from scheme deadlines"""
        critical_count = 0
        urgent_count = 0
        
        for scheme in schemes:
            if not scheme.eligible:
                continue
            
            if scheme.deadline_warning:
                if "days left" in scheme.deadline_warning.lower():
                    # Extract days
                    try:
                        import re
                        match = re.search(r'(\d+)\s+days?', scheme.deadline_warning)
                        if match:
                            days = int(match.group(1))
                            if days <= 1:
                                critical_count += 1
                            elif days <= 7:
                                urgent_count += 1
                    except:
                        pass
        
        if critical_count > 0:
            return UrgencyLevel.CRITICAL
        elif urgent_count > 0:
            return UrgencyLevel.HIGH
        elif len([s for s in schemes if s.eligible]) > 0:
            return UrgencyLevel.MEDIUM
        else:
            return UrgencyLevel.LOW
    
    def _build_header(self, language: Language) -> dict:
        """Build greeting header"""
        return {
            "en": "🌾 Your Pre-Seeding Planning Report",
            "hi": "🌾 आपकी बुवाई-पूर्व योजना रिपोर्ट"
        }
    
    def _build_weather_summary(self, weather: EnvironmentalContext, language: Language) -> dict:
        """Build weather summary"""
        temp = weather.temperature_c
        rain = weather.rain_mm_next_7_days
        
        # English
        en_parts = [f"Temperature: {temp}°C"]
        if weather.rain_forecast:
            en_parts.append(f"Expected rainfall: {rain}mm in next 7 days")
        else:
            en_parts.append("No significant rainfall expected")
        
        if weather.alerts:
            en_parts.extend(weather.alerts)
        
        en_summary = ". ".join(en_parts) + "."
        
        # Hindi
        hi_parts = [f"तापमान: {temp}°C"]
        if weather.rain_forecast:
            hi_parts.append(f"अगले 7 दिनों में अनुमानित वर्षा: {rain}mm")
        else:
            hi_parts.append("कोई विशेष वर्षा की संभावना नहीं")
        
        hi_summary = "। ".join(hi_parts) + "।"
        
        return {"en": en_summary, "hi": hi_summary}
    
    def _build_speech_text(
        self,
        crops: List[CropRecommendation],
        schemes: List[SchemeEligibilityResult],
        urgency: UrgencyLevel,
        language: Language
    ) -> dict:
        """Build concise speech text for voice assistant"""
        eligible_schemes = [s for s in schemes if s.eligible]
        urgent_schemes = [s for s in eligible_schemes if s.deadline_warning and "days left" in s.deadline_warning.lower()]
        
        # English
        en_parts = []
        
        if not crops:
            en_parts.append("No suitable crops found for current conditions.")
        else:
            top_crop = crops[0]
            en_parts.append(f"Top recommendation: {top_crop.crop_name} with {top_crop.score:.0f}% suitability.")
            en_parts.append(f"It offers {top_crop.profit_level.value} profit potential.")
        
        if urgent_schemes:
            scheme_names = ", ".join([s.scheme_name for s in urgent_schemes[:2]])
            en_parts.append(f"⚠️ URGENT: Apply for {scheme_names} before deadline!")
        elif eligible_schemes:
            en_parts.append(f"You are eligible for {len(eligible_schemes)} government schemes.")
        
        en_parts.append("Check full report for details.")
        en_speech = " ".join(en_parts)
        
        # Hindi
        hi_parts = []
        
        if not crops:
            hi_parts.append("वर्तमान परिस्थितियों के लिए कोई उपयुक्त फसल नहीं मिली।")
        else:
            top_crop = crops[0]
            crop_name_hi = top_crop.crop_name_hi or top_crop.crop_name
            hi_parts.append(f"शीर्ष सिफारिश: {crop_name_hi} {top_crop.score:.0f}% उपयुक्तता के साथ।")
            hi_parts.append(f"यह {top_crop.profit_level.value} लाभ क्षमता प्रदान करता है।")
        
        if urgent_schemes:
            scheme_names_hi = ", ".join([
                s.scheme_name_hi or s.scheme_name for s in urgent_schemes[:2]
            ])
            hi_parts.append(f"⚠️ तत्काल: समय सीमा से पहले {scheme_names_hi} के लिए आवेदन करें!")
        elif eligible_schemes:
            hi_parts.append(f"आप {len(eligible_schemes)} सरकारी योजनाओं के लिए पात्र हैं।")
        
        hi_parts.append("विवरण के लिए पूरी रिपोर्ट देखें।")
        hi_speech = " ".join(hi_parts)
        
        return {"en": en_speech, "hi": hi_speech}
    
    def _build_detailed_reasoning(
        self,
        crops: List[CropRecommendation],
        schemes: List[SchemeEligibilityResult],
        language: Language
    ) -> str:
        """Build detailed reasoning section"""
        if language == Language.HINDI:
            return self._build_detailed_reasoning_hi(crops, schemes)
        else:
            return self._build_detailed_reasoning_en(crops, schemes)
    
    def _build_detailed_reasoning_en(
        self,
        crops: List[CropRecommendation],
        schemes: List[SchemeEligibilityResult]
    ) -> str:
        """Build detailed reasoning in English"""
        parts = ["## Detailed Analysis\n"]
        
        # Crop reasoning
        parts.append("### Crop Recommendations\n")
        for i, crop in enumerate(crops, 1):
            parts.append(f"**{i}. {crop.crop_name}** (Score: {crop.score:.1f}/100)")
            parts.append(f"- Profit Level: {crop.profit_level.value.title()}")
            parts.append(f"- Why recommended: {', '.join(crop.reasons)}")
            if crop.risks:
                parts.append(f"- Risks: {', '.join(crop.risks)}")
            parts.append("")
        
        # Scheme reasoning
        eligible_schemes = [s for s in schemes if s.eligible]
        if eligible_schemes:
            parts.append("### Eligible Schemes\n")
            for scheme in eligible_schemes[:3]:
                parts.append(f"**{scheme.scheme_name}**")
                parts.append(f"- Why eligible: {'; '.join(scheme.why_eligible)}")
                if scheme.deadline_warning:
                    parts.append(f"- {scheme.deadline_warning}")
                parts.append("")
        
        return "\n".join(parts)
    
    def _build_detailed_reasoning_hi(
        self,
        crops: List[CropRecommendation],
        schemes: List[SchemeEligibilityResult]
    ) -> str:
        """Build detailed reasoning in Hindi"""
        parts = ["## विस्तृत विश्लेषण\n"]
        
        # Crop reasoning
        parts.append("### फसल सिफारिशें\n")
        for i, crop in enumerate(crops, 1):
            crop_name = crop.crop_name_hi or crop.crop_name
            parts.append(f"**{i}. {crop_name}** (स्कोर: {crop.score:.1f}/100)")
            parts.append(f"- लाभ स्तर: {crop.profit_level.value}")
            parts.append(f"- क्यों सिफारिश की गई: {', '.join(crop.reasons)}")
            if crop.risks:
                parts.append(f"- जोखिम: {', '.join(crop.risks)}")
            parts.append("")
        
        # Scheme reasoning
        eligible_schemes = [s for s in schemes if s.eligible]
        if eligible_schemes:
            parts.append("### पात्र योजनाएं\n")
            for scheme in eligible_schemes[:3]:
                scheme_name = scheme.scheme_name_hi or scheme.scheme_name
                parts.append(f"**{scheme_name}**")
                parts.append(f"- पात्रता: {'; '.join(scheme.why_eligible)}")
                if scheme.deadline_warning:
                    parts.append(f"- {scheme.deadline_warning}")
                parts.append("")
        
        return "\n".join(parts)
