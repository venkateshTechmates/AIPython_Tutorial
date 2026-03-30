import { useAppStore } from "../store/appStore";
import { allParts } from "../data/parts";

export function useProgress() {
  const store = useAppStore();

  const getPartStatus = (partId: string) => {
    if (store.completedParts.includes(partId)) return "complete";
    if (store.inProgressPart === partId) return "in-progress";
    const part = allParts.find((p) => p.id === partId);
    if (!part) return "locked";
    if (store.isPartUnlocked(partId)) return "not-started";
    return "locked";
  };

  const nextIncompletePart = () => {
    for (const part of allParts) {
      if (!store.completedParts.includes(part.id)) return part;
    }
    return null;
  };

  const getTotalCriteria = () =>
    allParts.reduce((acc, p) => acc + p.acceptanceCriteria.length, 0);

  const getCompletedCriteriaCount = () =>
    Object.values(store.completedCriteria).reduce(
      (acc, arr) => acc + arr.length,
      0
    );

  const getSkillScore = (skill: SkillKey) => {
    const contributing = SKILL_MAP[skill];
    const done = contributing.filter((p) =>
      store.completedParts.includes(p)
    ).length;
    return Math.round((done / contributing.length) * 100);
  };

  return {
    ...store,
    getPartStatus,
    nextIncompletePart,
    getTotalCriteria,
    getCompletedCriteriaCount,
    getSkillScore,
  };
}

type SkillKey =
  | "FastAPI"
  | "LangChain"
  | "LangGraph"
  | "RAG"
  | "Pydantic"
  | "SQLite"
  | "Testing"
  | "Deployment";

export const SKILL_MAP: Record<SkillKey, string[]> = {
  FastAPI: ["01", "03", "09", "13"],
  LangChain: ["01", "04", "07"],
  LangGraph: ["05", "06", "08", "09"],
  RAG: ["04", "08"],
  Pydantic: ["01", "02"],
  SQLite: ["03", "05", "08"],
  Testing: ["11"],
  Deployment: ["13"],
};
