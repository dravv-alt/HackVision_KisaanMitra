import sys
import os

# Add Backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from database.connection import db, get_database
    print("Database module import successful")
except ImportError as e:
    print(f"Import failed: {e}")
