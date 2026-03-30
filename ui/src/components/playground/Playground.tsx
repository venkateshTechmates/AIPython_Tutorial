import React, { useState } from "react";
import { useAppStore } from "../../store/appStore";
import { allPlaygrounds, playgroundById } from "../../data/playgrounds";
import { partsById } from "../../data/parts";
import { EndpointList } from "./EndpointList";
import { RequestPane } from "./RequestPane";
import { RequestHistory } from "./RequestHistory";
import { Tabs, TabList, Tab, TabPanel } from "../ui/Tabs";
import { History } from "lucide-react";
import { clsx } from "clsx";
import type { PlaygroundEndpoint } from "../../types";

interface PlaygroundProps {
  initialPartId?: string;
}

export const Playground: React.FC<PlaygroundProps> = ({ initialPartId }) => {
  const [selectedPartId, setSelectedPartId] = useState(
    initialPartId ?? allPlaygrounds[0]?.partId ?? "01"
  );
  const [selectedEndpoint, setSelectedEndpoint] = useState<PlaygroundEndpoint | null>(null);
  const [showHistory, setShowHistory] = useState(false);

  const config = playgroundById[selectedPartId];

  return (
    <div className="flex flex-col h-full gap-4">
      {/* Part selector */}
      <div className="flex items-center gap-3">
        <label className="text-xs text-slate-500 font-medium flex-shrink-0">Part:</label>
        <select
          value={selectedPartId}
          onChange={(e) => {
            setSelectedPartId(e.target.value);
            setSelectedEndpoint(null);
          }}
          className="bg-surface-2 border border-surface-3 rounded-lg text-sm text-slate-200 px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-brand-500 cursor-pointer"
        >
          {allPlaygrounds.map((pg) => (
            <option key={pg.partId} value={pg.partId}>
              {pg.partId} — {partsById[pg.partId]?.title ?? `Part ${pg.partId}`}
            </option>
          ))}
        </select>

        <button
          onClick={() => setShowHistory((h) => !h)}
          className={clsx(
            "ml-auto flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-colors border",
            showHistory
              ? "bg-brand-600/20 border-brand-500/30 text-brand-300"
              : "bg-surface-2 border-surface-3 text-slate-400 hover:text-slate-200"
          )}
        >
          <History size={13} />
          History
        </button>
      </div>

      {showHistory ? (
        <RequestHistory onClose={() => setShowHistory(false)} />
      ) : (
        <div className="flex gap-4 flex-1 min-h-0">
          {/* Endpoint list */}
          <div className="w-64 flex-shrink-0 rounded-xl border border-surface-3 bg-surface-1 overflow-hidden">
            {config ? (
              <EndpointList
                endpoints={config.endpoints}
                selected={selectedEndpoint}
                onSelect={setSelectedEndpoint}
              />
            ) : (
              <div className="flex items-center justify-center h-full text-slate-600 text-sm p-4">
                No endpoints for this part
              </div>
            )}
          </div>

          {/* Request / response pane */}
          <div className="flex-1 min-h-0 rounded-xl border border-surface-3 bg-surface-1 p-4 overflow-hidden">
            <RequestPane endpoint={selectedEndpoint} />
          </div>
        </div>
      )}
    </div>
  );
};
