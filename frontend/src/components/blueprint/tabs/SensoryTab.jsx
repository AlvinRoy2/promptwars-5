import React from 'react';
import { motion } from 'motion/react';
import { Check, Lightbulb, Music, Sparkles } from 'lucide-react';

export function SensoryTab({ blueprint, copyToClipboard, copiedHex }) {
  return (
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
  );
}

