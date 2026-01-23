from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional
from pydantic import BaseModel

from Backend.api.dependencies import get_current_user
from Backend.Financial_tracking.service import FinanceTrackingService
from Backend.Financial_tracking.models import FinanceModuleOutput, FinanceTransaction
from Backend.Financial_tracking.constants import SeasonType

router = APIRouter()

class TransactionCreate(BaseModel):
    season: str = SeasonType.KHARIF.value
    category: str
    amount: float
    notes: Optional[str] = None
    relatedCropId: Optional[str] = None

@router.get("/finance/report", response_model=FinanceModuleOutput)
async def get_finance_report(
    season: str = SeasonType.KHARIF.value,
    language: str = "hi",
    current_user = Depends(get_current_user)
):
    """
    Get profit/loss report and optimization advice.
    """
    try:
        service = FinanceTrackingService()
        return service.run_finance_report(
            farmerId=current_user["id"],
            season=season,
            language=language
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/finance/expense", response_model=FinanceTransaction)
async def add_expense(
    data: TransactionCreate,
    current_user = Depends(get_current_user)
):
    """
    Record a new expense.
    """
    try:
        service = FinanceTrackingService()
        return service.add_expense(
            farmerId=current_user["id"],
            season=data.season,
            category=data.category,
            amount=data.amount,
            notes=data.notes,
            relatedCropId=data.relatedCropId
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/finance/income", response_model=FinanceTransaction)
async def add_income(
    data: TransactionCreate,
    current_user = Depends(get_current_user)
):
    """
    Record a new income.
    """
    try:
        service = FinanceTrackingService()
        return service.add_income(
            farmerId=current_user["id"],
            season=data.season,
            category=data.category,
            amount=data.amount,
            notes=data.notes,
            relatedCropId=data.relatedCropId
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
