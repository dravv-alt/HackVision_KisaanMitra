from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import Optional
from pydantic import BaseModel
import os
import shutil

from Backend.api.dependencies import get_db_client, get_current_user
from Backend.Voice_agent.core.agent import get_voice_agent
from Backend.Voice_agent.input_processing.speech_to_text import get_speech_to_text, WhisperSTT as SpeechToText

router = APIRouter()

class VoiceTextRequest(BaseModel):
    """Request model for text-based voice agent input"""
    hindi_text: str
    farmer_id: Optional[str] = None
    session_id: Optional[str] = None

@router.post("/voice/process")
async def process_voice_input(
    request: VoiceTextRequest,
    db_client = Depends(get_db_client),
    current_user = Depends(get_current_user)
):
    """
    Process text input for the conversational voice agent.
    
    Request body:
    {
        "hindi_text": "मेरी फसल में बीमारी है",
        "farmer_id": "F001",  // optional
        "session_id": "abc123"  // optional
    }
    """
    try:
        # Resolve Farmer ID
        fid = request.farmer_id or current_user.get("id", "F001")
        sid = request.session_id
        
        # Initialize Agent
        agent = get_voice_agent(db_client=db_client)
        
        # Process through Agent
        response = agent.process_input(
            hindi_text=request.hindi_text,
            farmer_id=fid,
            session_id=sid
        )
        
        return response.to_dict()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice/process-audio")
async def process_audio_input(
    audio: UploadFile = File(...),
    farmer_id: Optional[str] = None,
    session_id: Optional[str] = None,
    db_client = Depends(get_db_client),
    current_user = Depends(get_current_user)
):
    """
    Process audio input for the conversational voice agent.
    Upload an audio file (wav, mp3, m4a, etc.) and it will be transcribed.
    """
    temp_path = None
    try:
        # Initialize STT
        stt = SpeechToText()
        
        # Save temp file
        temp_dir = "temp_voice"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, audio.filename or "input.wav")
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        
        # Transcribe (auto-detect language)
        hindi_text = stt.transcribe(temp_path, language=None)
        
        # Cleanup temp file
        os.remove(temp_path)
        temp_path = None
        
        # Resolve Farmer ID
        fid = farmer_id or current_user.get("id", "F001")
        
        # Initialize Agent
        agent = get_voice_agent(db_client=db_client)
        
        # Process through Agent
        response = agent.process_input(
            hindi_text=hindi_text,
            farmer_id=fid,
            session_id=session_id
        )
        
        response_dict = response.to_dict()
        response_dict["transcription"] = hindi_text
        return response_dict
        
    except Exception as e:
        # Clean up temp file on error
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))
