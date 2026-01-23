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
        from Backend.Voice_agent.retrieval.sources import get_knowledge_registry
        
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
            self.collection.add(
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

# Singleton
_vector_store = None

def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
