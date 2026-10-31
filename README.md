# ✦ Event Architecture & Production Studio

A production-grade GenAI event planning platform built with a **Python FastAPI** backend for structured LLM synthesis and a high-craft **React + Tailwind CSS** frontend implementing an obsidian glassmorphic UI.

---

## 🏛 Architecture & Tech Stack

```
Promptwars-5/
├── backend/
│   ├── main.py              # FastAPI application (Native SDK inference, structured outputs)
│   ├── schemas.py           # Strict Pydantic v2 data models (EventRequest, EventBlueprintResponse)
│   ├── requirements.txt     # Python backend dependencies
│   ├── .env.example         # Environment template
│   └── run.py               # Direct runner script: python backend/run.py
│
├── frontend/
│   ├── src/
│   │   ├── components/magicui/ # Magic UI Components (ScrollProgress, Particles, NumberTicker, BorderBeam)
│   │   ├── App.jsx          # React application matching exact 5-section UI layout
│   │   ├── index.css        # Tailwind CSS + Obsidian Glassmorphic styling
│   │   └── main.jsx         # React root entry point
│   ├── index.html           # HTML5 entry with Plus Jakarta Sans & JetBrains Mono
│   ├── vite.config.js       # Vite build configuration with Tailwind v4 plugin
│   └── package.json         # React 19, Tailwind CSS, Lucide React, Motion
│
├── requirements.txt         # Root requirements
└── README.md                # System documentation & execution instructions
```

---

## 🎨 Visual Design System

- **Palette**:
  - Deep Obsidian Slate: `#070A10`
  - Card Surface: `#111827` with 60% opacity (`bg-[#111827]/60` with `backdrop-blur-xl`)
  - Borders: `rgba(255, 255, 255, 0.08)`
  - Primary Accent Cyan: `#06B6D4`
  - Violet Accent: `#8B5CF6`
  - Emerald Positive: `#10B981`
- **Typography**:
  - `Plus Jakarta Sans` for headings, body copy, and labels.
  - `JetBrains Mono` for numerical metrics, budget numbers, and telemetry badges.
- **Effects**:
  - Subtle top-edge glows on active cards (`box-shadow: 0 -1px 0 0 rgba(6,182,212,0.5)`).
  - Hover elevation with cubic-bezier spring physics (`hover-elevate`).
  - Active button tactile compression (`active:scale-[0.99]`).

---

## 📋 Component Layout & Features

1. **Header Banner**:
   - Brand Title: `PROMPTWARS | EVENT INTELLIGENCE STUDIO`
   - Page Title: `Event Architecture & Production Studio`
   - Subtitle: *"A surgical, high-craft planning suite for high-stakes weddings, birthdays, and community gatherings. Mathematically verified itemized budgets, sensory design blueprints, and ruthless vendor interview contracts."*
2. **Telemetry Badges Bar**:
   - `+2200K ARCHITECTURAL KELVIN AMBIANCE`
   - `+78dB ACOUSTIC DINING LIMITS`
   - `+10% GUARDED CONTINGENCY RESERVE`
   - `+STRICT CERTIFICATE OF INSURANCE / COI LOCK`
3. **Curated Archetype Quick-Select Pills**:
   - `Napa Valley Botanical Wedding (120 Guests)`
   - `Cyberpunk 30th Milestone Birthday (85 Guests)`
   - `Community Sustainable Arts & Tech Gala (250 Guests)`
   - Auto-fills the specification form on click.
4. **Event Profile Specification Form**:
   - Row 1: Event Type/Occasion | Location & Venue Characteristics | Guest Count | Currency
   - Row 2: Total Budget Constraint | Planning Horizon (Weeks to Event) | Target Spend / Guest (Live auto-computed: `Budget / Guests`)
   - Row 3: Stylistic Theme & Sensory Vibe (Textarea) | Operational Constraints & Dietary Mandates (Textarea)
   - CTA Button: `⚡ Synthesize Production Blueprint`
5. **Blueprint Output Canvas (Tabs View)**:
   - **Tab 1: Financial Ledger**: Itemized table, visual spend breakdown bar, 10% auto-allocated contingency reserve, cost per guest analytics.
   - **Tab 2: Timeline & Milestones**: Chronological phase-gated execution roadmap (T-minus weeks out down to Day-Of run-of-show).
   - **Tab 3: Sensory & Creative Concept**: Lighting specs (Kelvin), acoustic guidelines, decor color palette (with swatches & hex click-to-copy), signature culinary/beverage experience.
   - **Tab 4: Vendor Execution Matrix**: Vendor category, allocated budget range, deliverable scope, 3 technical interview questions per vendor, and COI permit mandates.
   - **Tab 5: Export Package**: One-click download of production brief (`.md`) or raw JSON (`.json`).

---

## 🚀 Execution Instructions

### 1. Start FastAPI Backend (Terminal 1)
```powershell
python backend/run.py
```
*or:*
```powershell
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
- **API Swagger Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

### 2. Start React + Tailwind Frontend (Terminal 2)
```powershell
cd frontend
npm.cmd run dev
```
- **Interactive UI**: [http://localhost:5173](http://localhost:5173)

---

## 🔒 No-Framework Native LLM Orchestration Rule

This codebase strictly avoids LangChain, LlamaIndex, or any heavy wrapper abstractions:
- Direct inference through the model's native SDK (`groq.Groq` / native OpenAI client format).
- Schema validation through **Pydantic v2** (`backend/schemas.py`).
- Deterministic curated engine fallback when API keys are not provided.
