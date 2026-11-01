import React from 'react';
import { BarChart3 } from 'lucide-react';

export function BudgetAllocationPanel({
  totalBudget,
  computedSpendPerGuest,
  allocatedAmt,
  contingencyAmt,
  curr,
}) {
  return (
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
  );
}

