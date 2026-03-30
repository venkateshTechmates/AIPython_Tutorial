import React, { useState } from "react";
import { Copy, Check } from "lucide-react";
import { clsx } from "clsx";

interface CommandBlockProps {
  label?: string;
  commands: string[];
  className?: string;
}

export const CommandBlock: React.FC<CommandBlockProps> = ({ label, commands, className }) => {
  const [copied, setCopied] = useState(false);
  const text = commands.join("\n");

  const copy = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={clsx("rounded-xl overflow-hidden border border-surface-3", className)}>
      {label && (
        <div className="flex items-center justify-between px-4 py-2 bg-surface-2 border-b border-surface-3">
          <span className="text-xs font-medium text-slate-400">{label}</span>
          <button
            onClick={copy}
            className="flex items-center gap-1 text-xs text-slate-500 hover:text-white transition-colors"
          >
            {copied ? <Check size={12} className="text-success-400" /> : <Copy size={12} />}
            {copied ? "Copied" : "Copy"}
          </button>
        </div>
      )}
      <div className="bg-[#0d1117] px-4 py-3 overflow-x-auto">
        {commands.map((cmd, i) => (
          <div key={i} className="flex items-start gap-2">
            <span className="text-slate-600 text-xs font-mono select-none mt-0.5">$</span>
            <code className="text-sm font-mono text-success-400 whitespace-pre">{cmd}</code>
          </div>
        ))}
      </div>
    </div>
  );
};
