import React, { useEffect, useRef, useState } from "react";
import { GitBranch, Copy, Check, Maximize2 } from "lucide-react";
import { Modal } from "../ui/Modal";

interface ArchDiagramProps {
  definition: string;
  title?: string;
}

declare global {
  interface Window {
    mermaid?: {
      initialize: (config: Record<string, unknown>) => void;
      render: (id: string, definition: string) => Promise<{ svg: string }>;
    };
  }
}

let mermaidInited = false;

async function getMermaid() {
  if (window.mermaid) return window.mermaid;
  const mod = await import("mermaid");
  window.mermaid = mod.default;
  if (!mermaidInited) {
    window.mermaid.initialize({
      startOnLoad: false,
      theme: "dark",
      darkMode: true,
      themeVariables: {
        primaryColor: "#6366f1",
        primaryTextColor: "#e2e8f0",
        primaryBorderColor: "#4f46e5",
        lineColor: "#6366f1",
        secondaryColor: "#1e293b",
        tertiaryColor: "#0f172a",
        background: "#0f172a",
        mainBkg: "#1e293b",
        nodeBorder: "#4f46e5",
        clusterBkg: "#1e293b",
        edgeLabelBackground: "#1e293b",
        fontSize: "14px",
      },
    });
    mermaidInited = true;
  }
  return window.mermaid;
}

let idCounter = 0;

export const ArchDiagram: React.FC<ArchDiagramProps> = ({ definition, title }) => {
  const containerId = useRef(`mermaid-${++idCounter}`);
  const [svg, setSvg] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [zoomed, setZoomed] = useState(false);
  const mounted = useRef(true);

  useEffect(() => {
    mounted.current = true;
    setError(null);
    setSvg("");

    getMermaid()
      .then((m) => m.render(containerId.current, definition))
      .then(({ svg }) => {
        if (mounted.current) setSvg(svg);
      })
      .catch((err) => {
        console.warn("Mermaid render error:", err);
        if (mounted.current) setError(String(err));
      });

    return () => { mounted.current = false; };
  }, [definition]);

  const copySource = async () => {
    await navigator.clipboard.writeText(definition);
    setCopied(true);
    setTimeout(() => { if (mounted.current) setCopied(false); }, 2000);
  };

  const DiagramContent = () => (
    <>
      {error ? (
        <div className="p-4 rounded-lg bg-danger-900/20 border border-danger-500/30 text-xs font-mono text-danger-300">
          Diagram render failed: {error}
          <pre className="mt-2 text-slate-400 whitespace-pre-wrap text-[10px]">{definition}</pre>
        </div>
      ) : svg ? (
        <div
          className="overflow-auto rounded-lg [&>svg]:max-w-full [&>svg]:h-auto"
          dangerouslySetInnerHTML={{ __html: svg }}
        />
      ) : (
        <div className="flex items-center justify-center h-32 text-slate-500 text-sm">
          <span className="animate-pulse">Rendering diagram…</span>
        </div>
      )}
    </>
  );

  return (
    <section className="mb-8">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <GitBranch size={18} className="text-brand-400" />
          <h2 className="text-lg font-bold text-slate-100">
            {title ?? "Architecture Diagram"}
          </h2>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={copySource}
            className="flex items-center gap-1 text-xs text-slate-400 hover:text-white px-2.5 py-1.5 rounded-lg hover:bg-surface-3 transition-colors"
          >
            {copied ? <Check size={12} className="text-success-400" /> : <Copy size={12} />}
            {copied ? "Copied" : "Source"}
          </button>
          <button
            onClick={() => setZoomed(true)}
            className="flex items-center gap-1 text-xs text-slate-400 hover:text-white px-2.5 py-1.5 rounded-lg hover:bg-surface-3 transition-colors"
          >
            <Maximize2 size={12} />
            Zoom
          </button>
        </div>
      </div>

      <div className="rounded-xl border border-surface-3 bg-surface-2 p-6">
        <DiagramContent />
      </div>

      <Modal open={zoomed} onClose={() => setZoomed(false)} title="Architecture Diagram" size="xl">
        <div className="p-6 overflow-auto">
          <DiagramContent />
        </div>
      </Modal>
    </section>
  );
};
