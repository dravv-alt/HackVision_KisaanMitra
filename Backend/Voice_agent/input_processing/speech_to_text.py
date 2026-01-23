"""
Speech-to-Text Module - Whisper Implementation
Uses OpenAI Whisper for Hindi speech recognition
"""

import whisper
import numpy as np
from typing import Union, Optional
import io


class WhisperSTT:
    """
    Speech-to-Text using OpenAI Whisper
    Supports Hindi language recognition
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize Whisper STT
        
        Args:
            model_name: Whisper model (tiny, base, small, medium, large)
                       If None, uses WHISPER_MODEL from config (default: base)
                       - tiny: Fastest, least accurate
                       - base: Good balance (recommended for hackathon)
                       - small: Better accuracy
                       - medium/large: Best accuracy, slower
        """
        # Check FFmpeg availability first
        import subprocess
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, timeout=5)
        except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
            raise RuntimeError(
                "FFmpeg not found. Whisper requires FFmpeg to process audio.\\n"
                "Install FFmpeg: https://ffmpeg.org/download.html\\n"
                "Add ffmpeg.exe to your system PATH, or use: choco install ffmpeg"
            )
        
        # Auto-detect model from config if not specified
        if model_name is None:
            from Backend.Voice_agent.config import get_config
            config = get_config()
            model_name = config.whisper_model
        
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model"""
        try:
            print(f"🔄 Loading Whisper model '{self.model_name}'...")
            self.model = whisper.load_model(self.model_name)
            print(f"✅ Whisper model '{self.model_name}' loaded successfully")
        except Exception as e:
            print(f"❌ Error loading Whisper model: {e}")
            raise
    
    def transcribe(
        self,
        audio_data: Union[str, bytes, np.ndarray],
        language: str = None  # None = precise auto-detection
    ) -> str:
        """
        Transcribe audio to text
        
        Args:
            audio_data: Audio file path, bytes, or numpy array
            language: Language code (default: "hi" for Hindi)
        
        Returns:
            Transcribed text in Hindi
        """
        if self.model is None:
            raise RuntimeError("Whisper model not loaded")
        
        try:
            # Transcribe with Whisper
            result = self.model.transcribe(
                audio_data,
                language=language,
                fp16=False  # Use FP32 for CPU compatibility
            )
            
            transcribed_text = result["text"].strip()
            print(f"✅ Transcription: {transcribed_text}")
            
            return transcribed_text
            
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            raise
    
    def transcribe_from_file(self, audio_file_path: str) -> str:
        """
        Transcribe from audio file
        
        Args:
            audio_file_path: Path to audio file (mp3, wav, m4a, etc.)
        
        Returns:
            Transcribed Hindi text
        """
        return self.transcribe(audio_file_path, language="hi")
    
    def transcribe_from_bytes(self, audio_bytes: bytes) -> str:
        """
        Transcribe from audio bytes
        
        Args:
            audio_bytes: Audio data as bytes
        
        Returns:
            Transcribed Hindi text
        """
        # Save bytes to temporary file for Whisper
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name
        
        try:
            result = self.transcribe(temp_path, language="hi")
            return result
        finally:
            # Clean up temp file
            import os
            os.unlink(temp_path)


# Singleton instance
_stt = None

def get_speech_to_text(model_name: str = None) -> WhisperSTT:
    """
    Get or create Speech-to-Text instance
    Auto-detects model from config if not specified
    
    Args:
        model_name: Whisper model name (optional, uses config default)
    
    Returns:
        WhisperSTT instance
    """
    global _stt
    if _stt is None:
        _stt = WhisperSTT(model_name=model_name)
    return _stt
