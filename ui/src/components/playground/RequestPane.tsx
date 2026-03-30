import React, { useState, useRef, useEffect } from "react";
import { Send, Loader2, Copy, Check, X } from "lucide-react";
import { api, resolvePath, buildCurlCommand } from "../../lib/api";
import { useAppStore } from "../../store/appStore";
import { MethodBadge } from "../ui/Badge";
import { Tabs, TabList, Tab, TabPanel } from "../ui/Tabs";
import { CodeBlock } from "../ui/CodeBlock";
import { useToast } from "../ui/Toast";
import { clsx } from "clsx";
import type { PlaygroundEndpoint } from "../../types";

interface RequestPaneProps {
  endpoint: PlaygroundEndpoint | null;
}

const REQUEST_TIMEOUT_MS = 30_000;

const StatusPill: React.FC<{ status: number }> = ({ status }) => {
  const color =
    status < 300 ? "bg-success-500/15 text-success-300 border-success-500/30" :
    status < 400 ? "bg-warn-500/15 text-warn-300 border-warn-500/30" :
    "bg-danger-500/15 text-danger-300 border-danger-500/30";
  return (
    <span className={clsx("px-2 py-0.5 rounded-full text-xs font-mono font-bold border", color)}>
      {status}
    </span>
  );
};

export const RequestPane: React.FC<RequestPaneProps> = ({ endpoint }) => {
  const { toast } = useToast();
  const addToHistory = useAppStore((s) => s.addToHistory);

  const [pathParams, setPathParams] = useState<Record<string, string>>({});
  const [queryParams, setQueryParams] = useState<Record<string, string>>({});
  const [headers, setHeaders] = useState<Record<string, string>>({});
  const [bodyText, setBodyText] = useState("{}");
  const [bodyError, setBodyError] = useState<string | null>(null);

  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<{
    status: number;
    data: unknown;
    time: number;
  } | null>(null);
  const [respError, setRespError] = useState<string | null>(null);
  const [streamLines, setStreamLines] = useState<string[]>([]);

  const abortRef = useRef<AbortController | null>(null);
  const mounted = useRef(true);

  useEffect(() => {
    mounted.current = true;
    // Reset form when endpoint changes
    setPathParams({});
    setQueryParams({});
    setBodyText(endpoint?.exampleBody ? JSON.stringify(endpoint.exampleBody, null, 2) : "{}");
    setBodyError(null);
    setResponse(null);
    setRespError(null);
    setStreamLines([]);
    return () => { mounted.current = false; };
  }, [endpoint?.path]);

  if (!endpoint) {
    return (
      <div className="flex items-center justify-center h-full text-slate-500 text-sm">
        Select an endpoint to get started
      </div>
    );
  }

  const validateBody = (text: string) => {
    if (!text.trim() || endpoint.method === "GET") return null;
    try { JSON.parse(text); return null; }
    catch { return "Invalid JSON"; }
  };

  const resolvedPath = resolvePath(endpoint.path, pathParams);
  const curlCmd = buildCurlCommand(
    endpoint.method,
    resolvedPath,
    endpoint.method !== "GET" ? bodyText : null,
    headers
  );

  const copyUrl = async () => {
    const base = api.defaults.baseURL ?? "http://localhost:8000";
    await navigator.clipboard.writeText(`${base}${resolvedPath}`);
    toast("success", "URL copied");
  };

  const copyCurl = async () => {
    await navigator.clipboard.writeText(curlCmd);
    toast("success", "cURL copied");
  };

  const sendRequest = async () => {
    const bErr = validateBody(bodyText);
    if (bErr) { setBodyError(bErr); return; }
    setBodyError(null);

    abortRef.current?.abort();
    abortRef.current = new AbortController();

    setLoading(true);
    setResponse(null);
    setRespError(null);
    setStreamLines([]);

    const start = performance.now();

    // Streaming endpoint
    if (endpoint.streaming) {
      try {
        const base = api.defaults.baseURL ?? "http://localhost:8000";
        const res = await fetch(`${base}${resolvedPath}`, {
          method: endpoint.method,
          headers: { "Content-Type": "application/json", ...headers },
          body: endpoint.method !== "GET" ? bodyText : undefined,
          signal: abortRef.current.signal,
        });

        const reader = res.body?.getReader();
        const decoder = new TextDecoder();
        if (!reader) throw new Error("No body reader");

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value);
          const lines = chunk.split("\n").filter((l) => l.startsWith("data:"));
          setStreamLines((prev) => [...prev, ...lines.map((l) => l.slice(5).trim())]);
        }

        const elapsed = Math.round(performance.now() - start);
        if (mounted.current) {
          setResponse({ status: res.status, data: "(stream ended)", time: elapsed });
          addToHistory({ id: crypto.randomUUID(), path: endpoint.path, method: endpoint.method, status: res.status, latencyMs: elapsed, timestamp: new Date().toISOString() });
        }
      } catch (err: unknown) {
        if (mounted.current && err instanceof Error && err.name !== "AbortError") {
          setRespError(err.message ?? "Streaming error");
        }
      } finally {
        if (mounted.current) setLoading(false);
      }
      return;
    }

    // Regular request
    try {
      let body: unknown;
      if (endpoint.method !== "GET" && bodyText.trim()) body = JSON.parse(bodyText);

      const res = await api.request({
        method: endpoint.method.toLowerCase(),
        url: resolvedPath,
        data: body,
        headers,
        params: Object.keys(queryParams).length > 0 ? queryParams : undefined,
        signal: abortRef.current.signal,
        timeout: REQUEST_TIMEOUT_MS,
      });

      const elapsed = Math.round(performance.now() - start);
      if (mounted.current) {
        setResponse({ status: res.status, data: res.data, time: elapsed });
        addToHistory({ id: crypto.randomUUID(), path: endpoint.path, method: endpoint.method, status: res.status, latencyMs: elapsed, timestamp: new Date().toISOString() });
      }
    } catch (err: unknown) {
      if (mounted.current) {
        if (err && typeof err === "object" && "response" in err) {
          const axiosErr = err as { response: { status: number; data: unknown } };
          setResponse({
            status: axiosErr.response.status,
            data: axiosErr.response.data,
            time: Math.round(performance.now() - start),
          });
        } else if (err instanceof Error && err.name !== "AbortError") {
          setRespError(err.message ?? "Network error");
        }
      }
    } finally {
      if (mounted.current) setLoading(false);
    }
  };

  // Detect path params
  const paramMatches = [...endpoint.path.matchAll(/\{(\w+)\}/g)].map((m) => m[1]);

  return (
    <div className="flex flex-col h-full gap-4">
      {/* URL bar */}
      <div className="flex items-center gap-2 p-3 bg-surface-2 rounded-xl border border-surface-3">
        <MethodBadge method={endpoint.method} />
        <code className="flex-1 text-sm font-mono text-slate-200 truncate">{resolvedPath}</code>
        <button onClick={copyUrl} className="p-1.5 rounded hover:bg-surface-3 text-slate-500 hover:text-slate-300 transition-colors" title="Copy URL">
          <Copy size={13} />
        </button>
      </div>

      <div className="flex flex-col lg:flex-row gap-4 flex-1 min-h-0">
        {/* Left: Request config */}
        <div className="flex-1 min-h-0 flex flex-col">
          <Tabs defaultTab="body">
            <TabList>
              <Tab id="body">Body</Tab>
              {paramMatches.length > 0 && <Tab id="params">Path Params</Tab>}
              <Tab id="headers">Headers</Tab>
              <Tab id="curl">cURL</Tab>
            </TabList>
            <div className="flex-1 mt-3">
              <TabPanel id="body">
                <div className="flex flex-col gap-2">
                  <textarea
                    className={clsx(
                      "w-full h-52 font-mono text-xs bg-surface-1 border rounded-xl p-3 text-slate-300 resize-none focus:outline-none focus:ring-2 focus:ring-brand-500",
                      bodyError ? "border-danger-500" : "border-surface-3"
                    )}
                    value={bodyText}
                    onChange={(e) => { setBodyText(e.target.value); setBodyError(validateBody(e.target.value)); }}
                    placeholder="{}"
                    disabled={endpoint.method === "GET"}
                    spellCheck={false}
                  />
                  {bodyError && <span className="text-xs text-danger-400">{bodyError}</span>}
                </div>
              </TabPanel>
              <TabPanel id="params">
                <div className="flex flex-col gap-2">
                  {paramMatches.map((param) => (
                    <div key={param} className="flex items-center gap-2">
                      <span className="font-mono text-xs text-slate-400 w-28 flex-shrink-0">
                        {`{${param}}`}
                      </span>
                      <input
                        className="flex-1 h-8 font-mono text-xs bg-surface-1 border border-surface-3 rounded-lg px-2.5 text-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500"
                        value={pathParams[param] ?? ""}
                        onChange={(e) => setPathParams((p) => ({ ...p, [param]: e.target.value }))}
                        placeholder={`Enter ${param}`}
                      />
                    </div>
                  ))}
                </div>
              </TabPanel>
              <TabPanel id="headers">
                <KeyValueEditor
                  data={headers}
                  onChange={setHeaders}
                  placeholder={{ key: "X-Header", value: "value" }}
                />
              </TabPanel>
              <TabPanel id="curl">
                <CodeBlock code={curlCmd} language="bash" showCopy maxHeight="12rem" />
                <button
                  onClick={copyCurl}
                  className="mt-2 text-xs text-brand-400 hover:text-brand-300 transition-colors"
                >
                  Copy to clipboard
                </button>
              </TabPanel>
            </div>
          </Tabs>

          {/* Send button */}
          <div className="mt-3 flex gap-2">
            <button
              onClick={sendRequest}
              disabled={loading}
              className="flex-1 flex items-center justify-center gap-2 py-2.5 bg-brand-600 hover:bg-brand-500 disabled:opacity-60 text-white font-semibold text-sm rounded-xl transition-colors"
            >
              {loading ? <Loader2 size={15} className="animate-spin" /> : <Send size={15} />}
              {loading ? "Sending…" : "Send Request"}
            </button>
            {loading && (
              <button
                onClick={() => abortRef.current?.abort()}
                className="px-3 py-2.5 bg-surface-3 hover:bg-danger-900/40 text-danger-400 rounded-xl transition-colors"
              >
                <X size={16} />
              </button>
            )}
          </div>
        </div>

        {/* Right: Response */}
        <div className="flex-1 min-h-0 flex flex-col">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-widest mb-2">
            Response
          </div>
          <div className="flex-1 rounded-xl border border-surface-3 bg-surface-1 overflow-auto">
            {respError && (
              <div className="p-4 text-sm text-danger-400 font-mono">{respError}</div>
            )}
            {response && !endpoint.streaming && (
              <div className="flex flex-col h-full">
                <div className="flex items-center gap-3 px-4 py-2 border-b border-surface-3 bg-surface-2 flex-shrink-0">
                  <StatusPill status={response.status} />
                  <span className="text-xs text-slate-500">{response.time}ms</span>
                </div>
                <div className="flex-1 overflow-auto p-4">
                  <pre className="text-xs font-mono text-slate-300 whitespace-pre-wrap break-all">
                    {JSON.stringify(response.data, null, 2)}
                  </pre>
                </div>
              </div>
            )}
            {streamLines.length > 0 && (
              <div className="flex flex-col">
                {response && (
                  <div className="flex items-center gap-3 px-4 py-2 border-b border-surface-3 bg-surface-2 flex-shrink-0">
                    <StatusPill status={response.status} />
                    <span className="text-xs text-slate-500">{response.time}ms</span>
                    <span className="text-xs text-brand-400">{streamLines.length} events</span>
                  </div>
                )}
                <div className="p-4">
                  {streamLines.map((line, i) => (
                    <div key={i} className="font-mono text-xs text-success-300 py-0.5">
                      <span className="text-slate-600 mr-2">{i + 1}</span>{line}
                    </div>
                  ))}
                  {loading && (
                    <div className="flex items-center gap-1.5 text-xs text-brand-400 mt-2">
                      <Loader2 size={12} className="animate-spin" /> streaming…
                    </div>
                  )}
                </div>
              </div>
            )}
            {!response && !respError && !loading && streamLines.length === 0 && (
              <div className="flex items-center justify-center h-full text-slate-600 text-sm">
                No response yet
              </div>
            )}
            {loading && !streamLines.length && (
              <div className="flex items-center justify-center h-full">
                <Loader2 size={20} className="animate-spin text-brand-500" />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Mini key-value editor for headers
interface KVEditorProps {
  data: Record<string, string>;
  onChange: (data: Record<string, string>) => void;
  placeholder?: { key: string; value: string };
}

const KeyValueEditor: React.FC<KVEditorProps> = ({ data, onChange, placeholder }) => {
  const entries = Object.entries(data);

  const update = (idx: number, field: "key" | "value", val: string) => {
    const arr = [...entries];
    if (field === "key") arr[idx] = [val, arr[idx][1]];
    else arr[idx] = [arr[idx][0], val];
    onChange(Object.fromEntries(arr.filter(([k]) => k)));
  };

  const add = () => onChange({ ...data, "": "" });

  const remove = (idx: number) => {
    const arr = entries.filter((_, i) => i !== idx);
    onChange(Object.fromEntries(arr));
  };

  return (
    <div className="flex flex-col gap-2">
      {entries.map(([k, v], i) => (
        <div key={i} className="flex items-center gap-2">
          <input
            className="flex-1 h-7 font-mono text-xs bg-surface-1 border border-surface-3 rounded-lg px-2 text-slate-300 focus:outline-none focus:ring-1 focus:ring-brand-500"
            value={k}
            onChange={(e) => update(i, "key", e.target.value)}
            placeholder={placeholder?.key ?? "key"}
          />
          <input
            className="flex-1 h-7 font-mono text-xs bg-surface-1 border border-surface-3 rounded-lg px-2 text-slate-300 focus:outline-none focus:ring-1 focus:ring-brand-500"
            value={v}
            onChange={(e) => update(i, "value", e.target.value)}
            placeholder={placeholder?.value ?? "value"}
          />
          <button onClick={() => remove(i)} className="text-slate-600 hover:text-danger-400 transition-colors">
            <X size={14} />
          </button>
        </div>
      ))}
      <button
        onClick={add}
        className="text-xs text-brand-400 hover:text-brand-300 transition-colors text-left"
      >
        + Add header
      </button>
    </div>
  );
};
