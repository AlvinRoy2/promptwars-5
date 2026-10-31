import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence, useScroll, useTransform } from 'motion/react';
import {
  Sparkles, DollarSign, Calendar, ShieldCheck, Download,
  Lightbulb, Music, CheckCircle2, Check, Activity,
  ArrowRight, Sliders, FileText, Zap, Clock,
  TrendingUp, LayoutGrid, BarChart3, MapPin, Users,
  ChevronRight, Eye
} from 'lucide-react';

import { ScrollProgress } from './components/magicui/ScrollProgress';
import { NumberTicker } from './components/magicui/NumberTicker';
import { Marquee } from './components/magicui/Marquee';

import imgWedding from './assets/hero-wedding.jpg';
import imgBirthday from './assets/hero-birthday.jpg';
import imgCommunity from './assets/hero-community.jpg';
import imgSpatialAi from './assets/hero-spatial-ai.jpg';
import imgMoodboard from './assets/hero-moodboard.jpg';

// ─── Curated Architectural Concepts & Scenes ──────────────────────────────────
const SCENES = [
  {
    id: 'wedding',
    title: 'Botanical Estate Wedding',
    tag: 'Napa Valley · 120 Guests',
    location: 'Napa Valley, CA — Private Vineyard & Stone Cellar',
    subtitle: 'Warm organic modernism with glowing 2200K amber candles & acoustic vinyl jazz',
    image: imgWedding,
    accentColor: '#FFAD32',
    accentDim: 'rgba(255, 173, 50, 0.15)',
    accentBorder: 'rgba(255, 173, 50, 0.45)',
    archetypeKey: 'Napa Valley Botanical Wedding',
    metrics: [
      { label: 'Kelvin Ambiance', value: '2200K' },
      { label: 'Capital Cap', value: '$48,000' },
      { label: 'Acoustic Ceiling', value: '78dB' }
    ],
    tags: ['Organic Modernism', 'Flax Linen', 'Wine Cellar', 'Zero Line Dances']
  },
  {
    id: 'spatial',
    title: 'Spatial AI Synthesis Core',
    tag: 'Algorithmic HUD · Multi-Sensory',
    location: 'Metropolitan Glass Pavilion — Kinetic Horizon',
    subtitle: 'Algorithmic event architecture with real-time risk calibration & phase gates',
    image: imgSpatialAi,
    accentColor: '#10CBE8',
    accentDim: 'rgba(16, 203, 232, 0.15)',
    accentBorder: 'rgba(16, 203, 232, 0.45)',
    archetypeKey: null,
    metrics: [
      { label: 'Contingency Safe', value: '10%' },
      { label: 'Phase-Gated', value: 'GANTT' },
      { label: 'Vendor COI', value: 'Audited' }
    ],
    tags: ['GenAI Synthesis', 'Mathematical Ledger', 'Live Hedging', 'COI Compliance']
  },
  {
    id: 'birthday',
    title: 'Milestone Celebration & Party',
    tag: 'Loft Studio · 85 Guests',
    location: 'Downtown Industrial Loft — Fluted Glass & Raw Concrete',
    subtitle: 'Neo-Tokyo aesthetic with modular synth live set and midnight street bao bar',
    image: imgBirthday,
    accentColor: '#915CFF',
    accentDim: 'rgba(145, 92, 255, 0.15)',
    accentBorder: 'rgba(145, 92, 255, 0.45)',
    archetypeKey: 'Cyberpunk 30th Milestone',
    metrics: [
      { label: 'Midnight Station', value: 'Bao Bar' },
      { label: 'Capital Cap', value: '$22,500' },
      { label: 'Sound Curfew', value: '01:00 AM' }
    ],
    tags: ['Brutalist Loft', 'Analog Synths', 'Craft Mixology', 'Arcade Nook']
  },
  {
    id: 'community',
    title: 'Civic Arts & Tech Gala',
    tag: 'Greenhouse · 250 Guests',
    location: 'Civic Greenhouse & Glass Pavilion — Waterfront Park',
    subtitle: 'Zero-waste architectural biophilia with hyper-local farm banquet and solar projections',
    image: imgCommunity,
    accentColor: '#22D3A5',
    accentDim: 'rgba(34, 211, 165, 0.15)',
    accentBorder: 'rgba(34, 211, 165, 0.45)',
    archetypeKey: 'Sustainable Arts & Tech Gala',
    metrics: [
      { label: 'Waste Protocol', value: 'Zero-Waste' },
      { label: 'Capital Cap', value: '$65,000' },
      { label: 'Transit Run', value: 'Shuttle' }
    ],
    tags: ['Living Moss', 'Hyper-Local Feast', 'Solar Kinetic', 'Curfew 22:00']
  },
  {
    id: 'moodboard',
    title: 'Sensory Chromatics & Texture',
    tag: 'Flax Linen · Florals · Stone',
    location: 'Studio Atelier — Tactile Material Library',
    subtitle: 'Tactile material board, natural Belgian flax, and custom letterpress stationery',
    image: imgMoodboard,
    accentColor: '#FFAD32',
    accentDim: 'rgba(255, 173, 50, 0.15)',
    accentBorder: 'rgba(255, 173, 50, 0.45)',
    archetypeKey: null,
    metrics: [
      { label: 'Color Palette', value: '5-Tone' },
      { label: 'Primary Linen', value: 'Belgian' },
      { label: 'Stationery', value: 'Letterpress' }
    ],
    tags: ['Atmospheric Lighting', 'Raw Terracotta', 'Handmade Paper', 'Smoked Glass']
  }
];

// ─── Telemetry Marquee Items ──────────────────────────────────────────────────
const MARQUEE_ITEMS = [
  { icon: Activity, label: '2200K Architectural Kelvin Lighting' },
  { icon: Music, label: '78dB Acoustic Dining Limits' },
  { icon: ShieldCheck, label: '10% Guarded Contingency Reserve' },
  { icon: CheckCircle2, label: 'COI Permit Lock & Vendor Audit' },
  { icon: Zap, label: 'Phase-Gated Chronological GANTT' },
  { icon: TrendingUp, label: 'Mathematical Capital Allocation Ledger' },
  { icon: MapPin, label: 'Venue Ordinance Sound Curfew Calibrated' },
  { icon: BarChart3, label: 'Per-Guest Spend Calibration' }
];

// ─── Curated Archetype Presets ────────────────────────────────────────────────
const ARCHETYPES = {
  'Napa Valley Botanical Wedding': {
    event_type: 'Wedding',
    location: 'Napa Valley, CA — Private Vineyard Lawn & Stone Cellar',
    guest_count: 120,
    currency: 'USD',
    total_budget: 48000.0,
    weeks_to_event: 36,
    sensory_theme: 'Warm Organic Modernism. Muted eucalyptus, raw linen, 2200K amber pillar candles, acoustic fingerstyle into vinyl jazz.',
    operational_constraints: 'Bride is celiac (strict gluten-free kitchen). Groom wants espresso bar after 10 PM. Zero corny line dances.'
  },
  'Cyberpunk 30th Milestone': {
    event_type: 'Milestone Birthday',
    location: 'Downtown Warehouse Loft — Concrete & Industrial Fluted Glass',
    guest_count: 85,
    currency: 'USD',
    total_budget: 22500.0,
    weeks_to_event: 14,
    sensory_theme: 'Neo-Tokyo Cyberpunk meets raw brutalism. Neon violet & obsidian accents, modular synth live set, craft mixology lab.',
    operational_constraints: 'Requires retro arcade cabinet nook and custom bao bun bar at midnight. City sound curfew at 01:00 AM.'
  },
  'Sustainable Arts & Tech Gala': {
    event_type: 'Community Gala',
    location: 'Civic Greenhouse & Glass Pavilion — Public Waterfront Park',
    guest_count: 250,
    currency: 'USD',
    total_budget: 65000.0,
    weeks_to_event: 24,
    sensory_theme: 'Zero-waste architectural biophilia. Living moss installations, solar-powered kinetic projections, hyper-local farm banquet.',
    operational_constraints: 'City sound permit curfew at 22:00. Requires wheelchair accessible shuttle runs from civic transit hub.'
  }
};

// ─── Robust Fallback Blueprint Generator ──────────────────────────────────────
function generateFallbackBlueprint(req) {
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

// ─── Main Application Component ───────────────────────────────────────────────
export default function App() {
  const [formData, setFormData] = useState(ARCHETYPES['Napa Valley Botanical Wedding']);
  const [selectedArchetype, setSelectedArchetype] = useState('Napa Valley Botanical Wedding');
  const [activeSceneIndex, setActiveSceneIndex] = useState(0);
  const activeScene = SCENES[activeSceneIndex];
  const [blueprint, setBlueprint] = useState(null);
  const [activeTab, setActiveTab] = useState('financial');
  const [isLoading, setIsLoading] = useState(false);
  const [backendOnline, setBackendOnline] = useState(false);
  // In development: Vite proxy forwards /api/* to localhost:8000
  // In production (Vercel): /api/* is routed to the serverless function
  // VITE_API_URL can override for custom deployments
  const [backendUrl] = useState(import.meta.env.VITE_API_URL || '');
  const [copiedHex, setCopiedHex] = useState(null);

  const heroRef = useRef(null);
  const workspaceRef = useRef(null);
  const conceptsRef = useRef(null);
  const blueprintRef = useRef(null);

  const { scrollYProgress } = useScroll({
    target: heroRef,
    offset: ['start start', 'end start']
  });
  const heroImgY = useTransform(scrollYProgress, [0, 1], ['0%', '18%']);

  // Check backend health via the canonical /api/health route (Vercel rewrite -> backend service)
  useEffect(() => {
    fetch(`${backendUrl}/api/health`)
      .then(r => r.json())
      .then(d => { if (d.status === 'healthy') setBackendOnline(true); })
      .catch(() => setBackendOnline(false));
  }, [backendUrl]);

  // Derived financial computations
  const totalBudget = Number(formData.total_budget || 0);
  const guestCount = Math.max(Number(formData.guest_count || 1), 1);
  const computedSpendPerGuest = (totalBudget / guestCount).toFixed(2);
  const contingencyAmt = Math.round(totalBudget * 0.10);
  const allocatedAmt = Math.round(totalBudget - contingencyAmt);
  const curr = formData.currency || 'USD';

  const scrollToSection = (sec) => {
    if (sec === 'workspace') workspaceRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    else if (sec === 'concepts') conceptsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    else if (sec === 'blueprint') blueprintRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const handleArchetypeClick = (name) => {
    if (ARCHETYPES[name]) {
      setFormData(ARCHETYPES[name]);
      setSelectedArchetype(name);
      const matchIdx = SCENES.findIndex(s => s.archetypeKey === name);
      if (matchIdx !== -1) {
        setActiveSceneIndex(matchIdx);
      }
    }
  };

  const handleSceneSelect = (idx) => {
    setActiveSceneIndex(idx);
    const scene = SCENES[idx];
    if (scene.archetypeKey && ARCHETYPES[scene.archetypeKey]) {
      setFormData(ARCHETYPES[scene.archetypeKey]);
      setSelectedArchetype(scene.archetypeKey);
    }
  };

  const handleSynthesize = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setBlueprint(null);

    if (backendOnline) {
      try {
        const res = await fetch(`${backendUrl}/api/blueprint`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });
        if (res.ok) {
          const data = await res.json();
          setBlueprint(data);
          setIsLoading(false);
          setTimeout(() => blueprintRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 200);
          return;
        }
      } catch (err) {
        console.warn('Backend unavailable, falling back to curated engine', err);
      }
    }

    // Graceful offline fallback
    setTimeout(() => {
      setBlueprint(generateFallbackBlueprint(formData));
      setIsLoading(false);
      setTimeout(() => blueprintRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 200);
    }, 750);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopiedHex(text);
    setTimeout(() => setCopiedHex(null), 1800);
  };

  const downloadFile = (content, filename, type) => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const exportMarkdown = () => {
    if (!blueprint) return '';
    let md = `# EVENT PRODUCTION BLUEPRINT\n**Event:** ${formData.event_type} (${formData.guest_count} guests)\n**Location:** ${formData.location}\n**Budget:** ${curr} ${Number(formData.total_budget).toLocaleString()}\n\n`;
    md += `## SUMMARY\n${blueprint.event_summary}\n\n`;
    md += `## SENSORY ARCHITECTURE\n- **Lighting:** ${blueprint.sensory_concept.lighting_ambiance}\n- **Acoustics:** ${blueprint.sensory_concept.acoustic_vibe}\n- **Signature Moment:** ${blueprint.sensory_concept.signature_experience}\n\n`;
    md += `## FINANCIAL CAPITAL ALLOCATION\nTotal Budget: ${curr} ${blueprint.financial_ledger.total_budget.toLocaleString()}\nAllocated: ${curr} ${blueprint.financial_ledger.allocated_budget.toLocaleString()}\nGuarded Contingency Reserve: ${curr} ${blueprint.financial_ledger.contingency_reserve.toLocaleString()}\n\n`;
    blueprint.financial_ledger.items.forEach(it => {
      md += `- **${it.category}** | ${it.item_name}: ${curr} ${it.estimated_cost.toLocaleString()} (${it.percentage_of_total}%) — ${it.notes}\n`;
    });
    return md;
  };

  return (
    <div className="relative min-h-screen bg-[#070A10] text-[#F6F4EF] selection:bg-[#10CBE8]/30">
      <ScrollProgress />

      {/* ── Fixed Site Navigation Bar ────────────────────────────────────────── */}
      <header className="site-nav">
        <div className="site-nav-inner">
          <div className="nav-brand">
            <Sparkles className="w-4 h-4 text-[#10CBE8]" />
            <span>PROMPTWARS</span>
            <span className="t-label text-[10px] text-[#526070] font-normal tracking-wider ml-1">/ STUDIO</span>
          </div>

          <nav className="nav-links">
            <button onClick={() => scrollToSection('concepts')} className="nav-link">Concepts</button>
            <button onClick={() => scrollToSection('workspace')} className="nav-link">Studio</button>
            {blueprint && (
              <>
                <button onClick={() => { scrollToSection('blueprint'); setActiveTab('financial'); }} className={`nav-link ${activeTab === 'financial' ? 'active' : ''}`}>Ledger</button>
                <button onClick={() => { scrollToSection('blueprint'); setActiveTab('timeline'); }} className={`nav-link ${activeTab === 'timeline' ? 'active' : ''}`}>Timeline</button>
                <button onClick={() => { scrollToSection('blueprint'); setActiveTab('sensory'); }} className={`nav-link ${activeTab === 'sensory' ? 'active' : ''}`}>Sensory</button>
                <button onClick={() => { scrollToSection('blueprint'); setActiveTab('vendors'); }} className={`nav-link ${activeTab === 'vendors' ? 'active' : ''}`}>Vendors</button>
              </>
            )}
          </nav>

          <div className="nav-actions">
            <div className="api-badge">
              <span className={`status-dot ${backendOnline ? 'online' : 'offline'}`} />
              <span className="t-mono text-[10px] text-[#9AA9BD] font-medium">
                {backendOnline ? 'GROQ ENGINE ACTIVE' : 'LOCAL ENGINE'}
              </span>
            </div>
            <button onClick={() => scrollToSection('workspace')} className="btn-configure">
              <Sliders className="w-3.5 h-3.5 text-[#10CBE8]" />
              <span>Configure</span>
            </button>
          </div>
        </div>
      </header>

      {/* ── 1. Cinematic Hero Section ──────────────────────────────────────── */}
      <section ref={heroRef} className="hero-section">
        {/* Parallax Edge-to-Edge Visual Showcase */}
        <div className="hero-bg">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeScene.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
              className="absolute inset-0"
            >
              <motion.img
                src={activeScene.image}
                alt={activeScene.title}
                className="hero-bg-img"
                style={{ y: heroImgY }}
              />
            </motion.div>
          </AnimatePresence>

          {/* Vignette Gradients for Editorial Contrast */}
          <div className="hero-vignette-top" />
          <div className="hero-vignette-left" />
          <div className="hero-vignette-bottom" />

          {/* Scene Accent Ambient Glow */}
          <div
            className="hero-glow transition-all duration-700"
            style={{
              background: `radial-gradient(ellipse 65% 55% at 75% 45%, ${activeScene.accentColor}25 0%, transparent 70%)`
            }}
          />
        </div>

        {/* Hero Content */}
        <div className="hero-content-wrapper">
          <div className="hero-grid">

            {/* Left: Headline & Actions */}
            <div>
              <motion.div
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 }}
                className="hero-eyebrow"
              >
                PROMPTWARS · PRODUCTION STUDIO 2026
              </motion.div>

              <motion.h1
                initial={{ opacity: 0, y: 22 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
                className="hero-headline mb-4"
              >
                Event Architecture <span className="hero-accent">&amp; Production Studio</span>
              </motion.h1>

              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, delay: 0.3 }}
                className="hero-copy"
              >
                High-craft GenAI blueprints for weddings, galas &amp; milestone celebrations — engineered with mathematical capital ledgers, sensory architecture, and hard-hitting vendor contracts.
              </motion.p>

              <motion.div
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
                className="hero-ctas"
              >
                <button onClick={() => scrollToSection('workspace')} className="btn-build">
                  <Sparkles className="w-4 h-4" />
                  <span>Configure Blueprint</span>
                  <ArrowRight className="w-4 h-4 ml-0.5" />
                </button>
                <button onClick={() => scrollToSection('concepts')} className="btn-explore">
                  <Eye className="w-4 h-4 text-[#9AA9BD]" />
                  <span>Explore Concepts</span>
                </button>
              </motion.div>

              <div className="hero-capabilities">
                <div className="hero-cap-item">
                  <ShieldCheck className="w-3.5 h-3.5 text-[#22D3A5]" />
                  <span>10% Guarded Contingency</span>
                </div>
                <div className="hero-cap-item">
                  <Music className="w-3.5 h-3.5 text-[#10CBE8]" />
                  <span>78dB Acoustic Decibel Limits</span>
                </div>
                <div className="hero-cap-item">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[#FFAD32]" />
                  <span>COI Permitted Vendors</span>
                </div>
              </div>
            </div>

            {/* Right: Floating Glassmorphism Concept Overlay Card */}
            <div className="hero-right-col">
              <motion.div
                key={activeScene.id + '-hud'}
                initial={{ opacity: 0, y: 18 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.55, ease: [0.16, 1, 0.3, 1] }}
                className="concept-overlay-card"
                style={{ borderColor: activeScene.accentBorder }}
              >
                <div className="concept-card-eyebrow">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: activeScene.accentColor }} />
                  <span className="t-label text-[10px]" style={{ color: activeScene.accentColor }}>{activeScene.tag}</span>
                </div>

                <h3 className="concept-card-title">{activeScene.title}</h3>

                <div className="concept-card-location">
                  <MapPin className="w-3.5 h-3.5 text-[#9AA9BD] shrink-0" />
                  <span className="truncate">{activeScene.location}</span>
                </div>

                <div className="concept-card-metrics">
                  {activeScene.metrics.map((m, i) => (
                    <div key={i} className="concept-metric">
                      <div>
                        <div className="concept-metric-val">{m.value}</div>
                        <div className="concept-metric-label">{m.label}</div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="concept-card-tags">
                  {activeScene.tags.map((t, i) => (
                    <span key={i} className="concept-tag">{t}</span>
                  ))}
                </div>
              </motion.div>
            </div>

          </div>
        </div>
      </section>

      {/* ── 2. Architectural Telemetry Marquee ─────────────────────────────── */}
      <section className="marquee-strip">
        <Marquee pauseOnHover repeat={3} className="h-full">
          {MARQUEE_ITEMS.map((item, i) => {
            const Icon = item.icon;
            return (
              <span key={i} className="marquee-pill">
                <Icon className="w-3 h-3 text-[#10CBE8]" />
                {item.label}
              </span>
            );
          })}
        </Marquee>
      </section>

      {/* ── 3. Curated Concepts Showcase Rail ──────────────────────────────── */}
      <section ref={conceptsRef} className="concepts-section">
        <div className="concepts-inner">
          <div className="concepts-header">
            <div>
              <span className="t-label text-[#10CBE8]">Curated Architectural Concepts</span>
              <p className="concepts-subtitle">Select any reference scenario to update the visual ambience and parameters</p>
            </div>
            <button
              onClick={() => handleSceneSelect((activeSceneIndex + 1) % SCENES.length)}
              className="concepts-arrow-btn"
              aria-label="Next concept"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          <div className="concepts-scroll">
            {SCENES.map((scene, idx) => {
              const isSelected = activeSceneIndex === idx;
              return (
                <div
                  key={scene.id}
                  role="button"
                  tabIndex={0}
                  aria-label={`Select concept: ${scene.title}`}
                  aria-pressed={isSelected}
                  onClick={() => handleSceneSelect(idx)}
                  onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && handleSceneSelect(idx)}
                  className={`concept-tile ${isSelected ? 'active' : ''}`}
                >
                  <div className="concept-tile-img-wrap">
                    <img src={scene.image} alt={scene.title} className="concept-tile-img" />
                    {isSelected && (
                      <div className="concept-tile-active-badge bg-[#FFAD32] text-black">
                        <Check className="w-3 h-3 stroke-[3]" />
                      </div>
                    )}
                  </div>
                  <div className="concept-tile-body">
                    <div className="concept-tile-title truncate">{scene.title}</div>
                    <div className="concept-tile-sub truncate">{scene.tag}</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ── 4. Main Workspace: Form & Live Budget Engine ───────────────────── */}
      <main ref={workspaceRef} className="workspace-main">
        <div className="workspace-inner">
          <div className="workspace-grid">

            {/* Left: Event Profile Specification Card */}
            <div className="ws-card">
              <div className="ws-card-header">
                <div className="ws-card-icon bg-[#10CBE8]/10 text-[#10CBE8] border-[#10CBE8]/30">
                  <Sliders className="w-4 h-4" />
                </div>
                <div className="ws-card-title-block">
                  <h2 className="ws-card-title">Event Profile Specification</h2>
                  <p className="ws-card-subtitle">Define parameters, constraints, and sensory guidelines</p>
                </div>
              </div>

              {/* Quick Archetype Pills */}
              <div className="mb-5">
                <span className="t-label block mb-2 text-[#9AA9BD]">Load Reference Archetype</span>
                <div className="quick-presets-row">
                  {Object.keys(ARCHETYPES).map((name) => (
                    <button
                      key={name}
                      type="button"
                      aria-label={`Select reference archetype: ${name}`}
                      onClick={() => handleArchetypeClick(name)}
                      className={`quick-preset-pill ${selectedArchetype === name ? 'text-[#10CBE8] border-[#10CBE8]/40 bg-[#10CBE8]/10' : ''}`}
                    >
                      {name}
                    </button>
                  ))}
                </div>
              </div>

              {/* Specification Form */}
              <form onSubmit={handleSynthesize} className="event-form">
                {/* Row 1: Type & Location */}
                <div className="form-row form-row-2">
                  <div className="form-field">
                    <label htmlFor="field-event-type" className="field-label">Event Type</label>
                    <div className="field-wrap">
                      <Sparkles className="field-icon" />
                      <input
                        id="field-event-type"
                        type="text"
                        required
                        value={formData.event_type}
                        onChange={(e) => setFormData({ ...formData, event_type: e.target.value })}
                        className="field field-padded"
                        placeholder="Wedding, Gala, Milestone…"
                      />
                    </div>
                  </div>
                  <div className="form-field">
                    <label htmlFor="field-location" className="field-label">Location &amp; Venue Space</label>
                    <div className="field-wrap">
                      <MapPin className="field-icon" />
                      <input
                        id="field-location"
                        type="text"
                        required
                        value={formData.location}
                        onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                        className="field field-padded"
                        placeholder="Venue name, city, architectural environment…"
                      />
                    </div>
                  </div>
                </div>

                {/* Row 2: Guests, Currency, Budget, Horizon */}
                <div className="form-row form-row-4">
                  <div className="form-field">
                    <label htmlFor="field-guest-count" className="field-label">Guest Count</label>
                    <div className="field-wrap">
                      <Users className="field-icon" />
                      <input
                        id="field-guest-count"
                        type="number"
                        min="1"
                        required
                        value={formData.guest_count}
                        onChange={(e) => setFormData({ ...formData, guest_count: e.target.value })}
                        className="field field-padded t-mono"
                      />
                    </div>
                  </div>

                  <div className="form-field">
                    <label htmlFor="field-total-budget" className="field-label">Total Budget ({curr})</label>
                    <div className="field-wrap">
                      <DollarSign className="field-icon" />
                      <input
                        id="field-total-budget"
                        type="number"
                        min="500"
                        step="500"
                        required
                        value={formData.total_budget}
                        onChange={(e) => setFormData({ ...formData, total_budget: e.target.value })}
                        className="field field-padded t-mono"
                      />
                    </div>
                  </div>

                  <div className="form-field">
                    <label htmlFor="field-weeks" className="field-label">Horizon (Weeks)</label>
                    <div className="field-wrap">
                      <Clock className="field-icon" />
                      <input
                        id="field-weeks"
                        type="number"
                        min="1"
                        max="104"
                        required
                        value={formData.weeks_to_event}
                        onChange={(e) => setFormData({ ...formData, weeks_to_event: e.target.value })}
                        className="field field-padded t-mono"
                      />
                    </div>
                  </div>

                  <div className="form-field">
                    <label htmlFor="field-currency" className="field-label">Currency</label>
                    <select
                      id="field-currency"
                      value={formData.currency}
                      onChange={(e) => setFormData({ ...formData, currency: e.target.value })}
                      className="field t-mono"
                    >
                      {['USD', 'EUR', 'GBP', 'INR', 'CAD', 'AUD', 'SGD', 'JPY'].map(c => (
                        <option key={c} value={c}>{c}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Row 3: Sensory Vibe & Constraints */}
                <div className="form-row form-row-2eq">
                  <div className="form-field">
                    <label htmlFor="field-sensory-theme" className="field-label">Sensory Atmosphere &amp; Theme</label>
                    <textarea
                      id="field-sensory-theme"
                      rows="3"
                      required
                      value={formData.sensory_theme}
                      onChange={(e) => setFormData({ ...formData, sensory_theme: e.target.value })}
                      className="field"
                      placeholder="Lighting Kelvin temperature, acoustics, color tones, signature moments…"
                    />
                  </div>
                  <div className="form-field">
                    <label htmlFor="field-constraints" className="field-label">Operational Constraints &amp; Directives</label>
                    <textarea
                      id="field-constraints"
                      rows="3"
                      value={formData.operational_constraints}
                      onChange={(e) => setFormData({ ...formData, operational_constraints: e.target.value })}
                      className="field"
                      placeholder="Dietary requirements (celiac, vegan), curfew, sound permit limits, special requests…"
                    />
                  </div>
                </div>

                {/* Synthesis Trigger Button */}
                <button type="submit" disabled={isLoading} className="generate-btn mt-3">
                  {isLoading ? (
                    <>
                      <div className="spinner" style={{ width: 18, height: 18 }} />
                      <span>Synthesizing Architecture Blueprint…</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5 text-white" />
                      <span>Synthesize Production Blueprint</span>
                      <ArrowRight className="w-4 h-4 ml-1" />
                    </>
                  )}
                </button>
              </form>
            </div>

            {/* Right: Real-time Budget & Allocation Breakdown */}
            <div className="ws-card budget-panel">
              <div className="ws-card-header">
                <div className="ws-card-icon bg-[#FFAD32]/10 text-[#FFAD32] border-[#FFAD32]/30">
                  <BarChart3 className="w-4 h-4" />
                </div>
                <div className="ws-card-title-block">
                  <h3 className="ws-card-title">Real-Time Capital Allocation</h3>
                  <p className="ws-card-subtitle">Live ledger balance with 10% safety reserve</p>
                </div>
              </div>

              {/* Amounts Header */}
              <div className="budget-amounts-row">
                <div className="budget-amount-block">
                  <div className="budget-amount-label t-label">Total Capital Cap</div>
                  <div className="budget-amount-total">
                    {curr} {totalBudget.toLocaleString()}
                  </div>
                </div>
                <div className="budget-divider" />
                <div className="budget-amount-block">
                  <div className="budget-amount-label t-label">Computed Spend / Guest</div>
                  <div className="budget-amount-per-guest text-[#10CBE8]">
                    {curr} {computedSpendPerGuest}
                  </div>
                </div>
              </div>

              {/* Multi-Segment Allocation Bar */}
              <div className="budget-alloc-bar">
                <div className="budget-alloc-seg bg-[#10CBE8]" style={{ width: '28.8%' }} title="Venue (28.8%)" />
                <div className="budget-alloc-seg bg-[#FFAD32]" style={{ width: '27.0%' }} title="Culinary (27%)" />
                <div className="budget-alloc-seg bg-[#915CFF]" style={{ width: '12.6%' }} title="Sensory (12.6%)" />
                <div className="budget-alloc-seg bg-[#38BDF8]" style={{ width: '10.8%' }} title="Production (10.8%)" />
                <div className="budget-alloc-seg bg-[#EC4899]" style={{ width: '10.8%' }} title="Documentation (10.8%)" />
                <div className="budget-alloc-seg bg-[#22D3A5]" style={{ width: '10.0%' }} title="Guarded Contingency (10%)" />
              </div>

              {/* Category Breakdown List */}
              <div className="budget-cat-list">
                {[
                  { name: 'Venue & Space Access', pct: '28.8%', color: 'bg-[#10CBE8]', val: Math.round(allocatedAmt * 0.32) },
                  { name: 'Catering & Beverage Program', pct: '27.0%', color: 'bg-[#FFAD32]', val: Math.round(allocatedAmt * 0.30) },
                  { name: 'Atmosphere & Sensory Lighting', pct: '12.6%', color: 'bg-[#915CFF]', val: Math.round(allocatedAmt * 0.14) },
                  { name: 'Production & Floral Art', pct: '10.8%', color: 'bg-[#38BDF8]', val: Math.round(allocatedAmt * 0.12) },
                  { name: 'Documentation & Sound', pct: '10.8%', color: 'bg-[#EC4899]', val: Math.round(allocatedAmt * 0.12) },
                  { name: 'Guarded Contingency Reserve', pct: '10.0%', color: 'bg-[#22D3A5]', val: contingencyAmt, highlight: true }
                ].map((cat, i) => (
                  <div key={i} className={`budget-cat-row ${cat.highlight ? 'text-[#22D3A5] font-semibold' : ''}`}>
                    <span className={`budget-cat-dot ${cat.color}`} />
                    <span className="budget-cat-name">{cat.name}</span>
                    <span className="budget-cat-pct">{cat.pct}</span>
                    <span className="budget-cat-amount">{curr} {cat.val.toLocaleString()}</span>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      </main>

      {/* ── 5. Loading State ─────────────────────────────────────────────────── */}
      <AnimatePresence>
        {isLoading && (
          <motion.div
            key="loading-panel"
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="loading-panel"
          >
            <div className="ws-card p-12 max-w-lg mx-auto text-center">
              <div className="spinner mx-auto mb-4" style={{ width: 36, height: 36, borderWidth: 3 }} />
              <h3 className="text-base font-bold text-white mb-1">Synthesizing Architecture Blueprint</h3>
              <p className="text-xs text-[#9AA9BD]">
                Calibrating capital allocation, sensory Kelvin lighting, and contractor delivery specifications…
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── 6. Blueprint Output Studio ───────────────────────────────────────── */}
      <AnimatePresence>
        {blueprint && (
          <motion.section
            key="blueprint-section"
            ref={blueprintRef}
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
            className="blueprint-section"
          >
            <div className="blueprint-inner">

              {/* 4 Metric Cards */}
              <div className="metrics-row">
                <div className="ws-card metric-card-bp">
                  <div className="t-label mb-1">Total Capital Cap</div>
                  <div className="t-mono text-2xl font-bold text-white">
                    {curr} <NumberTicker value={blueprint.financial_ledger.total_budget} />
                  </div>
                </div>
                <div className="ws-card metric-card-bp">
                  <div className="t-label mb-1">Program Allocated Spend</div>
                  <div className="t-mono text-2xl font-bold text-white">
                    {curr} <NumberTicker value={blueprint.financial_ledger.allocated_budget} />
                  </div>
                </div>
                <div className="ws-card metric-card-bp">
                  <div className="t-label mb-1 text-[#22D3A5]">Guarded Contingency (10%)</div>
                  <div className="t-mono text-2xl font-bold text-[#22D3A5]">
                    {curr} <NumberTicker value={blueprint.financial_ledger.contingency_reserve} />
                  </div>
                </div>
                <div className="ws-card metric-card-bp">
                  <div className="t-label mb-1 text-[#10CBE8]">Cost Per Guest</div>
                  <div className="t-mono text-2xl font-bold text-[#10CBE8]">
                    {curr} <NumberTicker value={blueprint.financial_ledger.cost_per_guest} decimalPlaces={2} />
                  </div>
                </div>
              </div>

              {/* Studio Tabs Navigation */}
              <div className="tab-bar" role="tablist" aria-label="Blueprint Architecture Views">
                {[
                  { id: 'financial', label: 'Financial Ledger', icon: DollarSign },
                  { id: 'timeline', label: 'Timeline & Milestones', icon: Calendar },
                  { id: 'sensory', label: 'Sensory Concept', icon: Lightbulb },
                  { id: 'vendors', label: 'Vendor Matrix', icon: ShieldCheck },
                  { id: 'export', label: 'Export Package', icon: Download }
                ].map(tab => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      role="tab"
                      id={`tab-${tab.id}`}
                      aria-controls={`panel-${tab.id}`}
                      aria-selected={activeTab === tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
                    >
                      <Icon className="w-3.5 h-3.5" aria-hidden="true" />
                      <span>{tab.label}</span>
                    </button>
                  );
                })}
              </div>

              {/* Tab Panel Content */}
              <div className="ws-card">
                <AnimatePresence mode="wait">

                  {/* Tab 1: Financial Ledger */}
                  {activeTab === 'financial' && (
                    <motion.div
                      key="tab-financial"
                      role="tabpanel"
                      id="panel-financial"
                      aria-labelledby="tab-financial"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                    >
                      <div className="flex flex-wrap items-start justify-between gap-4 mb-6">
                        <div>
                          <h3 className="text-xl font-bold text-white mb-1">Granular Capital Allocation</h3>
                          <p className="text-sm text-[#9AA9BD] max-w-2xl leading-relaxed">{blueprint.event_summary}</p>
                        </div>
                        <span className="badge badge-emerald">
                          <ShieldCheck className="w-3.5 h-3.5" />
                          <span>10% Reserve Guaranteed</span>
                        </span>
                      </div>

                      {/* Visual Allocation Bar */}
                      <div className="mb-6">
                        <div className="flex justify-between t-label mb-2">
                          <span>Visual Capital Distribution</span>
                          <span>{curr} {blueprint.financial_ledger.total_budget.toLocaleString()}</span>
                        </div>
                        <div className="budget-bar">
                          {blueprint.financial_ledger.items.map((it, idx) => (
                            <div
                              key={idx}
                              style={{ width: `${it.percentage_of_total}%` }}
                              title={`${it.category}: ${it.percentage_of_total}%`}
                              className={`h-full ${['bg-[#10CBE8]', 'bg-[#FFAD32]', 'bg-[#915CFF]', 'bg-[#38BDF8]', 'bg-[#EC4899]'][idx % 5]}`}
                            />
                          ))}
                          <div style={{ width: '10%' }} title="Contingency: 10%" className="h-full bg-[#22D3A5]" />
                        </div>
                      </div>

                      {/* Line Items Table */}
                      <div className="overflow-x-auto rounded-xl border border-white/[0.08]">
                        <table className="data-table">
                          <thead>
                            <tr>
                              <th>Category</th>
                              <th>Line Item Scope</th>
                              <th className="text-right">Estimated Cost</th>
                              <th className="text-right">% Cap</th>
                              <th>Negotiation &amp; Execution Notes</th>
                            </tr>
                          </thead>
                          <tbody>
                            {blueprint.financial_ledger.items.map((item, i) => (
                              <tr key={i}>
                                <td className="font-semibold text-white whitespace-nowrap">{item.category}</td>
                                <td className="text-[#CBD5E1]">{item.item_name}</td>
                                <td className="text-right t-mono font-bold text-white whitespace-nowrap">
                                  {curr} {item.estimated_cost.toLocaleString()}
                                </td>
                                <td className="text-right t-mono text-[#10CBE8]">{item.percentage_of_total}%</td>
                                <td className="text-xs text-[#9AA9BD]">{item.notes}</td>
                              </tr>
                            ))}
                            <tr style={{ background: 'rgba(34, 211, 165, 0.05)' }}>
                              <td className="text-[#22D3A5] font-bold">Guarded Contingency</td>
                              <td className="text-[#6EE7B7] text-sm">Emergency reserve locked until T-Minus 14 Days</td>
                              <td className="text-right t-mono font-bold text-[#22D3A5]">
                                {curr} {blueprint.financial_ledger.contingency_reserve.toLocaleString()}
                              </td>
                              <td className="text-right t-mono text-[#22D3A5]">10.0%</td>
                              <td className="text-xs text-[#6EE7B7]">Discretionary buffer released only on signed client order</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </motion.div>
                  )}

                  {/* Tab 2: Timeline */}
                  {activeTab === 'timeline' && (
                    <motion.div
                      key="tab-timeline"
                      role="tabpanel"
                      id="panel-timeline"
                      aria-labelledby="tab-timeline"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="space-y-4"
                    >
                      <div className="mb-4">
                        <h3 className="text-xl font-bold text-white mb-1">Phase-Gated Chronological Roadmap</h3>
                        <p className="text-sm text-[#9AA9BD]">Sequential production milestones with execution checkpoints and hard deadlines</p>
                      </div>

                      {blueprint.timeline.map((phase, idx) => (
                        <div key={idx} className="timeline-phase-card">
                          <div className="flex flex-wrap items-center justify-between gap-3 mb-4 pb-3 border-b border-white/[0.08]">
                            <div className="flex items-center gap-3">
                              <div className="phase-number">{idx + 1}</div>
                              <h4 className="font-bold text-white text-base">{phase.phase_title}</h4>
                            </div>
                            <span className="badge badge-cyan">
                              <Clock className="w-3 h-3" />
                              <span>{phase.timeframe}</span>
                            </span>
                          </div>

                          <ul className="space-y-2 mb-4">
                            {phase.action_items.map((act, j) => (
                              <li key={j} className="flex items-start gap-2.5 text-sm text-[#CBD5E1]">
                                <CheckCircle2 className="w-4 h-4 text-[#22D3A5] mt-0.5 shrink-0" />
                                <span>{act}</span>
                              </li>
                            ))}
                          </ul>

                          <div className="pt-3 border-t border-white/[0.05] flex items-center gap-2 text-xs">
                            <Zap className="w-3.5 h-3.5 text-[#FFAD32] shrink-0" />
                            <span className="text-[#9AA9BD]">
                              Critical Gate: <strong className="text-white">{phase.critical_deadline}</strong>
                            </span>
                          </div>
                        </div>
                      ))}
                    </motion.div>
                  )}

                  {/* Tab 3: Sensory Concept */}
                  {activeTab === 'sensory' && (
                    <motion.div
                      key="tab-sensory"
                      role="tabpanel"
                      id="panel-sensory"
                      aria-labelledby="tab-sensory"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                    >
                      <div className="mb-6">
                        <h3 className="text-xl font-bold text-white mb-1">Atmosphere &amp; Sensory Architecture</h3>
                        <p className="text-sm text-[#9AA9BD]">Kelvin lighting temperatures, acoustic limits, and chromatic palette</p>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                        <div className="p-5 rounded-xl border border-white/[0.08] bg-black/25">
                          <div className="flex items-center gap-2 mb-2 text-[#10CBE8]">
                            <Lightbulb className="w-4 h-4" />
                            <span className="t-label text-[#10CBE8]">Architectural Lighting Specs</span>
                          </div>
                          <p className="text-sm text-[#CBD5E1] leading-relaxed">{blueprint.sensory_concept.lighting_ambiance}</p>
                        </div>

                        <div className="p-5 rounded-xl border border-white/[0.08] bg-black/25">
                          <div className="flex items-center gap-2 mb-2 text-[#915CFF]">
                            <Music className="w-4 h-4" />
                            <span className="t-label text-[#915CFF]">Acoustic Landscape &amp; Decibel Limits</span>
                          </div>
                          <p className="text-sm text-[#CBD5E1] leading-relaxed">{blueprint.sensory_concept.acoustic_vibe}</p>
                        </div>
                      </div>

                      {/* Curated Chromatics Palette */}
                      <div className="mb-6">
                        <span className="t-label block mb-3 text-[#9AA9BD]">Curated Chromatic Palette (Click to Copy HEX)</span>
                        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
                          {blueprint.sensory_concept.decor_color_palette.map((colorStr, i) => {
                            const parts = colorStr.split(' ');
                            const hex = parts[0];
                            const name = parts.slice(1).join(' ');
                            return (
                              <div
                                key={i}
                                role="button"
                                tabIndex={0}
                                aria-label={`Copy color code ${hex} ${name} to clipboard`}
                                className="swatch relative cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#10CBE8]"
                                style={{ backgroundColor: hex, minHeight: 85 }}
                                onClick={() => copyToClipboard(hex)}
                                onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); copyToClipboard(hex); } }}
                              >
                                <div className="absolute bottom-0 left-0 right-0 p-2 bg-black/75 backdrop-blur-sm">
                                  <div className="t-mono text-white text-xs font-bold flex items-center gap-1">
                                    {copiedHex === hex ? (
                                      <>
                                        <Check className="w-3 h-3 text-[#22D3A5]" />
                                        <span className="text-[#22D3A5]">Copied</span>
                                      </>
                                    ) : (
                                      hex
                                    )}
                                  </div>
                                  <div className="text-[11px] text-white/70 truncate">{name}</div>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      </div>

                      {/* Signature Experience */}
                      <div className="p-5 rounded-xl border border-[#FFAD32]/30 bg-[#FFAD32]/05">
                        <div className="flex items-center gap-2 mb-2 text-[#FFAD32]">
                          <Sparkles className="w-4 h-4" />
                          <span className="t-label text-[#FFAD32]">Signature Culinary / Beverage Moment</span>
                        </div>
                        <p className="text-sm text-[#CBD5E1] leading-relaxed">
                          {blueprint.sensory_concept.signature_experience}
                        </p>
                      </div>
                    </motion.div>
                  )}

                  {/* Tab 4: Vendor Matrix */}
                  {activeTab === 'vendors' && (
                    <motion.div
                      key="tab-vendors"
                      role="tabpanel"
                      id="panel-vendors"
                      aria-labelledby="tab-vendors"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="space-y-4"
                    >
                      <div className="mb-4">
                        <h3 className="text-xl font-bold text-white mb-1">Vendor Execution Matrix &amp; Interview Probes</h3>
                        <p className="text-sm text-[#9AA9BD]">Deliverables, rigorous qualification questions, and insurance mandates</p>
                      </div>

                      {blueprint.vendor_matrix.map((v, i) => (
                        <div key={i} className="p-5 rounded-xl border border-white/[0.08] bg-black/25">
                          <div className="flex flex-wrap items-center justify-between gap-3 mb-4 pb-3 border-b border-white/[0.08]">
                            <h4 className="font-bold text-white text-base">{v.category}</h4>
                            <span className="badge badge-emerald">
                              <DollarSign className="w-3.5 h-3.5" />
                              <span>{curr} {v.estimated_budget.toLocaleString()}</span>
                            </span>
                          </div>

                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                            <div>
                              <span className="t-label text-[#10CBE8] block mb-2">Deliverable Scope</span>
                              <ul className="space-y-1.5">
                                {v.deliverables.map((d, j) => (
                                  <li key={j} className="flex items-start gap-2 text-sm text-[#CBD5E1]">
                                    <span className="text-[#10CBE8] shrink-0">→</span>
                                    <span>{d}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                            <div>
                              <span className="t-label text-[#915CFF] block mb-2">Hard-Hitting Interview Probes</span>
                              <ul className="space-y-2">
                                {v.interview_questions.map((q, j) => (
                                  <li key={j} className="text-sm text-[#CBD5E1] italic bg-white/[0.03] rounded-lg px-3 py-2 border-l-2 border-[#915CFF]/60">
                                    "{q}"
                                  </li>
                                ))}
                              </ul>
                            </div>
                          </div>

                          <div className="pt-3 border-t border-white/[0.05] flex items-start gap-2 text-xs">
                            <ShieldCheck className="w-4 h-4 text-[#22D3A5] shrink-0 mt-0.5" />
                            <span className="text-[#9AA9BD]">
                              <strong className="text-white">Insurance / Permit Mandate:</strong> {v.required_permits_coi}
                            </span>
                          </div>
                        </div>
                      ))}
                    </motion.div>
                  )}

                  {/* Tab 5: Export */}
                  {activeTab === 'export' && (
                    <motion.div
                      key="tab-export"
                      role="tabpanel"
                      id="panel-export"
                      aria-labelledby="tab-export"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                    >
                      <div className="mb-4">
                        <h3 className="text-xl font-bold text-white mb-1">Export Production Blueprint Package</h3>
                        <p className="text-sm text-[#9AA9BD]">Download complete specifications for venue operators, financial controllers, and vendors</p>
                      </div>

                      <div className="flex flex-wrap gap-3 mb-6">
                        <button
                          type="button"
                          aria-label="Download Production Brief in Markdown format"
                          onClick={() => downloadFile(exportMarkdown(), `blueprint_${formData.event_type.toLowerCase().replace(/\s+/g, '_')}.md`, 'text/markdown')}
                          className="btn-ghost"
                        >
                          <FileText className="w-4 h-4 text-[#10CBE8]" />
                          <span>Production Brief (.md)</span>
                          <Download className="w-3.5 h-3.5 ml-1" />
                        </button>
                        <button
                          type="button"
                          aria-label="Download Structured Schema in JSON format"
                          onClick={() => downloadFile(JSON.stringify(blueprint, null, 2), `blueprint_${formData.event_type.toLowerCase().replace(/\s+/g, '_')}.json`, 'application/json')}
                          className="btn-ghost"
                        >
                          <LayoutGrid className="w-4 h-4 text-[#915CFF]" />
                          <span>Structured Schema (.json)</span>
                          <Download className="w-3.5 h-3.5 ml-1" />
                        </button>
                      </div>

                      <div className="bg-[#04060C] border border-white/[0.08] rounded-xl p-5 t-mono text-xs text-[#9AA9BD] max-h-96 overflow-y-auto whitespace-pre-wrap leading-relaxed">
                        {exportMarkdown()}
                      </div>
                    </motion.div>
                  )}

                </AnimatePresence>
              </div>

            </div>
          </motion.section>
        )}
      </AnimatePresence>

      {/* ── 7. Clean Empty State (When no blueprint synthesized yet) ────────── */}
      {!blueprint && !isLoading && (
        <section className="empty-state-panel">
          <div className="empty-state-icon">
            <Sparkles className="w-6 h-6 text-[#10CBE8]" />
          </div>
          <h3 className="text-base font-bold text-white mb-1">Ready to Synthesize Event Architecture</h3>
          <p className="text-sm text-[#526070] max-w-sm">
            Select a curated archetype or enter your custom parameters above, then click Synthesize Production Blueprint to generate the full 5-pillar event blueprint.
          </p>
        </section>
      )}

      {/* ── Minimal Footer ─────────────────────────────────────────────────── */}
      <footer className="border-t border-white/[0.06] py-8 text-center text-xs text-[#526070]">
        <div className="max-w-[1360px] mx-auto px-6 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-bold text-white/80">PROMPTWARS</span>
            <span>—</span>
            <span>GenAI Event Architecture &amp; Production Studio</span>
          </div>
          <div className="t-mono text-[11px] text-[#526070]">
            GROQ LLAMA-3.3-70B · 10% HEDGED RESERVE · 2200K KELVIN SPECS
          </div>
        </div>
      </footer>
    </div>
  );
}
