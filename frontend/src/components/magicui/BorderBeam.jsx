import React from "react";

export function BorderBeam({
  className = "",
  size = 200,
  duration = 8,
  borderWidth = 1.5,
  colorFrom = "#38BDF8",
  colorTo = "#D4AF37",
  delay = 0
}) {
  return (
    <div
      style={{
        "--size": size,
        "--duration": duration,
        "--border-width": borderWidth,
        "--color-from": colorFrom,
        "--color-to": colorTo,
        "--delay": `-${delay}s`
      }}
      className={`border-beam ${className}`}
    />
  );
}
