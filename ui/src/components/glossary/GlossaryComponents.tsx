import React, { useState, useMemo } from "react";
import { Search } from "lucide-react";
import { glossaryTerms as allTerms } from "../../data/glossary";
import { clsx } from "clsx";

export const GlossarySearch: React.FC<{
  search: string;
  onSearch: (q: string) => void;
}> = ({ search, onSearch }) => (
  <div className="relative">
    <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none" />
    <input
      type="search"
      value={search}
      onChange={(e) => onSearch(e.target.value)}
      placeholder="Search terms, definitions…"
      className="w-full h-11 pl-10 pr-4 bg-surface-2 border border-surface-3 rounded-xl text-sm text-slate-300 placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
    />
  </div>
);

const CATEGORY_STYLES: Record<string, string> = {
  "Core Concepts": "bg-brand-500/10 text-brand-300 border-brand-500/20",
  LangGraph: "bg-purple-500/10 text-purple-300 border-purple-500/20",
  LangChain: "bg-blue-500/10 text-blue-300 border-blue-500/20",
  Pydantic: "bg-agent-500/10 text-agent-300 border-agent-500/20",
  Database: "bg-success-500/10 text-success-300 border-success-500/20",
  RAG: "bg-warn-500/10 text-warn-300 border-warn-500/20",
  "Vector DB": "bg-orange-500/10 text-orange-300 border-orange-500/20",
  Framework: "bg-teal-500/10 text-teal-300 border-teal-500/20",
  Streaming: "bg-cyan-500/10 text-cyan-300 border-cyan-500/20",
  Deployment: "bg-slate-500/10 text-slate-300 border-slate-500/20",
  Tooling: "bg-lime-500/10 text-lime-300 border-lime-500/20",
  LLM: "bg-pink-500/10 text-pink-300 border-pink-500/20",
  Workflow: "bg-indigo-500/10 text-indigo-300 border-indigo-500/20",
  Observability: "bg-rose-500/10 text-rose-300 border-rose-500/20",
};

export const TermCard: React.FC<{ term: (typeof allTerms)[number] }> = ({ term }) => (
  <div className="rounded-xl border border-surface-3 bg-surface-2 p-4 hover:border-brand-500/30 transition-colors">
    <div className="flex items-start justify-between gap-3 mb-2">
      <h3 className="font-bold text-slate-100 text-sm">{term.term}</h3>
      <span
        className={clsx(
          "text-[10px] font-medium px-2 py-0.5 rounded-full border flex-shrink-0",
          CATEGORY_STYLES[term.category] ?? "bg-surface-3 text-slate-400 border-surface-3"
        )}
      >
        {term.category}
      </span>
    </div>
    <p className="text-xs text-slate-400 leading-relaxed mb-3">{term.definition}</p>
    {term.usedInParts.length > 0 && (
      <div className="flex flex-wrap gap-1">
        <span className="text-[10px] text-slate-600">Parts:</span>
        {term.usedInParts.map((id) => (
          <span key={id} className="font-mono text-[10px] text-brand-400 bg-brand-500/10 px-1.5 py-0.5 rounded border border-brand-500/20">
            {id}
          </span>
        ))}
      </div>
    )}
  </div>
);

export const AlphaIndex: React.FC<{
  activeLetter: string;
  onLetter: (l: string) => void;
  available: Set<string>;
}> = ({ activeLetter, onLetter, available }) => {
  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
  return (
    <div className="flex flex-wrap gap-1">
      <button
        onClick={() => onLetter("")}
        className={clsx(
          "px-2 py-1 rounded text-xs font-medium transition-colors",
          activeLetter === "" ? "bg-brand-600 text-white" : "bg-surface-2 text-slate-400 hover:text-slate-200"
        )}
      >
        All
      </button>
      {letters.map((l) => (
        <button
          key={l}
          onClick={() => onLetter(l)}
          disabled={!available.has(l)}
          className={clsx(
            "w-7 h-7 flex items-center justify-center rounded text-xs font-mono font-bold transition-colors",
            activeLetter === l
              ? "bg-brand-600 text-white"
              : available.has(l)
              ? "bg-surface-2 text-slate-400 hover:text-slate-200"
              : "text-slate-700 cursor-not-allowed"
          )}
        >
          {l}
        </button>
      ))}
    </div>
  );
};
