"""
Test script to verify VisionEngine model loading
Diagnoses why the local Keras model might not be loading correctly
"""

import os
import sys

# Add Backend to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("VISION ENGINE DIAGNOSTIC TEST")
print("=" * 60)

# Step 1: Check TensorFlow availability
print("\n1. Checking TensorFlow...")
try:
    import tensorflow as tf
    from tensorflow import keras
    print(f"   ✅ TensorFlow version: {tf.__version__}")
    print(f"   ✅ Keras available")
except ImportError as e:
    print(f"   ❌ TensorFlow not available: {e}")
    sys.exit(1)

# Step 2: Check Pillow
print("\n2. Checking Pillow (PIL)...")
try:
    from PIL import Image
    print(f"   ✅ Pillow available")
except ImportError as e:
    print(f"   ❌ Pillow not available: {e}")
    sys.exit(1)

# Step 3: Check model file
model_path = os.path.join(
    os.path.dirname(__file__),
    "farm_management",
    "farming_stage",
    "models",
    "plant_disease_recog_model_pwp.keras"
)
print(f"\n3. Checking model file at:\n   {model_path}")
if os.path.exists(model_path):
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"   ✅ Model file exists ({size_mb:.1f} MB)")
else:
    print(f"   ❌ Model file NOT FOUND")
    sys.exit(1)

# Step 4: Try to load model
print("\n4. Attempting to load model...")
try:
    model = keras.models.load_model(model_path)
    print(f"   ✅ Model loaded successfully!")
    print(f"   - Input shape: {model.input_shape}")
    print(f"   - Output shape: {model.output_shape}")
except Exception as e:
    print(f"   ❌ Failed to load model:")
    print(f"   Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 5: Try to initialize VisionEngine
print("\n5. Testing VisionEngine initialization...")
try:
    from farm_management.farming_stage.engines.vision_engine import VisionEngine
    engine = VisionEngine()
    print(f"   ✅ VisionEngine initialized successfully!")
except Exception as e:
    print(f"   ❌ VisionEngine initialization failed:")
    print(f"   Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL CHECKS PASSED - Vision Engine is ready")
print("=" * 60)
