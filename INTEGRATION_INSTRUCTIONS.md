# KisaanMitra Integration - Startup Instructions

**Last Updated**: 2026-01-23  
**Status**: Integrated

---

## Prerequisites

- **Python 3.13+** installed
- **Node.js 18+** installed
- **FFmpeg** installed (for voice audio processing)
- MongoDB (optional - system uses in-memory fallback)

---

## 1. Starting the Backend (FastAPI)

### Step 1: Navigate to Backend
```bash
cd Backend
```

### Step 2: Activate Virtual Environment
**Windows (PowerShell)**:
```bash
..\venv\Scripts\Activate.ps1
```

**Windows (CMD)**:
```bash
..\venv\Scripts\activate.bat
```

**Linux/Mac**:
```bash
source ../venv/bin/activate
```

### Step 3: Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```

### Step 4: Start the Server
```bash
# Option 1: Using uvicorn (recommended)
uvicorn api.main:app --reload

# Option 2: Using Python module
python -m api.main
```

**Expected Output**:
```
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

**Server will be running at**: `http://localhost:8000`

**API Documentation**: `http://localhost:8000/docs`

---

## 2. Starting the Frontend (React + Vite)

### Step 1: Navigate to Frontend App
```bash
cd Frontend/kisanmitra-app
```

### Step 2: Install Dependencies (first time only)
```bash
npm install
```

### Step 3: Start Development Server
```bash
npm run dev
```

**Expected Output**:
```
VITE vX.X.X ready in XXX ms
➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**Frontend will be running at**: `http://localhost:5173`

---

## 3. Verifying the Integration

### Test 1: Backend Health Check
```bash
curl http://localhost:8000/health
```
**Expected**: `{"status":"healthy"}`

### Test 2: API Endpoints
```bash
# Test market price endpoint
curl "http://localhost:8000/api/v1/farming/market-price?crop=Onion"

# Test schemes endpoint
curl http://localhost:8000/api/v1/schemes
```

### Test 3: Frontend Connection
1. Open browser to `http://localhost:5173`
2. Open browser console (F12)
3. Try any feature that uses API (e.g., voice chat, crop selection)
4. Verify no CORS errors in console
5. Verify API requests succeed

---

## 4. Testing Voice Chat

### Text Input
1. Navigate to Voice Chat Interface in frontend
2. Type a message: "प्याज की कीमत क्या है"
3. Click Send
4. Verify response appears

### Audio Input
1. Click microphone icon
2. Record audio
3. Upload
4. Verify transcription and response

---

## 5. Testing Farm Features

### Crop Recommendations
1. Navigate to Farm Management → Planning Stage → Crop Selection
2. Fill in farm details:
   - **Farmer ID**: F001 (or F002, F003, F004)
   - **State**: Maharashtra
   - **Soil Type**: loamy
   - **Farm Size**: 5 acres
   - **Season**: kharif
3. Click "Get Recommendations"
4. Verify crop cards appear

### Market Prices
1. Navigate to Farm Management → Market Prices
2. Select crop (e.g., Onion)
3. Verify price, trend, and forecast display

### Disease Detection
1. Navigate to Farm Management → Crop Doctor
2. Upload crop image
3. **Note**: May show error due to TensorFlow model issue
4. **Expected**: Error message about model loading (known issue)

---

## 6. Testing Financial Tracking

1. Navigate to Financial Tracking
2. View P&L Report
3. Add test expense:
   - **Category**: seeds
   - **Amount**: 5000
   - **Season**: kharif
4. Verify transaction appears

---

## 7. Testing Government Schemes

1. Navigate to Government Schemes
2. Verify scheme cards load
3. Filter by state (e.g., Maharashtra)
4. Click on a scheme to see details

---

## 8. Troubleshooting

### Backend Won't Start

**Error**: `python: command not found`  
**Solution**: Install Python 3.13+ and add to PATH

**Error**: `ModuleNotFoundError`  
**Solution**: `pip install -r requirements.txt`

**Error**: `FFmpeg not found`  
**Solution**: Install FFmpeg:
```bash
# Windows
winget install ffmpeg

# Restart terminal after installation
```

**Error**: `TensorFlow/Keras not available`  
**Solution**: Expected - disease detection will not work until model retrained

### Frontend Won't Start

**Error**: `npm: command not found`  
**Solution**: Install Node.js from https://nodejs.org

**Error**: `Cannot find module`  
**Solution**: `npm install`

### Integration Issues

**Error**: `Failed to fetch` or CORS errors  
**Solution**: 
1. Verify backend is running on port 8000
2. Check `.env` file in frontend has correct URL
3. Verify no firewall blocking localhost

**Error**: `Farmer not found: xyz`  
**Solution**: Use valid test farmer IDs: F001, F002, F003, or F004

**Error**: `farmer_location must be [latitude, longitude]`  
**Solution**: Use numeric coordinates: `[19.9975, 73.7898]`

---

## 9. Development Workflow

### Making Backend Changes
1. Edit Python files in `Backend/`
2. Changes auto-reload (if using `--reload` flag)
3. Check terminal for errors
4. Test endpoint in browser/Postman

### Making Frontend Changes
1. Edit React files in `Frontend/kisanmitra-app/src/`
2. Changes auto-reload in browser
3. Check browser console for errors
4. Test UI interactions

### Adding New API Endpoints
1. Create endpoint in appropriate router (`Backend/api/routers/`)
2. Add to main.py if new router
3. Test with curl/Postman
4. Create service function in frontend (`Frontend/kisanmitra-app/src/services/`)
5. Integrate into React component

---

## 10. Known Issues

| Issue                               | Workaround                                                         |
| :---------------------------------- | :----------------------------------------------------------------- |
| Disease detection fails             | TensorFlow model needs retraining - endpoint will return 500 error |
| Collaborative endpoints not working | Router may not be registered - check api/main.py                   |
| Voice audio transcription slow      | Whisper model loading time - first request may take longer         |

---

## 11. Production Deployment

### Backend
- Set environment variables securely
- Use production WSGI server (gunicorn)
- Configure MongoDB for persistence
- Setup HTTPS/SSL
- Configure CORS for frontend domain only

### Frontend
- Build production bundle: `npm run build`
- Serve from `dist/` directory
- Configure API_BASE_URL to production backend
- Setup CDN for static assets

---

## 12. Support

**API Documentation**: http://localhost:8000/docs  
**Backend Docs**: `Backend/codebase_docs/README_Codebase.md`  
**Frontend Docs**: `Frontend/Frontend_Readme.md`

**Test Farmer IDs**: F001, F002, F003, F004  
**Example Coordinates**: [19.9975, 73.7898] (Nasik, Maharashtra)

---

**Integration Complete** ✅  
**Date**: 2026-01-23
