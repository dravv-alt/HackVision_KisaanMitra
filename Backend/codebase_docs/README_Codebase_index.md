# KisaanMitra Backend - Complete Codebase Documentation Index

## Overview

This directory contains comprehensive documentation for the KisaanMitra backend system, designed to provide full context for API endpoint development and system understanding.

## Documentation Structure

### 1. Farm Management Module
**File**: [`1_farm_management_documentation.md`](./1_farm_management_documentation.md)

**Covers**:
- **Planning Stage** (Pre-Seeding): Crop recommendations, government schemes, weather integration, reminders
- **Farming Stage** (Cultivation): Disease detection (AI vision), pest/disease knowledge, market prices, weather guidance
- **Post-Harvest Stage** (Marketing): Market selection, storage decisions, spoilage modeling, profit optimization

**Key Components**:
- 20+ Pydantic models for type-safe data handling
- 12+ engines for business logic (crop scoring, scheme eligibility, price forecasting, etc.)
- 12+ repositories for data access (MongoDB-ready with mock fallback)
- 3 main service orchestrators

**Total Coverage**: ~50 files, 15+ significant functions

---

### 2. Voice Agent Module
**File**: [`2_voice_agent_documentation.md`](./2_voice_agent_documentation.md)

**Covers**:
- **Core Orchestration**: Main agent coordinator
- **Intent Classification**: LLM-based intent detection (25+ intents) using Groq/Gemini
- **RAG Retrieval**: Vector DB (ChromaDB) + live APIs (weather, market)
- **Reasoning**: Intent-specific planning and synthesis
- **Memory Management**: Session memory (short-term) + summary memory (long-term)
- **Response Cards**: Structured data containers (CropCard, SchemeCard, MarketCard, etc.)
- **Backend Connectors**: Integration with all backend modules
- **Input Processing**: Speech-to-text, translation

**Key Components**:
- Intent classifier with 25+ supported intents
- Vector store with semantic search
- Session memory (MongoDB-ready)
- 6+ card types for structured responses
- 4+ connectors for backend integration
- Bilingual explanation builder (Hindi/English)

**Total Coverage**: ~40 files, 10+ significant functions

---

### 3. Government Schemes, Financial Tracking & Collaborative Farming Modules
**File**: [`3_gov_schemes_financial_collaborative_documentation.md`](./3_gov_schemes_financial_collaborative_documentation.md)

#### Government Schemes Module
**Covers**:
- Scheme fetching from external APIs with 24-hour caching
- Location-based filtering (state, district, category)
- New scheme detection and alert generation
- Multilingual scheme cards

**Key Components**:
- 4 engines (fetch, filter, alert, response builder)
- 5 repositories (schemes, farmer, API client, alerts, audit)
- Alert system for new schemes and deadlines

#### Financial Tracking Module
**Covers**:
- Transaction ledger (expense/income tracking)
- Profit/loss calculation
- Loss cause analysis
- Cost optimization suggestions

**Key Components**:
- 5 engines (ledger, P&L, loss analysis, optimization, response builder)
- 3 repositories (transactions, summaries, crop metadata)
- 8+ expense categories, 3+ income categories

#### Collaborative Farming Module
**Covers**:
- Equipment rental marketplace
- Land pooling for joint farming/bulk selling
- Residue management marketplace
- Rental deadline reminders

**Key Components**:
- 6 engines (equipment, rental, land pool, residue, reminder, response builder)
- 7 repositories (equipment, rental, land pool, residue, farmer, alerts, audit)
- Complete rental lifecycle management

**Total Coverage**: ~50 files across three modules, 15+ significant functions

---

## Module Interaction Map

```
┌─────────────────────────────────────────────────────────────────┐
│                         Voice Agent                             │
│  (Central Orchestrator - Hindi/English Voice-First Interface)  │
└─────────────────┬───────────────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┬───────────────┬──────────────┐
    │             │             │               │              │
    v             v             v               v              v
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Farm   │  │   Gov    │  │Financial │  │Collabora-│  │ Alerts & │
│Manage-  │  │ Schemes  │  │ Tracking │  │  tive    │  │Inventory │
│  ment   │  │          │  │          │  │ Farming  │  │          │
└─────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
│            │            │            │            │
├─Planning   ├─Fetch API  ├─Ledger     ├─Equipment  ├─Alerts
├─Farming    ├─Filter     ├─P&L Report ├─Rental     ├─Reminders
└─Post-      ├─Alerts     ├─Loss       ├─Land Pool  └─Inventory
  Harvest    └─Response   │  Analysis  └─Residue
                          └─Optimize
```

---

## Quick Reference by Use Case

### For Building API Endpoints

**Crop Planning API**:
- Module: `farm_management.planning_stage`
- Entry Point: `PreSeedingService.run(PlanningRequest)`
- Returns: `PreSeedingOutput` with crop cards, scheme cards, reminders
- Documentation: Section 1 of doc #1

**Disease Diagnosis API**:
- Module: `farm_management.farming_stage`
- Entry Point: `VisionEngine.detect_disease(image_path)`
- Returns: `DiseaseDetectionResult` with disease name, confidence, treatment
- Documentation: Section 2 of doc #1

**Post-Harvest Planning API**:
- Module: `farm_management.post_harvest_stage`
- Entry Point: `PostHarvestEngine.plan(HarvestContext)`
- Returns: `PostHarvestPlan` with market options, storage advice
- Documentation: Section 3 of doc #1

**Voice Interaction API**:
- Module: `voice_agent`
- Entry Point: `VoiceAgent.process_input(hindi_text, farmer_id, session_id)`
- Returns: `AgentResponse` with cards, explanations, reasoning
- Documentation: Doc #2

**Government Schemes API**:
- Module: `gov_schemes`
- Entry Point: `GovSchemesDisplayService.get_schemes_display(farmer_id)`
- Returns: `GovSchemesOutput` with scheme cards, alerts
- Documentation: Section 1 of doc #3

**Financial Report API**:
- Module: `financial_tracking`
- Entry Point: `FinanceTrackingService.run_finance_report(farmer_id, season)`
- Returns: `FinanceModuleOutput` with P&L, suggestions
- Documentation: Section 2 of doc #3

**Collaborative Marketplace API**:
- Module: `collaborative_farming`
- Entry Point: `CollaborativeFarmingService.run_marketplace_view(farmer_id)`
- Returns: `CollaborativeOutput` with equipment, rentals, land pools
- Documentation: Section 3 of doc #3

---

## Data Flow Patterns

### Input → Processing → Output

All modules follow this pattern:

1. **Input**: Pydantic request models (type-safe)
2. **Processing**: 
   - Service orchestrates engines
   - Engines handle business logic
   - Repositories manage data access
3. **Output**: Pydantic output models with:
   - Structured cards (for UI)
   - Speech text (for TTS)
   - Detailed reasoning (for debugging)

### Common Output Structure

```python
class ModuleOutput(BaseModel):
    header: str                  # Title
    language: Language           # hi/en
    speechText: str              # Voice-ready summary
    cards: List[Card]            # Structured data
    detailedReasoning: str       # Full explanation
    urgencyLevel: UrgencyLevel   # LOW/MEDIUM/HIGH/CRITICAL
```

---

## Technology Stack

**Backend**:
- **Language**: Python 3.11+
- **Web Framework**: FastAPI (recommended)
- **Data Validation**: Pydantic
- **Database**: MongoDB (with in-memory fallback)
- **Vector DB**: ChromaDB (for RAG)
- **LLM Providers**: Groq (Mixtral/Llama3), Gemini (1.5 Flash/Pro)

**External APIs**:
- OpenWeather API (weather data)
- Government scheme portals (scheme data)
- Agmarknet (market prices, future scope)

**AI/ML**:
- TensorFlow/Keras (plant disease detection)
- Sentence-Transformers (embeddings for vector search)
- Groq/Gemini (intent classification, response generation)

---

## Key Design Principles

1. **Voice-First**: Every output includes `speechText` for TTS
2. **Bilingual**: Hindi/English support throughout
3. **Modular**: Clear separation of concerns (service → engine → repository)
4. **Type-Safe**: Pydantic models everywhere
5. **Mock-Ready**: All repositories have in-memory fallback for demos
6. **MongoDB-Ready**: Easy transition from mock to production DB
7. **RAG-Enabled**: Vector search for semantic information retrieval
8. **Card-Based**: Structured responses for UI consumption

---

## File Count by Module

| Module                | Python Files | Models  | Engines | Repositories | Services |
| --------------------- | ------------ | ------- | ------- | ------------ | -------- |
| farm_management       | ~50          | 20+     | 12+     | 12+          | 3        |
| voice_agent           | ~40          | 10+     | 5+      | 3+           | 1        |
| gov_schemes           | ~18          | 6       | 4       | 5            | 1        |
| financial_tracking    | ~15          | 7       | 5       | 3            | 1        |
| collaborative_farming | ~20          | 8       | 6       | 7            | 1        |
| **TOTAL**             | **~143**     | **51+** | **32+** | **30+**      | **7**    |

---

## Significant Functions by Module

### Farm Management (Top 10)
1. `PreSeedingService.run()` - Complete pre-seeding workflow
2. `CropRecommendationEngine.recommend()` - Multi-factor crop scoring
3. `SchemeEngine.check_eligibility()` - Scheme eligibility logic
4. `WeatherEngine.get_context()` - Weather data with fallback
5. `PostHarvestEngine.plan()` - Post-harvest optimization
6. `MarketSelector.select_best_markets()` - Profit-based market selection
7. `StorageDecisionEngine.evaluate_storage()` - Store vs sell analysis
8. `SpoilageModel.predict_spoilage()` - Spoilage forecasting
9. `VisionEngine.detect_disease()` - AI disease detection
10. `KnowledgeEngine.get_disease_info()` - Pest/disease knowledge retrieval

### Voice Agent (Top 10)
1. `VoiceAgent.process_input()` - Main orchestration
2. `LLMIntentClassifier.classify()` - LLM-based intent detection
3. `Retriever.retrieve()` - RAG information retrieval
4. `Synthesizer.synthesize()` - Card generation
5. `ExplanationBuilder.build_explanation()` - Natural language generation
6. `SessionMemory.save_context()` - Conversation persistence
7. `VectorStore.search()` - Semantic search
8. `SpeechToText.transcribe()` - Audio to text
9. `Translator.translate_to_hindi()` - Translation
10. `FinancialConnector.get_profit_loss_summary()` - Backend integration

### Gov Schemes (Top 5)
1. `GovSchemesDisplayService.get_schemes_display()` - Main orchestration
2. `SchemeFetchEngine.sync_schemes()` - API sync with caching
3. `SchemeFilterEngine.filter_by_location()` - Location filtering
4. `SchemeAlertEngine.detect_new_schemes()` - New scheme detection
5. `SchemeAlertEngine.generate_alerts_for_farmer()` - Alert generation

### Financial Tracking (Top 5)
1. `FinanceTrackingService.run_finance_report()` - Complete P&L report
2. `ProfitLossEngine.calculate()` - P&L calculation
3. `LossAnalysisEngine.analyze()` - Loss cause identification
4. `OptimizationEngine.suggest()` - Cost-saving suggestions
5. `FinanceTrackingService.add_expense()` - Record transaction

### Collaborative Farming (Top 5)
1. `CollaborativeFarmingService.run_marketplace_view()` - Marketplace dashboard
2. `EquipmentEngine.list_available_equipment()` - Equipment search
3. `RentalEngine.request_booking()` - Rental booking
4. `LandPoolEngine.find_matching_requests()` - Land pool matching
5. `ReminderEngine.generate_rental_return_reminders()` - Deadline reminders

---

## Testing & Validation

Each module includes:
- **CLI Demo**: Interactive command-line testing
- **Mock Data**: Comprehensive test data for all models
- **Unit Tests**: Test runners for engines and repositories

**Demo Commands**:
```bash
# Farm Management
python farm_management/planning_stage/cli_demo.py
python farm_management/farming_stage/main_driver.py
python farm_management/post_harvest_stage/cli_demo.py

# Voice Agent
python voice_agent/cli_demo.py
python voice_agent/full_integration_demo.py

# Other Modules
python gov_schemes/cli_demo.py
python financial_tracking/cli_demo.py
python collaborative_farming/cli_demo.py
```

---

## Next Steps for API Development

1. **Read Module Documentation**: Start with the specific module docs
2. **Understand Data Models**: Review Pydantic models in `models.py` files
3. **Identify Entry Points**: Look for main service methods (e.g., `run()`, `get_schemes_display()`)
4. **Create FastAPI Endpoints**: Wrap service calls in REST endpoints
5. **Handle Errors**: Add try-except blocks and return appropriate HTTP status codes
6. **Add Authentication**: Integrate farmer_id from JWT tokens
7. **Test with Mock Data**: Use CLI demos as reference
8. **Connect to MongoDB**: Replace in-memory repos with real DB connections
9. **Deploy**: Set up environment variables from `.env` files

---

## Support & Contact

For questions about this documentation:
- Review the detailed module docs
- Check the code inline comments
- Test with CLI demos
- Refer to the README files in each module

**Documentation Created**: January 2026  
**Version**: 1.0  
**Coverage**: 100% of backend modules (5/5 modules documented)
