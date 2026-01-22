"""
inventory Log Repository with Mock Fallback
"""

from datetime import datetime, timedelta
from typing import List, Optional
import uuid

from ..models import inventoryLogEntry
from ..constants import inventoryAction


class inventoryLogRepo:
    """Repository for inventory action logs with mock fallback"""
    
    def __init__(self):
        # Mock in-memory storage (simulates MongoDB collection)
        self._mock_logs: List[inventoryLogEntry] = []
    
    def add_log(self, entry: inventoryLogEntry) -> inventoryLogEntry:
        """Add new log entry"""
        self._mock_logs.append(entry)
        return entry
    
    def list_logs(self, farmer_id: str, item_id: Optional[str] = None) -> List[inventoryLogEntry]:
        """
        List logs for a farmer, optionally filtered by item
        Returns mock data if empty
        """
        logs = [log for log in self._mock_logs if log.farmerId == farmer_id]
        
        if item_id:
            logs = [log for log in logs if log.itemId == item_id]
        
        if not logs:
            # Seed mock data if empty
            self.seed_mock_logs_if_empty(farmer_id)
            logs = [log for log in self._mock_logs if log.farmerId == farmer_id]
            if item_id:
                logs = [log for log in logs if log.itemId == item_id]
        
        return sorted(logs, key=lambda x: x.ts, reverse=True)
    
    def seed_mock_logs_if_empty(self, farmer_id: str):
        """Seed mock log data for testing"""
        now = datetime.now()
        
        # Mock item IDs (would come from inventory in real scenario)
        mock_item_id_1 = "ITEM001"
        mock_item_id_2 = "ITEM002"
        
        mock_logs = [
            inventoryLogEntry(
                logId=str(uuid.uuid4()),
                farmerId=farmer_id,
                itemId=mock_item_id_1,
                action=inventoryAction.ADD,
                quantityKg=500.0,
                notes="Initial harvest storage",
                ts=now - timedelta(days=10),
                createdAt=now - timedelta(days=10)
            ),
            inventoryLogEntry(
                logId=str(uuid.uuid4()),
                farmerId=farmer_id,
                itemId=mock_item_id_1,
                action=inventoryAction.SELL,
                quantityKg=200.0,
                pricePerKg=35.0,
                notes="Sold to local mandi",
                ts=now - timedelta(days=5),
                createdAt=now - timedelta(days=5)
            ),
            inventoryLogEntry(
                logId=str(uuid.uuid4()),
                farmerId=farmer_id,
                itemId=mock_item_id_2,
                action=inventoryAction.ADD,
                quantityKg=1000.0,
                notes="Wheat harvest",
                ts=now - timedelta(days=30),
                createdAt=now - timedelta(days=30)
            ),
            inventoryLogEntry(
                logId=str(uuid.uuid4()),
                farmerId=farmer_id,
                itemId=mock_item_id_1,
                action=inventoryAction.SPOILAGE,
                quantityKg=50.0,
                notes="Some spoilage due to moisture",
                ts=now - timedelta(days=3),
                createdAt=now - timedelta(days=3)
            ),
        ]
        
        self._mock_logs.extend(mock_logs)
