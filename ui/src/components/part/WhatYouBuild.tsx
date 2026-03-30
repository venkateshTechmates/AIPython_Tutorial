import React from "react";
import { Boxes } from "lucide-react";
import type { PartData } from "../../types";

interface WhatYouBuildProps {
  endpoints: PartData["whatYouBuild"];
}

export const WhatYouBuild: React.FC<WhatYouBuildProps> = ({ endpoints }) => (
  <section className="mb-8">
    <div className="flex items-center gap-2 mb-4">
      <Boxes size={18} className="text-brand-400" />
      <h2 className="text-lg font-bold text-slate-100">What You'll Build</h2>
    </div>
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
      {endpoints.map((ep, i) => (
        <div
          key={i}
          className="flex flex-col gap-2 p-4 rounded-xl bg-surface-2 border border-surface-3 hover:border-brand-500/30 transition-colors group"
        >
          <span className="text-xs font-bold text-brand-400 uppercase tracking-wide">{ep.label}</span>
          <p className="text-xs text-slate-500 leading-relaxed">{ep.description}</p>
        </div>
      ))}
    </div>
  </section>
);
