import axios from "axios";

export const BASE_URL = "http://localhost:8000";

export const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30_000,
  headers: { "Content-Type": "application/json" },
});

// Resolve path params like /patient/{id} → /patient/P001
export function resolvePath(
  path: string,
  pathParams: Record<string, string>
): string {
  return path.replace(/\{(\w+)\}/g, (_, key) => pathParams[key] ?? `{${key}}`);
}

// Generate a curl command string
export function buildCurlCommand(
  method: string,
  path: string,
  body: string | null,
  headers: Record<string, string> = {}
): string {
  const url = `${BASE_URL}${path}`;
  const headerFlags = Object.entries({
    "Content-Type": "application/json",
    ...headers,
  })
    .map(([k, v]) => `-H "${k}: ${v}"`)
    .join(" ");

  const bodyFlag =
    body && method !== "GET" ? `-d '${body.replace(/'/g, `'\\''`)}' ` : "";

  return `curl -X ${method.toUpperCase()} "${url}" ${headerFlags} ${bodyFlag}`.trim();
}
