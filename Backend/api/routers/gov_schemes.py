from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from Backend.api.dependencies import get_current_user
from Backend.Gov_Schemes.service import GovSchemesDisplayService
from Backend.Gov_Schemes.models import GovSchemesOutput, SchemeRecord
from Backend.Gov_Schemes.constants import SchemeCategory

router = APIRouter()

@router.get("/schemes", response_model=GovSchemesOutput)
async def get_schemes_display(
    category: Optional[SchemeCategory] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    force_refresh: bool = False,
    current_user = Depends(get_current_user)
):
    """
    Get eligible schemes, filtered by location/category, with voice summary.
    """
    try:
        service = GovSchemesDisplayService()
        
        # Use location from params or user profile
        filter_state = state or current_user.get("state")
        filter_district = district or current_user.get("district")
        
        return service.get_schemes_display(
            farmer_id=current_user["id"],
            state=filter_state,
            district=filter_district,
            category=category,
            force_refresh=force_refresh,
            generate_alerts=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/schemes/{scheme_id}", response_model=SchemeRecord)
async def get_scheme_details(
    scheme_id: str,
    current_user = Depends(get_current_user)
):
    """
    Get detailed information for a specific scheme.
    """
    try:
        service = GovSchemesDisplayService()
        scheme = service.get_scheme_by_id(scheme_id)
        if not scheme:
            raise HTTPException(status_code=404, detail="Scheme not found")
        return scheme
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
