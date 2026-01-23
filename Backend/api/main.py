from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .config import settings
from .routers import (
    farm_management,
    voice_agent,
    gov_schemes,
    financial,
    collaborative,
    dashboard,
    inventory
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Backend API for KisaanMitra - Voice-First Farming Assistant",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Authentication"])
app.include_router(onboarding.router, prefix=settings.API_V1_STR, tags=["Onboarding"])
app.include_router(inventory.router, prefix=settings.API_V1_STR, tags=["Inventory"])
app.include_router(crops.router, prefix=settings.API_V1_STR, tags=["Active Crops"])
app.include_router(calendar.router, prefix=settings.API_V1_STR, tags=["Calendar"])
app.include_router(alerts.router, prefix=settings.API_V1_STR, tags=["Alerts"])
app.include_router(farm_management.router, prefix=settings.API_V1_STR, tags=["Farm Management"])
app.include_router(voice_agent.router, prefix=settings.API_V1_STR, tags=["Voice Agent"])
app.include_router(gov_schemes.router, prefix=settings.API_V1_STR, tags=["Government Schemes"])
app.include_router(financial.router, prefix=settings.API_V1_STR, tags=["Financial Tracking"])
app.include_router(collaborative.router, prefix=settings.API_V1_STR, tags=["Collaborative Farming"])
app.include_router(dashboard.router, prefix=settings.API_V1_STR, tags=["Dashboard"])
app.include_router(inventory.router, prefix=settings.API_V1_STR, tags=["Inventory"])

# Mount static files for uploads (optional)
# os.makedirs("temp_uploads", exist_ok=True)
# app.mount("/static", StaticFiles(directory="temp_uploads"), name="static")

@app.get("/")
def read_root():
    return {
        "project": settings.PROJECT_NAME,
        "status": "running",
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
