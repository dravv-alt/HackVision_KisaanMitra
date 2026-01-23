# Testing Twilio Authentication - Step by Step Guide

## Prerequisites Checklist

Before testing, make sure you have:
- ✅ Twilio credentials configured in `Backend/.env`
- ✅ Dependencies installed (`twilio`, `PyJWT`)
- ✅ MongoDB running
- ✅ Backend server ready to start
- ✅ Frontend ready to start

---

## Step 1: Verify Twilio Configuration

Run the test script:

```bash
cd C:\Users\bhavv\OneDrive\Desktop\RAD\HackVision_KisaanMitra
python Backend\test_twilio_auth.py
```

**Expected Output:**
```
============================================================
🔐 TESTING TWILIO AUTHENTICATION SETUP
============================================================

📋 Checking Environment Variables...
✅ TWILIO_ACCOUNT_SID: ACxxxxxxxx...
✅ TWILIO_AUTH_TOKEN: xxxxxxxxxx...
✅ TWILIO_PHONE_NUMBER: +1234567890
✅ JWT_SECRET_KEY: Configured

🔧 Testing Twilio Service...
✅ Twilio client initialized successfully
✅ Ready to send SMS

🔑 Testing JWT Service...
✅ JWT token created: eyJ0eXAiOiJKV1QiLCJhbGc...
✅ JWT token verified successfully

============================================================
📊 SUMMARY
============================================================
✅ Twilio is CONFIGURED - Real SMS will be sent
📱 You can test with your phone number
```

---

## Step 2: Start Backend Server

### Option 1: Using batch file
```bash
start_backend.bat
```

### Option 2: Manual start
```bash
cd Backend
python -m uvicorn api.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Verify Backend:**
- Open browser: `http://localhost:8000/docs`
- You should see Swagger UI
- Look for **Authentication** section with endpoints:
  - `POST /api/v1/auth/send-otp`
  - `POST /api/v1/auth/verify-otp`
  - `POST /api/v1/auth/resend-otp`
  - `POST /api/v1/auth/refresh-token`
  - `GET /api/v1/auth/verify-token`

---

## Step 3: Start Frontend

```bash
cd Frontend\kisanmitra-app
npm run dev
```

**Expected Output:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

---

## Step 4: Test Login Flow

### 4.1 Navigate to Login Page

Open browser: `http://localhost:5173/login`

**You should see:**
- 🌾 KisanMitra logo
- किसानमित्र title
- "अपने फ़ोन नंबर से लॉगिन करें" subtitle
- Phone number input with +91 prefix
- "OTP भेजें" button

### 4.2 Enter Phone Number

**Test with your real phone number:**
```
Enter: 9876543210
(System will convert to +919876543210)
```

**Important:**
- Use a phone number that can receive SMS
- Must be a valid Indian mobile number (10 digits)
- Make sure you have access to this phone

### 4.3 Send OTP

Click **"OTP भेजें"** button

**What happens:**
1. Button shows "भेजा जा रहा है..." (Sending...)
2. Frontend sends request to backend
3. Backend generates 6-digit OTP
4. Twilio sends SMS to your phone
5. Page changes to OTP input screen

**Expected SMS:**
```
आपका KisanMitra OTP है: 123456

यह OTP 10 मिनट के लिए मान्य है।

Your KisanMitra OTP is: 123456

Valid for 10 minutes.
```

### 4.4 Enter OTP

**On the OTP screen you'll see:**
- "OTP दर्ज करें (Enter OTP)" label
- 6-digit input field
- "+91 9876543210 पर भेजा गया" (Sent to...)
- "OTP 10 मिनट के लिए मान्य है" (Valid for 10 minutes)
- "सत्यापित करें और लॉगिन करें" button
- "OTP फिर से भेजें" link

**Enter the 6-digit OTP** you received via SMS

### 4.5 Verify and Login

Click **"सत्यापित करें और लॉगिन करें"**

**What happens:**
1. Button shows "सत्यापित किया जा रहा है..." (Verifying...)
2. Frontend sends OTP to backend
3. Backend verifies OTP
4. Backend checks if user exists
5. If new user:
   - Creates user in database
   - Generates JWT token
   - Redirects to `/onboarding/language`
6. If existing user:
   - Generates JWT token
   - Redirects to `/dashboard`

**Success!** You should be logged in and redirected.

---

## Step 5: Verify Login Success

### Check Browser Console

Press `F12` and check Console tab:

**You should see:**
```javascript
// Token stored
localStorage.getItem('kisanmitra_auth_token')
// Returns: "eyJ0eXAiOiJKV1QiLCJhbGc..."

localStorage.getItem('kisanmitra_user_id')
// Returns: "U12345678"

localStorage.getItem('kisanmitra_farmer_id')
// Returns: "F12345678"
```

### Check Database

Open MongoDB Compass or mongo shell:

```javascript
use kisanmitra
db.farmers.find({ phone: "+919876543210" })
```

**You should see:**
```javascript
{
  "_id": ObjectId("..."),
  "user_id": "U12345678",
  "farmer_id": "F12345678",
  "phone": "+919876543210",
  "name": "Farmer",
  "language": "hi",
  "onboarding_completed": false,
  "created_at": ISODate("..."),
  "updated_at": ISODate("...")
}
```

---

## Step 6: Test Different Scenarios

### Scenario 1: Resend OTP

1. Enter phone number
2. Click "OTP भेजें"
3. On OTP screen, click **"OTP फिर से भेजें"**
4. ✅ New OTP should be sent
5. Old OTP becomes invalid

### Scenario 2: Wrong OTP

1. Enter phone number
2. Receive OTP
3. Enter **wrong OTP** (e.g., 000000)
4. Click verify
5. ✅ Should show: "Incorrect OTP. 2 attempts remaining."
6. Try again with correct OTP

### Scenario 3: Expired OTP

1. Send OTP
2. Wait 10+ minutes
3. Try to verify
4. ✅ Should show: "OTP has expired. Please request a new OTP."

### Scenario 4: Change Phone Number

1. Enter phone number
2. Receive OTP
3. Click **"← नंबर बदलें"**
4. ✅ Should go back to phone input
5. Can enter different number

### Scenario 5: Existing User Login

1. Complete onboarding once
2. Logout
3. Login again with same number
4. ✅ Should go directly to `/dashboard` (not onboarding)

---

## Step 7: Test API Directly (Optional)

### Using Swagger UI

Visit: `http://localhost:8000/docs`

#### Test Send OTP:
1. Expand `POST /api/v1/auth/send-otp`
2. Click "Try it out"
3. Enter:
```json
{
  "phone_number": "+919876543210"
}
```
4. Click "Execute"
5. ✅ Should return success with message

#### Test Verify OTP:
1. Expand `POST /api/v1/auth/verify-otp`
2. Click "Try it out"
3. Enter:
```json
{
  "phone_number": "+919876543210",
  "otp": "123456"
}
```
4. Click "Execute"
5. ✅ Should return token and user data

### Using cURL

```bash
# Send OTP
curl -X POST "http://localhost:8000/api/v1/auth/send-otp" \
  -H "Content-Type: application/json" \
  -d "{\"phone_number\": \"+919876543210\"}"

# Verify OTP
curl -X POST "http://localhost:8000/api/v1/auth/verify-otp" \
  -H "Content-Type: application/json" \
  -d "{\"phone_number\": \"+919876543210\", \"otp\": \"123456\"}"
```

---

## Troubleshooting

### Issue: SMS not received

**Check:**
1. ✅ Phone number is correct (+91 prefix)
2. ✅ Phone can receive SMS
3. ✅ Twilio account has balance
4. ✅ Twilio phone number is active
5. ✅ Check Twilio console logs

**Solution:**
- Visit: https://console.twilio.com/us1/monitor/logs/sms
- Check SMS delivery status
- Verify phone number format

### Issue: "Failed to send OTP"

**Check:**
1. ✅ Backend server is running
2. ✅ Twilio credentials in `.env` are correct
3. ✅ Internet connection is working
4. ✅ Check backend console for errors

**Solution:**
```bash
# Check backend logs
# Look for error messages
# Verify Twilio credentials
```

### Issue: "Invalid token"

**Check:**
1. ✅ JWT_SECRET_KEY is set in `.env`
2. ✅ Token is stored in localStorage
3. ✅ Token hasn't expired (30 days)

**Solution:**
```javascript
// Clear and login again
localStorage.clear();
// Go to /login and login again
```

### Issue: Stuck on loading

**Check:**
1. ✅ Backend is running on port 8000
2. ✅ Frontend is running on port 5173
3. ✅ No CORS errors in console
4. ✅ Network tab shows requests

**Solution:**
```bash
# Restart both servers
# Check browser console for errors
```

---

## Success Checklist

After successful testing, you should have:

- ✅ Received SMS with OTP
- ✅ Successfully verified OTP
- ✅ JWT token stored in localStorage
- ✅ User created in MongoDB
- ✅ Redirected to onboarding or dashboard
- ✅ Can login again with same number
- ✅ Can resend OTP
- ✅ Error handling works

---

## Next Steps

After successful testing:

1. **Test with multiple users**
   - Different phone numbers
   - Verify user isolation

2. **Test onboarding flow**
   - Complete onboarding
   - Verify data is saved
   - Login again (should skip onboarding)

3. **Test token refresh**
   - Use refresh-token endpoint
   - Verify new token works

4. **Monitor Twilio usage**
   - Check SMS count
   - Monitor costs
   - Set up alerts

5. **Deploy to production**
   - Use production Twilio credentials
   - Enable HTTPS
   - Set up rate limiting

---

## Testing Checklist

```
□ Twilio credentials configured
□ Dependencies installed
□ Backend server started
□ Frontend server started
□ Login page loads
□ Phone number input works
□ OTP sent successfully
□ SMS received on phone
□ OTP verification works
□ JWT token generated
□ User created in database
□ Redirect works correctly
□ Resend OTP works
□ Wrong OTP shows error
□ Change number works
□ Existing user login works
```

---

## Support

If you encounter issues:

1. **Check backend logs** for errors
2. **Check browser console** for errors
3. **Check Twilio console** for SMS logs
4. **Verify `.env` configuration**
5. **Restart both servers**

For Twilio support:
- Docs: https://www.twilio.com/docs
- Console: https://console.twilio.com
- Support: https://support.twilio.com

---

## Summary

✅ **Twilio authentication is ready to test!**

**Quick Start:**
```bash
# 1. Test setup
python Backend\test_twilio_auth.py

# 2. Start backend
start_backend.bat

# 3. Start frontend
cd Frontend\kisanmitra-app && npm run dev

# 4. Test login
Visit: http://localhost:5173/login
```

🎉 **Happy Testing!**
