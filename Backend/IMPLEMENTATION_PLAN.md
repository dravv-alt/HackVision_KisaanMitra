# FastAPI Implementation Plan

## Overview
This plan outlines the steps to build the FastAPI application for KisaanMitra, exposing the 5 core backend modules via REST endpoints.

## 1. Project Structure

We will use the existing `Backend/` directory as the root. The FastAPI specific code will reside in `Backend/api/`.

```
Backend/
├── api/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Global configuration (env vars)
│   ├── dependencies.py      # Dependency injection (e.g., user auth, db)
│   └── routers/             # API Routers
│       ├── __init__.py
│       ├── farm_management.py
│       ├── voice_agent.py
│       ├── gov_schemes.py
│       ├── financial.py
│       └── collaborative.py
├── requirements.txt
└── .env                     # Environment variables
```

## 2. Dependencies

The `requirements.txt` already contains:
- `fastapi>=0.104.0`
- `uvicorn>=0.24.0`
- `pydantic>=2.0.0`
- `python-dotenv>=1.0.0`
- `pymongo`, `chromadb`, etc.

## 3. Configuration (`api/config.py`)

Will define a `Settings` class using `pydantic-settings` to manage:
- API Prefix (`/api/v1`)
- Project Name
- CORS Origins
- MongoDB URL
- External API Keys (OpenWeather, LLMs)

## 4. Routers & Endpoints Specification

### A. Farm Management (`routers/farm_management.py`)
- **POST** `/planning/pre-seeding`: Get crop plan (Input: `PlanningRequest`)
- **POST** `/farming/disease-detect`: Upload image for detection
- **GET** `/farming/market-price`: Get prices
- **POST** `/post-harvest/plan`: Get harvest plan

### B. Voice Agent (`routers/voice_agent.py`)
- **POST** `/voice/process`: Main voice input processing (Input: text/audio, Output: `AgentResponse`)

### C. Gov Schemes (`routers/gov_schemes.py`)
- **GET** `/schemes`: Get schemes details/alerts
- **GET** `/schemes/{scheme_id}`: Get specific scheme details

### D. Financial Tracking (`routers/financial.py`)
- **GET** `/finance/report`: Get P&L report
- **POST** `/finance/transaction`: Add expense/income

### E. Collaborative Farming (`routers/collaborative.py`)
- **GET** `/collaborative/marketplace`: Get marketplace dashboard
- **POST** `/collaborative/equipment`: List equipment
- **POST** `/collaborative/rental`: Request rental
- **POST** `/collaborative/land-pool`: Create land pool request

## 5. Security & Dependencies (`api/dependencies.py`)
- `get_current_user`: Mock or simple header-based auth for now (as per hackathon scope).
- `get_db`: MongoDB connection dependency.

## 6. Implementation Steps
1.  **Environment**: Verify `.env` and `requirements.txt`.
2.  **Core**: Create `api/config.py` and `api/dependencies.py`.
3.  **Routers**: Implement each router file importing services from sibling modules.
4.  **Main**: Create `api/main.py` assembling the app.
5.  **Test**: Launch with `uvicorn api.main:app --reload`.

