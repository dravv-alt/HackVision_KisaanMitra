"""
Reminder Engine for Collaborative Farming
"""

from typing import List
from datetime import datetime, timedelta
from ..models import RentalRequest, ReminderRecord
from ..constants import RentalStatus


class ReminderEngine:
    """Engine for generating reminders for rental deadlines"""
    
    def generate_rental_return_reminders(self, rentals: List[RentalRequest]) -> List[ReminderRecord]:
        """Generate reminders for ongoing rentals nearing end date"""
        reminders = []
        now = datetime.now()
        
        for rental in rentals:
            if rental.status != RentalStatus.ONGOING:
                continue
                
            # If end date is within 2 days
            if rental.endDate - now <= timedelta(days=2):
                # 2-day reminder
                reminders.append(ReminderRecord(
                    farmerId=rental.renterFarmerId,
                    title="Equipment Return Reminder",
                    message=f"Equipment rental ends in {(rental.endDate - now).days} days. Please prepare for return.",
                    reminderDateTime=rental.endDate - timedelta(days=1),
                    relatedRentalId=rental.rentalId
                ))
                
                # End date morning reminder
                reminders.append(ReminderRecord(
                    farmerId=rental.renterFarmerId,
                    title="Return Deadline Today",
                    message="Today is the final day for your equipment rental. Please return it to the owner.",
                    reminderDateTime=rental.endDate.replace(hour=8, minute=0),
                    relatedRentalId=rental.rentalId
                ))
                
        return reminders
