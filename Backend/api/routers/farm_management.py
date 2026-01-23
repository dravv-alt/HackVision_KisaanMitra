from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import Dict, Any, Optional

from ..dependencies import get_db_client, get_current_user
from Backend.Farm_management.Planning_stage.service import PreSeedingService
from Backend.Farm_management.Planning_stage.models import PlanningRequest, PreSeedingOutput
from Backend.Farm_management.Farming_stage.engines.vision_engine import VisionEngine
from Backend.Farm_management.Farming_stage.engines.market_engine import MarketEngine
from Backend.Farm_management.Post_Harvest_stage.core.engine import PostHarvestDecisionEngine, DecisionResult as PostHarvestPlan
from Backend.Farm_management.Post_Harvest_stage.core.context import FarmerContext as HarvestContext

router = APIRouter()

# -----------------------------------------------------------------------------
# PLANNING STAGE
# -----------------------------------------------------------------------------

@router.post("/planning/pre-seeding", response_model=PreSeedingOutput)
async def get_pre_seeding_plan(
    request: PlanningRequest,
    db_client = Depends(get_db_client),
    current_user = Depends(get_current_user)
):
    """
    Get comprehensive crop recommendations and scheme eligibility.
    """
    try:
        # Initialize service with user's DB connection if available
        # Note: Repositories in the service will handle None client by using mock data
        service = PreSeedingService() 
        output = service.run(request)
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------------------------------------------------
# FARMING STAGE
# -----------------------------------------------------------------------------

@router.post("/farming/disease-detect")
async def detect_disease(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    """
    Detect plant disease from uploaded image.
    """
    try:
        # Save temp file
        import shutil
        import os
        
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Run detection
        engine = VisionEngine()
        result = engine.detect_disease(temp_path)
        
        # Cleanup
        os.remove(temp_path)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/farming/market-price")
async def get_market_prices(
    crop: str,
    state: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """
    Get real-time market prices.
    """
    try:
        engine = MarketEngine()
        # Use user's state if not provided
        state_filter = state or current_user.get("state")
        return engine.get_prices(crop_name=crop, state=state_filter)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------------------------------------------------
# POST-HARVEST STAGE
# -----------------------------------------------------------------------------

@router.post("/post-harvest/plan", response_model=PostHarvestPlan)
async def get_post_harvest_plan(
    context: HarvestContext,
    current_user = Depends(get_current_user)
):
    """
    Get post-harvest optimization plan (sell vs store, market selection).
    """
    try:
        engine = PostHarvestDecisionEngine()
        return engine.run_decision(context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
