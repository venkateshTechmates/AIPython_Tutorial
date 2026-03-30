import React, { useState } from "react";
import { Search } from "lucide-react";
import { MethodBadge } from "../ui/Badge";
import { clsx } from "clsx";
import type { PlaygroundEndpoint } from "../../types";

interface EndpointListProps {
  endpoints: PlaygroundEndpoint[];
  selected: PlaygroundEndpoint | null;
  onSelect: (ep: PlaygroundEndpoint) => void;
}

export const EndpointList: React.FC<EndpointListProps> = ({
  endpoints,
  selected,
  onSelect,
}) => {
  const [search, setSearch] = useState("");

  const filtered = search
    ? endpoints.filter(
        (ep) =>
          ep.path.toLowerCase().includes(search.toLowerCase()) ||
          ep.description.toLowerCase().includes(search.toLowerCase())
      )
    : endpoints;

  // Group by first path segment
  const groups: Record<string, PlaygroundEndpoint[]> = {};
  for (const ep of filtered) {
    const tag = ep.path.split("/")[1] ?? "endpoints";
    if (!groups[tag]) groups[tag] = [];
    groups[tag].push(ep);
  }

  return (
    <div className="flex flex-col h-full">
      {/* Search */}
      <div className="p-3 border-b border-surface-3">
        <div className="relative">
          <Search
            size={13}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none"
          />
          <input
            type="search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search endpoints…"
            className="w-full h-8 pl-8 pr-3 font-mono text-xs bg-surface-1 border border-surface-3 rounded-lg text-slate-300 focus:outline-none focus:ring-2 focus:ring-brand-500"
          />
        </div>
      </div>

      {/* List */}
      <div className="flex-1 overflow-y-auto p-2 scrollbar-thin">
        {Object.entries(groups).map(([tag, eps]) => (
          <div key={tag} className="mb-3">
            <div className="text-[10px] font-bold uppercase tracking-widest text-slate-600 px-2 mb-1">
              {tag}
            </div>
            {eps.map((ep) => {
              const isSelected = selected?.path === ep.path && selected?.method === ep.method;
              return (
                <button
                  key={`${ep.method}${ep.path}`}
                  onClick={() => onSelect(ep)}
                  className={clsx(
                    "w-full flex items-center gap-2 px-2 py-2 rounded-lg text-left transition-colors mb-0.5 group",
                    isSelected
                      ? "bg-brand-600/20 border border-brand-500/30"
                      : "hover:bg-surface-3 border border-transparent"
                  )}
                >
                  <MethodBadge method={ep.method} size="xs" />
                  <div className="flex flex-col min-w-0">
                    <span className="font-mono text-xs text-slate-300 truncate">{ep.path}</span>
                    {ep.description && (
                      <span className="text-[10px] text-slate-500 truncate">{ep.description}</span>
                    )}
                  </div>
                  {ep.streaming && (
                    <span className="ml-auto text-[9px] text-brand-400 bg-brand-500/10 px-1.5 py-0.5 rounded flex-shrink-0">
                      SSE
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        ))}
        {filtered.length === 0 && (
          <p className="text-xs text-slate-600 text-center py-8">No matching endpoints</p>
        )}
      </div>
    </div>
  );
};
