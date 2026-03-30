import React, { useState, useMemo } from "react";
import { glossaryTerms as allTerms } from "../data/glossary";
import {
  GlossarySearch,
  TermCard,
  AlphaIndex,
} from "../components/glossary/GlossaryComponents";

export const GlossaryPage: React.FC = () => {
  const [search, setSearch] = useState("");
  const [activeLetter, setActiveLetter] = useState("");

  const filtered = useMemo(() => {
    let terms = allTerms;
    if (search) {
      const q = search.toLowerCase();
      terms = terms.filter(
        (t) =>
          t.term.toLowerCase().includes(q) ||
          t.definition.toLowerCase().includes(q) ||
          t.category.toLowerCase().includes(q)
      );
    }
    if (activeLetter) {
      terms = terms.filter((t) =>
        t.term.toUpperCase().startsWith(activeLetter)
      );
    }
    return terms;
  }, [search, activeLetter]);

  const availableLetters = useMemo(() => {
    const s = new Set<string>();
    for (const t of allTerms) {
      s.add(t.term[0].toUpperCase());
    }
    return s;
  }, []);

  return (
    <div className="flex flex-col gap-6 max-w-5xl">
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">Glossary</h1>
        <p className="text-sm text-slate-400">
          {allTerms.length} terms covering AI, LangGraph, FastAPI, and more.
        </p>
      </div>

      <GlossarySearch search={search} onSearch={(q) => { setSearch(q); setActiveLetter(""); }} />

      <AlphaIndex
        activeLetter={activeLetter}
        onLetter={setActiveLetter}
        available={availableLetters}
      />

      <div className="text-xs text-slate-600">
        {filtered.length === allTerms.length
          ? `${allTerms.length} terms`
          : `${filtered.length} of ${allTerms.length} terms`}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((term) => (
          <TermCard key={term.id} term={term} />
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-16 text-slate-600">
          No terms match your search
        </div>
      )}
    </div>
  );
};
