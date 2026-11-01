import React from 'react';
import { motion } from 'motion/react';
import { CheckCircle2, Clock, Zap } from 'lucide-react';

export function TimelineTab({ blueprint }) {
  return (
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
  );
}
