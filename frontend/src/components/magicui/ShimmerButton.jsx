import React from "react";

export function ShimmerButton({
  children,
  className = "",
  shimmerColor = "#ffffff",
  shimmerSize = "0.05em",
  shimmerDuration = "3s",
  borderRadius = "12px",
  background = "linear-gradient(135deg, #0284C7 0%, #0369A1 100%)",
  onClick,
  disabled = false,
  ...props
}) {
  return (
    <button
      style={{
        "--shimmer-color": shimmerColor,
        "--shimmer-size": shimmerSize,
        "--border-radius": borderRadius,
        "--speed": shimmerDuration,
        "--bg": background
      }}
      className={`shimmer-btn ${className}`}
      onClick={onClick}
      disabled={disabled}
      {...props}
    >
      <div className="shimmer-spin" />
      <div className="shimmer-content">
        {children}
      </div>
    </button>
  );
}
