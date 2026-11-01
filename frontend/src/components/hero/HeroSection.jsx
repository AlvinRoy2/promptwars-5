import React from 'react';
import { motion, AnimatePresence } from 'motion/react';
import {
  ArrowRight,
  CheckCircle2,
  Eye,
  MapPin,
  Music,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';

export function HeroSection({ heroRef, heroImgY, activeScene, scrollToSection }) {
  return (
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
  );
}

