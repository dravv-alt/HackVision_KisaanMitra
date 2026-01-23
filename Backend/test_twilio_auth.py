"""
Test Twilio Authentication System
Run this script to verify Twilio setup and test OTP flow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backend.auth.twilio_service import get_twilio_service
from Backend.auth.jwt_service import get_jwt_service
from dotenv import load_dotenv

load_dotenv()

def test_twilio_setup():
    """Test Twilio configuration"""
    print("=" * 60)
    print("🔐 TESTING TWILIO AUTHENTICATION SETUP")
    print("=" * 60)
    
    # Check environment variables
    print("\n📋 Checking Environment Variables...")
    
    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
    jwt_secret = os.getenv("JWT_SECRET_KEY")
    
    if twilio_sid and twilio_sid != "your_twilio_account_sid_here":
        print(f"✅ TWILIO_ACCOUNT_SID: {twilio_sid[:10]}...")
    else:
        print("❌ TWILIO_ACCOUNT_SID: Not configured")
    
    if twilio_token and twilio_token != "your_twilio_auth_token_here":
        print(f"✅ TWILIO_AUTH_TOKEN: {twilio_token[:10]}...")
    else:
        print("❌ TWILIO_AUTH_TOKEN: Not configured")
    
    if twilio_phone and twilio_phone != "your_twilio_phone_number_here":
        print(f"✅ TWILIO_PHONE_NUMBER: {twilio_phone}")
    else:
        print("❌ TWILIO_PHONE_NUMBER: Not configured")
    
    if jwt_secret and jwt_secret != "your_super_secret_jwt_key_change_this_in_production":
        print(f"✅ JWT_SECRET_KEY: Configured")
    else:
        print("⚠️ JWT_SECRET_KEY: Using default (change in production)")
    
    # Test Twilio Service
    print("\n🔧 Testing Twilio Service...")
    twilio_service = get_twilio_service()
    
    if twilio_service.client:
        print("✅ Twilio client initialized successfully")
        print("✅ Ready to send SMS")
    else:
        print("⚠️ Twilio client not initialized - Running in MOCK MODE")
        print("   OTPs will be printed to console instead of SMS")
    
    # Test JWT Service
    print("\n🔑 Testing JWT Service...")
    jwt_service = get_jwt_service()
    
    # Create test token
    test_data = {
        "user_id": "TEST123",
        "farmer_id": "FTEST123",
        "phone_number": "+919876543210"
    }
    
    token = jwt_service.create_access_token(test_data)
    print(f"✅ JWT token created: {token[:50]}...")
    
    # Verify token
    verified = jwt_service.verify_token(token)
    if verified and verified.get("user_id") == "TEST123":
        print("✅ JWT token verified successfully")
    else:
        print("❌ JWT token verification failed")
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    if twilio_service.client:
        print("✅ Twilio is CONFIGURED - Real SMS will be sent")
        print("📱 You can test with your phone number")
    else:
        print("⚠️ Twilio is in MOCK MODE - OTPs will be shown in console")
        print("🧪 Perfect for testing without SMS costs")
    
    print("\n🚀 Next Steps:")
    print("1. Start backend: python -m uvicorn Backend.api.main:app --reload --port 8000")
    print("2. Start frontend: cd Frontend/kisanmitra-app && npm run dev")
    print("3. Visit: http://localhost:5173/login")
    print("4. Enter your phone number and test!")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_twilio_setup()
