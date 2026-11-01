"""
FastAPI Backend for Event Architecture & Production Studio.
Relying strictly on native LLM SDKs (Groq / Native OpenAI format) with zero LangChain/LlamaIndex.
Enforces Pydantic v2 structured schemas and mathematical verification.
"""

# -- Standard Library ----------------------------------------------------------
import hashlib
import json
import logging
import os
import sys
import time
from collections import defaultdict
from typing import Optional

# -- Third-party ---------------------------------------------------------------
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

# -- Local ---------------------------------------------------------------------
# Ensure backend directory is on sys.path for direct-run and pytest invocations
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from fallback import generate_curated_fallback  # noqa: E402
from prompts import SYSTEM_PROMPT  # noqa: E402
from schemas import EventBlueprintResponse, EventRequest  # noqa: E402

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EventStudioBackend")

app = FastAPI(
    title="Event Architecture & Production Studio API",
    description="High-performance GenAI event architecture backend. Native SDK structured output without LangChain.",
    version="2.1.0"
)

# 1. Security Headers Middleware (OWASP Defense-in-Depth)
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# 2. Configurable CORS with environment override and Vercel preview domain support
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env:
    allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]
else:
    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://0.0.0.0:8000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins != ["*"] else ["*"],
    allow_origin_regex=r"^https://.*\.vercel\.app$",
    allow_credentials=True if allowed_origins != ["*"] else False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# 3. In-Memory Sliding-Window Rate Limiter
RATE_LIMIT_WINDOW_SECS = 60
RATE_LIMIT_MAX_REQUESTS = 30
_request_timestamps = defaultdict(list)

def enforce_rate_limit(client_ip: str):
    now = time.time()
    history = _request_timestamps[client_ip]
    _request_timestamps[client_ip] = [t for t in history if now - t < RATE_LIMIT_WINDOW_SECS]
    if len(_request_timestamps[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
        logger.warning(f"Rate limit exceeded for client IP: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Maximum 30 blueprint synthesis requests per minute."
        )
    _request_timestamps[client_ip].append(now)

# 4. In-Memory TTL Blueprint Cache
_blueprint_cache = {}
CACHE_TTL_SECS = 1800  # 30 minutes

def get_cached_blueprint(cache_key: str) -> Optional[EventBlueprintResponse]:
    if cache_key in _blueprint_cache:
        data, ts = _blueprint_cache[cache_key]
        if time.time() - ts < CACHE_TTL_SECS:
            return data
        del _blueprint_cache[cache_key]
    return None

def set_cached_blueprint(cache_key: str, blueprint: EventBlueprintResponse):
    # Enforce maximum cache capacity to prevent memory creep
    if len(_blueprint_cache) >= 200 and cache_key not in _blueprint_cache:
        oldest_key = min(_blueprint_cache.keys(), key=lambda k: _blueprint_cache[k][1])
        del _blueprint_cache[oldest_key]
    _blueprint_cache[cache_key] = (blueprint, time.time())


@app.get("/health")
@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "Event Architecture & Production Studio API",
        "sdk": "Native Groq / OpenAI SDK (No LangChain)",
        "model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    }


@app.post("/api/blueprint", response_model=EventBlueprintResponse, status_code=status.HTTP_200_OK)
@app.post("/api/plan/all", response_model=EventBlueprintResponse, status_code=status.HTTP_200_OK)
def synthesize_blueprint(req: EventRequest, request: Request):
    """
    Synthesize complete production blueprint using native LLM SDK with structured JSON output.
    Protected with sliding-window rate limiting and response caching.
    """
    # 1. Enforce Client Rate Limit
    client_ip = request.client.host if request.client else "127.0.0.1"
    enforce_rate_limit(client_ip)

    # 2. Check Blueprint Cache
    cache_key = hashlib.sha256(json.dumps(req.model_dump(), sort_keys=True).encode()).hexdigest()
    cached = get_cached_blueprint(cache_key)
    if cached:
        logger.info(f"Serving cached blueprint for key={cache_key[:8]}")
        return cached

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.info("GROQ_API_KEY not set. Serving high-craft deterministic blueprint.")
        blueprint = generate_curated_fallback(req)
        set_cached_blueprint(cache_key, blueprint)
        return blueprint

    try:
        from groq import Groq
        client = Groq(api_key=api_key, timeout=35.0)
        model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

        user_content = f"""EVENT PROFILE:
- Occasion: {req.event_type}
- Location & Setting: {req.location}
- Attendees: {req.guest_count}
- Currency: {req.currency}
- Total Budget: {req.total_budget:,.2f}
- Timeline: {req.weeks_to_event} weeks out
- Stylistic Theme & Sensory Vibe: {req.sensory_theme}
- Operational Constraints & Dietary: {req.operational_constraints or 'None'}

Generate the exact JSON response adhering to the schema and financial constraints."""

        logger.info(f"Invoking native Groq SDK model={model} ...")
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=4096
        )

        raw = completion.choices[0].message.content
        data = json.loads(raw)

        # Ensure financial math integrity
        if "financial_ledger" in data:
            data["financial_ledger"]["total_budget"] = req.total_budget
            data["financial_ledger"]["cost_per_guest"] = round(req.total_budget / req.guest_count, 2)
            if "contingency_reserve" not in data["financial_ledger"] or data["financial_ledger"]["contingency_reserve"] == 0:
                data["financial_ledger"]["contingency_reserve"] = round(req.total_budget * 0.10, 2)
            data["financial_ledger"]["allocated_budget"] = round(req.total_budget - data["financial_ledger"]["contingency_reserve"], 2)

        blueprint = EventBlueprintResponse(**data)
        set_cached_blueprint(cache_key, blueprint)
        return blueprint

    except ValidationError as ve:
        logger.error(f"Pydantic Validation Error: {ve}")
        blueprint = generate_curated_fallback(req)
        set_cached_blueprint(cache_key, blueprint)
        return blueprint
    except Exception as e:
        logger.error(f"Native SDK call failed: {e}. Falling back to curated engine.")
        blueprint = generate_curated_fallback(req)
        set_cached_blueprint(cache_key, blueprint)
        return blueprint


# ── Serve Built Frontend SPA (Docker / Local only — skipped on Vercel Services) ─
# On Vercel, the frontend is its own service served by Vite.
# We only mount static files when NOT on Vercel and a built dist/ exists.
if not os.environ.get("VERCEL"):
    try:
        from fastapi.staticfiles import StaticFiles
        from fastapi.responses import FileResponse

        FRONTEND_DIST = os.path.abspath(os.path.join(CURRENT_DIR, "..", "frontend", "dist"))
        if not os.path.exists(FRONTEND_DIST):
            FRONTEND_DIST = os.path.abspath(os.path.join(CURRENT_DIR, "static"))

        if os.path.exists(FRONTEND_DIST):
            assets_dir = os.path.join(FRONTEND_DIST, "assets")
            if os.path.exists(assets_dir):
                app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

            @app.get("/")
            async def serve_root():
                index_file = os.path.join(FRONTEND_DIST, "index.html")
                if os.path.isfile(index_file):
                    return FileResponse(index_file)
                raise HTTPException(status_code=404, detail="Frontend index.html not found")

            @app.get("/{full_path:path}")
            async def serve_spa(full_path: str):
                # Allow API routes, docs, and health checks to pass through
                if full_path.startswith("api/") or full_path in ("health", "docs", "redoc", "openapi.json"):
                    raise HTTPException(status_code=404, detail="Not Found")
                file_path = os.path.join(FRONTEND_DIST, full_path)
                if full_path and os.path.isfile(file_path):
                    return FileResponse(file_path)
                index_file = os.path.join(FRONTEND_DIST, "index.html")
                if os.path.isfile(index_file):
                    return FileResponse(index_file)
                raise HTTPException(status_code=404, detail="Frontend index.html not found")

    except Exception as e:
        logger.warning(f"Could not mount frontend static files: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
