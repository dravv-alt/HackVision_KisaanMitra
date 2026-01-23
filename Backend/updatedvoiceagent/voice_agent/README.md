# Voice Agent - Voice-First Agentic Orchestration Layer

**Last Updated**: 2026-01-23  
**Status**: ✅ Production Ready  
**Version**: 2.0

## Overview

The **Voice Agent** is a voice-first agentic orchestration layer that acts as the "brain" of the farming assistant application. It processes Hindi voice or text input, understands farmer intent using LLM-based classification, retrieves relevant information via RAG, reasons about recommendations, and generates UI-ready cards with bilingual explanations.

## Key Features

- ✅ **Hindi Voice Input Processing** (Whisper STT with FFmpeg)
- ✅ **LLM-Based Intent Classification** (Gemini/Groq - 25+ intents)
- ✅ **RAG-style Information Retrieval** with ChromaDB vector search
- ✅ **Reasoning & Planning** for context-aware recommendations
- ✅ **UI-Ready Card Generation** (Crop, Weather, Market, Scheme, etc.)
- ✅ **Bilingual Explanations** in Hindi and English
- ✅ **MongoDB-Ready Memory** with in-memory fallback
- ✅ **Conversation Context Management** with session tracking
- ✅ **Backend Module Integration** via connectors

## Architecture

```
Hindi Voice/Text Input
         ↓
┌────────────────────────────────────────┐
│ INPUT PROCESSING                        │
│ - Speech-to-Text (Whisper + FFmpeg)   │
│ - Translation (Argos Translate)         │
└────────────┬───────────────────────────┘
             ↓
┌────────────────────────────────────────┐
│ CORE AGENT ORCHESTRATOR                 │
│ - LLM Intent Classification (Gemini)   │
│ - Context Management (Session Memory)  │
└────────────┬───────────────────────────┘
             ↓
┌────────────────────────────────────────┐
│ RETRIEVAL (RAG)                         │
│ - Vector Search (ChromaDB)              │
│ - Live APIs (Weather, Market Prices)   │
│ - Knowledge Sources                     │
└────────────┬───────────────────────────┘
             ↓
┌────────────────────────────────────────┐
│ REASONING & SYNTHESIS                   │
│ - LLM-based Planning                    │
│ - Information Synthesis                 │
│ - Card Generation                       │
└────────────┬───────────────────────────┘
             ↓
┌────────────────────────────────────────┐
│ EXPLANATION GENERATION                  │
│ - Natural Language Output               │
│ - Hindi & English Bilingual            │
│ - Voice-ready Text                      │
└────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- FFmpeg installed (required for Whisper audio processing)
- Gemini or Groq API key in `.env`
- Python 3.13+

### Running the CLI Demo

```bash
cd Backend/voice_agent
python cli_demo.py
```

### Basic Usage

```python
from voice_agent.core import get_voice_agent

# Initialize agent
agent = get_voice_agent()

# Process Hindi text input
response = agent.process_input(
    hindi_text="मेरी फसल में कीड़े लग गए हैं",
    farmer_id="F001"
)

# Access results
print(f"Intent: {response.intent.value}")
print(f"Confidence: {response.intent_confidence}")
print(f"Cards: {len(response.cards)}")
print(f"Explanation (Hindi): {response.explanation_hindi}")
print(f"Reasoning: {response.reasoning}")
```

### API Usage

#### Text Input (JSON)
```bash
curl -X POST http://localhost:8000/api/v1/voice/process \
  -H "Content-Type: application/json" \
  -d '{
    "hindi_text": "प्याज की कीमत क्या है",
    "farmer_id": "F001"
  }'
```

#### Audio Input (Multipart)
```bash
curl -X POST http://localhost:8000/api/v1/voice/process-audio \
  -F "audio=@recording.wav" \
  -F "farmer_id=F001"
```

## Module Structure

```
voice_agent/
├── input_processing/       # STT (Whisper), translation
│   ├── speech_to_text.py  # WhisperSTT class
│   └── translator.py       # Argos Translate wrapper
├── core/                   # Agent orchestration
│   ├── agent.py           # Main VoiceAgent class
│   ├── intent.py          # LLM intent classifier
│   └── context.py         # Conversation context
├── memory/                 # Persistent memory
│   ├── session_memory.py  # Short-term memory
│   └── summary_memory.py  # Long-term summaries
├── retrieval/              # RAG components
│   ├── retriever.py       # Main retriever
│   ├── vector_store.py    # ChromaDB wrapper
│   ├── sources.py         # Knowledge sources
│   ├── weather_service.py # Weather API
│   └── market_service.py  # Market price API
├── reasoning/              # LLM reasoning
│   ├── planner.py         # Reasoning plans
│   └── synthesizer.py     # Information synthesis
├── cards/                  # UI card types
│   ├── base.py
│   ├── crop_card.py
│   ├── weather_card.py
│   ├── market_card.py
│   └── scheme_card.py
├── connectors/             # Backend integrations
│   ├── financial_connector.py
│   ├── inventory_connector.py
│   └── alerts_connector.py
├── explain/                # Explanation generation
│   └── builder.py         # Bilingual explanations
├── config.py              # Configuration management
├── cli_demo.py            # CLI testing tool
└── README.md              # This file
```

## Supported Intents (25+)

### Primary Intents
1. **CROP_PLANNING** - Crop selection and planning
2. **DISEASE_DETECTION** - Disease identification
3. **DISEASE_TREATMENT** - Treatment recommendations
4. **MARKET_PRICE** - Market price queries
5. **WEATHER_QUERY** - Weather information
6. **GOVERNMENT_SCHEME** - Scheme information
7. **FERTILIZER_ADVICE** - Fertilizer recommendations
8. **IRRIGATION_ADVICE** - Irrigation guidance
9. **HARVEST_PLANNING** - Harvest timing
10. **STORAGE_DECISION** - Storage vs sell decisions
11. **MARKET_SELECTION** - Best market selection
12. **FINANCIAL_QUERY** - P&L and expense tracking
13. **EQUIPMENT_RENTAL** - Equipment marketplace
14. **LAND_POOLING** - Collaborative farming

### Support Intents
15. **FOLLOW_UP** - Follow-up questions
16. **CLARIFICATION** - Clarification requests
17. **GREETING** - Greetings
18. **THANKS** - Gratitude
19. **UNKNOWN** - Unknown intent

## Card Types

### CropCard
Crop recommendations with score, reasons, risks, profit level, and seed sources.

### WeatherCard
Weather information with temperature, humidity, rain forecast, wind speed, and advisory.

### MarketCard
Market prices with crop name, current price, trend, demand level, and forecast.

### SchemeCard
Government schemes with eligibility status, reasons, deadlines, and application process.

### DiseaseCard
Disease information with symptoms, treatment, organic alternatives, and safety warnings.

## Configuration

### Environment Variables

Required in `Backend/.env`:

```env
# LLM Provider (Gemini or Groq)
GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# Whisper Model (tiny, base, small, medium, large)
WHISPER_MODEL=base

# MongoDB (optional)
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=farming_assistant

# External APIs (optional)
OPENWEATHER_API_KEY=your_key_here
MANDI_API_KEY=your_key_here
```

### Auto-Configuration

The voice agent automatically:
- Detects LLM provider (Gemini first, then Groq)
- Loads Whisper model from config
- Falls back to in-memory if MongoDB unavailable
- Connects to available external APIs

## MongoDB Integration

Session memory is MongoDB-ready:

```python
from pymongo import MongoClient
from voice_agent.core import get_voice_agent

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client.farming_assistant

# Initialize agent with MongoDB
agent = get_voice_agent(db_client=db)
```

## Example Queries

### Crop Planning
```
Hindi: अब मुझे तय करना है कि कौन सी फसल लगाऊं
English: Now I need to decide which crop to plant
Intent: CROP_PLANNING
```

### Disease Detection
```
Hindi: मेरी फसल में कीड़े लग गए हैं
English: My crop has pests
Intent: DISEASE_DETECTION
```

### Government Schemes
```
Hindi: मुझे सरकारी योजना के बारे में बताओ
English: Tell me about government schemes
Intent: GOVERNMENT_SCHEME
```

### Weather
```
Hindi: आज मौसम कैसा है
English: How is the weather today
Intent: WEATHER_QUERY
```

### Market Prices
```
Hindi: प्याज की कीमत क्या है
English: What is the price of onions
Intent: MARKET_PRICE
```

## Testing

### Predefined Tests
```bash
python cli_demo.py
# Select option 1: Run Predefined Tests
```

### Interactive Mode
```bash
python cli_demo.py
# Select option 2: Interactive Mode
# Enter Hindi queries interactively
```

### Full Integration Test
```bash
python full_integration_demo.py
```

## Technology Stack

- **Python**: 3.13+
- **Speech-to-Text**: OpenAI Whisper (with FFmpeg)
- **Translation**: Argos Translate
- **Intent Detection**: LLM-based (Gemini/Groq)
- **Reasoning**: LLM-based synthesis
- **Vector Search**: ChromaDB
- **Memory**: MongoDB with in-memory fallback
- **API Framework**: FastAPI

## Recent Updates (Jan 2026)

### Major Changes
- ✅ LLM-based intent classification (replacing rule-based)
- ✅ Real Whisper STT with FFmpeg integration
- ✅ Split API endpoints (text vs audio)
- ✅ Enhanced error handling with helpful messages
- ✅ Backend module connectors implemented
- ✅ ChromaDB vector search for RAG

### Bug Fixes
- ✅ FFmpeg dependency check on initialization
- ✅ Fixed imports for FastAPI integration
- ✅ Whisper language code correction (hi-IN → hi)

## Troubleshooting

### FFmpeg Not Found
```bash
# Windows
winget install ffmpeg

# Restart terminal/IDE after installation
```

### LLM API Key Missing
Check `.env` file has `GEMINI_API_KEY` or `GROQ_API_KEY`

### MongoDB Connection Fails
System automatically falls back to in-memory storage

## Notes

- **Language**: Hindi input → English processing → Bilingual output
- **Explainability**: Every decision includes clear reasoning
- **LLM-Powered**: No more rule-based heuristics
- **Voice-Ready**: All outputs optimized for text-to-speech
- **MongoDB-Ready**: Easy production deployment

---

**Status**: Production Ready  
**Version**: 2.0  
**Built For**: Indian Farmers
