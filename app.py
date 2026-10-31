"""
Root entry point shim for Event Architecture & Production Studio.
Delegates to legacy_streamlit/app.py when run with Streamlit,
or starts the FastAPI production backend when run with Python directly.
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LEGACY_DIR = os.path.join(ROOT_DIR, "legacy_streamlit")
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")

for p in [ROOT_DIR, BACKEND_DIR, LEGACY_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

legacy_app_path = os.path.join(LEGACY_DIR, "app.py")

# If executed via 'streamlit run app.py'
if "streamlit" in sys.modules or os.path.basename(sys.argv[0]).startswith("streamlit"):
    if os.path.exists(legacy_app_path):
        with open(legacy_app_path, "r", encoding="utf-8") as f:
            code = compile(f.read(), legacy_app_path, "exec")
            exec(code)
    else:
        print(f"Streamlit application file not found at {legacy_app_path}")
elif __name__ == "__main__":
    # If run directly with python app.py, start the FastAPI backend
    import uvicorn
    print("Starting FastAPI Backend Server on http://0.0.0.0:8000 ...")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

