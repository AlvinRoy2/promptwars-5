"""
FastAPI Backend for Event Architecture & Production Studio.
Relying strictly on native LLM SDKs (Groq / Native OpenAI format) with zero LangChain/LlamaIndex.
Enforces Pydantic v2 structured schemas and mathematical verification.
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Optional

# Ensure backend directory is in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

load_dotenv()
logger = logging.getLogger("EventStudioBackend")
logging.basicConfig(level=logging.INFO)

from schemas import (
    EventRequest,
    EventBlueprintResponse,
    FinancialBlueprint,
    BudgetItem,
    TimelinePhase,
    VendorContractSpec,
    SensoryBlueprint,
)

# Security & Performance Middleware Setup
from fastapi import Request
from collections import defaultdict
import time
import hashlib

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
    if len(_blueprint_cache) > 200:
        oldest_key = min(_blueprint_cache.keys(), key=lambda k: _blueprint_cache[k][1])
        del _blueprint_cache[oldest_key]
    _blueprint_cache[cache_key] = (blueprint, time.time())

SYSTEM_PROMPT = """You are an elite Event Architect and Production Director.
Your task is to synthesize a comprehensive, production-grade event plan with mathematical rigor and multi-sensory depth.

CRITICAL FINANCIAL & DESIGN DIRECTIVES:
1. Mathematical Balance: Reserve approximately 10% for the contingency_reserve. The remaining 90% is allocated across itemized categories.
2. The sum of all item estimated_cost values must equal total_budget - contingency_reserve.
3. cost_per_guest = total_budget / guest_count.
4. Sensory depth: Specify exact architectural lighting Kelvin temperatures (e.g. 2200K amber glow), exact decibel and acoustic transitions, refined color palettes (hex codes and names), and signature culinary/beverage moments.
5. Vendor matrix: Provide realistic category budgets, clear deliverables, and 3 hard-hitting interview questions per vendor.
6. Timeline: Provide chronological execution phases from early planning (T-Minus weeks) down to day-of run-of-show.

Return ONLY a valid JSON object matching this schema:
{
  "event_summary": "Crisp executive synthesis of the event concept and operational footprint",
  "sensory_concept": {
    "lighting_ambiance": "Specific architectural lighting, lumens, and Kelvin temperatures (e.g., 2200K amber)",
    "acoustic_vibe": "Curated acoustic landscape, decibel guidelines, transition pacing",
    "decor_color_palette": ["#Hex1 Color Name", "#Hex2 Color Name", "#Hex3 Color Name", "#Hex4 Color Name"],
    "signature_experience": "Distinct sensory or culinary highlight that anchors the event"
  },
  "financial_ledger": {
    "total_budget": 0.0,
    "allocated_budget": 0.0,
    "contingency_reserve": 0.0,
    "cost_per_guest": 0.0,
    "items": [
      {
        "category": "Category name",
        "item_name": "Specific line item",
        "estimated_cost": 0.0,
        "percentage_of_total": 0.0,
        "notes": "Cost mitigation tip or contract stipulation"
      }
    ]
  },
  "timeline": [
    {
      "timeframe": "T-Minus X to Y Weeks",
      "phase_title": "Phase title",
      "action_items": ["Action 1", "Action 2"],
      "critical_deadline": "Hard deadline date or trigger"
    }
  ],
  "vendor_matrix": [
    {
      "category": "Vendor category",
      "estimated_budget": 0.0,
      "deliverables": ["Deliverable 1", "Deliverable 2"],
      "interview_questions": ["Question 1", "Question 2", "Question 3"],
      "required_permits_coi: "Required insurance and municipal permits"
    }
  ]
}
"""


def generate_curated_fallback(req: EventRequest) -> EventBlueprintResponse:
    """Deterministic, high-craft fallback conforming strictly to EventBlueprintResponse."""
    total = req.total_budget
    contingency = round(total * 0.10, 2)
    allocated = round(total - contingency, 2)
    cost_per_guest = round(total / req.guest_count, 2)

    return EventBlueprintResponse(
        event_summary=(
            f"An architectural, high-craft {req.event_type.lower()} tailored for {req.guest_count} guests in {req.location}. "
            f"Capital allocation is forensic with a guarded 10% emergency reserve ({req.currency} {contingency:,.2f}), "
            f"anchored around '{req.sensory_theme}'."
        ),
        sensory_concept=SensoryBlueprint(
            lighting_ambiance="2200K warm-amber clustered pillar illumination, recessed table pin-spots, and soft kinetic architectural grazing along natural surfaces.",
            acoustic_vibe="Live acoustic fingerstyle guitar transitioning into low-tempo vinyl jazz; dining acoustics strictly capped at 78dB for uninterrupted dialogue.",
            decor_color_palette=[
                "#1A1D24 Obsidian Slate",
                "#C85A32 Weathered Terracotta",
                "#D8CAB8 Raw Belgian Flax",
                "#556048 Aged Olive Leaf",
                "#E69C24 Amber Glow"
            ],
            signature_experience="Smoked botanical aperitif welcome served in fluted crystal coupes alongside an unhurried, wood-fired communal banquet."
        ),
        financial_ledger=FinancialBlueprint(
            total_budget=total,
            allocated_budget=allocated,
            contingency_reserve=contingency,
            cost_per_guest=cost_per_guest,
            items=[
                BudgetItem(
                    category="Venue & Site",
                    item_name="Exclusive Property & Grounds Hire (12-hour window)",
                    estimated_cost=round(allocated * 0.28, 2),
                    percentage_of_total=25.2,
                    notes="Negotiate complimentary load-in hours the morning prior to avoid 1.5x weekend overtime."
                ),
                BudgetItem(
                    category="Catering & Bar",
                    item_name="Farm-to-Table Plated Banquet & Curated Natural Wines",
                    estimated_cost=round(allocated * 0.35, 2),
                    percentage_of_total=31.5,
                    notes="Lock a flat-rate corkage agreement rather than standard per-bottle markups."
                ),
                BudgetItem(
                    category="Florals & Atmosphere",
                    item_name="Architectural Foliage, Olive Branch Clusters & Pillar Arrays",
                    estimated_cost=round(allocated * 0.12, 2),
                    percentage_of_total=10.8,
                    notes="Repurpose welcome focal botanicals to flank the banquet tables post-reception."
                ),
                BudgetItem(
                    category="Production & Audio",
                    item_name="2200K Ambient Lighting Grid & High-Fidelity Wireless Sound",
                    estimated_cost=round(allocated * 0.10, 2),
                    percentage_of_total=9.0,
                    notes="Bundle sound and lighting under a unified AV contractor to eliminate redundant travel fees."
                ),
                BudgetItem(
                    category="Photography & Film",
                    item_name="Documentary Film & Digital Visual Capture (8 Hours)",
                    estimated_cost=round(allocated * 0.10, 2),
                    percentage_of_total=9.0,
                    notes="Request full digital printing rights and select selects within 72 hours."
                ),
                BudgetItem(
                    category="Coordination & Permits",
                    item_name="Principal Producer, Day-Of Team & Municipal Permits",
                    estimated_cost=round(allocated * 0.05, 2),
                    percentage_of_total=4.5,
                    notes="Flat project fee contract with clear overtime parameters beyond midnight."
                )
            ]
        ),
        timeline=[
            TimelinePhase(
                timeframe=f"T-Minus {req.weeks_to_event} to {max(req.weeks_to_event - 12, 12)} Weeks",
                phase_title="Phase 1: Foundation & High-Leverage Anchors",
                action_items=[
                    "Execute venue contract with certified sound ordinance and strike curfew hours.",
                    "Lock documentary photographer and culinary partner deposits.",
                    "Verify electrical load amperage capacity for production runs."
                ],
                critical_deadline="Week 4: Irrevocable venue deposit lock"
            ),
            TimelinePhase(
                timeframe="T-Minus 12 to 4 Weeks",
                phase_title="Phase 2: Sensory Architecture & Vendor Specs",
                action_items=[
                    "Finalize seasonal menu tasting and allergen protocol matrix.",
                    "Approve lighting schematic (2200K) and microphone RF frequency scans.",
                    "Collect all vendor Certificates of Insurance (COI)."
                ],
                critical_deadline="T-Minus 30 Days: Sourcing and permits sign-off"
            ),
            TimelinePhase(
                timeframe="T-Minus 4 to 1 Weeks",
                phase_title="Phase 3: Operational Logistics & Seating Matrix",
                action_items=[
                    "Finalize exact guest guarantee count and dietary list with caterer.",
                    "Stagger delivery dock load-in times for florist and AV crews.",
                    "Conduct wireless mic walk-around sound check on site."
                ],
                critical_deadline="T-Minus 14 Days: Final headcount lock"
            ),
            TimelinePhase(
                timeframe="Event Day: Hour-by-Hour Run of Show",
                phase_title="Phase 4: Day-Of Precision Execution",
                action_items=[
                    "09:00 - Heavy kitchen equipment & AV structural load-in.",
                    "13:00 - Floral installation, table styling, and lighting dimmer calibration.",
                    "16:30 - Guest arrival & amber aperitif service (acoustic guitar begins).",
                    "18:00 - Main proceedings & toasts.",
                    "19:30 - Seated banquet dinner (78dB acoustic ceiling).",
                    "23:30 - Guest farewell & systematic rental strike."
                ],
                critical_deadline="23:30: Sound curfew strict enforcement"
            )
        ],
        vendor_matrix=[
            VendorContractSpec(
                category="Venue & Facilities",
                estimated_budget=round(allocated * 0.28, 2),
                deliverables=[
                    "12-hour continuous private estate access",
                    "Dedicated power runs (minimum four 20A circuits)",
                    "Secure on-site staging and refrigeration room"
                ],
                interview_questions=[
                    "What is your exact fee structure if the load-out crew exceeds the midnight cutoff by 30 minutes?",
                    "Can you walk us through the emergency generator protocol if local grid power fluctuates?",
                    "Are there mandatory vendor lists, or are outside licensed contractors permitted without penalty?"
                ],
                required_permits_coi="Active $2M General Liability COI naming venue and client as additional insureds."
            ),
            VendorContractSpec(
                category="Culinary & Beverage",
                estimated_budget=round(allocated * 0.35, 2),
                deliverables=[
                    "Hand-passed canapés, 3-course seasonal plated dinner, wine service",
                    "Complete kitchen setup, breakdown, and allergen-safe preparation",
                    "Trained service staff at a 1:10 guest ratio"
                ],
                interview_questions=[
                    "How do you accommodate unforeseen severe dietary allergies on the night without delay?",
                    "Are kitchen cleanup, linen pressing, and ice included in the quote or billed in arrears?",
                    "What percentage of prep is executed live on-site versus reheated commissary food?"
                ],
                required_permits_coi="State Food Handler certifications, Liquor Liability Insurance, Health Dept Permit."
            ),
            VendorContractSpec(
                category="Audio, DJ & Lighting Production",
                estimated_budget=round(allocated * 0.10, 2),
                deliverables=[
                    "Wireless handheld and lapel mics with dual-channel receivers",
                    "2200K architectural ambient uplights and spotlight array",
                    "Backup audio console and secondary playback machine on standby"
                ],
                interview_questions=[
                    "How do you manage room acoustics and reverberation in high-ceiling or glass-heavy areas?",
                    "What is your backup protocol if your primary mixer or amplifier fails during speeches?",
                    "Do you respect strict client song veto lists, and what is your overtime billing increment?"
                ],
                required_permits_coi="Commercial General Liability COI and local Municipal Amplified Sound Permit."
            ),
            VendorContractSpec(
                category="Documentary Photography & Film",
                estimated_budget=round(allocated * 0.10, 2),
                deliverables=[
                    "Dual-camera documentary coverage (8 continuous hours)",
                    "Color-graded sneak-peek gallery of 40 selects within 72 hours",
                    "Complete high-resolution digital master gallery with full print release"
                ],
                interview_questions=[
                    "Do your cameras record to dual redundant memory cards simultaneously in real-time?",
                    "Who specifically is shooting my event—you personally or an associate shooter?",
                    "How are raw master files archived, and how many years do you guarantee file safety?"
                ],
                required_permits_coi="Standard Equipment Liability and Commercial Production Insurance."
            )
        ]
    )


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
