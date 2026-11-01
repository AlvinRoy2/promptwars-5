/**
 * Robust Client-Side Fallback Blueprint Generator
 * Used when backend is offline or during instant preview fallback.
 */

export function generateFallbackBlueprint(req) {
  const total = Number(req.total_budget) || 48000;
  const contingency = Math.round(total * 0.10);
  const allocated = Math.round(total - contingency);
  const guestCount = Math.max(Number(req.guest_count) || 120, 1);
  const costPerGuest = (total / guestCount).toFixed(2);
  const curr = req.currency || "USD";

  return {
    event_summary: `An architectural, high-craft ${req.event_type.toLowerCase()} engineered for ${req.guest_count} guests in ${req.location}. Financial ledger is strictly balanced with a 10% guarded contingency reserve (${curr} ${contingency.toLocaleString()}), calibrated to '${req.sensory_theme.slice(0, 60)}...'.`,
    sensory_concept: {
      lighting_ambiance: "2200K warm-amber clustered pillar illumination, recessed table pin-spots, and soft kinetic architectural grazing along raw stone backdrops.",
      acoustic_vibe: "Live acoustic fingerstyle guitar transitioning into low-tempo vinyl jazz; dining acoustics strictly capped at 78dB for uninterrupted dialogue.",
      decor_color_palette: [
        "#1A1D24 Obsidian Slate",
        "#C85A32 Weathered Terracotta",
        "#D8CAB8 Raw Belgian Flax",
        "#556048 Aged Olive Leaf",
        "#FFAD32 Warm Amber Glow"
      ],
      signature_experience: "Smoked botanical aperitif welcome served in fluted crystal coupes alongside an unhurried, wood-fired communal banquet."
    },
    financial_ledger: {
      total_budget: total,
      allocated_budget: allocated,
      contingency_reserve: contingency,
      cost_per_guest: Number(costPerGuest),
      items: [
        {
          category: "Venue & Architectural Space",
          item_name: "Exclusive Historic Vineyard Estate & Covered Wine Cellar",
          estimated_cost: Math.round(allocated * 0.32),
          percentage_of_total: 28.8,
          notes: "Includes 12-hour exclusive access, back-of-house commercial kitchen, and site load-in supervisor."
        },
        {
          category: "Catering & Beverage Program",
          item_name: "Multi-Course Wood-Fired Dinner & Natural Wine Pairing",
          estimated_cost: Math.round(allocated * 0.30),
          percentage_of_total: 27.0,
          notes: "Dedicated gluten-free certified prep line, Sommelier pairing, and late-night artisan espresso bar."
        },
        {
          category: "Atmosphere & Sensory Lighting",
          item_name: "Architectural 2200K Filament Lighting & Acoustic Shell",
          estimated_cost: Math.round(allocated * 0.14),
          percentage_of_total: 12.6,
          notes: "Custom dimmable warm ambient strings, table candle clusters, and calibrated dining acoustic baffles."
        },
        {
          category: "Production & Florals",
          item_name: "Seasonal Organic Botanicals & Raw Linen Installations",
          estimated_cost: Math.round(allocated * 0.12),
          percentage_of_total: 10.8,
          notes: "Zero floral foam, locally foraged olive branches, raw unbleached linen runners and letterpress paper."
        },
        {
          category: "Documentation & Sound",
          item_name: "Documentary Editorial Photography & Hybrid Sound Set",
          estimated_cost: Math.round(allocated * 0.12),
          percentage_of_total: 10.8,
          notes: "35mm analog and digital stills coverage; discrete ceremony lapels and vinyl playback system."
        }
      ]
    },
    timeline: [
      {
        timeframe: `T-Minus ${req.weeks_to_event} to ${Math.max(req.weeks_to_event - 8, 12)} Weeks`,
        phase_title: "Phase 1: Architectural Foundation & Anchor Locking",
        action_items: [
          "Execute venue lease contract with 48-hour cancellation buffer and noise ordinance schedule.",
          "Issue RFPs for catering with strict gluten-free safety audit protocols.",
          "Lock lead documentation team and establish shotlist guidelines."
        ],
        critical_deadline: `T-Minus ${Math.max(req.weeks_to_event - 8, 12)} Weeks: Non-refundable deposit caps locked.`
      },
      {
        timeframe: `T-Minus ${Math.max(req.weeks_to_event - 8, 12)} to 6 Weeks`,
        phase_title: "Phase 2: Sensory Engineering & Production Design",
        action_items: [
          "Conduct evening site lighting study at 19:30 to calibrate 2200K kelvin fixtures against venue ambient dusk.",
          "Finalize acoustic timeline: acoustic guitar for aperitif, vinyl jazz through dinner, groove set post-dinner.",
          "Coordinate specialty bar equipment requirements: dual group-head espresso machine electrical draw."
        ],
        critical_deadline: "T-Minus 6 Weeks: Power and sound permit endorsements filed with municipal authority."
      },
      {
        timeframe: "T-Minus 6 Weeks to T-Minus 14 Days",
        phase_title: "Phase 3: Operational Hardening & Contract Lockdown",
        action_items: [
          "Collect Certificates of Insurance (COI) naming venue as additional insured with $2M general liability.",
          "Lock finalized dietary headcount with catering kitchen; verify dedicated allergen workspace.",
          "Produce master load-in timeline with 45-minute staging windows for delivery trucks."
        ],
        critical_deadline: "T-Minus 14 Days: Final balance release; 10% contingency reserve locked for on-day adjustments."
      },
      {
        timeframe: "T-Minus 14 Days to Event Day",
        phase_title: "Phase 4: Run-of-Show Execution & Live Cadence",
        action_items: [
          "Pre-event walk-through with lead coordinator, venue manager, and catering head captain.",
          "Conduct acoustic dB soundcheck at 16:00 to verify 78dB cap during dinner segment.",
          "Release 10% contingency reserve exclusively for unexpected day-of overtime or weather adaptation."
        ],
        critical_deadline: "Event Day 16:30: Doors open. Sensory environment fully online."
      }
    ],
    vendor_matrix: [
      {
        category: "Venue Operator",
        estimated_budget: Math.round(allocated * 0.32),
        deliverables: [
          "12-hour exclusive site usage (10:00 - 22:00)",
          "Access to 200A 3-phase dedicated event power distribution",
          "Back-of-house waste and recycling sorting facility"
        ],
        interview_questions: [
          "What is the exact municipal decibel limit at the property boundary after 21:00?",
          "Are there load restrictions on delivery vehicles exceeding 10,000 lbs on access driveways?"
        ],
        required_permits_coi: "$2M Aggregate General Liability Certificate naming property owner as Additional Insured."
      },
      {
        category: "Catering & Beverage Lead",
        estimated_budget: Math.round(allocated * 0.30),
        deliverables: [
          "Hand-passed welcome aperitifs and 4-course wood-fired seated dinner",
          "Certified gluten-free preparation protocols and dedicated fryers",
          "Professional sommelier service and late-night espresso bar operation"
        ],
        interview_questions: [
          "What is your cross-contamination protocol when working in an off-premise mobile kitchen?",
          "What is your server-to-guest ratio during the main seated dining sequence?"
        ],
        required_permits_coi: "State Health Dept Food Handler Certification & ABC Liquor Liability Endorsement."
      },
      {
        category: "Lighting & Atmospheric Engineer",
        estimated_budget: Math.round(allocated * 0.14),
        deliverables: [
          "Complete low-voltage 2200K filament lighting array with flicker-free dimming",
          "Table accent pin-spots focused exclusively on floral arrangements",
          "On-site lighting technician from load-in through load-out"
        ],
        interview_questions: [
          "How do your fixtures handle generator voltage fluctuations without flickering on camera?",
          "What backup power supply is included in case of primary circuit trip?"
        ],
        required_permits_coi: "Commercial General Liability and Electrical Subcontractor License."
      },
      {
        category: "Acoustic & Audio Director",
        estimated_budget: Math.round(allocated * 0.12),
        deliverables: [
          "Line-array sound reinforcement system calibrated to 78dB maximum in dining zone",
          "Wireless UHF diversity microphone package with RF spectrum scan",
          "Turntable isolation booth and high-fidelity vinyl playback chain"
        ],
        interview_questions: [
          "How will you zone the audio so dining conversation remains effortless while dance zone is vibrant?",
          "Do you maintain duplicate backup transceivers on site for all microphones?"
        ],
        required_permits_coi: "Equipment In-Transit Inland Marine Insurance & General Liability."
      }
    ]
  };
}
