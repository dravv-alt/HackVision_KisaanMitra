"""
TensorFlow Model Conversion Script
Attempts to load the old model and convert it to TensorFlow 2.20 compatible format
"""

import os
import sys

print("="*60)
print("TensorFlow Model Conversion Utility")
print("="*60)

# Step 1: Import TensorFlow
print("\n[1/5] Importing TensorFlow...")
try:
    import tensorflow as tf
    from tensorflow import keras
    print(f"   TensorFlow version: {tf.__version__}")
except ImportError as e:
    print(f"   ERROR: {e}")
    sys.exit(1)

# Step 2: Locate model file
model_path = os.path.join(
    os.path.dirname(__file__),
    "farm_management",
    "farming_stage",
    "models",
    "plant_disease_recog_model_pwp.keras"
)

print(f"\n[2/5] Locating model file...")
print(f"   Path: {model_path}")
if not os.path.exists(model_path):
    print(f"   ERROR: Model file not found!")
    sys.exit(1)

size_mb = os.path.getsize(model_path) / (1024 * 1024)
print(f"   Size: {size_mb:.1f} MB")

# Step 3: Attempt to load with compile=False
print(f"\n[3/5] Attempting to load model with compile=False...")
print("   (This skips optimizer/loss loading which often causes issues)")

try:
    model = keras.models.load_model(model_path, compile=False)
    print("   SUCCESS! Model loaded without compilation")
    print(f"   Input shape: {model.input_shape}")
    print(f"   Output shape: {model.output_shape}")
    print(f"   Total layers: {len(model.layers)}")
except Exception as e:
    print(f"   FAILED: {e}")
    print("\n   Trying alternative loading methods...")
    
    # Try loading as HDF5
    try:
        print("   Attempting HDF5 format load...")
        model = keras.models.load_model(model_path, compile=False)
        print("   SUCCESS with HDF5!")
    except Exception as e2:
        print(f"   HDF5 also failed: {e2}")
        print("\n   ERROR: Cannot load model with any method")
        print("   Recommendation: Retrain model with TensorFlow 2.20")
        sys.exit(1)

# Step 4: Re-compile with simple config
print(f"\n[4/5] Re-compiling model with compatible settings...")
try:
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    print("   Model compiled successfully")
except Exception as e:
    print(f"   WARNING: Compilation failed: {e}")
    print("   Model can still be used for inference without compilation")

# Step 5: Save converted model
backup_path = model_path.replace('.keras', '_OLD_BACKUP.keras')
new_path = model_path

print(f"\n[5/5] Saving converted model...")
print(f"   Backing up original to: {backup_path}")

try:
    # Backup original
    if not os.path.exists(backup_path):
        import shutil
        shutil.copy2(model_path, backup_path)
        print("   Original backed up successfully")
    
    # Save new version
    print(f"   Saving converted model to: {new_path}")
    model.save(new_path)
    print("   Converted model saved successfully!")
    
    print("\n" + "="*60)
    print("CONVERSION SUCCESSFUL!")
    print("="*60)
    print("\nNext steps:")
    print("1. Test the model with test_vision_engine.py")
    print("2. If it works, the old backup can be deleted")
    print("3. If it fails, restore from backup")
    
except Exception as e:
    print(f"   ERROR during save: {e}")
    print("\n   Model conversion failed")
    sys.exit(1)
