#!/usr/bin/env python
"""
Test script to verify all dependencies are installed
"""
import sys

print("Python version:", sys.version)
print("\nTesting imports...\n")

try:
    import flask
    print("✓ Flask installed:", flask.__version__)
except ImportError as e:
    print("✗ Flask NOT installed:", e)

try:
    import lxml
    print("✓ lxml installed:", lxml.__version__)
except ImportError as e:
    print("✗ lxml NOT installed:", e)

try:
    import markupsafe
    print("✓ MarkupSafe installed:", markupsafe.__version__)
except ImportError as e:
    print("✗ MarkupSafe NOT installed:", e)

print("\n" + "="*50)
print("Testing app import...")
print("="*50 + "\n")

try:
    from app import create_app
    print("✓ app.create_app imported successfully")

    application = create_app()
    print("✓ Application created successfully:", type(application))

except Exception as e:
    print("✗ Error importing/creating app:")
    print(f"  {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
