import React from "react";
import { Link } from "react-router-dom";
import { useAppStore } from "../../store/appStore";
import { allParts } from "../../data/parts";
import { useProgress } from "../../hooks/useProgress";
import { clsx } from "clsx";

export const PartGrid: React.FC = () => {
  const { getPartStatus } = useProgress();

  return (
    <div>
      <h2 className="text-lg font-bold text-slate-100 mb-4">All Parts</h2>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-7 gap-3">
        {allParts.map((part) => {
          const status = getPartStatus(part.id);
          return (
            <Link
              key={part.id}
              to={`/part/${part.id}`}
              className={clsx(
                "flex flex-col items-center gap-2 p-3 rounded-xl border text-center transition-all group",
                status === "complete"
                  ? "bg-success-900/15 border-success-500/30 hover:border-success-500/60"
                  : status === "in-progress"
                  ? "bg-brand-900/15 border-brand-500/30 hover:border-brand-500/60"
                  : status === "locked"
                  ? "bg-surface-2 border-surface-3 opacity-50 pointer-events-none"
                  : "bg-surface-2 border-surface-3 hover:border-brand-500/30"
              )}
            >
              <span
                className={clsx(
                  "text-lg",
                  status === "complete"
                    ? "text-success-400"
                    : status === "in-progress"
                    ? "text-brand-400"
                    : status === "locked"
                    ? "text-slate-700"
                    : "text-slate-400 group-hover:text-slate-200"
                )}
              >
                {status === "complete" ? "✓" : status === "locked" ? "🔒" : "○"}
              </span>
              <span className="font-mono text-xs font-bold text-slate-500">{part.id}</span>
              <span className="text-[11px] text-slate-400 leading-snug line-clamp-2 group-hover:text-slate-200 transition-colors">
                {part.title}
              </span>
            </Link>
          );
        })}
      </div>
    </div>
  );
};
