"""
Reminder Engine - generates scheme deadline reminders
"""
from typing import List
from datetime import datetime, timedelta
from ..models import (
    ReminderRecord, SchemeEligibilityResult, FarmerProfile
)
from ..constants import REMINDER_DAYS, ReminderStatus, Language


class ReminderEngine:
    """Engine for generating scheme reminders"""
    
    def __init__(self):
        """Initialize reminder engine"""
        self.reminder_intervals = REMINDER_DAYS  # [15, 7, 1] days before
    
    def generate(
        self,
        scheme_results: List[SchemeEligibilityResult],
        farmer: FarmerProfile
    ) -> List[ReminderRecord]:
        """
        Generate reminders for eligible schemes with deadlines
        
        Args:
            scheme_results: Scheme eligibility results
            farmer: Farmer profile
            
        Returns:
            List of reminder records to be saved
        """
        reminders = []
        now = datetime.now()
        
        for result in scheme_results:
            # Only create reminders for eligible schemes with deadlines
            if not result.eligible:
                continue
            
            # Need to get deadline from original scheme record
            # For now, infer from deadline_warning
            if not result.deadline_warning:
                continue
            
            # Extract days from warning message
            days_left = self._extract_days_from_warning(result.deadline_warning)
            if days_left is None:
                continue
            
            deadline = now + timedelta(days=days_left)
            
            # Generate reminders at specified intervals
            for interval_days in self.reminder_intervals:
                if interval_days >= days_left:
                    continue  # Skip if interval is beyond current time
                
                reminder_datetime = deadline - timedelta(days=interval_days)
                
                # Don't create reminders for the past
                if reminder_datetime < now:
                    continue
                
                # Create reminder
                message = self._build_reminder_message(
                    result.scheme_name,
                    interval_days,
                    Language.ENGLISH
                )
                message_hi = self._build_reminder_message(
                    result.scheme_name_hi or result.scheme_name,
                    interval_days,
                    Language.HINDI
                )
                
                reminder = ReminderRecord(
                    farmer_id=farmer.farmer_id,
                    scheme_key=result.scheme_key,
                    scheme_name=result.scheme_name,
                    reminder_datetime=reminder_datetime,
                    message=message,
                    message_hi=message_hi,
                    status=ReminderStatus.PENDING
                )
                
                reminders.append(reminder)
        
        return reminders
    
    def _extract_days_from_warning(self, warning: str) -> int:
        """Extract number of days from deadline warning text"""
        try:
            # Look for pattern like "X days"
            import re
            match = re.search(r'(\d+)\s+days?', warning)
            if match:
                return int(match.group(1))
        except:
            pass
        return None
    
    def _build_reminder_message(
        self,
        scheme_name: str,
        days_before: int,
        language: Language
    ) -> str:
        """Build reminder message text"""
        if language == Language.HINDI:
            if days_before == 1:
                return f"⚠️ कल आखिरी दिन! {scheme_name} के लिए आवेदन करें।"
            elif days_before == 7:
                return f"🔔 याद दिलाना: {scheme_name} की समय सीमा 7 दिनों में समाप्त होती है। जल्द आवेदन करें।"
            else:
                return f"📌 {scheme_name} की समय सीमा {days_before} दिनों में समाप्त होती है। तैयारी शुरू करें।"
        else:  # English
            if days_before == 1:
                return f"⚠️ Last day tomorrow! Apply for {scheme_name} scheme."
            elif days_before == 7:
                return f"🔔 Reminder: {scheme_name} deadline in 7 days. Apply soon."
            else:
                return f"📌 {scheme_name} deadline in {days_before} days. Start preparing documents."
