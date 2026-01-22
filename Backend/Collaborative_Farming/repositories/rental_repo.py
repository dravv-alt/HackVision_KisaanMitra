"""
Rental Repository for Collaborative Farming
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import uuid

from ..models import RentalRequest
from ..constants import RentalStatus, PaymentMethod


class RentalRepo:
    def __init__(self):
        self._rentals: Dict[str, RentalRequest] = {}
        self.seed_mock_rentals_if_empty()

    def create_rental_request(self, request: RentalRequest) -> RentalRequest:
        """Create a new rental request"""
        self._rentals[request.rentalId] = request
        return request

    def get_rental(self, rental_id: str) -> Optional[RentalRequest]:
        """Fetch a specific rental request"""
        return self._rentals.get(rental_id)

    def list_rentals_by_farmer(self, farmer_id: str, as_owner: bool = False) -> List[RentalRequest]:
        """List rentals for a farmer (as renter or owner)"""
        if as_owner:
            return [r for r in self._rentals.values() if r.ownerFarmerId == farmer_id]
        return [r for r in self._rentals.values() if r.renterFarmerId == farmer_id]

    def update_rental_status(self, rental_id: str, status: RentalStatus):
        """Update rental status"""
        if rental_id in self._rentals:
            self._rentals[rental_id].status = status
            self._rentals[rental_id].updatedAt = datetime.now()

    def seed_mock_rentals_if_empty(self):
        """Seed mock rentals if repository is empty"""
        if self._rentals:
            return
            
        now = datetime.now()
        
        # Mock rental for FARMER001 (Ongoing)
        rental1 = RentalRequest(
            rentalId=str(uuid.uuid4()),
            listingId="MOCK_LISTING_1", # Reference
            renterFarmerId="FARMER001",
            ownerFarmerId="FARMER002",
            startDate=now - timedelta(days=2),
            endDate=now + timedelta(days=1),
            totalAmount=2400.0,
            serviceFee=0.0,
            paymentMethod=PaymentMethod.CASH_ON_DELIVERY,
            status=RentalStatus.ONGOING
        )
        
        # Mock requested rental for FARMER001
        rental2 = RentalRequest(
            rentalId=str(uuid.uuid4()),
            listingId="MOCK_LISTING_2",
            renterFarmerId="FARMER001",
            ownerFarmerId="FARMER003",
            startDate=now + timedelta(days=5),
            endDate=now + timedelta(days=7),
            totalAmount=1600.0,
            serviceFee=0.0,
            paymentMethod=PaymentMethod.CASH_ON_DELIVERY,
            status=RentalStatus.REQUESTED
        )
        
        self._rentals[rental1.rentalId] = rental1
        self._rentals[rental2.rentalId] = rental2
