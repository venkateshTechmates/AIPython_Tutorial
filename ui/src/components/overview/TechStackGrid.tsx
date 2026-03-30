import React from "react";
import { Tooltip } from "../ui/Tooltip";

interface TechItem {
  name: string;
  version: string;
  emoji: string;
  description: string;
  category: string;
  url: string;
}

const TECH_STACK: TechItem[] = [
  { name: "FastAPI", version: "0.111", emoji: "⚡", description: "Async Python web framework with automatic OpenAPI docs", category: "Backend", url: "https://fastapi.tiangolo.com" },
  { name: "LangGraph", version: "0.2", emoji: "🕸", description: "Stateful, multi-actor LLM application framework from LangChain", category: "AI", url: "https://langchain-ai.github.io/langgraph/" },
  { name: "LangChain", version: "0.2", emoji: "🔗", description: "Framework for building LLM-powered applications", category: "AI", url: "https://python.langchain.com" },
  { name: "OpenAI", version: "gpt-4o", emoji: "🤖", description: "GPT-4o models for reasoning, function calling, and generation", category: "LLM", url: "https://platform.openai.com" },
  { name: "Pydantic", version: "v2", emoji: "🔷", description: "Data validation and serialization using Python type hints", category: "Backend", url: "https://docs.pydantic.dev" },
  { name: "SQLAlchemy", version: "2.0", emoji: "🗄", description: "Async SQLite ORM for persistent data storage", category: "Database", url: "https://docs.sqlalchemy.org" },
  { name: "Qdrant", version: "1.9", emoji: "🔍", description: "High-performance vector database for semantic search and RAG", category: "Database", url: "https://qdrant.tech" },
  { name: "React", version: "18", emoji: "⚛️", description: "UI component library with hooks and concurrent rendering", category: "Frontend", url: "https://react.dev" },
  { name: "TypeScript", version: "5", emoji: "🟦", description: "Typed JavaScript for safer, more scalable code", category: "Frontend", url: "https://typescriptlang.org" },
  { name: "Tailwind CSS", version: "3.4", emoji: "🎨", description: "Utility-first CSS framework for rapid UI development", category: "Frontend", url: "https://tailwindcss.com" },
  { name: "pytest", version: "8", emoji: "✅", description: "Python testing framework with fixtures and plugins", category: "Testing", url: "https://pytest.org" },
  { name: "LangSmith", version: "0.1", emoji: "🔭", description: "LLM observability, tracing, and evaluation platform", category: "Observability", url: "https://smith.langchain.com" },
  { name: "Docker", version: "24", emoji: "🐳", description: "Containerization for consistent, portable deployment", category: "Deploy", url: "https://docker.com" },
  { name: "Zustand", version: "4", emoji: "🐻", description: "Lightweight React state management with persistence", category: "Frontend", url: "https://zustand-demo.pmnd.rs" },
];

const CATEGORY_COLORS: Record<string, string> = {
  Backend: "bg-agent-500/10 text-agent-300 border-agent-500/20",
  AI: "bg-brand-500/10 text-brand-300 border-brand-500/20",
  LLM: "bg-purple-500/10 text-purple-300 border-purple-500/20",
  Database: "bg-success-500/10 text-success-300 border-success-500/20",
  Frontend: "bg-warn-500/10 text-warn-300 border-warn-500/20",
  Testing: "bg-teal-500/10 text-teal-300 border-teal-500/20",
  Observability: "bg-orange-500/10 text-orange-300 border-orange-500/20",
  Deploy: "bg-blue-500/10 text-blue-300 border-blue-500/20",
};

export const TechStackGrid: React.FC = () => (
  <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-7 gap-3">
    {TECH_STACK.map((tech) => (
      <Tooltip
        key={tech.name}
        content={
          <div className="max-w-[180px]">
            <div className="font-semibold mb-0.5">{tech.name} <span className="text-slate-400 text-[10px]">{tech.version}</span></div>
            <div className="text-slate-300 text-[11px] leading-relaxed">{tech.description}</div>
          </div>
        }
        placement="top"
      >
        <a
          href={tech.url}
          target="_blank"
          rel="noopener noreferrer"
          className="flex flex-col items-center gap-2 p-3 rounded-xl bg-surface-2 border border-surface-3 hover:border-brand-500/40 hover:bg-surface-3 transition-all group cursor-pointer"
        >
          <span className="text-2xl">{tech.emoji}</span>
          <span className="text-xs font-medium text-slate-300 group-hover:text-white transition-colors text-center leading-tight">
            {tech.name}
          </span>
          <span
            className={`text-[9px] px-1.5 py-0.5 rounded-full border font-medium ${CATEGORY_COLORS[tech.category] ?? "bg-surface-3 text-slate-400 border-surface-3"}`}
          >
            {tech.category}
          </span>
        </a>
      </Tooltip>
    ))}
  </div>
);
