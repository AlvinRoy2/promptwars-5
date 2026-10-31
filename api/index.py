"""
Vercel Serverless Function entry point.
Mounts the backend FastAPI app so Vercel can route /api/* requests to it.
"""

import sys
import os

# Add backend directory to path so imports resolve correctly
BACKEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Import the FastAPI app from backend
from main import app  # noqa: F401 — Vercel expects 'app' at module level
