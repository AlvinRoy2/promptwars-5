import React from 'react';
import { Marquee } from '../magicui/Marquee';
import { MARQUEE_ITEMS } from '../../data/constants';

export function TelemetryMarquee() {
  return (
    <section className="marquee-strip">
      <Marquee pauseOnHover repeat={3} className="h-full">
        {MARQUEE_ITEMS.map((item, i) => {
          const Icon = item.icon;
          return (
            <span key={i} className="marquee-pill">
              <Icon className="w-3 h-3 text-[#10CBE8]" />
              {item.label}
            </span>
          );
        })}
      </Marquee>
    </section>
  );
}

