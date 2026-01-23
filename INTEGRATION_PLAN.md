# KisaanMitra Frontend-Backend Integration Plan

**Created**: 2026-01-23  
**Status**: AWAITING APPROVAL

---

## 📊 STEP 1 & 2: API & FRONTEND ANALYSIS

### Backend API Endpoints (FastAPI)

Based on analysis of `Backend/api/` directory:

#### 1. **Voice Agent** (`/api/v1/voice`)
- `POST /voice/process` - Process text input from voice/text
- `POST /voice/process-audio` - Process audio file (multipart)

#### 2. **Farm Management** (`/api/v1/farming` & `/api/v1/planning` & `/api/v1/post-harvest`)
- `POST /planning/pre-seeding` - Get crop recommendations
- `POST /farming/disease-detect` - Upload crop image for disease detection
- `GET /farming/market-price` - Get market prices for crops
- `POST /post-harvest/plan` - Get post-harvest plan

#### 3. **Government Schemes** (`/api/v1/schemes`)
- `GET /schemes` - List all government schemes
- `GET /schemes/{scheme_id}` - Get scheme details

#### 4. **Financial Tracking** (`/api/v1/finance`)
- `POST /finance/report` - Get P&L report
- `POST /finance/add-transaction` - Add income/expense
- `GET /finance/dashboard/{farmer_id}` - Get financial dashboard

#### 5. **Collaborative Farming** (`/api/v1/collaborative`)
- `GET /collaborative/marketplace/{farmer_id}` - Get marketplace listings
- `POST /collaborative/equipment/request` - Request equipment rental
- `POST /collaborative/land-pool` - Create land pool request

---

### Frontend Pages Analysis

#### Currently **HARDCODED** Pages:
1. ✅ **GovernmentSchemes.jsx** - Already integrated (completed earlier)
2. ❌ **Dashboard.jsx** - Hardcoded weather, crops, prices, finance
3. ❌ **PlanningStage.jsx** - Hardcoded crop recommendations
4. ❌ **FarmingStage.jsx** - Hardcoded disease detection
5. ❌ **PostHarvestStage.jsx** - Hardcoded storage advice
6. ❌ **Finance.jsx** - Hardcoded transactions and P&L
7. ❌ **ActiveCrops.jsx** - Hardcoded crop list
8. ❌ **Inventory.jsx** - Hardcoded inventory data
9. ❌ **CollaborativeFarming.jsx** - Hardcoded marketplace
10. ❌ **PriorityAlerts.jsx** - Hardcoded alerts
11. ❌ **VoiceInterface.jsx** - **REVERTED** to hardcoded (previously broken)

---

## 📋 STEP 3: ENDPOINT TO FRONTEND MAPPING

### Priority 1: Core Features

| Frontend Component              | Backend Endpoint                         | Method | Data Flow                             |
| :------------------------------ | :--------------------------------------- | :----- | :------------------------------------ |
| **Dashboard** → Weather         | `/planning/pre-seeding`                  | POST   | Farmer context → Weather data         |
| **Dashboard** → Active Crops    | `/planning/pre-seeding`                  | POST   | Farmer ID → Crop recommendations      |
| **Dashboard** → Market Prices   | `/farming/market-price`                  | GET    | Query params → Price list             |
| **Dashboard** → Finance Summary | `/finance/dashboard/{farmer_id}`         | GET    | Farmer ID → Revenue/Expense           |
| **PlanningStage**               | `/planning/pre-seeding`                  | POST   | Farmer context → Crop cards           |
| **FarmingStage** (Disease)      | `/farming/disease-detect`                | POST   | Image upload → Disease diagnosis      |
| **PostHarvestStage**            | `/post-harvest/plan`                     | POST   | Farmer context → Storage plan         |
| **Finance**                     | `/finance/report`                        | POST   | Farmer ID + season → P&L report       |
| **Finance** (Add Transaction)   | `/finance/add-transaction`               | POST   | Transaction data → Confirmation       |
| **CollaborativeFarming**        | `/collaborative/marketplace/{farmer_id}` | GET    | Farmer ID → Listings                  |
| **VoiceInterface** (Text)       | `/voice/process`                         | POST   | Hindi text → AI response              |
| **VoiceInterface** (Audio)      | `/voice/process-audio`                   | POST   | Audio file → Transcription → Response |

### Priority 2: Already Complete
| Frontend Component    | Status                                        |
| :-------------------- | :-------------------------------------------- |
| **GovernmentSchemes** | ✅ Already integrated with `/schemes` endpoint |

---

## 🎨 STEP 4: VISUAL INTEGRATION FLOW

```mermaid
graph TB
    subgraph Frontend[Frontend - React]
        D[Dashboard.jsx]
        P[PlanningStage.jsx]
        F[FarmingStage.jsx]
        PH[PostHarvestStage.jsx]
        FN[Finance.jsx]
        CF[CollaborativeFarming.jsx]
        VI[VoiceInterface.jsx]
    end

    subgraph Services[Frontend Services Layer]
        API[api.js - HTTP Client]
        VS[voiceService.js]
        FS[farmService.js]
        FNS[financeService.js]
        SS[schemesService.js ✅]
        CS[collaborativeService.js - NEW]
    end

    subgraph Backend[Backend - FastAPI]
        VA[/voice/*]
        FM[/farming/*]
        PL[/planning/*]
        PHS[/post-harvest/*]
        FI[/finance/*]
        CO[/collaborative/*]
        SC[/schemes/* ✅]
    end

    D -->|Weather, Crops, Prices| FS
    P -->|Crop Planning| FS
    F -->|Disease Detection| FS
    PH -->|Storage Plan| FS
    FN -->|P&L, Transactions| FNS
    CF -->|Marketplace| CS
    VI -->|Voice Queries| VS

    VS --> API
    FS --> API
    FNS --> API
    SS --> API
    CS --> API

    API -->|POST| VA
    API -->|POST/GET| FM
    API -->|POST| PL
    API -->|POST| PHS
    API -->|POST/GET| FI
    API -->|GET/POST| CO
    API -->|GET| SC

    style D fill:#ffeb3b
    style P fill:#ffeb3b
    style F fill:#ffeb3b
    style PH fill:#ffeb3b
    style FN fill:#ffeb3b
    style CF fill:#ffeb3b
    style VI fill:#ffeb3b
    style SS fill:#4caf50
    style SC fill:#4caf50
```

### Data Flow Example: **Dashboard Weather Widget**

```
User Opens Dashboard
        ↓
Dashboard.jsx (useEffect)
        ↓
farmService.getCropRecommendations(farmerId)
        ↓
api.post('/planning/pre-seeding', { farmer_id })
        ↓
FastAPI → PreSeedingService
        ↓
Weather API Call (OpenWeather)
        ↓
Response: { weather_summary, temperature, humidity, ... }
        ↓
Frontend receives JSON
        ↓
setState({ weather: response.weather })
        ↓
Dashboard displays: "32°C SUNNY, 10% RAIN"
```

---

## ✅ STEP 5: IMPLEMENTATION CHECKLIST

### Phase 1: Dashboard Integration (30 min)
- [ ] Create `useEffect` hook to fetch data on mount
- [ ] Call `farmService.getCropRecommendations()` for weather
- [ ] Call `farmService.getMarketPrice()` for market prices
- [ ] Call `financeService.getDashboard()` for finance summary
- [ ] Replace hardcoded values with API data
- [ ] Add loading states

### Phase 2: Planning Stage (20 min)
- [ ] Update `PlanningStage.jsx` to call `/planning/pre-seeding`
- [ ] Parse crop recommendation cards from API
- [ ] Display weather and scheme data

### Phase 3: Farming Stage (25 min)
- [ ] Add image upload handler
- [ ] Call `/farming/disease-detect` with FormData
- [ ] Display disease diagnosis results
- [ ] Add error handling for unsupported image types

### Phase 4: Post-Harvest Stage (15 min)
- [ ] Call `/post-harvest/plan` with farmer context
- [ ] Display storage recommendations
- [ ] Show sell/store decision advice

### Phase 5: Finance Page (30 min)
- [ ] Fetch P&L report from `/finance/report`
- [ ] Display income/expense charts
- [ ] Add transaction form calling `/finance/add-transaction`
- [ ] Update UI after successful transaction

### Phase 6: Collaborative Farming (20 min)
- [ ] Create `collaborativeService.js`
- [ ] Fetch marketplace from `/collaborative/marketplace`
- [ ] Display equipment rental listings
- [ ] Add request equipment functionality

### Phase 7: Voice Interface (15 min)
- [ ] **FIX** the broken VoiceInterface
- [ ] Add text input field
- [ ] Call `/voice/process` for text queries
- [ ] Display AI responses with cards
- [ ] Add mic recording (optional - Phase 8)

### Phase 8: Audio Recording (Optional, 45 min)
- [ ] Install `react-mic` library
- [ ] Implement microphone recording
- [ ] Upload to `/voice/process-audio`
- [ ] Show transcription to user

---

## 🚨 CRITICAL INTEGRATION REQUIREMENTS

### 1. Environment Variables
**Frontend `.env`:**
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```
✅ Already configured

### 2. CORS Configuration
**Backend** already has permissive CORS:
```python
allow_origins=["*"]  # Development mode
```
✅ No changes needed

### 3. Error Handling Pattern
All API calls must use:
```javascript
try {
  const response = await farmService.getCropRecommendations(farmerId);
  setData(response);
} catch (error) {
  setError(getErrorMessage(error));
}
```

### 4. Loading States
All components must show:
- Spinner during API calls
- Error messages with retry button
- Empty state if no data

---

## 📊 ESTIMATED TIME

| Phase              | Component            | Time           |
| :----------------- | :------------------- | :------------- |
| Phase 1            | Dashboard            | 30 min         |
| Phase 2            | Planning Stage       | 20 min         |
| Phase 3            | Farming Stage        | 25 min         |
| Phase 4            | Post-Harvest         | 15 min         |
| Phase 5            | Finance              | 30 min         |
| Phase 6            | Collaborative        | 20 min         |
| Phase 7            | Voice (Text)         | 15 min         |
| **TOTAL**          | **Core Integration** | **~2.5 hours** |
| Phase 8 (Optional) | Voice (Audio)        | 45 min         |

---

## 🔄 APPROVAL REQUIRED

**BEFORE PROCEEDING**, please confirm:

✅ **Do you approve this integration plan?**
✅ **Should I start with Phase 1 (Dashboard)?**
✅ **Any specific pages you want prioritized?**
✅ **Should I skip audio recording (Phase 8) for now?**

**Reply with your approval and any changes you'd like!**
