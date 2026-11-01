"""
Deterministic Curated Fallback Engine for Event Architecture & Production Studio.
Provides high-craft fallback data conforming strictly to EventBlueprintResponse.
"""

from schemas import (
    BudgetItem,
    EventBlueprintResponse,
    EventRequest,
    FinancialBlueprint,
    SensoryBlueprint,
    TimelinePhase,
    VendorContractSpec,
)


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
                "#E69C24 Amber Glow",
            ],
            signature_experience="Smoked botanical aperitif welcome served in fluted crystal coupes alongside an unhurried, wood-fired communal banquet.",
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
                    notes="Negotiate complimentary load-in hours the morning prior to avoid 1.5x weekend overtime.",
                ),
                BudgetItem(
                    category="Catering & Bar",
                    item_name="Farm-to-Table Plated Banquet & Curated Natural Wines",
                    estimated_cost=round(allocated * 0.35, 2),
                    percentage_of_total=31.5,
                    notes="Lock a flat-rate corkage agreement rather than standard per-bottle markups.",
                ),
                BudgetItem(
                    category="Florals & Atmosphere",
                    item_name="Architectural Foliage, Olive Branch Clusters & Pillar Arrays",
                    estimated_cost=round(allocated * 0.12, 2),
                    percentage_of_total=10.8,
                    notes="Repurpose welcome focal botanicals to flank the banquet tables post-reception.",
                ),
                BudgetItem(
                    category="Production & Audio",
                    item_name="2200K Ambient Lighting Grid & High-Fidelity Wireless Sound",
                    estimated_cost=round(allocated * 0.10, 2),
                    percentage_of_total=9.0,
                    notes="Bundle sound and lighting under a unified AV contractor to eliminate redundant travel fees.",
                ),
                BudgetItem(
                    category="Photography & Film",
                    item_name="Documentary Film & Digital Visual Capture (8 Hours)",
                    estimated_cost=round(allocated * 0.10, 2),
                    percentage_of_total=9.0,
                    notes="Request full digital printing rights and select selects within 72 hours.",
                ),
                BudgetItem(
                    category="Coordination & Permits",
                    item_name="Principal Producer, Day-Of Team & Municipal Permits",
                    estimated_cost=round(allocated * 0.05, 2),
                    percentage_of_total=4.5,
                    notes="Flat project fee contract with clear overtime parameters beyond midnight.",
                ),
            ],
        ),
        timeline=[
            TimelinePhase(
                timeframe=f"T-Minus {req.weeks_to_event} to {max(req.weeks_to_event - 12, 12)} Weeks",
                phase_title="Phase 1: Foundation & High-Leverage Anchors",
                action_items=[
                    "Execute venue contract with certified sound ordinance and strike curfew hours.",
                    "Lock documentary photographer and culinary partner deposits.",
                    "Verify electrical load amperage capacity for production runs.",
                ],
                critical_deadline="Week 4: Irrevocable venue deposit lock",
            ),
            TimelinePhase(
                timeframe="T-Minus 12 to 4 Weeks",
                phase_title="Phase 2: Sensory Architecture & Vendor Specs",
                action_items=[
                    "Finalize seasonal menu tasting and allergen protocol matrix.",
                    "Approve lighting schematic (2200K) and microphone RF frequency scans.",
                    "Collect all vendor Certificates of Insurance (COI).",
                ],
                critical_deadline="T-Minus 30 Days: Sourcing and permits sign-off",
            ),
            TimelinePhase(
                timeframe="T-Minus 4 to 1 Weeks",
                phase_title="Phase 3: Operational Logistics & Seating Matrix",
                action_items=[
                    "Finalize exact guest guarantee count and dietary list with caterer.",
                    "Stagger delivery dock load-in times for florist and AV crews.",
                    "Conduct wireless mic walk-around sound check on site.",
                ],
                critical_deadline="T-Minus 14 Days: Final headcount lock",
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
                    "23:30 - Guest farewell & systematic rental strike.",
                ],
                critical_deadline="23:30: Sound curfew strict enforcement",
            ),
        ],
        vendor_matrix=[
            VendorContractSpec(
                category="Venue & Facilities",
                estimated_budget=round(allocated * 0.28, 2),
                deliverables=[
                    "12-hour continuous private estate access",
                    "Dedicated power runs (minimum four 20A circuits)",
                    "Secure on-site staging and refrigeration room",
                ],
                interview_questions=[
                    "What is your exact fee structure if the load-out crew exceeds the midnight cutoff by 30 minutes?",
                    "Can you walk us through the emergency generator protocol if local grid power fluctuates?",
                    "Are there mandatory vendor lists, or are outside licensed contractors permitted without penalty?",
                ],
                required_permits_coi="Active $2M General Liability COI naming venue and client as additional insureds.",
            ),
            VendorContractSpec(
                category="Culinary & Beverage",
                estimated_budget=round(allocated * 0.35, 2),
                deliverables=[
                    "Hand-passed canapés, 3-course seasonal plated dinner, wine service",
                    "Complete kitchen setup, breakdown, and allergen-safe preparation",
                    "Trained service staff at a 1:10 guest ratio",
                ],
                interview_questions=[
                    "How do you accommodate unforeseen severe dietary allergies on the night without delay?",
                    "Are kitchen cleanup, linen pressing, and ice included in the quote or billed in arrears?",
                    "What percentage of prep is executed live on-site versus reheated commissary food?",
                ],
                required_permits_coi="State Food Handler certifications, Liquor Liability Insurance, Health Dept Permit.",
            ),
            VendorContractSpec(
                category="Audio, DJ & Lighting Production",
                estimated_budget=round(allocated * 0.10, 2),
                deliverables=[
                    "Wireless handheld and lapel mics with dual-channel receivers",
                    "2200K architectural ambient uplights and spotlight array",
                    "Backup audio console and secondary playback machine on standby",
                ],
                interview_questions=[
                    "How do you manage room acoustics and reverberation in high-ceiling or glass-heavy areas?",
                    "What is your backup protocol if your primary mixer or amplifier fails during speeches?",
                    "Do you respect strict client song veto lists, and what is your overtime billing increment?",
                ],
                required_permits_coi="Commercial General Liability COI and local Municipal Amplified Sound Permit.",
            ),
            VendorContractSpec(
                category="Documentary Photography & Film",
                estimated_budget=round(allocated * 0.10, 2),
                deliverables=[
                    "Dual-camera documentary coverage (8 continuous hours)",
                    "Color-graded sneak-peek gallery of 40 selects within 72 hours",
                    "Complete high-resolution digital master gallery with full print release",
                ],
                interview_questions=[
                    "Do your cameras record to dual redundant memory cards simultaneously in real-time?",
                    "Who specifically is shooting my event—you personally or an associate shooter?",
                    "How are raw master files archived, and how many years do you guarantee file safety?",
                ],
                required_permits_coi="Standard Equipment Liability and Commercial Production Insurance.",
            ),
        ],
    )

