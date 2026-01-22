"""
Rental Engine for Collaborative Farming
"""

from typing import Optional
from datetime import datetime, timedelta
import uuid

from ..models import RentalRequest, EquipmentListing
from ..constants import RentalStatus, ListingStatus, PaymentMethod
from ..repositories import RentalRepo, EquipmentRepo


class RentalEngine:
    """Engine for managing the rental lifecycle and workflow"""
    
    def __init__(self, rental_repo: RentalRepo, equipment_repo: EquipmentRepo):
        self.rental_repo = rental_repo
        self.equipment_repo = equipment_repo

    def request_booking(
        self, 
        renter_id: str, 
        listing_id: str, 
        start_date: datetime, 
        end_date: datetime,
        payment_method: PaymentMethod = PaymentMethod.CASH_ON_DELIVERY
    ) -> RentalRequest:
        """Create a new booking request with validations"""
        listing = self.equipment_repo.get_listing(listing_id)
        
        if not listing:
            raise ValueError("Equipment listing not found")
            
        if listing.status != ListingStatus.AVAILABLE:
            raise ValueError("Equipment is currently not available for rent")
            
        if start_date < listing.availableFrom or end_date > listing.availableTo:
            raise ValueError("Requested dates are outside the equipment's availability range")
            
        # Calculate total amount
        days = (end_date - start_date).days + 1
        total_amount = days * listing.pricePerDay
        
        request = RentalRequest(
            rentalId=str(uuid.uuid4()),
            listingId=listing_id,
            renterFarmerId=renter_id,
            ownerFarmerId=listing.ownerFarmerId,
            startDate=start_date,
            endDate=end_date,
            totalAmount=total_amount,
            paymentMethod=payment_method,
            status=RentalStatus.REQUESTED
        )
        
        return self.rental_repo.create_rental_request(request)

    def approve_request(self, owner_id: str, rental_id: str) -> RentalRequest:
        """Approve a rental request and block the equipment"""
        rental = self.rental_repo.get_rental(rental_id)
        
        if not rental:
            raise ValueError("Rental request not found")
            
        if rental.ownerFarmerId != owner_id:
            raise ValueError("Only the owner can approve this request")
            
        # Update rental status
        self.rental_repo.update_rental_status(rental_id, RentalStatus.APPROVED)
        
        # Block the listing
        self.equipment_repo.update_listing_status(rental.listingId, ListingStatus.BOOKED)
        
        return self.rental_repo.get_rental(rental_id)

    def reject_request(self, owner_id: str, rental_id: str) -> RentalRequest:
        """Reject a rental request"""
        rental = self.rental_repo.get_rental(rental_id)
        
        if not rental:
            raise ValueError("Rental request not found")
            
        if rental.ownerFarmerId != owner_id:
            raise ValueError("Only the owner can reject this request")
            
        self.rental_repo.update_rental_status(rental_id, RentalStatus.REJECTED)
        return self.rental_repo.get_rental(rental_id)

    def start_rental(self, rental_id: str) -> RentalRequest:
        """Mark a rental as ongoing"""
        self.rental_repo.update_rental_status(rental_id, RentalStatus.ONGOING)
        return self.rental_repo.get_rental(rental_id)

    def complete_rental(self, rental_id: str) -> RentalRequest:
        """Complete a rental and release the equipment"""
        rental = self.rental_repo.get_rental(rental_id)
        
        if not rental:
            raise ValueError("Rental request not found")
            
        # Update rental status
        self.rental_repo.update_rental_status(rental_id, RentalStatus.COMPLETED)
        
        # Release the listing
        self.equipment_repo.update_listing_status(rental.listingId, ListingStatus.AVAILABLE)
        
        return self.rental_repo.get_rental(rental_id)
