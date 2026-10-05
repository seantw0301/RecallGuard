async function call<T>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch(path, { ...init, headers: { "Content-Type": "application/json" } });
  if (!r.ok) throw new Error(`${r.status} ${(await r.text()).slice(0, 200)}`);
  return r.json();
}
const post = <T,>(p: string, body?: unknown) => call<T>(p, { method: "POST", body: body ? JSON.stringify(body) : undefined });

import type { AttributionView, Decision, Incident, Memory, ReplayOriginal, Verify } from "@/types";

export const api = {
  reset: () => post<{ session2: string; demo_request: string }>("/api/demo/reset"),
  memories: () => call<Memory[]>("/api/memories"),
  addMemory: (content: string) => post<Memory>("/api/memory", { content }),
  decide: (session_id: string, message: string) => post<Decision>("/api/agent/decide", { session_id, message }),
  report: (decision_id: string) => post<Incident>("/api/incidents", { decision_id }),
  replay: (id: string) => post<ReplayOriginal>(`/api/incidents/${id}/replay`),
  counterfactual: (id: string) => post<unknown>(`/api/incidents/${id}/counterfactual`),
  attribution: (id: string) => call<AttributionView>(`/api/incidents/${id}/attribution`),
  quarantine: (id: string) => post<Memory>(`/api/memories/${id}/quarantine`),
  restore: (id: string) => post<Memory>(`/api/memories/${id}/restore`),
  verify: (id: string) => post<Verify>(`/api/incidents/${id}/verify`),
};
