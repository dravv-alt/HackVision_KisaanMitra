
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

print("Attempting to import Backend...")
try:
    import Backend
    print("Backend imported.")
except Exception as e:
    print(f"Failed to import Backend: {e}")

print("Attempting to import Backend.api.routers.farm_management...")
try:
    from Backend.api.routers import farm_management
    print("Backend.api.routers.farm_management imported successfully.")
except Exception as e:
    print(f"Failed to import farm_management router: {e}")
    import traceback
    traceback.print_exc()

