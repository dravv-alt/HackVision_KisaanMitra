"""
Response Builder - UI Output Generation
"""

from typing import List
from datetime import datetime

from ..models import SchemeRecord, SchemeCardOutput, GovSchemesOutput, FarmerProfile
from ..constants import Language, SchemeCategory, CATEGORY_DISPLAY_NAMES


class ResponseBuilder:
    """Engine for building UI-ready responses"""
    
    def build(
        self,
        farmer: FarmerProfile,
        schemes: List[SchemeRecord],
        new_schemes_count: int,
        filter_applied: dict
    ) -> GovSchemesOutput:
        """
        Build complete government schemes display output
        
        Args:
            farmer: Farmer profile
            schemes: Filtered list of schemes
            new_schemes_count: Count of new schemes
            filter_applied: Dictionary of applied filters
            
        Returns:
            Complete GovSchemesOutput for UI
        """
        language = farmer.language
        
        # Convert schemes to cards
        scheme_cards = self._build_scheme_cards(schemes, language)
        
        # Generate speech text
        speech_text = self._generate_speech_text(
            language,
            len(schemes),
            new_schemes_count,
            filter_applied
        )
        
        # Generate header
        header = self._generate_header(language, len(schemes))
        
        # Generate detailed reasoning
        detailed_reasoning = self._generate_detailed_reasoning(
            language,
            schemes,
            new_schemes_count,
            filter_applied
        )
        
        return GovSchemesOutput(
            header=header,
            language=language,
            speechText=speech_text,
            schemeCards=scheme_cards,
            totalSchemes=len(schemes),
            newSchemesCount=new_schemes_count,
            filterApplied=filter_applied,
            detailedReasoning=detailed_reasoning
        )
    
    def _build_scheme_cards(
        self,
        schemes: List[SchemeRecord],
        language: Language
    ) -> List[SchemeCardOutput]:
        """Convert scheme records to UI cards"""
        cards = []
        now = datetime.now()
        
        # Determine which schemes are new (created in last 7 days)
        for scheme in schemes:
            days_since_created = (now - scheme.createdAt).days
            is_new = days_since_created <= 7
            
            # Calculate days remaining if end date exists
            days_remaining = None
            if scheme.endDate:
                days_remaining = (scheme.endDate - now).days
            
            # Determine scope
            if scheme.district:
                scope = f"{scheme.district} District"
            elif scheme.state:
                scope = f"{scheme.state} State"
            else:
                if language == Language.HINDI:
                    scope = "पूरे भारत"
                else:
                    scope = "All India"
            
            # Get category display name
            category_display = CATEGORY_DISPLAY_NAMES.get(
                scheme.category, {}
            ).get(language.value, scheme.category.value)
            
            # Select language-appropriate fields
            if language == Language.HINDI:
                name = scheme.schemeNameHindi or scheme.schemeName
                description = scheme.descriptionHindi or scheme.description
                benefits = scheme.benefitsHindi or scheme.benefits
                eligibility = scheme.eligibilityHindi or scheme.eligibility
                how_to_apply = scheme.howToApplyHindi or scheme.howToApply
            else:
                name = scheme.schemeName
                description = scheme.description
                benefits = scheme.benefits
                eligibility = scheme.eligibility
                how_to_apply = scheme.howToApply
            
            card = SchemeCardOutput(
                schemeId=scheme.schemeId,
                schemeName=name,
                category=scheme.category,
                categoryDisplay=category_display,
                description=description,
                benefits=benefits,
                eligibility=eligibility,
                howToApply=how_to_apply,
                officialLink=scheme.officialLink,
                contactNumber=scheme.contactNumber,
                scope=scope,
                isNew=is_new,
                daysRemaining=days_remaining
            )
            cards.append(card)
        
        return cards
    
    def _generate_speech_text(
        self,
        language: Language,
        total_schemes: int,
        new_schemes_count: int,
        filter_applied: dict
    ) -> str:
        """Generate voice-friendly speech text"""
        if language == Language.HINDI:
            if total_schemes == 0:
                return "आपके क्षेत्र के लिए कोई योजना उपलब्ध नहीं है।"
            
            speech = f"आपके लिए {total_schemes} सरकारी योजनाएं उपलब्ध हैं। "
            
            if new_schemes_count > 0:
                speech += f"{new_schemes_count} नई योजनाएं हाल ही में जोड़ी गई हैं। "
            
            # Mention filters
            if filter_applied.get("state"):
                speech += f"{filter_applied['state']} राज्य के लिए। "
            
            if filter_applied.get("category"):
                cat_name = CATEGORY_DISPLAY_NAMES.get(
                    filter_applied["category"], {}
                ).get("hi", "")
                if cat_name:
                    speech += f"{cat_name} श्रेणी। "
            
            speech += "अधिक जानकारी के लिए योजना कार्ड देखें।"
            
        else:  # English
            if total_schemes == 0:
                return "No schemes available for your region."
            
            speech = f"You have {total_schemes} government schemes available. "
            
            if new_schemes_count > 0:
                speech += f"{new_schemes_count} new schemes were recently added. "
            
            # Mention filters
            if filter_applied.get("state"):
                speech += f"For {filter_applied['state']} state. "
            
            if filter_applied.get("category"):
                cat_name = CATEGORY_DISPLAY_NAMES.get(
                    filter_applied["category"], {}
                ).get("en", "")
                if cat_name:
                    speech += f"{cat_name} category. "
            
            speech += "View scheme cards for more details."
        
        return speech.strip()
    
    def _generate_header(self, language: Language, total_schemes: int) -> str:
        """Generate dashboard header"""
        if language == Language.HINDI:
            return f"सरकारी योजनाएं - {total_schemes} योजनाएं"
        else:
            return f"Government Schemes - {total_schemes} Schemes"
    
    def _generate_detailed_reasoning(
        self,
        language: Language,
        schemes: List[SchemeRecord],
        new_schemes_count: int,
        filter_applied: dict
    ) -> str:
        """Generate detailed reasoning for display"""
        if language == Language.HINDI:
            reasoning = "योजना सूची:\n\n"
            
            if new_schemes_count > 0:
                reasoning += f"🆕 {new_schemes_count} नई योजनाएं उपलब्ध हैं।\n"
            
            # Group by category
            categories = {}
            for scheme in schemes:
                cat = scheme.category
                if cat not in categories:
                    categories[cat] = 0
                categories[cat] += 1
            
            reasoning += "\nश्रेणी के अनुसार:\n"
            for cat, count in categories.items():
                cat_name = CATEGORY_DISPLAY_NAMES.get(cat, {}).get("hi", cat.value)
                reasoning += f"  • {cat_name}: {count} योजनाएं\n"
            
            if filter_applied.get("state") or filter_applied.get("district"):
                reasoning += "\nफ़िल्टर लागू: "
                if filter_applied.get("district"):
                    reasoning += f"{filter_applied['district']} जिला"
                elif filter_applied.get("state"):
                    reasoning += f"{filter_applied['state']} राज्य"
            
        else:  # English
            reasoning = "Scheme List:\n\n"
            
            if new_schemes_count > 0:
                reasoning += f"🆕 {new_schemes_count} new schemes available.\n"
            
            # Group by category
            categories = {}
            for scheme in schemes:
                cat = scheme.category
                if cat not in categories:
                    categories[cat] = 0
                categories[cat] += 1
            
            reasoning += "\nBy Category:\n"
            for cat, count in categories.items():
                cat_name = CATEGORY_DISPLAY_NAMES.get(cat, {}).get("en", cat.value)
                reasoning += f"  • {cat_name}: {count} schemes\n"
            
            if filter_applied.get("state") or filter_applied.get("district"):
                reasoning += "\nFilter Applied: "
                if filter_applied.get("district"):
                    reasoning += f"{filter_applied['district']} District"
                elif filter_applied.get("state"):
                    reasoning += f"{filter_applied['state']} State"
        
        return reasoning
