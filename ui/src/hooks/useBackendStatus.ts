import { useState, useEffect, useCallback, useRef } from "react";
import { BASE_URL } from "../lib/api";

export interface BackendStatus {
  connected: boolean;
  latencyMs: number | null;
  lastChecked: Date | null;
  checking: boolean;
}

export function useBackendStatus(intervalMs = 5000): BackendStatus {
  const [status, setStatus] = useState<BackendStatus>({
    connected: false,
    latencyMs: null,
    lastChecked: null,
    checking: false,
  });
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const check = useCallback(async () => {
    setStatus((s) => ({ ...s, checking: true }));
    const start = performance.now();
    try {
      const res = await fetch(`${BASE_URL}/health`, {
        signal: AbortSignal.timeout(4000),
      });
      const latencyMs = Math.round(performance.now() - start);
      setStatus({
        connected: res.ok,
        latencyMs,
        lastChecked: new Date(),
        checking: false,
      });
    } catch {
      setStatus({
        connected: false,
        latencyMs: null,
        lastChecked: new Date(),
        checking: false,
      });
    }
  }, []);

  useEffect(() => {
    check();
    timerRef.current = setInterval(check, intervalMs);
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [check, intervalMs]);

  return status;
}
