"""
Scheme Card - Government scheme card
"""

from dataclasses import dataclass
from typing import List
from Voice_agent.cards.base_card import BaseCard


@dataclass
class SchemeCard(BaseCard):
    """Government scheme card"""
    
    def __init__(
        self,
        scheme_name: str,
        scheme_name_hindi: str,
        eligible: bool,
        reasons: List[str],
        deadline: str = None,
        **kwargs
    ):
        status = "पात्र हैं" if eligible else "पात्र नहीं हैं"
        
        super().__init__(
            card_type="scheme",
            title=f"{scheme_name} ({scheme_name_hindi})",
            summary=f"आप {status}",
            details={
                "scheme_name": scheme_name,
                "scheme_name_hindi": scheme_name_hindi,
                "eligible": eligible,
                "reasons": reasons,
                "deadline": deadline,
            },
            **kwargs
        )
