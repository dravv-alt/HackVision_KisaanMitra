"""
inventory Service - Main Orchestration Layer
"""

from datetime import datetime
from typing import Optional

from .models import inventoryModuleOutput
from .repositories import (
    FarmerRepo,
    inventoryRepo,
    inventoryLogRepo,
    MarketRepo,
    AlertRepo,
    AuditRepo
)
from .engines import (
    StockEngine,
    ShelfLifeEngine,
    HealthEngine,
    SellPriorityEngine,
    ReminderEngine,
    ResponseBuilder
)


class inventoryService:
    """
    Main service for inventory management
    Orchestrates all engines and repositories
    """
    
    def __init__(self):
        # Initialize repositories
        self.farmer_repo = FarmerRepo()
        self.inventory_repo = inventoryRepo()
        self.log_repo = inventoryLogRepo()
        self.market_repo = MarketRepo()
        self.alert_repo = AlertRepo()
        self.audit_repo = AuditRepo()
        
        # Initialize engines
        self.stock_engine = StockEngine()
        self.shelf_life_engine = ShelfLifeEngine()
        self.health_engine = HealthEngine()
        self.sell_priority_engine = SellPriorityEngine()
        self.reminder_engine = ReminderEngine()
        self.response_builder = ResponseBuilder()
    
    def get_inventory_dashboard(
        self,
        farmer_id: str,
        include_reminders: bool = True
    ) -> inventoryModuleOutput:
        """
        Get complete inventory dashboard for a farmer
        
        This is the main entry point that will be called from FastAPI endpoints
        
        Args:
            farmer_id: Farmer ID
            include_reminders: Whether to generate and save expiry reminders
            
        Returns:
            inventoryModuleOutput with complete dashboard data
        """
        try:
            # Audit log
            self.audit_repo.log(farmer_id, "get_inventory_dashboard", {"timestamp": datetime.now()})
            
            # 1. Get farmer profile
            farmer = self.farmer_repo.get_farmer(farmer_id)
            
            # 2. Get inventory items (with mock fallback)
            items = self.inventory_repo.list_items(farmer_id)
            
            # 3. Get inventory logs (with mock fallback)
            logs = self.log_repo.list_logs(farmer_id)
            
            # 4. Build current stock view by applying logs
            current_stock = self.stock_engine.build_current_stock_view(items, logs)
            
            # 5. Compute shelf life for each item
            now = datetime.now()
            shelf_life_info = {}
            for item in current_stock:
                shelf_life_info[item.itemId] = self.shelf_life_engine.compute_shelf_life(item, now)
            
            # 6. Infer health status for each item
            health_info = {}
            for item in current_stock:
                shelf_info = shelf_life_info[item.itemId]
                health_status = self.health_engine.infer_health_status(
                    item,
                    shelf_info["remainingDays"],
                    item.spoilageRisk
                )
                health_info[item.itemId] = health_status
            
            # 7. Get market context (optional)
            market_context = {}
            for item in current_stock:
                try:
                    market_data = self.market_repo.get_latest_price(item.cropKey)
                    market_context[item.cropKey] = market_data
                except Exception:
                    # Graceful fallback if market data unavailable
                    pass
            
            # 8. Rank stock by sell priority
            stock_cards = self.sell_priority_engine.rank_stock(
                current_stock,
                shelf_life_info,
                health_info,
                market_context if market_context else None
            )
            
            # 9. Generate expiry reminders (optional)
            if include_reminders and stock_cards:
                reminders = self.reminder_engine.generate_expiry_reminders(
                    stock_cards,
                    farmer_id,
                    farmer.language.value
                )
                
                # Save reminders
                if reminders:
                    self.alert_repo.save_expiry_reminders(reminders)
            
            # 10. Build final response
            output = self.response_builder.build(
                farmer.language,
                stock_cards,
                farmer_id
            )
            
            # Audit log success
            self.audit_repo.log(
                farmer_id,
                "dashboard_success",
                {
                    "itemCount": len(stock_cards),
                    "criticalCount": output.criticalCount,
                    "warningCount": output.warningCount
                }
            )
            
            return output
            
        except Exception as e:
            # Audit log error
            self.audit_repo.log(
                farmer_id,
                "dashboard_error",
                {"error": str(e)}
            )
            raise
    
    def simulate_sell_action(
        self,
        farmer_id: str,
        item_id: str,
        quantity_kg: float,
        price_per_kg: Optional[float] = None
    ) -> inventoryModuleOutput:
        """
        Simulate a sell action and return updated dashboard
        
        Args:
            farmer_id: Farmer ID
            item_id: Item to sell
            quantity_kg: Quantity to sell
            price_per_kg: Optional price per kg
            
        Returns:
            Updated inventory dashboard
        """
        from .models import inventoryLogEntry
        from .constants import inventoryAction
        import uuid
        
        # Create sell log entry
        log_entry = inventoryLogEntry(
            logId=str(uuid.uuid4()),
            farmerId=farmer_id,
            itemId=item_id,
            action=inventoryAction.SELL,
            quantityKg=quantity_kg,
            pricePerKg=price_per_kg,
            notes="Simulated sell action",
            ts=datetime.now()
        )
        
        # Add log
        self.log_repo.add_log(log_entry)
        
        # Audit log
        self.audit_repo.log(
            farmer_id,
            "simulate_sell",
            {"itemId": item_id, "quantity": quantity_kg}
        )
        
        # Return updated dashboard
        return self.get_inventory_dashboard(farmer_id, include_reminders=False)
    
    def simulate_spoilage_action(
        self,
        farmer_id: str,
        item_id: str,
        quantity_kg: float,
        notes: Optional[str] = None
    ) -> inventoryModuleOutput:
        """
        Simulate a spoilage action and return updated dashboard
        
        Args:
            farmer_id: Farmer ID
            item_id: Item with spoilage
            quantity_kg: Quantity spoiled
            notes: Optional notes
            
        Returns:
            Updated inventory dashboard
        """
        from .models import inventoryLogEntry
        from .constants import inventoryAction
        import uuid
        
        # Create spoilage log entry
        log_entry = inventoryLogEntry(
            logId=str(uuid.uuid4()),
            farmerId=farmer_id,
            itemId=item_id,
            action=inventoryAction.SPOILAGE,
            quantityKg=quantity_kg,
            notes=notes or "Simulated spoilage",
            ts=datetime.now()
        )
        
        # Add log
        self.log_repo.add_log(log_entry)
        
        # Audit log
        self.audit_repo.log(
            farmer_id,
            "simulate_spoilage",
            {"itemId": item_id, "quantity": quantity_kg}
        )
        
        # Return updated dashboard
        return self.get_inventory_dashboard(farmer_id, include_reminders=False)
    def add_stock(
        self,
        farmer_id: str,
        crop_name: str,
        quantity_kg: float,
        storage_type: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add stock to inventory (Agentic Feature)
        
        Args:
            farmer_id: Farmer ID
            crop_name: Name of crop (e.g. "Wheat")
            quantity_kg: Quantity to add
            storage_type: Storage type
            notes: Notes
            
        Returns:
            Result dict with success status and message
        """
        from .models import inventoryItem
        from .constants import StockStage, HealthStatus, QualityGrade, SHELF_LIFE_DAYS, StorageType
        import uuid
        
        # 1. Check if crop already exists
        crop_key = crop_name.lower().replace(" ", "_")
        existing_items = self.inventory_repo.list_items(farmer_id)
        
        target_item = None
        for item in existing_items:
            if item.cropKey == crop_key:
                target_item = item
                break
        
        if target_item:
            # Update existing
            new_quantity = target_item.quantityKg + quantity_kg
            self.inventory_repo.update_item(
                target_item.itemId,
                {
                    "quantityKg": new_quantity,
                    "updatedAt": datetime.now(),
                    "notes": f"{target_item.notes or ''} | Added {quantity_kg}kg on {datetime.now().strftime('%d/%m')}"
                }
            )
            message = f"Updated {crop_name} stock. New quantity: {new_quantity}kg"
            action = "updated"
        else:
            # Create new
            shelf_life = SHELF_LIFE_DAYS.get(crop_key, 30) # Default 30 days
            now = datetime.now()
            
            new_item = inventoryItem(
                itemId=str(uuid.uuid4()),
                farmerId=farmer_id,
                cropKey=crop_key,
                cropName=crop_name.capitalize(),
                quantityKg=quantity_kg,
                qualityGrade=QualityGrade.A, # Default
                storageType=storage_type or StorageType.HOME,
                storedAt=now,
                shelfLifeDays=shelf_life,
                expectedSellBy=now + timedelta(days=shelf_life - 5),
                stage=StockStage.STORED,
                healthStatus=HealthStatus.GOOD,
                spoilageRisk="low",
                notes=notes or f"Added via Voice Agent on {now.strftime('%d/%m')}"
            )
            self.inventory_repo.add_item(new_item)
            message = f"Added new stock: {quantity_kg}kg of {crop_name}"
            action = "added"

        # Log action
        self.audit_repo.log(
            farmer_id,
            "add_stock_voice",
            {"crop": crop_name, "quantity": quantity_kg, "action": action}
        )
        
        return {
            "success": True,
            "message": message,
            "crop_name": crop_name,
            "item_id": target_item.itemId if target_item else new_item.itemId,
            "quantity_added": quantity_kg,
            "total_quantity": target_item.quantityKg + quantity_kg if target_item else quantity_kg
        }
