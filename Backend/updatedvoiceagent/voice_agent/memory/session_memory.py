"""
Session Memory - MongoDB-ready short-term memory
Stores conversation turns and can be easily connected to MongoDB
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from voice_agent.core.context import ConversationContext


class SessionMemory:
    """
    Short-term session memory
    MongoDB-ready: Can store/retrieve from MongoDB when connected
    """
    
    def __init__(self, db_client=None):
        """
        Initialize session memory
        
        Args:
            db_client: MongoDB client (optional, uses in-memory if None)
        """
        self.db_client = db_client
        self.use_mongodb = db_client is not None
        
        # In-memory storage (fallback)
        self._memory_store: Dict[str, ConversationContext] = {}
        
        # MongoDB collection name
        self.collection_name = "session_memory"
    
    def save_context(self, context: ConversationContext):
        """
        Save conversation context
        
        Args:
            context: Conversation context to save
        """
        if self.use_mongodb:
            # MongoDB storage
            collection = self.db_client[self.collection_name]
            context_dict = context.to_dict()
            
            # Upsert (update or insert)
            collection.update_one(
                {"session_id": context.session_id},
                {"$set": context_dict},
                upsert=True
            )
        else:
            # In-memory storage
            self._memory_store[context.session_id] = context
    
    def load_context(self, session_id: str) -> Optional[ConversationContext]:
        """
        Load conversation context
        
        Args:
            session_id: Session identifier
        
        Returns:
            Conversation context or None if not found
        """
        if self.use_mongodb:
            # MongoDB retrieval
            collection = self.db_client[self.collection_name]
            doc = collection.find_one({"session_id": session_id})
            
            if doc:
                # Reconstruct context from document
                # (Would need from_dict method in ConversationContext)
                return self._reconstruct_context(doc)
            return None
        else:
            # In-memory retrieval
            return self._memory_store.get(session_id)
    
    def get_recent_sessions(self, farmer_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent sessions for a farmer
        
        Args:
            farmer_id: Farmer identifier
            limit: Maximum number of sessions to return
        
        Returns:
            List of session summaries
        """
        if self.use_mongodb:
            # MongoDB query
            collection = self.db_client[self.collection_name]
            sessions = collection.find(
                {"farmer_id": farmer_id}
            ).sort("last_updated", -1).limit(limit)
            
            return list(sessions)
        else:
            # In-memory query
            farmer_sessions = [
                ctx for ctx in self._memory_store.values()
                if ctx.farmer_profile.farmer_id == farmer_id
            ]
            farmer_sessions.sort(key=lambda x: x.last_updated, reverse=True)
            return [ctx.to_dict() for ctx in farmer_sessions[:limit]]
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        if self.use_mongodb:
            collection = self.db_client[self.collection_name]
            collection.delete_one({"session_id": session_id})
        else:
            self._memory_store.pop(session_id, None)
    
    def clear_old_sessions(self, days: int = 30):
        """
        Clear sessions older than specified days
        
        Args:
            days: Number of days to keep
        """
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        if self.use_mongodb:
            collection = self.db_client[self.collection_name]
            collection.delete_many({
                "last_updated": {"$lt": datetime.fromtimestamp(cutoff).isoformat()}
            })
        else:
            to_delete = [
                sid for sid, ctx in self._memory_store.items()
                if ctx.last_updated.timestamp() < cutoff
            ]
            for sid in to_delete:
                del self._memory_store[sid]
    
    def _reconstruct_context(self, doc: Dict[str, Any]) -> ConversationContext:
        """
        Reconstruct ConversationContext from MongoDB document
        
        Args:
            doc: MongoDB document
        
        Returns:
            Reconstructed conversation context
        """
        # Create new context
        context = ConversationContext(
            farmer_id=doc["farmer_id"],
            session_id=doc["session_id"]
        )
        
        # Restore farmer profile
        profile_data = doc.get("farmer_profile", {})
        context.update_farmer_profile(**profile_data)
        
        # Restore context variables
        context.context_variables = doc.get("context_variables", {})
        context.pending_confirmation = doc.get("pending_confirmation")
        
        # Note: Conversation history reconstruction would require
        # recreating ConversationTurn objects from the stored data
        # Simplified for hackathon - can be enhanced later
        
        return context


# Singleton instance
_session_memory = None

def get_session_memory(db_client=None) -> SessionMemory:
    """
    Get or create session memory instance
    
    Args:
        db_client: MongoDB client (optional)
    
    Returns:
        SessionMemory instance
    """
    global _session_memory
    if _session_memory is None:
        _session_memory = SessionMemory(db_client=db_client)
    return _session_memory
