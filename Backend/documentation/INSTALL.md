# Backend Requirements - Installation Guide

## Quick Install

```bash
cd Backend
pip install -r requirements.txt
```

## What's Included

This single `requirements.txt` contains ALL dependencies for:
- ✅ Voice Agent (Whisper, Argos Translate, Groq/Gemini, LangGraph)
- ✅ Farm Management (Planning, Farming, Post-Harvest stages)
- ✅ Database (MongoDB)
- ✅ API (FastAPI)
- ✅ Testing & Development tools

## Core Dependencies

### Voice Agent
- `openai-whisper` - Speech-to-text
- `argostranslate` - Offline translation
- `groq` - Groq LLM client
- `google-generativeai` - Gemini client
- `langgraph` - Agent orchestration

### Farm Management
- `numpy`, `pandas`, `scikit-learn` - Data processing
- `pydantic` - Data validation

### Database & Storage
- `pymongo` - MongoDB client

### Utilities
- `python-dotenv` - Environment variables
- `requests` - HTTP requests
- `fastapi` - API framework

## Installation Notes

### For CPU-only (no GPU)
```bash
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
```

### For GPU (CUDA)
```bash
pip install -r requirements.txt
```

### Minimal Install (Voice Agent only)
```bash
pip install openai-whisper argostranslate groq google-generativeai python-dotenv pydantic
```

## Troubleshooting

### Whisper Installation Issues
If Whisper fails to install:
```bash
pip install --upgrade pip setuptools wheel
pip install openai-whisper
```

### Argos Translate Issues
```bash
pip install argostranslate --no-deps
pip install argostranslate
```

### Torch/Torchaudio Issues
For CPU-only systems:
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## Verify Installation

```bash
python -c "import whisper; import argostranslate; print('✅ All core dependencies installed')"
```
