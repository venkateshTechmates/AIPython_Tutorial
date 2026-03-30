import React from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Lock } from "lucide-react";
import { useAppStore } from "../../store/appStore";
import { partsById, allParts } from "../../data/parts";
import type { PartData } from "../../types";
import { clsx } from "clsx";

interface NextPartCTAProps {
  part: PartData;
}

export const NextPartCTA: React.FC<NextPartCTAProps> = ({ part }) => {
  const nextId = part.unlocks[0];
  const nextPart = nextId ? partsById[nextId] : null;
  const completedParts = useAppStore((s) => s.completedParts);
  const isPartUnlocked = useAppStore((s) => s.isPartUnlocked);

  if (!nextPart) {
    // This is Part 14 — show completion card
    return (
      <div className="rounded-2xl border border-brand-500/30 bg-gradient-to-br from-brand-900/20 to-surface-2 p-8 text-center">
        <div className="text-4xl mb-3">🎉</div>
        <h3 className="text-xl font-bold text-white mb-2">Congratulations!</h3>
        <p className="text-slate-400 max-w-md mx-auto">
          You've completed all parts of the Hospital AI Platform series. You've built a
          production-ready LangGraph AI system from scratch!
        </p>
        <Link
          to="/progress"
          className="inline-flex items-center gap-2 mt-6 px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-semibold rounded-xl transition-colors"
        >
          View Your Progress
          <ArrowRight size={16} />
        </Link>
      </div>
    );
  }

  const unlocked = isPartUnlocked(nextPart.id);

  return (
    <div className="rounded-2xl border border-surface-3 bg-surface-2 p-6 flex flex-col sm:flex-row items-start sm:items-center gap-4">
      <div className="flex-1">
        <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">Next Up</div>
        <h3 className="text-lg font-bold text-white">
          Part {nextPart.id}: {nextPart.title}
        </h3>
        <p className="text-sm text-slate-400 mt-1 max-w-lg">{nextPart.goal}</p>
        {!unlocked && (
          <div className="flex items-center gap-1.5 mt-2 text-xs text-warn-400">
            <Lock size={12} />
            Complete this part to unlock
          </div>
        )}
      </div>
      <Link
        to={`/part/${nextPart.id}`}
        onClick={(e) => !unlocked && e.preventDefault()}
        className={clsx(
          "flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-sm transition-colors flex-shrink-0",
          unlocked
            ? "bg-brand-600 hover:bg-brand-500 text-white shadow shadow-brand-900/30"
            : "bg-surface-3 text-slate-500 cursor-not-allowed"
        )}
      >
        {unlocked ? "Start Part" : "Locked"}
        <ArrowRight size={16} />
      </Link>
    </div>
  );
};
