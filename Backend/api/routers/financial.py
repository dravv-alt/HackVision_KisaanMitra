"""
Finance Management API Router
Handles financial transactions, income, expenses, and tracking
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from bson import ObjectId

from Backend.api.dependencies import get_db_client

router = APIRouter(prefix="/finance", tags=["Finance"])

# Request/Response Models
class TransactionRequest(BaseModel):
    farmer_id: str
    type: str  # income or expense
    category: str
    amount: float
    description: str
    date: Optional[str] = None
    payment_method: Optional[str] = "cash"

class TransactionResponse(BaseModel):
    transaction_id: str
    farmer_id: str
    type: str
    category: str
    amount: float
    description: str
    date: str
    payment_method: str
    created_at: str

# API Endpoints

@router.post("/transaction")
async def add_transaction(
    request: TransactionRequest,
    db_client = Depends(get_db_client)
):
    """Add new financial transaction"""
    try:
        db = db_client["kisanmitra"]
        
        transaction = {
            "farmer_id": request.farmer_id,
            "type": request.type,
            "category": request.category,
            "amount": request.amount,
            "description": request.description,
            "date": request.date or datetime.utcnow().isoformat(),
            "payment_method": request.payment_method,
            "created_at": datetime.utcnow()
        }
        
        result = db.financial_transactions.insert_one(transaction)
        transaction["transaction_id"] = str(result.inserted_id)
        transaction["_id"] = str(result.inserted_id)
        
        return {
            "success": True,
            "message": "Transaction added successfully",
            "transaction": transaction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions/{farmer_id}")
async def get_transactions(
    farmer_id: str,
    type: Optional[str] = None,
    limit: int = 50,
    db_client = Depends(get_db_client)
):
    """Get all transactions for a farmer"""
    try:
        db = db_client["kisanmitra"]
        
        query = {"farmer_id": farmer_id}
        if type:
            query["type"] = type
        
        transactions = list(db.financial_transactions.find(query).sort("date", -1).limit(limit))
        
        for txn in transactions:
            txn["_id"] = str(txn["_id"])
            txn["transaction_id"] = txn.get("transaction_id", str(txn["_id"]))
        
        return {
            "success": True,
            "transactions": transactions,
            "count": len(transactions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary/{farmer_id}")
async def get_financial_summary(
    farmer_id: str,
    days: int = 30,
    db_client = Depends(get_db_client)
):
    """Get financial summary for a farmer"""
    try:
        db = db_client["kisanmitra"]
        
        # Get transactions from last N days
        start_date = datetime.utcnow() - timedelta(days=days)
        
        transactions = list(db.financial_transactions.find({
            "farmer_id": farmer_id,
            "created_at": {"$gte": start_date}
        }))
        
        total_income = sum(t["amount"] for t in transactions if t["type"] == "आय" or t["type"] == "income")
        total_expense = sum(t["amount"] for t in transactions if t["type"] == "खर्च" or t["type"] == "expense")
        net_profit = total_income - total_expense
        
        # Category breakdown
        expense_by_category = {}
        income_by_category = {}
        
        for txn in transactions:
            category = txn.get("category", "other")
            amount = txn.get("amount", 0)
            
            if txn["type"] in ["खर्च", "expense"]:
                expense_by_category[category] = expense_by_category.get(category, 0) + amount
            else:
                income_by_category[category] = income_by_category.get(category, 0) + amount
        
        return {
            "success": True,
            "summary": {
                "total_income": total_income,
                "total_expense": total_expense,
                "net_profit": net_profit,
                "transaction_count": len(transactions),
                "expense_by_category": expense_by_category,
                "income_by_category": income_by_category,
                "period_days": days
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/transaction/{transaction_id}")
async def delete_transaction(
    transaction_id: str,
    db_client = Depends(get_db_client)
):
    """Delete a transaction"""
    try:
        db = db_client["kisanmitra"]
        
        result = db.financial_transactions.delete_one({"_id": ObjectId(transaction_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return {
            "success": True,
            "message": "Transaction deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
