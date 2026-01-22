"""
Time utilities - Date operations
"""

from datetime import date,  timedelta


def days_between(start_date: date, end_date: date) -> int:
    """
    Calculate days between two dates
    
    Args:
        start_date: Earlier date
        end_date: Later date
        
    Returns:
        Number of days (can be negative if end < start)
    """
    delta = end_date - start_date
    return delta.days


def add_days(base_date: date, days: int) -> date:
    """
    Add days to a date
    
    Args:
        base_date: Starting date
        days: Number of days to add (can be negative)
        
    Returns:
        New date
    """
    return base_date + timedelta(days=days)


def format_date(d: date) -> str:
    """Format date for display"""
    return d.strftime("%d %b %Y")
