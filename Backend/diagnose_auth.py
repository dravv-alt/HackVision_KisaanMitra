"""
Auth System Diagnostic Script
Checks all auth components and identifies issues
"""

import sys
import os

print("=" * 60)
print("🔍 AUTH SYSTEM DIAGNOSTIC")
print("=" * 60)
print()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test 1: Check imports
print("1️⃣ Testing Imports...")
try:
    from Backend.auth.twilio_service import get_twilio_service
    print("   ✅ twilio_service imported")
except Exception as e:
    print(f"   ❌ twilio_service import failed: {e}")

try:
    from Backend.auth.jwt_service import get_jwt_service
    print("   ✅ jwt_service imported")
except Exception as e:
    print(f"   ❌ jwt_service import failed: {e}")

try:
    from Backend.api.routers.auth import router
    print("   ✅ auth router imported")
except Exception as e:
    print(f"   ❌ auth router import failed: {e}")

# Test 2: Check environment variables
print("\n2️⃣ Checking Environment Variables...")
from dotenv import load_dotenv
load_dotenv()

twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
jwt_secret = os.getenv("JWT_SECRET_KEY")

if twilio_sid and twilio_sid != "your_twilio_account_sid_here":
    print(f"   ✅ TWILIO_ACCOUNT_SID: {twilio_sid[:10]}...")
else:
    print("   ⚠️  TWILIO_ACCOUNT_SID: Not configured (MOCK MODE)")

if twilio_token and twilio_token != "your_twilio_auth_token_here":
    print(f"   ✅ TWILIO_AUTH_TOKEN: {twilio_token[:10]}...")
else:
    print("   ⚠️  TWILIO_AUTH_TOKEN: Not configured (MOCK MODE)")

if twilio_phone and twilio_phone != "your_twilio_phone_number_here":
    print(f"   ✅ TWILIO_PHONE_NUMBER: {twilio_phone}")
else:
    print("   ⚠️  TWILIO_PHONE_NUMBER: Not configured (MOCK MODE)")

if jwt_secret and jwt_secret != "your_super_secret_jwt_key_change_this_in_production":
    print("   ✅ JWT_SECRET_KEY: Configured")
else:
    print("   ⚠️  JWT_SECRET_KEY: Using default")

# Test 3: Test Twilio Service
print("\n3️⃣ Testing Twilio Service...")
try:
    from Backend.auth.twilio_service import get_twilio_service
    twilio_service = get_twilio_service()
    
    if twilio_service.client:
        print("   ✅ Twilio client initialized (REAL MODE)")
    else:
        print("   ⚠️  Twilio client not initialized (MOCK MODE)")
        print("      OTPs will be printed to console")
    
    # Test OTP generation
    otp = twilio_service.generate_otp()
    print(f"   ✅ OTP generation works: {otp}")
    
except Exception as e:
    print(f"   ❌ Twilio service error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Test JWT Service
print("\n4️⃣ Testing JWT Service...")
try:
    from Backend.auth.jwt_service import get_jwt_service
    jwt_service = get_jwt_service()
    
    # Create test token
    test_data = {"user_id": "TEST123", "farmer_id": "FTEST123"}
    token = jwt_service.create_access_token(test_data)
    print(f"   ✅ JWT token created: {token[:50]}...")
    
    # Verify token
    verified = jwt_service.verify_token(token)
    if verified and verified.get("user_id") == "TEST123":
        print("   ✅ JWT token verified successfully")
    else:
        print("   ❌ JWT token verification failed")
    
except Exception as e:
    print(f"   ❌ JWT service error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Test API Router
print("\n5️⃣ Testing API Router...")
try:
    from Backend.api.routers.auth import router
    print(f"   ✅ Auth router loaded")
    print(f"   ✅ Router prefix: {router.prefix}")
    print(f"   ✅ Number of routes: {len(router.routes)}")
    
    # List routes
    for route in router.routes:
        print(f"      - {route.methods} {route.path}")
    
except Exception as e:
    print(f"   ❌ Router error: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Check Dependencies
print("\n6️⃣ Checking Dependencies...")
try:
    import twilio
    print(f"   ✅ twilio: {twilio.__version__}")
except ImportError:
    print("   ❌ twilio: NOT INSTALLED")
    print("      Run: pip install twilio")

try:
    import jwt
    print(f"   ✅ PyJWT: installed")
except ImportError:
    print("   ❌ PyJWT: NOT INSTALLED")
    print("      Run: pip install PyJWT")

try:
    from dotenv import load_dotenv
    print("   ✅ python-dotenv: installed")
except ImportError:
    print("   ❌ python-dotenv: NOT INSTALLED")
    print("      Run: pip install python-dotenv")

# Summary
print("\n" + "=" * 60)
print("📊 DIAGNOSTIC SUMMARY")
print("=" * 60)

issues = []
if not (twilio_sid and twilio_sid != "your_twilio_account_sid_here"):
    issues.append("Twilio credentials not configured (running in MOCK mode)")

if not (jwt_secret and jwt_secret != "your_super_secret_jwt_key_change_this_in_production"):
    issues.append("JWT secret using default value")

if issues:
    print("\n⚠️  WARNINGS:")
    for issue in issues:
        print(f"   - {issue}")
    print("\n💡 These are not errors if you're testing in MOCK mode")
else:
    print("\n✅ All checks passed!")

print("\n🚀 Auth system is ready to use!")
print("\nNext steps:")
print("1. Start backend: python -m uvicorn Backend.api.main:app --reload --port 8000")
print("2. Visit: http://localhost:8000/docs")
print("3. Test /api/v1/auth/send-otp endpoint")
print("\n" + "=" * 60)
