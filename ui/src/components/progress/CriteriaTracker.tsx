import React from "react";
import { useAppStore } from "../../store/appStore";
import { allParts } from "../../data/parts";
import { clsx } from "clsx";

export const CriteriaTracker: React.FC = () => {
  const completedCriteria = useAppStore((s) => s.completedCriteria);
  const completedParts = useAppStore((s) => s.completedParts);

  // Only show parts that have at least some criteria started
  const activeParts = allParts.filter((part) => {
    const done = completedCriteria[part.id] ?? [];
    return done.length > 0 || completedParts.includes(part.id);
  });

  if (activeParts.length === 0) {
    return (
      <div className="p-6 rounded-xl bg-surface-2 border border-surface-3 text-center text-sm text-slate-500">
        Complete acceptance criteria in part detail pages to track here
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-lg font-bold text-slate-100 mb-4">Criteria Tracker</h2>
      <div className="flex flex-col gap-3">
        {activeParts.map((part) => {
          const done = (completedCriteria[part.id] ?? []).length;
          const total = part.acceptanceCriteria.length;
          const pct = total > 0 ? (done / total) * 100 : 0;
          return (
            <div key={part.id} className="flex items-center gap-4 p-3 rounded-xl bg-surface-2 border border-surface-3">
              <span className="font-mono text-sm text-slate-500 w-8 flex-shrink-0">{part.id}</span>
              <span className="text-sm text-slate-300 flex-1 truncate">{part.title}</span>
              <div className="w-32 flex-shrink-0">
                <div className="h-1.5 rounded-full bg-surface-3">
                  <div
                    className={clsx(
                      "h-full rounded-full transition-all",
                      pct === 100 ? "bg-success-400" : "bg-brand-500"
                    )}
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>
              <span className="text-xs text-slate-500 w-12 text-right flex-shrink-0">
                {done}/{total}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
