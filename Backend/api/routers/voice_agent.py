from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Body
from typing import Optional
import os
import shutil

from Backend.api.dependencies import get_db_client, get_current_user
from Backend.Voice_agent.core.agent import get_voice_agent
from Backend.Voice_agent.input_processing.speech_to_text import get_speech_to_text, WhisperSTT as SpeechToText

router = APIRouter()

@router.post("/voice/process")
async def process_voice_input(
    text: Optional[str] = Form(None),
    audio: Optional[UploadFile] = File(None),
    session_id: Optional[str] = Form(None),
    farmer_id: Optional[str] = Form(None),
    db_client = Depends(get_db_client),
    current_user = Depends(get_current_user)
):
    """
    Process voice or text input for the conversational agent.
    If audio is provided, it is transcribed first.
    """
    try:
        # Resolve Farmer ID
        fid = farmer_id or current_user.get("id", "F001")
        
        # Initialize Agent
        agent = get_voice_agent(db_client=db_client)
        
        input_text = text
        
        # Handle Audio Transcribing
        if audio:
            stt = SpeechToText()
            
            # Save temp file
            temp_dir = "temp_voice"
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, audio.filename or "input.wav")
            
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(audio.file, buffer)
            
            # Transcribe (assuming Hindi input)
            input_text = stt.transcribe(temp_path, language="hi-IN")
            
            # Cleanup
            os.remove(temp_path)
            
        if not input_text:
            raise HTTPException(status_code=400, detail="No text or audio input provided")
            
        # Process through Agent
        response = agent.process_input(
            hindi_text=input_text,
            farmer_id=fid,
            session_id=session_id
        )
        
        return response.to_dict()
        
    except Exception as e:
        # Clean cleanup just in case
        if audio and 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))
