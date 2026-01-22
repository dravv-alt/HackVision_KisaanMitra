# KisaanMitra FastAPI Backend

This is the main backend API for the KisaanMitra application, consolidating various modules into a unified REST interface.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- MongoDB (running locally or URI in .env)
- Environment variables configured in `.env` inside `Backend/` directory.

### Installation

Dependencies are listed in `Backend/requirements.txt`.

```bash
cd Backend
pip install -r requirements.txt
```

### Running the Server

Run the following command from the `Backend` directory:

```bash
python -m api.main
```

The server will start at `http://localhost:8000`.

## 📚 API Documentation

Once running, access the interactive documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🛠️ API Structure

The API is organized into the following routers:

1.  **Farm Management** (`/api/v1/planning`, `/api/v1/farming`, `/api/v1/post-harvest`)
    - Crop planning, disease detection, market prices, post-harvest advice.
2.  **Voice Agent** (`/api/v1/voice`)
    - Main entry point for voice/text processing via the intelligent agent.
3.  **Government Schemes** (`/api/v1/schemes`)
    - List and filter government schemes, check eligibility.
4.  **Financial Tracking** (`/api/v1/finance`)
    - Manage expenses/income, generate P&L reports.
5.  **Collaborative Farming** (`/api/v1/collaborative`)
    - Marketplace for equipment rental and land pooling.

## 🧪 Testing

You can test the health of the API:

```bash
curl http://localhost:8000/health
```

Expected response: `{"status": "healthy"}`
