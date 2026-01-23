"""
inventory Repository with Mock Fallback
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import uuid

from ..models import inventoryItem
from ..constants import (
    StorageType,
    StockStage,
    HealthStatus,
    QualityGrade,
    SHELF_LIFE_DAYS
)


class inventoryRepo:
    """Repository for inventory items with mock fallback"""
    
    def __init__(self):
        # Local JSON persistence for "real" data storage
        import os
        from pathlib import Path
        
        self.data_dir = Path(__file__).resolve().parent.parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.db_file = self.data_dir / "inventory_db.json"
        
        self._mock_items: Dict[str, inventoryItem] = {}
        self._load_db()

    def _load_db(self):
        """Load data from local JSON file"""
        import json
        from datetime import datetime
        
        if self.db_file.exists():
            try:
                with open(self.db_file, "r") as f:
                    data = json.load(f)
                    for item_data in data:
                        # Convert ISO strings back to datetime
                        if "storedAt" in item_data and item_data["storedAt"]:
                            item_data["storedAt"] = datetime.fromisoformat(item_data["storedAt"])
                        if "expectedSellBy" in item_data and item_data["expectedSellBy"]:
                            item_data["expectedSellBy"] = datetime.fromisoformat(item_data["expectedSellBy"])
                        if "updatedAt" in item_data and item_data["updatedAt"]:
                            item_data["updatedAt"] = datetime.fromisoformat(item_data["updatedAt"])
                            
                        item = inventoryItem(**item_data)
                        self._mock_items[item.itemId] = item
                print(f"✓ Loaded {len(self._mock_items)} items from local DB")
            except Exception as e:
                print(f"⚠️ Error loading inventory DB: {e}")
                self._mock_items = {}
        
    def _save_db(self):
        """Save data to local JSON file"""
        import json
        
        try:
            data = []
            for item in self._mock_items.values():
                item_dict = item.dict()
                # ISO format for dates
                if item_dict.get("storedAt"):
                    item_dict["storedAt"] = item_dict["storedAt"].isoformat()
                if item_dict.get("expectedSellBy"):
                    item_dict["expectedSellBy"] = item_dict["expectedSellBy"].isoformat()
                if item_dict.get("updatedAt"):
                    item_dict["updatedAt"] = item_dict["updatedAt"].isoformat()
                data.append(item_dict)
                
            with open(self.db_file, "w") as f:
                json.dump(data, f, indent=2)
            # print("✓ Saved inventory DB")
        except Exception as e:
            print(f"⚠️ Error saving inventory DB: {e}")

    def list_items(self, farmer_id: str) -> List[inventoryItem]:
        """
        List all inventory items for a farmer
        Returns mock data if empty
        """
        items = [item for item in self._mock_items.values() if item.farmerId == farmer_id]
        
        if not items and not self.db_file.exists():
            # Seed mock data if empty AND no DB exists
            self.seed_mock_inventory_if_empty(farmer_id)
            items = [item for item in self._mock_items.values() if item.farmerId == farmer_id]
        
        return items
    
    def add_item(self, item: inventoryItem) -> inventoryItem:
        """Add new inventory item"""
        self._mock_items[item.itemId] = item
        self._save_db()
        return item
    
    def update_item(self, item_id: str, updates: Dict[str, Any]) -> inventoryItem:
        """Update existing inventory item"""
        if item_id not in self._mock_items:
            raise ValueError(f"Item {item_id} not found")
        
        item = self._mock_items[item_id]
        for key, value in updates.items():
            if hasattr(item, key):
                setattr(item, key, value)
        
        item.updatedAt = datetime.now()
        self._mock_items[item_id] = item
        self._save_db()
        return item
    
    def seed_mock_inventory_if_empty(self, farmer_id: str):
        """Seed realistic mock inventory data"""
        now = datetime.now()
        
        mock_items = [
            # Critical: Tomato near expiry
            inventoryItem(
                itemId=str(uuid.uuid4()),
                farmerId=farmer_id,
                cropKey="tomato",
                cropName="Tomato",
                quantityKg=150.0,
                qualityGrade=QualityGrade.A,
                storageType=StorageType.HOME,
                storedAt=now - timedelta(days=5),
                shelfLifeDays=SHELF_LIFE_DAYS.get("tomato", 10),
                expectedSellBy=now + timedelta(days=2),
                stage=StockStage.READY_TO_SELL,
                healthStatus=HealthStatus.WARNING,
                spoilageRisk="high",
                notes="Fresh harvest, sell quickly"
            ),
            
            # Warning: Onion medium shelf life
            inventoryItem(
                itemId=str(uuid.uuid4()),
                farmerId=farmer_id,
                cropKey="onion",
                cropName="Onion",
                quantityKg=500.0,
                qualityGrade=QualityGrade.A,
                storageType=StorageType.WAREHOUSE,
                storedAt=now - timedelta(days=24),
                shelfLifeDays=SHELF_LIFE_DAYS.get("onion", 60),
                expectedSellBy=now + timedelta(days=6),
                stage=StockStage.PACKED,
                healthStatus=HealthStatus.WARNING,
                spoilageRisk="medium",
                notes="Good quality, warehouse stored"
            ),
            
            # Good: Potato long shelf life
            inventoryItem(
                itemId=str(uuid.uuid4()),
                farmerId=farmer_id,
                cropKey="potato",
                cropName="Potato",
                quantityKg=800.0,
                qualityGrade=QualityGrade.B,
                storageType=StorageType.COLD_STORAGE,
                storedAt=now - timedelta(days=15),
                shelfLifeDays=SHELF_LIFE_DAYS.get("potato", 90),
                expectedSellBy=now + timedelta(days=45),
                stage=StockStage.STORED,
                healthStatus=HealthStatus.GOOD,
                spoilageRisk="low",
                notes="Cold storage, can wait for better prices"
            ),
            
            # Good: Wheat very long shelf life
            inventoryItem(
                itemId=str(uuid.uuid4()),
                farmerId=farmer_id,
                cropKey="wheat",
                cropName="Wheat",
                quantityKg=2000.0,
                qualityGrade=QualityGrade.A,
                storageType=StorageType.WAREHOUSE,
                storedAt=now - timedelta(days=30),
                shelfLifeDays=SHELF_LIFE_DAYS.get("wheat", 180),
                expectedSellBy=now + timedelta(days=150),
                stage=StockStage.PACKED,
                healthStatus=HealthStatus.GOOD,
                spoilageRisk="low",
                notes="Premium quality wheat"
            ),
            
            # Partial sold: Groundnut
            inventoryItem(
                itemId=str(uuid.uuid4()),
                farmerId=farmer_id,
                cropKey="groundnut",
                cropName="Groundnut",
                quantityKg=300.0,
                qualityGrade=QualityGrade.A,
                storageType=StorageType.WAREHOUSE,
                storedAt=now - timedelta(days=20),
                shelfLifeDays=SHELF_LIFE_DAYS.get("groundnut", 90),
                expectedSellBy=now + timedelta(days=70),
                stage=StockStage.SOLD_PARTIAL,
                healthStatus=HealthStatus.GOOD,
                spoilageRisk="low",
                notes="Sold 200kg already, 300kg remaining"
            ),
        ]
        
        for item in mock_items:
            self.add_item(item) # This will save to DB
