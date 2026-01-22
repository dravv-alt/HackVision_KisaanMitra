"""
Test Configuration Setup
Quick script to verify .env configuration and auto-detection
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_config():
    """Test configuration loading"""
    print("=" * 70)
    print("  Testing Voice Agent Configuration")
    print("=" * 70)
    
    try:
        from voice_agent.config import get_config
        
        print("\n🔄 Loading configuration...")
        config = get_config()
        
        print("\n✅ Configuration loaded successfully!")
        print(f"\n📋 Configuration Details:")
        print(f"   LLM Provider: {config.llm_provider}")
        print(f"   LLM Model: {config.llm_model or 'default'}")
        print(f"   Whisper Model: {config.whisper_model}")
        print(f"   MongoDB URI: {config.mongodb_uri or 'Not configured'}")
        print(f"   MongoDB DB: {config.mongodb_db_name}")
        print(f"   OpenWeather API: {'Configured' if config.openweather_api_key else 'Not configured'}")
        
        print("\n" + "=" * 70)
        print("✅ Configuration test passed!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Configuration test failed: {e}")
        print("\n💡 Make sure to:")
        print("   1. Set GEMINI_API_KEY or GROQ_API_KEY in Backend/.env")
        print("   2. Run from Backend/voice_agent directory")
        return False


def test_components():
    """Test component initialization"""
    print("\n" + "=" * 70)
    print("  Testing Component Initialization")
    print("=" * 70)
    
    try:
        # Test intent classifier
        print("\n🔄 Testing Intent Classifier...")
        from voice_agent.core import get_intent_classifier
        classifier = get_intent_classifier()
        print(f"✅ Intent Classifier initialized with {classifier.provider}")
        
        # Test speech-to-text
        print("\n🔄 Testing Speech-to-Text...")
        from voice_agent.input_processing import get_speech_to_text
        stt = get_speech_to_text()
        print(f"✅ Speech-to-Text initialized with model: {stt.model_name}")
        
        # Test translator
        print("\n🔄 Testing Translator...")
        from voice_agent.input_processing import get_translator
        translator = get_translator()
        print("✅ Translator initialized")
        
        print("\n" + "=" * 70)
        print("✅ All components initialized successfully!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Component initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🌾 Voice Agent Configuration Test\n")
    
    # Test configuration
    config_ok = test_config()
    
    if config_ok:
        # Test components
        components_ok = test_components()
        
        if components_ok:
            print("\n🎉 All tests passed! Voice Agent is ready to use.")
        else:
            print("\n⚠️  Component tests failed. Check error messages above.")
    else:
        print("\n⚠️  Configuration test failed. Fix .env file and try again.")
