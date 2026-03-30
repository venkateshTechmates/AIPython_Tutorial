import React from "react";
import { useProgress, SKILL_MAP } from "../../hooks/useProgress";
import type { } from "../../hooks/useProgress";
import { ProgressBar } from "../ui/ProgressBar";

type SkillKey = keyof typeof SKILL_MAP;

export const SkillsRadar: React.FC = () => {
  const { getSkillScore } = useProgress();
  const skills = Object.keys(SKILL_MAP) as SkillKey[];

  return (
    <div>
      <h2 className="text-lg font-bold text-slate-100 mb-4">Skill Progression</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {skills.map((skill) => {
          const score = getSkillScore(skill);
          const partIds = SKILL_MAP[skill];
          return (
            <div key={skill} className="p-4 rounded-xl bg-surface-2 border border-surface-3">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-semibold text-slate-200">{skill}</span>
                <span className="text-sm font-bold text-brand-400">{Math.round(score)}%</span>
              </div>
              <ProgressBar
                value={score}
                color={score === 100 ? "success" : score > 50 ? "brand" : "warn"}
                size="sm"
              />
              <div className="flex gap-1 mt-2 flex-wrap">
                {partIds.map((id: string) => (
                  <span key={id} className="font-mono text-[10px] text-slate-600 bg-surface-1 px-1.5 py-0.5 rounded">
                    {id}
                  </span>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
