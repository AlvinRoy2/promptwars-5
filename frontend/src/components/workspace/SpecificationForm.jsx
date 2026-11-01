import React from 'react';
import {
  ArrowRight,
  Clock,
  DollarSign,
  MapPin,
  Sliders,
  Sparkles,
  Users,
} from 'lucide-react';
import { ARCHETYPES } from '../../data/constants';

export function SpecificationForm({
  formData,
  setFormData,
  handleSynthesize,
  selectedArchetype,
  handleArchetypeClick,
  isLoading,
  curr,
}) {
  return (
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
  );
}
