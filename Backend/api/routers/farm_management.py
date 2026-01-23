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
        service = PreSeedingService(db_client=db_client) 
        output = service.run(request)
        return output
    except ValueError as e:
        error_msg = str(e)
        if "Farmer not found" in error_msg:
            # Provide helpful guidance with available test IDs
            raise HTTPException(
                status_code=404, 
                detail={
                    "error": error_msg,
                    "help": "Use one of the test farmer IDs: F001, F002, F003, or F004"
                }
            )
        raise HTTPException(status_code=400, detail=error_msg)
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
        market_data = engine.get_market_data(crop)
        return {
            "crop": crop,
            "state": state or current_user.get("state"),
            "current_price": market_data.current_price,
            "trend": market_data.price_trend.value,
            "demand": market_data.demand_level.value,
            "forecast": engine.get_price_forecast(crop)
        }
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
