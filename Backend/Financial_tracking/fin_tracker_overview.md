# Financial Tracking Module

## Overview

Complete backend module for farm financial tracking with profit/loss analysis, loss cause detection, and optimization suggestions for Indian farmers.

## Features

- ✅ **Transaction Management**: Track expenses (10 categories) and income (4 categories)
- ✅ **Profit/Loss Analysis**: Complete P&L reports with margin calculations
- ✅ **Loss Cause Detection**: AI-powered identification of financial waste areas
- ✅ **Optimization Suggestions**: Actionable recommendations with estimated savings
- ✅ **Multilingual Support**: Hindi/English via voice_agent translator
- ✅ **Voice-Agent Integration**: Ready for voice-first farming assistant
- ✅ **Mock Fallback**: Reliable demo mode when DB is empty

## Quick Start

### As a Python Module

```python
from financial_tracking import get_finance_tracking_service

# Initialize service
service = get_finance_tracking_service()

# Generate financial report
output = service.run_finance_report(
    farmerId="FARMER_001",
    season="KHARIF",
    language="hi",  # Hindi or "en" for English
)

# Access results
print(output.speechText)  # Voice-ready output
print(f"Profit/Loss: ₹{output.totals.profitOrLoss:,.0f}")
print(f"Issues: {len(output.lossCauses)}")
print(f"Suggestions: {len(output.suggestions)}")

# Get voice-agent card
card = service.get_finance_card("FARMER_001", "KHARIF", "hi")
```

### CLI Demo

```bash
cd Backend
python -m financial_tracking.cli_demo
```

Choose:
- **Interactive Mode**: Full demonstration with prompts
- **Quick Test**: Automated test of both languages

## API Reference

### Main Service

```python
service = get_finance_tracking_service()
```

#### Generate Financial Report

```python
output = service.run_finance_report(
    farmerId: str,
    season: str = "KHARIF",  # KHARIF/RABI/ZAID
    language: str = "hi",    # hi/en
    force_refresh: bool = False,
) -> FinanceModuleOutput
```

Returns complete report with:
- `totals`: Income, expense, profit/loss, margin
- `topExpenseCategories`: Category breakdown
- `lossCauses`: Identified issues [with impact estimates
- `suggestions`: Actionable recommendations
- `speechText`: Voice-ready multilingual text

#### Add Expense

```python
service.add_expense(
    farmerId: str,
    season: str,
    category: str,  # SEEDS, FERTILIZER, LABOUR, etc.
    amount: float,
    notes: Optional[str] = None,
)
```

#### Add Income

```python
service.add_income(
    farmerId: str,
    season: str,
    category: str,  # SALE, SUBSIDY, INSURANCE_CLAIM, etc.
    amount: float,
    notes: Optional[str] = None,
)
```

#### Get Voice Card

```python
card = service.get_finance_card(
    farmerId: str,
    season: str = "KHARIF",
    language: str = "hi",
) -> FinanceCard
```

## Constants

### Transaction Types
- `TransactionType.EXPENSE`
- `TransactionType.INCOME`

### Expense Categories
- `ExpenseCategory.SEEDS`
- `ExpenseCategory.FERTILIZER`
- `ExpenseCategory.PESTICIDE`
- `ExpenseCategory.LABOUR`
- `ExpenseCategory.WATER`
- `ExpenseCategory.ELECTRICITY`
- `ExpenseCategory.TRANSPORT`
- `ExpenseCategory.EQUIPMENT`
- `ExpenseCategory.STORAGE`
- `ExpenseCategory.OTHER`

### Income Categories
- `IncomeCategory.SALE`
- `IncomeCategory.SUBSIDY`
- `IncomeCategory.INSURANCE_CLAIM`
- `IncomeCategory.OTHER`

### Seasons
- `SeasonType.KHARIF` - Monsoon (Jun-Oct)
- `SeasonType.RABI` - Winter (Nov-Mar)
- `SeasonType.ZAID` - Summer (Mar-Jun)

## Data Models

### FinanceTransaction
- `transactionId`, `farmerId`, `season`
- `type`: EXPENSE/INCOME
- `category`: Expense or income category
- `amount`, `currency`, `notes`
- `ts`, `createdAt`, `updatedAt`

### FinanceTotals
- `farmerId`, `season`
- `totalExpense`, `totalIncome`
- `profitOrLoss`, `profitMarginPct`

### LossCause
- `title`, `description`
- `impactAmount`: Potential savings
- `confidenceScore`: 0-1

### OptimizationSuggestion
- `suggestionTitle`, `whyThisHelps`
- `estimatedSavings`
- `priority`: 1-5 (1 is highest)
- `actionableSteps`: List of steps

## Integration with Voice Agent

The module uses `voice_agent.input_processing.translator` for proper Hindi/English translation:

```python
# Automatic translation in response_builder.py
from voice_agent.input_processing.translator import get_translator

translator = get_translator()
hindi_text = translator.english_to_hindi("Your profit is ₹5000")
```

## Integration with FastAPI (Future)

```python
from fastapi import APIRouter
from financial_tracking import get_finance_tracking_service

router = APIRouter(prefix="/api/finance")

@router.get("/report/{farmer_id}")
async def get_report(farmer_id: str, season: str, language: str = "hi"):
    service = get_finance_tracking_service()
    output = service.run_finance_report(farmer_id, season, language)
    return output.dict()

@router.post("/expense")
async def add_expense(data: dict):
    service = get_finance_tracking_service()
    return service.add_expense(**data)
```

## Architecture

```
financial_tracking/
├── constants.py         # Enums & constants
├── models.py            # Pydantic schemas
├── service.py           # Main orchestrator
├── repositories/        # Data access layer
│   ├── transaction_repo.py
│   ├── summary_repo.py
│   └── crop_repo.py
└── engines/             # Business logic
    ├── ledger_engine.py
    ├── profit_loss_engine.py
    ├── loss_analysis_engine.py
    ├── optimization_engine.py
    └── response_builder.py
```

## Example Output

### Hindi Speech Text
```
आपको KHARIF सीजन में 4,500 रुपये की हानि हुई है। 
आपकी कुल आय 83,000 रुपये थी, लेकिन खर्च 87,500 रुपये आया। 
सबसे ज़्यादा खर्च मजदूरी पर 28,500 रुपये (32.6%) आया। 
सुझाव: Mechanization & Efficient Labour Management। 
इससे लगभग 4,275 रुपये बचा सकते हैं।
```

### Loss Causes Detected
1. **High Labour Costs** - Impact: ₹4,275
2. **Excessive Fertilizer Use** - Impact: ₹4,200
3. **Low Selling Price** - Impact: ₹2,250

### Optimization Suggestions
1. **Mechanization & Labour Management** (Priority 1)
   - Estimated Savings: ₹4,275
   - Steps: Rent harvester, use seed drill, plan labour advance

2. **Soil Testing & Balanced Fertilizer** (Priority 1)
   - Estimated Savings: ₹4,200
   - Steps: Get soil health card, apply based on tests, buy bulk

## Design Principles

1. **Mock Data ONLY as Fallback**: Real data always prioritized
2. **Voice-First**: Natural speech text generation
3. **Indian Context**: Realistic amounts, categories, schemes
4. **Hackathon-Ready**: Never fails, graceful fallbacks
5. **Clean Architecture**: Repositories, engines, services separation

## Dependencies

- `pydantic` - Data validation
- `voice_agent` (optional) - For translation

## Testing

Run CLI demo to test all features:
```bash
python -m financial_tracking.cli_demo
```

## License

Part of HackVision_KisaanMitra project

## Support

For issues or questions, refer to the [walkthrough.md](file:///C:/Users/Bhavik%20Sheth/.gemini/antigravity/brain/24f57747-c8aa-45d6-a3dc-cee1e4c28a5d/walkthrough.md) for detailed implementation documentation.
