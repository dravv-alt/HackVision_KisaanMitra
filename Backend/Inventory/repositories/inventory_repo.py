"""
Inventory Repository with Mock Fallback
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import uuid

from ..models import InventoryItem
from ..constants import (
    StorageType,
    StockStage,
    HealthStatus,
    QualityGrade,
    SHELF_LIFE_DAYS
)


class InventoryRepo:
    """Repository for inventory items with mock fallback"""
    
    def __init__(self):
        # Mock in-memory storage (simulates MongoDB collection)
        self._mock_items: Dict[str, InventoryItem] = {}
    
    def list_items(self, farmer_id: str) -> List[InventoryItem]:
        """
        List all inventory items for a farmer
        Returns mock data if empty
        """
        items = [item for item in self._mock_items.values() if item.farmerId == farmer_id]
        
        if not items:
            # Seed mock data if empty
            self.seed_mock_inventory_if_empty(farmer_id)
            items = [item for item in self._mock_items.values() if item.farmerId == farmer_id]
        
        return items
    
    def add_item(self, item: InventoryItem) -> InventoryItem:
        """Add new inventory item"""
        self._mock_items[item.itemId] = item
        return item
    
    def update_item(self, item_id: str, updates: Dict[str, Any]) -> InventoryItem:
        """Update existing inventory item"""
        if item_id not in self._mock_items:
            raise ValueError(f"Item {item_id} not found")
        
        item = self._mock_items[item_id]
        for key, value in updates.items():
            if hasattr(item, key):
                setattr(item, key, value)
        
        item.updatedAt = datetime.now()
        return item
    
    def seed_mock_inventory_if_empty(self, farmer_id: str):
        """Seed realistic mock inventory data"""
        now = datetime.now()
        
        mock_items = [
            # Critical: Tomato near expiry
            InventoryItem(
                itemId=str(uuid.uuid4()),
                farmerId=farmer_id,
                cropKey="tomato",
                cropName="Tomato",
                quantityKg=150.0,
                qualityGrade=QualityGrade.A,
                storageType=StorageType.HOME,
                storedAt=now - timedelta(days=5),
                shelfLifeDays=SHELF_LIFE_DAYS["tomato"],
                expectedSellBy=now + timedelta(days=2),
                stage=StockStage.READY_TO_SELL,
                healthStatus=HealthStatus.WARNING,
                spoilageRisk="high",
                notes="Fresh harvest, sell quickly"
            ),
            
            # Warning: Onion medium shelf life
            InventoryItem(
                itemId=str(uuid.uuid4()),
                farmerId=farmer_id,
                cropKey="onion",
                cropName="Onion",
                quantityKg=500.0,
                qualityGrade=QualityGrade.A,
                storageType=StorageType.WAREHOUSE,
                storedAt=now - timedelta(days=24),
                shelfLifeDays=SHELF_LIFE_DAYS["onion"],
                expectedSellBy=now + timedelta(days=6),
                stage=StockStage.PACKED,
                healthStatus=HealthStatus.WARNING,
                spoilageRisk="medium",
                notes="Good quality, warehouse stored"
            ),
            
            # Good: Potato long shelf life
            InventoryItem(
                itemId=str(uuid.uuid4()),
                farmerId=farmer_id,
                cropKey="potato",
                cropName="Potato",
                quantityKg=800.0,
                qualityGrade=QualityGrade.B,
                storageType=StorageType.COLD_STORAGE,
                storedAt=now - timedelta(days=15),
                shelfLifeDays=SHELF_LIFE_DAYS["potato"],
                expectedSellBy=now + timedelta(days=45),
                stage=StockStage.STORED,
                healthStatus=HealthStatus.GOOD,
                spoilageRisk="low",
                notes="Cold storage, can wait for better prices"
            ),
            
            # Good: Wheat very long shelf life
            InventoryItem(
                itemId=str(uuid.uuid4()),
                farmerId=farmer_id,
                cropKey="wheat",
                cropName="Wheat",
                quantityKg=2000.0,
                qualityGrade=QualityGrade.A,
                storageType=StorageType.WAREHOUSE,
                storedAt=now - timedelta(days=30),
                shelfLifeDays=SHELF_LIFE_DAYS["wheat"],
                expectedSellBy=now + timedelta(days=150),
                stage=StockStage.PACKED,
                healthStatus=HealthStatus.GOOD,
                spoilageRisk="low",
                notes="Premium quality wheat"
            ),
            
            # Partial sold: Groundnut
            InventoryItem(
                itemId=str(uuid.uuid4()),
                farmerId=farmer_id,
                cropKey="groundnut",
                cropName="Groundnut",
                quantityKg=300.0,
                qualityGrade=QualityGrade.A,
                storageType=StorageType.WAREHOUSE,
                storedAt=now - timedelta(days=20),
                shelfLifeDays=SHELF_LIFE_DAYS["groundnut"],
                expectedSellBy=now + timedelta(days=70),
                stage=StockStage.SOLD_PARTIAL,
                healthStatus=HealthStatus.GOOD,
                spoilageRisk="low",
                notes="Sold 200kg already, 300kg remaining"
            ),
        ]
        
        for item in mock_items:
            self._mock_items[item.itemId] = item
