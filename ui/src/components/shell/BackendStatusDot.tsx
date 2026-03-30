import React from "react";
import { useBackendStatus } from "../../hooks/useBackendStatus";
import { Tooltip } from "../ui/Tooltip";
import { clsx } from "clsx";

export const BackendStatusDot: React.FC = () => {
  const { connected, latencyMs, checking } = useBackendStatus();

  const dotColor = checking
    ? "bg-slate-500 animate-pulse"
    : connected
    ? "bg-success-400"
    : "bg-danger-400";

  const label = checking
    ? "Checking backend…"
    : connected
    ? `Backend live · ${latencyMs}ms`
    : "Backend offline — start uvicorn";

  return (
    <Tooltip content={label} placement="bottom">
      <div className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-surface-2 border border-surface-3 cursor-default">
        <span className={clsx("inline-block w-2 h-2 rounded-full flex-shrink-0", dotColor)} />
        <span className="text-xs font-medium text-slate-400 hidden sm:block">
          {connected ? `${latencyMs}ms` : "Offline"}
        </span>
      </div>
    </Tooltip>
  );
};
