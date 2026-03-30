import React from "react";
import { useBackendStatus } from "../../hooks/useBackendStatus";
import { CheckCircle2, XCircle, Loader2, Terminal, RefreshCw } from "lucide-react";
import { clsx } from "clsx";

export const BackendStatusPanel: React.FC = () => {
  const { connected, latencyMs, lastChecked, checking } = useBackendStatus();

  return (
    <div
      className={clsx(
        "rounded-xl border p-5 bg-surface-2",
        connected
          ? "border-success-500/30"
          : checking
          ? "border-surface-3"
          : "border-danger-500/30"
      )}
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2.5">
          {checking ? (
            <Loader2 size={18} className="text-slate-400 animate-spin" />
          ) : connected ? (
            <CheckCircle2 size={18} className="text-success-400" />
          ) : (
            <XCircle size={18} className="text-danger-400" />
          )}
          <div>
            <h3 className="text-sm font-semibold text-slate-200">Backend Status</h3>
            <p className="text-xs text-slate-500">
              {checking
                ? "Checking connection…"
                : connected
                ? `Live · ${latencyMs}ms latency · ${new Date(lastChecked!).toLocaleTimeString()}`
                : "Not reachable · Start the FastAPI server"}
            </p>
          </div>
        </div>
        <div
          className={clsx(
            "px-2.5 py-1 rounded-full text-xs font-semibold",
            checking
              ? "bg-surface-3 text-slate-400"
              : connected
              ? "bg-success-500/15 text-success-300"
              : "bg-danger-500/15 text-danger-300"
          )}
        >
          {checking ? "Checking" : connected ? "Online" : "Offline"}
        </div>
      </div>

      {!connected && !checking && (
        <div className="rounded-lg border border-surface-3 bg-surface-1 p-3">
          <div className="flex items-center gap-2 mb-2">
            <Terminal size={14} className="text-slate-400" />
            <span className="text-xs font-medium text-slate-300">Start the development server</span>
          </div>
          <pre className="text-xs font-mono text-success-400 bg-black/30 rounded-md p-2.5 overflow-x-auto">
            {`cd tutorial/part_14_capstone
pip install -r requirements.txt
uvicorn main:app --reload --port 8000`}
          </pre>
          <p className="text-xs text-slate-500 mt-2">
            Or run any individual part server for Playground access.
          </p>
        </div>
      )}

      {connected && (
        <div className="grid grid-cols-3 gap-3">
          {[
            { label: "Latency", value: `${latencyMs}ms`, ok: (latencyMs ?? 999) < 200 },
            { label: "Endpoint", value: "localhost:8000", ok: true },
            { label: "Health", value: "/health ✓", ok: true },
          ].map((item) => (
            <div key={item.label} className="rounded-lg bg-surface-1 border border-surface-3 p-3 text-center">
              <div className={clsx("text-sm font-mono font-bold", item.ok ? "text-success-300" : "text-warn-300")}>
                {item.value}
              </div>
              <div className="text-[11px] text-slate-500 mt-0.5">{item.label}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
