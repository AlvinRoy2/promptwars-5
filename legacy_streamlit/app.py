"""
PROMPTWARS | Event Planning Intelligence Assistant
Frontend Web Application (Streamlit)
Crafted with high-taste design principles:
- Apple WWDC Fluid Design & tactile responsiveness
- Obsidian titanium dark theme with Magic UI border-beam micro-accents
- Emil Kowalski polish (deliberate typography, responsive feedback)
- Break-UI Adversarial Stress-Test Toggle for edge-case resilience
"""

import os
import sys
import json
import requests
import pandas as pd
import streamlit as st
from datetime import datetime

# Ensure project root and backend are in Python search path
FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(FRONTEND_DIR)
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")

for path in [PROJECT_ROOT, BACKEND_DIR, FRONTEND_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Import backend modules for direct fallback capability
try:
    from backend.models import EventProfileRequest, FullEventPlanResponse
    from backend.llm_provider import get_llm_provider, DEFAULT_GROQ_MODEL
    from backend.prompts import (
        IDEAS_SYSTEM_PROMPT,
        BUDGET_SYSTEM_PROMPT,
        TIMELINE_SYSTEM_PROMPT,
        VENDORS_SYSTEM_PROMPT,
    )
except ImportError:
    from models import EventProfileRequest, FullEventPlanResponse
    from llm_provider import get_llm_provider, DEFAULT_GROQ_MODEL
    from prompts import (
        IDEAS_SYSTEM_PROMPT,
        BUDGET_SYSTEM_PROMPT,
        TIMELINE_SYSTEM_PROMPT,
        VENDORS_SYSTEM_PROMPT,
    )

# -----------------------------------------------------------------------------
# Streamlit Page Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PROMPTWARS | Event Intelligence Studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load External CSS
css_path = os.path.join(FRONTEND_DIR, "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Session State
# -----------------------------------------------------------------------------
if "current_plan" not in st.session_state:
    st.session_state.current_plan = None
if "api_url" not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"
if "break_ui_mode" not in st.session_state:
    st.session_state.break_ui_mode = False

# -----------------------------------------------------------------------------
# Sidebar Configuration & Controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ✦ Studio Configuration")

    api_endpoint = st.text_input(
        "FastAPI Backend Endpoint",
        value=st.session_state.api_url,
        help="Address of the running FastAPI server (default: http://localhost:8000)"
    )
    st.session_state.api_url = api_endpoint

    # Test Backend Connection
    backend_online = False
    try:
        r = requests.get(f"{st.session_state.api_url}/health", timeout=1.5)
        if r.status_code == 200:
            backend_online = True
            info = r.json()
            st.success(f"✓ Backend Live ({info.get('mode', 'live')})")
        else:
            st.warning("Backend returned non-200")
    except Exception:
        st.info("ℹ Standalone Direct Mode (Internal LLM Engine Active)")

    st.markdown("---")

    # BREAK-UI Adversarial Testing Toggle (/break-ui skill)
    st.markdown("### 🛡️ Break-UI Stress Lab")
    break_mode = st.toggle(
        "Adversarial Worst-Case Mode",
        value=st.session_state.break_ui_mode,
        help="Injects realistic edge-case worst data (extreme budgets, long unbreakable strings, complex allergens) to verify layout integrity."
    )
    st.session_state.break_ui_mode = break_mode

    st.markdown("---")
    st.markdown("### ⚡ Quick Presets")

    if not st.session_state.break_ui_mode:
        preset_choice = st.selectbox(
            "Load Curated Archetype",
            [
                "Custom (Fill Below)",
                "Napa Valley Botanical Wedding (120 Guests)",
                "Cyberpunk 30th Milestone Birthday (55 Guests)",
                "Community Sustainable Arts & Tech Gala (250 Guests)",
            ]
        )
    else:
        preset_choice = st.selectbox(
            "Load Adversarial Stress Case",
            [
                "Worst Case 1: Ultra-Budget Macro-Crowd ($1,250 for 420 Guests)",
                "Worst Case 2: Multi-Millionaire Micro-Guest Gala ($2,450,000 for 14 Guests)",
                "Worst Case 3: Extreme Unbreakable Text & Historic Landmark Constraint",
            ]
        )

    # Dataset Presets
    NORMAL_PRESETS = {
        "Napa Valley Botanical Wedding (120 Guests)": {
            "type": "Wedding",
            "guests": 120,
            "budget": 48000.0,
            "currency": "USD",
            "location": "Napa Valley, CA - Private Vineyard Lawn & Stone Cellar",
            "vibe": "Warm Organic Modernism, muted eucalyptus, raw linen, 2200K amber pillar candles, and acoustic fingerstyle transitioning into vinyl jazz.",
            "notes": "Bride is celiac (strict gluten-free kitchen requirement). Groom's family wants an espresso bar after 10 PM. Strictly no corny line dances.",
            "weeks": 36
        },
        "Cyberpunk 30th Milestone Birthday (55 Guests)": {
            "type": "Milestone Birthday",
            "guests": 55,
            "budget": 16500.0,
            "currency": "USD",
            "location": "Downtown Warehouse Loft - Concrete & Industrial Glass",
            "vibe": "Neo-Tokyo Cyberpunk meets raw brutalism. Neon violet & obsidian accents, modular synth live set, and interactive craft mixology lab.",
            "notes": "Must have an analog retro arcade cabinet nook and a custom bao bun bar at midnight.",
            "weeks": 12
        },
        "Community Sustainable Arts & Tech Gala (250 Guests)": {
            "type": "Community Gala",
            "guests": 250,
            "budget": 65000.0,
            "currency": "USD",
            "location": "Civic Greenhouse & Glass Pavilion - Public Waterfront Park",
            "vibe": "Zero-waste architectural biophilia. Living moss installations, solar-powered kinetic projections, and hyper-local farm banquet.",
            "notes": "City sound permit curfew strictly at 22:00. Requires wheelchair accessible shuttle runs from civic transit hub.",
            "weeks": 24
        }
    }

    BREAK_UI_PRESETS = {
        "Worst Case 1: Ultra-Budget Macro-Crowd ($1,250 for 420 Guests)": {
            "type": "Community Assembly / Radical Austerity Potluck",
            "guests": 420,
            "budget": 1250.0,
            "currency": "USD",
            "location": "Municipal Park Open Pavilion (Uncovered, Zero Electrical Outlets, Public Restrooms 400m away)",
            "vibe": "Minimalist communal resourcefulness, unamplified megaphone announcements, volunteer acoustic guitar, solar lanterns",
            "notes": "Cost per guest is under $3.00. Must rely on community volunteer cooks, municipal water fountains, and paper signposts.",
            "weeks": 3
        },
        "Worst Case 2: Multi-Millionaire Micro-Guest Gala ($2,450,000 for 14 Guests)": {
            "type": "Ultra-High-Net-Worth Private Summit & Banquet",
            "guests": 14,
            "budget": 2450000.0,
            "currency": "USD",
            "location": "Private Superyacht & Historic Venetian Palazzo San Cassiano, Venice, Italy",
            "vibe": "Imperial Venetian decadence, 24-karat gold leaf table scaping, private philharmonic quartet, helicopter transport, rare vintage 1945 Romanée-Conti pairings",
            "notes": "Requires round-the-clock private maritime security detail, discrete non-disclosure agreements for all 38 service staff, and certified sommelier master.",
            "weeks": 52
        },
        "Worst Case 3: Extreme Unbreakable Text & Historic Landmark Constraint": {
            "type": "Schloss Neuschwanstein & Königliche Gärten Sommernachtsfest",
            "guests": 85,
            "budget": 95000.0,
            "currency": "EUR",
            "location": "Schloss Neuschwanstein, Neuschwansteinstraße 20, 87645 Schwangau, Bavaria, Germany (Historical Landmark Protection Class 1A - Zero Open Flame, Decibel Limit 68dB, Alpine Wind > 75km/h)",
            "vibe": "Bavarian Neuschwanstein Romanticism with delicate contemporary glass enclosures, flameless LED luminary arrays, and chamber orchestra",
            "notes": "Allergens: Severe airborne peanut, tree nut, allium, sulfite, and sesame anaphylaxis. Strictly zero synthetic materials.",
            "weeks": 18
        }
    }

    st.markdown("---")
    st.markdown("### 🔑 Groq LLM Key")
    groq_input_key = st.text_input(
        "Groq API Key (Optional)",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        help="Enter your Groq key (gsk_...) or set GROQ_API_KEY. If omitted, the high-craft curated engine delivers instant designs."
    )
    if groq_input_key:
        os.environ["GROQ_API_KEY"] = groq_input_key

# -----------------------------------------------------------------------------
# Header Hero Section
# -----------------------------------------------------------------------------
if st.session_state.break_ui_mode:
    st.markdown(
        """
        <div class="break-ui-banner">
            <div><strong>🛡️ Break-UI Adversarial Mode Active:</strong> Stress-testing extreme real-world budgets, edge-case guest ratios, and long unbreakable strings.</div>
            <div><code>STATUS: DEV_ADVERSARIAL</code></div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="hero-container">
        <div class="hero-badge">✦ Anti-AI Slop Intelligence Studio</div>
        <h1 class="hero-title">Event Architecture & Production Engine</h1>
        <p class="hero-subtitle">
            A surgical, high-craft planning suite for high-stakes weddings, birthdays, and community gatherings.
            Mathematically verified itemized budgets, sensory design roadmaps, and ruthless vendor interview contracts.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# Profile Form
# -----------------------------------------------------------------------------
current_presets = BREAK_UI_PRESETS if st.session_state.break_ui_mode else NORMAL_PRESETS
default_vals = current_presets.get(preset_choice, list(current_presets.values())[0])

with st.expander("✦ Event Profile Specification", expanded=(st.session_state.current_plan is None)):
    with st.form("event_profiling_form"):
        col1, col2, col3 = st.columns([1.5, 1, 1])

        with col1:
            event_type = st.text_input(
                "Event Type / Occasion",
                value=default_vals["type"],
                help="e.g. Wedding, Milestone Birthday, Civic Charity Gala, Tech Summit"
            )
            location = st.text_input(
                "Location & Venue Characteristics",
                value=default_vals["location"],
                help="City, indoor/outdoor balance, architectural character"
            )

        with col2:
            guest_count = st.number_input(
                "Estimated Guest Count",
                min_value=1,
                max_value=50000,
                value=int(default_vals["guests"]),
                step=5
            )
            total_budget = st.number_input(
                "Total Budget Constraint",
                min_value=100.0,
                max_value=50000000.0,
                value=float(default_vals["budget"]),
                step=500.0
            )

        with col3:
            curr_list = ["USD", "EUR", "GBP", "INR", "CAD", "AUD", "SGD", "JPY"]
            curr_idx = curr_list.index(default_vals.get("currency", "USD")) if default_vals.get("currency", "USD") in curr_list else 0
            currency = st.selectbox("Currency Code", curr_list, index=curr_idx)

            timeline_urgency = st.slider(
                "Planning Horizon (Weeks to Event)",
                min_value=1,
                max_value=104,
                value=int(default_vals["weeks"])
            )

        aesthetic_vibe = st.text_area(
            "Stylistic Theme & Sensory Vibe",
            value=default_vals["vibe"],
            help="Describe the tactile mood, lighting temperature, acoustic progression, and palette inspirations."
        )

        custom_notes = st.text_area(
            "Operational Constraints, Dietary Mandates & Must-Haves",
            value=default_vals["notes"],
            help="Allergies, sound ordinances, strike deadlines, specific cultural traditions"
        )

        generate_submitted = st.form_submit_button(
            "✦ Generate Production-Ready Blueprint",
            use_container_width=True,
            type="primary"
        )

# -----------------------------------------------------------------------------
# Plan Execution Logic
# -----------------------------------------------------------------------------
if generate_submitted:
    profile_payload = EventProfileRequest(
        event_type=event_type,
        guest_count=guest_count,
        total_budget=total_budget,
        currency=currency,
        location=location,
        aesthetic_vibe=aesthetic_vibe,
        custom_notes=custom_notes,
        timeline_urgency_weeks=timeline_urgency,
    )

    with st.spinner("Synthesizing creative atmosphere, balancing financial ledger, and stress-testing run-of-show..."):
        success = False
        plan_dict = None

        # 1. Try FastAPI backend if online
        if backend_online:
            try:
                resp = requests.post(
                    f"{st.session_state.api_url}/api/plan/all",
                    json=profile_payload.model_dump(),
                    timeout=90
                )
                if resp.status_code == 200:
                    plan_dict = resp.json()
                    success = True
                else:
                    st.error(f"Backend API error: {resp.status_code} - {resp.text}")
            except Exception as e:
                st.warning(f"Could not reach backend ({e}). Falling back to internal engine.")

        # 2. Direct internal execution if backend is unavailable
        if not success:
            try:
                provider = get_llm_provider("groq")
                user_ctx = f"""EVENT SPECIFICATION:
- Event Type: {profile_payload.event_type}
- Guest Count: {profile_payload.guest_count} attendees
- Total Budget: {profile_payload.total_budget:,.2f} {profile_payload.currency}
- Location & Venue Setting: {profile_payload.location}
- Aesthetic & Style Vibe: {profile_payload.aesthetic_vibe}
- Special Notes / Constraints: {profile_payload.custom_notes or 'None specified'}
- Planning Window: {profile_payload.timeline_urgency_weeks} weeks until event date"""

                ideas_d = provider.generate_json(IDEAS_SYSTEM_PROMPT, user_ctx, temperature=0.7)
                budget_d = provider.generate_json(BUDGET_SYSTEM_PROMPT, user_ctx, temperature=0.2)
                budget_d["currency"] = profile_payload.currency
                timeline_d = provider.generate_json(TIMELINE_SYSTEM_PROMPT, user_ctx, temperature=0.3)
                vendors_d = provider.generate_json(VENDORS_SYSTEM_PROMPT, user_ctx, temperature=0.3)

                plan_dict = {
                    "profile": profile_payload.model_dump(),
                    "ideas": ideas_d,
                    "budget": budget_d,
                    "timeline": timeline_d,
                    "vendors": vendors_d,
                    "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "model_used": DEFAULT_GROQ_MODEL if os.getenv("GROQ_API_KEY") else "high-craft-curated-engine",
                    "status": "success"
                }
                success = True
            except Exception as ex:
                st.error(f"Execution Error: {str(ex)}")

        if success and plan_dict:
            st.session_state.current_plan = plan_dict
            st.toast("Production Blueprint generated successfully!", icon="✦")

# -----------------------------------------------------------------------------
# Results Presentation Tabs
# -----------------------------------------------------------------------------
if st.session_state.current_plan:
    plan = st.session_state.current_plan
    ideas = plan["ideas"]
    budget = plan["budget"]
    timeline = plan["timeline"]
    vendors = plan["vendors"]
    profile = plan["profile"]
    curr = profile.get("currency", "USD")

    # Bento Grid Top Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f"""
            <div class="bento-card">
                <div class="bento-label">Total Capital Cap</div>
                <div class="bento-value">{curr} {budget['total_budget']:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f"""
            <div class="bento-card">
                <div class="bento-label">Allocated Spend</div>
                <div class="bento-value">{curr} {budget['allocated_subtotal']:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f"""
            <div class="bento-card">
                <div class="bento-label">Guarded Contingency</div>
                <div class="bento-value" style="color: #34D399;">{curr} {budget['contingency_reserve']:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            f"""
            <div class="bento-card">
                <div class="bento-label">Target Spend / Guest</div>
                <div class="bento-value" style="color: #38BDF8;">{curr} {budget['cost_per_guest']:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Main Tabs
    tab_ideas, tab_budget, tab_timeline, tab_vendors, tab_export = st.tabs([
        "✦ 1. Concept & Atmosphere",
        "💰 2. Financial Ledger & Budget",
        "⏱ 3. Operational Timeline",
        "📋 4. Vendor Command & Contracts",
        "📦 5. Export Package",
    ])

    # -------------------------------------------------------------------------
    # TAB 1: Concept & Atmosphere
    # -------------------------------------------------------------------------
    with tab_ideas:
        st.markdown(f"### {ideas['theme_title']}")
        st.markdown(f"*{ideas['tagline']}*")

        st.markdown(
            f"""
            <div style="background: rgba(14, 21, 34, 0.6); border-left: 3px solid #38BDF8; padding: 1.1rem 1.4rem; border-radius: 0 10px 10px 0; margin: 1.2rem 0; line-height: 1.6; color: #E2E8F0;">
                {ideas['creative_narrative']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("#### Curated Chromatic Palette")
        palette_cols = st.columns(len(ideas["color_palette"]))
        for idx, swatch in enumerate(ideas["color_palette"]):
            with palette_cols[idx]:
                hex_c = swatch["hex_code"]
                st.markdown(
                    f"""
                    <div class="swatch-box" style="background-color: {hex_c};">
                        <span class="swatch-hex">{hex_c}</span>
                    </div>
                    <div style="font-size: 0.85rem; font-weight: 600; margin-top: 6px; color: #F8FAFC;">{swatch['name']}</div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">{swatch['usage_role']}</div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

        st.markdown("#### Sensory Dimensions")
        s1, s2, s3, s4 = st.columns(4)
        sensory = ideas["sensory_atmosphere"]
        with s1:
            st.markdown(
                f"""
                <div class="sensory-card">
                    <h4>💡 Architectural Lighting</h4>
                    <p>{sensory['lighting_design']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with s2:
            st.markdown(
                f"""
                <div class="sensory-card">
                    <h4>🎵 Acoustic Landscape</h4>
                    <p>{sensory['acoustic_profile']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with s3:
            st.markdown(
                f"""
                <div class="sensory-card">
                    <h4>🏺 Tactile Textures</h4>
                    <p>{sensory['tactile_textures']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with s4:
            st.markdown(
                f"""
                <div class="sensory-card">
                    <h4>🌿 Botanicals & Scent</h4>
                    <p>{sensory['scent_and_botanicals']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

        col_moments, col_activities = st.columns(2)
        with col_moments:
            st.markdown("#### Signature Moments")
            for m in ideas["signature_moments"]:
                with st.container(border=True):
                    st.markdown(f"**{m['moment_name']}** — `{m['timing']}`")
                    st.write(m['description'])
                    st.caption(f"✨ *Execution Hook:* {m['wow_factor_detail']}")

        with col_activities:
            st.markdown("#### Interactive Guest Experiences")
            for act in ideas["interactive_activities"]:
                with st.container(border=True):
                    st.markdown(f"**{act['activity_name']}**")
                    st.markdown(f"<span style='display:inline-block; padding:2px 8px; background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); border-radius:6px; font-size:0.75rem; color:#38BDF8;'>{act['audience_fit']}</span>", unsafe_allow_html=True)
                    st.write(act['description'])
                    st.caption(f"🛠 *Logistics:* {act['setup_requirement']}")

    # -------------------------------------------------------------------------
    # TAB 2: Financial Ledger
    # -------------------------------------------------------------------------
    with tab_budget:
        st.markdown("### Granular Capital Allocation")
        st.markdown(f"*{budget['financial_health_summary']}*")

        items = budget["items"]
        df_items = pd.DataFrame(items)

        st.dataframe(
            df_items,
            column_config={
                "category": st.column_config.TextColumn("Discipline", width="medium"),
                "item_name": st.column_config.TextColumn("Line Item Specification", width="large"),
                "estimated_cost": st.column_config.NumberColumn(
                    f"Estimated Spend ({curr})",
                    format=f"{curr} %.2f",
                ),
                "percentage_of_budget": st.column_config.ProgressColumn(
                    "% of Budget",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100
                ),
                "priority": st.column_config.TextColumn("Priority", width="small"),
                "pro_negotiation_tip": st.column_config.TextColumn("Negotiation Lever", width="large"),
            },
            hide_index=True,
            use_container_width=True
        )

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("#### High-Leverage Cost Mitigations")
        for lever in budget.get("top_cost_saving_levers", []):
            st.markdown(f"- 💡 {lever}")

    # -------------------------------------------------------------------------
    # TAB 3: Timeline & Run-of-Show
    # -------------------------------------------------------------------------
    with tab_timeline:
        st.markdown("### Chronological Roadmap & Day-Of Execution")
        st.markdown(f"**Buffer Philosophy:** {timeline['buffer_strategy']}")
        st.warning(f"⚠️ **Critical Path Dependency:** {timeline['critical_path_warning']}")

        st.markdown("#### Strategic Planning Milestones")
        for ms in timeline["planning_milestones"]:
            with st.container(border=True):
                c_p1, c_p2 = st.columns([3, 1])
                with c_p1:
                    st.markdown(f"##### {ms['phase']} (`{ms['timeframe']}`)")
                with c_p2:
                    st.caption(f"Lead: **{ms['responsible_party']}**")

                for act in ms["action_items"]:
                    st.markdown(f"- [ ] {act}")
                st.markdown(f"**Irrevocable Milestone:** `{ms['critical_deadline']}`")

        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

        st.markdown("#### Day-Of Hour-by-Hour Run of Show")
        df_dayof = pd.DataFrame(timeline["day_of_run_of_show"])
        st.dataframe(
            df_dayof,
            column_config={
                "time_window": st.column_config.TextColumn("Time Window", width="small"),
                "segment_title": st.column_config.TextColumn("Segment", width="medium"),
                "description": st.column_config.TextColumn("Stage & Backstage Direction", width="large"),
                "coordinator_in_charge": st.column_config.TextColumn("Headset Lead", width="small"),
                "buffer_minutes": st.column_config.NumberColumn("Injected Buffer", format="%d min"),
            },
            hide_index=True,
            use_container_width=True
        )

    # -------------------------------------------------------------------------
    # TAB 4: Vendors Command
    # -------------------------------------------------------------------------
    with tab_vendors:
        st.markdown("### Vendor Procurement, Interviewing & Contract Traps")
        st.info(f"🛡️ **Permit & Liability Advisory:** {vendors['liability_and_permit_advice']}")

        st.markdown("#### Discipline-Specific Contracting Guides")
        for v in vendors["vendor_categories"]:
            with st.expander(f"✦ {v['vendor_type']} (Allocation: {v['recommended_budget_allocation']})", expanded=True):
                v_col1, v_col2 = st.columns(2)

                with v_col1:
                    st.markdown("**Sourcing Checklist & Must-Haves:**")
                    for req in v["sourcing_checklist"]:
                        st.markdown(f"- {req}")

                    st.markdown("<br>**Hard-Hitting Interview Probes:**", unsafe_allow_html=True)
                    for q in v["hard_hitting_interview_questions"]:
                        st.markdown(f"- ❓ *\"{q}\"*")

                with v_col2:
                    st.markdown("**Contract Red Flags to Strike:**")
                    for flag in v["contract_red_flags"]:
                        st.markdown(f"- 🚨 <span style='color:#F87171;'>{flag}</span>", unsafe_allow_html=True)

                    st.markdown("<br>**Key Deliverables to Lock:**", unsafe_allow_html=True)
                    for deliv in v["key_deliverables_to_lock"]:
                        st.markdown(f"- 🔒 {deliv}")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("#### Golden Contractual Rules")
        for rule in vendors.get("contract_golden_rules", []):
            st.markdown(f"- ⚖️ **Rule:** {rule}")

    # -------------------------------------------------------------------------
    # TAB 5: Export Package
    # -------------------------------------------------------------------------
    with tab_export:
        st.markdown("### Export Production Package")
        st.markdown("Download comprehensive documentation for clients, vendors, and coordinators.")

        md_export = f"""# EVENT PRODUCTION BLUEPRINT
**Generated:** {plan.get('generated_at', datetime.utcnow().isoformat())}
**Engine:** {plan.get('model_used', 'Event Intelligence Engine')}

---
## 1. EVENT PROFILE
- **Type:** {profile['event_type']}
- **Guest Count:** {profile['guest_count']}
- **Total Budget:** {budget['total_budget']:,.2f} {curr}
- **Location:** {profile['location']}
- **Vibe:** {profile['aesthetic_vibe']}

---
## 2. CREATIVE CONCEPT & THEME
### {ideas['theme_title']}
*{ideas['tagline']}*

{ideas['creative_narrative']}

### Sensory Specs
- **Lighting:** {ideas['sensory_atmosphere']['lighting_design']}
- **Acoustics:** {ideas['sensory_atmosphere']['acoustic_profile']}
- **Textures:** {ideas['sensory_atmosphere']['tactile_textures']}
- **Botanicals:** {ideas['sensory_atmosphere']['scent_and_botanicals']}

---
## 3. FINANCIAL BREAKDOWN
- **Total Budget:** {curr} {budget['total_budget']:,.2f}
- **Allocated Spend:** {curr} {budget['allocated_subtotal']:,.2f}
- **Contingency Buffer:** {curr} {budget['contingency_reserve']:,.2f}
- **Per Guest Spend:** {curr} {budget['cost_per_guest']:,.2f}

### Line Items
"""
        for it in budget["items"]:
            md_export += f"- **{it['category']}** | {it['item_name']}: {curr} {it['estimated_cost']:,.2f} ({it['percentage_of_budget']}%) [{it['priority']}]\n  *Negotiation Tip:* {it['pro_negotiation_tip']}\n"

        md_export += f"\n---\n## 4. CRITICAL PATH & TIMELINE\n**Buffer Strategy:** {timeline['buffer_strategy']}\n**Warning:** {timeline['critical_path_warning']}\n\n### Day-Of Run of Show\n"
        for seg in timeline["day_of_run_of_show"]:
            md_export += f"- `{seg['time_window']}` **{seg['segment_title']}** (Lead: {seg['coordinator_in_charge']}, Buffer: {seg['buffer_minutes']} min)\n  {seg['description']}\n"

        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.download_button(
                label="📄 Download Production Brief (.md)",
                data=md_export,
                file_name=f"event_blueprint_{profile['event_type'].lower().replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        with d_col2:
            st.download_button(
                label="⚙️ Download Structured JSON Data (.json)",
                data=json.dumps(plan, indent=2),
                file_name=f"event_data_{profile['event_type'].lower().replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True
            )

        st.text_area("Preview Export Markdown", value=md_export, height=320)

else:
    st.markdown(
        """
        <div style="text-align: center; padding: 4rem 2rem; background: rgba(14, 21, 34, 0.4); border: 1px dashed rgba(255, 255, 255, 0.1); border-radius: 16px; margin-top: 2rem;">
            <div style="font-size: 2.2rem; margin-bottom: 0.8rem;">✦</div>
            <h3 style="color: #F8FAFC; margin-bottom: 0.5rem;">No Active Event Blueprint</h3>
            <p style="color: #94A3B8; max-width: 520px; margin: 0 auto 1.5rem auto;">
                Select a curated archetype from the sidebar or customize your event specifications in the panel above to generate an itemized, sensory-crafted blueprint.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
