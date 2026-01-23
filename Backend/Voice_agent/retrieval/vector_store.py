"""
Vector Store - Semantic Search Engine using ChromaDB
Stores and retrieves knowledge about crops, schemes, etc.
"""

import chromadb
from chromadb.utils import embedding_functions
import os
from typing import List, Dict, Any, Optional
import json

class VectorStore:
    """
    ChromaDB-based vector store for semantic search
    """
    
    def __init__(self, persist_path: str = "chroma_db"):
        """
        Initialize Vector Store
        
        Args:
            persist_path: Path to store ChromaDB data
        """
        # Initialize client
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        full_path = os.path.join(base_path, persist_path)
        
        self.client = chromadb.PersistentClient(path=full_path)
        
        # Use default MiniLM-L6-v2 embeddings (lightweight, runs on CPU)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="farming_knowledge",
            embedding_function=self.embedding_fn
        )
        
        # Bootstrap if empty
        if self.collection.count() == 0:
            print("🚀 Bootstrapping Vector DB with initial knowledge...")
            self._bootstrap_knowledge()
        else:
            print(f"✅ Vector DB loaded with {self.collection.count()} documents")
            
    def _bootstrap_knowledge(self):
        """Bootstrap vector DB with data from KnowledgeSourceRegistry"""
        from voice_agent.retrieval.sources import get_knowledge_registry
        
        registry = get_knowledge_registry()
        documents = []
        metadatas = []
        ids = []
        
        # 1. Ingest Crops
        crops = registry.get_source("crops")
        if crops:
            for crop_id, data in crops.data.items():
                # create a rich text description for embedding
                text = f"{data['name']} ({data['name_hindi']}). "
                text += f"Suitable soil: {', '.join(data['suitable_soil'])}. "
                text += f"Season: {data['season']}. "
                text += f"Requirements: {data['water_requirement']} water. "
                
                documents.append(text)
                metadatas.append({
                    "type": "crop_info",
                    "id": crop_id,
                    "name": data["name"],
                    "data_json": json.dumps(data)  # Store full data for retrieval
                })
                ids.append(f"crop_{crop_id}")
                
        # 2. Ingest Schemes
        schemes = registry.get_source("schemes")
        if schemes:
            for scheme_id, data in schemes.data.items():
                text = f"{data['name']} ({data['name_hindi']}). "
                text += f"{data['description']}. "
                text += f"Eligibility: {data['eligibility']}."
                
                documents.append(text)
                metadatas.append({
                    "type": "scheme_info",
                    "id": scheme_id,
                    "name": data["name"],
                    "data_json": json.dumps(data)
                })
                ids.append(f"scheme_{scheme_id}")
        
        # Add to collection
        if documents:
            self.collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ Bootstrapped {len(documents)} documents into Vector DB")
            
    def search(self, query: str, limit: int = 3, type_filter: str = None) -> List[Dict[str, Any]]:
        """
        Semantic search
        
        Args:
            query: Search query
            limit: Number of results
            type_filter: Optional filter by 'type' metadata (e.g. 'crop_info')
            
        Returns:
            List of results with data
        """
        where = {"type": type_filter} if type_filter else None
        
        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where=where
        )
        
        parsed_results = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                meta = results["metadatas"][0][i]
                
                # Parse stored JSON data back to dict
                data = json.loads(meta["data_json"]) if "data_json" in meta else {}
                
                parsed_results.append({
                    "text": doc,
                    "type": meta["type"],
                    "id": meta["id"],
                    "name": meta["name"],
                    "data": data,
                    "distance": results["distances"][0][i] if "distances" in results else 0
                })
                
        return parsed_results

    def add_text(self, text: str, metadata: Dict[str, Any], doc_id: str):
        """Generic method to add text to vector store"""
        # Ensure ID is unique string
        doc_id = str(doc_id)
        
        # Serialize complex nested data in metadata
        if "data" in metadata:
            metadata["data_json"] = json.dumps(metadata.pop("data"))
            
        self.collection.upsert(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        # print(f"✓ Ingested doc {doc_id} into Vector DB")

    def ingest_scheme(self, scheme_data: Dict[str, Any]):
        """Ingest single scheme"""
        scheme_id = scheme_data.get("id") or scheme_data.get("name")
        text = f"{scheme_data.get('name')} ({scheme_data.get('name_hindi')}). "
        text += f"{scheme_data.get('description')}. "
        text += f"Eligibility: {scheme_data.get('eligibility')}."
        
        self.add_text(
            text=text,
            metadata={
                "type": "scheme_info",
                "id": str(scheme_id),
                "name": scheme_data.get("name"),
                "data": scheme_data
            },
            doc_id=f"scheme_{scheme_id}"
        )

    def ingest_financial_summary(self, summary_data: Dict[str, Any]):
        """Ingest financial summary"""
        season = summary_data.get("season", "Current")
        text = f"Financial Summary for {season}. "
        text += f"Total Income: {summary_data.get('totalIncome')}. "
        text += f"Total Expense: {summary_data.get('totalExpense')}. "
        text += f"Profit: {summary_data.get('profitOrLoss')}. "
        
        # Add high cost reasoning for context
        if summary_data.get("lossCauses"):
            text += f"Issues: {', '.join([c.get('description') for c in summary_data.get('lossCauses', [])])}"

        self.add_text(
            text=text,
            metadata={
                "type": "financial_info",
                "id": f"fin_{season}",
                "name": f"Finance {season}",
                "data": summary_data
            },
            doc_id=f"fin_{season}_{summary_data.get('timestamp', '')}"
        )

    def ingest_conversation_turn(self, turn_data: Dict[str, Any]):
        """Ingest conversation history"""
        # We only want to index semantic content, not system metadata
        user_text = turn_data.get("user_input_english")
        agent_text = turn_data.get("agent_response_english")
        turn_id = turn_data.get("turn_id")
        timestamp = turn_data.get("timestamp")
        
        text = f"User: {user_text}\nAssistant: {agent_text}"
        
        self.add_text(
            text=text,
            metadata={
                "type": "conversation",
                "id": str(turn_id),
                "name": f"Turn {turn_id}",
                "timestamp": str(timestamp), 
                "data": turn_data
            },
            doc_id=f"chat_{turn_id}_{timestamp}"
        )

# Singleton
_vector_store = None

def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
