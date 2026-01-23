# Twilio Authentication Integration Guide

## Overview
Complete Twilio-based OTP authentication system for KisanMitra. Farmers can log in using their phone numbers with SMS OTP verification.

---

## Features

✅ **Phone Number Authentication** - No email required
✅ **SMS OTP Verification** - 6-digit OTP via Twilio
✅ **JWT Token Management** - Secure session handling
✅ **Auto User Creation** - New users created automatically
✅ **Onboarding Detection** - Redirects to onboarding if needed
✅ **Mock Mode** - Works without Twilio for development
✅ **Hindi Interface** - Complete Hindi Devanagari UI
✅ **Token Refresh** - Long-lived sessions (30 days)

---

## Setup Instructions

### Step 1: Install Dependencies

```bash
cd Backend
pip install twilio PyJWT python-dotenv
```

Or use the requirements file:
```bash
pip install -r auth/requirements.txt
```

### Step 2: Get Twilio Credentials

1. **Sign up for Twilio**: https://www.twilio.com/try-twilio
2. **Get a phone number**: https://console.twilio.com/us1/develop/phone-numbers/manage/incoming
3. **Find your credentials**: https://console.twilio.com

You'll need:
- **Account SID** (starts with AC...)
- **Auth Token** (secret key)
- **Phone Number** (e.g., +1234567890)

### Step 3: Configure Environment Variables

Edit `Backend/.env`:

```env
# Twilio Credentials
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890

# JWT Configuration
JWT_SECRET_KEY=your_super_secret_key_change_this_in_production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=720  # 30 days
```

**Important**: 
- Replace with your actual Twilio credentials
- Change `JWT_SECRET_KEY` to a random secret string
- Keep `.env` file secure (never commit to git)

### Step 4: Start Backend

```bash
cd Backend
python -m uvicorn api.main:app --reload --port 8000
```

### Step 5: Test API

Visit: `http://localhost:8000/docs`

You'll see new endpoints:
- `POST /api/v1/auth/send-otp`
- `POST /api/v1/auth/verify-otp`
- `POST /api/v1/auth/resend-otp`
- `POST /api/v1/auth/refresh-token`
- `GET /api/v1/auth/verify-token`

---

## API Documentation

### 1. Send OTP

**Endpoint**: `POST /api/v1/auth/send-otp`

**Request**:
```json
{
  "phone_number": "+919876543210"
}
```

**Response**:
```json
{
  "success": true,
  "message": "OTP sent successfully",
  "expires_in_minutes": 10,
  "otp": "123456"  // Only in mock mode
}
```

### 2. Verify OTP

**Endpoint**: `POST /api/v1/auth/verify-otp`

**Request**:
```json
{
  "phone_number": "+919876543210",
  "otp": "123456",
  "name": "राम कुमार"  // Optional, for new users
}
```

**Response**:
```json
{
  "success": true,
  "message": "Authentication successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "U12345678",
  "farmer_id": "F12345678",
  "is_new_user": false,
  "needs_onboarding": false
}
```

### 3. Resend OTP

**Endpoint**: `POST /api/v1/auth/resend-otp`

**Request**:
```json
{
  "phone_number": "+919876543210"
}
```

### 4. Refresh Token

**Endpoint**: `POST /api/v1/auth/refresh-token`

**Headers**:
```
Authorization: Bearer <your_token>
```

**Response**:
```json
{
  "success": true,
  "access_token": "new_token_here",
  "message": "Token refreshed successfully"
}
```

### 5. Verify Token

**Endpoint**: `GET /api/v1/auth/verify-token`

**Headers**:
```
Authorization: Bearer <your_token>
```

**Response**:
```json
{
  "success": true,
  "message": "Token is valid",
  "user_data": {
    "user_id": "U12345678",
    "farmer_id": "F12345678",
    "phone_number": "+919876543210"
  }
}
```

---

## Frontend Integration

### Login Flow

1. **User enters phone number**
2. **Click "OTP भेजें"**
3. **Receive OTP via SMS**
4. **Enter 6-digit OTP**
5. **Click "सत्यापित करें और लॉगिन करें"**
6. **Redirect to**:
   - `/onboarding/language` if new user
   - `/dashboard` if existing user

### Code Example

```javascript
// Send OTP
const response = await fetch('http://localhost:8000/api/v1/auth/send-otp', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ phone_number: '+919876543210' })
});

// Verify OTP
const response = await fetch('http://localhost:8000/api/v1/auth/verify-otp', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    phone_number: '+919876543210',
    otp: '123456'
  })
});

const data = await response.json();

// Store token
localStorage.setItem('kisanmitra_auth_token', data.access_token);
localStorage.setItem('kisanmitra_user_id', data.user_id);
localStorage.setItem('kisanmitra_farmer_id', data.farmer_id);
```

---

## Mock Mode (Development)

If Twilio credentials are not configured, the system runs in **mock mode**:

- ✅ OTP is printed to console
- ✅ OTP is shown in alert (frontend)
- ✅ No SMS sent
- ✅ Perfect for development/testing

**Example Console Output**:
```
🔐 MOCK OTP for +919876543210: 123456
```

---

## Security Features

### OTP Security
- ✅ 6-digit random OTP
- ✅ 10-minute expiration
- ✅ Maximum 3 verification attempts
- ✅ One-time use (deleted after verification)
- ✅ Stored in-memory (use Redis in production)

### JWT Security
- ✅ HS256 algorithm
- ✅ 30-day expiration (configurable)
- ✅ Includes user_id, farmer_id, phone_number
- ✅ Refresh token support
- ✅ Token verification endpoint

### Best Practices
- 🔒 Store JWT in localStorage (or httpOnly cookies)
- 🔒 Include token in Authorization header
- 🔒 Validate token on protected routes
- 🔒 Refresh token before expiry
- 🔒 Never expose JWT secret key

---

## Testing

### Test with Mock Mode

1. **Start backend** (without Twilio credentials)
2. **Go to login page**: `http://localhost:5173/login`
3. **Enter phone**: `9876543210`
4. **Click "OTP भेजें"**
5. **Check console/alert** for OTP
6. **Enter OTP** and verify
7. ✅ Should login successfully

### Test with Real Twilio

1. **Configure Twilio credentials** in `.env`
2. **Restart backend**
3. **Enter your real phone number**
4. **Receive SMS** with OTP
5. **Enter OTP** and verify
6. ✅ Should login successfully

---

## Phone Number Format

The system accepts phone numbers in multiple formats:

**Input Formats**:
- `9876543210` → Converts to `+919876543210`
- `919876543210` → Converts to `+919876543210`
- `+919876543210` → Already correct

**E.164 Format** (International):
- Country code: `+91` (India)
- Number: `9876543210`
- Full: `+919876543210`

---

## Database Schema

### Farmers Collection

```javascript
{
  "user_id": "U12345678",
  "farmer_id": "F12345678",
  "phone": "+919876543210",
  "name": "राम कुमार",
  "language": "hi",
  "onboarding_completed": false,
  "created_at": ISODate("2024-01-23T..."),
  "updated_at": ISODate("2024-01-23T...")
}
```

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "No OTP found" | OTP expired or never sent | Request new OTP |
| "OTP has expired" | More than 10 minutes passed | Request new OTP |
| "Maximum attempts exceeded" | 3 wrong OTP entries | Request new OTP |
| "Incorrect OTP" | Wrong OTP entered | Try again (2 attempts left) |
| "Invalid token" | Token expired or invalid | Login again |

---

## Production Deployment

### Environment Variables

```env
# Production Twilio
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_production_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Production JWT
JWT_SECRET_KEY=use_a_very_long_random_string_here_min_32_chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=720
```

### Recommendations

1. **Use Redis** for OTP storage (instead of in-memory)
2. **Enable HTTPS** for all API calls
3. **Rate limiting** on OTP endpoints
4. **Monitor Twilio usage** and costs
5. **Implement CAPTCHA** to prevent abuse
6. **Use httpOnly cookies** for JWT (more secure)
7. **Set up logging** for auth events
8. **Add 2FA** for admin accounts

---

## Cost Estimation

### Twilio Pricing (India)

- **SMS to India**: ~₹0.50 per message
- **Phone Number**: ~₹100/month
- **1000 users/month**: ~₹500 for OTPs

**Free Tier**:
- $15 credit on signup
- ~30 SMS for testing

---

## Troubleshooting

### Issue: OTP not received

**Solutions**:
1. Check Twilio phone number is verified
2. Check recipient number is in correct format
3. Check Twilio account balance
4. Check SMS logs in Twilio console
5. Try mock mode for testing

### Issue: "Invalid token"

**Solutions**:
1. Check JWT_SECRET_KEY matches
2. Check token not expired
3. Check token format in Authorization header
4. Try logging in again

### Issue: "Failed to send OTP"

**Solutions**:
1. Check Twilio credentials in `.env`
2. Check internet connection
3. Check Twilio account status
4. Check error logs

---

## Files Created

### Backend
- ✅ `Backend/auth/twilio_service.py` - Twilio OTP service
- ✅ `Backend/auth/jwt_service.py` - JWT token service
- ✅ `Backend/auth/__init__.py` - Auth module init
- ✅ `Backend/api/routers/auth.py` - Auth API endpoints
- ✅ `Backend/auth/requirements.txt` - Dependencies

### Frontend
- ✅ `Frontend/kisanmitra-app/src/pages/Login.jsx` - Login UI

### Configuration
- ✅ `Backend/.env` - Twilio credentials
- ✅ `Backend/api/main.py` - Router registration

### Documentation
- ✅ `TWILIO_AUTH_GUIDE.md` - This file

---

## Summary

✅ **Complete OTP authentication** with Twilio
✅ **JWT token management** for sessions
✅ **Hindi interface** for farmers
✅ **Mock mode** for development
✅ **Auto user creation** on first login
✅ **Onboarding detection** and redirect
✅ **Secure and scalable** architecture

🎉 **Authentication system is ready to use!**

---

## Next Steps

1. **Get Twilio credentials** and configure `.env`
2. **Install dependencies**: `pip install twilio PyJWT`
3. **Restart backend** server
4. **Test login flow** on frontend
5. **Deploy to production** with proper security

For support, check:
- Twilio Docs: https://www.twilio.com/docs
- JWT Docs: https://jwt.io
- FastAPI Docs: https://fastapi.tiangolo.com
