import React from 'react';
import { motion } from 'motion/react';
import { DollarSign, ShieldCheck } from 'lucide-react';

export function VendorTab({ blueprint, curr }) {
  return (
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
  );
}

