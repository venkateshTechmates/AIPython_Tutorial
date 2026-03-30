import React from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Zap } from "lucide-react";
import { useAppStore } from "../../store/appStore";
import { ProgressBar } from "../ui/ProgressBar";

export const HeroBanner: React.FC = () => {
  const getOverallProgress = useAppStore((s) => s.getOverallProgress);
  const completedParts = useAppStore((s) => s.completedParts);

  const progress = getOverallProgress();

  // SVG ring parameters
  const radius = 36;
  const circ = 2 * Math.PI * radius;
  const offset = circ - (progress / 100) * circ;

  return (
    <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-brand-900/40 via-surface-2 to-surface-2 border border-brand-700/30 p-8">
      {/* Background glow */}
      <div className="absolute -top-20 -right-20 w-80 h-80 bg-brand-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-20 -left-20 w-60 h-60 bg-agent-600/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative flex flex-col md:flex-row items-start md:items-center gap-8">
        {/* Left content */}
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-3">
            <Zap size={16} className="text-brand-400" />
            <span className="text-xs font-semibold uppercase tracking-widest text-brand-400">
              Hospital AI Platform
            </span>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-3 leading-tight">
            Build a production-grade{" "}
            <span className="text-brand-400">AI platform</span>
            <br />with LangGraph & FastAPI
          </h1>
          <p className="text-slate-400 max-w-xl mb-6 leading-relaxed">
            A 14-part hands-on series covering FastAPI foundations, RAG, multi-agent
            orchestration, tool calling, streaming, observability, and production deployment —
            all within a real hospital management domain.
          </p>

          <div className="flex flex-wrap gap-3">
            <Link
              to={completedParts.length > 0 ? `/part/${completedParts.length < 14 ? String(completedParts.length + 1).padStart(2, "0") : "14"}` : "/part/01"}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-medium rounded-xl transition-colors shadow-lg shadow-brand-900/30"
            >
              {completedParts.length > 0 ? "Continue Learning" : "Start Learning"}
              <ArrowRight size={16} />
            </Link>
            <Link
              to="/setup"
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-surface-3 hover:bg-slate-700 text-slate-200 font-medium rounded-xl transition-colors border border-surface-3"
            >
              Setup Guide
            </Link>
          </div>
        </div>

        {/* Progress ring */}
        <div className="flex flex-col items-center gap-3">
          <div className="relative w-28 h-28">
            <svg className="w-full h-full -rotate-90" viewBox="0 0 88 88">
              <circle cx="44" cy="44" r={radius} fill="none" stroke="#1e293b" strokeWidth="8" />
              <circle
                cx="44"
                cy="44"
                r={radius}
                fill="none"
                stroke="#6366f1"
                strokeWidth="8"
                strokeDasharray={circ}
                strokeDashoffset={offset}
                strokeLinecap="round"
                className="transition-all duration-700"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-2xl font-bold text-white">{Math.round(progress)}%</span>
              <span className="text-[10px] text-slate-400 uppercase tracking-wide">complete</span>
            </div>
          </div>
          <div className="text-center">
            <div className="text-sm font-semibold text-slate-200">
              {completedParts.length} / 14 parts
            </div>
            <div className="text-xs text-slate-500">
              {completedParts.length === 0
                ? "Not started"
                : completedParts.length === 14
                ? "All done! 🎉"
                : "In progress"}
            </div>
          </div>
        </div>
      </div>

      {/* Phase progress strip */}
      <div className="relative mt-8 grid grid-cols-5 gap-2">
        {[
          { n: 1, label: "Foundations", color: "#38bdf8", parts: ["01","02","03"] },
          { n: 2, label: "AI Core", color: "#4ade80", parts: ["04","05"] },
          { n: 3, label: "Agents", color: "#fb923c", parts: ["06","07","08"] },
          { n: 4, label: "Production", color: "#f87171", parts: ["09","10","11","12","13"] },
          { n: 5, label: "Capstone", color: "#a78bfa", parts: ["14"] },
        ].map((phase) => {
          const done = phase.parts.filter((id) => completedParts.includes(id)).length;
          const pct = (done / phase.parts.length) * 100;
          return (
            <div key={phase.n} className="flex flex-col gap-1">
              <div className="flex justify-between items-center">
                <span className="text-[11px] text-slate-400 font-medium">P{phase.n}</span>
                <span className="text-[11px] text-slate-500">{done}/{phase.parts.length}</span>
              </div>
              <div className="h-1.5 rounded-full bg-surface-3 overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-700"
                  style={{ width: `${pct}%`, backgroundColor: phase.color }}
                />
              </div>
              <span className="text-[10px] text-slate-500 truncate">{phase.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
