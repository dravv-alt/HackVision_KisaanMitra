"""
Retriever - RAG-style information retrieval
"""

from typing import List, Dict, Any
from Backend.Voice_agent.core.intent import Intent
from Backend.Voice_agent.retrieval.weather_service import get_weather_service
from Backend.Voice_agent.retrieval.market_service import get_market_service

# Optional imports - graceful fallback if not available
try:
    from Backend.Voice_agent.retrieval.sources import get_knowledge_registry
except ImportError:
    get_knowledge_registry = None

try:
    from Backend.Voice_agent.retrieval.vector_store import get_vector_store
except ImportError:
    get_vector_store = None


class Retriever:
    """RAG-style retriever using Vector DB (Chroma) and specialized services"""
    
    def __init__(self):
        # Optional components - only initialize if available
        self.registry = get_knowledge_registry() if get_knowledge_registry else None
        self.vector_store = get_vector_store() if get_vector_store else None
        self.weather_service = get_weather_service()
        self.market_service = get_market_service()
    
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
            # RAG Search for crops
            retrieved.extend(self._retrieve_crop_info(query_text, context))
            # Weather for context
            retrieved.extend(self._retrieve_weather_info())
            # Market for context
            retrieved.extend(self._retrieve_market_info(query_text))
        
        elif intent == Intent.FINANCE_REPORT or intent == Intent.COST_ANALYSIS or intent == Intent.OPTIMIZATION_ADVICE:
             # Try retrieving semantic financial context
             retrieved.extend(self._retrieve_financial_info(query_text))

        elif intent == Intent.STORAGE_DECISION or intent == Intent.SELLING_DECISION:
            retrieved.extend(self._retrieve_market_info(query_text))
        
        elif intent == Intent.GOVERNMENT_SCHEME:
            retrieved.extend(self._retrieve_scheme_info(query_text, context))
        
        elif intent == Intent.WEATHER_QUERY:
            retrieved.extend(self._retrieve_weather_info())
        
        elif intent == Intent.MARKET_PRICE:
            retrieved.extend(self._retrieve_market_info(query_text))
            
        elif intent == Intent.FOLLOW_UP or intent == Intent.UNKNOWN:
            # For general conversation, search history
            retrieved.extend(self._retrieve_conversation_history(query_text))
        
        return retrieved
    
    def _retrieve_crop_info(self, query: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Retrieve crop information via Vector Search"""
        # If vector store not available, return empty
        if not self.vector_store:
            return []
        
        # If query is very generic, ensure we get some results
        search_query = query if len(query) > 5 else "best crops for this season"
        
        results = self.vector_store.search(
            query=search_query,
            limit=5,
            type_filter="crop_info"
        )
        
        # Map vector results to document format
        docs = []
        for res in results:
            docs.append({
                "source": "vector_db",
                "type": "crop_info",
                "data": res["data"],
                "score": res["distance"] 
            })
            
        return docs
    
    def _retrieve_weather_info(self) -> List[Dict[str, Any]]:
        """Retrieve weather information via Live Service"""
        weather_data = self.weather_service.get_current_weather()
        
        return [{
            "source": weather_data.get("source", "weather_service"),
            "type": "weather_info",
            "data": weather_data
        }]
    
    def _retrieve_market_info(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve market information via Live Service"""
        # Extract commodity from query if possible (simple heuristic)
        # In a real app, use an LLM or NER to extract key entity
        commodity = None
        for crop in ["wheat", "rice", "cotton", "onion", "soybean", "maize"]:
            if crop in query.lower():
                commodity = crop
                break
        
        market_data_list = self.market_service.get_market_prices(commodity=commodity)
        
        docs = []
        for data in market_data_list:
            docs.append({
                "source": data.get("source", "market_service"),
                "type": "market_price",
                "crop": data.get("crop", "Unknown"),
                "data": data
            })
        
        return docs
    
    def _retrieve_scheme_info(self, query: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Retrieve government scheme information via Vector Search"""
        # If vector store not available, return empty
        if not self.vector_store:
            return []
        
        results = self.vector_store.search(
            query=query,
            limit=3,
            type_filter="scheme_info"
        )
        
        docs = []
        for res in results:
            docs.append({
                "source": "vector_db",
                "type": "scheme_info",
                "data": res["data"]
            })
        
        return docs

    def _retrieve_conversation_history(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant conversation history"""
        if not self.vector_store:
            return []
            
        results = self.vector_store.search(
            query=query,
            limit=3,
            type_filter="conversation"
        )
        
        docs = []
        for res in results:
            docs.append({
                "source": "memory_rag",
                "type": "conversation_history",
                "data": res["data"],
                "text": res["text"]
            })
        return docs

    def _retrieve_financial_info(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve financial context"""
        if not self.vector_store:
            return []
            
        results = self.vector_store.search(
            query=query,
            limit=2,
            type_filter="financial_info"
        )
        
        docs = []
        for res in results:
            docs.append({
                "source": "financial_rag",
                "type": "financial_info",
                "data": res["data"],
                "text": res["text"]
            })
        return docs


# Singleton instance
_retriever = None

def get_retriever() -> Retriever:
    """Get or create retriever instance"""
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever
