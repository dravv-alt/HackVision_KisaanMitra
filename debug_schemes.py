import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

try:
    print("Importing GovSchemesDisplayService...")
    from Backend.Gov_Schemes.service import GovSchemesDisplayService
    
    print("Initializing service...")
    service = GovSchemesDisplayService()
    
    print("Running get_schemes_display...")
    # Mock farmer_id 'FARMER001'
    result = service.get_schemes_display(
        farmer_id="FARMER001",
        force_refresh=True
    )
    
    print("Success!")
    print(f"Got {len(result.schemeCards)} schemes")

except Exception as e:
    print("CAUGHT EXCEPTION:")
    print(e)
    import traceback
    traceback.print_exc()
