"""
Vision Engine - Handles image-based disease detection
Supports Keras/TensorFlow model with critical fallback to dummy results
"""

import os
import io
import numpy as np
from typing import Tuple, Optional
from ..models import DiseaseDetectionResult

# Optional imports for Keras model support
try:
    from tensorflow import keras
    from PIL import Image
    KERAS_AVAILABLE = True
except ImportError:
    KERAS_AVAILABLE = False
    print("⚠️  TensorFlow/Keras not available. Install with: pip install tensorflow")


class VisionEngine:
    """
    Analyzes crop images for disease detection
    Attempts to load Keras model, falls back to dummy results if unavailable
    """
    
    # Dummy disease database for fallback
    FALLBACK_DISEASES = [
        ("Leaf Blight", 0.98),
        ("Powdery Mildew", 0.95),
        ("Bacterial Spot", 0.92),
        ("Early Blight", 0.89),
        ("Healthy", 0.99)
    ]
    
    # Default class names for plant disease model
    # Update this list based on your actual model's classes
    DEFAULT_CLASS_NAMES = [
        "Apple___Apple_scab",
        "Apple___Black_rot",
        "Apple___Cedar_apple_rust",
        "Apple___healthy",
        "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        "Corn_(maize)___Common_rust_",
        "Corn_(maize)___Northern_Leaf_Blight",
        "Corn_(maize)___healthy",
        "Grape___Black_rot",
        "Grape___Esca_(Black_Measles)",
        "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
        "Grape___healthy",
        "Potato___Early_blight",
        "Potato___Late_blight",
        "Potato___healthy",
        "Tomato___Bacterial_spot",
        "Tomato___Early_blight",
        "Tomato___Late_blight",
        "Tomato___Leaf_Mold",
        "Tomato___Septoria_leaf_spot",
        "Tomato___Spider_mites Two-spotted_spider_mite",
        "Tomato___Target_Spot",
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "Tomato___Tomato_mosaic_virus",
        "Tomato___healthy"
    ]
    
    def __init__(self, model_path: str = None, class_names: list = None):
        """
        Initialize vision engine
        
        Args:
            model_path: Path to .keras model file (optional)
            class_names: List of class names corresponding to model output (optional)
        """
        self.model_path = model_path or os.getenv(
            "DISEASE_MODEL_PATH", 
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "plant_disease_recog_model_pwp.keras")
        )
        self.class_names = class_names or self.DEFAULT_CLASS_NAMES
        self.model = None
        self.model_loaded = False
        
        # Try to load model
        self._load_model()
    
    def _load_model(self):
        """
        Attempt to load Keras model from disk
        Silently fails if model not available (uses fallback instead)
        """
        if not KERAS_AVAILABLE:
            print("ℹ️  TensorFlow/Keras not installed. Using fallback mode.")
            return
            
        if not os.path.exists(self.model_path):
            print(f"ℹ️  Model file not found at {self.model_path}. Using fallback mode.")
            return
        
        try:
            self.model = keras.models.load_model(self.model_path)
            self.model_loaded = True
            print(f"✅ Disease detection model loaded from {self.model_path}")
            print(f"   Model input shape: {self.model.input_shape}")
            print(f"   Number of classes: {len(self.class_names)}")
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
        Use loaded Keras model for prediction
        
        Args:
            image_bytes: Raw image data
            
        Returns:
            DiseaseDetectionResult from model
        """
        # 1. Decode image bytes to PIL Image
        img = Image.open(io.BytesIO(image_bytes))
        
        # 2. Get target size from model input shape
        target_size = self.model.input_shape[1:3]  # (height, width)
        
        # 3. Preprocess image
        img = img.convert('RGB')  # Ensure RGB format
        img = img.resize(target_size)  # Resize to model's expected input
        img_array = np.array(img)
        
        # 4. Normalize pixel values (0-255 to 0-1)
        img_array = img_array.astype('float32') / 255.0
        
        # 5. Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        # 6. Run prediction
        predictions = self.model.predict(img_array, verbose=0)
        
        # 7. Get top prediction
        class_index = np.argmax(predictions[0])
        confidence = float(predictions[0][class_index])
        
        # 8. Map to disease name
        disease_name = self.class_names[class_index] if class_index < len(self.class_names) else "Unknown"
        
        # Clean up disease name (remove crop prefix and underscores)
        disease_name = disease_name.replace("___", " - ").replace("_", " ")
        
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
