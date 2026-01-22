"""
CLI Demo - Manual Testing Runner for inventory Management
Demonstrates complete functionality without web framework
"""

import sys
from datetime import datetime


def print_header(text: str):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_stock_card(card, rank: int = None):
    """Pretty print a stock card"""
    if rank:
        print(f"\n{'─' * 80}")
        print(f"📦 RANK #{rank}: {card.cropName.upper()}")
    else:
        print(f"\n{'─' * 80}")
        print(f"📦 {card.cropName.upper()}")
    
    print(f"{'─' * 80}")
    print(f"  Item ID: {card.itemId}")
    print(f"  Quantity: {card.quantityKg} kg")
    print(f"  Grade: {card.grade.value}")
    print(f"  Storage: {card.storageType.value}")
    print(f"  Stage: {card.stage.value}")
    print(f"\n  📅 Storage Info:")
    print(f"     Stored on: {card.storedAt.strftime('%Y-%m-%d')}")
    print(f"     Shelf life remaining: {card.shelfLifeRemainingDays} days")
    print(f"     Expected sell by: {card.expectedSellBy.strftime('%Y-%m-%d')}")
    
    # Health status with emoji
    health_emoji = {
        "good": "✅",
        "warning": "⚠️",
        "critical": "🚨"
    }
    print(f"\n  {health_emoji.get(card.healthStatus.value, '❓')} Health: {card.healthStatus.value.upper()}")
    print(f"     Spoilage Risk: {card.spoilageRisk}")
    
    # Sell priority
    sell_emoji = "🔥" if card.sellNowRecommendation else "📊"
    print(f"\n  {sell_emoji} Sell Priority: #{card.sellPriorityRank}")
    print(f"     Sell Now: {'YES' if card.sellNowRecommendation else 'NO'}")
    
    # Reasons
    print(f"\n  💡 Reasons:")
    for reason in card.reasons:
        print(f"     • {reason}")
    
    # Suggested action
    print(f"\n  🎯 Suggested Action:")
    print(f"     {card.suggestedNextAction}")
    print(f"{'─' * 80}")


def print_dashboard_summary(output):
    """Print dashboard summary"""
    print_header("inventory DASHBOARD SUMMARY")
    
    print(f"\n🏠 {output.header}")
    print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Language: {output.language.value.upper()}")
    
    print(f"\n📊 Stock Overview:")
    print(f"   Total Items: {output.totalStockCount}")
    print(f"   ⚠️  Warning: {output.warningCount}")
    print(f"   🚨 Critical: {output.criticalCount}")
    
    # Urgency indicator
    urgency_emoji = {
        "low": "🟢",
        "medium": "🟡",
        "high": "🔴"
    }
    print(f"\n{urgency_emoji.get(output.urgencyLevel.value, '⚪')} Urgency Level: {output.urgencyLevel.value.upper()}")
    
    print(f"\n🗣️  Voice Summary:")
    print(f"   \"{output.speechText}\"")
    
    print(f"\n📝 Detailed Reasoning:")
    for line in output.detailedReasoning.split('\n'):
        print(f"   {line}")


def run_basic_demo():
    """Run basic inventory dashboard demo"""
    from .service import inventoryService
    
    print_header("inventory MANAGEMENT - BASIC DEMO")
    
    # Initialize service
    service = inventoryService()
    
    # Test farmer ID
    farmer_id = "FARMER001"
    
    print(f"\n🧑‍🌾 Farmer ID: {farmer_id}")
    print("📥 Fetching inventory dashboard...")
    
    # Get dashboard
    output = service.get_inventory_dashboard(farmer_id)
    
    # Print summary
    print_dashboard_summary(output)
    
    # Print all stock cards
    print_header("STOCK CARDS (SORTED BY SELL PRIORITY)")
    
    for card in output.stockCards:
        print_stock_card(card, card.sellPriorityRank)
    
    return service, farmer_id, output


def run_sell_simulation(service, farmer_id):
    """Simulate sell action"""
    print_header("SIMULATION: SELL ACTION")
    
    # Get current dashboard
    current = service.get_inventory_dashboard(farmer_id, include_reminders=False)
    
    if not current.stockCards:
        print("\n❌ No stock items to sell!")
        return
    
    # Sell the highest priority item
    top_item = current.stockCards[0]
    sell_quantity = min(50.0, top_item.quantityKg)
    
    print(f"\n📤 Selling: {top_item.cropName}")
    print(f"   Quantity: {sell_quantity} kg")
    print(f"   From total: {top_item.quantityKg} kg")
    print(f"   Price: ₹30/kg (simulated)")
    
    # Execute sell
    updated = service.simulate_sell_action(
        farmer_id,
        top_item.itemId,
        sell_quantity,
        price_per_kg=30.0
    )
    
    print(f"\n✅ Sell action completed!")
    print(f"\n📊 Updated Dashboard:")
    print(f"   Total Items: {updated.totalStockCount}")
    print(f"   Warning: {updated.warningCount}")
    print(f"   Critical: {updated.criticalCount}")
    
    # Show updated top item
    updated_item = next((c for c in updated.stockCards if c.itemId == top_item.itemId), None)
    if updated_item:
        print(f"\n📦 Updated Item: {updated_item.cropName}")
        print(f"   New Quantity: {updated_item.quantityKg} kg")
        print(f"   Stage: {updated_item.stage.value}")


def run_spoilage_simulation(service, farmer_id):
    """Simulate spoilage action"""
    print_header("SIMULATION: SPOILAGE ACTION")
    
    # Get current dashboard
    current = service.get_inventory_dashboard(farmer_id, include_reminders=False)
    
    if not current.stockCards:
        print("\n❌ No stock items!")
        return
    
    # Simulate spoilage on a warning/critical item
    target_item = None
    for card in current.stockCards:
        if card.healthStatus.value in ["warning", "critical"]:
            target_item = card
            break
    
    if not target_item:
        target_item = current.stockCards[0]
    
    spoilage_quantity = min(20.0, target_item.quantityKg)
    
    print(f"\n🗑️  Spoilage detected: {target_item.cropName}")
    print(f"   Quantity spoiled: {spoilage_quantity} kg")
    print(f"   Reason: Moisture damage (simulated)")
    
    # Execute spoilage
    updated = service.simulate_spoilage_action(
        farmer_id,
        target_item.itemId,
        spoilage_quantity,
        notes="Moisture damage during storage"
    )
    
    print(f"\n✅ Spoilage recorded!")
    print(f"\n📊 Updated Dashboard:")
    print(f"   Total Items: {updated.totalStockCount}")
    print(f"   Warning: {updated.warningCount}")
    print(f"   Critical: {updated.criticalCount}")
    
    # Show updated item
    updated_item = next((c for c in updated.stockCards if c.itemId == target_item.itemId), None)
    if updated_item:
        print(f"\n📦 Updated Item: {updated_item.cropName}")
        print(f"   New Quantity: {updated_item.quantityKg} kg")
        print(f"   Spoilage Risk: {updated_item.spoilageRisk}")


def run_interactive_demo():
    """Run interactive demo with menu"""
    service, farmer_id, output = run_basic_demo()
    
    while True:
        print_header("INTERACTIVE MENU")
        print("\n1. Refresh Dashboard")
        print("2. Simulate SELL Action")
        print("3. Simulate SPOILAGE Action")
        print("4. View Stock Cards")
        print("5. Switch Farmer (FARMER002 - English)")
        print("6. Exit")
        
        choice = input("\n👉 Enter choice (1-6): ").strip()
        
        if choice == "1":
            output = service.get_inventory_dashboard(farmer_id)
            print_dashboard_summary(output)
            
        elif choice == "2":
            run_sell_simulation(service, farmer_id)
            
        elif choice == "3":
            run_spoilage_simulation(service, farmer_id)
            
        elif choice == "4":
            output = service.get_inventory_dashboard(farmer_id, include_reminders=False)
            print_header("STOCK CARDS")
            for card in output.stockCards:
                print_stock_card(card, card.sellPriorityRank)
                
        elif choice == "5":
            farmer_id = "FARMER002"
            print(f"\n✅ Switched to {farmer_id} (English language)")
            output = service.get_inventory_dashboard(farmer_id)
            print_dashboard_summary(output)
            
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
            
        else:
            print("\n❌ Invalid choice!")


def main():
    """Main entry point"""
    print("\n" + "🌾" * 40)
    print("  inventory MANAGEMENT - CLI DEMO")
    print("  Voice-First Farming Assistant")
    print("🌾" * 40)
    
    try:
        # Check if interactive mode
        if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
            run_interactive_demo()
        else:
            # Run automated demo
            service, farmer_id, output = run_basic_demo()
            
            # Run simulations
            run_sell_simulation(service, farmer_id)
            run_spoilage_simulation(service, farmer_id)
            
            # Final dashboard
            print_header("FINAL DASHBOARD AFTER SIMULATIONS")
            final = service.get_inventory_dashboard(farmer_id)
            print_dashboard_summary(final)
            
            print("\n" + "=" * 80)
            print("  ✅ DEMO COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            print("\n💡 Run with --interactive flag for interactive menu")
            print("   Example: python cli_demo.py --interactive")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
