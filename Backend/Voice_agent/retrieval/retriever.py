"""
Retriever - RAG-style information retrieval
"""

from typing import List, Dict, Any
from voice_agent.core.intent import Intent
from voice_agent.retrieval.sources import get_knowledge_registry, KnowledgeSource


class Retriever:
    """RAG-style retriever for knowledge sources"""
    
    def __init__(self):
        self.registry = get_knowledge_registry()
    
    def retrieve(
        self,
        intent: Intent,
        query_text: str,
        context: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant information based on intent and query
        
        Args:
            intent: Detected intent
            query_text: Query text
            context: Additional context
        
        Returns:
            List of retrieved documents/facts
        """
        retrieved = []
        
        # Intent-based retrieval
        if intent == Intent.CROP_PLANNING:
            retrieved.extend(self._retrieve_crop_info(query_text, context))
            retrieved.extend(self._retrieve_weather_info())
            retrieved.extend(self._retrieve_market_info(query_text))
        
        elif intent == Intent.STORAGE_DECISION or intent == Intent.SELLING_DECISION:
            retrieved.extend(self._retrieve_market_info(query_text))
        
        elif intent == Intent.GOVERNMENT_SCHEME:
            retrieved.extend(self._retrieve_scheme_info(query_text, context))
        
        elif intent == Intent.WEATHER_QUERY:
            retrieved.extend(self._retrieve_weather_info())
        
        elif intent == Intent.MARKET_PRICE:
            retrieved.extend(self._retrieve_market_info(query_text))
        
        return retrieved
    
    def _retrieve_crop_info(self, query: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Retrieve crop information"""
        source = self.registry.get_source("crops")
        if not source:
            return []
        
        results = []
        for crop_id, crop_data in source.data.items():
            results.append({
                "source": "crops",
                "type": "crop_info",
                "data": crop_data
            })
        
        return results
    
    def _retrieve_weather_info(self) -> List[Dict[str, Any]]:
        """Retrieve weather information"""
        source = self.registry.get_source("weather")
        if not source:
            return []
        
        return [{
            "source": "weather",
            "type": "weather_info",
            "data": source.data["current"]
        }]
    
    def _retrieve_market_info(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve market information"""
        source = self.registry.get_source("market")
        if not source:
            return []
        
        results = []
        for crop, price_data in source.data.items():
            results.append({
                "source": "market",
                "type": "market_price",
                "crop": crop,
                "data": price_data
            })
        
        return results
    
    def _retrieve_scheme_info(self, query: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Retrieve government scheme information"""
        source = self.registry.get_source("schemes")
        if not source:
            return []
        
        results = []
        for scheme_id, scheme_data in source.data.items():
            results.append({
                "source": "schemes",
                "type": "scheme_info",
                "data": scheme_data
            })
        
        return results


# Singleton instance
_retriever = None

def get_retriever() -> Retriever:
    """Get or create retriever instance"""
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever
