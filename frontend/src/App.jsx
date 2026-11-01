import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence, useScroll, useTransform } from 'motion/react';

import { ScrollProgress } from './components/magicui/ScrollProgress';
import { Navbar } from './components/layout/Navbar';
import { Footer } from './components/layout/Footer';
import { HeroSection } from './components/hero/HeroSection';
import { TelemetryMarquee } from './components/hero/TelemetryMarquee';
import { ConceptsRail } from './components/hero/ConceptsRail';
import { SpecificationForm } from './components/workspace/SpecificationForm';
import { BudgetAllocationPanel } from './components/workspace/BudgetAllocationPanel';
import { EmptyState } from './components/workspace/EmptyState';
import { BlueprintStudio } from './components/blueprint/BlueprintStudio';

import { SCENES, ARCHETYPES } from './data/constants';
import { generateFallbackBlueprint } from './utils/fallbackGenerator';

export default function App() {
  const [formData, setFormData] = useState(ARCHETYPES['Napa Valley Botanical Wedding']);
  const [selectedArchetype, setSelectedArchetype] = useState('Napa Valley Botanical Wedding');
  const [activeSceneIndex, setActiveSceneIndex] = useState(0);
  const activeScene = SCENES[activeSceneIndex];
  const [blueprint, setBlueprint] = useState(null);
  const [activeTab, setActiveTab] = useState('financial');
  const [isLoading, setIsLoading] = useState(false);
  const [backendOnline, setBackendOnline] = useState(false);
  const [backendUrl] = useState(import.meta.env.VITE_API_URL || '');
  const [copiedHex, setCopiedHex] = useState(null);

  const heroRef = useRef(null);
  const workspaceRef = useRef(null);
  const conceptsRef = useRef(null);
  const blueprintRef = useRef(null);

  const { scrollYProgress } = useScroll({
    target: heroRef,
    offset: ['start start', 'end start']
  });
  const heroImgY = useTransform(scrollYProgress, [0, 1], ['0%', '18%']);

  // Check backend health via canonical /api/health (Vercel rewrite -> backend service)
  useEffect(() => {
    fetch(`${backendUrl}/api/health`)
      .then(r => r.json())
      .then(d => { if (d.status === 'healthy') setBackendOnline(true); })
      .catch(() => setBackendOnline(false));
  }, [backendUrl]);

  // Derived financial computations
  const totalBudget = Number(formData.total_budget || 0);
  const guestCount = Math.max(Number(formData.guest_count || 1), 1);
  const computedSpendPerGuest = (totalBudget / guestCount).toFixed(2);
  const contingencyAmt = Math.round(totalBudget * 0.10);
  const allocatedAmt = Math.round(totalBudget - contingencyAmt);
  const curr = formData.currency || 'USD';

  const scrollToSection = (sec) => {
    if (sec === 'workspace') workspaceRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    else if (sec === 'concepts') conceptsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    else if (sec === 'blueprint') blueprintRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const handleArchetypeClick = (name) => {
    if (ARCHETYPES[name]) {
      setFormData(ARCHETYPES[name]);
      setSelectedArchetype(name);
      const matchIdx = SCENES.findIndex(s => s.archetypeKey === name);
      if (matchIdx !== -1) {
        setActiveSceneIndex(matchIdx);
      }
    }
  };

  const handleSceneSelect = (idx) => {
    setActiveSceneIndex(idx);
    const scene = SCENES[idx];
    if (scene.archetypeKey && ARCHETYPES[scene.archetypeKey]) {
      setFormData(ARCHETYPES[scene.archetypeKey]);
      setSelectedArchetype(scene.archetypeKey);
    }
  };

  const handleSynthesize = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setBlueprint(null);

    if (backendOnline) {
      try {
        const res = await fetch(`${backendUrl}/api/blueprint`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });
        if (res.ok) {
          const data = await res.json();
          setBlueprint(data);
          setIsLoading(false);
          setTimeout(() => blueprintRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 200);
          return;
        }
      } catch (err) {
        console.warn('Backend unavailable, falling back to curated engine', err);
      }
    }

    // Graceful offline fallback
    setTimeout(() => {
      setBlueprint(generateFallbackBlueprint(formData));
      setIsLoading(false);
      setTimeout(() => blueprintRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 200);
    }, 750);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).catch(() => {});
    setCopiedHex(text);
    setTimeout(() => setCopiedHex(null), 1800);
  };

  const downloadFile = (content, filename, type) => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const exportMarkdown = () => {
    if (!blueprint) return '';
    let md = `# EVENT PRODUCTION BLUEPRINT\n**Event:** ${formData.event_type} (${formData.guest_count} guests)\n**Location:** ${formData.location}\n**Budget:** ${curr} ${Number(formData.total_budget).toLocaleString()}\n\n`;
    md += `## SUMMARY\n${blueprint.event_summary}\n\n`;
    md += `## SENSORY ARCHITECTURE\n- **Lighting:** ${blueprint.sensory_concept.lighting_ambiance}\n- **Acoustics:** ${blueprint.sensory_concept.acoustic_vibe}\n- **Signature Moment:** ${blueprint.sensory_concept.signature_experience}\n\n`;
    md += `## FINANCIAL CAPITAL ALLOCATION\nTotal Budget: ${curr} ${blueprint.financial_ledger.total_budget.toLocaleString()}\nAllocated: ${curr} ${blueprint.financial_ledger.allocated_budget.toLocaleString()}\nGuarded Contingency Reserve: ${curr} ${blueprint.financial_ledger.contingency_reserve.toLocaleString()}\n\n`;
    blueprint.financial_ledger.items.forEach(it => {
      md += `- **${it.category}** | ${it.item_name}: ${curr} ${it.estimated_cost.toLocaleString()} (${it.percentage_of_total}%) — ${it.notes}\n`;
    });
    return md;
  };

  return (
    <div className="relative min-h-screen bg-[#070A10] text-[#F6F4EF] selection:bg-[#10CBE8]/30">
      <ScrollProgress />

      <Navbar
        scrollToSection={scrollToSection}
        backendOnline={backendOnline}
        blueprint={blueprint}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      <HeroSection
        heroRef={heroRef}
        heroImgY={heroImgY}
        activeScene={activeScene}
        scrollToSection={scrollToSection}
      />

      <TelemetryMarquee />

      <ConceptsRail
        conceptsRef={conceptsRef}
        activeSceneIndex={activeSceneIndex}
        handleSceneSelect={handleSceneSelect}
      />

      <main ref={workspaceRef} className="workspace-main">
        <div className="workspace-inner">
          <div className="workspace-grid">
            <SpecificationForm
              formData={formData}
              setFormData={setFormData}
              handleSynthesize={handleSynthesize}
              selectedArchetype={selectedArchetype}
              handleArchetypeClick={handleArchetypeClick}
              isLoading={isLoading}
              curr={curr}
            />

            <BudgetAllocationPanel
              totalBudget={totalBudget}
              computedSpendPerGuest={computedSpendPerGuest}
              allocatedAmt={allocatedAmt}
              contingencyAmt={contingencyAmt}
              curr={curr}
            />
          </div>
        </div>
      </main>

      {/* Loading State */}
      <AnimatePresence>
        {isLoading && (
          <motion.div
            key="loading-panel"
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="loading-panel"
          >
            <div className="ws-card p-12 max-w-lg mx-auto text-center">
              <div className="spinner mx-auto mb-4" style={{ width: 36, height: 36, borderWidth: 3 }} />
              <h3 className="text-base font-bold text-white mb-1">Synthesizing Architecture Blueprint</h3>
              <p className="text-xs text-[#9AA9BD]">
                Calibrating capital allocation, sensory Kelvin lighting, and contractor delivery specifications…
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Blueprint Output Studio */}
      <AnimatePresence>
        {blueprint && (
          <BlueprintStudio
            blueprintRef={blueprintRef}
            blueprint={blueprint}
            curr={curr}
            activeTab={activeTab}
            setActiveTab={setActiveTab}
            copyToClipboard={copyToClipboard}
            copiedHex={copiedHex}
            formData={formData}
            exportMarkdown={exportMarkdown}
            downloadFile={downloadFile}
          />
        )}
      </AnimatePresence>

      {/* Clean Empty State */}
      {!blueprint && !isLoading && <EmptyState />}

      <Footer />
    </div>
  );
}
