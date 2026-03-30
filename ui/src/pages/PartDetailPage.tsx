import React, { useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { partsById } from "../data/parts";
import { useAppStore } from "../store/appStore";
import { PartHeader } from "../components/part/PartHeader";
import { WhatYouBuild } from "../components/part/WhatYouBuild";
import { ArchDiagram } from "../components/part/ArchDiagram";
import { ConceptAccordion } from "../components/part/ConceptAccordion";
import { StepGuide } from "../components/part/StepGuide";
import { AcceptanceCriteria } from "../components/part/AcceptanceCriteria";
import { ErrorsTable } from "../components/part/ErrorsTable";
import { NextPartCTA } from "../components/part/NextPartCTA";
import { Playground } from "../components/playground/Playground";
import { FlaskConical } from "lucide-react";

export const PartDetailPage: React.FC = () => {
  const { partId } = useParams<{ partId: string }>();
  const navigate = useNavigate();
  const setInProgress = useAppStore((s) => s.setInProgress);
  const completedParts = useAppStore((s) => s.completedParts);
  const isPartUnlocked = useAppStore((s) => s.isPartUnlocked);

  const part = partId ? partsById[partId] : null;

  useEffect(() => {
    if (!part) {
      navigate("/", { replace: true });
      return;
    }
    if (!completedParts.includes(part.id)) {
      setInProgress(part.id);
    }
  }, [part?.id]);

  if (!part) return null;

  if (!isPartUnlocked(part.id)) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-4 text-center">
        <div className="text-4xl">🔒</div>
        <h2 className="text-xl font-bold text-slate-200">Part Locked</h2>
        <p className="text-slate-400 max-w-sm">
          Complete the prerequisites to unlock this part:{" "}
          {part.prerequisites.map((id) => `Part ${id}`).join(", ")}
        </p>
        <button
          onClick={() => navigate(-1)}
          className="px-4 py-2 bg-surface-2 border border-surface-3 rounded-xl text-sm text-slate-300 hover:bg-surface-3 transition-colors"
        >
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl">
      <PartHeader part={part} />
      <WhatYouBuild endpoints={part.whatYouBuild} />
      <ArchDiagram definition={part.mermaidDiagram} />
      <ConceptAccordion concepts={part.concepts} />
      <StepGuide steps={part.steps} partId={part.id} />
      <AcceptanceCriteria criteria={part.acceptanceCriteria} partId={part.id} />

      {/* Embedded playground */}
      <section className="mb-8">
        <div className="flex items-center gap-2 mb-4">
          <FlaskConical size={18} className="text-brand-400" />
          <h2 className="text-lg font-bold text-slate-100">Live Playground</h2>
        </div>
        <div className="rounded-xl border border-surface-3 bg-surface-1 p-4 min-h-[500px]">
          <Playground initialPartId={part.id} />
        </div>
      </section>

      {part.gotchas.length > 0 && <ErrorsTable gotchas={part.gotchas} />}

      {/* Resources */}
      {part.resources && part.resources.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-bold text-slate-100 mb-4">Resources</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {part.resources.map((res, i) => (
              <a
                key={i}
                href={res.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex flex-col gap-1 p-4 rounded-xl bg-surface-2 border border-surface-3 hover:border-brand-500/30 transition-colors group"
              >
                <span className="text-sm font-semibold text-slate-200 group-hover:text-brand-300 transition-colors">
                  {res.title}
                </span>
                <span className="text-xs text-brand-500 font-mono truncate">{res.url}</span>
              </a>
            ))}
          </div>
        </section>
      )}

      <NextPartCTA part={part} />
    </div>
  );
};
