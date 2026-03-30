import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { CheckCircle2, Circle, Lock, Loader2, ChevronRight } from "lucide-react";
import { useAppStore } from "../../store/appStore";
import { allParts } from "../../data/parts";
import { PHASES } from "../../types";
import { clsx } from "clsx";

const PHASE_COLORS: Record<number, string> = {
  1: "text-agent-400",
  2: "text-success-400",
  3: "text-warn-400",
  4: "text-danger-400",
  5: "text-brand-400",
};

export const Sidebar: React.FC = () => {
  const sidebarCollapsed = useAppStore((s) => s.sidebarCollapsed);
  const completedParts = useAppStore((s) => s.completedParts);
  const inProgressPart = useAppStore((s) => s.inProgressPart);
  const isPartUnlocked = useAppStore((s) => s.isPartUnlocked);
  const navigate = useNavigate();

  const getPartStatus = (id: string) => {
    if (completedParts.includes(id)) return "complete";
    if (inProgressPart === id) return "in-progress";
    if (!isPartUnlocked(id)) return "locked";
    return "not-started";
  };

  if (sidebarCollapsed) {
    return (
      <nav className="flex-1 overflow-y-auto py-4 scrollbar-thin">
        <div className="flex flex-col items-center gap-1 px-2">
          {allParts.map((part) => {
            const status = getPartStatus(part.id);
            return (
              <NavLink
                key={part.id}
                to={`/part/${part.id}`}
                title={`Part ${part.id}: ${part.title}`}
                className={({ isActive }) =>
                  clsx(
                    "w-9 h-9 rounded-lg flex items-center justify-center text-xs font-mono font-bold transition-colors",
                    isActive
                      ? "bg-brand-600 text-white"
                      : status === "locked"
                      ? "bg-surface-2 text-slate-600 cursor-not-allowed pointer-events-none"
                      : "bg-surface-2 hover:bg-surface-3 text-slate-400 hover:text-white"
                  )
                }
              >
                {part.id}
              </NavLink>
            );
          })}
        </div>
      </nav>
    );
  }

  return (
    <nav className="flex-1 overflow-y-auto py-3 scrollbar-thin px-2">
      {PHASES.map((phase) => {
        const phaseParts = allParts.filter((p) => p.phase === phase.number);
        return (
          <div key={phase.number} className="mb-4">
            <div className="flex items-center gap-2 px-3 py-1.5 mb-1">
              <span
                className={clsx(
                  "text-[10px] font-bold uppercase tracking-widest",
                  PHASE_COLORS[phase.number]
                )}
              >
                Phase {phase.number}
              </span>
              <span className="text-[10px] text-slate-500 truncate">{phase.label}</span>
            </div>
            <div className="flex flex-col gap-0.5">
              {phaseParts.map((part) => {
                const status = getPartStatus(part.id);
                const locked = status === "locked";
                return (
                  <NavLink
                    key={part.id}
                    to={`/part/${part.id}`}
                    className={({ isActive }) =>
                      clsx(
                        "flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors group",
                        isActive
                          ? "bg-brand-600/20 text-brand-200"
                          : locked
                          ? "text-slate-600 cursor-not-allowed pointer-events-none"
                          : "text-slate-400 hover:bg-surface-3 hover:text-slate-200"
                      )
                    }
                    onClick={(e) => {
                      if (locked) e.preventDefault();
                    }}
                  >
                    {/* Status icon */}
                    <span className="flex-shrink-0 w-4 h-4 flex items-center justify-center">
                      {status === "complete" ? (
                        <CheckCircle2 size={14} className="text-success-400" />
                      ) : status === "in-progress" ? (
                        <Loader2 size={14} className="text-brand-400 animate-spin" />
                      ) : locked ? (
                        <Lock size={12} className="text-slate-600" />
                      ) : (
                        <Circle size={12} className="text-slate-600 group-hover:text-slate-400" />
                      )}
                    </span>
                    {/* Part number */}
                    <span className="font-mono text-[11px] font-bold text-slate-500 flex-shrink-0">
                      {part.id}
                    </span>
                    {/* Title */}
                    <span className="truncate text-[13px] leading-snug">{part.title}</span>
                    {/* Active chevron */}
                    <ChevronRight
                      size={12}
                      className="ml-auto flex-shrink-0 text-brand-400 opacity-0 group-[.active]:opacity-100"
                    />
                  </NavLink>
                );
              })}
            </div>
          </div>
        );
      })}
    </nav>
  );
};
