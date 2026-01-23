"""
Knowledge Sources - Registry of knowledge sources for RAG
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class KnowledgeSource:
    """Knowledge source definition"""
    source_id: str
    name: str
    description: str
    keywords: List[str]
    data: Dict[str, Any]


class KnowledgeSourceRegistry:
    """Registry of all knowledge sources"""
    
    def __init__(self):
        self.sources: Dict[str, KnowledgeSource] = {}
        self._initialize_sources()
    
    def _initialize_sources(self):
        """Initialize mock knowledge sources"""
        
        # Crop knowledge
        self.sources["crops"] = KnowledgeSource(
            source_id="crops",
            name="Crop Database",
            description="Information about crops, requirements, and characteristics",
            keywords=["crop", "फसल", "plant", "grow"],
            data={
                "wheat": {
                    "name": "Wheat",
                    "name_hindi": "गेहूं",
                    "suitable_soil": ["alluvial", "loamy"],
                    "season": "rabi",
                    "water_requirement": "medium",
                    "profit_potential": "medium",
                },
                "rice": {
                    "name": "Rice",
                    "name_hindi": "धान",
                    "suitable_soil": ["clay", "loamy"],
                    "season": "kharif",
                    "water_requirement": "high",
                    "profit_potential": "medium",
                },
                "cotton": {
                    "name": "Cotton",
                    "name_hindi": "कपास",
                    "suitable_soil": ["black", "alluvial"],
                    "season": "kharif",
                    "water_requirement": "medium",
                    "profit_potential": "high",
                },
            }
        )
        
        # Weather knowledge
        self.sources["weather"] = KnowledgeSource(
            source_id="weather",
            name="Weather Information",
            description="Current weather and forecasts",
            keywords=["weather", "मौसम", "rain", "temperature"],
            data={
                "current": {
                    "temperature": 28.0,
                    "humidity": 65.0,
                    "rain_forecast": False,
                    "advisory": "Good weather for farming activities"
                }
            }
        )
        
        # Market knowledge
        self.sources["market"] = KnowledgeSource(
            source_id="market",
            name="Market Prices",
            description="Current market prices and trends",
            keywords=["market", "price", "कीमत", "बाजार"],
            data={
                "wheat": {"price": 25.0, "trend": "rising"},
                "rice": {"price": 30.0, "trend": "stable"},
                "cotton": {"price": 60.0, "trend": "rising"},
                "onion": {"price": 35.0, "trend": "rising"},
            }
        )
        
        # Government schemes
        self.sources["schemes"] = KnowledgeSource(
            source_id="schemes",
            name="Government Schemes",
            description="Government schemes and eligibility",
            keywords=["scheme", "योजना", "government", "subsidy"],
            data={
                "pm-kisan": {
                    "name": "PM-KISAN",
                    "name_hindi": "पीएम-किसान",
                    "description": "Direct income support",
                    "eligibility": "All farmers with land",
                },
                "pmfby": {
                    "name": "PMFBY",
                    "name_hindi": "प्रधानमंत्री फसल बीमा योजना",
                    "description": "Crop insurance",
                    "eligibility": "All farmers",
                },
            }
        )
    
    def get_source(self, source_id: str) -> KnowledgeSource:
        """Get knowledge source by ID"""
        return self.sources.get(source_id)
    
    def search_sources(self, keywords: List[str]) -> List[KnowledgeSource]:
        """Search sources by keywords"""
        matching_sources = []
        
        for source in self.sources.values():
            for keyword in keywords:
                if any(kw.lower() in keyword.lower() for kw in source.keywords):
                    matching_sources.append(source)
                    break
        
        return matching_sources


# Singleton instance
_registry = None

def get_knowledge_registry() -> KnowledgeSourceRegistry:
    """Get or create knowledge source registry"""
    global _registry
    if _registry is None:
        _registry = KnowledgeSourceRegistry()
    return _registry
