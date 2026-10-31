"""
Root conftest.py — ensures pytest discovers 'backend' as a top-level package
by inserting the repo root into sys.path before any test collection.
"""
import sys
import os

# Insert project root so `from backend.main import app` resolves correctly
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
