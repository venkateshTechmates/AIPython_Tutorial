import React from "react";
import { clsx } from "clsx";
import type { HttpMethod, Difficulty } from "../../types";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "method" | "difficulty" | "phase" | "status" | "category" | "default";
  method?: HttpMethod;
  difficulty?: Difficulty;
  size?: "xs" | "sm" | "md";
  className?: string;
}

const METHOD_STYLES: Record<HttpMethod, string> = {
  GET: "bg-agent-500/15 text-agent-300 border border-agent-500/30",
  POST: "bg-success-500/15 text-success-300 border border-success-500/30",
  PUT: "bg-warn-500/15 text-warn-300 border border-warn-500/30",
  DELETE: "bg-danger-500/15 text-danger-300 border border-danger-500/30",
  PATCH: "bg-purple-500/15 text-purple-300 border border-purple-500/30",
};

const DIFFICULTY_STYLES: Record<Difficulty, string> = {
  beginner: "bg-success-500/15 text-success-300 border border-success-500/30",
  intermediate: "bg-warn-500/15 text-warn-300 border border-warn-500/30",
  advanced: "bg-danger-500/15 text-danger-300 border border-danger-500/30",
};

const STATUS_STYLES = {
  complete: "bg-success-500/15 text-success-300 border border-success-500/30",
  "in-progress": "bg-brand-500/15 text-brand-300 border border-brand-500/30",
  "not-started": "bg-surface-3 text-slate-400 border border-surface-3",
  locked: "bg-surface-2 text-slate-500 border border-surface-2",
};

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = "default",
  method,
  difficulty,
  size = "sm",
  className,
}) => {
  const base = "inline-flex items-center font-medium rounded-full tracking-wide";

  const sizes = {
    xs: "text-[10px] px-1.5 py-0.5",
    sm: "text-xs px-2 py-0.5",
    md: "text-sm px-3 py-1",
  };

  let colorClass = "bg-surface-3 text-slate-300 border border-surface-3";

  if (variant === "method" && method) {
    colorClass = METHOD_STYLES[method];
  } else if (variant === "difficulty" && difficulty) {
    colorClass = DIFFICULTY_STYLES[difficulty];
  } else if (variant === "status") {
    const text = String(children).toLowerCase().replace(" ", "-") as keyof typeof STATUS_STYLES;
    colorClass = STATUS_STYLES[text] ?? colorClass;
  } else if (variant === "phase") {
    colorClass = "bg-brand-600/20 text-brand-300 border border-brand-600/30";
  } else if (variant === "category") {
    colorClass = "bg-slate-700/50 text-slate-300 border border-slate-600/30";
  }

  return (
    <span className={clsx(base, sizes[size], colorClass, className)}>
      {children}
    </span>
  );
};

/** Convenience component for HTTP method badges */
export const MethodBadge: React.FC<{ method: HttpMethod; size?: BadgeProps["size"] }> = ({
  method,
  size = "sm",
}) => (
  <Badge variant="method" method={method} size={size} className="font-mono font-bold uppercase">
    {method}
  </Badge>
);
