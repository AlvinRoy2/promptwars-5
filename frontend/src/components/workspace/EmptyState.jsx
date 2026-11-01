import React from 'react';
import { Sparkles } from 'lucide-react';

export function EmptyState() {
  return (
    <section className="empty-state-panel">
      <div className="empty-state-icon">
        <Sparkles className="w-6 h-6 text-[#10CBE8]" />
      </div>
      <h3 className="text-base font-bold text-white mb-1">Ready to Synthesize Event Architecture</h3>
      <p className="text-sm text-[#526070] max-w-sm">
        Select a curated archetype or enter your custom parameters above, then click Synthesize Production Blueprint to generate the full 5-pillar event blueprint.
      </p>
    </section>
  );
}
