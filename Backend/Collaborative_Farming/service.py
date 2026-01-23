"""
Collaborative Farming Service - Orchestration Entrypoint
"""

from typing import Optional, List, Dict
from datetime import datetime

from .repositories import (
    FarmerRepo, EquipmentRepo, RentalRepo, 
    LandPoolRepo, ResidueRepo, AlertRepo, AuditRepo
)
from .engines import (
    EquipmentEngine, RentalEngine, LandPoolEngine, 
    ResidueEngine, ReminderEngine, ResponseBuilder
)
from .models import CollaborativeOutput, FarmerProfile, EquipmentListing, LandPoolRequest
from .constants import Language, EquipmentType, PoolRequestType, PaymentMethod


class CollaborativeFarmingService:
    """Main service providing orchestration for all collaborative farming features"""
    
    def __init__(self, db_client=None):
        # Repositories
        self.farmer_repo = FarmerRepo(db_client)
        self.equipment_repo = EquipmentRepo(db_client)
        self.rental_repo = RentalRepo(db_client)
        self.land_pool_repo = LandPoolRepo(db_client)
        self.residue_repo = ResidueRepo(db_client)
        self.alert_repo = AlertRepo(db_client)
        self.audit_repo = AuditRepo(db_client)
        
        # Engines
        self.equipment_engine = EquipmentEngine(self.equipment_repo)
        self.rental_engine = RentalEngine(self.rental_repo, self.equipment_repo)
        self.land_pool_engine = LandPoolEngine(self.land_pool_repo)
        self.residue_engine = ResidueEngine(self.residue_repo)
        self.reminder_engine = ReminderEngine()
        self.response_builder = ResponseBuilder()

    def run_marketplace_view(self, farmer_id: str, filters: Dict = {}) -> CollaborativeOutput:
        """Fetch the full collaborative farming dashboard for a farmer"""
        farmer = self.farmer_repo.get_farmer(farmer_id)
        
        # 1. Discover Equipment
        equipment = self.equipment_engine.list_available_equipment(
            district=filters.get("district", farmer.district),
            equipment_type=filters.get("equipmentType")
        )
        
        # 2. Open Land Pooling Requests
        pools = self.land_pool_engine.find_matching_requests(farmer)
        
        # 3. Farmer's own rentals
        rentals = self.rental_repo.list_rentals_by_farmer(farmer_id)
        
        # 4. Residue offers (Future Scope)
        residue = self.residue_engine.list_residue_offers(farmer.district)
        
        # 5. Deadlines & Reminders
        reminders = self.reminder_engine.generate_rental_return_reminders(rentals)
        self.alert_repo.save_reminders(reminders)
        
        # 6. Build final response
        self.audit_repo.log(farmer_id, "view_marketplace", {"filter": filters})
        
        return self.response_builder.build(
            language=farmer.language,
            equipment=equipment,
            rentals=rentals,
            pools=pools,
            residue=residue,
            reminders=reminders
        )

    def create_equipment_listing(
        self, 
        owner_id: str, 
        equipment_type: EquipmentType, 
        model_name: str, 
        price_per_day: float,
        available_from: datetime,
        available_to: datetime,
        condition: str = "Good",
        hp_required: Optional[str] = None
    ) -> EquipmentListing:
        """Farmer lists their equipment for rent"""
        farmer = self.farmer_repo.get_farmer(owner_id)
        listing = self.equipment_engine.create_listing(
            owner_id, equipment_type, model_name, price_per_day, 
            available_from, available_to, farmer.district, farmer.pincode,
            condition, hp_required
        )
        self.audit_repo.log(owner_id, "create_listing", {"listing_id": listing.listingId})
        return listing

    def request_equipment_rental(
        self, 
        renter_id: str, 
        listing_id: str, 
        start_date: datetime, 
        end_date: datetime,
        payment_method: PaymentMethod = PaymentMethod.CASH_ON_DELIVERY
    ):
        """Farmer requests to rent equipment"""
        try:
            rental = self.rental_engine.request_booking(
                renter_id, listing_id, start_date, end_date, payment_method
            )
            self.audit_repo.log(renter_id, "request_rental", {"listing_id": listing_id, "rental_id": rental.rentalId})
            return rental
        except Exception as e:
            self.audit_repo.log(renter_id, "request_rental_failed", {"listing_id": listing_id, "error": str(e)})
            raise

    def approve_rental(self, owner_id: str, rental_id: str):
        """Owner approves a rental request"""
        rental = self.rental_engine.approve_request(owner_id, rental_id)
        self.audit_repo.log(owner_id, "approve_rental", {"rental_id": rental_id})
        return rental

    def create_land_pool_request(
        self, 
        farmer_id: str, 
        req_type: PoolRequestType, 
        land_size: float, 
        crop_pref: Optional[str] = None
    ) -> LandPoolRequest:
        """Farmer starts a land pooling request"""
        farmer = self.farmer_repo.get_farmer(farmer_id)
        req = self.land_pool_engine.create_pool_request(
            farmer_id, req_type, land_size, 
            farmer.district, farmer.pincode, crop_pref
        )
        self.audit_repo.log(farmer_id, "create_pool_request", {"request_id": req.requestId})
        return req

    def join_land_pool(self, farmer_id: str, request_id: str):
        """Farmer joins an existing land pool"""
        req = self.land_pool_engine.join_pool(request_id, farmer_id)
        self.audit_repo.log(farmer_id, "join_pool", {"request_id": request_id})
        return req
