"""
CLI Demo - Manual Testing Runner for Collaborative Farming
"""

import sys
from pathlib import Path

# Add Backend directory to Python path for imports
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from datetime import datetime, timedelta
from Backend.Collaborative_Farming.service import CollaborativeFarmingService
from Backend.Collaborative_Farming.constants import EquipmentType, PoolRequestType, RentalStatus


def print_header(text: str):
    print("\n" + "="*80)
    print(f" {text}")
    print("="*80)


def run_demo():
    print_header("🌾 KISSAN MITRA - COLLABORATIVE FARMING DEMO 🌾")

    service = CollaborativeFarmingService()
    farmer_id = "FARMER001"
    
    # 1. Show Marketplace View (Nearby Equipment + Land Pools)
    print(f"\n[DASHBOARD] Fetching marketplace view for farmer: {farmer_id}")
    output = service.run_marketplace_view(farmer_id)
    
    print(f"\n🚩 UI Header: {output.header}")
    print(f"🔊 Speech Output: {output.speechText}")
    print(f"⚠️ Urgency Level: {output.urgencyLevel.upper()}")
    
    print(f"\n🚜 EQUIPMENT NEARBY ({len(output.equipmentCards)} items):")
    for eq in output.equipmentCards:
        verified = "✅ verified" if eq.isVerified else ""
        print(f"   - {eq.equipmentType.upper()}: {eq.modelName} | ₹{eq.pricePerDay}/day | {eq.hpRequired} | {eq.condition} | {verified}")

    print(f"\n🤝 LAND POOLING REQUESTS ({len(output.landPoolCards)} items):")
    for pool in output.landPoolCards:
        stage = pool.currentStage.upper() if pool.currentStage else "OPEN"
        bid_info = f"| Bid: ₹{pool.highestBid}" if pool.highestBid else ""
        print(f"   - {pool.requestType.upper()} | {pool.landSizeAcres} Acres | Crop: {pool.cropPreference} | Stage: {stage} {bid_info} | Benefit: {pool.keyBenefit}")

    # 2. Simulate Rental Request
    listing_id = output.equipmentCards[0].listingId
    print(f"\n[ACTION] Requesting to rent {output.equipmentCards[0].modelName}...")
    
    start_date = datetime.now() + timedelta(days=10)
    end_date = start_date + timedelta(days=2)
    
    rental = service.request_equipment_rental(farmer_id, listing_id, start_date, end_date)
    print(f"   ✅ Rental Request Created! ID: {rental.rentalId[:8]}... | Status: {rental.status}")

    # 3. Simulate Rental Approval (by Owner)
    owner_id = rental.ownerFarmerId
    print(f"\n[ACTION] Owner ({owner_id}) approving the rental...")
    approved_rental = service.approve_rental(owner_id, rental.rentalId)
    print(f"   ✅ Rental Approved! Status: {approved_rental.status}")

    # 4. Show Ongoing Rentals & Reminders
    print(f"\n[DASHBOARD] Refreshing marketplace view...")
    output2 = service.run_marketplace_view(farmer_id)
    
    print(f"\n📂 ACTIVE RENTALS ({len(output2.rentalCards)} items):")
    for r in output2.rentalCards:
        print(f"   - Rental ID: {r.rentalId[:8]}... | Status: {r.status} | End Date: {r.endDate.strftime('%Y-%m-%d')}")

    print(f"\n⏰ REMINDERS GENERATED ({len(output2.remindersSuggested)} items):")
    for r in output2.remindersSuggested:
        print(f"   - {r.title}: {r.message}")

    # 5. Land Pooling Interaction
    print(f"\n[ACTION] Creating a new land pooling request...")
    new_pool = service.create_land_pool_request(farmer_id, PoolRequestType.SEEK_PARTNER, 5.0, "Cotton")
    print(f"   ✅ Land Pool Request Created! ID: {new_pool.requestId[:8]}...")
    
    # 6. Future Scope: Residue
    print(f"\n[FUTURE SCOPE] Bulk Residue Offers:")
    # Using internal engine logic helper
    residue_summaries = service.residue_engine.group_residue_for_bulk_offer(output2.residueCards)
    for g in residue_summaries:
        print(f"   - GROUP: {g['cropType'].upper()} | Total Qty: {g['totalQty']}Kg | Members: {g['memberCount']}")

    print_header("✅ COLLABORATIVE FARMING DEMO COMPLETED!")


if __name__ == "__main__":
    run_demo()
