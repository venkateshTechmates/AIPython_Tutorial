import React, { useRef } from "react";
import { Link } from "react-router-dom";
import { CheckCircle2, Lock, ArrowRight, ChevronLeft, ChevronRight } from "lucide-react";
import { useAppStore } from "../../store/appStore";
import { allParts } from "../../data/parts";
import { Badge } from "../ui/Badge";
import { clsx } from "clsx";

export const PartCardsStrip: React.FC = () => {
  const scrollRef = useRef<HTMLDivElement>(null);
  const completedParts = useAppStore((s) => s.completedParts);
  const inProgressPart = useAppStore((s) => s.inProgressPart);
  const isPartUnlocked = useAppStore((s) => s.isPartUnlocked);

  const scroll = (dir: "left" | "right") => {
    const el = scrollRef.current;
    if (!el) return;
    el.scrollBy({ left: dir === "left" ? -320 : 320, behavior: "smooth" });
  };

  return (
    <div className="relative">
      {/* Scroll buttons */}
      <button
        onClick={() => scroll("left")}
        className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-3 z-10 w-8 h-8 rounded-full bg-surface-2 border border-surface-3 flex items-center justify-center hover:bg-surface-3 transition-colors shadow-lg"
        aria-label="Scroll left"
      >
        <ChevronLeft size={16} className="text-slate-400" />
      </button>
      <button
        onClick={() => scroll("right")}
        className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-3 z-10 w-8 h-8 rounded-full bg-surface-2 border border-surface-3 flex items-center justify-center hover:bg-surface-3 transition-colors shadow-lg"
        aria-label="Scroll right"
      >
        <ChevronRight size={16} className="text-slate-400" />
      </button>

      {/* Cards strip */}
      <div
        ref={scrollRef}
        className="flex gap-4 overflow-x-auto scrollbar-none pb-2 px-2 -mx-2"
        style={{ scrollSnapType: "x mandatory" }}
      >
        {allParts.map((part) => {
          const done = completedParts.includes(part.id);
          const active = inProgressPart === part.id;
          const locked = !isPartUnlocked(part.id);

          return (
            <Link
              key={part.id}
              to={`/part/${part.id}`}
              style={{ scrollSnapAlign: "start", minWidth: "220px" }}
              className={clsx(
                "flex flex-col gap-3 p-4 rounded-xl border bg-surface-2 hover:bg-surface-3 transition-all group flex-shrink-0",
                done
                  ? "border-success-500/30"
                  : active
                  ? "border-brand-500/40 bg-brand-900/20"
                  : locked
                  ? "border-surface-3 opacity-50 pointer-events-none"
                  : "border-surface-3 hover:border-brand-500/20"
              )}
              onClick={(e) => locked && e.preventDefault()}
            >
              {/* Header row */}
              <div className="flex items-start justify-between gap-2">
                <span className="font-mono text-sm font-bold text-slate-500">
                  {part.id}
                </span>
                {done ? (
                  <CheckCircle2 size={14} className="text-success-400 flex-shrink-0" />
                ) : locked ? (
                  <Lock size={12} className="text-slate-600 flex-shrink-0" />
                ) : (
                  <ArrowRight size={12} className="text-slate-600 group-hover:text-brand-400 transition-colors flex-shrink-0" />
                )}
              </div>

              {/* Title */}
              <h4 className="text-sm font-semibold text-slate-200 leading-snug line-clamp-2">
                {part.title}
              </h4>

              {/* Meta */}
              <div className="flex flex-wrap gap-1 mt-auto">
                <Badge variant="difficulty" difficulty={part.difficulty} size="xs">
                  {part.difficulty}
                </Badge>
                <span className="text-[10px] text-slate-500 flex items-center">
                  ~{part.estimatedHours}h
                </span>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
};
