"""
Voice Agent CLI Demo
Manual testing interface for the voice agent
"""

import sys
from pathlib import Path

# Add Backend directory to Python path for imports
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from voice_agent.core import get_voice_agent


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_separator():
    """Print separator"""
    print("-" * 70)


def display_response(response):
    """Display agent response in formatted way"""
    print_separator()
    print(f"\n🎯 Detected Intent: {response.intent.value}")
    print(f"   Confidence: {response.intent_confidence:.2f}")
    
    print(f"\n🔍 Retrieved Sources: {response.retrieved_sources}")
    
    print(f"\n💡 Reasoning:")
    print(f"   {response.reasoning}")
    
    if response.cards:
        print(f"\n📋 Generated Cards ({len(response.cards)}):")
        for i, card in enumerate(response.cards, 1):
            print(f"\n   {i}. {card.card_type.upper()}: {card.title}")
            print(f"      Summary: {card.summary}")
            if card.details:
                print(f"      Details: {list(card.details.keys())[:3]}")
    
    print(f"\n🗣️  Explanation (English):")
    print(f"   {response.explanation_english}")
    
    print(f"\n🗣️  Explanation (Hindi):")
    print(f"   {response.explanation_hindi}")
    
    print_separator()


def run_predefined_tests():
    """Run predefined test scenarios"""
    print_header("🌾 VOICE AGENT - PREDEFINED TESTS 🌾")
    
    agent = get_voice_agent()
    
    test_cases = [
        {
            "name": "Crop Planning Query",
            "hindi_input": "अब मुझे तय करना है कि कौन सी फसल लगाऊं",
            "description": "Farmer asking which crop to plant"
        },
        {
            "name": "Government Scheme Query",
            "hindi_input": "मुझे सरकारी योजना के बारे में बताओ",
            "description": "Farmer asking about government schemes"
        },
        {
            "name": "Weather Query",
            "hindi_input": "आज मौसम कैसा है",
            "description": "Farmer asking about weather"
        },
        {
            "name": "Market Price Query",
            "hindi_input": "गेहूं की कीमत क्या है",
            "description": "Farmer asking about wheat price"
        },
    ]
    
    for i, test in enumerate(test_cases, 1):
        print_header(f"TEST {i}: {test['name']}")
        print(f"\nDescription: {test['description']}")
        print(f"\n📝 Hindi Input:")
        print(f"   {test['hindi_input']}")
        
        # Process input
        response = agent.process_input(
            hindi_text=test['hindi_input'],
            farmer_id="F001"
        )
        
        # Display response
        display_response(response)
        
        input("\nPress Enter to continue to next test...")


def run_interactive_mode():
    """Run interactive mode"""
    print_header("🌾 VOICE AGENT - INTERACTIVE MODE 🌾")
    print("\nWelcome! Enter Hindi queries (or 'exit' to quit)")
    print("Example: अब मुझे तय करना है कि कौन सी फसल लगाऊं")
    
    agent = get_voice_agent()
    session_id = None
    
    while True:
        print_separator()
        hindi_input = input("\n🎤 Enter Hindi query: ").strip()
        
        if hindi_input.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not hindi_input:
            print("❌ Please enter a query")
            continue
        
        try:
            # Process input
            response = agent.process_input(
                hindi_text=hindi_input,
                farmer_id="F001",
                session_id=session_id
            )
            
            # Save session ID for continuity
            session_id = response.session_id
            
            # Display response
            display_response(response)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main CLI demo"""
    print_header("🌾 VOICE AGENT CLI DEMO 🌾")
    print("\nVoice-First Agentic Orchestration Layer")
    print("Processes Hindi input, detects intent, retrieves information,")
    print("reasons about recommendations, and generates UI-ready cards.")
    
    while True:
        print_header("MAIN MENU")
        print("\n1. Run Predefined Tests")
        print("2. Interactive Mode")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            run_predefined_tests()
        elif choice == "2":
            run_interactive_mode()
        elif choice == "3":
            print_header("Thank you for using Voice Agent!")
            print("\n👋 Goodbye!\n")
            break
        else:
            print("❌ Invalid choice. Please enter 1-3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
