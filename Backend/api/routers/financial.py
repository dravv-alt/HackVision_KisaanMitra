from fastapi import APIRouter, Depends, HTTPException, Body, Query
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

# Import dependencies (using optional auth for flexibility in demo)
from Backend.Financial_tracking.service import FinanceTrackingService
from Backend.Financial_tracking.models import FinanceModuleOutput, FinanceTransaction
from Backend.Financial_tracking.constants import SeasonType, TransactionType

router = APIRouter()

# --- Models ---

class TransactionCreate(BaseModel):
    season: str = SeasonType.KHARIF.value
    category: str
    amount: float
    notes: Optional[str] = None
    relatedCropId: Optional[str] = None
    type: str = "expense" # "expense" or "income"

class CropPerformance(BaseModel):
    id: str
    name: str
    area: str
    income: float
    expense: float
    profit: float
    status: str
    trend: str

class FinanceDashboardResponse(BaseModel):
    totals: Any # FinanceTotals
    crop_performance: List[CropPerformance]
    recent_transactions: List[dict]
    insights: Any # FinanceModuleOutput (or subset)

# --- Service Helper ---
def get_service():
    return FinanceTrackingService()

# --- Endpoints ---

@router.get("/finance/{farmer_id}/dashboard", response_model=FinanceDashboardResponse)
async def get_finance_dashboard(
    farmer_id: str,
    season: str = SeasonType.KHARIF.value,
    language: str = "en"
):
    """
    Get complete financial dashboard data in one go.
    Aggregates report, crop performance, and transactions.
    """
    try:
        service = get_service()
        
        # 1. Get Main Report (Totals, Insights)
        report = service.run_finance_report(
            farmerId=farmer_id,
            season=season,
            language=language,
            force_refresh=True # Ensure fresh data
        )

        # 2. Get Raw Transactions
        transactions = service.transaction_repo.list_transactions(farmer_id, season)
        
        # 3. Calculate Crop Performance
        # Group transactions by crop (using relatedCropId or inferring from notes/mock)
        # For this Hackathon demo, we might need to map raw transactions to the 'CropData' structure 
        # expected by frontend if relatedCropId is not strictly set.
        
        # Mocking Crop Metadata linkage for demo purposes since Repo might be simple
        crops_map = {
            "wheat": {"name": "Wheat", "area": "15 Acres", "income": 0, "expense": 0},
            "mustard": {"name": "Mustard", "area": "5 Acres", "income": 0, "expense": 0},
            "chana": {"name": "Chickpea (Chana)", "area": "8 Acres", "income": 0, "expense": 0},
            "other": {"name": "General Farm", "area": "-", "income": 0, "expense": 0}
        }

        # Aggregate Real Transaction Data
        recent_txs = []
        for tx in transactions:
            # Add to recent list (formatted)
            recent_txs.append({
                "id": str(tx.transactionId),
                "title": tx.notes or tx.category,
                "date": tx.ts.strftime("%b %d, %I:%M %p"),
                "amount": f"{'-' if tx.type == TransactionType.EXPENSE else '+'} ₹{tx.amount:,.0f}",
                "type": "expense" if tx.type == TransactionType.EXPENSE else "income",
                "category": tx.category,
                "iconColor": _get_category_color(tx.category)
            })

            # Crop Aggregation
            # Simple heuristic matching for demo: checks if 'wheat', 'mustard', etc is in notes/category
            cat_lower = (tx.category + " " + (tx.notes or "")).lower()
            target_crop = "other"
            if "wheat" in cat_lower: target_crop = "wheat"
            elif "mustard" in cat_lower: target_crop = "mustard"
            elif "chana" in cat_lower or "chickpea" in cat_lower: target_crop = "chana"
            
            if tx.type == TransactionType.INCOME:
                crops_map[target_crop]["income"] += tx.amount
            else:
                crops_map[target_crop]["expense"] += tx.amount

        # Build Crop List
        crop_list = []
        for key, data in crops_map.items():
            if data["income"] == 0 and data["expense"] == 0 and key != "wheat": continue # Skip empty non-defaults
            
            profit = data["income"] - data["expense"]
            status = "Profitable" if profit > 0 else "Loss" if profit < 0 else "Neutral"
            trend = "up" if profit > 10000 else "down"

            crop_list.append(CropPerformance(
                id=key,
                name=data["name"],
                area=data["area"],
                income=data["income"],
                expense=data["expense"],
                profit=profit,
                status=status,
                trend=trend
            ))
            
        # Ensure at least some dummy mock data if empty (for UI visual validation)
        if not crop_list:
             crop_list = [
                CropPerformance(id="1", name='Wheat', area='15 Acres', income=450000, expense=180000, profit=270000, status='Profitable', trend='up'),
                CropPerformance(id="2", name='Mustard', area='5 Acres', income=120000, expense=95000, profit=25000, status='Low Margin', trend='down')
            ]

        return FinanceDashboardResponse(
            totals=report.totals,
            crop_performance=crop_list,
            recent_transactions=sorted(recent_txs, key=lambda x: x['date'], reverse=True)[:10], # Last 10
            insights=report
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/finance/{farmer_id}/transaction")
async def add_transaction(
    farmer_id: str,
    data: TransactionCreate
):
    """
    Record a new transaction (expense or income)
    """
    try:
        service = get_service()
        if data.type.lower() == "income":
            return service.add_income(
                farmerId=farmer_id,
                season=data.season,
                category=data.category,
                amount=data.amount,
                notes=data.notes,
                relatedCropId=data.relatedCropId
            )
        else:
            return service.add_expense(
                farmerId=farmer_id,
                season=data.season,
                category=data.category,
                amount=data.amount,
                notes=data.notes,
                relatedCropId=data.relatedCropId
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _get_category_color(category: str):
    cat = category.lower()
    if "seeds" in cat: return "green"
    if "labor" in cat: return "orange"
    if "fert" in cat: return "blue"
    if "machin" in cat or "tractor" in cat: return "red"
    return "blue" # default
