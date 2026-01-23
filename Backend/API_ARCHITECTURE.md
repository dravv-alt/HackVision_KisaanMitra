# API Architecture & Data Flow Analysis

This document provides a visual and logical breakdown of the KisaanMitra FastAPI application (`api/main.py`), detailing how data flows from user requests through the system's various layers.

## 1. High-Level System Architecture

The application follows a **Vertical Slice Architecture**, separating distinct domains (Farm Management, Voice Agent, Financials) into their own self-contained services and engines.

### Visual Data Flow

The following diagram illustrates the path of a request from the user (farmer) effectively interacting with the different layers of the backend.

```mermaid
graph TD
    %% Actors
    User((Farmer/User))

    %% Framework Layer
    subgraph "FastAPI Application (api/main.py)"
        Auth[Auth Dependency] 
        Router_Voice["/voice/process"]
        Router_Plan["/planning/pre-seeding"]
        Router_Farm["/farming/disease-detect"]
        Router_Harvest["/post-harvest/plan"]
    end

    %% Input Processing Layer
    subgraph "Input Processing"
        STT[Whisper STT<br/>(Audio -> Text)]
        TempFile[Temp File Storage]
    end

    %% Intelligence Layer (Engines)
    subgraph "Business Logic / Engines"
        VoiceCore[Voice Agent]
        PlanService[Pre-Seeding Service]
        Vision[Vision Engine<br/>(Disease Detection)]
        Market[Post-Harvest Engine]
    end

    %% Infrastructure Layer
    subgraph "Data Persistence"
        DB[(MongoDB)]
        Models[Data Models]
    end

    %% Flows
    User --> |"1. Audio/Text Input"| Router_Voice
    User --> |"1. Upload Image"| Router_Farm
    User --> |"1. Form Data"| Router_Plan

    %% Voice Flow
    Router_Voice --> |"2. Save Audio"| TempFile
    TempFile --> |"3. Transcribe"| STT
    STT --> |"4. Text Query"| VoiceCore
    VoiceCore --> |"5. Fetch Context"| DB
    VoiceCore --> |"6. JSON Response"| User

    %% Vision Flow
    Router_Farm --> |"2. Save Image"| TempFile
    TempFile --> |"3. Analyze Path"| Vision
    Vision --> |"4. Diagnosis"| User

    %% Planning Flow
    Router_Plan --> |"2. Request Object"| PlanService
    PlanService --> |"3. Optimization"| Models
    Models --> |"4. Plan Data"| User
```

---

## 2. Detailed Data Flows

### A. Disease Detection (`/farming/disease-detect`)
This flow handles image processing for plant pathology.

1.  **Trigger**: User uploads an image of a crop leaf.
2.  **API Layer**:
    *   Endpoint receives `UploadFile`.
    *   `get_current_user` dependency ensures authentication.
3.  **I/O Operations**:
    *   The image stream is written to a local `temp_uploads/` directory.
4.  **Engine Layer**:
    *   `VisionEngine` is initialized.
    *   The engine reads the file from the temp path and runs inference (likely TensorFlow/PyTorch).
5.  **Cleanup**:
    *   The temporary file is deleted `os.remove()` to prevent storage bloat.
6.  **Response**: JSON result containing disease name, confidence, and cure.

### B. Voice Commands (`/voice/process` and `/voice/process-audio`)
This flow powers the "Voice-First" experience with separate endpoints for text and audio.

#### B1. Text Input (`/voice/process`)
1.  **Trigger**: User submits text query via JSON request body.
2.  **API Layer**: 
    *   Accepts JSON with `hindi_text`, `farmer_id` (optional), `session_id` (optional).
    *   Using Pydantic `VoiceTextRequest` model for validation.
3.  **Agent Layer**:
    *   `VoiceAgent` receives the text directly.
    *   Queries LLM (Gemini/Groq) to understand intent.
    *   Fetches context from MongoDB (user location, past crops, session history).
4.  **Response**: JSON with cards, explanations (Hindi/English), and reasoning.

#### B2. Audio Input (`/voice/process-audio`)
1.  **Trigger**: User uploads audio file (wav, mp3, m4a).
2.  **API Layer**:
    *   Accepts multipart/form-data with `audio` file.
    *   Optional `farmer_id` and `session_id` as form fields.
3.  **Audio Processing**:
    *   File saved to `temp_voice/` temporarily.
    *   `WhisperSTT` transcribes audio to Hindi text (requires FFmpeg).
    *   Temporary file deleted after transcription.
4.  **Agent Layer** (same as text input):
    *   Transcribed text sent to `VoiceAgent`.
    *   LLM intent classification and RAG retrieval.
5.  **Response**: Same JSON format as text endpoint.

### C. Crop Planning (`/planning/pre-seeding`)
This flow provides agronomic advice based on land parameters.

1.  **Trigger**: User sends a JSON payload (Soil Type, Land Size, Season).
2.  **Service Layer**:
    *   `PreSeedingService` is instantiated with the `db_client`.
3.  **Business Logic**:
    *   Analyzes soil compatibility and seasonality.
    *   Checks for government schemes (if integrated).
4.  **Data Layer**:
    *   Uses Mock Repositories (if DB is empty/disconnected) purely as fallback.
5.  **Response**: A `PreSeedingOutput` model containing recommended crops over a timeline.

---

## 3. Key Technical Observations

1.  **Temp File Management**:
    *   Files are manually created and deleted in controllers (`shutil.copyfileobj`, `os.remove`).
    *   *Recommendation*: Move this to a context manager utility to handle cleanup automatically, even if errors occur during processing.

2.  **Dependency Injection**:
    *   The app heavily uses FastAPI's `Depends` for database connections (`get_db_client`) and Auth (`get_current_user`). This ensures statelessness and easier testing.

3.  **Modular Routing**:
    *   `api/main.py` is kept thin. All logic is delegated to `api/routers/`, which further delegates to `engines/` or `services/`. This is clean SOLID design.
