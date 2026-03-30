import React from "react";

interface EnvVar {
  name: string;
  required: boolean;
  description: string;
  example: string;
}

const ENV_VARS: EnvVar[] = [
  { name: "OPENAI_API_KEY", required: true, description: "Your OpenAI API key for GPT-4o access", example: "sk-proj-..." },
  { name: "LANGSMITH_API_KEY", required: false, description: "LangSmith key for LLM tracing (Part 12+)", example: "ls__..." },
  { name: "LANGSMITH_PROJECT", required: false, description: "Project name in LangSmith dashboard", example: "hospital-ai-platform" },
  { name: "QDRANT_URL", required: false, description: "Qdrant service URL if not using localhost", example: "http://localhost:6333" },
  { name: "QDRANT_API_KEY", required: false, description: "Qdrant API key for cloud deployments", example: "your-key" },
  { name: "DATABASE_URL", required: false, description: "SQLite connection string (auto-created if omitted)", example: "sqlite+aiosqlite:///./hospital.db" },
  { name: "SECRET_KEY", required: false, description: "JWT signing secret for authentication", example: "super-secret-change-me" },
];

export const EnvVarsTable: React.FC = () => (
  <div>
    <h2 className="text-lg font-bold text-slate-100 mb-4">Environment Variables</h2>
    <div className="overflow-x-auto rounded-xl border border-surface-3">
      <table className="w-full text-sm">
        <thead>
          <tr className="bg-surface-2 border-b border-surface-3">
            <th className="text-left py-3 px-4 text-xs font-bold uppercase tracking-wide text-slate-400">Variable</th>
            <th className="text-left py-3 px-4 text-xs font-bold uppercase tracking-wide text-slate-400">Required</th>
            <th className="text-left py-3 px-4 text-xs font-bold uppercase tracking-wide text-slate-400">Description</th>
            <th className="text-left py-3 px-4 text-xs font-bold uppercase tracking-wide text-slate-400">Example</th>
          </tr>
        </thead>
        <tbody>
          {ENV_VARS.map((env, i) => (
            <tr
              key={env.name}
              className={i % 2 === 0 ? "bg-surface-1" : "bg-surface-2"}
            >
              <td className="py-3 px-4">
                <code className="text-xs font-mono text-brand-300 font-bold">{env.name}</code>
              </td>
              <td className="py-3 px-4">
                {env.required ? (
                  <span className="text-xs font-semibold text-danger-400 uppercase">Required</span>
                ) : (
                  <span className="text-xs text-slate-600">Optional</span>
                )}
              </td>
              <td className="py-3 px-4 text-xs text-slate-400">{env.description}</td>
              <td className="py-3 px-4">
                <code className="text-xs font-mono text-success-400">{env.example}</code>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);
