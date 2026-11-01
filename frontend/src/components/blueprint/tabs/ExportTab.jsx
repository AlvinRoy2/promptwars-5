import React from 'react';
import { motion } from 'motion/react';
import { Download, FileText, LayoutGrid } from 'lucide-react';

export function ExportTab({
  blueprint,
  formData,
  exportMarkdown,
  downloadFile,
}) {
  return (
    <motion.div
      key="tab-export"
      role="tabpanel"
      id="panel-export"
      aria-labelledby="tab-export"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="mb-4">
        <h3 className="text-xl font-bold text-white mb-1">Export Production Blueprint Package</h3>
        <p className="text-sm text-[#9AA9BD]">Download complete specifications for venue operators, financial controllers, and vendors</p>
      </div>

      <div className="flex flex-wrap gap-3 mb-6">
        <button
          type="button"
          aria-label="Download Production Brief in Markdown format"
          onClick={() => downloadFile(exportMarkdown(), `blueprint_${formData.event_type.toLowerCase().replace(/\s+/g, '_')}.md`, 'text/markdown')}
          className="btn-ghost"
        >
          <FileText className="w-4 h-4 text-[#10CBE8]" />
          <span>Production Brief (.md)</span>
          <Download className="w-3.5 h-3.5 ml-1" />
        </button>
        <button
          type="button"
          aria-label="Download Structured Schema in JSON format"
          onClick={() => downloadFile(JSON.stringify(blueprint, null, 2), `blueprint_${formData.event_type.toLowerCase().replace(/\s+/g, '_')}.json`, 'application/json')}
          className="btn-ghost"
        >
          <LayoutGrid className="w-4 h-4 text-[#915CFF]" />
          <span>Structured Schema (.json)</span>
          <Download className="w-3.5 h-3.5 ml-1" />
        </button>
      </div>

      <div className="bg-[#04060C] border border-white/[0.08] rounded-xl p-5 t-mono text-xs text-[#9AA9BD] max-h-96 overflow-y-auto whitespace-pre-wrap leading-relaxed">
        {exportMarkdown()}
      </div>
    </motion.div>
  );
}

