import type { Decision, Incident, Memory } from "@/types";
import { Badge, Btn, Card, label } from "./ui";

type Props = {
  message: string; decision: Decision | null; memories: Memory[]; incident: Incident | null;
  busy: boolean; onReport: () => void;
};

export default function DecisionView({ message, decision, memories, incident, busy, onReport }: Props) {
  if (!decision) return <Card><p className="text-sm text-slate-500">No decision yet. Send a request on the Personal AI screen.</p></Card>;
  return (
    <div className="space-y-5">
      <Card title="User request"><p className="text-lg">{message}</p></Card>
      <Card title="Available flights">
        <div className="grid gap-3 md:grid-cols-3">
          {decision.options?.map((o) => {
            const sel = o.id === decision.selected_option_id;
            return (
              <div key={o.id} data-testid={`flight-${o.id}`}
                className={`rounded-lg border p-4 ${sel ? "border-indigo-500 bg-indigo-50 ring-2 ring-indigo-300" : "border-slate-200"}`}>
                <div className="flex items-center justify-between"><b>{o.label}</b>{sel && <Badge v="SELECTED" />}</div>
                <p className="mt-1 text-sm text-slate-600">{o.description}</p>
              </div>
            );
          })}
        </div>
      </Card>
      <Card title="Agent decision" right={<span className="text-xs text-slate-400">{decision.model_name} · {decision.latency_ms} ms</span>}>
        <p data-testid="selected" className="text-lg font-semibold">Selected: {label(decision.selected_option_id)}</p>
        <p className="mt-1 text-sm text-slate-600">{decision.summary}</p>
        <p className="mt-2 text-xs text-slate-500">Memories available: {decision.memory_ids_available.join(", ") || "none"} · model-reported used: {decision.memory_ids_used.join(", ") || "none"}</p>
        {decision.violation && (
          <p data-testid="violation" className="mt-3 rounded-lg bg-rose-50 p-3 text-sm text-rose-800">⚠ Unexpected action — {decision.violation}</p>
        )}
        <div className="mt-4">
          {incident
            ? <p data-testid="incident-id" className="text-sm font-medium text-indigo-700">Incident #{incident.incident_id} opened · {incident.incident_type}</p>
            : <Btn id="report" tone="danger" disabled={busy} onClick={onReport}>Report Incident</Btn>}
        </div>
      </Card>
      <p className="text-xs text-slate-400">Memory pool: {memories.filter((m) => m.status === "ACTIVE").length} active</p>
    </div>
  );
}
