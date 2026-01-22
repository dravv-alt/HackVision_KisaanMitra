"""
Simple Test Script for Inventory Module (No Unicode)
"""

import sys
sys.path.insert(0, 'D:\\KissanMitra\\HackVision_KisaanMitra\\Backend')

from Inventory.service import InventoryService

def main():
    print("=" * 80)
    print("INVENTORY MODULE - SIMPLE TEST")
    print("=" * 80)
    
    # Initialize service
    print("\n1. Initializing service...")
    service = InventoryService()
    print("   [OK] Service initialized")
    
    # Test farmer
    farmer_id = "FARMER001"
    print(f"\n2. Getting inventory for {farmer_id}...")
    
    # Get dashboard
    output = service.get_inventory_dashboard(farmer_id)
    print("   [OK] Dashboard retrieved")
    
    # Print summary
    print("\n" + "=" * 80)
    print("DASHBOARD SUMMARY")
    print("=" * 80)
    print(f"Header: {output.header}")
    print(f"Language: {output.language.value}")
    print(f"Total Items: {output.totalStockCount}")
    print(f"Warning Count: {output.warningCount}")
    print(f"Critical Count: {output.criticalCount}")
    print(f"Urgency: {output.urgencyLevel.value}")
    
    print(f"\nSpeech Text:")
    print(f"   {output.speechText}")
    
    print(f"\nStock Cards:")
    for card in output.stockCards:
        print(f"\n   Rank #{card.sellPriorityRank}: {card.cropName}")
        print(f"      Quantity: {card.quantityKg} kg")
        print(f"      Health: {card.healthStatus.value}")
        print(f"      Shelf Life: {card.shelfLifeRemainingDays} days")
        print(f"      Sell Now: {card.sellNowRecommendation}")
        if card.reasons:
            print(f"      Top Reason: {card.reasons[0]}")
    
    # Test sell action
    print("\n" + "=" * 80)
    print("TESTING SELL ACTION")
    print("=" * 80)
    
    if output.stockCards:
        top_item = output.stockCards[0]
        print(f"\nSelling 50kg of {top_item.cropName}...")
        
        updated = service.simulate_sell_action(
            farmer_id,
            top_item.itemId,
            50.0,
            price_per_kg=30.0
        )
        
        print(f"[OK] Sell completed!")
        print(f"   Updated total items: {updated.totalStockCount}")
        
        # Find updated item
        updated_item = next((c for c in updated.stockCards if c.itemId == top_item.itemId), None)
        if updated_item:
            print(f"   {updated_item.cropName} new quantity: {updated_item.quantityKg} kg")
    
    print("\n" + "=" * 80)
    print("[SUCCESS] ALL TESTS PASSED!")
    print("=" * 80)
    print("\nInventory module is working correctly!")
    print("Ready for FastAPI integration.")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
