# 🔧 Auth System Troubleshooting Guide

## Quick Fix

```bash
# Run this to diagnose and fix:
fix_auth.bat
```

This will:
1. Run diagnostics
2. Install/update dependencies
3. Test backend startup
4. Show any errors

---

## Common Issues & Solutions

### Issue 1: "Module not found" Error

**Error**: `ModuleNotFoundError: No module named 'twilio'` or similar

**Solution**:
```bash
cd Backend
pip install twilio PyJWT python-dotenv
```

---

### Issue 2: Backend Won't Start

**Error**: Backend crashes on startup

**Solution**:
```bash
# Check for detailed errors:
cd Backend
python -m uvicorn api.main:app --reload --port 8000

# Look for the error message
```

**Common causes**:
- Missing dependencies
- Import errors
- Port 8000 already in use

---

### Issue 3: "404 Not Found" on Auth Endpoints

**Error**: `POST /api/v1/auth/send-otp` returns 404

**Solution**:

Check if auth router is registered:
1. Open `Backend/api/main.py`
2. Look for:
   ```python
   from .routers import auth
   app.include_router(auth.router, prefix=settings.API_V1_STR)
   ```

If missing, the router isn't registered.

---

### Issue 4: OTP Not Sending

**Error**: "Failed to send OTP"

**Solutions**:

**If using Real Twilio**:
1. Check `.env` file has correct credentials
2. Check Twilio account balance
3. Check phone number format (+91...)

**If in MOCK Mode**:
1. OTP should appear in console
2. OTP should appear in alert popup
3. Check browser console (F12)

---

### Issue 5: OTP Verification Fails

**Error**: "Invalid OTP" or "OTP expired"

**Solutions**:
1. Check OTP is correct (6 digits)
2. Check OTP hasn't expired (10 min limit)
3. Try resending OTP
4. Check backend console for errors

---

### Issue 6: Database Connection Error

**Error**: "Failed to connect to MongoDB"

**Solutions**:
1. Start MongoDB:
   ```bash
   mongod --dbpath C:\data\db
   ```

2. Check if MongoDB is running:
   ```bash
   mongo --eval "db.adminCommand('ping')"
   ```

3. Check connection string in code

---

### Issue 7: CORS Error

**Error**: "CORS policy blocked" in browser console

**Solution**:

Backend should have CORS enabled. Check `Backend/api/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Diagnostic Steps

### Step 1: Run Diagnostic Script

```bash
python Backend\diagnose_auth.py
```

This checks:
- ✅ All imports work
- ✅ Environment variables set
- ✅ Twilio service works
- ✅ JWT service works
- ✅ Router loaded
- ✅ Dependencies installed

---

### Step 2: Check Backend Logs

```bash
cd Backend
python -m uvicorn api.main:app --reload --port 8000
```

Look for:
- ✅ "Application startup complete"
- ❌ Any error messages
- ❌ Import errors
- ❌ Module not found

---

### Step 3: Test in Swagger UI

1. Start backend
2. Visit: `http://localhost:8000/docs`
3. Look for "Authentication" section
4. Try `/api/v1/auth/send-otp`
5. Enter: `{"phone_number": "+919876543210"}`
6. Click "Execute"

**Expected**: 200 OK with OTP (in MOCK mode)
**If Error**: Check response for details

---

### Step 4: Test Frontend

1. Visit: `http://localhost:5173/login`
2. Open browser console (F12)
3. Enter phone number
4. Click "OTP भेजें"
5. Check console for errors

**Expected**: OTP sent message
**If Error**: Check Network tab for failed requests

---

## Manual Fixes

### Fix 1: Reinstall Dependencies

```bash
cd Backend
pip uninstall twilio PyJWT python-dotenv -y
pip install twilio PyJWT python-dotenv
```

---

### Fix 2: Reset Auth Module

```bash
# Delete __pycache__ folders
cd Backend
rmdir /s /q auth\__pycache__
rmdir /s /q api\__pycache__
rmdir /s /q api\routers\__pycache__
```

---

### Fix 3: Check File Structure

Ensure these files exist:
```
Backend/
  auth/
    __init__.py
    twilio_service.py
    jwt_service.py
  api/
    routers/
      auth.py
    main.py
```

---

### Fix 4: Verify .env File

Check `Backend/.env` has:
```env
TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_PHONE_NUMBER=+1234567890
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=720
```

---

## Testing Checklist

After fixing, test:

```
□ Backend starts without errors
□ Swagger UI loads (http://localhost:8000/docs)
□ Auth endpoints visible in Swagger
□ Can send OTP via Swagger
□ Frontend login page loads
□ Can enter phone number
□ Can send OTP from frontend
□ Can verify OTP
□ Can login successfully
```

---

## Get Help

If still broken, provide:

1. **Error message** (exact text)
2. **Backend console output**
3. **Browser console errors** (F12 → Console)
4. **Network tab** (F12 → Network → failed request)
5. **Diagnostic output** (from `diagnose_auth.py`)

---

## Quick Commands

```bash
# Diagnose
python Backend\diagnose_auth.py

# Fix
fix_auth.bat

# Test backend
cd Backend
python -m uvicorn api.main:app --reload --port 8000

# Test in browser
http://localhost:8000/docs
http://localhost:5173/login
```

---

## Success Indicators

When working correctly:

✅ Backend starts: "Application startup complete"
✅ Swagger shows: Authentication section with 5 endpoints
✅ Send OTP works: Returns 200 with success message
✅ Frontend loads: Login page visible
✅ OTP sends: Alert/console shows OTP (MOCK mode)
✅ OTP verifies: Returns token and redirects

---

## Still Broken?

Run this and share the output:

```bash
fix_auth.bat > auth_debug.txt 2>&1
```

Then share `auth_debug.txt` file.
