# 🚀 Complete System Launch Guide

## Quick Start (One Click!)

### **Option 1: Launch Everything**
```bash
# Double-click this file:
launch_all.bat
```

This will automatically start:
- ✅ MongoDB Server
- ✅ Backend API Server (port 8000)
- ✅ Frontend Dev Server (port 5173)
- ✅ Opens login page in browser

---

## Manual Launch (Step by Step)

### **Step 1: Start MongoDB**

**Option A - Windows Service** (if installed as service):
```bash
net start MongoDB
```

**Option B - Manual Start**:
```bash
mongod --dbpath C:\data\db
```

**Verify**: MongoDB should be running on `mongodb://localhost:27017`

---

### **Step 2: Start Backend API**

```bash
# Double-click:
start_backend.bat

# Or manually:
cd Backend
python -m uvicorn api.main:app --reload --port 8000
```

**Verify**: 
- Backend running: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

---

### **Step 3: Start Frontend**

```bash
cd Frontend\kisanmitra-app
npm run dev
```

**Verify**: Frontend running on `http://localhost:5173`

---

## 🔐 Testing Authentication

### **Quick Test**:
```bash
# Double-click:
test_auth.bat
```

### **Manual Test**:

1. **Open Login Page**:
   ```
   http://localhost:5173/login
   ```

2. **Enter Phone Number**:
   - Format: `9876543210` (10 digits)
   - System adds +91 automatically

3. **Send OTP**:
   - Click "OTP भेजें"
   - Wait for SMS (or check console in MOCK mode)

4. **Enter OTP**:
   - Enter 6-digit OTP
   - Click "सत्यापित करें और लॉगिन करें"

5. **Success!**:
   - New user → Redirects to `/onboarding/language`
   - Existing user → Redirects to `/dashboard`

---

## 📊 Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:5173 | Main application |
| **Login** | http://localhost:5173/login | Authentication |
| **Backend API** | http://localhost:8000 | API server |
| **Swagger UI** | http://localhost:8000/docs | API documentation |
| **MongoDB** | mongodb://localhost:27017 | Database |

---

## 🧪 Testing Endpoints

### **1. Health Check**
```bash
curl http://localhost:8000/health
```

### **2. Test Auth API**
```bash
# Send OTP
curl -X POST http://localhost:8000/api/v1/auth/send-otp \
  -H "Content-Type: application/json" \
  -d "{\"phone_number\": \"+919876543210\"}"

# Verify OTP
curl -X POST http://localhost:8000/api/v1/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d "{\"phone_number\": \"+919876543210\", \"otp\": \"123456\"}"
```

### **3. Test Inventory API**
```bash
# Get items
curl http://localhost:8000/api/v1/inventory/items/F001

# Add item
curl -X POST http://localhost:8000/api/v1/inventory/add \
  -H "Content-Type: application/json" \
  -d "{\"farmer_id\": \"F001\", \"category\": \"seeds\", \"name\": \"गेहूँ के बीज\", \"quantity\": 50, \"unit\": \"kg\", \"cost_per_unit\": 40}"
```

---

## 🔍 Troubleshooting

### **MongoDB Not Starting**

**Issue**: MongoDB fails to start

**Solutions**:
1. Check if MongoDB is installed:
   ```bash
   mongod --version
   ```

2. Create data directory:
   ```bash
   mkdir C:\data\db
   ```

3. Check if port 27017 is free:
   ```bash
   netstat -ano | findstr :27017
   ```

4. Try starting manually:
   ```bash
   mongod --dbpath C:\data\db
   ```

---

### **Backend Not Starting**

**Issue**: Backend fails to start

**Solutions**:
1. Check Python version:
   ```bash
   python --version
   # Should be 3.8+
   ```

2. Install dependencies:
   ```bash
   cd Backend
   pip install -r requirements.txt
   pip install twilio PyJWT python-dotenv
   ```

3. Check if port 8000 is free:
   ```bash
   netstat -ano | findstr :8000
   ```

4. Check for errors:
   ```bash
   cd Backend
   python -m uvicorn api.main:app --reload --port 8000
   # Look for error messages
   ```

---

### **Frontend Not Starting**

**Issue**: Frontend fails to start

**Solutions**:
1. Check Node.js version:
   ```bash
   node --version
   # Should be 16+
   ```

2. Install dependencies:
   ```bash
   cd Frontend\kisanmitra-app
   npm install
   ```

3. Clear cache and reinstall:
   ```bash
   cd Frontend\kisanmitra-app
   rm -rf node_modules package-lock.json
   npm install
   ```

4. Check if port 5173 is free:
   ```bash
   netstat -ano | findstr :5173
   ```

---

### **OTP Not Received**

**Issue**: SMS not received

**Solutions**:

**If using Real Twilio**:
1. Check Twilio credentials in `.env`
2. Check Twilio account balance
3. Check phone number format (+91...)
4. Check Twilio console logs

**If in MOCK Mode**:
1. Check browser console (F12)
2. Look for alert popup with OTP
3. Check yellow debug box on page
4. OTP is printed in backend console

---

### **Login Fails**

**Issue**: Can't login after entering OTP

**Solutions**:
1. Check browser console for errors
2. Check backend console for errors
3. Verify OTP is correct
4. Check if OTP expired (10 min limit)
5. Try resending OTP
6. Check MongoDB is running

---

## 📝 Pre-Launch Checklist

Before launching, ensure:

```
□ MongoDB installed
□ Python 3.8+ installed
□ Node.js 16+ installed
□ Dependencies installed (pip install -r requirements.txt)
□ Frontend dependencies installed (npm install)
□ .env file configured with Twilio credentials
□ MongoDB data directory exists (C:\data\db)
□ Ports 8000, 5173, 27017 are free
```

---

## 🎯 Launch Sequence

### **Automated** (Recommended):
```bash
1. Double-click: launch_all.bat
2. Wait for all services to start
3. Browser opens automatically
4. Start testing!
```

### **Manual**:
```bash
1. Start MongoDB
   mongod --dbpath C:\data\db

2. Start Backend (new terminal)
   cd Backend
   python -m uvicorn api.main:app --reload --port 8000

3. Start Frontend (new terminal)
   cd Frontend\kisanmitra-app
   npm run dev

4. Open browser
   http://localhost:5173/login
```

---

## 🛑 Stopping Services

### **Automated**:
```bash
# Double-click:
stop_all_services.bat
```

### **Manual**:
```bash
# Stop each terminal with Ctrl+C
# Or close the terminal windows
```

---

## 📊 System Status Check

### **Check All Services**:
```bash
# MongoDB
mongo --eval "db.adminCommand('ping')"

# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:5173
```

### **Check Processes**:
```bash
# MongoDB
tasklist | findstr mongod

# Backend
tasklist | findstr python

# Frontend
tasklist | findstr node
```

---

## 🎉 Success Indicators

When everything is running correctly:

✅ **MongoDB**: No errors in console
✅ **Backend**: Shows "Application startup complete"
✅ **Frontend**: Shows "Local: http://localhost:5173/"
✅ **Swagger**: http://localhost:8000/docs loads
✅ **Login Page**: http://localhost:5173/login loads
✅ **OTP**: Can send and receive OTP
✅ **Login**: Can login successfully

---

## 📚 Quick Reference

### **Start Everything**:
```bash
launch_all.bat
```

### **Stop Everything**:
```bash
stop_all_services.bat
```

### **Test Auth**:
```bash
test_auth.bat
```

### **View Logs**:
- MongoDB: Check MongoDB console window
- Backend: Check Backend console window
- Frontend: Check Frontend console window
- Browser: Press F12 → Console tab

---

## 🚀 Ready to Launch!

Everything is set up and ready to go!

**Just run**:
```bash
launch_all.bat
```

And start testing your KisanMitra application! 🎉
