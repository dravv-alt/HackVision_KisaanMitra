"""
Transaction Repository - Ledger Data Access
Provides interface for transaction CRUD operations
IMPORTANT: Mock fallback ONLY when DB unavailable or empty
"""

from typing import List, Optional, Dict
from datetime import datetime, timedelta
import uuid
from financial_tracking.models import FinanceTransaction
from financial_tracking.constants import (
    TransactionType,
    ExpenseCategory,
    IncomeCategory,
    SeasonType,
)


class TransactionRepo:
    """
    Transaction repository with in-memory fallback
    In production, this would connect to MongoDB
    """

    def __init__(self):
        """Initialize repository with empty in-memory storage"""
        self._transactions: List[FinanceTransaction] = []
        self._mock_seeded: Dict[str, bool] = {}  # Track which farmers have mock data

    def add_transaction(self, tx: FinanceTransaction) -> FinanceTransaction:
        """
        Add a new transaction to the ledger
        
        Args:
            tx: Transaction to add
            
        Returns:
            The added transaction
        """
        # In production: db.transactions.insert_one(tx.dict())
        # For hackathon demo: store in memory
        self._transactions.append(tx)
        return tx

    def list_transactions(
        self, 
        farmerId: str, 
        season: Optional[str] = None
    ) -> List[FinanceTransaction]:
        """
        List all transactions for a farmer, optionally filtered by season
        
        Args:
            farmerId: Farmer ID
            season: Optional season filter
            
        Returns:
            List of transactions
        """
        # In production: db.transactions.find({"farmerId": farmerId, ...})
        
        transactions = [
            tx for tx in self._transactions
            if tx.farmerId == farmerId
        ]
        
        if season:
            transactions = [tx for tx in transactions if tx.season == season]
        
        return transactions

    def seed_mock_data_if_empty(self, farmerId: str, season: str = SeasonType.KHARIF.value) -> None:
        """
        Seed realistic mock data ONLY if there are no transactions
        This ensures hackathon demos never fail due to empty DB
        
        IMPORTANT: Only used as emergency fallback!
        
        Args:
            farmerId: Farmer to seed data for
            season: Season to use for mock data
        """
        # Check if this farmer already has data
        existing_txs = self.list_transactions(farmerId, season)
        
        if len(existing_txs) > 0:
            # Farmer has actual data - DO NOT override with mock!
            return
        
        # Check if already seeded for demo
        seed_key = f"{farmerId}_{season}"
        if self._mock_seeded.get(seed_key, False):
            return
        
        print(f"⚠️  No transactions found for farmer {farmerId} ({season})")
        print(f"   Seeding realistic mock data for demo purposes...")
        
        # Create realistic mock transactions for Indian farming context
        base_date = datetime.now() - timedelta(days=90)  # 3 months ago
        
        mock_transactions = [
            # Seed purchase
            FinanceTransaction(
                transactionId=str(uuid.uuid4()),
                farmerId=farmerId,
                season=season,
                type=TransactionType.EXPENSE,
                category=ExpenseCategory.SEEDS.value,
                amount=8500.00,
                notes="Hybrid wheat seeds - 50kg",
                ts=base_date + timedelta(days=1),
            ),
            
            # Fertilizer - First application
            FinanceTransaction(
                transactionId=str(uuid.uuid4()),
                farmerId=farmerId,
                season=season,
                type=TransactionType.EXPENSE,
                category=ExpenseCategory.FERTILIZER.value,
                amount=12000.00,
                notes="DAP and Urea - First application",
                ts=base_date + timedelta(days=5),
            ),
            
            # Labour - Sowing
            FinanceTransaction(
                transactionId=str(uuid.uuid4()),
                farmerId=farmerId,
                season=season,
                type=TransactionType.EXPENSE,
                category=ExpenseCategory.LABOUR.value,
                amount=6000.00,
                notes="Labour for sowing - 4 workers for 2 days",
                ts=base_date + timedelta(days=2),
            ),
            
            # Water/Irrigation
            FinanceTransaction(
                transactionId=str(uuid.uuid4()),
                farmerId=farmerId,
                season=season,
                type=TransactionType.EXPENSE,
                category=ExpenseCategory.WATER.value,
                amount=4500.00,
                notes="Irrigation water charges",
                ts=base_date + timedelta(days=15),
            ),
            
            # Electricity for pump
            FinanceTransaction(
                transactionId=str(uuid.uuid4()),
                farmerId=farmerId,
                season=season,
                type=TransactionType.EXPENSE,
                category=ExpenseCategory.ELECTRICITY.value,
                amount=8000.00,
                notes="Electricity for irrigation pump - 2 months",
                ts=base_date + timedelta(days=30),
            ),
            
            # Pesticide
            FinanceTransaction(
                transactionId=str(uuid.uuid4()),
                farmerId=farmerId,
                season=season,
                type=TransactionType.EXPENSE,
                category=ExpenseCategory.PESTICIDE.value,
                amount=5500.00,
                notes="Pesticide spray for pest control",
                ts=base_date + timedelta(days=25),
            ),
            
            # Labour - Weeding
            FinanceTransaction(
                transactionId=str(uuid.uuid4()),
                farmerId=farmerId,
                season=season,
                type=TransactionType.EXPENSE,
                category=ExpenseCategory.LABOUR.value,
                amount=7500.00,
                notes="Weeding labour - 5 workers for 2 days",
                ts=base_date + timedelta(days=35),
            ),
            
            # Fertilizer - Second application
            FinanceTransaction(
                transactionId=str(uuid.uuid4()),
                farmerId=farmerId,
                season=season,
                type=TransactionType.EXPENSE,
                category=ExpenseCategory.FERTILIZER.value,
                amount=9000.00,
                notes="Second fertilizer application - Urea",
                ts=base_date + timedelta(days=40),
            ),
            
            # Labour - Harvesting
            FinanceTransaction(
                transactionId=str(uuid.uuid4()),
                farmerId=farmerId,
                season=season,
                type=TransactionType.EXPENSE,
                category=ExpenseCategory.LABOUR.value,
                amount=15000.00,
                notes="Harvesting labour - 10 workers for 3 days",
                ts=base_date + timedelta(days=85),
            ),
            
            # Transport to mandi
            FinanceTransaction(
                transactionId=str(uuid.uuid4()),
                farmerId=farmerId,
                season=season,
                type=TransactionType.EXPENSE,
                category=ExpenseCategory.TRANSPORT.value,
                amount=8500.00,
                notes="Transport to mandi - 3 trips",
                ts=base_date + timedelta(days=87),
            ),
            
            # Storage/loading charges
            FinanceTransaction(
                transactionId=str(uuid.uuid4()),
                farmerId=farmerId,
                season=season,
                type=TransactionType.EXPENSE,
                category=ExpenseCategory.STORAGE.value,
                amount=3000.00,
                notes="Mandi storage and loading charges",
                ts=base_date + timedelta(days=87),
            ),
            
            # INCOME - Main crop sale (but at slightly low price)
            FinanceTransaction(
                transactionId=str(uuid.uuid4()),
                farmerId=farmerId,
                season=season,
                type=TransactionType.INCOME,
                category=IncomeCategory.SALE.value,
                amount=78000.00,
                notes="Wheat sale - 35 quintals @ ₹2230/quintal",
                ts=base_date + timedelta(days=88),
            ),
            
            # INCOME - Government subsidy
            FinanceTransaction(
                transactionId=str(uuid.uuid4()),
                farmerId=farmerId,
                season=season,
                type=TransactionType.INCOME,
                category=IncomeCategory.SUBSIDY.value,
                amount=5000.00,
                notes="PM-KISAN subsidy installment",
                ts=base_date + timedelta(days=90),
            ),
        ]
        
        # Add all mock transactions
        for tx in mock_transactions:
            self.add_transaction(tx)
        
        self._mock_seeded[seed_key] = True
        print(f"✅ Seeded {len(mock_transactions)} mock transactions for demo")

    def get_transaction_by_id(self, transaction_id: str) -> Optional[FinanceTransaction]:
        """Get a single transaction by ID"""
        for tx in self._transactions:
            if tx.transactionId == transaction_id:
                return tx
        return None

    def update_transaction(self, transaction_id: str, updates: Dict) -> Optional[FinanceTransaction]:
        """Update a transaction"""
        tx = self.get_transaction_by_id(transaction_id)
        if tx:
            for key, value in updates.items():
                if hasattr(tx, key):
                    setattr(tx, key, value)
            tx.updatedAt = datetime.now()
            return tx
        return None

    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete a transaction"""
        for i, tx in enumerate(self._transactions):
            if tx.transactionId == transaction_id:
                self._transactions.pop(i)
                return True
        return False
