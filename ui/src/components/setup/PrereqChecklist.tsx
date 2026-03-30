import React from "react";
import { useAppStore } from "../../store/appStore";

interface SetupItem {
  id: string;
  label: string;
  description: string;
  command?: string;
}

const SETUP_ITEMS: SetupItem[] = [
  { id: "python", label: "Python 3.11+", description: "Verify Python installation", command: "python --version" },
  { id: "node", label: "Node.js 18+", description: "Required for the UI", command: "node --version" },
  { id: "openai_key", label: "OPENAI_API_KEY set", description: "Export OPENAI_API_KEY in your shell or .env file", command: "echo $OPENAI_API_KEY" },
  { id: "qdrant", label: "Qdrant running", description: "Start via Docker for RAG parts", command: "docker run -p 6333:6333 qdrant/qdrant" },
  { id: "deps", label: "pip install done", description: "Install Python dependencies", command: "pip install -r requirements.txt" },
  { id: "server", label: "uvicorn server up", description: "FastAPI server running on :8000", command: "uvicorn main:app --reload" },
];

export const PrereqChecklist: React.FC = () => {
  const setupChecklist = useAppStore((s) => s.setupChecklist);
  const toggleChecklist = useAppStore((s) => s.toggleSetupItem);

  const doneCount = SETUP_ITEMS.filter((i) => setupChecklist[i.id]).length;

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-slate-100">Prerequisites Checklist</h2>
        <span className="text-xs text-slate-500">{doneCount}/{SETUP_ITEMS.length} checked</span>
      </div>
      <div className="flex flex-col gap-2">
        {SETUP_ITEMS.map((item) => {
          const checked = setupChecklist[item.id] ?? false;
          return (
            <label
              key={item.id}
              className="flex items-start gap-3 p-4 rounded-xl bg-surface-2 border border-surface-3 cursor-pointer hover:bg-surface-3 transition-colors"
            >
              <input
                type="checkbox"
                checked={checked}
                onChange={() => toggleChecklist(item.id)}
                className="mt-0.5 accent-brand-500 w-4 h-4 flex-shrink-0 cursor-pointer"
              />
              <div className="flex-1 min-w-0">
                <div className="text-sm font-semibold text-slate-200">{item.label}</div>
                <div className="text-xs text-slate-500 mt-0.5">{item.description}</div>
                {item.command && (
                  <code className="block mt-1.5 text-xs font-mono text-success-400 bg-surface-1 px-2.5 py-1.5 rounded-lg border border-surface-3">
                    $ {item.command}
                  </code>
                )}
              </div>
            </label>
          );
        })}
      </div>
    </div>
  );
};
