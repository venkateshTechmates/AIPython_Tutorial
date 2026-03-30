import React from "react";
import { ShieldCheck, CheckSquare, Square } from "lucide-react";
import { useAppStore } from "../../store/appStore";
import { clsx } from "clsx";
import type { AcceptanceCriterion } from "../../types";

interface AcceptanceCriteriaProps {
  criteria: AcceptanceCriterion[];
  partId: string;
}

export const AcceptanceCriteria: React.FC<AcceptanceCriteriaProps> = ({ criteria, partId }) => {
  const completedCriteria = useAppStore((s) => s.completedCriteria);
  const toggleCriteria = useAppStore((s) => s.toggleCriteria);
  const markPartComplete = useAppStore((s) => s.markPartComplete);
  const completedParts = useAppStore((s) => s.completedParts);

  const partCriteria = completedCriteria[partId] ?? [];
  const doneCount = criteria.filter((c) => partCriteria.includes(c.id)).length;
  const allDone = doneCount === criteria.length;
  const alreadyComplete = completedParts.includes(partId);

  return (
    <section className="mb-8">
      <div className="flex items-center gap-2 mb-4">
        <ShieldCheck size={18} className="text-brand-400" />
        <h2 className="text-lg font-bold text-slate-100">Acceptance Criteria</h2>
        <span className="text-xs text-slate-500">
          {doneCount}/{criteria.length}
        </span>
        {allDone && (
          <span className="text-xs text-success-400 font-semibold ml-1">✓ All passing</span>
        )}
      </div>

      <div className="rounded-xl border border-surface-3 bg-surface-2 overflow-hidden">
        {criteria.map((criterion, i) => {
          const done = partCriteria.includes(criterion.id);
          return (
            <button
              key={criterion.id}
              onClick={() => toggleCriteria(partId, criterion.id)}
              className={clsx(
                "w-full flex items-start gap-3 px-4 py-3 text-left transition-colors hover:bg-surface-3",
                i < criteria.length - 1 && "border-b border-surface-3",
                done && "bg-success-900/10"
              )}
            >
              {done ? (
                <CheckSquare size={16} className="text-success-400 flex-shrink-0 mt-0.5" />
              ) : (
                <Square size={16} className="text-slate-600 flex-shrink-0 mt-0.5" />
              )}
              <span
                className={clsx(
                  "text-sm transition-colors",
                  done ? "text-slate-500 line-through" : "text-slate-300"
                )}
              >
                {criterion.text}
              </span>
            </button>
          );
        })}
      </div>

      {/* Complete button */}
      {!alreadyComplete && (
        <div className="mt-4 flex justify-end">
          <button
            onClick={() => {
              if (allDone || window.confirm(`Mark Part ${partId} as complete? (${doneCount}/${criteria.length} criteria checked)`)) {
                markPartComplete(partId);
              }
            }}
            className={clsx(
              "px-5 py-2.5 rounded-xl text-sm font-semibold transition-all",
              allDone
                ? "bg-success-600 hover:bg-success-500 text-white shadow shadow-success-900/30"
                : "bg-surface-3 text-slate-400 border border-surface-3 hover:border-slate-500"
            )}
          >
            {allDone ? "✓ Mark Part Complete" : `Complete (${doneCount}/${criteria.length} done)`}
          </button>
        </div>
      )}
      {alreadyComplete && (
        <div className="mt-4 flex items-center gap-2 justify-end">
          <span className="text-success-400 text-sm font-semibold">Part Complete ✓</span>
        </div>
      )}
    </section>
  );
};
