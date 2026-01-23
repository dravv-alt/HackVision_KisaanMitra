# KisaanMitra Backend - Codebase Documentation Index

**Last Updated**: 2026-01-23  
**Status**: Production Ready (v1.0)

---

## 📋 Documentation Overview

This directory contains comprehensive documentation for the KisaanMitra backend system. The documentation is split into logical modules for easier navigation.

### Documentation Files

1. **[Farm Management Documentation](./1_farm_management_documentation.md)**
   - Pre-Seeding Planning Stage
   - Farming Stage (Disease Detection, Market Prices)
   - Post-Harvest Stage
   - Models and engines

2. **[Voice Agent Documentation](./2_voice_agent_documentation.md)**
   - Voice-first conversational AI
   - Speech-to-Text (Whisper)
   - Intent Classification
   - Translation (Hindi ↔ English)
   - LangGraph orchestration

3. **[Government Schemes, Financial & Collaborative Documentation](./3_gov_schemes_financial_collaborative_documentation.md)**
   - Government schemes API
   - Financial tracking
   - Collaborative farming (equipment rental, land pooling)

---

## 🚀 Quick Start

### Running the Backend

```bash
cd Backend

# Option 1: Using Python module
python -m api.main

# Option 2: Using uvicorn directly (recommended)
uvicorn api.main:app --reload
```

Server will start at: **http://localhost:8000**

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 🏗️ Project Structure

```
Backend/
├── api/                          # FastAPI application
│   ├── main.py                   # Main FastAPI app
│   ├── config.py                 # API configuration
│   ├── dependencies.py           # Shared dependencies
│   └── routers/                  # API route handlers
│       ├── farm_management.py
│       ├── voice_agent.py
│       ├── gov_schemes.py
│       ├── financial.py
│       └── collaborative.py
│
├── farm_management/              # Farm management modules
│   ├── planning_stage/           # Pre-seeding planning
│   ├── farming_stage/            # Disease detection, prices
│   └── post_harvest_stage/       # Storage & market selection
│
├── voice_agent/                  # Voice-first AI agent
│   ├── core/                     # Agent orchestration
│   ├── input_processing/         # STT & translation
│   ├── reasoning/                # Planning & synthesis
│   ├── retrieval/                # Data retrieval
│   └── connectors/               # Module integrations
│
├── government_schemes/           # Scheme database & API
├── financial_tracking/           # Expense/income tracking
├── collaborative_farming/        # Equipment & land sharing
│
└── codebase_docs/               # This directory
    ├── README_Codebase_index.md
    ├── 1_farm_management_documentation.md
    ├── 2_voice_agent_documentation.md
    └── 3_gov_schemes_financial_collaborative_documentation.md
```

---

## 🔑 Key Technologies

- **FastAPI**: Modern async Python web framework
- **Pydantic**: Data validation and settings management
- **TensorFlow**: Disease detection CNN model
- **Whisper**: OpenAI speech-to-text (requires FFmpeg)
- **LangGraph**: Agent orchestration framework
- **Gemini/Groq**: LLM providers for intent & reasoning
- **MongoDB**: Optional database (falls back to in-memory)

---

## 📊 API Endpoints Summary

### Farm Management
- `POST /api/v1/planning/pre-seeding` - Crop recommendations
- `GET /api/v1/farming/market-price` - Market prices
- `POST /api/v1/farming/disease-detect` - Disease detection (image upload)
- `POST /api/v1/post-harvest/plan` - Post-harvest planning

### Voice Agent
- `POST /api/v1/voice/process` - Process text input (JSON)
- `POST /api/v1/voice/process-audio` - Process audio input (multipart)

### Government Schemes
- `GET /api/v1/schemes` - List all schemes
- `POST /api/v1/schemes/filter` - Filter schemes

### Financial Tracking
- `GET /api/v1/finance/summary` - Financial summary
- `POST /api/v1/finance/expense` - Add expense
- `POST /api/v1/finance/income` - Add income

### Collaborative Farming
- `GET /api/v1/collaborative/equipment` - List equipment
- `GET /api/v1/collaborative/land-pooling` - Land pooling opportunities

---

## ✅ Recent Updates (Jan 2026)

### Major Changes
1. **FastAPI Integration**: Unified all modules under single API server
2. **Vision AI Cleanup**: Removed external API dependencies, using local model only
3. **Validation Improvements**: Better error messages with examples
4. **Voice Agent Enhancement**: Split into text and audio endpoints
5. **FFmpeg Integration**: Added system checks for Whisper dependencies

### Bug Fixes
- Fixed MarketEngine method naming (`get_prices` → `get_market_data`)
- Fixed post-harvest location validation with clear lat/lon guidance
- Fixed pre-seeding farmer lookup with helpful test ID suggestions
- Fixed VisionEngine to fail explicitly instead of returning mock data

### Dependencies
- Added `openai-whisper` for speech-to-text
- Requires FFmpeg installed on system (Windows: `winget install ffmpeg`)
- TensorFlow 2.20+ (Python 3.13 compatible)

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in `Backend/` directory:

```env
# LLM Provider (Gemini or Groq)
GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# Whisper Model
WHISPER_MODEL=base

# MongoDB (optional)
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=farming_assistant

# APIs
OPENWEATHER_API_KEY=your_key_here
MANDI_API_KEY=your_key_here
```

---

## 🧪 Testing

### Manual Testing

Use the provided test scripts:
```bash
python test_features_simple.py
```

Or test individual endpoints:
```bash
# Health check
curl http://localhost:8000/health

# Voice agent
curl -X POST http://localhost:8000/api/v1/voice/process \
  -H "Content-Type: application/json" \
  -d '{"hindi_text": "meri fasal", "farmer_id": "F001"}'

# Market price
curl "http://localhost:8000/api/v1/farming/market-price?crop=Onion"
```

---

## 📝 Common Issues & Solutions

### Issue: FFmpeg Not Found
**Error**: `"FFmpeg not found. Whisper requires FFmpeg..."`
**Solution**: 
```bash
winget install ffmpeg
# Then restart your terminal/server
```

### Issue: Farmer Not Found
**Error**: `"Farmer not found: xyz"`
**Solution**: Use test farmer IDs: `F001`, `F002`, `F003`, or `F004`

### Issue: Invalid Location Format
**Error**: `"farmer_location must be [latitude, longitude]"`
**Solution**: Use numeric coordinates: `[19.9975, 73.7898]`

### Issue: TensorFlow Model Loading
**Error**: Model fails to load
**Current Status**: Known issue - model trained on older TensorFlow version
**Workaround**: Disease detection endpoint disabled until model retrained

---

## 👥 Support & Contribution

For detailed module-specific documentation, see:
- Farm Management: `1_farm_management_documentation.md`
- Voice Agent: `2_voice_agent_documentation.md`
- Other Modules: `3_gov_schemes_financial_collaborative_documentation.md`

---

**Built with ❤️ for Indian Farmers**
