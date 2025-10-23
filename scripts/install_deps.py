#!/usr/bin/env python
"""
Script to install dependencies from requirements.txt
"""
import subprocess
import sys
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
requirements_file = os.path.join(script_dir, 'requirements.txt')

print(f"Installing dependencies from {requirements_file}...")

try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
    print("\n✓ Dependencies installed successfully!")
except subprocess.CalledProcessError as e:
    print(f"\n✗ Error installing dependencies: {e}")
    sys.exit(1)
