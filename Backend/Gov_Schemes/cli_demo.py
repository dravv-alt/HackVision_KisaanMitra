"""
CLI Demo - Manual Testing Runner for Government Schemes
Demonstrates complete functionality without web framework
Offline-safe with mock data
"""

import sys
from datetime import datetime


def print_header(text: str):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_scheme_card(card, index: int = None):
    """Pretty print a scheme card"""
    if index:
        print(f"\n{'-' * 80}")
        print(f"SCHEME #{index}: {card.schemeName}")
    else:
        print(f"\n{'-' * 80}")
        print(f"{card.schemeName}")
    
    print(f"{'-' * 80}")
    
    # New badge
    if card.isNew:
        print("  [NEW] Recently Added!")
    
    print(f"  Category: {card.categoryDisplay}")
    print(f"  Scope: {card.scope}")
    
    print(f"\n  Description:")
    print(f"     {card.description}")
    
    print(f"\n  Benefits:")
    print(f"     {card.benefits}")
    
    if card.eligibility:
        print(f"\n  Eligibility:")
        print(f"     {card.eligibility}")
    
    if card.howToApply:
        print(f"\n  How to Apply:")
        print(f"     {card.howToApply}")
    
    if card.officialLink:
        print(f"\n  Official Link: {card.officialLink}")
    
    if card.contactNumber:
        print(f"  Contact: {card.contactNumber}")
    
    if card.daysRemaining is not None:
        if card.daysRemaining > 0:
            print(f"\n  [!] Application deadline in {card.daysRemaining} days")
        else:
            print(f"\n  [!] Application deadline passed")
    
    print(f"{'-' * 80}")


def print_dashboard_summary(output):
    """Print dashboard summary"""
    print_header("GOVERNMENT SCHEMES DASHBOARD")
    
    print(f"\n{output.header}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Language: {output.language.value.upper()}")
    
    print(f"\n  Total Schemes: {output.totalSchemes}")
    if output.newSchemesCount > 0:
        print(f"  [NEW] New Schemes: {output.newSchemesCount}")
    
    # Filters applied
    if output.filterApplied:
        print(f"\n  Filters Applied:")
        if output.filterApplied.get("state"):
            print(f"    State: {output.filterApplied['state']}")
        if output.filterApplied.get("district"):
            print(f"    District: {output.filterApplied['district']}")
        if output.filterApplied.get("category"):
            print(f"    Category: {output.filterApplied['category'].value}")
    
    print(f"\n  Voice Summary:")
    print(f"     \"{output.speechText}\"")
    
    print(f"\n  Detailed Info:")
    for line in output.detailedReasoning.split('\n'):
        print(f"     {line}")


def run_basic_demo():
    """Run basic schemes display demo"""
    from .service import GovSchemesDisplayService
    
    print_header("GOVERNMENT SCHEMES - BASIC DEMO")
    
    # Initialize service
    service = GovSchemesDisplayService()
    
    # Test farmer ID (Maharashtra, Nashik)
    farmer_id = "FARMER001"
    
    print(f"\nFarmer ID: {farmer_id}")
    print("Fetching government schemes...")
    
    # Get schemes display
    output = service.get_schemes_display(farmer_id)
    
    # Print summary
    print_dashboard_summary(output)
    
    # Print scheme cards
    print_header("SCHEME CARDS")
    
    for idx, card in enumerate(output.schemeCards, start=1):
        print_scheme_card(card, idx)
    
    return service, farmer_id, output


def run_filter_demo(service, farmer_id):
    """Demonstrate filtering capabilities"""
    from .constants import SchemeCategory
    
    print_header("FILTER DEMO: LOAN SCHEMES ONLY")
    
    # Filter by category
    output = service.get_schemes_display(
        farmer_id,
        category=SchemeCategory.LOAN
    )
    
    print(f"\nFiltered Results: {output.totalSchemes} schemes")
    print(f"Category: {SchemeCategory.LOAN.value}")
    
    for idx, card in enumerate(output.schemeCards, start=1):
        print(f"\n  {idx}. {card.schemeName}")
        print(f"     {card.description[:100]}...")


def run_state_filter_demo(service):
    """Demonstrate state-level filtering"""
    print_header("FILTER DEMO: PUNJAB STATE SCHEMES")
    
    # Filter by state (different from farmer's state)
    output = service.get_schemes_display(
        "FARMER002",  # Punjab farmer
        state="Punjab"
    )
    
    print(f"\nPunjab Schemes: {output.totalSchemes} schemes")
    
    for idx, card in enumerate(output.schemeCards, start=1):
        print(f"\n  {idx}. {card.schemeName}")
        print(f"     Scope: {card.scope}")


def run_alerts_demo(service, farmer_id):
    """Demonstrate alert system"""
    print_header("ALERTS DEMO: NEW SCHEME NOTIFICATIONS")
    
    # Get alerts
    alerts = service.get_alerts_for_farmer(farmer_id)
    
    print(f"\nTotal Alerts: {len(alerts)}")
    
    for idx, alert in enumerate(alerts, start=1):
        print(f"\n  Alert #{idx}:")
        print(f"    Title: {alert.title}")
        print(f"    Urgency: {alert.urgency.value.upper()}")
        print(f"    Status: {alert.status.value}")
        print(f"    Message: {alert.message[:150]}...")
        print(f"    Created: {alert.createdAt.strftime('%Y-%m-%d %H:%M')}")


def run_interactive_demo():
    """Run interactive demo with menu"""
    service, farmer_id, output = run_basic_demo()
    
    while True:
        print_header("INTERACTIVE MENU")
        print("\n1. Refresh Schemes Display")
        print("2. Filter by Category (Loans)")
        print("3. Filter by Category (Insurance)")
        print("4. Filter by Category (Subsidy)")
        print("5. View Punjab State Schemes")
        print("6. View Alerts")
        print("7. Switch to English Farmer (FARMER002)")
        print("8. Exit")
        
        choice = input("\nEnter choice (1-8): ").strip()
        
        if choice == "1":
            output = service.get_schemes_display(farmer_id, force_refresh=True)
            print_dashboard_summary(output)
            
        elif choice == "2":
            run_filter_demo(service, farmer_id)
            
        elif choice == "3":
            from .constants import SchemeCategory
            output = service.get_schemes_display(
                farmer_id,
                category=SchemeCategory.INSURANCE
            )
            print(f"\nInsurance Schemes: {output.totalSchemes}")
            for card in output.schemeCards:
                print(f"  - {card.schemeName}")
                
        elif choice == "4":
            from .constants import SchemeCategory
            output = service.get_schemes_display(
                farmer_id,
                category=SchemeCategory.SUBSIDY
            )
            print(f"\nSubsidy Schemes: {output.totalSchemes}")
            for card in output.schemeCards:
                print(f"  - {card.schemeName}")
                
        elif choice == "5":
            run_state_filter_demo(service)
            
        elif choice == "6":
            run_alerts_demo(service, farmer_id)
            
        elif choice == "7":
            farmer_id = "FARMER002"
            print(f"\nSwitched to {farmer_id} (English, Punjab)")
            output = service.get_schemes_display(farmer_id)
            print_dashboard_summary(output)
            
        elif choice == "8":
            print("\nGoodbye!")
            break
            
        else:
            print("\nInvalid choice!")


def main():
    """Main entry point"""
    print("\n" + "=" * 80)
    print("  GOVERNMENT SCHEMES DISPLAY - CLI DEMO")
    print("  Voice-First Farming Assistant")
    print("=" * 80)
    
    try:
        # Check if interactive mode
        if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
            run_interactive_demo()
        else:
            # Run automated demo
            service, farmer_id, output = run_basic_demo()
            
            # Run filter demos
            run_filter_demo(service, farmer_id)
            run_state_filter_demo(service)
            run_alerts_demo(service, farmer_id)
            
            print("\n" + "=" * 80)
            print("  [SUCCESS] DEMO COMPLETED!")
            print("=" * 80)
            print("\nRun with --interactive flag for interactive menu")
            print("   Example: python -m gov_schemes.cli_demo --interactive")
            
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
