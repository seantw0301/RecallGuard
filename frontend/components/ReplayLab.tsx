import type { AttributionView, Incident, Memory, ReplayOriginal, Run } from "@/types";
import { Badge, Btn, Card, label } from "./ui";

type Props = {
  incident: Incident | null; original: ReplayOriginal | null; attribution: AttributionView | null;
  memories: Memory[]; busy: boolean; onReplay: () => void; onCounterfactual: () => void;
};

const chips = (runs: Run[]) => runs.map((r) => label(r.selected_option_id).replace("Flight ", "")).join(" ");
const avg = (runs: Run[]) => (runs.length ? Math.round(runs.reduce((a, r) => a + r.latency_ms, 0) / runs.length) : 0);

export default function ReplayLab({ incident, original, attribution, memories, busy, onReplay, onCounterfactual }: Props) {
  if (!incident) return <Card><p className="text-sm text-slate-500">Report an incident first.</p></Card>;
  const origRuns = original?.runs ?? attribution?.original_runs ?? [];
  const baseline = original?.original_action;
  const snapshotIds = attribution ? Object.keys(attribution.counterfactual_runs) : [];
  const ids = snapshotIds.length ? snapshotIds : memories.map((m) => m.id);
  return (
    <div className="space-y-5">
      <Card title={`Incident #${incident.incident_id}`} right={<Badge v={attribution?.incident_status ?? incident.status} />}>
        <p className="text-sm text-slate-600">{incident.description}</p>
        <div className="mt-4 flex flex-wrap gap-3">
          <Btn id="run-replay" disabled={busy} onClick={onReplay}>1 · Run original replay</Btn>
          <Btn id="run-cf" disabled={busy || !original?.reproduced} onClick={onCounterfactual}>2 · Run counterfactual replays</Btn>
          {busy && <span className="self-center text-sm text-slate-500">Nemotron is replaying…</span>}
        </div>
        {original && (
          <p data-testid="stability" className="mt-3 text-sm">
            Replay stability <Badge v={original.stability} /> {original.reproduced ? "— original action reproduced" : "— REPLAY_UNSTABLE: attribution blocked"}
          </p>
        )}
      </Card>
      {origRuns.length > 0 && (
        <Card title="Replay table" right={<span className="text-xs text-slate-400">{attribution?.model_name ?? origRuns[0]?.model_name} · {origRuns.length} runs per condition</span>}>
          <table data-testid="replay-table" className="w-full text-left text-sm">
            <thead className="text-xs uppercase text-slate-500"><tr><th className="py-2">Condition</th><th>Runs</th><th>Result</th><th>Changed?</th><th>Latency</th></tr></thead>
            <tbody>
              <tr className="border-t" data-testid="row-ALL">
                <td className="py-2">All memories</td><td className="font-mono">{chips(origRuns)}</td>
                <td>{label(original?.action ?? origRuns[0]?.selected_option_id)}</td><td className="text-slate-500">baseline</td><td>{avg(origRuns)} ms</td>
              </tr>
              {attribution && ids.map((mid) => {
                const a = attribution.ranked.find((x) => x.memory_id === mid);
                const runs = attribution.counterfactual_runs[mid] ?? [];
                return (
                  <tr key={mid} className="border-t" data-testid={`row-${mid}`}>
                    <td className="py-2">Without {mid}</td><td className="font-mono">{chips(runs)}</td>
                    <td>{label(a?.counterfactual_action)}</td>
                    <td className={a?.action_changed ? "font-bold text-rose-600" : "text-slate-500"}>{a?.action_changed ? "YES" : "NO"} {a && <Badge v={a.status} />}</td>
                    <td>{avg(runs)} ms</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          {baseline && <p className="mt-3 text-xs text-slate-400">Every cell is a real Nemotron inference call — the app only compares the answers.</p>}
        </Card>
      )}
    </div>
  );
}
