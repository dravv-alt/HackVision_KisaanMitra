"""
Comprehensive System Feature Test - Simple Version
Tests all API endpoints and modules
"""

import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, files=None, description=""):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Endpoint: {method} {endpoint}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(url, params=data, timeout=10)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files, timeout=10)
            else:
                response = requests.post(url, json=data, timeout=10)
        else:
            print(f"[X] Unsupported method: {method}")
            return False
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"[OK] SUCCESS")
            try:
                result = response.json()
                print(f"Response preview: {json.dumps(result, indent=2)[:300]}...")
            except:
                print(f"Response text: {response.text[:200]}...")
            return True
        else:
            print(f"[FAIL] FAILED - Status {response.status_code}")
            print(f"Error: {response.text[:500]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"[FAIL] CONNECTION FAILED - Server not running?")
        return False
    except Exception as e:
        print(f"[FAIL] ERROR: {e}")
        return False

def main():
    print("="*60)
    print("KISAAN MITRA BACKEND - COMPREHENSIVE FEATURE TEST")
    print("="*60)
    
    results = {}
    
    # 1. Health Check
    results['health'] = test_endpoint(
        "GET", "/health",
        description="System Health Check"
    )
    
    # 2. Voice Agent
    results['voice_process'] = test_endpoint(
        "POST", "/api/v1/voice/process",
        data={
            "hindi_text": "meri fasal mein bimari hai",
            "farmer_id": "F001"
        },
        description="Voice Agent - Process Hindi Input"
    )
    
    # 3. Pre-Seeding Plan
    results['pre_seeding'] = test_endpoint(
        "POST", "/api/v1/planning/pre-seeding",
        data={
            "location": {"state": "Maharashtra", "district": "Nasik"},
            "soil_type": "loamy",
            "season": "kharif",
            "farm_size_acres": 5.0,
            "irrigation_available": True,
            "farmer_category": "small"
        },
        description="Planning Stage - Pre-Seeding Recommendations"
    )
    
    # 4. Market Prices
    results['market_prices'] = test_endpoint(
        "GET", "/api/v1/farming/market-price",
        data={"crop": "Onion", "state": "Maharashtra"},
        description="Farming Stage - Market Prices"
    )
    
    # 5. Post-Harvest Plan
    results['post_harvest'] = test_endpoint(
        "POST", "/api/v1/post-harvest/plan",
        data={
            "crop_name": "Tomato",
            "quantity_kg": 1000,
            "farmer_location": [19.9975, 73.7898],
            "harvest_date": "2024-01-15",
            "today_date": str(date.today())
        },
        description="Post-Harvest - Harvest Plan"
    )
    
    # 6. Government Schemes
    results['schemes_list'] = test_endpoint(
        "GET", "/api/v1/schemes",
        description="Government Schemes - List All"
    )
    
    results['schemes_filter'] = test_endpoint(
        "POST", "/api/v1/schemes/filter",
        data={
            "state": "Maharashtra",
            "category": "credit"
        },
        description="Government Schemes - Filter by State/Category"
    )
    
    # 7. Financial Tracking
    results['finance_summary'] = test_endpoint(
        "GET", "/api/v1/finance/summary",
        data={"farmer_id": "F001"},
        description="Financial - Summary"
    )
    
    results['finance_add_expense'] = test_endpoint(
        "POST", "/api/v1/finance/expense",
        data={
            "farmer_id": "F001",
            "amount": 5000,
            "category": "seeds",
            "description": "Tomato seeds purchase",
            "date": str(date.today())
        },
        description="Financial - Add Expense"
    )
    
    # 8. Collaborative Farming
    results['equipment_list'] = test_endpoint(
        "GET", "/api/v1/collaborative/equipment",
        description="Collaborative - List Equipment"
    )
    
    results['land_pooling'] = test_endpoint(
        "GET", "/api/v1/collaborative/land-pooling",
        description="Collaborative - Land Pooling Opportunities"
    )
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    print(f"\nTotal Tests: {total}")
    print(f"[OK] Passed: {passed}")
    print(f"[X] Failed: {failed}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    print("\nDetailed Results:")
    for test_name, result in results.items():
        status = "[OK]" if result else "[X]"
        print(f"  {status} {test_name}")
    
    print("\n" + "="*60)
    return results

if __name__ == "__main__":
    main()
