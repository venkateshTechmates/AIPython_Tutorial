import React from "react";
import { PrereqChecklist } from "../components/setup/PrereqChecklist";
import { CommandBlock } from "../components/setup/CommandBlock";
import { EnvVarsTable } from "../components/setup/EnvVarsTable";

const QUICK_START = [
  "git clone https://github.com/your-org/hospital-ai-platform.git",
  "cd hospital-ai-platform",
  "python -m venv .venv && source .venv/bin/activate",
  "pip install -r requirements.txt",
  "cp .env.example .env  # Add your OPENAI_API_KEY",
  "cd part_01_fastapi_foundations && uvicorn main:app --reload",
];

const QDRANT_START = [
  "docker pull qdrant/qdrant",
  "docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant",
];

export const SetupPage: React.FC = () => (
  <div className="flex flex-col gap-10 max-w-4xl">
    <div>
      <h1 className="text-2xl font-bold text-white mb-2">Setup Guide</h1>
      <p className="text-slate-400">
        Get your development environment ready to run all 14 parts of the Hospital AI Platform.
      </p>
    </div>

    <PrereqChecklist />

    <section>
      <h2 className="text-lg font-bold text-slate-100 mb-4">Quick Start</h2>
      <CommandBlock label="Clone & run Part 1" commands={QUICK_START} />
    </section>

    <section>
      <h2 className="text-lg font-bold text-slate-100 mb-4">Qdrant (Required for Part 4+)</h2>
      <p className="text-sm text-slate-400 mb-3">
        Parts 4 and beyond use Qdrant for vector search. Start it with Docker:
      </p>
      <CommandBlock label="Start Qdrant" commands={QDRANT_START} />
    </section>

    <EnvVarsTable />

    <section className="rounded-xl border border-surface-3 bg-surface-2 p-5">
      <h2 className="text-base font-bold text-slate-100 mb-3">Cost Estimate</h2>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { label: "Parts 1-3", range: "$0", note: "No LLM usage" },
          { label: "Parts 4-8", range: "$0.50–$2", note: "per part (GPT-4o)" },
          { label: "Parts 9-13", range: "$1–$3", note: "per part (streaming)" },
          { label: "Part 14", range: "$3–$8", note: "capstone full run" },
        ].map((item) => (
          <div key={item.label} className="p-3 rounded-lg bg-surface-1 border border-surface-3 text-center">
            <div className="text-xs text-slate-500 mb-1">{item.label}</div>
            <div className="text-base font-bold text-success-300">{item.range}</div>
            <div className="text-[11px] text-slate-600 mt-0.5">{item.note}</div>
          </div>
        ))}
      </div>
      <p className="text-xs text-slate-600 mt-3">
        * Estimates for GPT-4o at current pricing. Costs may vary with usage patterns.
      </p>
    </section>
  </div>
);
