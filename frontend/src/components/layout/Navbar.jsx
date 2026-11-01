import React from 'react';
import { Sliders, Sparkles } from 'lucide-react';

export function Navbar({ scrollToSection, backendOnline, blueprint, activeTab, setActiveTab }) {
  return (
    <header className="site-nav">
      <div className="site-nav-inner">
        <div className="nav-brand">
          <Sparkles className="w-4 h-4 text-[#10CBE8]" />
          <span>PROMPTWARS</span>
          <span className="t-label text-[10px] text-[#526070] font-normal tracking-wider ml-1">/ STUDIO</span>
        </div>

        <nav className="nav-links">
          <button onClick={() => scrollToSection('concepts')} className="nav-link">Concepts</button>
          <button onClick={() => scrollToSection('workspace')} className="nav-link">Studio</button>
          {blueprint && (
            <>
              <button
                onClick={() => { scrollToSection('blueprint'); setActiveTab('financial'); }}
                className={`nav-link ${activeTab === 'financial' ? 'active' : ''}`}
              >
                Ledger
              </button>
              <button
                onClick={() => { scrollToSection('blueprint'); setActiveTab('timeline'); }}
                className={`nav-link ${activeTab === 'timeline' ? 'active' : ''}`}
              >
                Timeline
              </button>
              <button
                onClick={() => { scrollToSection('blueprint'); setActiveTab('sensory'); }}
                className={`nav-link ${activeTab === 'sensory' ? 'active' : ''}`}
              >
                Sensory
              </button>
              <button
                onClick={() => { scrollToSection('blueprint'); setActiveTab('vendors'); }}
                className={`nav-link ${activeTab === 'vendors' ? 'active' : ''}`}
              >
                Vendors
              </button>
            </>
          )}
        </nav>

        <div className="nav-actions">
          <div className="api-badge">
            <span className={`status-dot ${backendOnline ? 'online' : 'offline'}`} />
            <span className="t-mono text-[10px] text-[#9AA9BD] font-medium">
              {backendOnline ? 'GROQ ENGINE ACTIVE' : 'LOCAL ENGINE'}
            </span>
          </div>
          <button onClick={() => scrollToSection('workspace')} className="btn-configure">
            <Sliders className="w-3.5 h-3.5 text-[#10CBE8]" />
            <span>Configure</span>
          </button>
        </div>
      </div>
    </header>
  );
}
