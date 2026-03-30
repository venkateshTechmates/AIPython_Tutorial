import React, { useEffect, useRef, useState } from "react";
import { clsx } from "clsx";
import { Copy, Check } from "lucide-react";

interface CodeBlockProps {
  code: string;
  language?: string;
  filename?: string;
  showCopy?: boolean;
  maxHeight?: string;
  className?: string;
}

// Simple token highlighting using regex patterns (no heavy deps at runtime)
function tokenize(code: string, language: string): string {
  if (!language || language === "text" || language === "plain") {
    return escapeHtml(code);
  }

  let result = escapeHtml(code);

  // Common patterns across languages
  const patterns: Array<[RegExp, string]> = [
    // Strings (double/single quoted)
    [/(["'`])((?:\\.|(?!\1)[^\\])*)\1/g, `<span class="ct-string">$1$2$1</span>`],
    // Line comments
    [/(\/\/[^\n]*|#[^\n]*)/g, `<span class="ct-comment">$1</span>`],
    // Block comments
    [/(\/\*[\s\S]*?\*\/)/g, `<span class="ct-comment">$1</span>`],
    // Numbers
    [/\b(\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\b/g, `<span class="ct-number">$1</span>`],
    // Python/TS keywords
    [/\b(def|class|return|import|from|as|if|elif|else|for|while|with|try|except|finally|raise|yield|async|await|pass|break|continue|lambda|in|not|and|or|is|None|True|False|self|const|let|var|function|interface|type|export|default|extends|implements|new|this|typeof|instanceof|void|null|undefined|true|false|string|number|boolean|any|never|readonly|public|private|protected|static|abstract|enum)\b/g, `<span class="ct-keyword">$1</span>`],
    // Decorators
    [/(@\w+)/g, `<span class="ct-decorator">$1</span>`],
    // Function calls
    [/\b(\w+)(?=\s*\()/g, `<span class="ct-func">$1</span>`],
  ];

  for (const [pattern, replacement] of patterns) {
    result = result.replace(pattern, replacement);
  }

  return result;
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export const CodeBlock: React.FC<CodeBlockProps> = ({
  code,
  language = "python",
  filename,
  showCopy = true,
  maxHeight = "24rem",
  className,
}) => {
  const [copied, setCopied] = useState(false);
  const [highlighted, setHighlighted] = useState<string>("");
  const mounted = useRef(true);

  useEffect(() => {
    mounted.current = true;
    const html = tokenize(code.trim(), language);
    if (mounted.current) setHighlighted(html);
    return () => { mounted.current = false; };
  }, [code, language]);

  const copy = async () => {
    await navigator.clipboard.writeText(code.trim());
    setCopied(true);
    setTimeout(() => { if (mounted.current) setCopied(false); }, 2000);
  };

  return (
    <div className={clsx("rounded-xl overflow-hidden border border-surface-3 bg-[#0d1117] group", className)}>
      {/* Header bar */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-surface-3 bg-surface-2">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-danger-500/60" />
            <div className="w-3 h-3 rounded-full bg-warn-500/60" />
            <div className="w-3 h-3 rounded-full bg-success-500/60" />
          </div>
          {filename && (
            <span className="text-xs text-slate-400 font-mono ml-2">{filename}</span>
          )}
          {!filename && language && (
            <span className="text-xs text-slate-500 capitalize ml-2">{language}</span>
          )}
        </div>
        {showCopy && (
          <button
            onClick={copy}
            className="opacity-0 group-hover:opacity-100 flex items-center gap-1 text-xs text-slate-400 hover:text-white transition-all px-2 py-1 rounded-md hover:bg-surface-3"
            title="Copy code"
          >
            {copied ? (
              <><Check size={12} className="text-success-400" /> Copied</>
            ) : (
              <><Copy size={12} /> Copy</>
            )}
          </button>
        )}
      </div>
      {/* Code area */}
      <div
        className="overflow-auto"
        style={{ maxHeight }}
      >
        <pre className="p-4 text-sm leading-6 font-mono text-slate-200">
          <code
            dangerouslySetInnerHTML={{ __html: highlighted || escapeHtml(code.trim()) }}
            className="code-highlighted"
          />
        </pre>
      </div>
    </div>
  );
};
