import React from "react";

export function Marquee({
  className = "",
  reverse = false,
  pauseOnHover = true,
  children,
  repeat = 2,
  ...props
}) {
  return (
    <div
      {...props}
      className={`marquee-container items-center ${pauseOnHover ? 'marquee-pause' : ''} ${className}`}
    >
      {Array(repeat)
        .fill(0)
        .map((_, i) => (
          <div
            key={i}
            aria-hidden={i > 0}
            className={`marquee-content ${reverse ? 'marquee-reverse' : ''}`}
          >
            {children}
          </div>
        ))}
    </div>
  );
}
