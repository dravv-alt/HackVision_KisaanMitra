from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel

from api.dependencies import get_current_user
from collaborative_farming.service import CollaborativeFarmingService
from collaborative_farming.models import CollaborativeOutput, EquipmentListing, RentalRequest, LandPoolRequest
from collaborative_farming.constants import EquipmentType, PaymentMethod, PoolRequestType

router = APIRouter()

# Request Models
class EquipmentCreate(BaseModel):
    equipment_type: EquipmentType
    model_name: str
    price_per_day: float
    available_from: datetime
    available_to: datetime
    condition: str = "Good"
    hp_required: Optional[str] = None

class RentalCreate(BaseModel):
    listing_id: str
    start_date: datetime
    end_date: datetime
    payment_method: PaymentMethod = PaymentMethod.CASH_ON_DELIVERY

class LandPoolCreate(BaseModel):
    req_type: PoolRequestType
    land_size: float
    crop_pref: Optional[str] = None


@router.get("/collaborative/marketplace", response_model=CollaborativeOutput)
async def get_marketplace(
    district: Optional[str] = None,
    equipment_type: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """
    Get marketplace dashboard with rentals, pools, and reminders.
    """
    try:
        service = CollaborativeFarmingService()
        filters = {}
        if district: filters["district"] = district
        if equipment_type: filters["equipmentType"] = equipment_type
        
        return service.run_marketplace_view(
            farmer_id=current_user["id"],
            filters=filters
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/collaborative/equipment", response_model=EquipmentListing)
async def list_equipment(
    data: EquipmentCreate,
    current_user = Depends(get_current_user)
):
    """
    List equipment for rent.
    """
    try:
        service = CollaborativeFarmingService()
        return service.create_equipment_listing(
            owner_id=current_user["id"],
            **data.dict()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/collaborative/rental", response_model=RentalRequest)
async def request_rental(
    data: RentalCreate,
    current_user = Depends(get_current_user)
):
    """
    Request to rent equipment.
    """
    try:
        service = CollaborativeFarmingService()
        return service.request_equipment_rental(
            renter_id=current_user["id"],
            listing_id=data.listing_id,
            start_date=data.start_date,
            end_date=data.end_date,
            payment_method=data.payment_method
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/collaborative/land-pool", response_model=LandPoolRequest)
async def create_land_pool(
    data: LandPoolCreate,
    current_user = Depends(get_current_user)
):
    """
    Create a land pooling request.
    """
    try:
        service = CollaborativeFarmingService()
        return service.create_land_pool_request(
            farmer_id=current_user["id"],
            req_type=data.req_type,
            land_size=data.land_size,
            crop_pref=data.crop_pref
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
