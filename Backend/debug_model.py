"""
Simplified diagnostic to read model error details
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

print("Testing Keras Model Load...")
print("-" * 60)

try:
    from tensorflow import keras
    model_path = os.path.join(
        os.path.dirname(__file__),
        "farm_management/farming_stage/models/plant_disease_recog_model_pwp.keras"
    )
    
    print(f"Model path: {model_path}")
    print(f"File exists: {os.path.exists(model_path)}")
    print("\nAttempting load...")
    
    model = keras.models.load_model(model_path)
    print("✅ SUCCESS")
    print(f"Input shape: {model.input_shape}")
    
except Exception as e:
    print(f"\n❌ FAILED")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print("\nFull traceback:")
    import traceback
    traceback.print_exc()
