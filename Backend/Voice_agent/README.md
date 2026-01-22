# Voice Agent - Voice-First Agentic Orchestration Layer

## Overview

The **Voice Agent** is a voice-first agentic orchestration layer that acts as the pilot of the farming assistant application. It processes Hindi voice input, understands farmer intent, retrieves relevant information, reasons about recommendations, and generates UI-ready cards with simple explanations.

## Key Features

- ✅ **Hindi Voice Input Processing** (mocked as text in CLI)
- ✅ **Rule-based Intent Detection** (12 intents)
- ✅ **RAG-style Information Retrieval** from knowledge sources
- ✅ **Reasoning & Planning** for recommendations
- ✅ **UI-Ready Card Generation** (Crop, Weather, Market, Scheme)
- ✅ **Simple Explanations** in Hindi and English
- ✅ **MongoDB-Ready Memory** with in-memory fallback
- ✅ **Conversation Context Management**
- ✅ **CLI Demo** for manual testing

## Architecture

```
Hindi Voice Input (Text in CLI)
         ↓
┌────────────────────────────────────────┐
│ INPUT PROCESSING                        │
│ - Speech-to-Text (mocked)              │
│ - Translation (Hindi ↔ English)        │
└────────────┬───────────────────────────┘
             ↓
┌────────────────────────────────────────┐
│ CORE AGENT                              │
│ - Intent Detection (Rule-based)        │
│ - Context Management                    │
└────────────┬───────────────────────────┘
             ↓
┌────────────────────────────────────────┐
│ RETRIEVAL (RAG-style)                   │
│ - Knowledge Sources                     │
│ - Keyword Filtering                     │
└────────────┬───────────────────────────┘
             ↓
┌────────────────────────────────────────┐
│ REASONING & PLANNING                    │
│ - Reasoning Plans                       │
│ - Information Synthesis                 │
└────────────┬───────────────────────────┘
             ↓
┌────────────────────────────────────────┐
│ CARD GENERATION                         │
│ - Crop, Weather, Market, Scheme Cards  │
└────────────┬───────────────────────────┘
             ↓
┌────────────────────────────────────────┐
│ EXPLANATION GENERATION                  │
│ - Simple, Spoken-style Language        │
│ - Hindi Translation                     │
└────────────────────────────────────────┘
```

## Quick Start

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

# Process Hindi input
response = agent.process_input(
    hindi_text="अब मुझे तय करना है कि कौन सी फसल लगाऊं",
    farmer_id="F001"
)

# Access results
print(f"Intent: {response.intent.value}")
print(f"Cards: {len(response.cards)}")
print(f"Explanation (Hindi): {response.explanation_hindi}")
```

## Module Structure

```
voice_agent/
├── input_processing/       # Speech-to-text, translation
├── core/                   # Agent, intent, context
├── memory/                 # Session & summary memory
├── retrieval/              # RAG-style retrieval
├── reasoning/              # Planning & synthesis
├── cards/                  # UI-ready card types
├── actions/                # Action routing (placeholder)
├── explain/                # Explanation generation
├── cli_demo.py            # Manual testing CLI
└── README.md              # This file
```

## Supported Intents

1. **CROP_PLANNING** - Crop selection and planning
2. **STORAGE_DECISION** - Storage decision making
3. **SELLING_DECISION** - Selling and market decision
4. **GOVERNMENT_SCHEME** - Government scheme information
5. **IRRIGATION_ADVICE** - Irrigation guidance
6. **DISEASE_TREATMENT** - Disease treatment advice
7. **FERTILIZER_ADVICE** - Fertilizer recommendations
8. **HARVEST_PLANNING** - Harvest timing planning
9. **WEATHER_QUERY** - Weather information
10. **MARKET_PRICE** - Market price information
11. **FOLLOW_UP** - Follow-up questions
12. **UNKNOWN** - Unknown intent

## Card Types

### CropCard
Crop recommendations with score, reasons, risks, and profit level.

### WeatherCard
Weather information with temperature, humidity, rain forecast, and advisory.

### MarketCard
Market prices with crop name, price, trend, and market name.

### SchemeCard
Government schemes with eligibility status, reasons, and deadline.

## MongoDB Integration

The session memory is MongoDB-ready:

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
```

### Government Schemes
```
Hindi: मुझे सरकारी योजना के बारे में बताओ
English: Tell me about government schemes
```

### Weather
```
Hindi: आज मौसम कैसा है
English: How is the weather today
```

### Market Prices
```
Hindi: गेहूं की कीमत क्या है
English: What is the price of wheat
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

## Technology Stack

- **Python**: 3.10+
- **Speech-to-Text**: Mocked (Whisper abstraction ready)
- **Translation**: Simple dictionary-based (Hindi ↔ English)
- **Intent Detection**: Rule-based keyword matching
- **Reasoning**: Pure Python logic
- **RAG**: Keyword filtering with mock knowledge sources
- **Memory**: MongoDB-ready with in-memory fallback

## Future Enhancements

- [ ] Integrate actual Whisper for speech-to-text
- [ ] Use Argos Translate for better translation
- [ ] Add LLM integration (Groq/Gemini) for reasoning
- [ ] Integrate with Farm Management backend modules
- [ ] Add LangChain for advanced orchestration
- [ ] Implement action routing and confirmations
- [ ] Add vector search with FAISS
- [ ] Enhance knowledge sources with real data

## Notes

- **Language**: Hindi input, English internal processing, Hindi output
- **Explainability**: Every decision has clear reasoning
- **Deterministic**: Uses retrieved facts, no hallucinations
- **CLI-First**: Working CLI demo for testing
- **MongoDB-Ready**: Easy to connect when database is available

---

**Status**: Production-Ready Demo Code  
**Version**: 1.0.0  
**Built For**: 24-Hour Hackathon
