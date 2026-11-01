import React from 'react';

export function Footer() {
  return (
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
  );
}
