import type { AttributionView, Incident, Memory, Verify } from "@/types";
import { Badge, Btn, Card, label } from "./ui";

type Props = {
  incident: Incident | null; attribution: AttributionView | null; memories: Memory[]; verify: Verify | null;
  busy: boolean; onQuarantine: (id: string) => void; onRestore: (id: string) => void; onVerify: () => void;
};

export default function MemoryReview({ incident, attribution, memories, verify, busy, onQuarantine, onRestore, onVerify }: Props) {
  if (!incident || !attribution?.ranked.length)
    return <Card><p className="text-sm text-slate-500">Run the counterfactual replays to rank memory influence.</p></Card>;
  const anyQuarantined = memories.some((m) => m.status === "QUARANTINED");
  return (
    <div className="space-y-5">
      {attribution.ranked.map((a) => {
        const m = memories.find((x) => x.id === a.memory_id);
        if (!m) return null;
        return (
          <Card key={a.memory_id}>
            <div data-testid={`review-${a.memory_id}`} className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p className="font-mono text-xs text-slate-500">{m.id}</p>
                <p className="text-lg">“{m.content}”</p>
                <p className="mt-1 text-sm text-slate-600">
                  Influence <Badge v={a.influence} /> · Counterfactual score <b data-testid={`score-${a.memory_id}`}>{a.attribution_score.toFixed(2)}</b> ({a.changed_runs}/{a.total_runs} runs changed the action) · <Badge v={m.status} />
                </p>
              </div>
              {m.status === "ACTIVE" && a.influence !== "LOW" && <Btn id={`quarantine-${a.memory_id}`} tone="danger" disabled={busy} onClick={() => onQuarantine(m.id)}>Quarantine</Btn>}
              {m.status === "QUARANTINED" && <Btn tone="ghost" disabled={busy} onClick={() => onRestore(m.id)}>Restore</Btn>}
            </div>
          </Card>
        );
      })}
      {anyQuarantined && (
        <Card title="Verify the fix">
          <Btn id="verify" disabled={busy} onClick={onVerify}>{busy ? "Nemotron is deciding…" : "Run the same task again"}</Btn>
          {verify && (
            <div data-testid="verify-result" className="mt-4 rounded-lg bg-emerald-50 p-4 text-sm text-emerald-900">
              <p className="text-lg font-semibold">{label(verify.original_action)} → {label(verify.decision.selected_option_id)} {verify.changed ? "· behavior changed ✓" : "· unchanged"}</p>
              <p className="mt-1">Memories used this time: {verify.decision.memory_ids_available.join(", ")} · incident {verify.incident_status}</p>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}
