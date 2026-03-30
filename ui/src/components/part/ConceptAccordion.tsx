import React from "react";
import { BookOpen } from "lucide-react";
import { Accordion, AccordionItem } from "../ui/Accordion";
import { CodeBlock } from "../ui/CodeBlock";
import type { Concept } from "../../types";

interface ConceptAccordionProps {
  concepts: Concept[];
}

export const ConceptAccordion: React.FC<ConceptAccordionProps> = ({ concepts }) => (
  <section className="mb-8">
    <div className="flex items-center gap-2 mb-4">
      <BookOpen size={18} className="text-brand-400" />
      <h2 className="text-lg font-bold text-slate-100">Key Concepts</h2>
      <span className="text-xs text-slate-500 bg-surface-3 px-2 py-0.5 rounded-full">
        {concepts.length}
      </span>
    </div>
    <Accordion>
      {concepts.map((concept, i) => (
        <AccordionItem
          key={concept.id}
          title={concept.title}
          defaultOpen={i === 0}
        >
          <div className="flex flex-col gap-4">
            <p className="text-sm text-slate-400 leading-relaxed">{concept.explanation}</p>
            {concept.code && (
              <CodeBlock
                code={concept.code.snippet}
                language={concept.code.language}
                filename={concept.code.filename}
              />
            )}
            {concept.glossaryTerms && concept.glossaryTerms.length > 0 && (
              <div className="flex flex-wrap gap-1.5">
                <span className="text-xs text-slate-500">Related terms:</span>
                {concept.glossaryTerms.map((term) => (
                  <span
                    key={term}
                    className="text-xs text-brand-400 bg-brand-500/10 px-2 py-0.5 rounded-full border border-brand-500/20"
                  >
                    {term}
                  </span>
                ))}
              </div>
            )}
          </div>
        </AccordionItem>
      ))}
    </Accordion>
  </section>
);
