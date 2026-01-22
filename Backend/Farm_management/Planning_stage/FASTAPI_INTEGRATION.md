# FastAPI Integration Guide

## Quick Integration Example

Here's how to integrate the Planning Stage module with FastAPI:

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional

from Backend.Farm_management.Planning_stage import (
    PreSeedingService, 
    PlanningRequest, 
    PreSeedingOutput,
    Season,
    RiskPreference
)

app = FastAPI(
    title="KisaanMitra - Planning API",
    description="Pre-seeding planning recommendations for farmers",
    version="1.0.0"
)

# Initialize service (singleton pattern)
planning_service = PreSeedingService()


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.post("/api/v1/planning/recommend", response_model=PreSeedingOutput)
async def get_planning_recommendations(request: PlanningRequest):
    """
    Get complete pre-seeding planning recommendations
    
    - **farmer_id**: Unique farmer identifier
    - **season**: Optional (auto-detects if not provided)
    - **risk_preference**: safe | balanced | high_profit
    """
    try:
        output = planning_service.run(request)
        return output
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/v1/planning/crops/{farmer_id}")
async def get_crop_recommendations(
    farmer_id: str,
    season: Optional[Season] = None,
    risk_preference: RiskPreference = RiskPreference.BALANCED
):
    """Get only crop recommendations"""
    try:
        request = PlanningRequest(
            farmer_id=farmer_id,
            season=season,
            risk_preference=risk_preference
        )
        output = planning_service.run(request)
        return {"crops": output.crop_cards}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/v1/planning/schemes/{farmer_id}")
async def get_scheme_eligibility(farmer_id: str):
    """Get government scheme eligibility"""
    try:
        request = PlanningRequest(farmer_id=farmer_id)
        output = planning_service.run(request)
        
        eligible = [s for s in output.scheme_cards if s.eligible]
        not_eligible = [s for s in output.scheme_cards if not s.eligible]
        
        return {
            "eligible_schemes": eligible,
            "not_eligible_schemes": not_eligible[:5]  # Top 5
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/v1/planning/voice-output/{farmer_id}")
async def get_voice_output(
    farmer_id: str,
    language: str = "hi"
):
    """Get voice-first output for voice assistant"""
    try:
        request = PlanningRequest(farmer_id=farmer_id)
        output = planning_service.run(request)
        
        speech = output.speech_text_hi if language == "hi" else output.speech_text
        
        return {
            "speech_text": speech,
            "urgency_level": output.urgency_level,
            "language": language,
            "top_crop": output.crop_cards[0].crop_name if output.crop_cards else None,
            "eligible_schemes_count": len([s for s in output.scheme_cards if s.eligible])
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "planning_stage"}


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Usage Examples

### 1. Complete Planning Request

```bash
curl -X POST "http://localhost:8000/api/v1/planning/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "farmer_id": "F001",
    "season": "kharif",
    "risk_preference": "balanced"
  }'
```

### 2. Get Crops Only

```bash
curl "http://localhost:8000/api/v1/planning/crops/F001?risk_preference=high_profit"
```

### 3. Get Scheme Eligibility

```bash
curl "http://localhost:8000/api/v1/planning/schemes/F001"
```

### 4. Get Voice Output (Hindi)

```bash
curl "http://localhost:8000/api/v1/planning/voice-output/F001?language=hi"
```

## Running the Server

```bash
# Install FastAPI and uvicorn
pip install fastapi uvicorn

# Run the server
python api_server.py

# Or with uvicorn directly
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `404`: Farmer not found
- `422`: Invalid request format
- `500`: Internal server error

## CORS Configuration

For frontend integration, add CORS middleware:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api_server:app
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install fastapi uvicorn pydantic

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Next Steps

1. Add authentication (JWT tokens)
2. Add rate limiting
3. Add request logging
4. Configure production database
5. Add caching for weather data
6. Set up monitoring (e.g., Prometheus)
