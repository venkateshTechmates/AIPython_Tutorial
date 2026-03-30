import React from "react";
import { Link } from "react-router-dom";
import { CheckCircle2, ArrowRight } from "lucide-react";
import { useAppStore } from "../../store/appStore";
import { allParts } from "../../data/parts";
import { clsx } from "clsx";

interface PhaseInfo {
  number: number;
  label: string;
  description: string;
  color: string;
  borderColor: string;
  parts: string[];
}

const PHASES: PhaseInfo[] = [
  {
    number: 1,
    label: "Foundations",
    description: "FastAPI, Pydantic v2, SQLite persistence, REST API design",
    color: "text-agent-300",
    borderColor: "border-agent-500/30",
    parts: ["01", "02", "03"],
  },
  {
    number: 2,
    label: "AI Core",
    description: "RAG with Qdrant, first LangGraph stateful agent, triage workflows",
    color: "text-success-300",
    borderColor: "border-success-500/30",
    parts: ["04", "05"],
  },
  {
    number: 3,
    label: "Agent Systems",
    description: "Multi-agent supervision, 13 hospital tools, 3-tier memory",
    color: "text-warn-300",
    borderColor: "border-warn-500/30",
    parts: ["06", "07", "08"],
  },
  {
    number: 4,
    label: "Production",
    description: "HITL, SSE streaming, pytest suite, LangSmith tracing, Docker",
    color: "text-danger-300",
    borderColor: "border-danger-500/30",
    parts: ["09", "10", "11", "12", "13"],
  },
  {
    number: 5,
    label: "Capstone",
    description: "Full hospital AI platform integrating all previous parts",
    color: "text-brand-300",
    borderColor: "border-brand-500/30",
    parts: ["14"],
  },
];

export const PhaseCard: React.FC<{ phase: PhaseInfo }> = ({ phase }) => {
  const completedParts = useAppStore((s) => s.completedParts);
  const done = phase.parts.filter((id) => completedParts.includes(id)).length;
  const allDone = done === phase.parts.length;
  const started = done > 0;

  const phaseParts = allParts.filter((p) => phase.parts.includes(p.id));

  return (
    <div
      className={clsx(
        "rounded-xl border bg-surface-2 p-5 flex flex-col gap-4 hover:bg-surface-3 transition-colors",
        allDone ? "border-success-500/30" : phase.borderColor
      )}
    >
      <div className="flex items-start justify-between gap-2">
        <div>
          <div className={clsx("text-xs font-bold uppercase tracking-widest mb-1", phase.color)}>
            Phase {phase.number}
          </div>
          <h3 className="text-base font-semibold text-slate-100">{phase.label}</h3>
          <p className="text-xs text-slate-400 mt-1 leading-relaxed">{phase.description}</p>
        </div>
        {allDone && <CheckCircle2 size={20} className="text-success-400 flex-shrink-0 mt-0.5" />}
      </div>

      {/* Progress bar */}
      <div>
        <div className="flex justify-between text-xs text-slate-500 mb-1.5">
          <span>{done} / {phase.parts.length} parts</span>
          <span>{Math.round((done / phase.parts.length) * 100)}%</span>
        </div>
        <div className="h-1.5 rounded-full bg-surface-1">
          <div
            className={clsx(
              "h-full rounded-full transition-all duration-700",
              allDone ? "bg-success-400" : started ? "bg-brand-500" : "bg-surface-3"
            )}
            style={{ width: `${(done / phase.parts.length) * 100}%` }}
          />
        </div>
      </div>

      {/* Part list */}
      <div className="flex flex-col gap-1">
        {phaseParts.map((part) => {
          const isDone = completedParts.includes(part.id);
          return (
            <Link
              key={part.id}
              to={`/part/${part.id}`}
              className="flex items-center gap-2 px-2 py-1.5 rounded-lg hover:bg-surface-1 group transition-colors"
            >
              {isDone ? (
                <CheckCircle2 size={12} className="text-success-400 flex-shrink-0" />
              ) : (
                <span className="w-3 h-3 rounded-full border border-slate-600 flex-shrink-0" />
              )}
              <span className="font-mono text-[11px] text-slate-500">{part.id}</span>
              <span className="text-xs text-slate-400 group-hover:text-slate-200 transition-colors truncate">
                {part.title}
              </span>
              <ArrowRight size={10} className="ml-auto text-slate-600 group-hover:text-brand-400 transition-colors flex-shrink-0" />
            </Link>
          );
        })}
      </div>
    </div>
  );
};

export const PhaseCardsGrid: React.FC = () => (
  <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
    {PHASES.map((phase) => (
      <PhaseCard key={phase.number} phase={phase} />
    ))}
  </div>
);
