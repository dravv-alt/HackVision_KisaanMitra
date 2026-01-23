from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from Backend.api.dependencies import get_db_client

router = APIRouter(prefix="/onboarding", tags=["onboarding"])

class LocationData(BaseModel):
    state: str
    district: str
    village: str
    pincode: str
    lat: Optional[float] = None
    lon: Optional[float] = None

class OnboardingCompleteRequest(BaseModel):
    language: str
    location: LocationData
    soilType: str
    landSizeAcres: float
    selectedCrops: List[str]

class OnboardingCompleteResponse(BaseModel):
    userId: str
    farmerId: str
    message: str

@router.post("/complete", response_model=OnboardingCompleteResponse)
async def complete_onboarding(
    request: OnboardingCompleteRequest,
    db_client = Depends(get_db_client)
):
    """
    Complete the onboarding process and create/update farmer profile
    """
    try:
        db = db_client["kisanmitra"]
        
        # Generate unique IDs (in production, use proper ID generation or get from auth)
        import uuid
        user_id = f"U{str(uuid.uuid4())[:8].upper()}"
        farmer_id = f"F{str(uuid.uuid4())[:8].upper()}"
        
        # Create farmer document
        farmer_document = {
            "farmer_id": farmer_id,
            "user_id": user_id,
            "name": "New Farmer",  # Can be collected in a future step
            "phone": "",  # Can be collected from login
            "language": request.language,
            "location": {
                "state": request.location.state,
                "district": request.location.district,
                "village": request.location.village,
                "pincode": request.location.pincode,
                "coordinates": {
                    "lat": request.location.lat,
                    "lon": request.location.lon
                } if request.location.lat and request.location.lon else None
            },
            "soil_type": request.soilType,
            "land_size_acres": request.landSizeAcres,
            "crops": request.selectedCrops,
            "onboarding_completed": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Insert into farmers collection
        result = db.farmers.insert_one(farmer_document)
        
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create farmer profile")
        
        return OnboardingCompleteResponse(
            userId=user_id,
            farmerId=farmer_id,
            message="Onboarding completed successfully"
        )
        
    except Exception as e:
        print(f"Error in complete_onboarding: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to complete onboarding: {str(e)}")
