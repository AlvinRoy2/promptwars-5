import React from 'react';
import { motion, AnimatePresence } from 'motion/react';
import {
  Calendar,
  DollarSign,
  Download,
  Lightbulb,
  ShieldCheck,
} from 'lucide-react';
import { NumberTicker } from '../magicui/NumberTicker';
import { FinancialTab } from './tabs/FinancialTab';
import { TimelineTab } from './tabs/TimelineTab';
import { SensoryTab } from './tabs/SensoryTab';
import { VendorTab } from './tabs/VendorTab';
import { ExportTab } from './tabs/ExportTab';

export function BlueprintStudio({
  blueprintRef,
  blueprint,
  curr,
  activeTab,
  setActiveTab,
  copyToClipboard,
  copiedHex,
  formData,
  exportMarkdown,
  downloadFile,
}) {
  const tabs = [
    { id: 'financial', label: 'Financial Ledger', icon: DollarSign },
    { id: 'timeline', label: 'Timeline & Milestones', icon: Calendar },
    { id: 'sensory', label: 'Sensory Concept', icon: Lightbulb },
    { id: 'vendors', label: 'Vendor Matrix', icon: ShieldCheck },
    { id: 'export', label: 'Export Package', icon: Download },
  ];

  return (
    <motion.section
      key="blueprint-section"
      ref={blueprintRef}
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      className="blueprint-section"
    >
      <div className="blueprint-inner">
        {/* 4 Metric Cards */}
        <div className="metrics-row">
          <div className="ws-card metric-card-bp">
            <div className="t-label mb-1">Total Capital Cap</div>
            <div className="t-mono text-2xl font-bold text-white">
              {curr} <NumberTicker value={blueprint.financial_ledger.total_budget} />
            </div>
          </div>
          <div className="ws-card metric-card-bp">
            <div className="t-label mb-1">Program Allocated Spend</div>
            <div className="t-mono text-2xl font-bold text-white">
              {curr} <NumberTicker value={blueprint.financial_ledger.allocated_budget} />
            </div>
          </div>
          <div className="ws-card metric-card-bp">
            <div className="t-label mb-1 text-[#22D3A5]">Guarded Contingency (10%)</div>
            <div className="t-mono text-2xl font-bold text-[#22D3A5]">
              {curr} <NumberTicker value={blueprint.financial_ledger.contingency_reserve} />
            </div>
          </div>
          <div className="ws-card metric-card-bp">
            <div className="t-label mb-1 text-[#10CBE8]">Cost Per Guest</div>
            <div className="t-mono text-2xl font-bold text-[#10CBE8]">
              {curr} <NumberTicker value={blueprint.financial_ledger.cost_per_guest} decimalPlaces={2} />
            </div>
          </div>
        </div>

        {/* Studio Tabs Navigation */}
        <div className="tab-bar" role="tablist" aria-label="Blueprint Architecture Views">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                role="tab"
                id={`tab-${tab.id}`}
                aria-controls={`panel-${tab.id}`}
                aria-selected={activeTab === tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
              >
                <Icon className="w-3.5 h-3.5" aria-hidden="true" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Tab Panel Content */}
        <div className="ws-card">
          <AnimatePresence mode="wait">
            {activeTab === 'financial' && (
              <FinancialTab blueprint={blueprint} curr={curr} />
            )}
            {activeTab === 'timeline' && (
              <TimelineTab blueprint={blueprint} />
            )}
            {activeTab === 'sensory' && (
              <SensoryTab
                blueprint={blueprint}
                copyToClipboard={copyToClipboard}
                copiedHex={copiedHex}
              />
            )}
            {activeTab === 'vendors' && (
              <VendorTab blueprint={blueprint} curr={curr} />
            )}
            {activeTab === 'export' && (
              <ExportTab
                blueprint={blueprint}
                formData={formData}
                exportMarkdown={exportMarkdown}
                downloadFile={downloadFile}
              />
            )}
          </AnimatePresence>
        </div>
      </div>
    </motion.section>
  );
}

