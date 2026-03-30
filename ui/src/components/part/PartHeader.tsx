import React from "react";
import { Link } from "react-router-dom";
import { ChevronLeft, ChevronRight, Clock, Folder } from "lucide-react";
import { Badge } from "../ui/Badge";
import { allParts } from "../../data/parts";
import type { PartData } from "../../types";
import { clsx } from "clsx";

const PHASE_COLORS: Record<number, string> = {
  1: "bg-agent-500/10 text-agent-300 border border-agent-500/20",
  2: "bg-success-500/10 text-success-300 border border-success-500/20",
  3: "bg-warn-500/10 text-warn-300 border border-warn-500/20",
  4: "bg-danger-500/10 text-danger-300 border border-danger-500/20",
  5: "bg-brand-500/10 text-brand-300 border border-brand-500/20",
};

interface PartHeaderProps {
  part: PartData;
}

export const PartHeader: React.FC<PartHeaderProps> = ({ part }) => {
  const currentIdx = allParts.findIndex((p) => p.id === part.id);
  const prevPart = currentIdx > 0 ? allParts[currentIdx - 1] : null;
  const nextPart = currentIdx < allParts.length - 1 ? allParts[currentIdx + 1] : null;

  return (
    <header className="mb-8">
      {/* Breadcrumb + prev/next */}
      <div className="flex items-center justify-between mb-4">
        <nav className="flex items-center gap-2 text-sm text-slate-500">
          <Link to="/" className="hover:text-slate-300 transition-colors">Overview</Link>
          <span>/</span>
          <span className="text-slate-300">Part {part.id}</span>
        </nav>
        <div className="flex items-center gap-2">
          {prevPart && (
            <Link
              to={`/part/${prevPart.id}`}
              className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-surface-2 hover:bg-surface-3 border border-surface-3 text-slate-400 hover:text-white text-xs transition-colors"
            >
              <ChevronLeft size={14} />
              <span className="font-mono">{prevPart.id}</span>
            </Link>
          )}
          {nextPart && (
            <Link
              to={`/part/${nextPart.id}`}
              className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-surface-2 hover:bg-surface-3 border border-surface-3 text-slate-400 hover:text-white text-xs transition-colors"
            >
              <span className="font-mono">{nextPart.id}</span>
              <ChevronRight size={14} />
            </Link>
          )}
        </div>
      </div>

      {/* Main header */}
      <div className="flex flex-col gap-3">
        {/* Phase + difficulty badges */}
        <div className="flex flex-wrap items-center gap-2">
          <span
            className={clsx(
              "text-xs font-semibold px-2.5 py-1 rounded-full",
              PHASE_COLORS[part.phase]
            )}
          >
            Phase {part.phase} · {part.phaseLabel}
          </span>
          <Badge variant="difficulty" difficulty={part.difficulty}>
            {part.difficulty}
          </Badge>
          <span className="flex items-center gap-1 text-xs text-slate-500">
            <Clock size={12} />
            ~{part.estimatedHours} hours
          </span>
          <span className="flex items-center gap-1 text-xs text-slate-500">
            <Folder size={12} />
            <code className="font-mono">{part.folder}/</code>
          </span>
        </div>

        {/* Title */}
        <div className="flex items-start gap-4">
          <span className="text-5xl font-black text-slate-700 font-mono select-none leading-none">
            {part.id}
          </span>
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-white leading-tight">
              {part.title}
            </h1>
            <p className="text-slate-400 mt-2 max-w-2xl leading-relaxed">{part.goal}</p>
          </div>
        </div>
      </div>
    </header>
  );
};
