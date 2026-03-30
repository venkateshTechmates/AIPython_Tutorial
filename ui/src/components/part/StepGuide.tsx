import React from "react";
import { ListChecks, CheckCircle2, Circle } from "lucide-react";
import { useAppStore } from "../../store/appStore";
import { CodeBlock } from "../ui/CodeBlock";
import type { Step } from "../../types";
import { clsx } from "clsx";

interface StepGuideProps {
  steps: Step[];
  partId: string;
}

export const StepGuide: React.FC<StepGuideProps> = ({ steps, partId }) => {
  const completedSteps = useAppStore((s) => s.completedSteps);
  const toggleStep = useAppStore((s) => s.toggleStep);
  const partSteps = completedSteps[partId] ?? [];

  const doneCount = steps.filter((s) => partSteps.includes(s.number)).length;

  return (
    <section className="mb-8">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <ListChecks size={18} className="text-brand-400" />
          <h2 className="text-lg font-bold text-slate-100">Step-by-Step Guide</h2>
        </div>
        <span className="text-xs text-slate-500">
          {doneCount}/{steps.length} steps
        </span>
      </div>

      {/* Progress strip */}
      <div className="flex gap-1 mb-6">
        {steps.map((step) => (
          <div
            key={step.number}
            className={clsx(
              "flex-1 h-1 rounded-full transition-colors duration-300",
              partSteps.includes(step.number) ? "bg-success-500" : "bg-surface-3"
            )}
          />
        ))}
      </div>

      <div className="flex flex-col gap-4">
        {steps.map((step) => {
          const done = partSteps.includes(step.number);
          return (
            <div
              key={step.number}
              className={clsx(
                "flex gap-4 p-4 rounded-xl border bg-surface-2 transition-colors",
                done ? "border-success-500/30" : "border-surface-3"
              )}
            >
              {/* Step number + checkbox */}
              <div className="flex flex-col items-center gap-2 flex-shrink-0">
                <button
                  onClick={() => toggleStep(partId, step.number)}
                  className={clsx(
                    "w-8 h-8 rounded-full border-2 flex items-center justify-center transition-all",
                    done
                      ? "bg-success-500/20 border-success-500 text-success-400"
                      : "border-surface-3 text-slate-600 hover:border-slate-500"
                  )}
                  title={done ? "Mark as incomplete" : "Mark as done"}
                >
                  {done ? <CheckCircle2 size={16} /> : <span className="text-xs font-bold">{step.number}</span>}
                </button>
                {step.number < steps.length && (
                  <div className="w-0.5 flex-1 min-h-[16px] bg-surface-3 rounded-full" />
                )}
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <h3
                  className={clsx(
                    "font-semibold text-sm mb-1 transition-colors",
                    done ? "text-slate-500 line-through" : "text-slate-200"
                  )}
                >
                  {step.title}
                </h3>
                <p className="text-xs text-slate-400 leading-relaxed mb-3">{step.description}</p>
                {step.code && (
                  <CodeBlock
                    code={step.code.snippet}
                    language={step.code.language}
                    filename={step.code.filename}
                    maxHeight="16rem"
                  />
                )}
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};
