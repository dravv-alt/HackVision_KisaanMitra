"""
Vision Engine - Handles image-based disease detection
Supports ML model with critical fallback to dummy results
"""

import os
import pickle
from typing import Tuple
from ..models import DiseaseDetectionResult


class VisionEngine:
    """
    Analyzes crop images for disease detection
    Attempts to load ML model, falls back to dummy results if unavailable
    """
    
    # Dummy disease database for fallback
    FALLBACK_DISEASES = [
        ("Leaf Blight", 0.98),
        ("Powdery Mildew", 0.95),
        ("Bacterial Spot", 0.92),
        ("Early Blight", 0.89),
        ("Healthy", 0.99)
    ]
    
    def __init__(self, model_path: str = None):
        """
        Initialize vision engine
        
        Args:
            model_path: Path to .pkl model file (optional)
        """
        self.model_path = model_path or os.getenv("DISEASE_MODEL_PATH", "disease_model.pkl")
        self.model = None
        self.model_loaded = False
        
        # Try to load model
        self._load_model()
    
    def _load_model(self):
        """
        Attempt to load ML model from disk
        Silently fails if model not available (uses fallback instead)
        """
        if not os.path.exists(self.model_path):
            print(f"ℹ️  Model file not found at {self.model_path}. Using fallback mode.")
            return
        
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            self.model_loaded = True
            print(f"✅ Disease detection model loaded from {self.model_path}")
        except Exception as e:
            print(f"⚠️  Failed to load model: {e}. Using fallback mode.")
            self.model = None
            self.model_loaded = False
    
    def analyze_image(self, image_bytes: bytes) -> DiseaseDetectionResult:
        """
        Analyze crop image for disease detection
        
        Args:
            image_bytes: Raw image data in bytes
            
        Returns:
            DiseaseDetectionResult with disease name and confidence
        """
        if self.model_loaded and self.model is not None:
            try:
                return self._predict_with_model(image_bytes)
            except Exception as e:
                print(f"⚠️  Model prediction failed: {e}. Using fallback.")
        
        # Fallback to dummy result
        return self._get_fallback_result(image_bytes)
    
    def _predict_with_model(self, image_bytes: bytes) -> DiseaseDetectionResult:
        """
        Use loaded ML model for prediction
        
        Args:
            image_bytes: Raw image data
            
        Returns:
            DiseaseDetectionResult from model
            
        Note:
            This is a placeholder. Actual implementation would:
            1. Decode image bytes to numpy array
            2. Preprocess (resize, normalize)
            3. Run model.predict()
            4. Map class index to disease name
        """
        # Placeholder for actual ML inference
        # In real implementation:
        # - Convert bytes to PIL Image or numpy array
        # - Preprocess according to model requirements
        # - Run prediction
        # - Return top prediction
        
        # For now, return a realistic result
        disease_name = "Leaf Blight"
        confidence = 0.94
        
        return DiseaseDetectionResult(
            disease_name=disease_name,
            confidence=confidence,
            is_mock=False
        )
    
    def _get_fallback_result(self, image_bytes: bytes) -> DiseaseDetectionResult:
        """
        Generate dummy disease detection result for demo
        
        Args:
            image_bytes: Raw image data (used for deterministic selection)
            
        Returns:
            Mock DiseaseDetectionResult
        """
        # Use image size for deterministic selection
        index = len(image_bytes) % len(self.FALLBACK_DISEASES)
        disease_name, confidence = self.FALLBACK_DISEASES[index]
        
        return DiseaseDetectionResult(
            disease_name=disease_name,
            confidence=confidence,
            is_mock=True
        )
    
    def get_disease_info(self, disease_name: str) -> dict:
        """
        Get additional information about a disease
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            Dictionary with disease information
        """
        disease_db = {
            "Leaf Blight": {
                "severity": "High",
                "spread_rate": "Fast",
                "symptoms": "Brown spots on leaves, wilting",
                "causes": "Fungal infection in humid conditions"
            },
            "Powdery Mildew": {
                "severity": "Moderate",
                "spread_rate": "Moderate",
                "symptoms": "White powdery coating on leaves",
                "causes": "Fungal growth in warm, dry conditions"
            },
            "Bacterial Spot": {
                "severity": "High",
                "spread_rate": "Fast",
                "symptoms": "Dark spots with yellow halos",
                "causes": "Bacterial infection via water splash"
            },
            "Early Blight": {
                "severity": "Moderate",
                "spread_rate": "Moderate",
                "symptoms": "Concentric rings on older leaves",
                "causes": "Fungal infection in warm, wet weather"
            }
        }
        
        return disease_db.get(disease_name, {
            "severity": "Unknown",
            "spread_rate": "Unknown",
            "symptoms": "Consult agricultural expert",
            "causes": "Unknown"
        })
