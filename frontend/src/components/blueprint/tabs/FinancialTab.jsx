import React from 'react';
import { motion } from 'motion/react';
import { ShieldCheck } from 'lucide-react';

export function FinancialTab({ blueprint, curr }) {
  return (
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
  );
}

