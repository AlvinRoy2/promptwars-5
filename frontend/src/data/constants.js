import {
  Activity,
  BarChart3,
  CheckCircle2,
  MapPin,
  Music,
  ShieldCheck,
  TrendingUp,
  Zap,
} from 'lucide-react';

import imgBirthday from '../assets/hero-birthday.jpg';
import imgCommunity from '../assets/hero-community.jpg';
import imgMoodboard from '../assets/hero-moodboard.jpg';
import imgSpatialAi from '../assets/hero-spatial-ai.jpg';
import imgWedding from '../assets/hero-wedding.jpg';

// ─── Curated Architectural Concepts & Scenes ──────────────────────────────────
export const SCENES = [
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
    location: 'Civic Greenhouse & Glass Pavilion — Public Waterfront Park',
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
export const MARQUEE_ITEMS = [
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
export const ARCHETYPES = {
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
