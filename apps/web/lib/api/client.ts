import type { components } from "./schema";
export type Answer = components["schemas"]["Answer"];
export type Evidence = components["schemas"]["Evidence"];
export type Entity = components["schemas"]["Entity"];
export type Me = components["schemas"]["Me"];
export type Persona = "Engineer" | "Lead" | "Viewer";
export type Source = components["schemas"]["SourceMetadata"];
export type SourceList = components["schemas"]["SourceList"];
export type Revision = components["schemas"]["RevisionMetadata"];
export type Job = components["schemas"]["JobStatus"];
export type Review = components["schemas"]["ReviewDTO"];
export type HistoryItem = components["schemas"]["HistoryDTO"];
export interface PendingRun {
  id?: string;
  status: "queued" | "running" | "failed";
  stage?: string;
  error?: { message: string; code: string };
}
export async function api<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers);
  headers.set("x-brain-csrf", "1");
  if (options.body && !(options.body instanceof FormData))
    headers.set("content-type", "application/json");
  const result = await fetch("/api/v1" + path, {
    ...options,
    headers,
    cache: "no-store",
  });
  const body = await result.json();
  if (!result.ok)
    throw new Error(body.error?.message || "The request could not complete");
  return body as T;
}
export const post = <T>(path: string, body: unknown) =>
  api<T>(path, { method: "POST", body: JSON.stringify(body) });
