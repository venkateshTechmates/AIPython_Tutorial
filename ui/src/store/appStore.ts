import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import type { RequestHistoryItem } from "../types";
import { partsById } from "../data/parts";

export type ColorTheme = "indigo" | "violet" | "teal" | "rose" | "amber" | "sky";

interface AppStore {
  // ── Theme ─────────────────────────────────────────────────────────────────
  theme: "dark" | "light";
  setTheme: (t: "dark" | "light") => void;
  toggleTheme: () => void;
  colorTheme: ColorTheme;
  setColorTheme: (t: ColorTheme) => void;

  // ── Setup checklist ───────────────────────────────────────────────────────
  setupChecklist: Record<string, boolean>;
  toggleSetupItem: (id: string) => void;

  // ── Progress ──────────────────────────────────────────────────────────────
  completedParts: string[];
  inProgressPart: string | null;
  completedCriteria: Record<string, string[]>;
  completedSteps: Record<string, number[]>;
  completionDates: Record<string, string>;

  markPartComplete: (partId: string) => void;
  unmarkPartComplete: (partId: string) => void;
  setInProgress: (partId: string | null) => void;
  toggleCriteria: (partId: string, criteriaId: string) => void;
  toggleStep: (partId: string, stepNumber: number) => void;
  isPartUnlocked: (partId: string) => boolean;
  getOverallProgress: () => number;

  // ── Playground history ────────────────────────────────────────────────────
  requestHistory: RequestHistoryItem[];
  addToHistory: (item: RequestHistoryItem) => void;
  clearHistory: () => void;

  // ── Sidebar ───────────────────────────────────────────────────────────────
  sidebarCollapsed: boolean;
  toggleSidebar: () => void;

  // ── Reset ─────────────────────────────────────────────────────────────────
  resetAll: () => void;
}

const initialState = {
  theme: "dark" as const,
  colorTheme: "indigo" as ColorTheme,
  setupChecklist: {},
  completedParts: [] as string[],
  inProgressPart: null,
  completedCriteria: {} as Record<string, string[]>,
  completedSteps: {} as Record<string, number[]>,
  completionDates: {} as Record<string, string>,
  requestHistory: [] as RequestHistoryItem[],
  sidebarCollapsed: false,
};

export const useAppStore = create<AppStore>()(
  persist(
    (set, get) => ({
      ...initialState,

      setTheme: (t) => set({ theme: t }),
      toggleTheme: () =>
        set((s) => ({ theme: s.theme === "dark" ? "light" : "dark" })),
      setColorTheme: (t) => set({ colorTheme: t }),

      toggleSetupItem: (id) =>
        set((s) => ({
          setupChecklist: {
            ...s.setupChecklist,
            [id]: !s.setupChecklist[id],
          },
        })),

      markPartComplete: (partId) =>
        set((s) => ({
          completedParts: s.completedParts.includes(partId)
            ? s.completedParts
            : [...s.completedParts, partId],
          inProgressPart: s.inProgressPart === partId ? null : s.inProgressPart,
          completionDates: {
            ...s.completionDates,
            [partId]: new Date().toISOString(),
          },
        })),

      unmarkPartComplete: (partId) =>
        set((s) => ({
          completedParts: s.completedParts.filter((p) => p !== partId),
        })),

      setInProgress: (partId) => set({ inProgressPart: partId }),

      toggleCriteria: (partId, criteriaId) =>
        set((s) => {
          const current = s.completedCriteria[partId] ?? [];
          const updated = current.includes(criteriaId)
            ? current.filter((c) => c !== criteriaId)
            : [...current, criteriaId];
          return { completedCriteria: { ...s.completedCriteria, [partId]: updated } };
        }),

      toggleStep: (partId, stepNumber) =>
        set((s) => {
          const current = s.completedSteps[partId] ?? [];
          const updated = current.includes(stepNumber)
            ? current.filter((n) => n !== stepNumber)
            : [...current, stepNumber];
          return { completedSteps: { ...s.completedSteps, [partId]: updated } };
        }),

      isPartUnlocked: (partId) => {
        // Part 01 is always unlocked
        if (partId === "01") return true;
        const { completedParts } = get();
        const part = partsById[partId];
        if (!part) return true;
        return part.prerequisites.every((p: string) => completedParts.includes(p));
      },

      getOverallProgress: () => {
        const { completedParts } = get();
        return Math.round((completedParts.length / 14) * 100);
      },

      addToHistory: (item) =>
        set((s) => ({
          requestHistory: [item, ...s.requestHistory].slice(0, 10),
        })),

      clearHistory: () => set({ requestHistory: [] }),

      toggleSidebar: () =>
        set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed })),

      resetAll: () => set({ ...initialState }),
    }),
    {
      name: "hospital-ai-platform",
      storage: createJSONStorage(() => localStorage),
    }
  )
);
