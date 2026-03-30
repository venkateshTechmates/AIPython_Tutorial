import React from "react";
import { AlertTriangle } from "lucide-react";
import { AccordionItem, Accordion } from "../ui/Accordion";
import type { Gotcha } from "../../types";

interface ErrorsTableProps {
  gotchas: Gotcha[];
}

export const ErrorsTable: React.FC<ErrorsTableProps> = ({ gotchas }) => {
  if (!gotchas.length) return null;

  return (
    <section className="mb-8">
      <div className="flex items-center gap-2 mb-4">
        <AlertTriangle size={18} className="text-warn-400" />
        <h2 className="text-lg font-bold text-slate-100">Common Gotchas</h2>
        <span className="text-xs text-slate-500 bg-surface-3 px-2 py-0.5 rounded-full">
          {gotchas.length}
        </span>
      </div>
      <Accordion>
        {gotchas.map((gotcha, i) => (
          <AccordionItem
            key={i}
            title={
              <span className="flex items-center gap-2">
                <span className="font-mono text-sm text-warn-300 bg-warn-900/20 px-2 py-0.5 rounded border border-warn-500/20">
                  {gotcha.error || "Error"}
                </span>
              </span>
            }
          >
            <div className="flex flex-col gap-3">
              <div>
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">Cause</div>
                <p className="text-sm text-slate-400 leading-relaxed">{gotcha.cause}</p>
              </div>
              <div>
                <div className="text-xs font-semibold text-success-500 uppercase tracking-wide mb-1">Fix</div>
                <p className="text-sm text-slate-300 leading-relaxed">{gotcha.fix}</p>
              </div>
            </div>
          </AccordionItem>
        ))}
      </Accordion>
    </section>
  );
};
