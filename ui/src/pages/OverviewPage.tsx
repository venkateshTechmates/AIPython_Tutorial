import React from "react";
import { HeroBanner } from "../components/overview/HeroBanner";
import { PhaseCardsGrid } from "../components/overview/PhaseCard";
import { TechStackGrid } from "../components/overview/TechStackGrid";
import { BackendStatusPanel } from "../components/overview/BackendStatusPanel";
import { PartCardsStrip } from "../components/overview/PartCardsStrip";

export const OverviewPage: React.FC = () => (
  <div className="flex flex-col gap-10">
    <HeroBanner />

    <section>
      <h2 className="text-lg font-bold text-slate-100 mb-4">Learning Phases</h2>
      <PhaseCardsGrid />
    </section>

    <section>
      <h2 className="text-lg font-bold text-slate-100 mb-4">Tech Stack</h2>
      <TechStackGrid />
    </section>

    <section>
      <h2 className="text-lg font-bold text-slate-100 mb-4">All Parts</h2>
      <PartCardsStrip />
    </section>

    <section>
      <BackendStatusPanel />
    </section>
  </div>
);
