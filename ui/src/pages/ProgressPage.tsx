import React from "react";
import { useAppStore } from "../store/appStore";
import { PartGrid } from "../components/progress/PartGrid";
import { SkillsRadar } from "../components/progress/SkillsRadar";
import { CriteriaTracker } from "../components/progress/CriteriaTracker";
import { ProgressBar } from "../components/ui/ProgressBar";
import { RotateCcw } from "lucide-react";

export const ProgressPage: React.FC = () => {
  const completedParts = useAppStore((s) => s.completedParts);
  const getOverallProgress = useAppStore((s) => s.getOverallProgress);
  const resetAll = useAppStore((s) => s.resetAll);

  const progress = getOverallProgress();

  return (
    <div className="flex flex-col gap-10 max-w-5xl">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">Your Progress</h1>
          <p className="text-sm text-slate-400">
            {completedParts.length} of 14 parts completed · {Math.round(progress)}% overall
          </p>
        </div>
        <button
          onClick={() => {
            if (window.confirm("Reset all progress? This cannot be undone.")) {
              resetAll();
            }
          }}
          className="flex items-center gap-1.5 px-3 py-2 text-xs text-slate-500 hover:text-danger-400 bg-surface-2 border border-surface-3 rounded-lg transition-colors"
        >
          <RotateCcw size={12} />
          Reset
        </button>
      </div>

      {/* Overall progress bar */}
      <div className="p-5 rounded-xl bg-surface-2 border border-surface-3">
        <div className="flex justify-between text-sm mb-3">
          <span className="font-semibold text-slate-200">Overall Completion</span>
          <span className="font-bold text-brand-400">{Math.round(progress)}%</span>
        </div>
        <ProgressBar
          value={progress}
          size="md"
          color={progress === 100 ? "success" : "brand"}
          showValue={false}
        />
        <div className="flex justify-between text-xs text-slate-600 mt-2">
          <span>0%</span>
          <span>{completedParts.length} / 14 parts</span>
          <span>100%</span>
        </div>
      </div>

      <PartGrid />
      <SkillsRadar />
      <CriteriaTracker />
    </div>
  );
};
