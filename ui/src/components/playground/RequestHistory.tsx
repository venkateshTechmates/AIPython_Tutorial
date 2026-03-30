import React from "react";
import { Clock, RotateCcw, Trash2, X } from "lucide-react";
import { useAppStore } from "../../store/appStore";
import { MethodBadge } from "../ui/Badge";
import { clsx } from "clsx";

interface RequestHistoryProps {
  onClose: () => void;
  onRestore?: (item: { path: string; method: string }) => void;
}

export const RequestHistory: React.FC<RequestHistoryProps> = ({ onClose, onRestore }) => {
  const requestHistory = useAppStore((s) => s.requestHistory);
  const clearHistory = useAppStore((s) => s.clearHistory);

  return (
    <div className="rounded-xl border border-surface-3 bg-surface-1 flex flex-col max-h-[600px]">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-surface-3">
        <div className="flex items-center gap-2">
          <Clock size={14} className="text-slate-400" />
          <span className="text-sm font-semibold text-slate-200">Request History</span>
          <span className="text-xs text-slate-500">({requestHistory.length})</span>
        </div>
        <div className="flex items-center gap-2">
          {requestHistory.length > 0 && (
            <button
              onClick={() => {
                if (window.confirm("Clear all request history?")) clearHistory();
              }}
              className="flex items-center gap-1 text-xs text-slate-500 hover:text-danger-400 transition-colors"
            >
              <Trash2 size={12} />
              Clear
            </button>
          )}
          <button
            onClick={onClose}
            className="p-1 rounded hover:bg-surface-3 transition-colors"
          >
            <X size={14} className="text-slate-400" />
          </button>
        </div>
      </div>

      {/* List */}
      <div className="flex-1 overflow-y-auto scrollbar-thin">
        {requestHistory.length === 0 ? (
          <div className="flex items-center justify-center h-24 text-slate-600 text-sm">
            No requests yet
          </div>
        ) : (
          [...requestHistory].reverse().map((item, i) => {
            const statusColor =
              item.status === null ? "text-slate-600" :
              item.status < 300 ? "text-success-400" :
              item.status < 400 ? "text-warn-400" :
              "text-danger-400";

            return (
              <div
                key={i}
                className="flex items-center gap-3 px-4 py-3 border-b border-surface-3 hover:bg-surface-2 transition-colors group"
              >
                <MethodBadge method={item.method} size="xs" />
                <code className="flex-1 text-xs font-mono text-slate-300 truncate">
                  {item.path}
                </code>
                <span className={clsx("text-xs font-mono font-bold", statusColor)}>
                  {item.status ?? "—"}
                </span>
                <span className="text-xs text-slate-600">{item.latencyMs ?? "—"}ms</span>
                <span className="text-[10px] text-slate-700">
                  {new Date(item.timestamp).toLocaleTimeString()}
                </span>
                {onRestore && (
                  <button
                    onClick={() => onRestore(item)}
                    className="opacity-0 group-hover:opacity-100 transition-opacity text-slate-500 hover:text-brand-400"
                    title="Restore"
                  >
                    <RotateCcw size={12} />
                  </button>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
