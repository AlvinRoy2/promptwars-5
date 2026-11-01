import React from 'react';
import { Check, ChevronRight } from 'lucide-react';
import { SCENES } from '../../data/constants';

export function ConceptsRail({ conceptsRef, activeSceneIndex, handleSceneSelect }) {
  return (
    <section ref={conceptsRef} className="concepts-section">
      <div className="concepts-inner">
        <div className="concepts-header">
          <div>
            <span className="t-label text-[#10CBE8]">Curated Architectural Concepts</span>
            <p className="concepts-subtitle">Select any reference scenario to update the visual ambience and parameters</p>
          </div>
          <button
            onClick={() => handleSceneSelect((activeSceneIndex + 1) % SCENES.length)}
            className="concepts-arrow-btn"
            aria-label="Next concept"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        <div className="concepts-scroll">
          {SCENES.map((scene, idx) => {
            const isSelected = activeSceneIndex === idx;
            return (
              <div
                key={scene.id}
                role="button"
                tabIndex={0}
                aria-label={`Select concept: ${scene.title}`}
                aria-pressed={isSelected}
                onClick={() => handleSceneSelect(idx)}
                onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && handleSceneSelect(idx)}
                className={`concept-tile ${isSelected ? 'active' : ''}`}
              >
                <div className="concept-tile-img-wrap">
                  <img src={scene.image} alt={scene.title} className="concept-tile-img" />
                  {isSelected && (
                    <div className="concept-tile-active-badge bg-[#FFAD32] text-black">
                      <Check className="w-3 h-3 stroke-[3]" />
                    </div>
                  )}
                </div>
                <div className="concept-tile-body">
                  <div className="concept-tile-title truncate">{scene.title}</div>
                  <div className="concept-tile-sub truncate">{scene.tag}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

