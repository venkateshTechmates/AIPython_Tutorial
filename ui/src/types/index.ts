// ─── Core shared types for the Hospital AI Platform UI ───────────────────────

export type Difficulty = "beginner" | "intermediate" | "advanced";
export type PartStatus = "locked" | "not-started" | "in-progress" | "complete";
export type HttpMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH";

export interface CodeSnippet {
  language: string;
  filename: string;
  snippet: string;
}

export interface EndpointBadge {
  label: string;
  description: string;
}

export interface Concept {
  id: string;
  title: string;
  explanation: string;
  code?: CodeSnippet;
  glossaryTerms?: string[];
}

export interface Step {
  number: number;
  title: string;
  description: string;
  code?: CodeSnippet;
}

export interface AcceptanceCriterion {
  id: string;
  text: string;
}

export interface Gotcha {
  error: string;
  cause: string;
  fix: string;
}

export interface Resource {
  title: string;
  url: string;
}

export interface FileNode {
  name: string;
  type: "file" | "dir";
  children?: FileNode[];
}

export interface PartData {
  id: string;
  title: string;
  goal: string;
  phase: number;
  phaseLabel: string;
  folder: string;
  estimatedHours: number;
  difficulty: Difficulty;
  prerequisites: string[];
  unlocks: string[];
  whatYouBuild: EndpointBadge[];
  mermaidDiagram: string;
  concepts: Concept[];
  steps: Step[];
  acceptanceCriteria: AcceptanceCriterion[];
  gotchas: Gotcha[];
  resources: Resource[];
  files?: FileNode[];
}

export interface PathParam {
  name: string;
  example: string;
}

export interface PlaygroundEndpoint {
  id: string;
  method: HttpMethod;
  path: string;
  description: string;
  exampleBody: Record<string, unknown> | null;
  pathParams?: PathParam[];
  queryParams?: PathParam[];
  streaming?: boolean;
}

export interface PlaygroundConfig {
  partId: string;
  endpoints: PlaygroundEndpoint[];
}

export interface GlossaryTerm {
  id: string;
  term: string;
  definition: string;
  usedInParts: string[];
  category: string;
}

export interface RequestHistoryItem {
  id: string;
  method: HttpMethod;
  path: string;
  status: number | null;
  latencyMs: number | null;
  timestamp: string;
  requestBody?: string;
  responseBody?: string;
}

export interface Phase {
  number: number;
  label: string;
  colorClass: string;
  parts: string[];
}

export const PHASES: Phase[] = [
  { number: 1, label: "Core Foundations", colorClass: "blue", parts: ["01", "02", "03"] },
  { number: 2, label: "RAG & First Agent", colorClass: "purple", parts: ["04", "05"] },
  { number: 3, label: "Multi-Agent Systems", colorClass: "orange", parts: ["06", "07", "08"] },
  { number: 4, label: "Production Patterns", colorClass: "red", parts: ["09", "10", "11", "12", "13"] },
  { number: 5, label: "Capstone", colorClass: "yellow", parts: ["14"] },
];

export const PHASE_COLORS: Record<number, { bg: string; text: string; border: string; pill: string }> = {
  1: { bg: "bg-blue-500/10", text: "text-blue-400", border: "border-blue-500/30", pill: "bg-blue-500" },
  2: { bg: "bg-purple-500/10", text: "text-purple-400", border: "border-purple-500/30", pill: "bg-purple-500" },
  3: { bg: "bg-orange-500/10", text: "text-orange-400", border: "border-orange-500/30", pill: "bg-orange-500" },
  4: { bg: "bg-red-500/10", text: "text-red-400", border: "border-red-500/30", pill: "bg-red-500" },
  5: { bg: "bg-yellow-500/10", text: "text-yellow-400", border: "border-yellow-500/30", pill: "bg-yellow-500" },
};

export const METHOD_COLORS: Record<HttpMethod, string> = {
  GET: "bg-green-500/20 text-green-400 border-green-500/30",
  POST: "bg-blue-500/20 text-blue-400 border-blue-500/30",
  PUT: "bg-amber-500/20 text-amber-400 border-amber-500/30",
  DELETE: "bg-red-500/20 text-red-400 border-red-500/30",
  PATCH: "bg-purple-500/20 text-purple-400 border-purple-500/30",
};

export const DIFFICULTY_COLORS: Record<Difficulty, string> = {
  beginner: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
  intermediate: "bg-amber-500/20 text-amber-400 border-amber-500/30",
  advanced: "bg-red-500/20 text-red-400 border-red-500/30",
};
