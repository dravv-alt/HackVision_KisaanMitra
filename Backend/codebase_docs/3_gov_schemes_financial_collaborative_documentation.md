# Government Schemes, Financial Tracking & Collaborative Farming Modules - Complete Documentation

## Table of Contents
1. [Government Schemes Module](#government-schemes-module)
2. [Financial Tracking Module](#financial-tracking-module)
3. [Collaborative Farming Module](#collaborative-farming-module)
4. [Module Interactions](#module-interactions)

---

# Government Schemes Module

## Module Overview

**Path**: `Backend/gov_schemes/`

**Purpose**: Manage government agricultural schemes by fetching data from APIs, filtering based on farmer profiles, generating alerts for new schemes, and providing actionable guidance.

### Architecture

```
gov_schemes/
├── models.py                # Pydantic data models
├── constants.py             # Enums and configuration
├── service.py               # Main orchestration service
├── config/                  # Configuration management
│   └── settings.py
├── engines/                 # Business logic engines
│   ├── scheme_fetch_engine.py       # API sync and caching
│   ├── scheme_filter_engine.py      # Location/category filtering
│   ├── scheme_alert_engine.py       # New scheme detection & alerts
│   └── response_builder.py          # Voice-first output formatting
└── repositories/            # Data access layer
    ├── farmer_repo.py               # Farmer profile data
    ├── scheme_repo.py               # Scheme data storage
    ├── scheme_api_client.py         # External API client
    ├── alert_repo.py                # Alert notifications storage
    └── audit_repo.py                # Audit logging
```

---

## Data Models (models.py)

### FarmerProfile
```python
class FarmerProfile(BaseModel):
    farmerId: str
    language: Language = Language.HINDI
    state: Optional[str] = None
    district: Optional[str] = None
    pincode: Optional[str] = None
```

### SchemeRecord
```python
class SchemeRecord(BaseModel):
    schemeId: str
    schemeName: str
    schemeNameHindi: Optional[str] = None
    category: SchemeCategory
    description: str
    descriptionHindi: Optional[str] = None
    state: Optional[str] = None         # None = All India
    district: Optional[str] = None      # None = State-wide
    benefits: str
    benefitsHindi: Optional[str] = None
    eligibility: Optional[str] = None
    eligibilityHindi: Optional[str] = None
    howToApply: Optional[str] = None
    howToApplyHindi: Optional[str] = None
    officialLink: Optional[str] = None
    contactNumber: Optional[str] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    isActive: bool = True
    createdAt: datetime
    updatedAt: datetime
```

### SchemeCardOutput
```python
class SchemeCardOutput(BaseModel):
    schemeId: str
    schemeName: str
    category: SchemeCategory
    categoryDisplay: str
    description: str
    benefits: str
    eligibility: Optional[str] = None
    howToApply: Optional[str] = None
    officialLink: Optional[str] = None
    contactNumber: Optional[str] = None
    scope: str                # "All India", "State-wide", "District-specific"
    isNew: bool = False       # New scheme (added in last 7 days)
    daysRemaining: Optional[int] = None  # Days until end date
```

### AlertRecord
```python
class AlertRecord(BaseModel):
    alertId: str
    farmerId: str
    alertType: AlertType      # GOV_SCHEME, WEATHER, PRICE, etc.
    urgency: AlertUrgency     # LOW, MEDIUM, HIGH, CRITICAL
    status: AlertStatus       # PENDING, SENT, READ
    title: str
    titleHindi: Optional[str] = None
    message: str
    messageHindi: Optional[str] = None
    relatedId: Optional[str] = None      # schemeId
    actionUrl: Optional[str] = None
    createdAt: datetime
    sentAt: Optional[datetime] = None
    readAt: Optional[datetime] = None
```

### GovSchemesOutput
```python
class GovSchemesOutput(BaseModel):
    header: str
    language: Language
    speechText: str                          # Voice-first summary
    schemeCards: List[SchemeCardOutput]
    totalSchemes: int
    newSchemesCount: int
    filterApplied: dict                      # state, district, category
    detailedReasoning: str
```

---

## Constants (constants.py)

```python
class SchemeCategory(str, Enum):
    CROP_INSURANCE = "crop_insurance"
    INPUT_SUBSIDY = "input_subsidy"
    CREDIT_SCHEME = "credit_scheme"
    PRICE_SUPPORT = "price_support"
    IRRIGATION = "irrigation"
    SOIL_HEALTH = "soil_health"
    MACHINERY_SUBSIDY = "machinery_subsidy"
    ALL = "all"

class AltertType(str, Enum):
    GOV_SCHEME = "gov_scheme"
    WEATHER_ALERT = "weather_alert"
    PRICE_ALERT = "price_alert"
    DEADLINE_REMINDER = "deadline_reminder"

class AlertUrgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    READ = "read"
```

---

## Main Service (service.py)

**Class**: `GovSchemesDisplayService`

### Main Method: `get_schemes_display()`

```python
def get_schemes_display(
    self,
    farmer_id: str,
    state: Optional[str] = None,
    district: Optional[str] = None,
    category: Optional[SchemeCategory] = None,
    force_refresh: bool = False,
    generate_alerts: bool = True
) -> GovSchemesOutput:
    """
    Generate complete government schemes display
    
    Workflow:
    1. Audit log
    2. Get farmer profile
    3. Sync schemes from API (with caching)
    4. Detect new schemes (last 7 days)
    5. Generate alerts for eligible new schemes
    6. Apply location/category filters
    7. Sort by relevance
    8. Build voice-first output
    9. Audit log success
    
    Returns: GovSchemesOutput with cards and speech text
    """
```

### Other Methods
- `get_scheme_by_id(scheme_id: str)`: Get detailed scheme info
- `get_alerts_for_farmer(farmer_id: str)`: Get all alerts
- `mark_alert_as_read(alert_id: str)`: Mark alert as read

---

## Engines

### 1. SchemeFetchEngine (engines/scheme_fetch_engine.py)

**Purpose**: Fetch schemes from external API and manage caching.

**Key Method**: `sync_schemes(force_refresh: bool = False)`

**Workflow**:
1. Check if cache refresh needed (age > 24 hours or force_refresh)
2. If refresh needed:
   - Fetch from API via `SchemeAPIClient`
   - Save to cache via `SchemeRepo`
3. Else: Return cached schemes

**Cache TTL**: Configurable, default 24 hours

---

### 2. SchemeFilterEngine (engines/scheme_filter_engine.py)

**Purpose**: Filter and sort schemes based on criteria.

**Key Methods**:
- `filter_by_location(state, district, category)`: Filter schemes by location and category
- `sort_schemes(schemes, sort_by)`: Sort by relevance, deadline, or category

**Filtering Logic**:
- **State filter**: Shows all-India schemes + state-specific
- **District filter**: Shows all-India + state + district-specific
- **Category filter**: Shows only selected category schemes

---

### 3. SchemeAlertEngine (engines/scheme_alert_engine.py)

**Purpose**: Detect new schemes and generate alerts for farmers.

**Key Methods**:
- `detect_new_schemes(since: datetime)`: Find schemes added since date
- `generate_alerts_for_farmer(farmer, new_schemes)`: Create alert records

**Alert Generation Logic**:
1. Filter new schemes by farmer location
2. For each relevant scheme:
   - Create AlertRecord with HIGH urgency
   - Set title: "नई सरकारी योजना: [scheme name]"
   - Set message: Benefits and how to apply
   - Set related ID to schemeId
3. Return list of AlertRecord

---

### 4. ResponseBuilder (engines/response_builder.py)

**Purpose**: Build voice-first multilingual output.

**Key Method**: `build(farmer, schemes, new_count, filter_applied)`

**Output Components**:
1. **Header**: "सरकारी योजनाएँ" / "Government Schemes"
2. **Speech Text**: Concise summary (2-3 sentences)
   - Example: "आपके लिए 12 सरकारी योजनाएं हैं। 2 नई योजनाएं हैं - PM-KISAN और PMFBY। आवेदन करने के लिए CSC जाएं।"
3. **Scheme Cards**: List of SchemeCardOutput
4. **Detailed Reasoning**: Full description of all schemes

---

## Repositories

### 1. SchemeRepo (repositories/scheme_repo.py)

**Purpose**: Manage scheme data storage.

**Key Methods**:
- `save_schemes(schemes: List[SchemeRecord])`: Bulk save/update
- `get_all_schemes()`: Retrieve all cached schemes
- `get_scheme_by_id(scheme_id)`: Get single scheme
- `get_last_sync_time()`: Get timestamp of last API sync

**Storage**: MongoDB collection `government_schemes` (or in-memory fallback)

---

### 2. SchemeAPIClient (repositories/scheme_api_client.py)

**Purpose**: Fetch schemes from external APIs.

**Key Method**: `fetch_schemes() -> List[SchemeRecord]`

**API Sources**:
- **Production**: Government scheme portals (e.g., pmkisan.gov.in, pmfby.gov.in)
- **Demo**: Mock data generator

---

### 3. AlertRepo (repositories/alert_repo.py)

**Purpose**: Manage alert notifications.

**Key Methods**:
- `save_alerts(alerts: List[AlertRecord])`: Save alerts
- `get_alerts_for_farmer(farmer_id, alert_type)`: Get pending alerts
- `mark_as_read(alert_id)`: Mark alert as read

---

### 4. AuditRepo (repositories/audit_repo.py)

**Purpose**: Log all operations for monitoring and analytics.

**Key Method**: `log(farmer_id, action, metadata)`

**Logged Actions**:
- `get_schemes_display`
- `display_success` / `display_error`
- Allows tracking usage patterns and errors

---

## Integration with Voice Agent

```python
# Voice Agent calls GovernmentSchemes module

from gov_schemes.service import GovSchemesDisplayService

service = GovSchemesDisplayService()
output = service.get_schemes_display(
    farmer_id="F001",
    generate_alerts=True
)

# output.schemeCards → Sent to UI
# output.speechText → Sent to TTS for voice
```

---

# Financial Tracking Module

## Module Overview

**Path**: `Backend/financial_tracking/`

**Purpose**: Track farm expenses and income, generate profit/loss reports, analyze loss causes, and provide optimization suggestions.

### Architecture

```
financial_tracking/
├── models.py                # Pydantic data models
├── constants.py             # Enums and configuration
├── service.py               # Main orchestration service
├── engines/                 # Business logic engines
│   ├── ledger_engine.py            # Transaction management
│   ├── profit_loss_engine.py       # P&L calculation
│   ├── loss_analysis_engine.py     # Loss cause identification
│   ├── optimization_engine.py      # Cost-saving suggestions
│   └── response_builder.py         # Voice-first output
└── repositories/            # Data access layer
    ├── transaction_repo.py          # Transaction storage
    ├── summary_repo.py              # Cached summaries
    └── crop_repo.py                 # Crop metadata
```

---

## Data Models (models.py)

### FinanceTransaction
```python
class FinanceTransaction(BaseModel):
    transactionId: str
    farmerId: str
    relatedCropId: Optional[str] = None
    season: str                      # KHARIF, RABI, ZAID
    type: TransactionType            # EXPENSE, INCOME
    category: str                    # ExpenseCategory or IncomeCategory
    amount: float = Field(gt=0)
    currency: str = Currency.INR.value
    notes: Optional[str] = None
    ts: datetime                     # Transaction timestamp
    createdAt: datetime
    updatedAt: datetime
```

### FinanceTotals
```python
class FinanceTotals(BaseModel):
    farmerId: str
    season: str
    totalExpense: float = 0.0
    totalIncome: float = 0.0
    profitOrLoss: float = 0.0
    profitMarginPct: float = 0.0
```

### ExpenseBreakdown
```python
class ExpenseBreakdown(BaseModel):
    category: str                    # SEED, FERTILIZER, PESTICIDE, etc.
    amount: float
    percent: float                   # % of total expense
    categoryNameEn: str
    categoryNameHi: str
```

### LossCause
```python
class LossCause(BaseModel):
    title: str                       # e.g., "High Fertilizer Cost"
    description: str
    impactAmount: float              # Financial impact
    confidenceScore: float           # 0-1
```

### OptimizationSuggestion
```python
class OptimizationSuggestion(BaseModel):
    suggestionTitle: str             # e.g., "Switch to Organic Fertilizer"
    whyThisHelps: str
    estimatedSavings: float
    priority: int = Field(ge=1, le=5)  # 1=highest
    actionableSteps: List[str]
```

### FinanceModuleOutput
```python
class FinanceModuleOutput(BaseModel):
    header: str
    language: str
    speechText: str                           # Voice summary
    totals: FinanceTotals
    topExpenseCategories: List[ExpenseBreakdown]
    lossCauses: List[LossCause]
    suggestions: List[OptimizationSuggestion]
    detailedReasoning: str
    urgencyLevel: UrgencyLevel
```

### FinanceCard
```python
class FinanceCard(BaseModel):
    """Voice agent compatible card"""
    card_type: str = "finance"
    title: str
    summary: str
    details: Dict[str, Any]
    source: str = "financial_tracking"
    confidence: float = 1.0
    timestamp: datetime
    metadata: Dict[str, Any]
```

---

## Constants (constants.py)

```python
class TransactionType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"

class ExpenseCategory(str, Enum):
    SEED = "seed"
    FERTILIZER = "fertilizer"
    PESTICIDE = "pesticide"
    LABOR = "labor"
    MACHINERY_RENT = "machinery_rent"
    IRRIGATION = "irrigation"
    TRANSPORT = "transport"
    OTHER = "other"

class IncomeCategory(str, Enum):
    CROP_SALE = "crop_sale"
    SUBSIDY = "subsidy"
    OTHER = "other"

class SeasonType(str, Enum):
    KHARIF = "kharif"
    RABI = "rabi"
    ZAID = "zaid"

class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Currency(str, Enum):
    INR = "INR"
```

---

## Main Service (service.py)

**Class**: `FinanceTrackingService`

### Main Method: `run_finance_report()`

```python
def run_finance_report(
    self,
    farmerId: str,
    season: str = SeasonType.KHARIF.value,
    language: str = "hi",
    force_refresh: bool = False
) -> FinanceModuleOutput:
    """
    Generate complete financial report
    
    Workflow:
    1. Get all transactions for farmer + season
    2. Calculate totals via ProfitLossEngine
    3. Analyze expense breakdown via LedgerEngine
    4. Identify loss causes via LossAnalysisEngine
    5. Generate optimization suggestions via OptimizationEngine
    6. Build voice-first output via ResponseBuilder
    7. Cache summary (optional)
    
    Returns: FinanceModuleOutput with P&L, analysis, suggestions
    """
```

### Transaction Management

**Add Expense**:
```python
def add_expense(
    self,
    farmerId: str,
    season: str,
    category: str,
    amount: float,
    notes: Optional[str] = None,
    relatedCropId: Optional[str] = None
) -> FinanceTransaction:
    """
    Add expense transaction
    
    Workflow:
    1. Create FinanceTransaction (type=EXPENSE)
    2. Save to TransactionRepo
    3. Invalidate cached summary (force recalculation)
    
    Returns: Created transaction
    """
```

**Add Income**:
```python
def add_income(
    self,
    farmerId: str,
    season: str,
    category: str,
    amount: float,
    notes: Optional[str] = None,
    relatedCropId: Optional[str] = None
) -> FinanceTransaction:
    """Add income transaction (similar to add_expense)"""
```

### Voice Agent Integration

```python
def get_finance_card(
    self,
    farmerId: str,
    season: str = SeasonType.KHARIF.value,
    language: str = "hi"
) -> FinanceCard:
    """
    Generate voice_agent compatible FinanceCard
    
    Returns: FinanceCard with profit/loss summary
    """
```

---

## Engines

### 1. LedgerEngine (engines/ledger_engine.py)

**Purpose**: Transaction-level operations and aggregation.

**Key Methods**:
- `aggregate_by_category(transactions)`: Group and sum by category
- `calculate_expense_breakdown(transactions)`: Generate ExpenseBreakdown list with percentages

---

### 2. ProfitLossEngine (engines/profit_loss_engine.py)

**Purpose**: Calculate profit/loss metrics.

**Key Method**: `calculate(transactions) -> FinanceTotals`

**Calculation**:
```python
total_expense = sum(t.amount for t in transactions if t.type == EXPENSE)
total_income = sum(t.amount for t in transactions if t.type == INCOME)
profit_or_loss = total_income - total_expense
profit_margin_pct = (profit_or_loss / total_income * 100) if total_income > 0 else 0
```

---

### 3. LossAnalysisEngine (engines/loss_analysis_engine.py)

**Purpose**: Identify causes of financial loss.

**Key Method**: `analyze(transactions, totals) -> List[LossCause]`

**Analysis Rules**:
1. **High Fertilizer Cost**: If fertilizer > 30% of expenses
2. **Excessive Pesticide Use**: If pesticide > 20%
3. **Low Crop Yield**: If income/expense ratio < 1.2
4. **High Labor Cost**: If labor > 40%

**Returns**: Top 3 loss causes with impact amounts

---

### 4. OptimizationEngine (engines/optimization_engine.py)

**Purpose**: Generate cost-saving suggestions.

**Key Method**: `suggest(transactions, losses) -> List[OptimizationSuggestion]`

**Suggestion Rules**:
- If high fertilizer: Suggest soil testing, organic alternatives
- If high pesticide: Suggest IPM (Integrated Pest Management)
- If high labor: Suggest mechanization, cooperative labor sharing
- If low yield: Suggest better seeds, irrigation improvements

**Prioritization**: Based on estimated savings (highest first)

---

### 5. ResponseBuilder (engines/response_builder.py)

**Purpose**: Build multilingual voice-first output.

**Key Method**: `build(farmer, totals, breakdowns, losses, suggestions, language)`

**Speech Text Example (Hindi)**:
```
"इस खरीफ सीजन में आपका कुल खर्च ₹45,000 और आय ₹52,000 है। आपको ₹7,000 का मुनाफा हुआ। 
उर्वरक की लागत बहुत ज्यादा है - मिट्टी परीक्षण कराएं। अनुमानित बचत: ₹5,000।"
```

---

## Repositories

### 1. TransactionRepo (repositories/transaction_repo.py)

**Purpose**: Store and retrieve transactions.

**Key Methods**:
- `save_transaction(transaction)`: Save single transaction
- `get_transactions(farmerId, season)`: Get all transactions for farmer + season
- `delete_transaction(transactionId)`: Soft delete

**Storage**: MongoDB collection `finance_transactions` (or in-memory)

---

### 2. SummaryRepo (repositories/summary_repo.py)

**Purpose**: Cache pre-calculated summaries.

**Key Methods**:
- `save_summary(farmerId, season, summary)`: Cache summary
- `get_summary(farmerId, season)`: Retrieve cached summary
- `invalidate(farmerId, season)`: Clear cache (when new transaction added)

**Cache Strategy**: Speeds up repeated queries

---

### 3. CropRepo (repositories/crop_repo.py)

**Purpose**: Provide crop metadata for profit calculations.

**Key Method**: `get_crop_metadata(cropId) -> Dict`

**Data**: Crop name, expected yield, avg market price, etc.

---

## Integration with Voice Agent

```python
# Voice Agent Integration

from financial_tracking.service import FinanceTrackingService

service = FinanceTrackingService()

# Get report
report = service.run_finance_report(
    farmerId="F001",
    season="kharif",
    language="hi"
)

# Add expense (voice command: "मैंने 5000 रुपये खाद पर खर्च किए")
service.add_expense(
    farmerId="F001",
    season="kharif",
    category="fertilizer",
    amount=5000.0,
    notes="DAP खाद"
)

# Get finance card for voice agent
card = service.get_finance_card(farmerId="F001", season="kharif")
```

---

# Collaborative Farming Module

## Module Overview

**Path**: `Backend/collaborative_farming/`

**Purpose**: Enable farmer-to-farmer collaboration via equipment rental, land pooling, and residue management marketplace.

### Architecture

```
collaborative_farming/
├── models.py                # Pydantic data models
├── constants.py             # Enums and configuration
├── service.py               # Main orchestration service
├── engines/                 # Business logic engines
│   ├── equipment_engine.py          # Equipment listing/search
│   ├── rental_engine.py             # Rental booking/management
│   ├── land_pool_engine.py          # Land pooling logic
│   ├── residue_engine.py            # Residue marketplace
│   ├── reminder_engine.py           # Rental return reminders
│   └── response_builder.py          # Voice-first output
└── repositories/            # Data access layer
    ├── farmer_repo.py               # Farmer profiles
    ├── equipment_repo.py            # Equipment listings
    ├── rental_repo.py               # Rental requests
    ├── land_pool_repo.py            # Land pools
    ├── residue_repo.py              # Residue listings
    ├── alert_repo.py                # Alerts
    └── audit_repo.py                # Audit logs
```

---

## Data Models (models.py)

### FarmerProfile
```python
class FarmerProfile(BaseModel):
    farmerId: str
    name: str
    language: Language = Language.HINDI
    state: str
    district: str
    pincode: str
    lat: float
    lon: float
```

### EquipmentListing
```python
class EquipmentListing(BaseModel):
    listingId: str
    ownerFarmerId: str
    equipmentType: EquipmentType     # TRACTOR, HARVESTER, SPRAYER, etc.
    modelName: str
    pricePerDay: float
    condition: str = "Good"          # Excellent, Good, Fair
    hpRequired: Optional[str] = None # e.g., "45-50 HP"
    isVerified: bool = True
    availableFrom: datetime
    availableTo: datetime
    district: str
    pincode: str
    status: ListingStatus            # AVAILABLE, RENTED, INACTIVE
    createdAt: datetime
    updatedAt: datetime
```

### RentalRequest
```python
class RentalRequest(BaseModel):
    rentalId: str
    listingId: str
    renterFarmerId: str
    ownerFarmerId: str
    startDate: datetime
    endDate: datetime
    totalAmount: float
    serviceFee: float = 0.0
    paymentMethod: PaymentMethod     # CASH_ON_DELIVERY, UPI, etc.
    status: RentalStatus             # REQUESTED, APPROVED, ONGOING, COMPLETED, CANCELLED
    createdAt: datetime
    updatedAt: datetime
```

### LandPoolRequest
```python
class LandPoolRequest(BaseModel):
    requestId: str
    farmerId: str                    # Pool creator
    requestType: PoolRequestType     # JOINT_FARMING, BULK_SELLING, INPUT_PURCHASE
    landSizeAcres: float
    cropPreference: Optional[str] = None
    season: Optional[str] = None
    expectedMembers: Optional[int] = None
    joinedFarmers: List[str] = []
    district: str
    pincode: str
    currentStage: PoolStage          # FORMATION, ACTIVE, COMPLETED
    progressPct: int = 0
    targetPrice: Optional[float] = None
    highestBid: Optional[float] = None
    sellingWindow: Optional[str] = None
    totalQuantity: float = 0.0
    keyBenefit: Optional[str] = None
    status: PoolStatus               # OPEN, CLOSED, COMPLETED
    createdAt: datetime
    updatedAt: datetime
```

### ResidueListing
```python
class ResidueListing(BaseModel):
    residueId: str
    farmerId: str
    cropType: str                    # "Rice straw", "Wheat stubble", etc.
    quantityKg: float
    expectedPricePerKg: float
    district: str
    pincode: str
    status: str = "OPEN"             # OPEN, CLOSED
    createdAt: datetime
```

### CollaborativeOutput
```python
class CollaborativeOutput(BaseModel):
    header: str
    language: Language
    speechText: str                           # Voice summary
    equipmentCards: List[EquipmentListing]
    rentalCards: List[RentalRequest]
    landPoolCards: List[LandPoolRequest]
    residueCards: List[ResidueListing]
    remindersSuggested: List[ReminderRecord]
    detailedReasoning: str
    urgencyLevel: UrgencyLevel
```

---

## Constants (constants.py)

```python
class EquipmentType(str, Enum):
    TRACTOR = "tractor"
    HARVESTER = "harvester"
    THRESHER = "thresher"
    SEED_DRILL = "seed_drill"
    SPRAYER = "sprayer"
    ROTAVATOR = "rotavator"
    OTHER = "other"

class ListingStatus(str, Enum):
    AVAILABLE = "available"
    RENTED = "rented"
    INACTIVE = "inactive"

class RentalStatus(str, Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class PoolRequestType(str, Enum):
    JOINT_FARMING = "joint_farming"        # Pool land for collaborative farming
    BULK_SELLING = "bulk_selling"          # Pool produce for better prices
    INPUT_PURCHASE = "input_purchase"      # Pool for bulk seed/fertilizer purchase

class PoolStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    COMPLETED = "completed"

class PoolStage(str, Enum):
    FORMATION = "formation"
    ACTIVE = "active"
    COMPLETED = "completed"

class PaymentMethod(str, Enum):
    CASH_ON_DELIVERY = "cash_on_delivery"
    UPI = "upi"
    BANK_TRANSFER = "bank_transfer"
```

---

## Main Service (service.py)

**Class**: `CollaborativeFarmingService`

### Main Method: `run_marketplace_view()`

```python
def run_marketplace_view(
    self,
    farmer_id: str,
    filters: Dict = {}
) -> CollaborativeOutput:
    """
    Generate complete collaborative farming marketplace view
    
    Workflow:
    1. Get farmer profile
    2. List available equipment (nearby)
    3. Find matching land pools
    4. Get farmer's active rentals
    5. List residue offers (nearby)
    6. Generate rental return reminders
    7. Build voice-first output
    
    Returns: CollaborativeOutput with all cards
    """
```

### Equipment Rental Methods

**Create Listing**:
```python
def create_equipment_listing(
    self,
    owner_id: str,
    equipment_type: EquipmentType,
    model_name: str,
    price_per_day: float,
    available_from: datetime,
    available_to: datetime,
    condition: str = "Good",
    hp_required: Optional[str] = None
) -> EquipmentListing:
    """
    Farmer lists equipment for rent
    
    Returns: Created EquipmentListing
    """
```

**Request Rental**:
```python
def request_equipment_rental(
    self,
    renter_id: str,
    listing_id: str,
    start_date: datetime,
    end_date: datetime,
    payment_method: PaymentMethod = PaymentMethod.CASH_ON_DELIVERY
) -> RentalRequest:
    """
    Farmer requests to rent equipment
    
    Returns: Created RentalRequest (status=REQUESTED)
    """
```

**Approve Rental**:
```python
def approve_rental(
    self,
    owner_id: str,
    rental_id: str
) -> RentalRequest:
    """
    Owner approves rental request
    
    Updates status: REQUESTED → APPROVED
    """
```

### Land Pooling Methods

**Create Pool Request**:
```python
def create_land_pool_request(
    self,
    farmer_id: str,
    req_type: PoolRequestType,
    land_size: float,
    crop_pref: Optional[str] = None
) -> LandPoolRequest:
    """
    Farmer initiates land pooling request
    
    Returns: Created LandPoolRequest (status=OPEN)
    """
```

**Join Pool**:
```python
def join_land_pool(
    self,
    farmer_id: str,
    request_id: str
) -> LandPoolRequest:
    """
    Farmer joins existing land pool
    
    Adds farmer to joinedFarmers list
    Updates progressPct
    """
```

---

## Engines

### 1. EquipmentEngine (engines/equipment_engine.py)

**Purpose**: Manage equipment listings and search.

**Key Methods**:
- `create_listing(...)`: Create new equipment listing
- `list_available_equipment(district, equipment_type)`: Search nearby equipment
- `update_listing_status(listing_id, status)`: Mark as rented/available

**Search Logic**: Prioritizes same district, then nearby districts

---

### 2. RentalEngine (engines/rental_engine.py)

**Purpose**: Handle rental booking lifecycle.

**Key Methods**:
- `request_booking(renter_id, listing_id, start_date, end_date, payment_method)`: Create rental request
- `approve_request(owner_id, rental_id)`: Approve rental (owner action)
- `mark_ongoing(rental_id)`: Update status when rental starts
- `mark_completed(rental_id)`: Update status when equipment returned

**Validation**: Checks equipment availability for requested dates

---

### 3. LandPoolEngine (engines/land_pool_engine.py)

**Purpose**: Manage land pooling operations.

**Key Methods**:
- `create_pool_request(farmer_id, type, land_size, district, pincode, crop_pref)`: Create pool
- `find_matching_requests(farmer)`: Find relevant open pools nearby
- `join_pool(request_id, farmer_id)`: Add farmer to pool
- `update_pool_progress(request_id)`: Calculate progress % based on members/land

**Matching Logic**: Same district + same crop preference (if specified)

---

### 4. ResidueEngine (engines/residue_engine.py)

**Purpose**: Manage crop residue marketplace.

**Key Methods**:
- `create_residue_listing(...)`: Post residue for sale
- `list_residue_offers(district)`: Find residue buyers nearby

**Use Case**: Farmer sells crop residue (straw, stubble) instead of burning

---

### 5. ReminderEngine (engines/reminder_engine.py)

**Purpose**: Generate reminders for rental returns.

**Key Method**: `generate_rental_return_reminders(rentals)`

**Logic**:
- For each ONGOING rental
- If end_date is within 2 days: Create HIGH urgency reminder
- Reminder message: "उपकरण वापसी की तिथि: [date]"

---

### 6. ResponseBuilder (engines/response_builder.py)

**Purpose**: Build voice-first output.

**Key Method**: `build(language, equipment, rentals, pools, residue, reminders)`

**Speech Text Example (Hindi)**:
```
"आपके आस-पास 5 ट्रैक्टर किराए पर उपलब्ध हैं। 2 भूमि पूलिंग समूह जुड़ने के लिए तैयार हैं। 
आपका ट्रैक्टर किराया 2 दिनों में समाप्त होता है - कृपया वापस करें।"
```

---

## Repositories

**Implementation**: Similar pattern to other modules - MongoDB with in-memory fallback.

### Key Repos:
- **EquipmentRepo**: CRUD for equipment listings
- **RentalRepo**: CRUD for rental requests
- **LandPoolRepo**: CRUD for land pools
- **ResidueRepo**: CRUD for residue listings
- **AlertRepo**: Notifications for rental deadlines, new pool requests
- **AuditRepo**: Logging all marketplace activities

---

## Integration with Voice Agent

```python
# Voice Agent Integration

from collaborative_farming.service import CollaborativeFarmingService

service = CollaborativeFarmingService()

# Get marketplace view
output = service.run_marketplace_view(farmer_id="F001")

# Create equipment listing (voice: "मैं अपना ट्रैक्टर किराए पर देना चाहता हूं")
listing = service.create_equipment_listing(
    owner_id="F001",
    equipment_type=EquipmentType.TRACTOR,
    model_name="Mahindra 575 DI",
    price_per_day=1500.0,
    available_from=datetime(2026, 2, 1),
    available_to=datetime(2026, 2, 28),
    condition="Good",
    hp_required="50 HP"
)

# Request rental (voice: "मुझे ट्रैक्टर किराए पर चाहिए")
rental = service.request_equipment_rental(
    renter_id="F002",
    listing_id=listing.listingId,
    start_date=datetime(2026, 2, 5),
    end_date=datetime(2026, 2, 7),
    payment_method=PaymentMethod.CASH_ON_DELIVERY
)

# Create land pool (voice: "गेहूं बेचने के लिए समूह बनाना है")
pool = service.create_land_pool_request(
    farmer_id="F001",
    req_type=PoolRequestType.BULK_SELLING,
    land_size=5.0,
    crop_pref="wheat"
)
```

---

# Module Interactions

## How These Three Modules Integrate with Voice Agent

### Integration Flow

```
Voice Agent
    ↓
Intent Detection (LLM)
    ↓
┌─────────────────────┬──────────────────────┬──────────────────────┐
│                     │                      │                      │
v                     v                      v                      v
GOVERNMENT_SCHEME     FINANCE_REPORT         EQUIPMENT_RENTAL       Other Intents
    ↓                     ↓                      ↓
GovSchemesService     FinanceService         CollaborativeService
    ↓                     ↓                      ↓
GovSchemesOutput      FinanceModuleOutput    CollaborativeOutput
    ↓                     ↓                      ↓
    └─────────────────────┴──────────────────────┘
                          ↓
                    Voice Agent
                          ↓
                ┌─────────┴─────────┐
                v                   v
            UI Cards            Speech TTS
            (JSON)              (Hindi/English)
```

### Connector Pattern

Each module exposes a connector for easy voice agent integration:

**Gov Schemes Connector**:
```python
from gov_schemes.service import GovSchemesDisplayService

class GovSchemesConnector:
    def __init__(self):
        self.service = GovSchemesDisplayService()
    
    def get_schemes(self, farmer_id: str, filters: Dict = {}):
        return self.service.get_schemes_display(
            farmer_id=farmer_id,
            state=filters.get("state"),
            district=filters.get("district"),
            category=filters.get("category")
        )
```

**Financial Connector**:
```python
from financial_tracking.service import FinanceTrackingService

class FinancialConnector:
    def __init__(self):
        self.service = FinanceTrackingService()
    
    def get_report(self, farmer_id: str, season: str = "kharif"):
        return self.service.get_finance_card(farmer_id, season)
    
    def add_expense(self, farmer_id: str, category: str, amount: float):
        return self.service.add_expense(farmer_id, "kharif", category, amount)
```

**Collaborative Connector**:
```python
from collaborative_farming.service import CollaborativeFarmingService

class CollaborativeConnector:
    def __init__(self):
        self.service = CollaborativeFarmingService()
    
    def get_marketplace(self, farmer_id: str):
        return self.service.run_marketplace_view(farmer_id)
    
    def create_equipment_listing(self, owner_id: str, details: Dict):
        return self.service.create_equipment_listing(owner_id, **details)
```

---

## Common Patterns Across All Modules

### 1. Service Layer Pattern
- Single entry point via `Service` class
- Orchestrates engines and repositories
- Handles business logic coordination

### 2. Engine Pattern
- Specialized business logic components
- Single responsibility (filtering, calculation, etc.)
- Reusable across services

### 3. Repository Pattern
- Data access abstraction
- MongoDB-ready with in-memory fallback
- Supports mock data for demos

### 4. Output Models
- Pydantic models for type safety
- Voice-first design (speechText field)
- Card-based structure for UI

### 5. Multilingual Support
- Hindi/English via `language` parameter
- Bilingual field patterns (`name` + `nameHindi`)
- TTS-ready text outputs

---

## API Endpoint Design Pattern

All modules follow similar FastAPI endpoint patterns:

```python
from fastapi import APIRouter
from gov_schemes.service import GovSchemesDisplayService
from financial_tracking.service import FinanceTrackingService
from collaborative_farming.service import CollaborativeFarmingService

router = APIRouter()

# Government Schemes
@router.get("/api/v1/schemes")
async def get_schemes(farmer_id: str, category: str = None):
    service = GovSchemesDisplayService()
    return service.get_schemes_display(farmer_id, category=category)

# Financial Tracking
@router.get("/api/v1/finance/report")
async def get_finance_report(farmer_id: str, season: str = "kharif"):
    service = FinanceTrackingService()
    return service.run_finance_report(farmer_id, season)

@router.post("/api/v1/finance/expense")
async def add_expense(req: ExpenseRequest):
    service = FinanceTrackingService()
    return service.add_expense(req.farmerId, req.season, req.category, req.amount)

# Collaborative Farming
@router.get("/api/v1/collaborative/marketplace")
async def get_marketplace(farmer_id: str):
    service = CollaborativeFarmingService()
    return service.run_marketplace_view(farmer_id)

@router.post("/api/v1/collaborative/equipment")
async def create_listing(req: EquipmentRequest):
    service = CollaborativeFarmingService()
    return service.create_equipment_listing(**req.dict())
```

---

## Summary of Key Functions

### Government Schemes
1. `GovSchemesDisplayService.get_schemes_display()` - Main orchestration
2. `SchemeFetchEngine.sync_schemes()` - API sync with caching
3. `SchemeFilterEngine.filter_by_location()` - Location/category filtering
4. `SchemeAlertEngine.detect_new_schemes()` - New scheme detection
5. `SchemeAlertEngine.generate_alerts_for_farmer()` - Alert generation

### Financial Tracking
1. `FinanceTrackingService.run_finance_report()` - Complete P&L report
2. `FinanceTrackingService.add_expense()` - Record expense
3. `ProfitLossEngine.calculate()` - P&L calculation
4. `LossAnalysisEngine.analyze()` - Loss cause identification
5. `OptimizationEngine.suggest()` - Cost-saving suggestions

### Collaborative Farming
1. `CollaborativeFarmingService.run_marketplace_view()` - Marketplace dashboard
2. `CollaborativeFarmingService.create_equipment_listing()` - List equipment
3. `CollaborativeFarmingService.request_equipment_rental()` - Rent equipment
4. `CollaborativeFarmingService.create_land_pool_request()` - Start land pool
5. `RentalEngine.approve_request()` - Approve rental booking

---

## Module Dependencies

All three modules depend on:
- **Pydantic** for data validation
- **MongoDB** (optional) for persistence
- **datetime** for timestamps
- **voice_agent** module for integration

They integrate seamlessly with:
- **farm_management** module (crop data, farmer profiles)
- **voice_agent** module (intent routing, response formatting)
- **alerts** system (cross-module notifications)

---

## Testing & Debugging

Each module includes a CLI demo:

```bash
# Government Schemes Demo
python gov_schemes/cli_demo.py

# Financial Tracking Demo
python financial_tracking/cli_demo.py

# Collaborative Farming Demo
python collaborative_farming/cli_demo.py
```

These demos:
- Initialize services with mock data
- Demonstrate main workflows
- Output voice-ready responses
- Test all engines and repositories
