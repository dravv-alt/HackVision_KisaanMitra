# 🚀 Quick Start - Testing Twilio Auth

## Fastest Way to Test (3 Steps)

### Step 1: Setup (One-time)
```bash
# Double-click this file:
setup_auth.bat
```

This will:
- Install `twilio` and `PyJWT` packages
- Test your Twilio configuration
- Show if everything is ready

### Step 2: Start Servers

**Terminal 1 - Backend:**
```bash
start_backend.bat
```

**Terminal 2 - Frontend:**
```bash
cd Frontend\kisanmitra-app
npm run dev
```

### Step 3: Test Login

1. Open browser: **`http://localhost:5173/login`**
2. Enter your phone number (10 digits)
3. Click **"OTP भेजें"**
4. Check your phone for SMS
5. Enter the 6-digit OTP
6. Click **"सत्यापित करें और लॉगिन करें"**
7. ✅ You're logged in!

---

## What You'll See

### Login Page
```
┌─────────────────────────────────────┐
│         🌾 किसानमित्र              │
│  अपने फ़ोन नंबर से लॉगिन करें      │
│                                     │
│  फ़ोन नंबर (Phone Number)          │
│  ┌────┬─────────────────────────┐  │
│  │+91 │ 9876543210              │  │
│  └────┴─────────────────────────┘  │
│                                     │
│  [     OTP भेजें     →]            │
└─────────────────────────────────────┘
```

### OTP Screen
```
┌─────────────────────────────────────┐
│         🌾 किसानमित्र              │
│       OTP दर्ज करें                 │
│                                     │
│  OTP दर्ज करें (Enter OTP)         │
│  ┌─────────────────────────────┐   │
│  │      1  2  3  4  5  6       │   │
│  └─────────────────────────────┘   │
│                                     │
│  +91 9876543210 पर भेजा गया        │
│  OTP 10 मिनट के लिए मान्य है       │
│                                     │
│  [सत्यापित करें और लॉगिन करें ✓]  │
│                                     │
│  ← नंबर बदलें  |  OTP फिर से भेजें │
└─────────────────────────────────────┘
```

---

## SMS You'll Receive

```
आपका KisanMitra OTP है: 123456

यह OTP 10 मिनट के लिए मान्य है।

Your KisanMitra OTP is: 123456

Valid for 10 minutes.
```

---

## After Login

**New User:**
- Redirects to → `/onboarding/language`
- Complete onboarding flow
- Then go to dashboard

**Existing User:**
- Redirects to → `/dashboard`
- See all your data

---

## Troubleshooting

### SMS not received?
1. Check phone number is correct
2. Check Twilio account has balance
3. Wait 1-2 minutes (SMS can be delayed)
4. Try "OTP फिर से भेजें" (Resend OTP)

### Backend not starting?
```bash
# Install dependencies first
cd Backend
pip install twilio PyJWT python-dotenv
```

### Frontend not starting?
```bash
cd Frontend\kisanmitra-app
npm install
npm run dev
```

### Wrong OTP error?
- You have 3 attempts
- After 3 wrong attempts, request new OTP
- OTP expires after 10 minutes

---

## Quick Commands

```bash
# Test Twilio setup
python Backend\test_twilio_auth.py

# Start backend
start_backend.bat

# Start frontend
cd Frontend\kisanmitra-app && npm run dev

# Visit login
http://localhost:5173/login
```

---

## Expected Flow

```
1. Enter phone: 9876543210
   ↓
2. Click "OTP भेजें"
   ↓
3. Receive SMS with OTP
   ↓
4. Enter OTP: 123456
   ↓
5. Click "सत्यापित करें"
   ↓
6. ✅ Logged in!
   ↓
7. Redirect to onboarding or dashboard
```

---

## Success Indicators

✅ Backend running on `http://localhost:8000`
✅ Frontend running on `http://localhost:5173`
✅ Login page loads with Hindi text
✅ Phone input accepts 10 digits
✅ OTP button sends request
✅ SMS received on phone
✅ OTP verification works
✅ Redirects after login

---

## Files You Need

All files are already created:
- ✅ `Backend/auth/twilio_service.py`
- ✅ `Backend/auth/jwt_service.py`
- ✅ `Backend/api/routers/auth.py`
- ✅ `Frontend/src/pages/Login.jsx`
- ✅ `Backend/.env` (with your Twilio credentials)

---

## Ready to Test!

Just run:
```bash
setup_auth.bat
```

Then start both servers and visit:
```
http://localhost:5173/login
```

🎉 **That's it!**
