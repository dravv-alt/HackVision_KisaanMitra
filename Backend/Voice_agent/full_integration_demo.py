"""
Voice Agent Full Integration Demo
Tests all 17 new intents across all backend modules

Run this to demonstrate voice control of:
- Financial Tracking
- Collaborative Farming
- Inventory Management  
- Alerts & Notifications
"""

import sys
from pathlib import Path

# Add Backend to path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from voice_agent.core import get_voice_agent
from voice_agent.core.intent import Intent


def print_header(title, char="="):
    """Print formatted header"""
    print(f"\n{char*80}")
    print(f"  {title}")
    print(f"{char*80}\n")


def print_result(response):
    """Print voice agent response"""
    print(f"🎯 Intent: {response.intent.value}")
    print(f"   Confidence: {response.intent_confidence:.2f}")
    print(f"\n💭 Reasoning:")
    print(f"   {response.reasoning}")
    if response.explanation_hindi:
        print(f"\n🗣️ Hindi: {response.explanation_hindi[:150]}...")
    if response.explanation_english:
        print(f"\n🗣️ English: {response.explanation_english[:150]}...")
    print()


def test_financial_tracking():
    """Test Financial Tracking intents"""
    print_header("FINANCIAL TRACKING MODULE - 5 INTENTS", "=")
    
    agent = get_voice_agent()
    
    test_cases = [
        {
            "name": "Finance Report",
            "query_hi": "मेरा मुनाफा बताओ",
            "query_en": "Show me my profit",
            "expected": Intent.FINANCE_REPORT
        },
        {
            "name": "Add Expense",
            "query_hi": "मैंने 5000 रुपये बीज पर खर्च किए",
            "query_en": "I spent 5000 rupees on seeds",
            "expected": Intent.ADD_EXPENSE
        },
        {
            "name": "Add Income",
            "query_hi": "मैंने गेहूं 50000 में बेची",
            "query_en": "I sold wheat for 50000",
            "expected": Intent.ADD_INCOME
        },
        {
            "name": "Cost Analysis",
            "query_hi": "कहां ज्यादा खर्च हो रहा है?",
            "query_en": "Where am I spending more?",
            "expected": Intent.COST_ANALYSIS
        },
        {
            "name": "Optimization Advice",
            "query_hi": "खर्च कैसे कम करूं?",
            "query_en": "How can I reduce costs?",
            "expected": Intent.OPTIMIZATION_ADVICE
        }
    ]
    
    for test in test_cases:
        print_header(f"TEST: {test['name']}", "-")
        print(f"Hindi Query: {test['query_hi']}")
        print(f"English Query: {test['query_en']}")
        print(f"Expected Intent: {test['expected'].value}\n")
        
        # Test with Hindi
        response = agent.process_input(test['query_hi'], "DEMO_FARMER")
        print_result(response)
        
        input("Press Enter for next test...")


def test_collaborative_farming():
    """Test Collaborative Farming intents"""
    print_header("COLLABORATIVE FARMING MODULE - 4 INTENTS", "=")
    
    agent = get_voice_agent()
    
    test_cases = [
        {
            "name": "View Marketplace",
            "query_hi": "आसपास कौनसे उपकरण मिलेंगे?",
            "query_en": "What equipment is available nearby?",
            "expected": Intent.VIEW_MARKETPLACE
        },
        {
            "name": "Equipment Rental",
            "query_hi": "ट्रैक्टर किराए पर चाहिए",
            "query_en": "I need to rent a tractor",
            "expected": Intent.EQUIPMENT_RENTAL
        },
        {
            "name": "Land Pooling",
            "query_hi": "साझे में खेती करनी है",
            "query_en": "I want to do cooperative farming",
            "expected": Intent.LAND_POOLING
        },
        {
            "name": "Residue Management",
            "query_hi": "पराली कहां बेचूं?",
            "query_en": "Where can I sell crop residue?",
            "expected": Intent.RESIDUE_MANAGEMENT
        }
    ]
    
    for test in test_cases:
        print_header(f"TEST: {test['name']}", "-")
        print(f"Hindi Query: {test['query_hi']}")
        print(f"English Query: {test['query_en']}")
        print(f"Expected Intent: {test['expected'].value}\n")
        
        response = agent.process_input(test['query_hi'], "DEMO_FARMER")
        print_result(response)
        
        input("Press Enter for next test...")


def test_inventory():
    """Test Inventory intents"""
    print_header("INVENTORY MANAGEMENT MODULE - 3 INTENTS", "=")
    
    agent = get_voice_agent()
    
    test_cases = [
        {
            "name": "Check Stock",
            "query_hi": "मेरा स्टॉक कितना है?",
            "query_en": "How much stock do I have?",
            "expected": Intent.CHECK_STOCK
        },
        {
            "name": "Sell Recommendation",
            "query_hi": "अभी बेचूं या नहीं?",
            "query_en": "Should I sell now?",
            "expected": Intent.SELL_RECOMMENDATION
        },
        {
            "name": "Spoilage Alert",
            "query_hi": "खराब होने वाला माल बताओ",
            "query_en": "Show me items that may spoil",
            "expected": Intent.SPOILAGE_ALERT
        }
    ]
    
    for test in test_cases:
        print_header(f"TEST: {test['name']}", "-")
        print(f"Hindi Query: {test['query_hi']}")
        print(f"English Query: {test['query_en']}")
        print(f"Expected Intent: {test['expected'].value}\n")
        
        response = agent.process_input(test['query_hi'], "DEMO_FARMER")
        print_result(response)
        
        input("Press Enter for next test...")


def test_alerts():
    """Test Alerts intents"""
    print_header("ALERTS & NOTIFICATIONS MODULE - 2 INTENTS", "=")
    
    agent = get_voice_agent()
    
    test_cases = [
        {
            "name": "Check Alerts",
            "query_hi": "मेरे लिए कोई अलर्ट है?",
            "query_en": "Do I have any alerts?",
            "expected": Intent.CHECK_ALERTS
        },
        {
            "name": "Reminder Check",
            "query_hi": "कल क्या करना है?",
            "query_en": "What should I do tomorrow?",
            "expected": Intent.REMINDER_CHECK
        }
    ]
    
    for test in test_cases:
        print_header(f"TEST: {test['name']}", "-")
        print(f"Hindi Query: {test['query_hi']}")
        print(f"English Query: {test['query_en']}")
        print(f"Expected Intent: {test['expected'].value}\n")
        
        response = agent.process_input(test['query_hi'], "DEMO_FARMER")
        print_result(response)
        
        input("Press Enter for next test...")


def test_all_quick():
    """Quick test of all 17 new intents"""
    print_header("QUICK TEST - ALL 17 NEW INTENTS", "=")
    
    agent = get_voice_agent()
    
    all_tests = [
        ("मेरा मुनाफा बताओ", Intent.FINANCE_REPORT),
        ("मैंने 5000 बीज पर खर्च किए", Intent.ADD_EXPENSE),
        ("मैंने गेहूं बेची", Intent.ADD_INCOME),
        ("कहां खर्च ज्यादा है?", Intent.COST_ANALYSIS),
        ("खर्च कम कैसे करूं?", Intent.OPTIMIZATION_ADVICE),
        ("आसपास उपकरण देखो", Intent.VIEW_MARKETPLACE),
        ("ट्रैक्टर चाहिए", Intent.EQUIPMENT_RENTAL),
        ("साझे में खेती करनी है", Intent.LAND_POOLING),
        ("पराली बेचनी है", Intent.RESIDUE_MANAGEMENT),
        ("मेरा स्टॉक कितना है?", Intent.CHECK_STOCK),
        ("अभी बेचूं?", Intent.SELL_RECOMMENDATION),
        ("खराब होने वाला माल?", Intent.SPOILAGE_ALERT),
        ("अलर्ट है क्या?", Intent.CHECK_ALERTS),
        ("कल क्या करूं?", Intent.REMINDER_CHECK),
    ]
    
    passed = 0
    failed = 0
    
    for query, expected_intent in all_tests:
        try:
            response = agent.process_input(query, "DEMO_FARMER")
            status = "✅" if response.intent == expected_intent else "❌"
            print(f"{status} {query[:30]:.<35} -> {response.intent.value}")
            
            if response.intent == expected_intent:
                passed += 1
            else:
                failed += 1
                
        except Exception as e:
            print(f"❌ {query[:30]:.<35} -> ERROR: {str(e)[:40]}")
            failed += 1
    
    print(f"\n{'-'*80}")
    print(f"Results: {passed} passed, {failed} failed out of {len(all_tests)} tests")
    print(f"{'-'*80}\n")


def run_interactive():
    """Interactive mode"""
    print_header("VOICE AGENT - INTERACTIVE MODE")
    print("Test any query in Hindi or English")
    print("Type 'exit' to quit\n")
    
    agent = get_voice_agent()
    
    while True:
        query = input("🎤 Enter query: ").strip()
        
        if query.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Goodbye!\n")
            break
        
        if not query:
            continue
        
        try:
            response = agent.process_input(query, "DEMO_FARMER")
            print_result(response)
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            import traceback
            traceback.print_exc()


def main():
    """Main menu"""
    print_header("🌾 VOICE AGENT - FULL BACKEND INTEGRATION DEMO 🌾")
    
    print("This demo tests voice control of ALL backend modules:")
    print("  1. Financial Tracking (5 intents)")
    print("  2. Collaborative Farming (4 intents)")
    print("  3. Inventory Management (3 intents)")
    print("  4. Alerts & Notifications (2 intents)")
    print("  ────────────────────────────────────")
    print("  Total: 17 NEW voice-controlled features!\n")
    
    while True:
        print_header("MAIN MENU", "-")
        print("1. Test Financial Tracking (5 intents)")
        print("2. Test Collaborative Farming (4 intents)")
        print("3. Test Inventory Management (3 intents)")
        print("4. Test Alerts & Notifications (2 intents)")
        print("5. Quick Test All 17 Intents")
        print("6. Interactive Mode")
        print("7. Exit")
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == "1":
            test_financial_tracking()
        elif choice == "2":
            test_collaborative_farming()
        elif choice == "3":
            test_inventory()
        elif choice == "4":
            test_alerts()
        elif choice == "5":
            test_all_quick()
        elif choice == "6":
            run_interactive()
        elif choice == "7":
            print_header("Thank you for testing!")
            print("Voice Agent can now drive ALL 7 backend modules! 🚀\n")
            break
        else:
            print("❌ Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
