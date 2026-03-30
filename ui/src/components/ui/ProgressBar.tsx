import React from "react";
import { clsx } from "clsx";

interface ProgressBarProps {
  value: number; // 0-100
  max?: number;
  label?: string;
  showValue?: boolean;
  size?: "xs" | "sm" | "md";
  color?: "brand" | "success" | "warn" | "danger";
  animated?: boolean;
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  max = 100,
  label,
  showValue = false,
  size = "sm",
  color = "brand",
  animated = true,
  className,
}) => {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));

  const trackSizes = { xs: "h-1", sm: "h-2", md: "h-3" };
  const fillColors = {
    brand: "bg-brand-500",
    success: "bg-success-500",
    warn: "bg-warn-500",
    danger: "bg-danger-500",
  };

  return (
    <div className={clsx("w-full", className)}>
      {(label || showValue) && (
        <div className="flex justify-between items-center mb-1.5">
          {label && <span className="text-xs text-slate-400">{label}</span>}
          {showValue && (
            <span className="text-xs font-mono font-medium text-slate-300 ml-auto">
              {Math.round(pct)}%
            </span>
          )}
        </div>
      )}
      <div
        className={clsx(
          "w-full rounded-full bg-surface-3 overflow-hidden",
          trackSizes[size]
        )}
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
      >
        <div
          className={clsx(
            "h-full rounded-full transition-all duration-500 ease-out",
            fillColors[color],
            animated && "relative overflow-hidden after:absolute after:inset-0 after:bg-gradient-to-r after:from-transparent after:via-white/10 after:to-transparent after:animate-pulse2"
          )}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
};
