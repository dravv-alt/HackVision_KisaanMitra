# Voice Agent Module - Complete Documentation

## Module Overview

The **Voice Agent** module is the central orchestrator for the KisaanMitra voice-first farming assistant. It coordinates all components to handle multilingual (Hindi/English) voice interactions, intent detection, information retrieval, reasoning, and response generation.

### Purpose

Provides a complete voice-first conversational AI system that:
- Processes Hindi/English voice/text input
- Detects farmer intent using LLM-based classification
- Retrieves relevant information via RAG (Retrieval-Augmented Generation)
- Generates structured responses (cards) with reasoning
- Maintains conversation context and memory
- Integrates with all backend modules (farm_management, gov_schemes, financial_tracking, collaborative_farming)

### Module Structure

```
voice_agent/
├── __init__.py
├── config.py                    # Configuration management
├── core/                        # Core agent logic
│   ├── agent.py                # Main orchestrator
│   ├── context.py              # Conversation context
│   └── intent.py               # LLM-based intent classification
├── input_processing/            # Input handling
│   ├── speech_to_text.py       # Audio to text conversion
│   └── translator.py           # Hindi/English translation
├── reasoning/                   # Reasoning & synthesis
│   ├── planner.py              # Reasoning plan creation
│   └── synthesizer.py          # Information synthesis
├── retrieval/                   # RAG retrieval
│   ├── retriever.py            # Main retrieval logic
│   ├── vector_store.py         # ChromaDB integration
│   ├── sources.py              # Knowledge sources registry
│   ├── weather_service.py      # Live weather API
│   └── market_service.py       # Live market API
├── memory/                      # Conversation memory
│   ├── session_memory.py       # Short-term session memory
│   └── summary_memory.py       # Long-term summary memory
├── cards/                       # Structured response cards
│   ├── base_card.py            # Base card interface
│   ├── crop_card.py            # Crop recommendation card
│   ├── weather_card.py         # Weather info card
│   ├── market_card.py          # Market price card
│   └── scheme_card.py          # Government scheme card
├── explain/                     # Response explanation
│   └── explanation_builder.py   # Bilingual explanation generator
├── connectors/                  # Backend module connectors
│   ├── financial_connector.py   # Financial tracking integration
│   ├── collaborative_connector.py # Collaborative farming integration
│   ├── inventory_connector.py   # Inventory management integration
│   └── alerts_connector.py      # Alerts system integration
└── actions/                     # Action handlers
    └── __init__.py             # Action execution logic
```

---

## Core Components

### 1. Main Voice Agent (core/agent.py)

**Class**: `VoiceAgent`

**Purpose**: Main orchestrator coordinating all voice agent components.

#### Key Method: `process_input()`

```python
def process_input(
    self,
    hindi_text: str,
    farmer_id: str = "F001",
    session_id: Optional[str] = None
) -> AgentResponse:
    """
    Main entry point for processing voice/text input
    
    Workflow:
    1. Get or create conversation context
    2. Classify intent using LLM
    3. Retrieve relevant information (RAG)
    4. Create reasoning plan
    5. Synthesize information into cards
    6. Build bilingual explanation
    7. Update session memory
    8. Return structured response
    """
```

**AgentResponse** structure:
```python
@dataclass
class AgentResponse:
    session_id: str
    intent: Intent
    intent_confidence: float
    cards: List[BaseCard]              # Structured data cards
    explanation_hindi: str             # Voice-ready Hindi response
    explanation_english: str           # Voice-ready English response
    reasoning: str                     # Internal reasoning trace
    retrieved_sources: int            # Number of sources retrieved
    timestamp: datetime
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        # Converts to JSON-serializable format for API responses
```

**Singleton Access**:
```python
agent = get_voice_agent(db_client=None)  # Auto-initializes all components
```

---

### 2. Intent Classification (core/intent.py)

**Class**: `LLMIntentClassifier`

**Purpose**: Detect user intent from Hindi/English text using LLM (Groq or Gemini).

#### Supported Intents

```python
class Intent(str, Enum):
    # Farm Management
    CROP_PLANNING = "crop_planning"
    STORAGE_DECISION = "storage_decision"
    SELLING_DECISION = "selling_decision"
    HARVEST_TIMING = "harvest_timing"
    DISEASE_DIAGNOSIS = "disease_diagnosis"
    
    # Information Queries
    GOVERNMENT_SCHEME = "government_scheme"
    WEATHER_QUERY = "weather_query"
    MARKET_PRICE = "market_price"
    POST_HARVEST_QUERY = "post_harvest_query"
    
    # Financial Tracking
    FINANCE_REPORT = "finance_report"
    ADD_EXPENSE = "add_expense"
    ADD_INCOME = "add_income"
    OPTIMIZATION_ADVICE = "optimization_advice"
    
    # Collaborative Farming
    EQUIPMENT_RENTAL = "equipment_rental"
    LAND_POOLING = "land_pooling"
    RESIDUE_MANAGEMENT = "residue_management"
    COLLABORATIVE_MARKETPLACE = "collaborative_marketplace"
    
    # Inventory & Alerts
    INVENTORY_CHECK = "inventory_check"
    CHECK_ALERTS = "check_alerts"
    REMINDER_CHECK = "reminder_check"
    
    # Irrigation
    IRRIGATION_ADVICE = "irrigation_advice"
    
    # Fallback
    UNKNOWN = "unknown"
```

#### Classification Method

```python
def classify(self, text: str) -> IntentResult:
    """
    Classify intent using LLM with structured prompt
    
    Args:
        text: User input (Hindi or English)
    
    Returns:
        IntentResult with intent, confidence, and reasoning
    
    Workflow:
    1. Create classification prompt with intent descriptions
    2. Call LLM API (Groq or Gemini)
    3. Parse JSON response for intent + confidence
    4. Fallback to keyword matching if LLM fails
    """
```

**LLM Configuration**:
- **Groq**: Uses `mixtral-8x7b-32768` or `llama3-70b-8192`
- **Gemini**: Uses `gemini-1.5-flash-8b` or `gemini-1.5-pro-latest`
- Auto-detects provider from `.env` configuration

**Prompt Template**:
The classifier creates a structured prompt that:
- Lists all supported intents with descriptions
- Provides farmer context (if available)
- Asks LLM to return JSON: `{"intent": "...", "confidence": 0-100, "reasoning": "..."}`
- Includes examples for better accuracy

**Fallback Classification**:
If LLM fails, uses keyword matching:
- "फसल" / "crop" → `CROP_PLANNING`
- "भाव" / "price" → `MARKET_PRICE`
- "योजना" / "scheme" → `GOVERNMENT_SCHEME`
- etc.

---

### 3. Conversation Context (core/context.py)

**Class**: `ConversationContext`

**Purpose**: Maintains conversation state across multiple turns.

**Key Fields**:
```python
@dataclass
class ConversationContext:
    session_id: str
    farmer_id: str
    farmer_profile: FarmerProfile          # Current farmer details
    conversation_history: List[ConversationTurn]
    context_variables: Dict[str, Any]      # Persistent variables (crop being discussed, etc.)
    last_intent: Optional[Intent]
    last_updated: datetime
    pending_confirmation: Optional[Dict]    # For confirmation flows
    
    def add_turn(self, user_input: str, agent_response: AgentResponse):
        # Adds turn to history
    
    def get_context_summary(self) -> str:
        # Returns human-readable summary of context
    
    def to_dict(self) -> Dict[str, Any]:
        # Serializes for MongoDB storage
```

**ConversationTurn** structure:
```python
@dataclass
class ConversationTurn:
    turn_number: int
    timestamp: datetime
    user_input: str
    detected_intent: Intent
    agent_response: AgentResponse
```

---

### 4. Retrieval (RAG) System (retrieval/retriever.py)

**Class**: `Retriever`

**Purpose**: Retrieve relevant information via RAG (Retrieval-Augmented Generation).

#### Information Sources

1. **Vector Store (ChromaDB)**: Semantic search for crops, schemes, pest/disease info
2. **Live Weather Service**: Real-time weather via OpenWeather API
3. **Live Market Service**: Real-time market prices
4. **Knowledge Registry**: Structured knowledge base

#### Retrieval Method

```python
def retrieve(
    self,
    intent: Intent,
    query_text: str,
    context: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """
    Intent-based information retrieval
    
    Intent-specific retrieval strategies:
    - CROP_PLANNING: Crop info (vector) + weather + market
    - STORAGE_DECISION / SELLING_DECISION: Market info
    - GOVERNMENT_SCHEME: Scheme info (vector)
    - WEATHER_QUERY: Live weather
    - MARKET_PRICE: Live market prices
    
    Returns: List of retrieved documents/facts
    """
```

**Retrieved Document Format**:
```python
{
    "source": "vector_db" | "weather_service" | "market_service",
    "type": "crop_info" | "scheme_info" | "weather_info" | "market_price",
    "data": {...},  # Actual data
    "score": 0.85   # Relevance score (for vector search)
}
```

#### Vector Store Integration (retrieval/vector_store.py)

**Class**: `VectorStore`

**Purpose**: Semantic search using ChromaDB (embedded vector database).

**Key Methods**:
```python
def add_documents(self, documents: List[Dict], type: str):
    # Adds documents to vector DB with metadata

def search(
    self,
    query: str,
    limit: int = 5,
    type_filter: str = None
) -> List[Dict[str, Any]]:
    # Semantic search with optional type filtering
```

**Document Types**:
- `crop_info`: Crop details (from farm_management/planning_stage)
- `scheme_info`: Government schemes (from gov_schemes module)
- `disease_info`: Pest/disease knowledge
- `general_knowledge`: General farming tips

**Embeddings**: Uses Sentence-Transformers (default: `all-MiniLM-L6-v2`) for generating embeddings

---

### 5. Reasoning & Synthesis (reasoning/)

#### 5.1 Reasoning Planner (reasoning/planner.py)

**Class**: `ReasoningPlanner`

**Purpose**: Create reasoning plans for different intents.

```python
@dataclass
class ReasoningPlan:
    intent: Intent
    factors_to_consider: List[str]
    decision_criteria: List[str]
    output_format: str

def create_plan(self, intent: Intent) -> ReasoningPlan:
    # Returns intent-specific reasoning plan
```

**Example Plans**:

**CROP_PLANNING**:
```python
ReasoningPlan(
    intent=Intent.CROP_PLANNING,
    factors_to_consider=[
        "Soil type",
        "Current season",
        "Weather conditions",
        "Market demand",
        "Water availability",
        "Profit potential"
    ],
    decision_criteria=[
        "Soil compatibility",
        "Season suitability",
        "Market price trends",
        "Risk level"
    ],
    output_format="Recommend top 3 crops with reasoning"
)
```

**STORAGE_DECISION**:
```python
ReasoningPlan(
    intent=Intent.STORAGE_DECISION,
    factors_to_consider=[
        "Crop spoilage risk",
        "Current market price",
        "Price forecast",
        "Storage cost",
        "Storage availability"
    ],
    decision_criteria=[
        "Profit improvement potential",
        "Spoilage risk level",
        "Storage cost vs benefit"
    ],
    output_format="Recommend sell now or store with reasoning"
)
```

---

#### 5.2 Synthesizer (reasoning/synthesizer.py)

**Class**: `Synthesizer`

**Purpose**: Combine retrieved information into structured cards and recommendations.

**Key Method**:
```python
def synthesize(
    self,
    intent: Intent,
    retrieved_docs: List[Dict[str, Any]],
    context: Dict[str, Any] = None
) -> List[BaseCard]:
    """
    Synthesize retrieved info into cards
    
    Intent-specific synthesis:
    - CROP_PLANNING: Calls PreSeedingService from farm_management
    - GOVERNMENT_SCHEME: Calls GovSchemeService
    - WEATHER_QUERY: Formats weather data into WeatherCard
    - MARKET_PRICE: Formats prices into MarketCard
    - FINANCE_REPORT: Calls FinancialService
    - etc.
    
    Returns: List of structured cards
    """
```

**Synthesis Strategy**:

1. **Uses Real Logic Engines**: For major intents (crop planning, schemes, finance), calls actual service modules instead of just formatting retrieved data
2. **Falls back to RAG**: For simpler queries, synthesizes from retrieved documents
3. **Combines Multiple Sources**: Merges vector search results with live API data

**Examples**:

**Crop Planning Synthesis**:
```python
def _synthesize_crop_planning(self, docs, context):
    # Calls farm_management.planning_stage.PreSeedingService
    service = PreSeedingService()
    output = service.run(PlanningRequest(farmer_id=context["farmer_id"]))
    
    # Converts PreSeedingOutput to CropCard list
    cards = [
        CropCard(
            crop_name=rec.crop_name,
            crop_name_hi=rec.crop_name_hi,
            score=rec.score,
            reasons=rec.reasons,
            risks=rec.risks,
            profit_level=rec.profit_level,
            sowing_window=rec.sowing_window_hint,
            next_action=rec.next_best_action,
            sources=rec.seed_material_sources
        )
        for rec in output.crop_cards[:3]
    ]
    return cards
```

**Government Scheme Synthesis**:
```python
def _synthesize_schemes(self, docs, context):
    # Calls gov_schemes.service.GovSchemeService
    service = GovSchemeService()
    results = service.check_eligibility(farmer_id=context["farmer_id"])
    
    cards = [
        SchemeCard(
            scheme_name=res.scheme_name,
            scheme_name_hi=res.scheme_name_hi,
            eligible=res.eligible,
            why_eligible=res.why_eligible,
            deadline_warning=res.deadline_warning,
            docs_required=res.docs_required,
            next_step=res.next_step,
            apply_url=res.apply_url
        )
        for res in results if res.eligible
    ]
    return cards
```

**Financial Report Synthesis**:
```python
def _synthesize_finance_report(self, context):
    # Calls financial_tracking.service.FinancialService
    connector = get_financial_connector()
    report = connector.get_profit_loss_summary(farmer_id=context["farmer_id"])
    
    # Returns report as card
    return [report_card]
```

---

### 6. Memory Management (memory/)

#### 6.1 Session Memory (memory/session_memory.py)

**Class**: `SessionMemory`

**Purpose**: Short-term conversation memory (per session).

**MongoDB-Ready**: Can store in MongoDB or use in-memory fallback.

**Key Methods**:
```python
def save_context(self, context: ConversationContext):
    # Saves session to MongoDB or in-memory
    
def load_context(self, session_id: str) -> Optional[ConversationContext]:
    # Loads session from storage
    
def get_recent_sessions(self, farmer_id: str, limit: int = 10) -> List[Dict]:
    # Gets recent sessions for a farmer
    
def clear_old_sessions(self, days: int = 30):
    # Deletes sessions older than N days
```

**Storage Format**:
```python
{
    "session_id": "sess_123",
    "farmer_id": "F001",
    "farmer_profile": {...},
    "conversation_history": [...],
    "context_variables": {...},
    "last_intent": "crop_planning",
    "last_updated": "2026-01-23T01:40:00Z"
}
```

---

#### 6.2 Summary Memory (memory/summary_memory.py)

**Class**: `SummaryMemory`

**Purpose**: Long-term memory via conversation summarization.

**Strategy**: After N turns, summarizes conversation and stores key facts for future reference.

**Key Methods**:
```python
def summarize_session(self, session_id: str) -> str:
    # Creates summary of session
    
def get_farmer_history_summary(self, farmer_id: str) -> str:
    # Gets combined summary of farmer's past interactions
```

**Use Case**: Multi-session context (e.g., "Last time you asked about wheat, now let's discuss...")

---

### 7. Response Cards (cards/)

Structured data containers for different information types.

#### Base Card (cards/base_card.py)

```python
class BaseCard:
    """Base interface for all cards"""
    
    def to_dict(self) -> Dict[str, Any]:
        # Converts to JSON for API response
    
    def to_speech_text(self, language: str = "hi") -> str:
        # Converts to voice-readable text
```

#### Specific Cards

**CropCard** (cards/crop_card.py):
```python
@dataclass
class CropCard(BaseCard):
    crop_name: str
    crop_name_hi: str
    score: float
    reasons: List[str]
    risks: List[str]
    profit_level: str
    sowing_window: str
    next_action: str
    sources: List[Dict]  # Seed procurement sources
```

**WeatherCard** (cards/weather_card.py):
```python
@dataclass
class WeatherCard(BaseCard):
    temperature_c: float
    humidity_pct: float
    rain_forecast: bool
    rain_mm_next_7_days: float
    alerts: List[str]
    farming_advice: str  # Weather-based guidance
```

**MarketCard** (cards/market_card.py):
```python
@dataclass
class MarketCard(BaseCard):
    crop_name: str
    mandi_name: str
    price_per_kg: float
    trend: str  # "RISING", "FALLING", "STABLE"
    last_updated: datetime
```

**SchemeCard** (cards/scheme_card.py):
```python
@dataclass
class SchemeCard(BaseCard):
    scheme_name: str
    scheme_name_hi: str
    eligible: bool
    why_eligible: List[str]
    deadline_warning: str
    docs_required: List[str]
    next_step: str
    apply_url: str
```

---

### 8. Explanation Builder (explain/explanation_builder.py)

**Class**: `ExplanationBuilder`

**Purpose**: Convert cards into natural language explanations (Hindi/English).

**Key Method**:
```python
def build_explanation(
    self,
    cards: List[BaseCard],
    intent: Intent,
    language: str = "hi"
) -> str:
    """
    Build voice-ready explanation from cards
    
    Strategy:
    - Concise 2-3 sentences for voice
    - Highlights most important info
    - Uses natural conversational tone
    - Bilingual support
    
    Returns: Voice-ready text
    """
```

**Example Output (Hindi)**:
```
"आपकी मिट्टी और मौसम के लिए सबसे अच्छी फसलें हैं: गेहूं (स्कोर: 92), चना (स्कोर: 85), और सरसों (स्कोर: 78)। 
गेहूं की बुवाई नवंबर में शुरू करें। आप PM-KISAN और PMFBY योजना के लिए पात्र हैं - 15 दिनों में डेडलाइन है।"
```

**Example Output (English)**:
```
"Best crops for your soil and season are: Wheat (score: 92), Chickpea (score: 85), and Mustard (score: 78).
Start wheat sowing in November. You're eligible for PM-KISAN and PMFBY schemes - deadline in 15 days."
```

---

### 9. Backend Module Connectors (connectors/)

These connectors integrate the voice agent with other backend modules.

#### Financial Connector (connectors/financial_connector.py)

```python
class FinancialConnector:
    def __init__(self):
        from financial_tracking.service import FinancialService
        self.service = FinancialService()
    
    def get_profit_loss_summary(self, farmer_id: str) -> Dict:
        return self.service.get_profit_loss(farmer_id)
    
    def add_expense(self, farmer_id: str, expense_data: Dict):
        return self.service.add_transaction(farmer_id, "expense", expense_data)
    
    def add_income(self, farmer_id: str, income_data: Dict):
        return self.service.add_transaction(farmer_id, "income", income_data)
    
    def get_optimization_advice(self, farmer_id: str) -> List[str]:
        return self.service.get_optimization_suggestions(farmer_id)
```

#### Collaborative Connector (connectors/collaborative_connector.py)

```python
class CollaborativeConnector:
    def __init__(self):
        from collaborative_farming.service import CollaborativeService
        self.service = CollaborativeService()
    
    def list_equipment_rentals(self, location: str, equipment_type: str):
        return self.service.search_equipment(location, equipment_type)
    
    def request_land_pooling(self, farmer_id: str, land_details: Dict):
        return self.service.create_land_pool_request(farmer_id, land_details)
    
    def list_marketplace_offers(self, crop_type: str, radius_km: int):
        return self.service.get_marketplace_offers(crop_type, radius_km)
```

#### Inventory Connector (connectors/inventory_connector.py)

```python
class InventoryConnector:
    def get_inventory(self, farmer_id: str) -> Dict:
        # Returns current inventory (seeds, fertilizers, equipment)
    
    def check_stock_levels(self, farmer_id: str) -> Dict:
        # Returns low-stock alerts
```

#### Alerts Connector (connectors/alerts_connector.py)

```python
class AlertsConnector:
    def get_pending_alerts(self, farmer_id: str) -> List[Dict]:
        # Returns pending alerts (weather, price, scheme deadlines, etc.)
    
    def mark_alert_read(self, alert_id: str):
        # Marks alert as read
```

---

### 10. Input Processing (input_processing/)

#### Speech-to-Text (input_processing/speech_to_text.py)

**Class**: `SpeechToText`

**Purpose**: Convert audio to text (Hindi/English).

**Providers**:
- Google Cloud Speech-to-Text
- Whisper API (OpenAI)
- Azure Speech Services

**Key Method**:
```python
def transcribe(self, audio_file_path: str, language: str = "hi-IN") -> str:
    # Returns transcribed text
```

---

#### Translator (input_processing/translator.py)

**Class**: `Translator`

**Purpose**: Translate between Hindi and English.

**Providers**:
- Google Translate API
- Groq/Gemini for translation

**Key Methods**:
```python
def translate_to_english(self, hindi_text: str) -> str:
    # Translates Hindi to English
    
def translate_to_hindi(self, english_text: str) -> str:
    # Translates English to Hindi
```

---

## Complete Interaction Flow

```
1. Voice Input (Audio/Text) → Farmer speaks/types in Hindi
   ↓
2. Speech-to-Text → Converts audio to text (if audio)
   ↓
3. Intent Classification → LLM detects intent (CROP_PLANNING, SCHEME, etc.)
   ↓
4. Context Retrieval → Loads/creates conversation context
   ↓
5. Information Retrieval (RAG) → Retrieves relevant data from:
   - Vector Store (semantic search)
   - Live APIs (weather, market)
   - Backend modules (farm_management, gov_schemes, etc.)
   ↓
6. Reasoning Plan → Creates intent-specific reasoning plan
   ↓
7. Information Synthesis → Calls backend services to generate cards:
   - PreSeedingService for crop planning
   - GovSchemeService for schemes
   - FinancialService for finance
   - Etc.
   ↓
8. Explanation Building → Converts cards to natural language (Hindi/English)
   ↓
9. Memory Update → Saves conversation turn to session memory
   ↓
10. Response Return → Returns AgentResponse with:
    - Structured cards (for UI display)
    - Voice-ready explanation (for speech synthesis)
    - Reasoning trace (for debugging)
```

---

## Configuration (config.py)

**Class**: `Config`

**Environment Variables** (from `.env.template`):
```bash
# LLM Provider
LLM_PROVIDER=groq  # or "gemini"
GROQ_API_KEY=...
GEMINI_API_KEY=...

# Weather
OPENWEATHER_API_KEY=...

# Database
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=kisaan_mitra

# ChromaDB
CHROMA_DB_PATH=./chroma_db

# Speech Services (optional)
GOOGLE_CLOUD_API_KEY=...
AZURE_SPEECH_KEY=...
```

**Config Access**:
```python
from voice_agent.config import get_config

config = get_config()
print(config.llm_provider)  # "groq"
print(config.groq_api_key)  # env var value
```

---

## Module Interactions

### How Voice Agent Integrates with Other Modules

```python
# Farm Management Integration
from farm_management.planning_stage.service import PreSeedingService
from farm_management.post_harvest_stage.core.engine import PostHarvestEngine

# Government Schemes Integration
from gov_schemes.service import GovSchemeService

# Financial Tracking Integration
from financial_tracking.service import FinancialService

# Collaborative Farming Integration
from collaborative_farming.service import CollaborativeService
```

**Voice Agent acts as the orchestrator**:
- Receives user intent
- Routes to appropriate backend module service
- Packages response for voice/UI consumption

---

## Key Dependencies

**Python Packages**:
```
groq  # Groq LLM API
google-generativeai  # Gemini API
chromadb  # Vector database
sentence-transformers  # Embeddings
pymongo  # MongoDB client
pydantic  # Data validation
```

---

## API Endpoint Design Pattern

```python
# Example FastAPI endpoint
from fastapi import APIRouter
from voice_agent import get_voice_agent

router = APIRouter()

@router.post("/api/v1/voice/process")
async def process_voice_input(request: VoiceInputRequest):
    """
    Process voice/text input
    
    Request:
    {
        "text": "मुझे किस फसल की बुवाई करनी चाहिए?",
        "farmer_id": "F001",
        "session_id": "sess_123" (optional)
    }
    
    Response:
    {
        "session_id": "sess_123",
        "intent": "crop_planning",
        "confidence": 0.95,
        "cards": [...],
        "explanation_hindi": "...",
        "explanation_english": "...",
        "timestamp": "..."
    }
    """
    agent = get_voice_agent()
    response = agent.process_input(
        hindi_text=request.text,
        farmer_id=request.farmer_id,
        session_id=request.session_id
    )
    return response.to_dict()
```

---

## Testing & Debugging

**CLI Demo** (`cli_demo.py`):
```bash
python voice_agent/cli_demo.py
# Interactive Hindi/English CLI for testing
```

**Test Intents** (`auto_test_intents.py`):
```bash
python voice_agent/auto_test_intents.py
# Automated test suite for all intents
```

**Full Integration Demo** (`full_integration_demo.py`):
```bash
python voice_agent/full_integration_demo.py
# End-to-end demo with all modules
```

---

## Summary of Significant Functions

### Core Agent Functions
1. `VoiceAgent.process_input()` - Main orchestration
2. `LLMIntentClassifier.classify()` - LLM-based intent detection
3. `Retriever.retrieve()` - RAG information retrieval
4. `Synthesizer.synthesize()` - Card generation from retrieved data
5. `ExplanationBuilder.build_explanation()` - Natural language generation

### Memory Functions
6. `SessionMemory.save_context()` - Persist conversation state
7. `SessionMemory.load_context()` - Retrieve conversation history
8. `SummaryMemory.summarize_session()` - Long-term memory creation

### Integration Functions
9. `FinancialConnector.get_profit_loss_summary()` - Financial module integration
10. `CollaborativeConnector.list_equipment_rentals()` - Collaborative module integration

---

## Voice Agent as Integration Hub

The Voice Agent module serves as the **central integration hub** that:

1. **Receives** user input (voice/text, Hindi/English)
2. **Detects** intent using LLM
3. **Retrieves** information via RAG
4. **Routes** to appropriate backend modules:
   - `farm_management` for crop planning, farming, post-harvest
   - `gov_schemes` for scheme eligibility
   - `financial_tracking` for expense/income tracking
   - `collaborative_farming` for equipment rental, land pooling
5. **Synthesizes** responses into structured cards
6. **Generates** bilingual natural language explanations
7. **Returns** unified response for both voice and UI

This design ensures **voice-first** interaction while maintaining **structured data** for dashboards and apps.
