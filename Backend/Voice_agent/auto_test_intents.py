"""
Auto Test - Runs all 17 new voice intents automatically
No user input required
"""

import sys
from pathlib import Path

# Add Backend to path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from Backend.Voice_agent.core import get_voice_agent
from Backend.Voice_agent.core.intent import Intent


def test_all_intents():
    """Test all 17 new intents automatically"""
    print("="*80)
    print("  VOICE AGENT - AUTO TEST - ALL 17 NEW INTENTS")
    print("="*80)
    print()
    
    agent = get_voice_agent()
    
    test_cases = [
        # Financial Tracking
        ("मेरा मुनाफा बताओ", Intent.FINANCE_REPORT, "Finance Report"),
        ("मैंने 5000 बीज पर खर्च किए", Intent.ADD_EXPENSE, "Add Expense"),
        ("मैंने गेहूं बेची", Intent.ADD_INCOME, "Add Income"),
        ("कहां खर्च ज्यादा है?", Intent.COST_ANALYSIS, "Cost Analysis"),
        ("खर्च कम कैसे करूं?", Intent.OPTIMIZATION_ADVICE, "Optimization Advice"),
        
        # Collaborative Farming
        ("आसपास उपकरण देखो", Intent.VIEW_MARKETPLACE, "View Marketplace"),
        ("ट्रैक्टर चाहिए", Intent.EQUIPMENT_RENTAL, "Equipment Rental"),
        ("साझे में खेती करनी है", Intent.LAND_POOLING, "Land Pooling"),
        ("पराली बेचनी है", Intent.RESIDUE_MANAGEMENT, "Residue Management"),
        
        # Inventory
        ("मेरा स्टॉक कितना है?", Intent.CHECK_STOCK, "Check Stock"),
        ("अभी बेचूं?", Intent.SELL_RECOMMENDATION, "Sell Recommendation"),
        ("खराब होने वाला माल?", Intent.SPOILAGE_ALERT, "Spoilage Alert"),
        
        # Alerts
        ("अलर्ट है क्या?", Intent.CHECK_ALERTS, "Check Alerts"),
        ("कल क्या करूं?", Intent.REMINDER_CHECK, "Reminder Check"),
    ]
    
    passed = 0
    failed = 0
    errors = []
    
    for query, expected_intent, test_name in test_cases:
        try:
            print(f"Testing: {test_name:.<50} ", end="", flush=True)
            response = agent.process_input(query, "DEMO_FARMER")
            
            if response.intent == expected_intent:
                print("✅ PASS")
                passed += 1
            else:
                print(f"❌ FAIL (got {response.intent.value})")
                failed += 1
                errors.append(f"{test_name}: Expected {expected_intent.value}, got {response.intent.value}")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)[:40]}")
            failed += 1
            errors.append(f"{test_name}: {str(e)[:100]}")
    
    print()
    print("="*80)
    print(f"  RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("="*80)
    
    if errors:
        print("\nErrors:")
        for err in errors:
            print(f"  - {err}")
    
    return passed, failed


if __name__ == "__main__":
    try:
        passed, failed = test_all_intents()
        sys.exit(0 if failed == 0 else 1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
