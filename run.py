#!/usr/bin/env python3
"""
Simple runner script for the Notion AI Assistant
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import main
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have installed the required dependencies:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
